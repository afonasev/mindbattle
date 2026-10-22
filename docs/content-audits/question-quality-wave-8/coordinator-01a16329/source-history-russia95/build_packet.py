import copy
import hashlib
import json
from pathlib import Path
import re


OUT = Path(__file__).resolve().parent
INV = OUT / "fresh-inventory-after94.json"
NATIVE_ID = "01a16531-58a4-72d2-ab7c-dc2b20b02e77"
TODAY = "2026-10-23"


def canonical_sha(value):
    encoded = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def file_sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def body_at_pointer(path, pointer):
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    for part in pointer.lstrip("/").split("/"):
        part = part.replace("~1", "/").replace("~0", "~")
        value = value[int(part)] if isinstance(value, list) else value[part]
    if not isinstance(value, str):
        raise TypeError(f"Expected text at {path}#{pointer}")
    return value


def write_json(name, value):
    (OUT / name).write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


inventory = json.loads(INV.read_text(encoding="utf-8"))
current = next(
    item for item in inventory["actualCurrentPeers"]
    if item["id"] == "history-russia-charter-cities"
)
before = copy.deepcopy(current["card"])
before_hash = canonical_sha(before)
assert before_hash == "a2330d5de88ddfb007e8a65bbcd62ceeeab86ef50ae1173535eb22843573026c"
assert before["difficulty"] == "hard" and before["correctIndex"] == 2

proposed = copy.deepcopy(before)
proposed["answers"][0]["note"] = (
    "В 1730 году Анна Иоанновна публично разорвала «Кондиции» после приезда в Москву."
)
proposed["answers"][1]["note"] = (
    "Стоглав — сборник решений церковного собора 1551 года о церковной жизни "
    "и обрядах."
)
proposed["answers"][2]["note"] = (
    "Грамота делила горожан на шесть разрядов по имущественным и социальным признакам."
)
proposed["answers"][3]["note"] = (
    "Судебник включал нормы Русской Правды, уставных грамот, Псковской судной грамоты "
    "и указов московских князей."
)
proposed["explanation"] = (
    "Жалованная грамота городам установила новые выборные учреждения и расширила "
    "круг избирателей. Она делила горожан на шесть разрядов по имущественным и "
    "социальным признакам."
)
proposed["source"] = {
    "title": "Екатерина II подписала два законодательных акта: «Жалованная грамота городам» и «Жалованная грамота дворянству» | Президентская библиотека имени Б. Н. Ельцина",
    "url": "https://www.prlib.ru/node/619213",
    "verifiedAt": TODAY,
}

groups = {
    "prompt_ordered_answers_key": {
        "prompt": proposed["prompt"],
        "answers": [answer["text"] for answer in proposed["answers"]],
        "correctIndex": proposed["correctIndex"],
    },
    "explanation": proposed["explanation"],
    **{f"note{i}": answer["note"] for i, answer in enumerate(proposed["answers"])},
}
before_groups = {
    "prompt_ordered_answers_key": {
        "prompt": before["prompt"],
        "answers": [answer["text"] for answer in before["answers"]],
        "correctIndex": before["correctIndex"],
    },
    "explanation": before["explanation"],
    **{f"note{i}": answer["note"] for i, answer in enumerate(before["answers"])},
}
field_groups = {
    name: {
        "beforeCanonicalSHA256": canonical_sha(before_groups[name]),
        "afterCanonicalSHA256": canonical_sha(groups[name]),
    }
    for name in groups
}
assert len(field_groups) == 6
after_hash = canonical_sha(proposed)

