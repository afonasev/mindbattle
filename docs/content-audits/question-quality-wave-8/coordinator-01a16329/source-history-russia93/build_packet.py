#!/usr/bin/env python3
"""Build the owned SOURCE93 author packet from the frozen task and current inventory."""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path


C = Path("/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle")
D = C / "docs/content-audits/question-quality-wave-8/coordinator-01a16329/source-history-russia93"
TASK = C / "docs/content-audits/question-quality-wave-8/coordinator-01a16329/source-history-russia93-task.json"
INVENTORY = D / "fresh-inventory.json"
AUTHOR_ID = "01a1651a-350d-7c00-b9ac-aa7a4ccb90a5"
AUTHOR_JOURNAL = Path("/Users/eaafonasev/.codex/sessions/2026/10/23/rollout-2026-10-23T00-32-58-01a1651a-350d-7c00-b9ac-aa7a4ccb90a5.jsonl")
COORDINATOR_ID = "01a16329-04c9-75f0-806f-091bcec4b169"


def canonical_sha(value: object) -> str:
    body = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def json_write(name: str, value: object) -> None:
    target = D / name
    target.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


task = json.loads(TASK.read_text(encoding="utf-8"))
inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
assert task["id"] == "history-russia-constitution-1977-leader"
assert task["cycle"] == 0 and task["sourceOrder"] == 93
assert task["authorNativeId"] == AUTHOR_ID
assert task["authorNativeJournal"] == str(AUTHOR_JOURNAL)
assert D.is_relative_to(C / "docs/content-audits/question-quality-wave-8")

# Bind the work to the exact native session and preserve the explicit zero-compaction fence.
native_rows = [json.loads(line) for line in AUTHOR_JOURNAL.read_text(encoding="utf-8").splitlines() if line.strip()]
assert sum(row.get("type") == "session_meta" and row.get("payload", {}).get("id") == AUTHOR_ID for row in native_rows) == 1
assert sum(row.get("type") == "compacted" for row in native_rows) == 0

before_item = next(item for item in inventory["actualCurrentPeers"] if item["id"] == task["id"])
before = before_item["card"]
assert before_item["sourceOrder"] == task["sourceOrder"]
assert before_item["sha256"] == task["beforeHash"]
assert canonical_sha(before) == task["beforeHash"]
assert before["difficulty"] == task["difficulty"]
assert before["correctIndex"] == task["correctIndex"]

proposed = json.loads(json.dumps(before, ensure_ascii=False))
proposed["prompt"] = "Кто из советских руководителей связан с Конституцией СССР, принятой в 1977 году?"
proposed["answers"][0]["note"] = "В 1956 году на XX съезде КПСС доклад Никиты Хрущёва критиковал культ личности и деятельность Сталина."
proposed["answers"][1]["note"] = "На XXVII съезде КПСС Горбачёв выступил за экономическое обновление; политику съезда назвали перестройкой, а её лозунгами стали «гласность» и «открытость»."
# Keep the existing Stalin note: it is source-backed and useful for this option.
proposed["answers"][3]["note"] = "Октябрьский пленум 1964 года избрал Брежнева Первым секретарём ЦК КПСС после смещения Хрущёва."
proposed["explanation"] = "Верховный Совет СССР принял Конституцию 7 октября 1977 года; Президентская библиотека называет её «Брежневской». Это название связано с Леонидом Брежневым."
proposed["source"] = {
    "title": "Родился генеральный секретарь ЦК КПСС Леонид Ильич Брежнев | Президентская библиотека имени Б.Н. Ельцина",
    "url": "https://www.prlib.ru/node/619823",
    "verifiedAt": "2026-10-23",
}
assert proposed["difficulty"] == task["frozen"]["difficulty"]
assert proposed["correctIndex"] == task["frozen"]["correctIndex"]
assert proposed["id"] == task["frozen"]["id"]
assert proposed["source"]["url"].startswith("https://")

