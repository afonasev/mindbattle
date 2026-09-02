import { describe, expect, it } from "vitest";
import { CatalogDomainContext } from "../../src/application/contentContext";
import { EMPTY_QUESTION_HISTORY, type ContentCatalog, type TopicPack, validateTopicPack } from "../../src/content";

function topicWithAnswers(answers: TopicPack["questions"][number]["answers"]): TopicPack {
  return {
    id: "topic-notes",
    title: "Тема справок",
    questions: [
      {
        id: "topic-notes-question",
        difficulty: "easy",
        prompt: "Какой вариант правильный?",
        answers,
        correctIndex: 2,
        explanation: "Третий вариант является правильным. Это проверяемая тестовая справка.",
        source: {
          title: "Источник",
          url: "https://example.com/reference",
          verifiedAt: "2026-09-02"
        }
      }
    ]
  };
}

function context(topic: TopicPack): CatalogDomainContext {
  const catalog: ContentCatalog = { revision: "answer-notes-r1", topics: [topic] };
  return new CatalogDomainContext(catalog, EMPTY_QUESTION_HISTORY);
}

function sizedTopic(
  answers: TopicPack["questions"][number]["answers"],
  size: 50 | 100
): TopicPack {
  const quotas = size === 50 ? { easy: 20, medium: 10, hard: 20 } : { easy: 40, medium: 40, hard: 20 };
  return {
    id: "topic-notes",
    title: "Тема справок",
    questions: (["easy", "medium", "hard"] as const).flatMap((difficulty) =>
      Array.from({ length: quotas[difficulty] }, (_, index) => ({
        ...topicWithAnswers(answers).questions[0],
        id: `topic-notes-${difficulty}-${index}`,
        difficulty
      }))
    )
  };
}

