import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import type { MatchState, PublicMatchView } from "../../src/domain";
import { DifficultyFeedbackScreen, QuestionBoard } from "../../src/ui/gameUi";

const state = {
  phase: {
    kind: "reveal",
    round: { mode: "main", difficulty: "easy" }
  },
  mainQuestionIndex: 0,
  config: { questionCount: 9 },
  tieBreak: null
} as unknown as MatchState;

function view(notes: NonNullable<PublicMatchView["question"]>["wrongAnswerNotes"]): PublicMatchView {
  return {
    phase: "reveal",
    paused: false,
    teams: [],
    question: {
      id: "question",
      topicId: "topic",
      prompt: "Проверочный вопрос?",
      options: { up: "Верный", right: "Первый", down: "Второй", left: "Третий" },
      explanation: ["Основное объяснение."],
      source: { title: "Проверочный источник", url: "https://example.com/source" },
      correctPosition: "up",
      wrongAnswerNotes: notes
    }
  };
}

describe("QuestionBoard wrong-answer notes", () => {
  it("shows the assigned difficulty in the team question header", () => {
    const html = renderToStaticMarkup(createElement(QuestionBoard, {
      state,
      view: view([]),
      assignments: [],
      titleById: { topic: "Тема" }
    }));

    expect(html).toContain("Вопрос 1 / 9 (Лёгкий)");
  });

  it("renders the source immediately after the explanation and selected notes below it", () => {
    const html = renderToStaticMarkup(createElement(QuestionBoard, {
      state,
      view: view([
        { position: "right", answer: "Первый", note: "Справка о первом." },
        { position: "left", answer: "Третий", note: "Справка о третьем." }
      ]),
      assignments: [],
      titleById: { topic: "Тема" }
    }));

    expect(html.match(/Справка о первом\./gu)).toHaveLength(1);
    expect(html.match(/Справка о третьем\./gu)).toHaveLength(1);
    expect(html).not.toContain("Справка о втором.");
    expect(html.indexOf("Основное объяснение.")).toBeLessThan(html.indexOf("Источник: Проверочный источник"));
    expect(html.indexOf("Источник: Проверочный источник")).toBeLessThan(html.indexOf("Справка о первом."));
  });

  it("omits the notes section when nobody selected a distractor", () => {
    const html = renderToStaticMarkup(createElement(QuestionBoard, {
      state,
      view: view([]),
      assignments: [],
      titleById: { topic: "Тема" }
    }));
    expect(html).not.toContain("Справки о выбранных неправильных ответах");
    expect(html).toContain("Источник: Проверочный источник");
  });
});

describe("DifficultyFeedbackScreen", () => {
  it("keeps the hard-question context visible during feedback", () => {
    const html = renderToStaticMarkup(createElement(DifficultyFeedbackScreen, {
      feedback: {
        eventId: "feedback-1",
        questionId: "question",
        assignedDifficulty: "hard",
        stage: "choice",
        hasComplaint: null,
        complaintReasons: [],
        complaintNote: "",
        cursor: 1
      },
      status: "idle",
      error: null,
      assignments: [],
      setNote: () => undefined
    }));

    expect(html).toContain("Сложность: Сложный");
  });
});