# Read the three immutable full native page captures by their exact retained source bindings.
defs = [
    {
        "key": "stalin",
        "index": C / "docs/content-audits/question-quality-wave-8/coordinator-01a15ff8/qualified-source-history-russia51/sourceproof.json",
        "path": C / "docs/content-audits/question-quality-wave-8/coordinator-01a15ff8/source-history-russia51/raw/prlib-stalin-biography.json",
        "url": "https://www.prlib.ru/history/619830",
        "title": "Родился советский государственный и партийный деятель Иосиф Виссарионович Сталин",
        "locator": "retained full original page L51, L53, L59",
        "claimCoverage": "L51 supports Stalin's party office and tenure; L53 supports his wartime state and military roles; L59 supports the 1956 Khrushchev report fact used for slot 0.",
        "lines": {
            "L51": ("Генеральным секретарём ЦК", "свыше 30\u00a0лет"),
            "L53": ("С началом Великой отечественной войны", "Верховным Главнокомандующим"),
            "L59": ("докладе Н.\u00a0С.\u00a0Хрущёва", "культ личности"),
        },
    },
    {
        "key": "brezhnev",
        "index": C / "docs/content-audits/question-quality-wave-8/coordinator-01a15ff8/qualified-source-history-russia51/sourceproof.json",
        "path": C / "docs/content-audits/question-quality-wave-8/coordinator-01a15ff8/source-history-russia51/raw/prlib-brezhnev-biography.json",
        "url": "https://www.prlib.ru/node/619823",
        "title": "Родился генеральный секретарь ЦК КПСС Леонид Ильич Брежнев",
        "locator": "retained full original page L52-L54",
        "claimCoverage": "L52 supports the October 1964 election of Brezhnev and his replacement of Khrushchev; L54 supports adoption of the USSR Constitution on 7 October 1977 and the label ‘Brezhnev Constitution’.",
        "lines": {
            "L52": ("избрал Брежнева Первым секретарём ЦК", "сместивший Хрущёва со всех постов"),
            "L54": ("7\u00a0октября 1977\u00a0г.", "«Брежневская» конституция"),
        },
    },
    {
        "key": "gorbachev",
        "index": C / "docs/content-audits/question-quality-wave-8/coordinator-01a15d80/qualified-source-history-russia13/sourceproof.json",
        "path": C / "docs/content-audits/question-quality-wave-8/coordinator-01a15d80/source-history-russia13/raw/prlib-gorbachev-1985.json",
        "url": "https://www.prlib.ru/node/619068",
        "title": "Родился Михаил Сергеевич Горбачёв, первый президент СССР",
        "locator": "retained full original page L44, L50-L51",
        "claimCoverage": "L44 establishes Gorbachev's senior Soviet offices; L50-L51 covers his 1985 election and his 1986 speech, perestroika, glasnost, and openness.",
        "lines": {
            "L44": ("генеральный секретарь ЦК\u00a0КПСС (1985–91)", "первый президент СССР"),
            "L51": ("Политика XXVII\u00a0съезда КПСС была названа «перестройкой»", "«гласность»"),
        },
    },
]

by_key = {}
raw_sources = []
immutable_outputs = []
for spec in defs:
    raw = json.loads(spec["path"].read_text(encoding="utf-8"))
    idx = json.loads(spec["index"].read_text(encoding="utf-8"))
    index_binding = next(item for item in idx["rawSources"] if item.get("url") == spec["url"] and item.get("path", "").endswith(spec["path"].relative_to(C).as_posix()))
    raw_sha = file_sha(spec["path"])
    assert raw_sha == index_binding.get("fileSHA256", index_binding.get("sha256"))
    assert raw.get("url") == spec["url"]
    output_pointer = raw["completeOutputPointer"]
    output = raw["originalRecord"]["payload"]["output"][1]["text"]
    body_sha = hashlib.sha256(output.encode("utf-8")).hexdigest()
    assert output_pointer == "/originalRecord/payload/output/1/text"
    assert body_sha == raw["completeOutputSHA256"]
    indexed = index_binding.get("completeOutputSHA256")
    assert indexed == body_sha
    body_lines = {line.split(":", 1)[0]: line for line in output.splitlines() if line.startswith("L") and ":" in line}
    for label, fragments in spec["lines"].items():
        assert label in body_lines
        assert all(fragment in body_lines[label] for fragment in fragments), (spec["key"], label)
    source_path = spec["path"].relative_to(C).as_posix()
    prior = index_binding.get("captureReadProvenance", {})
    if not isinstance(prior, dict):
        prior = {}
    provenance = {
        "capture": "Reused immutable full original native web output; no SOURCE93 network request.",
        "originalSourceNativeId": raw["sourceNativeId"],
        "nativeJournal": raw["nativeJournal"],
        "nativeRecordLine": raw["nativeRecordLine"],
        "completeOutputPointer": output_pointer,
        "completeOutputSHA256": body_sha,
        "readThisNativeId": AUTHOR_ID,
        "personallyReadRelevantContext": True,
        "relevantLocator": spec["locator"],
        "claimCoverage": spec["claimCoverage"],
    }
    item = {
        "path": source_path,
        "url": spec["url"],
        "title": spec["title"],
        "sha256": raw_sha,
        "fileSHA256": raw_sha,
        "sourceOutputLocator": spec["locator"],
        "completeOutputPointer": output_pointer,
        "completeOutputSHA256": body_sha,
        "captureReadProvenance": provenance,
        "originalSourceBinding": {
            "path": source_path,
            "url": spec["url"],
            "title": spec["title"],
            "fileSHA256": raw_sha,
            "sourceNativeId": raw["sourceNativeId"],
            "nativeJournal": raw["nativeJournal"],
            "nativeRecordLine": raw["nativeRecordLine"],
            "completeOutputPointer": output_pointer,
            "completeOutputSHA256": body_sha,
            "priorReadProvenance": prior.get("personalReadCoverage"),
        },
    }
    by_key[spec["key"]] = {"item": item, "body": output, "path": source_path, "path_object": spec["path"], "raw_sha": raw_sha, "body_sha": body_sha}
    raw_sources.append(item)
    immutable_outputs.append({"path": source_path, "sha256": raw_sha, "jsonPointer": output_pointer})

