import { describe, expect, it } from "vitest";
import { phoneStatus } from "../../src/ui/networkStatus";
import type { NetworkSnapshot } from "../../src/network/protocol";
const base = { role: "player", paused: false, isLeader: false, titles: { topic: "Тестовая тема" }, leaderName: "Анна", chooserName: "Иван" } as unknown as NetworkSnapshot;
describe("phone action status", () => {
  it("distinguishes choosing and waiting", () => {
    expect(phoneStatus({ ...base, phase: "normal-topic", canChoose: true })?.required).toBe(true);
    expect(phoneStatus({ ...base, phase: "normal-topic", canChoose: false })).toEqual({ required: false, text: "Выбирает Иван. Вы ждёте" });
  });
  it("confirms own veto and keeps replacement visible", () => {
    expect(phoneStatus({ ...base, phase: "bonus-veto", canVeto: true })?.required).toBe(true);
    const chosen = phoneStatus({ ...base, phase: "bonus-veto", canVeto: true, ownVeto: "topic" });
    expect(chosen?.required).toBe(false);
    expect(chosen?.text).toContain("Тестовая тема");
    expect(chosen?.text).toContain("заменить или снять");
    expect(phoneStatus({ ...base, phase: "bonus-veto", canVeto: false })?.text).toBe("Другие игроки исключают темы. Вы ждёте");
  });
  it("distinguishes unanswered, answered, timed out and spectator", () => {
    expect(phoneStatus({ ...base, phase: "answering", canAnswer: true })?.required).toBe(true);
    expect(phoneStatus({ ...base, phase: "answering", canAnswer: true, ownAnswer: "up" })?.text).toContain("можно изменить");
    expect(phoneStatus({ ...base, phase: "answering", canAnswer: false })?.text).toContain("истекло");
    expect(phoneStatus({ ...base, phase: "answering", spectating: true })?.text).toContain("наблюдаете");
  });
  it("updates leader authority on transitions and hides status during pause", () => {
    for (const phase of ["reveal", "standings", "finished", "difficulty-feedback"] as const) {
      expect(phoneStatus({ ...base, phase, isLeader: true })?.required).toBe(true);
      expect(phoneStatus({ ...base, phase })?.required).toBe(false);
    }
    expect(phoneStatus({ ...base, phase: "reveal", paused: true })).toBeNull();
    expect(phoneStatus({ ...base, phase: "reveal", role: "display" })).toBeNull();
  });
});
