import type { ResultSink } from '../src/statistics/events';
import { randomBytes, scrypt, timingSafeEqual } from "node:crypto";
import type { IncomingMessage, ServerResponse } from "node:http";
import { NetworkRoom, RoomError } from "../src/network/room";
import { CatalogDomainContext } from "../src/application/contentContext";
import { catalog } from "../src/content/catalog";
import { EMPTY_QUESTION_HISTORY } from "../src/content/scheduler";
import type { DifficultyFeedbackEventV3 } from "../src/feedback/types";
import type { CommandEnvelope, LobbyRoom } from "../src/network/protocol";
import { promisify } from "node:util";
const deriveKey = promisify(scrypt);
export function createNetworkApi(
  submit: (event: DifficultyFeedbackEventV3) => Promise<void>,
  results?: ResultSink,
) {
  const rooms = new Map<string, NetworkRoom>();
  const passwords = new Map<NetworkRoom, { salt: Buffer; hash: Buffer }>();
  let hashing = 0;
  const hashPassword = async (password: string, salt: Buffer) => {
    if (hashing >= 16) throw new RoomError("Сервер занят. Попробуйте позже.", 503);
    hashing++;
    try { return await deriveKey(password, salt, 32) as Buffer; }
    finally { hashing--; }
  };
  const passwordInput = (value: unknown) => {
    if (value === undefined) return "";
    if (typeof value !== "string" || value.length > 128)
      throw new RoomError("Пароль должен содержать не более 128 символов");
    return value;
  };
  const streams = new Map<
    NetworkRoom,
    Set<{ token: string; response: ServerResponse; generation: number }>
  >();
  const limits = new Map<string, { time: number; count: number }>();
  const now = () => performance.now();
  const secret = () => randomBytes(24).toString("hex");
  const broadcast = (room: NetworkRoom) => {
    for (const stream of streams.get(room) ?? []) {
      try {
        if (stream.response.writableLength > 262144) {
          stream.response.destroy();
          continue;
        }
        stream.response.write(
          `data: ${JSON.stringify(room.snapshot(stream.token, now()))}\n\n`,
        );
      } catch {
        stream.response.write("event: expired\ndata: {}\n\n");
        stream.response.end();
      }
    }
  };
  const timer = setInterval(() => {
    for (const room of rooms.values()) {
      room.tick(now());
      broadcast(room);
      if (
        room.closed ||
        (!room.display.connected &&
          !room.players.some((p) => p.connected) &&
          now() -
            Math.max(
              room.display.lastSeen,
              ...room.players.map((p) => p.lastSeen),
            ) >
            86400000)
      ) {
        for (const stream of streams.get(room) ?? []) stream.response.end();
        room.interruptResults("expired");
        streams.delete(room);
        rooms.delete(room.code);
        passwords.delete(room);
      }
    }
    for (const [key, value] of limits)
      if (now() - value.time > 60000) limits.delete(key);
  }, 250);
  timer.unref();
  const json = (res: ServerResponse, status: number, value: unknown) => {
    res.writeHead(status, {
      "content-type": "application/json",
      "cache-control": "no-store",
    });
    res.end(JSON.stringify(value));
  };
  const body = async (req: IncomingMessage) => {
    const chunks: Buffer[] = [];
    let size = 0;
    for await (const chunk of req) {
      const bytes = Buffer.from(chunk);
      chunks.push(bytes);
      size += bytes.length;
      if (size > 8192) throw new RoomError("Запрос слишком большой", 413);
    }
    try {
      return JSON.parse(Buffer.concat(chunks).toString("utf8"));
    } catch {
      throw new RoomError("Некорректный JSON");
    }
  };
  return async function handle(
    req: IncomingMessage,
    res: ServerResponse,
  ): Promise<boolean> {
    const url = new URL(req.url ?? "/", "http://local");
    if (!url.pathname.startsWith("/api/network/")) return false;
    try {
      if (
        req.headers.origin &&
        new URL(req.headers.origin).host !== req.headers.host
      )
        throw new RoomError("Другой origin запрещён", 403);
      const path = url.pathname.slice("/api/network/".length);
      if (path === "catalog" && req.method === "POST") {
        const data = await body(req);
        const credentials = data?.credentials ?? [];
        if (!Array.isArray(credentials) || credentials.length > 20)
          throw new RoomError("Некорректный список сохранённых игр");
        const ownRooms: LobbyRoom[] = [];
        const invalidIndexes: number[] = [];
        for (const [index, credential] of credentials.entries()) {
          try {
            if (!credential || typeof credential.code !== "string" || typeof credential.token !== "string" || credential.token.length > 128)
              throw new RoomError("Некорректный доступ", 403);
            const room = rooms.get(credential.code);
            if (!room) throw new RoomError("Комната закрыта", 404);
            const summary = room.lobbySummary(credential.token);
            if (!ownRooms.some(r => r.code === summary.code && r.role === summary.role)) ownRooms.push(summary);
          } catch { invalidIndexes.push(index); }
        }
        json(res, 200, {
          rooms: [...rooms.values()].filter(room => !room.closed && !room.state).map(room => {
            const { leaderName: _leader, ...summary } = room.lobbySummary();
            return summary;
          }), ownRooms, invalidIndexes,
        });
        return true;
      }
      if (path === "room" && req.method === "GET") {
        const room = rooms.get(url.searchParams.get("code") ?? "");
        if (!room) throw new RoomError("Комната не найдена", 404);
        json(res, 200, room.lobbySummary());
        return true;
      }
      if (req.method === "POST" && (path === "create" || path === "join")) {
        const remote = req.socket.remoteAddress ?? "unknown";
        // Only our loopback Caddy connection may assert the public client IP.
        const forwarded = req.headers["x-forwarded-for"];
        const key =
          ["127.0.0.1", "::1", "::ffff:127.0.0.1"].includes(remote) &&
          typeof forwarded === "string"
            ? forwarded.split(",").at(-1)!.trim()
            : remote;
        const limit = limits.get(key) ?? { time: now(), count: 0 };
        limit.count++;
        limits.set(key, limit);
        if (limit.count > 60)
          throw new RoomError("Слишком много попыток. Подождите минуту.", 429);
        const data = await body(req);
        if (!data || typeof data !== "object") throw new RoomError("Некорректный запрос");
        if (path === "create") {
          if (rooms.size >= 32)
            throw new RoomError("Сервер занят. Попробуйте позже.", 503);
          if (typeof data.title !== "string") throw new RoomError("Введите название игры");
          const title = data.title.trim();
          if (!title || [...title].length > 60 || /[\p{Cc}\p{Cf}]/u.test(title))
            throw new RoomError("Название должно содержать от 1 до 60 символов");
          if (data.collectStatistics !== undefined && typeof data.collectStatistics !== "boolean") throw new RoomError("Некорректная настройка статистики");
          if ([data.statisticsRevision, data.statisticsGeneration].some(value => value !== undefined && (!Number.isSafeInteger(value) || value < 0))) throw new RoomError("Некорректная версия настройки статистики");
          const password = passwordInput(data.password);
          const salt = randomBytes(16);
          const hash = password ? await hashPassword(password, salt) : undefined;
          if (rooms.size >= 32) throw new RoomError("Сервер занят. Попробуйте позже.", 503);
          let code: string;
          do { code = randomBytes(8).toString("hex"); } while (rooms.has(code));
          const room = new NetworkRoom(
            code,
            secret(),
            new CatalogDomainContext(catalog, EMPTY_QUESTION_HISTORY),
            Object.fromEntries(catalog.topics.map((t) => [t.id, t.title])),
            secret,
            submit,
            () => broadcast(room),
            results,
            title,
            !!hash,
            data.collectStatistics ?? true,
            undefined, data.statisticsRevision ?? 0, data.statisticsGeneration ?? 0,
          );
          room.display.lastSeen = now();
          rooms.set(code, room);
          if (hash) passwords.set(room, { salt, hash });
          json(res, 201, { code, token: room.organizerToken, role: "display" });
        } else {
          if (
            typeof data.code !== "string" ||
            data.code.length > 64 ||
            typeof data.name !== "string"
          )
            throw new RoomError("Выберите игру и введите имя");
          const room = rooms.get(data.code);
          if (!room) throw new RoomError("Комната не найдена", 404);
          room.lobbySummary();
          if ([data.statisticsRevision, data.statisticsGeneration].some(value => value !== undefined && (!Number.isSafeInteger(value) || value < 0))) throw new RoomError("Некорректная версия настройки статистики");
          const password = passwordInput(data.password);
          const protection = passwords.get(room);
          if (protection && !timingSafeEqual(await hashPassword(password, protection.salt), protection.hash))
            throw new RoomError("Неверный пароль игры", 403);
          if (rooms.get(data.code) !== room) throw new RoomError("Комната закрыта", 404);
          const seat = room.join(data.name, now());
          json(res, 201, {
            code: room.code,
            token: seat.token,
            role: "player",
          });
        }
        return true;
      }
      const code = url.searchParams.get("code") ?? "";
      const room = rooms.get(code);
      if (!room) throw new RoomError("Комната не найдена или уже закрыта", 404);
      const auth = req.headers.authorization ?? "";
      const token = auth.startsWith("Bearer ") ? auth.slice(7) : "";
      room.snapshot(token, now());
      if (path === "stream" && req.method === "GET") {
        const generation = room.connect(token, now());
        res.writeHead(200, {
          "content-type": "text/event-stream",
          "cache-control": "no-store",
          connection: "keep-alive",
          "x-accel-buffering": "no",
        });
        const set = streams.get(room) ?? new Set();
        for (const previous of set) {
          if (previous.token === token) {
            previous.response.write("event: replaced\ndata: {}\n\n");
            previous.response.end();
            set.delete(previous);
          }
        }
        const stream = { token, response: res, generation };
        set.add(stream);
        streams.set(room, set);
        res.write(
          `event: connected\ndata: ${JSON.stringify({ generation })}\n\n`,
        );
        res.write(`data: ${JSON.stringify(room.snapshot(token, now()))}\n\n`);
        res.on("close", () => {
          set.delete(stream);
          if (set.size === 0) streams.delete(room);
          room.disconnect(token, generation, now());
        });
        return true;
      }
      if (path === "heartbeat" && req.method === "POST") {
        const data = await body(req);
        room.heartbeat(token, data.generation, now());
        json(res, 200, {});
        return true;
      }
      if (path === "statistics" && req.method === "POST") {
        const data = await body(req);
        await room.setStatistics(token, data?.enabled, data?.revision, data?.generation);
        json(res, 200, {});
        return true;
      }
      if (path === "command" && req.method === "POST") {
        room.command(token, (await body(req)) as CommandEnvelope, now());
        json(
          res,
          200,
          room.closed ? { closed: true } : room.snapshot(token, now()),
        );
        return true;
      }
      throw new RoomError("Неизвестный сетевой запрос", 404);
    } catch (error) {
      json(res, error instanceof RoomError ? error.status : 500, {
        error: error instanceof Error ? error.message : "Ошибка сервера",
      });
      return true;
    }
  };
}