# Only the source used for each whole literal/triple is named; retained files are not duplicated.
path_stalin = by_key["stalin"]["path"]
path_brezhnev = by_key["brezhnev"]["path"]
path_gorbachev = by_key["gorbachev"]["path"]


def groups(card: dict) -> dict:
    return {
        "prompt_ordered_answers_key": {
            "prompt": card["prompt"],
            "answers": [answer["text"] for answer in card["answers"]],
            "correctIndex": card["correctIndex"],
        },
        "explanation": card["explanation"],
        **{"note" + str(i): answer["note"] for i, answer in enumerate(card["answers"])},
    }


before_groups = groups(before)
after_groups = groups(proposed)
field_groups = {
    key: {
        "beforeCanonicalSHA256": canonical_sha(before_groups[key]),
        "afterCanonicalSHA256": canonical_sha(after_groups[key]),
    }
    for key in before_groups
}
before_hash = canonical_sha(before)
after_hash = canonical_sha(proposed)
assert before_hash == task["beforeHash"]

all_paths = [path_stalin, path_gorbachev, path_brezhnev]
literal_ground = {
    "prompt_ordered_answers_key": (
        "The question now asks who is linked to the 1977 USSR Constitution, matching the source's exact historical label. The date, adoption by the USSR Supreme Soviet, and Brezhnev association are explicit at Brezhnev biography L54; the named leaders and their periods are checked against the four cited full variants.",
        [path_brezhnev, path_stalin, path_gorbachev],
        "Brezhnev biography L52-L54; Stalin biography L51/L53/L59; Gorbachev biography L44/L50-L51",
    ),
    "explanation": (
        "The Supreme Soviet of the USSR adopted the Constitution on 7 October 1977, and the official Presidential Library page calls it the ‘Brezhnev Constitution’; it directly ties the label to Leonid Brezhnev.",
        [path_brezhnev],
        "Brezhnev biography L54",
    ),
    "note0": (
        "The claim is the 1956 XX Congress report by Nikita Khrushchev criticizing Stalin's personality cult and activity; the retained official page states this directly.",
        [path_stalin],
        "Stalin biography L59",
    ),
    "note1": (
        "The note distinguishes Gorbachev's 1986 Congress speech for economic renewal from the Congress policy called perestroika and its slogans glasnost and openness; the retained official page states each link.",
        [path_gorbachev],
        "Gorbachev biography L50-L51",
    ),
    "note2": (
        "The retained official biography states that Stalin was named chairman of the State Defense Committee, Defence Commissar, and Supreme Commander after the war began.",
        [path_stalin],
        "Stalin biography L53",
    ),
    "note3": (
        "The retained official biography states that the October 1964 Central Committee plenary elected Brezhnev First Secretary after removing Khrushchev from all posts.",
        [path_brezhnev],
        "Brezhnev biography L52",
    ),
}

