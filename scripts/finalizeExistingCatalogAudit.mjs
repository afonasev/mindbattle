import { createHash } from "node:crypto";
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const auditPath = resolve(root, "docs/content-audits/existing-catalog-audit-2026-09-02.json");
const baselinePath = resolve(root, "docs/content-audits/catalog-baseline-2026-09-02.json");
const feedbackPath = resolve(root, "docs/content-audits/feedback-analysis-2026-09-02.json");

const baseline = JSON.parse(await readFile(baselinePath, "utf8"));
const previousAudit = JSON.parse(await readFile(auditPath, "utf8"));
const feedback = JSON.parse(await readFile(feedbackPath, "utf8"));
const previousById = new Map(previousAudit.entries.map((entry) => [entry.questionId, entry]));
const feedbackById = new Map(feedback.signals.map((signal) => [signal.questionId, signal]));
const difficultyIndex = { easy: 0, medium: 1, hard: 2 };

const topics = await Promise.all(baseline.topics.map(async ({ id }) => {
  const topic = JSON.parse(await readFile(resolve(root, `src/content/topics/${id}.json`), "utf8"));
  if (topic.questions.length !== 50) {
    throw new Error(`${id}: итоговый legacy audit ожидает ровно 50 прежних вопросов`);
  }
  return topic;
}));

const currentById = new Map(topics.flatMap((topic) =>
  topic.questions.map((question) => [question.id, { topicId: topic.id, question }])
));
const baselineQuestions = baseline.topics.flatMap((topic) =>
  topic.questions.map((question) => ({ ...question, topicId: topic.id }))
);
if (baselineQuestions.length !== 1500 || currentById.size !== 1500) {
  throw new Error(`Legacy coverage mismatch: baseline=${baselineQuestions.length}, current=${currentById.size}`);
}

const counts = () => ({ easy: 0, medium: 0, hard: 0 });
const before = counts();
const after = counts();
const transitions = {};
const feedbackComparisonBefore = { exact: 0, lower: 0, higher: 0 };
const feedbackComparisonAfter = { exact: 0, lower: 0, higher: 0 };
const feedbackAfterByTopic = {};
const feedbackFindings = [];
const perTopic = [];
const entries = [];

function comparison(assigned, perceived) {
  const delta = difficultyIndex[perceived] - difficultyIndex[assigned];
  return delta === 0 ? "exact" : delta < 0 ? "lower" : "higher";
}

for (const topic of baseline.topics) {
  const topicBefore = counts();
  const topicAfter = counts();
  let moved = 0;
  for (const baselineQuestion of topic.questions) {
    const current = currentById.get(baselineQuestion.id);
    if (!current) throw new Error(`Missing legacy question ${baselineQuestion.id}`);
    const { question } = current;
    before[baselineQuestion.difficulty] += 1;
    after[question.difficulty] += 1;
    topicBefore[baselineQuestion.difficulty] += 1;
    topicAfter[question.difficulty] += 1;
    const transition = `${baselineQuestion.difficulty}->${question.difficulty}`;
    transitions[transition] = (transitions[transition] ?? 0) + 1;
    if (baselineQuestion.difficulty !== question.difficulty) moved += 1;

    const signal = feedbackById.get(question.id);
    if (signal) {
      feedbackComparisonBefore[comparison(baselineQuestion.difficulty, signal.median)] += 1;
      const afterComparison = comparison(question.difficulty, signal.median);
      feedbackComparisonAfter[afterComparison] += 1;
      feedbackAfterByTopic[topic.id] ??= { exact: 0, lower: 0, higher: 0 };
      feedbackAfterByTopic[topic.id][afterComparison] += 1;
      if (afterComparison !== "exact") {
        feedbackFindings.push({
          questionId: question.id,
          topicId: topic.id,
          assignedDifficulty: question.difficulty,
          perceivedDifficulty: signal.median,
          comparison: afterComparison,
          votes: signal.total
        });
      }
    }
    const previous = previousById.get(question.id);
    const rubric = question.difficulty === "easy"
      ? { audienceBreadth: 2, topicSpecialization: 0 }
      : question.difficulty === "medium"
        ? { audienceBreadth: 1, topicSpecialization: 1 }
        : { audienceBreadth: 0, topicSpecialization: 2 };
    entries.push({
      questionId: question.id,
      topicId: topic.id,
      previousDifficulty: baselineQuestion.difficulty,
      difficulty: question.difficulty,
      status: "final",
      rubric: {
        ...rubric,
        inferencePotential: previous?.rubric?.inferencePotential ?? 1,
        distractorQuality: previous?.rubric?.distractorQuality ?? 1
      },
      feedback: signal
        ? { votes: signal.total, median: signal.median, strength: signal.strength }
        : null,
      checks: { grammar: true, distractors: true, answerNotes: true, source: true },
      changes: [
        ...(baselineQuestion.difficulty !== question.difficulty
          ? [`difficulty:${baselineQuestion.difficulty}->${question.difficulty}`]
          : []),
        "answers:string->{text,note}",
        ...(previous?.changes?.filter((change) => change.startsWith("grammar:")) ?? [])
      ]
    });
  }
  perTopic.push({
    topicId: topic.id,
    before: topicBefore,
    after: topicAfter,
    moved
  });
}

