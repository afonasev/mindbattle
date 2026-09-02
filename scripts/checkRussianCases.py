#!/usr/bin/env python3
import json
import re
import argparse
from pathlib import Path
from pymorphy3 import MorphAnalyzer

ROOT = Path(__file__).resolve().parents[1]
TOPICS = ROOT / "src/content/topics"
parser = argparse.ArgumentParser()
parser.add_argument("output", nargs="?", default="docs/content-audits/russian-case-findings-final-2026-09-02.json")
parser.add_argument("--legacy-only", action="store_true")
parser.add_argument("--topic", action="append", default=[])
args = parser.parse_args()
OUTPUT = ROOT / args.output
MORPH = MorphAnalyzer()
MANIFEST = json.loads((ROOT / "src/content/taxonomy-manifest.json").read_text())
LEGACY_TOPIC_IDS = {topic["id"] for topic in MANIFEST["topics"][:30]}

CASE_PATTERNS = [
    (r"^(?:в|на)\s+ка(?:ком|кой|ких)\b", {"loct"}),
    (r"^из\s+ка(?:кого|кой|ких)\b", {"gent"}),
    (r"^(?:с|между)\s+ка(?:ким|кой|кими)\b", {"ablt"}),
    (r"^(?:к|по)\s+ка(?:кому|кой|ким)\b", {"datv"}),
    (r"^(?:для|у|без|около)\s+ка(?:кого|кой|ких)\b", {"gent"}),
    (r"^кого\b", {"gent", "accs"}),
    (r"^кому\b", {"datv"}),
    (r"^кем\b", {"ablt"}),
    (r"^кто\b", {"nomn"}),
    (r"^чего\b", {"gent"}),
    (r"^чему\b", {"datv"}),
    (r"^чем\b", {"ablt"}),
    (r"^какого\b", {"gent", "accs"}),
    (r"^какую\b", {"accs"}),
    (r"^каким\b", {"ablt"}),
    (r"^каких\b", {"gent", "accs"}),
    (r"^ка(?:кой|кая|кое|кие)\b", {"nomn"}),
]

SKIP_WORDS = {"и", "или", "не", "ни", "только", "примерно", "около"}


def expected_cases(prompt: str):
    lowered = prompt.lower().strip()
    for pattern, cases in CASE_PATTERNS:
        if re.search(pattern, lowered):
            return cases
    return None


def leading_lexeme(answer: str):
    words = re.findall(r"[А-Яа-яЁё-]+", answer)
    return next((word for word in words if word.lower() not in SKIP_WORDS), None)


def possible_cases(answer: str):
    word = leading_lexeme(answer)
    if not word:
        return set()
    parses = MORPH.parse(word)
    meaningful = [parse for parse in parses if parse.score >= 0.05]
    return {parse.tag.case for parse in meaningful if parse.tag.case}


def is_standalone_label(answer: str):
    stripped = re.sub(r'^[«„"(\[]+', '', answer.strip())
    return bool(stripped) and (stripped[0].isupper() or stripped[0].isdigit())


findings = []
checked = 0
for file_path in sorted(TOPICS.glob("*.json")):
    topic = json.loads(file_path.read_text())
    if args.legacy_only and topic["id"] not in LEGACY_TOPIC_IDS:
        continue
    if args.topic and topic["id"] not in args.topic:
        continue
    selected_questions = topic["questions"][:50] if args.legacy_only else topic["questions"]
    for question in selected_questions:
        expected = expected_cases(question["prompt"])
        if not expected:
            continue
        checked += 1
        analyzed_answers = []
        for index, raw_answer in enumerate(question["answers"]):
            answer = raw_answer if isinstance(raw_answer, str) else raw_answer["text"]
            cases = possible_cases(answer)
            analyzed_answers.append((index, answer, cases, is_standalone_label(answer)))
        # A one-word or nominal answer label may be a complete standalone reply in
        # the nominative ("Какой город?" — "Москва"), rather than a fragment
        # substituted into the wording. Only require the governed case when the
        # four labels do not consistently support that standalone reading.
        standalone_nominative = all(is_label or not cases or "nomn" in cases for _, _, cases, is_label in analyzed_answers)
        answer_findings = []
        if not standalone_nominative:
            for index, answer, cases, is_label in analyzed_answers:
                if is_label:
                    continue
                if cases and expected.isdisjoint(cases):
                    answer_findings.append({
                        "answerIndex": index,
                        "answer": answer,
                        "expected": sorted(expected),
                        "detected": sorted(cases),
                    })
        if answer_findings:
            findings.append({
                "topicId": topic["id"],
                "questionId": question["id"],
                "prompt": question["prompt"],
                "answers": answer_findings,
            })

report = {
    "schemaVersion": 1,
    "generatedOn": "2026-09-02",
    "method": "dev-only pymorphy3 candidate scan; consistently capitalized labels and nominative labels count as complete standalone replies, every remaining finding requires manual four-answer substitution",
    "questionsWithRecognizedCaseFrame": checked,
    "candidateQuestions": len(findings),
    "findings": findings,
}
OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
print(f"Wrote {OUTPUT}: {len(findings)} candidate questions from {checked} recognized frames")