literal_groups = []
for group_name, literal in after_groups.items():
    ground, source_paths, locator = literal_ground[group_name]
    literal_groups.append({
        "group": group_name,
        "literal": literal,
        "literalSHA256": canonical_sha(literal),
        "primaryGround": ground,
        "sourcePaths": source_paths,
        "locator": locator,
    })

variant_grounds = [
    {
        "grammar": "The standalone nominative answer label ‘Никита Хрущёв’ is consistent with all four person-name options; the prompt's ‘кто’ accepts a nominative answer.",
        "assessment": "Khrushchev is a plausible Soviet-leader distractor, but the Brezhnev page places his removal from all posts in October 1964, long before the 1977 event. The note gives a separate, sourced fact about his 1956 report, not the exhausted thaw association.",
        "sourcePaths": [path_stalin, path_brezhnev],
        "locator": "Stalin biography L59; Brezhnev biography L52-L54",
    },
    {
        "grammar": "The standalone nominative answer label ‘Михаил Горбачёв’ is consistent with the other three person-name options and the prompt's ‘кто’ construction.",
        "assessment": "Gorbachev is a plausible Soviet-leader distractor: the official biography dates his General Secretary election to 1985 and documents his 1986 Congress speech. That chronology excludes him from the 1977 Constitution; the note precisely summarizes perestroika and its slogans.",
        "sourcePaths": [path_gorbachev],
        "locator": "Gorbachev biography L44/L50-L51",
    },
    {
        "grammar": "The standalone nominative answer label ‘Иосиф Сталин’ is consistent with the other three person-name options and the prompt's ‘кто’ construction.",
        "assessment": "Stalin is a plausible Soviet-leader distractor, but the official biography places his wartime command roles in 1941-1945 and records his death in 1953, which excludes him from a 1977 event. The existing note is a concrete fact about this option.",
        "sourcePaths": [path_stalin],
        "locator": "Stalin biography L53/L57",
    },
    {
        "grammar": "The standalone nominative answer label ‘Леонид Брежнев’ is consistent with the other three person-name options and directly answers the prompt.",
        "assessment": "Brezhnev is the unique key: the official page identifies the 7 October 1977 Constitution as the ‘Brezhnev Constitution.’ His 1964 election as First Secretary also makes the option's added note factual and useful.",
        "sourcePaths": [path_brezhnev],
        "locator": "Brezhnev biography L52-L54",
    },
]

variants = []
for i, (answer, grounds) in enumerate(zip(proposed["answers"], variant_grounds)):
    triple = {"prompt": proposed["prompt"], "answer": answer["text"], "note": answer["note"]}
    variants.append({
        "slot": i,
        "fullPrompt": proposed["prompt"],
        "answer": answer["text"],
        "note": answer["note"],
        "tripleSHA256": canonical_sha(triple),
        "grammar": grounds["grammar"],
        "plausibilityUniqueKeyAndNoteTruthUsefulness": grounds["assessment"],
        "sourcePaths": grounds["sourcePaths"],
        "locator": grounds["locator"],
    })

sourceproof_entry = {
    "id": task["id"],
    "status": "READY_FOR_INDEPENDENT_REVIEW",
    "beforeHash": before_hash,
    "literalGroups": literal_groups,
    "fourFullPromptAnswerNoteAssessments": variants,
    "correctNoteNewFact": {
        "fact": "In October 1964 the Central Committee plenary removed Khrushchev from all posts and elected Brezhnev First Secretary of the CPSU Central Committee.",
        "locator": "Brezhnev biography L52",
        "sourcePaths": [path_brezhnev],
        "whyAdditional": "The prompt and key identify the person associated with the 1977 Constitution; this adds the distinct year and party office that established Brezhnev's leadership before adoption.",
    },
    "absoluteDifficulty": {
        "level": "medium",
        "audienceGround": "An adult familiar with Soviet history is likely to recognize the named 1977 Constitution and its Brezhnev association. An adult outside the theme can narrow by chronology only if they know the leadership eras; all four choices are real Soviet leaders and none is an absurd option.",
        "judgment": "The frozen medium level is appropriate: the question asks for a specific Soviet-historical association, while the date and plausible leader names permit some contextual narrowing without making the key obvious to an untutored adult.",
        "supportingEvidence": {
            "path": path_brezhnev,
            "pointer": "/originalRecord/payload/output/1/text",
            "sha256": by_key["brezhnev"]["body_sha"],
            "locator": "L52-L54",
        },
    },
}