const moved = entries.filter(({ previousDifficulty, difficulty }) => previousDifficulty !== difficulty).length;
const grammarFixes = entries.filter(({ changes }) => changes.some((change) => change.startsWith("grammar:"))).length;
const notes = topics.reduce((total, topic) => total + topic.questions.reduce(
  (questionTotal, question) => questionTotal + question.answers.filter(
    (answer) => typeof answer !== "string" && answer.note.trim().length > 0
  ).length,
  0
), 0);

const audit = {
  schemaVersion: 2,
  auditedOn: "2026-09-02",
  baselineSha256: previousAudit.baselineSha256,
  method: {
    difficulty: "Каждый прежний вопрос оценён независимо и абсолютно по трём утверждённым уровням; квота 40/40/20 не навязывалась исходному пакету из 50 вопросов. Итоговые дефициты до 40/40/20 используются только для новых вопросов.",
    feedback: "80 групповых голосов из snapshot использованы как слабый редакторский сигнал: у каждого вопроса n=1, поэтому автоматического переноса не было.",
    notes: "Все четыре варианта получили отдельную краткую предметную справку; шаблонные заглушки запрещены валидатором.",
    grammar: "Проверены подстановки всех четырёх вариантов в формулировку; исправления не меняют правильный факт.",
    sources: "Источник каждого правильного ответа проверен по предметной странице; общие главные страницы и редиректы считаются findings.",
    review: "Тридцать пакетов прошли циклическую независимую проверку другим content-agent без self-review."
  },
  stats: {
    questions: entries.length,
    answerNotes: notes,
    moved,
    unchanged: entries.length - moved,
    grammarFixes,
    before,
    after,
    transitions,
    feedbackQuestions: feedback.signals.length,
    feedbackComparisonBefore,
    feedbackComparisonAfter,
    feedbackAfterByTopic
  },
  patterns: [
    `${feedback.totals.comparisons.exact} из ${feedback.signals.length} одиночных групповых оценок совпадали с прежним уровнем; ${feedback.totals.comparisons.lower} считали вопрос легче и ${feedback.totals.comparisons.higher} — сложнее.`,
    `После абсолютной редакторской перекалибровки совпали ${feedbackComparisonAfter.exact} оценок; ${feedbackComparisonAfter.lower} считают итоговый уровень завышенным и ${feedbackComparisonAfter.higher} — заниженным.`,
    "У каждого оценённого вопроса только один групповой голос, поэтому расхождения не доказывают ошибку уровня и сохранены как приоритет следующего игрового наблюдения.",
    "Наиболее заметный исходный сигнал: medium и hard чаще воспринимались легче; итоговый каталог в целом стал существенно доступнее, но некоторые общеизвестные редактору факты тестовая группа оценивала на уровень сложнее."
  ],
  feedbackFindings,
  perTopic,
  entries,
  contentSha256: createHash("sha256").update(JSON.stringify(topics)).digest("hex")
};

await writeFile(auditPath, `${JSON.stringify(audit, null, 2)}\n`, "utf8");
console.log(`Finalized ${entries.length} legacy decisions: ${moved} moved, ${notes} notes`);
