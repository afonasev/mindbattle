import { randomBytes, randomInt } from "node:crypto";
import type { IncomingMessage, ServerResponse } from "node:http";
import { NetworkRoom, RoomError } from "../src/network/room";
import { CatalogDomainContext } from "../src/application/contentContext";
import { catalog } from "../src/content/catalog";
import { EMPTY_QUESTION_HISTORY } from "../src/content/scheduler";
import type { DifficultyFeedbackEventV3 } from "../src/feedback/types";
import type { CommandEnvelope } from "../src/network/protocol";
export function createNetworkApi(
  submit: (event: DifficultyFeedbackEventV3) => Promise<void>,
) {
  const rooms = new Map<string, NetworkRoom>();
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
        streams.delete(room);
        rooms.delete(room.code);
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
        if (path === "create") {
          if (rooms.size >= 32)
            throw new RoomError("Сервер занят. Попробуйте позже.", 503);
          let code: string;
          do {
            code = String(randomInt(10000)).padStart(4, "0");
          } while (rooms.has(code));
          const room = new NetworkRoom(
            code,
            secret(),
            new CatalogDomainContext(catalog, EMPTY_QUESTION_HISTORY),
            Object.fromEntries(catalog.topics.map((t) => [t.id, t.title])),
            secret,
            submit,
            () => broadcast(room),
          );
          room.display.lastSeen = now();
          rooms.set(code, room);
          json(res, 201, { code, token: room.organizerToken, role: "display" });
        } else {
          if (
            typeof data.code !== "string" ||
            !/^\d{4}$/.test(data.code) ||
            typeof data.name !== "string"
          )
            throw new RoomError("Введите четыре цифры кода и имя");
          const room = rooms.get(data.code);
          if (!room) throw new RoomError("Комната не найдена", 404);
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
