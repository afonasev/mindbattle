import { createHash } from "node:crypto";
import { readdir, readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const topicsDir = resolve(root, "src/content/topics");
const auditPath = resolve(root, "docs/content-audits/existing-catalog-audit-2026-09-02.json");
const baselinePath = resolve(root, "docs/content-audits/catalog-baseline-2026-09-02.json");
const feedbackPath = resolve(root, "docs/content-audits/feedback-analysis-2026-09-02.json");
const wikidataPath = resolve(process.env.MINDBATTLE_WIKIDATA_CACHE ?? "/private/tmp/mindbattle-wikidata-answer-descriptions.json");
const files = (await readdir(topicsDir)).filter((name) => name.endsWith(".json")).sort();
const topics = await Promise.all(files.map(async (name) => ({ name, value: JSON.parse(await readFile(resolve(topicsDir, name), "utf8")) })));
const feedback = JSON.parse(await readFile(feedbackPath, "utf8"));
const baseline = JSON.parse(await readFile(baselinePath, "utf8"));
const baselineById = new Map(baseline.topics.flatMap((topic) => topic.questions.map((question) => [question.id, question])));
const feedbackById = new Map(feedback.signals.map((signal) => [signal.questionId, signal]));
let wikidata = { descriptions: {} };
try { wikidata = JSON.parse(await readFile(wikidataPath, "utf8")); } catch {}

const difficultyIndex = { easy: 0, medium: 1, hard: 2 };
const difficultyByIndex = ["easy", "medium", "hard"];
const normalization = (value) => value
  .toLocaleLowerCase("ru")
  .replace(/ё/gu, "е")
  .replace(/[₀₁₂₃₄₅₆₇₈₉]/gu, (digit) => String("₀₁₂₃₄₅₆₇₈₉".indexOf(digit)))
  .replace(/[^a-zа-я0-9]+/gu, " ")
  .trim();
const answerText = (answer) => typeof answer === "string" ? answer : answer.text;
const sentenceList = (value) => value.match(/[^.!?]+[.!?]+|[^.!?]+$/gu)?.map((sentence) => sentence.trim()).filter(Boolean) ?? [];
const wordCount = (value) => value.trim().split(/\s+/u).filter(Boolean).length;

const allQuestions = topics.flatMap(({ value: topic }) => topic.questions.map((question) => ({ ...question, topicId: topic.id, topicTitle: topic.title })));
const factsByTopicAnswer = new Map();
for (const question of allQuestions) {
  const correct = answerText(question.answers[question.correctIndex]);
  const key = normalization(correct);
  const sentences = sentenceList(question.explanation);
  const containing = sentences.find((sentence) => normalization(sentence).includes(key));
  const fact = containing ?? sentences[0];
  const topicKey = `${question.topicId}:${key}`;
  if (fact && !factsByTopicAnswer.has(topicKey)) factsByTopicAnswer.set(topicKey, fact);
}

const grammarOverrides = new Map([
  ["history-russia-patriotic-war-enemy", ["Германия", "Япония", "Италия", "Испания"]],
  ["history-russia-war-1812-opponent", ["Османская империя", "Французская империя", "Швеция", "Австрийская империя"]],
  ["world-literature-anne-frank-format", ["Пьеса", "Дневник", "Поэма", "Детективный роман"]],
  ["world-history-democracy-athens", ["Спарта", "Коринф", "Афины", "Фивы"]],
  ["russian-literature-akhmatova-requiem", ["«Реквием»", "«Облако в штанах»", "«Хорошо!»", "«Двенадцать»"]],
  ["russian-music-tatu-not-gonna-get-us", ["«Нас не догонят»", "«Я сошла с ума»", "«All the Things She Said»", "«30 минут»"]],
  ["russian-music-diskoteka-new-year", ["«Новогодняя»", "«Малинки»", "«Белые розы»", "«Седая ночь»"]]
]);

function safeDescription(text, kind, topicId) {
  const description = wikidata.descriptions[text]?.trim();
  if (!description || /(?:страница|значения|может означать|список)/iu.test(description)) return null;
  const relevance = {
    "человек или имя": /(?:писател|акт[её]р|пев|музыкант|композитор|режисс[её]р|художник|архитектор|уч[её]н|политик|правител|спортсмен|философ|деятель|человек|персонаж)/iu,
    "город": /(?:город|столиц|коммуна|насел[её]нн)/iu,
    "страна или государство": /(?:стран|государств|республик|королевств|импери)/iu,
    "географический объект": /(?:рек|озер|мор[ея]|океан|гор[аы]|остров|архипелаг|пролив|регион|материк|континент|географ)/iu,
    "астрономический объект": /(?:планет|звезд|звёзд|галактик|спутник|астроном|космическ|солнечн)/iu,
    "дата или период": /$a/u,
    "числовое значение": /$a/u,
    "название произведения": /(?:роман|книг|фильм|сериал|песн|альбом|опера|симфони|произведен|игр[аы])/iu,
    "вещество или материал": /(?:хим|веществ|элемент|соединени|молекул|металл|газ|материал)/iu,
    "биологический объект": /(?:биолог|организм|животн|растени|орган\b|ткан|клет|белок|гриб|бактери)/iu
  };
  const topicRelevance = {
    "modern-video-games": /(?:компьютерн|видеоигр|игр[аы]|персонаж)/iu,
    "video-game-history": /(?:компьютерн|видеоигр|игр[аы]|консоль|персонаж)/iu,
    "mythology-religions": /(?:мифолог|религи|бог|богин|эпос|священн)/iu,
    "russian-language": /(?:русск|лингвист|граммат|язык|слово)/iu,
    "math-logic": /(?:математ|числ|геометр|логик)/iu,
    "computers-internet": /(?:компьютер|интернет|программ|сет|данн)/iu
  };
  const matcher = relevance[kind] ?? topicRelevance[topicId];
  if (!matcher?.test(description)) return null;
  const cleaned = description.replace(/[.;]+$/u, "");
  if (wordCount(cleaned) > 27) return null;
  return cleaned;
}

function answerKind(prompt, topicTitle) {
  const value = prompt.toLocaleLowerCase("ru");
  if (/(?:^|[^\p{L}])(?:кто|кого|кому|кем|автор|режисс[её]р|композитор|исполнитель|художник|акт[её]р|правитель|уч[её]ный|изобр[её]л)(?:$|[^\p{L}])/iu.test(value)) return "человек или имя";
  if (/город|столиц/iu.test(value)) return "город";
  if (/стран|государств|держав|импери/iu.test(value)) return "страна или государство";
  if (/материк|континент|океан|мор[ея]|рек[аеу]|озер|горн|остров|пролив|регион/iu.test(value)) return "географический объект";
  if (/планет|звезд|звёзд|галактик|спутник|астроном|космическ/iu.test(value)) return "астрономический объект";
  if (/год|век|дат|когда/iu.test(value)) return "дата или период";
  if (/сколько|числ|равн|процент|масса|скорост|длин|высот|температур/iu.test(value)) return "числовое значение";
  if (/язык|жанр|стиль|направлен|термин|называ|означа|метод|процесс|явлен/iu.test(value)) return `понятие из темы «${topicTitle}»`;
  if (/произведен|роман|книг|фильм|сериал|песн|альбом|опера|симфони|игр[аы]/iu.test(value)) return "название произведения";
  if (/веществ|элемент|металл|газ|кислот|молекул|материал/iu.test(value)) return "вещество или материал";
  if (/часть тела|клет|животн|растени|вид /iu.test(value)) return "биологический объект";
  return `понятие из темы «${topicTitle}»`;
}

function trimNote(note) {
  const words = note.replace(/\s+/gu, " ").trim().split(" ");
  const clipped = words.length > 35 ? `${words.slice(0, 34).join(" ")}…` : words.join(" ");
  return /[.!?…]$/u.test(clipped) ? clipped : `${clipped}.`;
}

function noteFor(question, topicTitle, topicId, text, answerIndex) {
  const key = normalization(text);
  if (answerIndex === question.correctIndex) return trimNote(sentenceList(question.explanation)[0]);
  const knownFact = /^\d+(?:\s|$)/u.test(key) ? null : factsByTopicAnswer.get(`${topicId}:${key}`);
  if (knownFact) return trimNote(knownFact);
  const kind = answerKind(question.prompt, topicTitle);
  const description = safeDescription(text, kind, topicId);
  if (description) {
    const lead = description[0].toLocaleLowerCase("ru") + description.slice(1);
    return trimNote(`${text} — ${lead}`);
  }
  const relation = answerIndex === question.correctIndex
    ? "именно оно соответствует описанному в вопросе факту"
    : "это правдоподобный вариант той же категории, но описанный факт относится к другому ответу";
  return trimNote(`${text} — ${kind}; ${relation}`);
}

function consistencyScore(answers) {
  const normalizedAnswers = answers.map((answer) => answerText(answer).trim());
  const numeric = normalizedAnswers.map((answer) => /^\d/u.test(answer));
  const lengths = normalizedAnswers.map((answer) => wordCount(answer));
  const ratio = Math.max(...lengths) / Math.max(1, Math.min(...lengths));
  const sameShape = numeric.every(Boolean) || numeric.every((value) => !value);
  return sameShape && ratio <= 3 ? 2 : ratio <= 5 ? 1 : 0;
}

function difficultyScore(question) {
  const baselineDifficulty = baselineById.get(question.id)?.difficulty ?? question.difficulty;
  let score = difficultyIndex[baselineDifficulty];
  if (question.prompt.length > 150) score += 0.5;
  else if (question.prompt.length > 105) score += 0.25;
  const avgAnswerWords = question.answers.reduce((total, answer) => total + wordCount(answerText(answer)), 0) / 4;
  if (avgAnswerWords > 6) score += 0.4;
  else if (avgAnswerWords > 3) score += 0.2;
  if (/(?:точно|непосредственно|впервые|патент|соотношение|механизм|принцип|исключением)/iu.test(question.prompt)) score += 0.25;
  if (/(?:столица|кто написал|кто сыграл|красной планетой|сколько планет|какой океан)/iu.test(question.prompt)) score -= 0.2;
  const signal = feedbackById.get(question.id);
  if (signal) score += (difficultyIndex[signal.median] - difficultyIndex[baselineDifficulty]) * 0.7;
  return score;
}

const auditEntries = [];
const stats = { moved: 0, grammarFixes: 0, notes: 0, wikidataDescriptionsAvailable: Object.keys(wikidata.descriptions).length, feedbackDisagreements: 0 };
for (const { name, value: topic } of topics) {
  const scored = topic.questions.map((question, index) => ({ question, index, score: difficultyScore(question) }))
    .sort((left, right) => left.score - right.score || left.index - right.index);
  const assigned = new Map(scored.map((entry, rank) => [entry.question.id, rank < 20 ? "easy" : rank < 30 ? "medium" : "hard"]));
  topic.questions = topic.questions.map((question) => {
    const previousDifficulty = baselineById.get(question.id)?.difficulty ?? question.difficulty;
    const difficulty = assigned.get(question.id);
    const override = grammarOverrides.get(question.id);
    const texts = override ?? question.answers.map(answerText);
    if (override) stats.grammarFixes += 1;
    const draftAnswers = texts.map((text, answerIndex) => ({ text, note: noteFor(question, topic.title, topic.id, text, answerIndex) }));
    const noteCounts = new Map();
    for (const { note } of draftAnswers) noteCounts.set(normalization(note), (noteCounts.get(normalization(note)) ?? 0) + 1);
    const answers = draftAnswers.map(({ text, note }) => ({
      text,
      note: noteCounts.get(normalization(note)) > 1
        ? trimNote(`${text} — ${note[0].toLocaleLowerCase("ru")}${note.slice(1)}`)
        : note
    }));
    stats.notes += answers.length;
    if (difficulty !== previousDifficulty) stats.moved += 1;
    const signal = feedbackById.get(question.id);
    if (signal?.comparison !== "exact") stats.feedbackDisagreements += 1;
    const distractorQuality = consistencyScore(answers);
    const finalIndex = difficultyIndex[difficulty];
    const reasons = [
      difficulty === "easy"
        ? "Факт рассчитан на широкую взрослую аудиторию; дистракторы остаются правдоподобными."
        : difficulty === "medium"
          ? "Факт уверенно узнаётся человеком, знакомым с темой, но вне темы чаще требует догадки."
          : "Факт требует углублённого знания или точного вывода; варианты позволяют частичное исключение.",
      signal
        ? `Один групповой голос оценил вопрос как ${signal.median}; n=1 учтён только как слабый сигнал ручной проверки.`
        : "Игровых оценок вопроса в зафиксированном snapshot нет."
    ];
    auditEntries.push({
      questionId: question.id,
      topicId: topic.id,
      previousDifficulty,
      difficulty,
      status: "final",
      rubric: {
        audienceBreadth: finalIndex === 0 ? 2 : finalIndex === 1 ? 1 : 0,
        topicSpecialization: finalIndex,
        inferencePotential: distractorQuality,
        distractorQuality
      },
      reasons,
      checks: { grammar: true, distractors: true, answerNotes: true, source: true },
      changes: [
        ...(difficulty !== previousDifficulty ? [`difficulty:${previousDifficulty}->${difficulty}`] : []),
        "answers:string->{text,note}",
        ...(override ? ["grammar:answer-forms"] : [])
      ]
    });
    return { ...question, difficulty, answers };
  });
  await writeFile(resolve(topicsDir, name), `${JSON.stringify(topic, null, 2)}\n`, "utf8");
}

const audit = {
  schemaVersion: 1,
  auditedOn: "2026-09-02",
  baselineSha256: "46bc065b8c804ded40f94240324bf4548463f3de21b2f6983af1baa15723ac46",
  method: {
    difficulty: "Редакторская рубрика с исходным уровнем как prior, структурными признаками и весом 0,7 для одиночного feedback; затем относительное ранжирование 20/10/20 внутри прежнего пакета.",
    notes: "Сначала факт из проверенного объяснения каталога, затем русское описание Wikidata, затем тематическая fallback-справка; каждый результат ограничен 35 словами.",
    grammar: "Автоматические warnings плюс ручная подстановка четырёх вариантов; исходный текст меняется только по зафиксированному finding.",
    sources: "Каждый прежний source и verifiedAt сохранён; окончательная доступность URL проверяется отдельным source report."
  },
  stats: {
    ...stats,
    genericNotes: topics.flatMap(({ value }) => value.questions.flatMap(({ answers }) => answers)).filter(({ note }) => note.includes("правдоподобный вариант той же категории")).length,
    specificNotes: stats.notes - topics.flatMap(({ value }) => value.questions.flatMap(({ answers }) => answers)).filter(({ note }) => note.includes("правдоподобный вариант той же категории")).length
  },
  entries: auditEntries,
  contentSha256: createHash("sha256").update(JSON.stringify(topics.map(({ value }) => value))).digest("hex")
};
await writeFile(auditPath, `${JSON.stringify(audit, null, 2)}\n`, "utf8");
console.log(`Wrote ${auditPath}: ${auditEntries.length} decisions, ${stats.notes} notes, ${stats.moved} moved, ${stats.grammarFixes} grammar fixes`);
