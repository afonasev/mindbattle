import type { ContentCatalog, Difficulty, ReviewEntry, TopicPack } from "./types";
import { TOPIC_DEFINITIONS } from "./topicDefinitions";
import { quotaForTopicSize } from "./taxonomy";
import taxonomyManifest from "./taxonomy-manifest.json";

const difficulties: readonly Difficulty[] = ["easy", "medium", "hard"];
const ISO_DATE = /^\d{4}-\d{2}-\d{2}$/;
const ID = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;
const FLOATING_PRESENT = /(на сегодняшний день|в настоящее время|сейчас)/iu;
const EXPLICIT_PERIOD = /(\d{4}|\b(?:век|год|годы|период)\b)/iu;
const HTML = /<\/?[a-z][^>]*>/iu;
const GENERIC_NOTE = new RegExp([
  "правдоподобный вариант той же категории",
  "другой вариант ответа",
  "не подходит",
  "смешивает свойство или связь",
  "здесь описано действие или свойство",
  "смысл этого утверждения",
  "вариант формулирует утверждение",
  "самостоятельное числовое значение",
  "самостоятельная дата в хронологии темы",
  "название произведения, проекта или игрового объекта",
  "название города",
  "название географического объекта",
  "термин из описанной предметной области",
  "имя человека из описанной области",
  "название организации или коллектива",
  "имя литератора",
  "имя художника",
  "имя музыканта",
  "имя акт[её]ра",
  "имя кинематографиста",
  "обозначает страну или территорию",
  "собственное имя, используемое для персонажа, места или объекта в массовой культуре",
  "прямо выражает действие, признак или оценку, названные входящими в неё словами",
  "обозначение:",
  "произведение написал",
  "название предмета, обычая, ремесла, материала или образа русской традиционной культуры",
  "слово, выражение, форма или языковой термин(?: русского языка)?",
  "географический объект или название",
  "число, дата или количественная оценка",
  "анатомический объект или медицинское понятие",
  "биологический объект или понятие",
  "название видеоигры, локации, студии или игрового объекта",
  "понятие, место, символ или обряд из мифологической и религиозной традиции",
  "химическое вещество или понятие",
  "город или географическое название",
  "компьютерный или сетевой термин",
  "физический термин, материал, величина или состояние из условия вопроса",
  "имя российского музыканта, певца, композитора или участника музыкальной группы",
  "название устройства, материала, вещества или технического объекта",
  "композитор или музыкант",
  "календарная дата или числовой вариант периода в истории техники",
  "астрономический объект или термин",
  "имя русского писателя, поэта или драматурга",
  "архитектурный объект или термин",
  "экономический термин или показатель",
  "музыкальный термин или имя",
  "историческое имя, событие или термин",
  "название, персонаж, профессия или кинематографический термин из вариантов вопроса",
  "имя персонажа или автора, связанного с современной игровой культурой",
  "имя советского, российского или зарубежного кинорежисс[её]ра",
  "страна или государство",
  "имя акт[её]ра или персонажа советского и российского кино",
  "историческая фигура или имя",
  "имя персонажа, автора, места или другого понятия русской литературы",
  "название, место, дата или термин из истории российской музыки",
  "имя персонажа, божества или религиозного деятеля одной из мировых традиций",
  "название музыкальной группы, дуэта, ансамбля или радиостанции",
  "числовой вариант результата вычисления или логического подсч[её]та",
  "архитектор или историческая фигура",
  "химическая формула или символ",
  "название текста, эпоса или корпуса религиозной традиции",
  "название фильма советского или российского кинематографа"
].join("|"), "iu");
const TARGET_SIZE_BY_TOPIC = new Map(
  taxonomyManifest.topics.map(({ id, targetSize }) => [id, targetSize] as const)
);
const EXPECTED_TOPIC_COUNT = taxonomyManifest.topics.length;
const EXPECTED_QUESTION_COUNT = taxonomyManifest.topics.reduce(
  (total, { targetSize }) => total + targetSize,
  0
);

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

function sharedSuffixWordCount(left: string, right: string): number {
  const tokens = (value: string) => value.toLocaleLowerCase("ru").match(/[a-zа-яё0-9]+/gu) ?? [];
  const leftTokens = tokens(left);
  const rightTokens = tokens(right);
  let count = 0;
  while (
    count < leftTokens.length &&
    count < rightTokens.length &&
    leftTokens[leftTokens.length - count - 1] === rightTokens[rightTokens.length - count - 1]
  ) count += 1;
  return count;
}

