import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import { SoloFeedbackScreen, SoloScreen } from "../../src/ui/soloUi";
import type { SoloRecord } from "../../src/adapters/storage";
import type { SoloState } from "../../src/domain/solo";

function record(index: number): SoloRecord {
  return { id: `top-${index}`, name: `Игрок ${index}`, score: 1_200 - index * 100, savedAt: `2026-09-05T${String(index).padStart(2, "0")}:00:00.000Z` };
}

describe("SoloScreen results", () => {
  it("keeps the current result visible with its full-table rank outside top-10", () => {
    const records = [...Array.from({ length: 11 }, (_, index) => record(index)), { id: "current", name: "Текущий", score: -100, savedAt: "2026-09-05T12:00:00.000Z" }];
    const html = renderToStaticMarkup(createElement(SoloScreen, {
      state: { phase: { kind: "finished" }, score: -100 } as SoloState,
      question: undefined,
      titleById: {},
      records,
      savedRecordId: "current",
      inputKind: "pointer" as const,
      command: () => undefined,
      finish: () => undefined,
      exit: () => undefined
    }));
    expect(html).toContain("Ваше место: 12");
    expect(html).toContain("-100 очков");
  });
});

describe("Solo question and feedback difficulty", () => {
  const round = {
    questionId: "question",
    topicId: "topic",
    difficulty: "medium" as const,
    risk: false,
    answerOrder: ["answer-0", "answer-1", "answer-2", "answer-3"] as const,
    correctPosition: "up" as const,
    points: 200
  };
  const question = {
    id: "question",
    topicId: "topic",
    difficulty: "medium" as const,
    prompt: "Проверочный вопрос?",
    answers: ["Первый", "Второй", "Третий", "Четвёртый"] as const,
    correctAnswerId: "answer-0",
    correctIndex: 0 as const,
    explanation: "Пояснение",
    source: { title: "Источник", url: "https://example.com/source", verifiedAt: "2026-09-05" }
  };

  it("shows medium difficulty after the solo question counter", () => {
    const html = renderToStaticMarkup(createElement(SoloScreen, {
      state: { slotIndex: 5, score: 0, lives: 3, reserveMs: 60_000, paused: false, phase: { kind: "answering", round, baseRemainingMs: 10_000, answer: null } } as SoloState,
      question,
      titleById: { topic: "Тема" },
      records: [],
      savedRecordId: null,
      inputKind: "pointer" as const,
      command: () => undefined,
      finish: () => undefined,
      exit: () => undefined
    }));

    expect(html).toContain("Вопрос 6 (Средний)");
  });

  it("shows hard difficulty on the solo feedback screen", () => {
    const html = renderToStaticMarkup(createElement(SoloFeedbackScreen, {
      value: { kind: "feedback", round: { ...round, difficulty: "hard" }, result: "correct", eventId: "feedback-1", hasComplaint: null, feedbackCursor: 1, complaintReasons: [], complaintNote: "" },
      choose: () => undefined,
      toggleReason: () => undefined,
      setNote: () => undefined,
      submit: () => undefined,
      pending: false,
      error: null
    }));

    expect(html).toContain("Сложность: Сложный");
  });
});
