import type {
  Credential,
  NetworkSnapshot,
  NetworkAction,
  CommandEnvelope,
} from "./protocol";
const key = "mindbattle-network-credentials-v1";
export function savedCredential(
  code?: string,
  role?: Credential["role"],
): Credential | null {
  try {
    const list = JSON.parse(localStorage.getItem(key) ?? "[]") as Credential[];
    return (
      list.find(
        (c) => (!code || c.code === code) && (!role || c.role === role),
      ) ?? null
    );
  } catch {
    return null;
  }
}
export function saveCredential(value: Credential) {
  let list: Credential[] = [];
  try {
    list = JSON.parse(localStorage.getItem(key) ?? "[]");
  } catch {
    /* empty */
  }
  localStorage.setItem(
    key,
    JSON.stringify(
      [
        value,
        ...list.filter((c) => c.code !== value.code || c.role !== value.role),
      ].slice(0, 20),
    ),
  );
}
export function forgetCredential(value: Credential) {
  try {
    const list = JSON.parse(localStorage.getItem(key) ?? "[]") as Credential[];
    localStorage.setItem(
      key,
      JSON.stringify(list.filter((c) => c.token !== value.token)),
    );
  } catch {
    /* empty */
  }
}
export async function networkRequest<T>(
  path: string,
  body: unknown,
  credential?: Credential,
  signal?: AbortSignal,
): Promise<T> {
  const response = await fetch(
    `/api/network/${path}${credential ? `?code=${credential.code}` : ""}`,
    {
      method: "POST",
      headers: {
        "content-type": "application/json",
        ...(credential ? { authorization: `Bearer ${credential.token}` } : {}),
      },
      body: JSON.stringify(body),
      signal,
    },
  );
  const value = await response.json();
  if (!response.ok) throw new Error(value.error ?? "Ошибка соединения");
  return value as T;
}
export class NetworkConnection {
  private abort = new AbortController();
  private generation = 0;
  private heartbeat?: ReturnType<typeof setInterval>;
  private streamAbort: AbortController | null = null;
  private latestAt = 0;
  constructor(
    readonly credential: Credential,
    private update: (snapshot: NetworkSnapshot) => void,
    private status: (message: string, terminal?: boolean) => void,
  ) {
    void this.run();
  }
  private async run() {
    this.heartbeat = setInterval(() => {
      if (this.generation)
        void networkRequest(
          "heartbeat",
          { generation: this.generation },
          this.credential,
          this.abort.signal,
        ).catch(() => {});
      if (this.latestAt && Date.now() - this.latestAt > 7000) {
        this.status("Связь потеряна. Восстанавливаем подключение…");
        this.streamAbort?.abort();
      }
    }, 2000);
    while (!this.abort.signal.aborted) {
      this.streamAbort = new AbortController();
      const streamAbort = this.streamAbort;
      const cancel = () => streamAbort.abort();
      this.abort.signal.addEventListener("abort", cancel, { once: true });
      try {
        const response = await fetch(
          `/api/network/stream?code=${this.credential.code}`,
          {
            headers: { authorization: `Bearer ${this.credential.token}` },
            signal: streamAbort.signal,
            cache: "no-store",
          },
        );
        if (!response.ok) {
          const data = await response.json();
          if ([403, 404, 410].includes(response.status)) {
            this.status(data.error, true);
            break;
          }
          throw new Error(data.error);
        }
        if (!response.body) throw new Error("Поток недоступен");
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = "";
        this.latestAt = Date.now();
        while (!streamAbort.signal.aborted) {
          const { value, done } = await reader.read();
          if (done) break;
          buffer += decoder.decode(value, { stream: true });
          let boundary: number;
          while ((boundary = buffer.indexOf("\n\n")) >= 0) {
            const event = buffer.slice(0, boundary);
            buffer = buffer.slice(boundary + 2);
            this.latestAt = Date.now();
            if (event.includes("event: replaced")) {
              this.status(
                "Игра открыта в другой вкладке этого устройства",
                true,
              );
              this.close();
              return;
            }
            if (event.includes("event: expired")) {
              this.status("Комната закрыта или вы исключены", true);
              this.close();
              return;
            }
            const data = event
              .split("\n")
              .find((line) => line.startsWith("data: "))
              ?.slice(6);
            if (!data) continue;
            if (event.includes("event: connected")) {
              this.generation = JSON.parse(data).generation;
              continue;
            }
            const snapshot = JSON.parse(data) as NetworkSnapshot;
            const connected =
              snapshot.role === "display"
                ? snapshot.displayConnected
                : snapshot.players.find((p) => p.id === snapshot.selfId)
                    ?.connected;
            if (!connected) {
              this.status("Связь потеряна. Восстанавливаем подключение…");
              streamAbort.abort();
              break;
            }
            this.update(snapshot);
            this.status("");
          }
        }
      } catch {
        if (!this.abort.signal.aborted)
          this.status("Связь потеряна. Восстанавливаем подключение…");
      } finally {
        this.abort.signal.removeEventListener("abort", cancel);
        streamAbort.abort();
        this.generation = 0;
      }
      if (!this.abort.signal.aborted)
        await new Promise<void>((resolve) => {
          const done = () => {
            clearTimeout(timer);
            this.abort.signal.removeEventListener("abort", done);
            resolve();
          };
          const timer = setTimeout(done, 1000);
          this.abort.signal.addEventListener("abort", done, { once: true });
        });
    }
    if (this.heartbeat) clearInterval(this.heartbeat);
  }
  async command(snapshot: NetworkSnapshot, action: NetworkAction) {
    const envelope: CommandEnvelope = {
      commandId: typeof crypto.randomUUID === "function" ? crypto.randomUUID() : Array.from(crypto.getRandomValues(new Uint32Array(4)), value => value.toString(16).padStart(8,"0")).join(""),
      epoch: snapshot.epoch,
      phaseRevision: snapshot.phaseRevision,
      action,
    };
    return networkRequest<NetworkSnapshot>(
      "command",
      envelope,
      this.credential,
      this.abort.signal,
    );
  }
  close() {
    this.abort.abort();
    this.streamAbort?.abort();
    if (this.heartbeat) clearInterval(this.heartbeat);
  }
}