candidate_entry = {
    "id": task["id"],
    "topicId": task["topicId"],
    "sourceOrder": task["sourceOrder"],
    "status": "READY_FOR_INDEPENDENT_REVIEW",
    "beforeCard": before,
    "beforeHash": before_hash,
    "proposedCard": proposed,
    "afterHash": after_hash,
    "fieldGroups": field_groups,
    "proposedCardCanonicalSHA256": after_hash,
}
candidate = {
    "owner": COORDINATOR_ID,
    "sourceNativeId": AUTHOR_ID,
    "stage": "SOURCE93_AUTHOR_READY_FOR_INDEPENDENT_REVIEW",
    "cycle": 0,
    "qualityCredit": 0,
    "scope": "One SOURCE93 card only; author READY is not qualification, application, independent review, QA, or credit.",
    "history": {
        "preimage": "Fresh current-inventory card and exact task beforeHash agree; no catalog file was modified.",
        "previousEvidence": "No prior HOLD claim or quality judgment is adopted. The consumed SOURCE76 thaw-association chain is not reopened; note0 is replaced by a distinct 1956 report fact supported by retained primary text.",
    },
    "entries": [candidate_entry],
}

indexes = [task["sourceIndex"]]
predecessor = json.loads(Path(task["manifest"]).read_text(encoding="utf-8"))["predecessorHandoff"]
pred = json.loads(Path(predecessor).read_text(encoding="utf-8"))
indexes.append(pred["sourceIndex"])
indexes.extend(task.get("additionalRetainedSourceIndexes", []))
indexes = list(dict.fromkeys(indexes))
source74 = next(path for path in indexes if "qualified-source-history-russia74/sourceproof.json" in path)

sourceproof = {
    "owner": COORDINATOR_ID,
    "sourceNativeId": AUTHOR_ID,
    "stage": "SOURCE93_AUTHOR_READY_FOR_INDEPENDENT_REVIEW",
    "cycle": 0,
    "qualityCredit": 0,
    "rawSources": raw_sources,
    "sourceIndex": {
        "candidate": [{"path": path_brezhnev, "locator": "Brezhnev biography L52-L54: election and 1977 Constitution label."}],
        "options": {
            "0": [{"path": path_stalin, "locator": "Stalin biography L59: Khrushchev's 1956 XX Congress report."}],
            "1": [{"path": path_gorbachev, "locator": "Gorbachev biography L44/L50-L51: offices, perestroika and slogans."}],
            "2": [{"path": path_stalin, "locator": "Stalin biography L53: wartime offices and command roles."}],
            "3": [{"path": path_brezhnev, "locator": "Brezhnev biography L52: October 1964 First Secretary election."}],
        },
        "coverage": {
            "currentIndex": task["sourceIndex"],
            "predecessorIndex": pred["sourceIndex"],
            "source74Index": source74,
            "enumeratedIndexCount": len(indexes),
            "uniqueRawPathsInInventoriedIndexes": 104,
            "targetedBodyScan": "Automated search across those indexed raw files found no retained ‘оттепель’ or Khrushchev-thaw body match; the three relevant full official biographies were then read personally at their claim-bearing lines.",
            "personallyReadRelevantFullSourceBodies": 3,
            "targetedThawBodyMatches": 0,
            "decision": "No retained full body was found for the consumed Khrushchev-thaw association. No consumed URL was reopened; a different source-backed 1956 report fact is used for slot 0.",
        },
        "country": "not applicable",
    },
    "entries": [sourceproof_entry],
    "limitations": [
        "The old SOURCE76 Khrushchev-thaw association and its exhausted source chain are not reused, retried, or promoted. Slot 0 uses a distinct claim from the retained official Stalin biography.",
        "All evidence is from previously captured full pages; SOURCE93 made zero web calls, so no new native web result required capture-helper recovery.",
    ],
    "immutableFullOriginalToolOutputs": immutable_outputs,
    "mechanicalIntake": [{"rawPacket": str(TASK), "rawSHA256": file_sha(TASK), "operation": "Scope/frozen preimage and attempt boundaries read; exact current inventory bound."}],
    "authorNativeContext": {
        "nativeJournal": str(AUTHOR_JOURNAL),
        "actualCompactedEventCount": 0,
        "actualWebCalls": 0,
    },
}

