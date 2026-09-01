import type { ContentCatalog, Difficulty, ReviewEntry, TopicPack } from "./types";
import { TOPIC_DEFINITIONS } from "./topicDefinitions";

const difficulties: readonly Difficulty[] = ["easy", "medium", "hard"];
const ISO_DATE = /^\d{4}-\d{2}-\d{2}$/;
const ID = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;
const FLOATING_PRESENT = /(на сегодняшний день|в настоящее время|сейчас)/iu;
const EXPLICIT_PERIOD = /(\d{4}|\b(?:век|год|годы|период)\b)/iu;
const HTML = /<\/?[a-z][^>]*>/iu;

export class CatalogValidationError extends Error {
  constructor(readonly issues: readonly string[]) {
    super(issues.join("\n"));
    this.name = "CatalogValidationError";
  }
}

function sentenceCount(text: string): number {
  return (text.match(/[.!?](?:\s|$)/g) ?? []).length;
}

function wordCount(text: string): number {
  return text.trim().split(/\s+/u).filter(Boolean).length;
}

export function validateTopicPack(topic: TopicPack): readonly string[] {
  const issues: string[] = [];
  const at = (suffix: string) => `${topic.id || "<topic>"}${suffix}`;

  if (!ID.test(topic.id)) issues.push(`${at("")}: некорректный topic id`);
  if (!topic.title.trim()) issues.push(`${at("")}: пустое название темы`);
  if (topic.questions.length !== 50) {
    issues.push(`${at("")}: ожидалось 50 вопросов, получено ${topic.questions.length}`);
  }

  const ids = new Set<string>();
  const expectedByDifficulty: Readonly<Record<Difficulty, number>> = {
    easy: 20,
    medium: 10,
    hard: 20
  };
  for (const difficulty of difficulties) {
    const count = topic.questions.filter((question) => question.difficulty === difficulty).length;
    if (count !== expectedByDifficulty[difficulty]) {
      issues.push(`${at("")}: ${difficulty} должно быть ${expectedByDifficulty[difficulty]}, получено ${count}`);
    }
  }

  for (const question of topic.questions) {
    const path = at(`/${question.id || "<question>"}`);
    if (!ID.test(question.id)) issues.push(`${path}: некорректный question id`);
    if (!question.id.startsWith(`${topic.id}-`)) {
      issues.push(`${path}: question id должен начинаться с topic id`);
    }
    if (ids.has(question.id)) issues.push(`${path}: повтор question id`);
    ids.add(question.id);
    if (!question.prompt.trim()) issues.push(`${path}: пустой вопрос`);
    if (question.prompt.length > 320) issues.push(`${path}: вопрос длиннее 320 символов`);
    if (HTML.test(question.prompt) || question.answers.some((answer) => HTML.test(answer))) {
      issues.push(`${path}: HTML в игровом тексте запрещён`);
    }
    if (FLOATING_PRESENT.test(question.prompt) && !EXPLICIT_PERIOD.test(question.prompt)) {
      issues.push(`${path}: меняющийся факт требует явного временного контекста`);
    }
    if (question.answers.length !== 4) issues.push(`${path}: требуется 4 ответа`);
    if (new Set(question.answers.map((answer) => answer.trim().toLocaleLowerCase("ru"))).size !== 4) {
      issues.push(`${path}: ответы должны различаться`);
    }
    if (question.answers.some((answer) => answer.length > 140)) {
      issues.push(`${path}: вариант ответа длиннее 140 символов`);
    }
    if (![0, 1, 2, 3].includes(question.correctIndex)) {
      issues.push(`${path}: correctIndex вне диапазона`);
    }
    const sentences = sentenceCount(question.explanation);
    if (sentences < 2 || sentences > 4) {
      issues.push(`${path}: explanation должен содержать 2–4 предложения`);
    }
    if (wordCount(question.explanation) > 70) {
      issues.push(`${path}: explanation длиннее 70 слов`);
    }
    if (HTML.test(question.explanation)) issues.push(`${path}: HTML в explanation запрещён`);
    if (!question.source.title.trim()) issues.push(`${path}: пустой source.title`);
    if (!/^https:\/\//.test(question.source.url)) issues.push(`${path}: source.url должен быть HTTPS`);
    if (!ISO_DATE.test(question.source.verifiedAt)) issues.push(`${path}: verifiedAt должен быть YYYY-MM-DD`);
  }

  return issues;
}

export function validateCatalog(
  catalog: ContentCatalog,
  reviews?: readonly ReviewEntry[]
): ContentCatalog {
  const issues: string[] = [];
  if (!catalog.revision.trim()) issues.push("catalog: пустая revision");
  if (catalog.topics.length !== 30) {
    issues.push(`catalog: ожидалось 30 тем, получено ${catalog.topics.length}`);
  }
  const topicIds = new Set<string>();
  const questionIds = new Set<string>();
  const promptKeys = new Set<string>();
  for (const topic of catalog.topics) {
    if (topicIds.has(topic.id)) issues.push(`${topic.id}: повтор topic id`);
    topicIds.add(topic.id);
    issues.push(...validateTopicPack(topic));
    for (const question of topic.questions) {
      if (questionIds.has(question.id)) issues.push(`${question.id}: глобальный повтор question id`);
      questionIds.add(question.id);
      const promptKey = question.prompt.toLocaleLowerCase("ru").replace(/[^a-zа-яё0-9]+/gu, " ").trim();
      if (promptKeys.has(promptKey)) issues.push(`${question.id}: глобальный повтор текста вопроса`);
      promptKeys.add(promptKey);
    }
  }
  for (const [id, title] of TOPIC_DEFINITIONS) {
    const topic = catalog.topics.find((candidate) => candidate.id === id);
    if (!topic) issues.push(`catalog: отсутствует тема ${id}`);
    else if (topic.title !== title) issues.push(`${id}: ожидалось название «${title}»`);
  }
  if (questionIds.size !== 1500) {
    issues.push(`catalog: ожидалось 1500 уникальных вопросов, получено ${questionIds.size}`);
  }
  if (reviews !== undefined) {
    if (reviews.length !== TOPIC_DEFINITIONS.length) {
      issues.push(`reviews: ожидалось 30 записей, получено ${reviews.length}`);
    }
    const reviewedTopicIds = new Set<string>();
    for (const review of reviews) {
      if (reviewedTopicIds.has(review.topicId)) {
        issues.push(`${review.topicId}: повтор редакторского review`);
      }
      reviewedTopicIds.add(review.topicId);
      if (!topicIds.has(review.topicId)) {
        issues.push(`${review.topicId}: review ссылается на неизвестную тему`);
      }
    }
    for (const topic of catalog.topics) {
      const review = reviews.find((entry) => entry.topicId === topic.id);
      if (!review) issues.push(`${topic.id}: нет редакторского review`);
      else if (review.author === review.reviewer) {
        issues.push(`${topic.id}: автор и reviewer должны различаться`);
      } else if (
        review.status !== "approved" ||
        !/^[a-f0-9]{64}$/.test(review.contentSha256) ||
        review.checkedQuestions !== 50 ||
        review.criticalFindingsOpen !== 0 ||
        !ISO_DATE.test(review.reviewedAt)
      ) {
        issues.push(`${topic.id}: редакторское review не завершено`);
      }
    }
  }
  if (issues.length > 0) throw new CatalogValidationError(issues);
  return catalog;
}