describe("content answer notes", () => {
  it("keeps stable answer ids, correctIndex and notes through JSON round-trip", () => {
    const original = topicWithAnswers([
      { text: "Первый", note: "Первый — тестовый неправильный вариант." },
      { text: "Второй", note: "Второй — тестовый неправильный вариант." },
      { text: "Третий", note: "Третий — тестовый правильный вариант." },
      { text: "Четвёртый", note: "Четвёртый — тестовый неправильный вариант." }
    ]);
    const restored = JSON.parse(JSON.stringify(original)) as TopicPack;
    const question = context(restored).getQuestion("topic-notes-question");
    expect(question?.answers).toEqual([
      { id: "answer-0", text: "Первый", note: "Первый — тестовый неправильный вариант." },
      { id: "answer-1", text: "Второй", note: "Второй — тестовый неправильный вариант." },
      { id: "answer-2", text: "Третий", note: "Третий — тестовый правильный вариант." },
      { id: "answer-3", text: "Четвёртый", note: "Четвёртый — тестовый неправильный вариант." }
    ]);
    expect(question?.correctAnswerId).toBe("answer-2");
  });

  it("loads legacy string answers without inventing a note", () => {
    const question = context(
      topicWithAnswers(["Первый", "Второй", "Третий", "Четвёртый"])
    ).getQuestion("topic-notes-question");
    expect(question?.answers.map(({ id, note }) => ({ id, note }))).toEqual([
      { id: "answer-0", note: "" },
      { id: "answer-1", note: "" },
      { id: "answer-2", note: "" },
      { id: "answer-3", note: "" }
    ]);
  });

  it("reports empty, oversized and HTML notes with answer paths", () => {
    const topic = topicWithAnswers([
      { text: "Первый", note: "" },
      { text: "Второй", note: `${"слово ".repeat(36)}.` },
      { text: "Третий", note: "<b>Справка</b>" },
      { text: "Четвёртый", note: "Корректная краткая справка." }
    ]);
    const issues = validateTopicPack(topic);
    expect(issues).toContain("topic-notes/topic-notes-question/answers/0: пустая справка ответа");
    expect(issues).toContain("topic-notes/topic-notes-question/answers/1: справка ответа длиннее 35 слов");
    expect(issues).toContain("topic-notes/topic-notes-question/answers/2: HTML в справке ответа запрещён");
  });

  it("rejects generic placeholder notes", () => {
    const issues = validateTopicPack(topicWithAnswers([
      { text: "Первый", note: "Это правдоподобный вариант той же категории, но не ответ." },
      { text: "Второй", note: "Вторая содержательная справка." },
      { text: "Третий", note: "Третья содержательная справка." },
      { text: "Четвёртый", note: "Четвёртая содержательная справка." }
    ]));
    expect(issues).toContain("topic-notes/topic-notes-question/answers/0: шаблонная справка без содержательного факта запрещена");
  });

  it("rejects a distractor-prefixed negative placeholder", () => {
    const issues = validateTopicPack(topicWithAnswers([
      { text: "Первый", note: "Первый — отдельный тестовый факт." },
      { text: "Второй", note: "«Второй» не подходит: правильным является другой ответ." },
      { text: "Третий", note: "Третий — отдельный тестовый факт." },
      { text: "Четвёртый", note: "Четвёртый — отдельный тестовый факт." }
    ]));
    expect(issues).toContain("topic-notes/topic-notes-question/answers/1: шаблонная справка без содержательного факта запрещена");
  });

  it("rejects a broad category label that does not describe the distractor", () => {
    const issues = validateTopicPack(topicWithAnswers([
      { text: "Рим", note: "Рим — город или географическое название." },
      { text: "Афины", note: "Афины — столица Греции." },
      { text: "Стамбул", note: "Стамбул расположен по обе стороны пролива Босфор." },
      { text: "Александрия", note: "Александрию основали на средиземноморском побережье Египта." }
    ]));
    expect(issues).toContain("topic-notes/topic-notes-question/answers/0: шаблонная справка без содержательного факта запрещена");
  });

  it("rejects search, home and chapter-introduction sources", () => {
    for (const url of [
      "https://www.britannica.com/",
      "https://example.com/search?q=fact",
      "https://openstax.org/books/prealgebra-2e/pages/4-introduction",
      "https://musicbrainz.org/artist/7da030e4-3b08-4e29-b497-344d809589fd"
    ]) {
      const base = topicWithAnswers([
        { text: "Первый", note: "Первый — отдельный тестовый факт." },
        { text: "Второй", note: "Второй — отдельный тестовый факт." },
        { text: "Третий", note: "Третий — отдельный тестовый факт." },
        { text: "Четвёртый", note: "Четвёртый — отдельный тестовый факт." }
      ]);
      const broken = {
        ...base,
        questions: base.questions.map((question) => ({
          ...question,
          source: { title: "Источник", url, verifiedAt: "2026-09-02" }
        }))
      };
      expect(validateTopicPack(broken).join("\n")).toMatch(/точную страницу факта/);
    }
  });

  it("rejects answer-prefixed copies of one common explanation", () => {
    const issues = validateTopicPack(topicWithAnswers([
      { text: "Рим", note: "Рим — итальянский город. Парфенон стоит на афинском Акрополе и посвящён богине Афине." },
      { text: "Афины", note: "Парфенон стоит на афинском Акрополе и посвящён богине Афине." },
      { text: "Стамбул", note: "Стамбул — турецкий город. Парфенон стоит на афинском Акрополе и посвящён богине Афине." },
      { text: "Александрия", note: "Александрия — египетский город. Парфенон стоит на афинском Акрополе и посвящён богине Афине." }
    ]));
    expect(issues).toContain("topic-notes/topic-notes-question: справки вариантов повторяют общий шаблонный хвост вместо отдельных фактов");
  });

  it("requires four distinct notes in final packs but permits legacy migration strings", () => {
    const duplicateNotes = sizedTopic([
      { text: "Первый", note: "Одинаковая справка." },
      { text: "Второй", note: "Одинаковая справка." },
      { text: "Третий", note: "Третья отдельная справка." },
      { text: "Четвёртый", note: "Четвёртая отдельная справка." }
    ], 100);
    expect(validateTopicPack(duplicateNotes)).toEqual(expect.arrayContaining([
      expect.stringContaining("справки вариантов должны различаться")
    ]));

    const stringAnswers = ["Первый", "Второй", "Третий", "Четвёртый"] as const;
    expect(validateTopicPack(sizedTopic(stringAnswers, 100))).toEqual(expect.arrayContaining([
      expect.stringContaining("каждый вариант финального каталога должен иметь справку")
    ]));
    expect(validateTopicPack(sizedTopic(stringAnswers, 50))).not.toEqual(expect.arrayContaining([
      expect.stringContaining("каждый вариант финального каталога должен иметь справку")
    ]));
  });
});