# Build the compact evidence projection: bindings/hash for all 110 topics, and full current same-topic cards.
rows = inventory["globalMAIN"]["rows"]
files = inventory["globalMAIN"]["allCurrentFileByteBindings"]
row_counts = Counter(row["topicId"] for row in rows)
file_bindings = []
for binding in files:
    topic = Path(binding["path"]).stem
    file_bindings.append({
        "path": binding["path"],
        "topicId": topic,
        "questionCount": row_counts[topic],
        "fileSha256": binding["sha256"],
    })
assert len(file_bindings) == 110 and len(rows) == 11000
same = inventory["sameTopicMAIN"]
actual = inventory["actualCurrentPeers"]
assert len(same["questions"]) == len(actual) == 100

peer_ids = [
    "history-russia-constitution-1936",
    "history-russia-wartime-leader",
    "history-russia-perestroika-leader",
    "history-russia-thaw-leader",
    "history-russia-collective-farms-policy",
    "history-russia-glasnost-policy",
    "history-russia-reform-1965-profit",
]
peer_by_id = {item["id"]: item for item in actual}
closest = [{k: peer_by_id[qid][k] for k in ("id", "topicId", "sourceOrder", "card", "sha256")} for qid in peer_ids]

candidate_ervc = {
    "entity": "Constitution of the USSR adopted in 1977",
    "relation": "historical leader associated with the document",
    "value": "Leonid Brezhnev",
    "context": "official USSR adoption on 7 October 1977; commonly labeled the ‘Brezhnev Constitution’",
}
peer_ervcs = {
    "history-russia-constitution-1936": {
        "entity": "USSR Constitution of 1936",
        "relation": "unofficial title",
        "value": "Stalin Constitution",
        "context": "1936 constitution; distinct document and title from the 1977 constitution",
    },
    "history-russia-wartime-leader": {
        "entity": "USSR leadership during the Great Patriotic War",
        "relation": "leader during wartime",
        "value": "Joseph Stalin",
        "context": "1941-1945 wartime period",
    },
    "history-russia-perestroika-leader": {
        "entity": "Perestroika",
        "relation": "Soviet leader primarily associated with the policy",
        "value": "Mikhail Gorbachev",
        "context": "1985-1986 political reforms, distinct from the 1977 Constitution",
    },
    "history-russia-thaw-leader": {
        "entity": "Khrushchev Thaw",
        "relation": "Soviet leader associated with the period",
        "value": "Nikita Khrushchev",
        "context": "post-Stalin liberalization; distinct from the 1977 Constitution association",
    },
    "history-russia-collective-farms-policy": {
        "entity": "mass consolidation of peasant farms into kolkhozes",
        "relation": "name of policy",
        "value": "collectivization",
        "context": "late 1920s and 1930s; not a leader-document relation",
    },
    "history-russia-glasnost-policy": {
        "entity": "public openness during perestroika",
        "relation": "name of policy",
        "value": "glasnost",
        "context": "1980s political discourse; distinct from 1977 constitutional adoption",
    },
    "history-russia-reform-1965-profit": {
        "entity": "1965 Soviet economic reform",
        "relation": "reform expanding enterprise autonomy",
        "value": "Kosygin reform",
        "context": "enterprise management and profit incentives, not constitutional leadership",
    },
}

comparisons = []
for qid in peer_ids:
    peer = peer_by_id[qid]
    comparisons.append({
        "kind": "same-topic MAIN relation comparison",
        "peerId": qid,
        "peerFullCardSHA256": peer["sha256"],
        "candidateERVC": candidate_ervc,
        "peerERVC": peer_ervcs[qid],
        "candidateToPeer": "Not a duplicate: the candidate tests a 1977 constitutional association with Brezhnev; the peer tests a distinct entity, relation, value, or period. Shared person names or Soviet-history vocabulary do not create the same factual relation.",
        "peerToCandidate": "The peer's fact does not ask or answer which leader is associated with the 1977 USSR Constitution; no direct reverse relation is present.",
        "isDuplicate": False,
    })

literal_terms = ("history-russia-wartime-leader", "history-russia-perestroika-leader", "history-russia-thaw-leader", task["id"])
source_file_sha = same["fileSHA256"]
retrieval_hits = []
for qid in literal_terms:
    row = next(row for row in rows if row["id"] == qid)
    retrieval_hits.append({
        "topicId": row["topicId"],
        "sourceOrder": next(peer["sourceOrder"] for peer in actual if peer["id"] == qid),
        "id": row["id"],
        "card": row,
        "cardCanonicalSHA256": canonical_sha(row),
        "sourceFilePath": same["path"],
        "sourceFileSHA256": source_file_sha,
    })

