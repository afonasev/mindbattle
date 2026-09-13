import { createMatch, reduceFrame } from "../../src/domain/match";
import { shuffle } from "../../src/domain/prng";
import type {
  DomainContext,
  QuestionDefinition,
  MatchState,
  DomainCommand,
  TeamId,
} from "../../src/domain/types";
export function makeContext(topicCount = 40): DomainContext {
  const topics = Array.from(
    { length: topicCount },
    (_, index) => `topic-${index}`,
  );
  const questions: QuestionDefinition[] = topics.flatMap((topicId) =>
    (["easy", "medium", "hard"] as const).flatMap((difficulty) =>
      Array.from({ length: 12 }, (_, index): QuestionDefinition => ({
        id: `${topicId}.${difficulty}.${index}`,
        topicId,
        difficulty,
        prompt: `Вопрос ${topicId} ${difficulty} ${index}`,
        answers: [
          { id: "a", text: "Верный", note: "Справка о верном варианте." },
          { id: "b", text: "Второй", note: "Справка о втором варианте." },
          { id: "c", text: "Третий", note: "Справка о третьем варианте." },
          { id: "d", text: "Четвёртый", note: "Справка о четвёртом варианте." },
        ],
        correctAnswerId: "a",
        explanation: ["Верный ответ подтверждён.", "Это тестовая справка."],
        source: {
          title: "Тестовый источник",
          url: "https://example.com/question",
        },
      })),
    ),
  );
  const byId = new Map(questions.map((question) => [question.id, question]));
  return {
    catalogRevision: "fixture-r1",
    selectTopics(request) {
      const eligible = topics.filter(
        (topicId) => !request.excludedTopicIds.includes(topicId),
      );
      const [ordered, random] = shuffle(eligible, request.random);
      return { topicIds: ordered.slice(0, request.count), random };
    },
    selectQuestion(request) {
      const eligible = questions.filter(
        (question) =>
          question.difficulty === request.difficulty &&
          (request.topicId === null || question.topicId === request.topicId) &&
          !request.excludedQuestionIds.includes(question.id),
      );
      if (eligible.length === 0) throw new Error("fixture catalog exhausted");
      const [ordered, random] = shuffle(eligible, request.random);
      return { question: ordered[0], random };
    },
    getQuestion(questionId) {
      return byId.get(questionId);
    },
  };
}

export const ids = Array.from(
  { length: 12 },
  (_, i) => `player-${i + 1}` as TeamId,
);
export function game(count = 12) {
  const context = makeContext();
  return {
    context,
    state: createMatch(
      {
        profile: "network-v1",
        teams: ids.slice(0, count),
        questionCount: 9,
        answerTimeMs: 10000,
        collectQuestionFeedback: false,
      },
      "network-seed",
      0,
      context,
    ),
  };
}
export function send(
  state: MatchState,
  context: DomainContext,
  commands: readonly DomainCommand[] = [],
  elapsed = 0,
) {
  return reduceFrame(
    state,
    { atMs: state.lastFrameAtMs + elapsed, sequence: 1, commands },
    context,
  );
}