raw_base = Path(__file__).resolve().parents[2]
source_definitions = [
    {
        "rawPath": raw_base / "coordinator-01a15f65/source-history-russia43/raw/prlib-charter-article-open.json",
        "url": "https://www.prlib.ru/node/619213",
        "sourceNativeId": "01a15f6c-1bc4-70b2-b6fe-1a3662194b00",
        "pointer": "/originalRecord/payload/output/1/text",
        "locator": "Президентская библиотека, L44, L48-L51: оба акта подписаны 21 апреля (2 мая) 1785 года; городская грамота ввела выборные учреждения, расширила круг избирателей, делила горожан на шесть разрядов.",
    },
    {
        "rawPath": raw_base / "coordinator-01a15f65/source-history-russia43/raw/prlib-supreme-council-anna-open.json",
        "url": "https://www.prlib.ru/history/619038",
        "sourceNativeId": "01a15f6c-1bc4-70b2-b6fe-1a3662194b00",
        "pointer": "/originalRecord/payload/output/1/text",
        "locator": "Президентская библиотека, L52-L54: условия «Кондиции» были предложены Анне Иоанновне в 1730 году и ограничивали её самостоятельные решения.",
    },
    {
        "rawPath": raw_base / "coordinator-01a15e8b/source-history-russia32/raw/native-web-attempts.json",
        "url": "https://www.prlib.ru/history/1902481",
        "sourceNativeId": "01a15eb0-06a5-7f03-a7e5-d3d9266b60b2",
        "pointer": "/calls/1/resultRecord/payload/output/1/text",
        "locator": "Президентская библиотека, L48: в 1551 году созван Стоглавый собор, а его решения о церковной жизни и обрядах собраны в «Стоглаве».",
    },
    {
        "rawPath": raw_base / "coordinator-01a15ff8/source-history-russia50/capture-prlib-official-alternative.json",
        "url": "https://www.prlib.ru/history/618966",
        "sourceNativeId": "01a15fff-0bf7-78c3-b7e8-4c7a33626c78",
        "pointer": "/originalRecord/payload/output/1/text",
        "locator": "Президентская библиотека, L58: Судебник введён в действие в сентябре 1497 года как единый законодательный кодекс для объединённых русских земель.",
    },
]
raw_sources = []
for source in source_definitions:
    path = source["rawPath"]
    raw_sources.append(
        {
            "path": str(path),
            "url": source["url"],
            "sha256": file_sha(path),
            "captureReadProvenance": {
                "captureNativeId": source["sourceNativeId"],
                "captureKind": "previously retained original tool output; no new network request",
                "completeOutputPointer": source["pointer"],
                "personallyReadByNativeId": NATIVE_ID,
            },
            "completeOutputPointer": source["pointer"],
            "completeOutputSHA256": hashlib.sha256(
                body_at_pointer(path, source["pointer"]).encode("utf-8")
            ).hexdigest(),
            "locator": source["locator"],
        }
    )

source_path = {item["url"]: item["path"] for item in raw_sources}
source_locator = {item["url"]: item["locator"] for item in raw_sources}

literal_claims = {
    "prompt_ordered_answers_key": (
        "The question asks for the 1785 Catherine II act regulating urban self-government; "
        "the official Presidential Library page identifies the Charter to Cities as one of "
        "two acts signed that day and describes its municipal institutions.",
        ["https://www.prlib.ru/node/619213"],
    ),
    "explanation": (
        "The library states that the Charter created new elected city institutions, expanded "
        "the electorate, and divided residents into six property and social classes.",
        ["https://www.prlib.ru/node/619213"],
    ),
    "note0": (
        "After arriving in Moscow in 1730, Anna Ioannovna publicly tore up the Conditions.",
        ["https://www.prlib.ru/history/619038"],
    ),
    "note1": (
        "The 1551 Stoglav council's decisions on church life and rites were collected in the "
        "Stoglav.",
        ["https://www.prlib.ru/history/1902481"],
    ),
    "note2": (
        "The Charter divided townspeople into six classes by property and social position.",
        ["https://www.prlib.ru/node/619213"],
    ),
    "note3": (
        "The Sudebnik incorporated norms from Russkaya Pravda, regional charters, the Pskov "
        "Judicial Charter, and Moscow princely decrees.",
        ["https://www.prlib.ru/history/618966"],
    ),
}
literal_groups = []
for name, literal in groups.items():
    ground, urls = literal_claims[name]
    locators = [source_locator[url] for url in urls]
    literal_groups.append(
        {
            "group": name,
            "literal": literal,
            "literalSHA256": canonical_sha(literal),
            "primaryGround": ground,
            "sourcePaths": [source_path[url] for url in urls],
            "locator": " | ".join(locators),
        }
    )

