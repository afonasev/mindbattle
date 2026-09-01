import type { DifficultyFeedbackEvent, DifficultyFeedbackSink } from "./types";

export class HttpDifficultyFeedbackSink implements DifficultyFeedbackSink {
  constructor(private readonly endpoint = "/api/difficulty-feedback") {}

  async submit(event: DifficultyFeedbackEvent): Promise<void> {
    let response: Response;
    try {
      response = await fetch(this.endpoint, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify(event)
      });
    } catch {
      throw new Error("Не удалось связаться с локальным сервером");
    }
    if (!response.ok) {
      const body = await response.json().catch(() => null) as { readonly error?: string } | null;
      throw new Error(body?.error ?? `Сервер отклонил оценку (${response.status})`);
    }
  }
}