candidate_peer = {
    "id": task["id"],
    "topicId": task["topicId"],
    "sourceOrder": task["sourceOrder"],
    "beforeCard": before,
    "beforeCardCanonicalSHA256": before_hash,
    "proposedCard": proposed,
    "proposedCardCanonicalSHA256": after_hash,
    "frozen": task["frozen"],
    "semanticEntity": candidate_ervc["entity"],
    "semanticRelation": candidate_ervc["relation"],
    "semanticValue": candidate_ervc["value"],
}

order92 = peer_by_id["history-russia-collective-farms-policy"]
peer_snapshot = {
    "owner": COORDINATOR_ID,
    "sourceNativeId": AUTHOR_ID,
    "stage": "SOURCE93_AUTHOR_READY_FOR_INDEPENDENT_REVIEW",
    "cycle": 0,
    "qualityCredit": 0,
    "candidate": candidate_peer,
    "globalMAIN": {
        "topicFileCount": 110,
        "questionCount": 11000,
        "projectionShape": "{topicId,id,prompt,answers:[four text strings],correctIndex}; rows were retrieved sorted by topic filename then original question order.",
        "rowsCanonicalSHA256": inventory["globalMAIN"]["rowsCanonicalSHA256"],
        "allCurrentFileByteBindings": file_bindings,
        "readDate": "2026-10-23",
    },
    "sameTopicMAIN": {
        "path": same["path"],
        "topicId": same["topicId"],
        "fileSHA256": same["fileSHA256"],
        "questionCount": same["questionCount"],
        "questions": same["questions"],
    },
    "fullClosestCurrentPeers": closest,
    "currentGuardRows": {
        "currentTargetBeforeCard": {
            "id": task["id"],
            "topicId": task["topicId"],
            "sourceOrder": task["sourceOrder"],
            "card": before,
            "cardCanonicalSHA256": before_hash,
            "reviewOnly": "Exact current baseline preimage; not quality evidence.",
        },
        "visibleConcurrentSource92CurrentCard": {
            "id": order92["id"],
            "topicId": order92["topicId"],
            "sourceOrder": order92["sourceOrder"],
            "card": order92["card"],
            "cardCanonicalSHA256": order92["sha256"],
            "reviewOnly": "The visible current card is about collectivization. The active SOURCE92 proposed card was not provided or inspected; no inference is made about its content or pair relationship.",
        },
    },
    "bilateralCurrentComparisons": comparisons,
    "globalLiteralRetrievalOnlyHits": retrieval_hits,
    "genuineProposalPairs": [],
    "observedNonmatchingProposals": [],
    "proposalSearchLimitations": "SOURCE92 authoring is active in parallel, but no proposed SOURCE92 body was supplied in this assignment. The visible current order92 card concerns collectivization and is unrelated; its existence does not reveal the unpublished proposal. No cross-proposal comparison is claimed.",
    "limitations": [
        "Global literal retrieval for the exact 1977 Constitution/leader relationship found the candidate itself only; literal Brezhnev hits are the same-topic history-russia rows listed above, not independent duplicates.",
        "No SOURCE92 proposal body was available. Only its visible current baseline card was inspected; unpublished content was not inferred.",
    ],
    "actualCurrentPeers": actual,
}

json_write("candidate.json", candidate)
json_write("sourceproof.json", sourceproof)
json_write("peer-snapshot.json", peer_snapshot)
print(json.dumps({
    "candidate": str(D / "candidate.json"),
    "sourceproof": str(D / "sourceproof.json"),
    "peerSnapshot": str(D / "peer-snapshot.json"),
    "status": "READY_FOR_INDEPENDENT_REVIEW",
    "beforeHash": before_hash,
    "afterHash": after_hash,
    "fieldGroupCount": len(field_groups),
    "fullVariantCount": len(variants),
    "rawSources": len(raw_sources),
    "topicPeers": len(actual),
    "globalRows": len(rows),
    "actualCompactedEvents": 0,
    "webCalls": 0,
    "qualityCredit": 0,
}, ensure_ascii=False))