assessments = [
    {
        "slot": 0,
        "fullPrompt": proposed["prompt"],
        "answer": proposed["answers"][0]["text"],
        "note": proposed["answers"][0]["note"],
        "grammar": "В сочетании с вопросом название документа оформлено как самостоятельный вариант; форма «Кондиции» допустима как собственное название акта.",
        "plausibilityUniqueKeyAndNoteTruthUsefulness": "Это законодательный акт, поэтому относится к той же широкой категории. Он связан с ограничением власти Анны Иоанновны в 1730 году, а не с городским самоуправлением при Екатерине II. Справка сообщает, что Анна публично разорвала документ после приезда в Москву.",
        "sourcePaths": [source_path["https://www.prlib.ru/history/619038"]],
        "locator": source_locator["https://www.prlib.ru/history/619038"],
    },
    {
        "slot": 1,
        "fullPrompt": proposed["prompt"],
        "answer": proposed["answers"][1]["text"],
        "note": proposed["answers"][1]["note"],
        "grammar": "Название документа стоит в именительном падеже и сочетается с вопросом «Какой документ?».",
        "plausibilityUniqueKeyAndNoteTruthUsefulness": "Стоглав — правовой и церковный сборник, поэтому это документ той же общей категории; он создан в 1551 году и не является актом о городском самоуправлении. Справка указывает отдельные содержание и контекст именно этого сборника.",
        "sourcePaths": [source_path["https://www.prlib.ru/history/1902481"]],
        "locator": source_locator["https://www.prlib.ru/history/1902481"],
    },
    {
        "slot": 2,
        "fullPrompt": proposed["prompt"],
        "answer": proposed["answers"][2]["text"],
        "note": proposed["answers"][2]["note"],
        "grammar": "Полное название документа отвечает на вопрос «Какой документ?».",
        "plausibilityUniqueKeyAndNoteTruthUsefulness": "Это единственный из четырёх вариантов, который Президентская библиотека связывает с Екатериной II, 1785 годом и выборными учреждениями городов. Справка сообщает дополнительный факт о шести разрядах горожан, которого нет в prompt/key.",
        "sourcePaths": [source_path["https://www.prlib.ru/node/619213"]],
        "locator": source_locator["https://www.prlib.ru/node/619213"],
    },
    {
        "slot": 3,
        "fullPrompt": proposed["prompt"],
        "answer": proposed["answers"][3]["text"],
        "note": proposed["answers"][3]["note"],
        "grammar": "Название документа стоит в именительном падеже и отвечает на вопрос «Какой документ?».",
        "plausibilityUniqueKeyAndNoteTruthUsefulness": "Это российский законодательный кодекс, поэтому он принадлежит к той же широкой категории, но относится к 1497 году и правовой системе объединённых земель, а не к городскому самоуправлению при Екатерине II. Справка перечисляет правовые источники, нормы которых вошли в кодекс.",
        "sourcePaths": [source_path["https://www.prlib.ru/history/618966"]],
        "locator": source_locator["https://www.prlib.ru/history/618966"],
    },
]
for item in assessments:
    triple = {
        "prompt": item["fullPrompt"],
        "answer": item["answer"],
        "note": item["note"],
    }
    item["tripleSHA256"] = canonical_sha(triple)

