import {
  chooseTopicCandidates,
  drawQuestion,
  nextRandom,
  type ContentCatalog,
  type QuestionHistory,
  type RandomState,
  type TopicPack
} from "../content";
import type {
  DomainContext,
  QuestionDefinition,
  QuestionSelectionRequest,
  TopicSelectionRequest
} from "../domain/types";

function toDomainQuestion(topic: TopicPack, questionId: string): QuestionDefinition {
  const question = topic.questions.find((candidate) => candidate.id === questionId);
  if (!question) throw new Error(`Вопрос ${questionId} отсутствует в теме ${topic.id}`);
  const answers = question.answers.map((answer, index) => ({
    id: `answer-${index}`,
    text: typeof answer === "string" ? answer : answer.text,
    note: typeof answer === "string" ? "" : answer.note
  })) as [
    { id: string; text: string; note: string },
    { id: string; text: string; note: string },
    { id: string; text: string; note: string },
    { id: string; text: string; note: string }
  ];
  return {
    id: question.id,
    topicId: topic.id,
    difficulty: question.difficulty,
    prompt: question.prompt,
    answers,
    correctAnswerId: answers[question.correctIndex].id,
    explanation: question.explanation
      .split(/(?<=[.!?])\s+/u)
      .map((sentence) => sentence.trim())
      .filter(Boolean),
    source: {
      title: question.source.title,
      url: question.source.url
    }
  };
}

export class CatalogDomainContext implements DomainContext {
  readonly catalogRevision: string;
  private historyState: QuestionHistory;
  private readonly questions = new Map<string, QuestionDefinition>();

  constructor(
    private readonly catalog: ContentCatalog,
    history: QuestionHistory
  ) {
    this.catalogRevision = catalog.revision;
    this.historyState = history;
    for (const topic of catalog.topics) {
      for (const question of topic.questions) {
        this.questions.set(question.id, toDomainQuestion(topic, question.id));
      }
    }
  }

  get history(): QuestionHistory {
    return this.historyState;
  }

  selectTopics(request: TopicSelectionRequest) {
    const selection = chooseTopicCandidates(
      this.catalog.topics,
      request.count,
      {
        selected: request.excludedTopicIds,
        shownCounts: request.shownTopicCounts
      },
      request.random
    );
    return { topicIds: selection.topicIds, random: selection.random };
  }

  selectQuestion(request: QuestionSelectionRequest) {
    let random: RandomState = request.random;
    let topic: TopicPack | undefined;
    let recycledAfterExhaustion = false;
    let excludedQuestionIds = new Set(request.excludedQuestionIds);
    if (request.topicId !== null) {
      topic = this.catalog.topics.find((candidate) => candidate.id === request.topicId);
    } else {
      let eligible = this.catalog.topics.filter((candidate) =>
        candidate.questions.some(
          (question) =>
            question.difficulty === request.difficulty &&
            !request.excludedQuestionIds.includes(question.id)
        )
      );
      if (eligible.length === 0 && request.allowRecycleWhenExhausted) {
        eligible = this.catalog.topics.filter((candidate) =>
          candidate.questions.some((question) => question.difficulty === request.difficulty)
        );
        excludedQuestionIds = new Set();
        recycledAfterExhaustion = true;
      }
      if (eligible.length > 0) {
        const [value, nextState] = nextRandom(random);
        random = nextState;
        topic = eligible[Math.floor(value * eligible.length)];
      }
    }
    if (!topic) throw new Error("Нет доступной темы для вопроса");
    const draw = drawQuestion(
      topic,
      request.difficulty,
      this.historyState,
      random,
      excludedQuestionIds
    );
    this.historyState = draw.history;
    return {
      question: toDomainQuestion(topic, draw.questionId),
      random: draw.random,
      recycledAfterExhaustion
    };
  }

  getQuestion(questionId: string): QuestionDefinition | undefined {
    return this.questions.get(questionId);
  }
}