function answerText(answer: TopicPack["questions"][number]["answers"][number]): string {
  return typeof answer === "string" ? answer : answer.text;
}

function answerNote(answer: TopicPack["questions"][number]["answers"][number]): string | null {
  return typeof answer === "string" ? null : answer.note;
}

function sourceSpecificityIssue(value: string): boolean {
  try {
    const url = new URL(value);
    const path = url.pathname.replace(/\/+$/u, "") || "/";
    const genericRootHosts = /(?:^|\.)(?:britannica\.com|culture\.ru|gramota\.ru|loc\.gov|musicbrainz\.org|nasa\.gov|openstax\.org|si\.edu)$/iu;
    return path === "/" && genericRootHosts.test(url.hostname) ||
      /\/(?:search|search-results|categories)$/iu.test(path) ||
      /^\/topics?$/iu.test(path) ||
      /\/pages\/\d+-introduction$/iu.test(path) ||
      /musicbrainz\.org$/iu.test(url.hostname) && /^\/artist\/[^/]+$/u.test(path) ||
      /(?:^|[?&])(?:q|query|search)=/iu.test(url.search);
  } catch {
    return true;
  }
}

export function validateTopicPack(topic: TopicPack): readonly string[] {
  const issues: string[] = [];
  const at = (suffix: string) => `${topic.id || "<topic>"}${suffix}`;

  if (!ID.test(topic.id)) issues.push(`${at("")}: некорректный topic id`);
  if (!topic.title.trim()) issues.push(`${at("")}: пустое название темы`);
  const transitionalLegacyPack = topic.questions.length === 50;
  const expectedByDifficulty = transitionalLegacyPack ? null : quotaForTopicSize(topic.questions.length);
  if (!transitionalLegacyPack && !expectedByDifficulty) {
    issues.push(
      `${at("")}: ожидался допустимый размер 50/100/200/300, получено ${topic.questions.length}`
    );
  }

  const ids = new Set<string>();
  for (const difficulty of difficulties) {
    if (expectedByDifficulty) {
      const count = topic.questions.filter((question) => question.difficulty === difficulty).length;
      if (count !== expectedByDifficulty[difficulty]) {
        issues.push(`${at("")}: ${difficulty} должно быть ${expectedByDifficulty[difficulty]}, получено ${count}`);
      }
    }
    const correctPositions = [0, 1, 2, 3].map((position) =>
      topic.questions.filter((question) => question.difficulty === difficulty && question.correctIndex === position).length
    );
    if (Math.max(...correctPositions) - Math.min(...correctPositions) > 1) {
      issues.push(`${at("")}: ${difficulty} имеет несбалансированные позиции правильных ответов ${correctPositions.join("/")}`);
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
    if (HTML.test(question.prompt) || question.answers.some((answer) => HTML.test(answerText(answer)))) {
      issues.push(`${path}: HTML в игровом тексте запрещён`);
    }
    if (FLOATING_PRESENT.test(question.prompt) && !EXPLICIT_PERIOD.test(question.prompt)) {
      issues.push(`${path}: меняющийся факт требует явного временного контекста`);
    }
    if (question.answers.length !== 4) issues.push(`${path}: требуется 4 ответа`);
    if (new Set(question.answers.map((answer) => answerText(answer).trim().toLocaleLowerCase("ru"))).size !== 4) {
      issues.push(`${path}: ответы должны различаться`);
    }
    if (question.answers.some((answer) => answerText(answer).length > 140)) {
      issues.push(`${path}: вариант ответа длиннее 140 символов`);
    }
    for (const [answerIndex, answer] of question.answers.entries()) {
      const text = answerText(answer);
      const note = answerNote(answer);
      if (!text.trim()) issues.push(`${path}/answers/${answerIndex}: пустой текст ответа`);
      if (note !== null) {
        if (!note.trim()) issues.push(`${path}/answers/${answerIndex}: пустая справка ответа`);
        if (wordCount(note) > 35) {
          issues.push(`${path}/answers/${answerIndex}: справка ответа длиннее 35 слов`);
        }
        if (HTML.test(note)) issues.push(`${path}/answers/${answerIndex}: HTML в справке ответа запрещён`);
        if (GENERIC_NOTE.test(note)) {
          issues.push(`${path}/answers/${answerIndex}: шаблонная справка без содержательного факта запрещена`);
        }
      }
    }
    if (topic.questions.length !== 50 && question.answers.some((answer) => answerNote(answer) === null)) {
      issues.push(`${path}: каждый вариант финального каталога должен иметь справку`);
    }
    const normalizedNotes = question.answers
      .map((answer) => answerNote(answer)?.trim().toLocaleLowerCase("ru"))
      .filter((note): note is string => Boolean(note));
    if (normalizedNotes.length > 0 && new Set(normalizedNotes).size !== normalizedNotes.length) {
      issues.push(`${path}: справки вариантов должны различаться`);
    }
    const completeNotes = question.answers.map(answerNote);
    if (completeNotes.every((note): note is string => note !== null) && completeNotes.some((left, leftIndex) =>
      completeNotes.some((right, rightIndex) => rightIndex > leftIndex && sharedSuffixWordCount(left, right) >= 8)
    )) {
      issues.push(`${path}: справки вариантов повторяют общий шаблонный хвост вместо отдельных фактов`);
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
    if (sourceSpecificityIssue(question.source.url)) {
      issues.push(`${path}: source.url должен вести на точную страницу факта, не на поиск, главную или introduction`);
    }
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
  const legacyCatalog = catalog.topics.length === 30 && catalog.topics.every(({ questions }) => questions.length === 50);
  if (!legacyCatalog && catalog.topics.length !== EXPECTED_TOPIC_COUNT) {
    issues.push(`catalog: ожидалось ${EXPECTED_TOPIC_COUNT} тем, получено ${catalog.topics.length}`);
  }
  const topicIds = new Set<string>();
  const questionIds = new Set<string>();
  const promptKeys = new Set<string>();
  for (const topic of catalog.topics) {
    if (topicIds.has(topic.id)) issues.push(`${topic.id}: повтор topic id`);
    topicIds.add(topic.id);
    issues.push(...validateTopicPack(topic));
    if (!legacyCatalog) {
      const targetSize = TARGET_SIZE_BY_TOPIC.get(topic.id);
      if (targetSize !== undefined && topic.questions.length !== targetSize) {
        issues.push(`${topic.id}: manifest ожидает ${targetSize} вопросов, получено ${topic.questions.length}`);
      }
    }
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
  const expectedQuestionCount = catalog.topics.reduce((total, topic) => total + topic.questions.length, 0);
  if (questionIds.size !== expectedQuestionCount) {
    issues.push(
      `catalog: ожидалось ${expectedQuestionCount} уникальных вопросов, получено ${questionIds.size}`
    );
  }
  if (!legacyCatalog && questionIds.size < EXPECTED_QUESTION_COUNT) {
    issues.push(`catalog: ожидалось минимум ${EXPECTED_QUESTION_COUNT} вопросов, получено ${questionIds.size}`);
  }
  if (reviews !== undefined) {
    if (reviews.length !== catalog.topics.length) {
      issues.push(`reviews: ожидалось ${catalog.topics.length} записей, получено ${reviews.length}`);
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
        review.checkedQuestions !== topic.questions.length ||
        review.criticalFindingsOpen !== 0 ||
        !ISO_DATE.test(review.reviewedAt) ||
        !/^[a-f0-9]{64}$/.test(review.evidence?.questionIdsSha256 ?? "") ||
        Object.values(review.evidence?.checks ?? {}).length !== 9 ||
        Object.values(review.evidence?.checks ?? {}).some(
          (checked) => checked !== topic.questions.length
        ) ||
        !Array.isArray(review.evidence?.reviewedPackageIds) ||
        review.evidence.reviewedPackageIds.length === 0 ||
        new Set(review.evidence.reviewedPackageIds).size !== review.evidence.reviewedPackageIds.length ||
        !Array.isArray(review.evidence?.resolvedFindings) ||
        review.evidence.resolvedFindings.some(
          ({ questionId, issue, resolution }) =>
            !questionId?.trim() || !issue?.trim() || !resolution?.trim()
        )
      ) {
        issues.push(`${topic.id}: редакторское review не завершено`);
      }
    }
  }
  if (issues.length > 0) throw new CatalogValidationError(issues);
  return catalog;
}