assert len(assessments) == 4
assert all(len(a["text"].encode("utf-16-le")) // 2 <= 140 for a in proposed["answers"])
assert all(len(a["note"].split()) <= 35 for a in proposed["answers"])
sentences = [s for s in re.split(r"(?<=[.!?])\s+", proposed["explanation"].strip()) if s]
assert 2 <= len(sentences) <= 4
assert len(proposed["explanation"].split()) <= 70

candidate_entry = {
    "id": before["id"],
    "topicId": "history-russia",
    "sourceOrder": 95,
    "status": "READY_FOR_INDEPENDENT_REVIEW",
    "beforeCard": before,
    "beforeHash": before_hash,
    "proposedCard": proposed,
    "afterHash": after_hash,
    "fieldGroups": field_groups,
}
candidate = {
    "owner": "01a16329-04c9-75f0-806f-091bcec4b169",
    "sourceNativeId": NATIVE_ID,
    "topicId": "history-russia",
    "cycle": 0,
    "baselineCode": "e0eac9fca1096df4e2c2a62299f76aae06a11677",
    "catalogCandidate": "e0eac9fca1096df4e2c2a62299f76aae06a11677",
    "entries": [candidate_entry],
}
write_json("candidate.json", candidate)

sourceproof_entry = {
    "id": before["id"],
    "topicId": "history-russia",
    "sourceOrder": 95,
    "status": "READY_FOR_INDEPENDENT_REVIEW",
    "literalGroups": literal_groups,
    "fourFullPromptAnswerNoteAssessments": assessments,
    "correctNoteNewFact": {
        "fact": "Горожане делились на шесть разрядов по имущественным и социальным признакам.",
        "primaryLocator": source_locator["https://www.prlib.ru/node/619213"],
    },
    "absoluteDifficulty": {
        "level": "hard",
        "ground": "Взрослому игроку нужно знать конкретный российский законодательный акт и его связь с городским управлением; четыре варианта — реальные российские исторические документы, так что правильный ответ требует специфического знания, а не распознавания абсурдного distractor.",
    },
}
sourceproof = {
    "owner": "01a16329-04c9-75f0-806f-091bcec4b169",
    "sourceNativeId": NATIVE_ID,
    "nativeJournalActual": "/Users/eaafonasev/.codex/sessions/2026/10/23/rollout-2026-10-23T00-58-15-01a16531-58a4-72d2-ab7c-dc2b20b02e77.jsonl",
    "actualCompactions": 0,
    "stage": "SOURCE",
    "cycle": 0,
    "qualityCredit": 0,
    "id": before["id"],
    "topicId": "history-russia",
    "sourceOrder": 95,
    "beforeHash": before_hash,
    "afterHash": after_hash,
    "rawSources": raw_sources,
    "sourceIndex": [
        "/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle/docs/content-audits/question-quality-wave-8/coordinator-01a16329/qualified-source-history-russia93/sourceproof.json",
        "/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle/docs/content-audits/question-quality-wave-8/coordinator-01a15f65/qualified-source-history-russia43/sourceproof.json",
        "/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle/docs/content-audits/question-quality-wave-8/coordinator-01a15e8b/source-history-russia32/sourceproof.json",
        "/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle/docs/content-audits/question-quality-wave-8/coordinator-01a15ff8/qualified-source-history-russia50/sourceproof.json",
    ],
    "sourceNetworkCalls": 0,
    "entries": [sourceproof_entry],
    "limitations": [
        "Existing retained full outputs were personally read; no new network calls were made. Each raw file is referenced once by path and exact output pointer; full bodies are not recopied into this packet.",
        "The task's bootstrap read-scope overrun remains uncured as recorded in source95-bootstrap-readscope-deviation.json (SHA256 2043aa678cbcb7380e2bace56bdb044b332cb8dcf691a3ca5607f488cfae436b). This packet does not assert procedural compliance.",
        "During this task, a broad predecessor handoff projection was inadvertently printed while extracting pointers; no files outside this output directory were written. This additional read-scope deviation is uncured and should be considered alongside the bootstrap record.",
        "The START message specified MEDIUM/key3, while the exact task and live preimage specify HARD/correctIndex2. The third answer position corresponds to zero-based correctIndex2 and is consistent; only difficulty conflicts. This packet preserves the exact current HARD preimage and makes no frozen-field change.",
    ],
    "peerSnapshot": "peer-snapshot.json",
}
write_json("sourceproof.json", sourceproof)

relevant_ids = {
    "history-russia-charter-to-nobility",
    "history-russia-military-settlements",
    "history-russia-anna-conditions",
    "history-russia-universal-conscription",
}
relevant_peers = [
    copy.deepcopy(item) for item in inventory["actualCurrentPeers"]
    if item["id"] in relevant_ids
]
assessments_by_id = {
    "history-russia-charter-to-nobility": {
        "candidateToCurrent": "Distinct fact: this peer asks about protections in the Charter to the Nobility; the proposal asks about the Charter to Cities and urban self-government. They share Catherine II and 1785 but test different charters and provisions.",
        "currentToCandidate": "The peer's key is the judicial condition for removing a noble's status, life, or property; it does not ask for the municipal charter or its city institutions.",
        "directReverse": "No: neither prompt is the reverse of the other's entity-relation-value-context.",
    },
    "history-russia-military-settlements": {
        "candidateToCurrent": "This peer asks which person is associated with early nineteenth-century military settlements; the proposal asks which eighteenth-century city-government statute Catherine II issued.",
        "currentToCandidate": "The proposal does not test Arakcheev or military settlements. No overlapping tested fact beyond broad Russian history.",
        "directReverse": "No shared entity-relation-value-context; no reverse pair.",
    },
    "history-russia-anna-conditions": {
        "candidateToCurrent": "This peer asks which document the Supreme Privy Council used in its attempt to limit Anna Ioannovna; the proposal asks which 1785 document regulated city self-government. The four document labels overlap as a same-category option set, but the facts, actors, dates, relations, and keys differ.",
        "currentToCandidate": "The peer's correct answer is «Кондиции», while the proposal's is Жалованная грамота городам. The peer's note for the city-charter distractor repeats the broad relation asked by the proposal; the proposed correct note instead adds the independently sourced six-city-class fact. The peer itself does not ask who issued the city charter or what municipal organization it established.",
        "directReverse": "No: the pair is not a reversed entity-relation-value-context. Retain the pair as distinct; do not alter the peer.",
    },
    "history-russia-universal-conscription": {
        "candidateToCurrent": "This peer asks which act created universal military service, whereas the proposal asks which act regulated urban self-government. Both include the Charter to Cities as an incorrect label in the other row, but their tested events and institutions differ.",
        "currentToCandidate": "The peer's key is the 1874 military-service statute; it does not ask about Catherine II, city government, or the Charter to Cities. Its reused distractor notes are not new evidence for the proposal.",
        "directReverse": "No shared entity-relation-value-context and no direct reverse; retain as a distinct historical-act question.",
    },
}
proposed_pairs = []
for peer in relevant_peers:
    peer_card = copy.deepcopy(peer["card"])
    proposed_pairs.append(
        {
            "candidateId": proposed["id"],
            "candidateCard": copy.deepcopy(proposed),
            "candidateCanonicalSHA256": after_hash,
            "actualPeerId": peer["id"],
            "actualPeerCard": peer_card,
            "actualPeerCanonicalSHA256": canonical_sha(peer_card),
            "bilateralMAIN": assessments_by_id[peer["id"]],
        }
    )

peer_snapshot = {
    "owner": "01a16329-04c9-75f0-806f-091bcec4b169",
    "sourceNativeId": NATIVE_ID,
    "topicId": "history-russia",
    "sourceOrder": 95,
    "beforeHash": before_hash,
    "proposedHash": after_hash,
    "globalMAIN": inventory["globalMAIN"],
    "sameTopicMAIN": inventory["sameTopicMAIN"],
    "actualCurrentPeers": inventory["actualCurrentPeers"],
    "relevantProposedPairs": proposed_pairs,
    "freshInventoryPath": str(INV),
    "freshInventorySHA256": file_sha(INV),
    "recentAppliedCurrentChecks": [
        {
            "id": "history-russia-glasnost-policy",
            "sourceOrder": 94,
            "currentCardSHA256": next(
                item["sha256"] for item in inventory["actualCurrentPeers"]
                if item["id"] == "history-russia-glasnost-policy"
            ),
            "relevance": "Read from refreshed current inventory after application at e435c18a65d69507b32a9e0cd84c16b2cbaaf779. This asks about the glasnost slogan during perestroika, a separate twentieth-century political fact; it creates no relevant semantic pair with the 1785 city charter. The full current card is retained in actualCurrentPeers.",
        }
    ],
}
write_json("peer-snapshot.json", peer_snapshot)

print(json.dumps({
    "candidate": str(OUT / "candidate.json"),
    "sourceproof": str(OUT / "sourceproof.json"),
    "peerSnapshot": str(OUT / "peer-snapshot.json"),
    "beforeHash": before_hash,
    "afterHash": after_hash,
    "frozen": {key: proposed[key] for key in ("id", "difficulty", "correctIndex")},
    "globalMAINRows": inventory["globalMAIN"]["questionCount"],
    "currentTopicPeers": len(inventory["actualCurrentPeers"]),
}))
