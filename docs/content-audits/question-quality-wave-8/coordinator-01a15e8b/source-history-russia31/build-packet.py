"""Build the bounded SOURCE31 author packet from named, immutable inputs."""
import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OWN = Path(__file__).resolve().parent
RAW = OWN / "raw"
TASK_PATH = OWN.parent / "source-history-russia31-task.json"
INVENTORY_PATH = OWN / "fresh-inventory.json"
CAPTURE_PATH = RAW / "prlib-sudebniki-ivan-iii-1497.json"
ATTEMPTS_PATH = RAW / "native-web-attempts.json"
DIAGNOSTIC_PATH = RAW / "preservation-diagnostic.json"
NATIVE_ID = "01a15ea2-3302-7a52-9b1c-526dadc9599b"
NATIVE_JOURNAL = f"/Users/eaafonasev/.codex/sessions/2026/10/21/rollout-2026-10-21T18-24-10-{NATIVE_ID}.jsonl"


def canonical_bytes(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def digest(value):
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def file_digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_json(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


task = json.loads(TASK_PATH.read_text())
inventory = json.loads(INVENTORY_PATH.read_text())
source_capture = json.loads(CAPTURE_PATH.read_text())
web_attempts = json.loads(ATTEMPTS_PATH.read_text())
preservation_diagnostic = json.loads(DIAGNOSTIC_PATH.read_text())

assert task["authorNativeId"] == NATIVE_ID
assert task["id"] == "history-russia-sudebnik-1497"
assert task["topicId"] == "history-russia"
assert task["sourceOrder"] == 31
assert task["difficulty"] == "hard"
assert task["correctIndex"] == 0
assert source_capture["sourceNativeId"] == NATIVE_ID
assert source_capture["url"] == "https://www.prlib.ru/item/372573"
assert len(web_attempts["calls"]) == 3
assert [x["label"] for x in web_attempts["calls"]] == [
    "discovery_search",
    "primary_document_open_failed_timeout",
    "official_alternative_open_metadata_only",
]

before_row = next(row for row in inventory["actualCurrentPeers"] if row["id"] == task["id"])
before_card = copy.deepcopy(before_row["card"])
before_hash = digest(before_card)
assert before_hash == task["beforeHash"] == before_row["sha256"]
proposed_card = copy.deepcopy(before_card)
after_hash = digest(proposed_card)

field_literals = {
    "prompt_ordered_answers_key": {
        "prompt": proposed_card["prompt"],
        "answers": [answer["text"] for answer in proposed_card["answers"]],
        "correctIndex": proposed_card["correctIndex"],
    },
    "explanation": proposed_card["explanation"],
    "note0": proposed_card["answers"][0]["note"],
    "note1": proposed_card["answers"][1]["note"],
    "note2": proposed_card["answers"][2]["note"],
    "note3": proposed_card["answers"][3]["note"],
}
field_groups = {
    name: {"beforeCanonicalSHA256": digest(literal), "afterCanonicalSHA256": digest(literal)}
    for name, literal in field_literals.items()
}

inventory_absolute = str(INVENTORY_PATH.resolve())
inventory_sha = file_digest(INVENTORY_PATH)
capture_absolute = str(CAPTURE_PATH.resolve())
capture_relative = str(CAPTURE_PATH.resolve().relative_to(ROOT))
capture_sha = file_digest(capture_absolute)
attempts_absolute = str(ATTEMPTS_PATH.resolve())
attempts_relative = str(ATTEMPTS_PATH.resolve().relative_to(ROOT))
attempts_sha = file_digest(attempts_absolute)
diagnostic_absolute = str(DIAGNOSTIC_PATH.resolve())
diagnostic_relative = str(DIAGNOSTIC_PATH.resolve().relative_to(ROOT))
diagnostic_sha = file_digest(diagnostic_absolute)

peer_match_terms = ("судебник", "иван iii", "иване iii", "юрьев", "1497", "иоанн iii")
relevant_ids = [
    "history-russia-streltsy-origin",
    "history-russia-novgorod-annexation",
    "history-russia-russkaya-pravda-prince",
    "history-russia-mongol-invasion-leader",
    "history-russia-ugra-ruler",
    "history-russia-kazan-conquest",
    "history-russia-church-council-1551",
    "history-russia-anna-conditions",
    "history-russia-brick-kremlin-ruler",
    "history-russia-charter-cities",
]
actual_peer_map = {row["id"]: row for row in inventory["actualCurrentPeers"]}
relevant_peers = [copy.deepcopy(actual_peer_map[peer_id]) for peer_id in relevant_ids]
assert len(relevant_peers) == 10

def peer_ervc(card):
    peer_id = card["id"]
    if peer_id == "history-russia-streltsy-origin":
        return {"entity": "первые постоянные стрелецкие части", "relation": "создание при правителе", "value": "Иван IV", "context": "середина XVI века"}
    if peer_id == "history-russia-novgorod-annexation":
        return {"entity": "Новгородская республика", "relation": "окончательное присоединение к Москве", "value": "1478 год", "context": "объединение русских земель"}
    if peer_id == "history-russia-russkaya-pravda-prince":
        return {"entity": "древнейшая часть Русской Правды", "relation": "князь, с именем которого связывают текст", "value": "Ярослав Мудрый", "context": "древнерусский правовой свод"}
    if peer_id == "history-russia-mongol-invasion-leader":
        return {"entity": "монгольское вторжение в русские земли", "relation": "военачальник", "value": "Батый", "context": "1237–1240 годы"}
    if peer_id == "history-russia-ugra-ruler":
        return {"entity": "стояние на Угре", "relation": "московский правитель", "value": "Иван III", "context": "1480 год"}
    if peer_id == "history-russia-kazan-conquest":
        return {"entity": "завоевание Казанского ханства", "relation": "царь-победитель", "value": "Иван IV", "context": "1552 год"}
    if peer_id == "history-russia-church-council-1551":
        return {"entity": "сборник решений церковного собора", "relation": "название", "value": "Стоглав", "context": "1551 год"}
    if peer_id == "history-russia-anna-conditions":
        return {"entity": "ограничение власти Анны Иоанновны", "relation": "документ Верховного тайного совета", "value": "Кондиции", "context": "1730 год"}
    if peer_id == "history-russia-brick-kremlin-ruler":
        return {"entity": "нынешние кирпичные стены Московского Кремля", "relation": "строительство при правителе", "value": "Иван III", "context": "конец XV века"}
    if peer_id == "history-russia-charter-cities":
        return {"entity": "городское самоуправление Российской империи", "relation": "документ Екатерины II", "value": "Жалованная грамота городам", "context": "1785 год"}
    raise AssertionError(peer_id)

candidate_ervc = {
    "entity": "Судебник 1497 года",
    "relation": "правитель, при котором принят",
    "value": "Иван III",
    "context": "московское законодательство конца XV века",
}
comparisons = []
for peer in relevant_peers:
    peer_id = peer["id"]
    other = peer_ervc(peer["card"])
    comparisons.append({
        "kind": "actualCurrent",
        "peerId": peer_id,
        "peerFullCardSHA256": peer["sha256"],
        "candidateERVC": copy.deepcopy(candidate_ervc),
        "peerERVC": other,
        "candidateToPeer": f"Кандидат MAIN: Судебник 1497 года — при каком правителе принят → Иван III. Соседний MAIN: {other['entity']} — {other['relation']} → {other['value']} ({other['context']}). Совпадение отдельных имён, даты или слова 'Судебник' не совпадает с этой связью и контекстом.",
        "peerToCandidate": f"Обратная сверка: ответ {other['value']} подтверждает только соседнюю связь {other['relation']} для сущности {other['entity']}; он не отвечает на вопрос, при ком принят Судебник 1497 года. Прямого reverse MAIN нет.",
        "directReverse": False,
        "isDuplicate": False,
    })

same_topic_questions = copy.deepcopy(inventory["sameTopicMAIN"]["questions"])
global_hits = []
for row in inventory["globalMAIN"]["rows"]:
    text = json.dumps(row, ensure_ascii=False).lower()
    if row["id"] != task["id"] and any(term in text for term in peer_match_terms):
        global_hits.append({"row": copy.deepcopy(row), "retrievalTerms": [term for term in peer_match_terms if term in text], "use": "lexical retrieval only; manually assessed through ERVC/direct reverse"})

prior_source_index = json.loads(Path(task["sourceIndex"]).read_text())
prior_index_entries = prior_source_index["sourceIndex"]["retainedIndexesPersonallyReviewed"]
source_index_paths = [Path(task["sourceIndex"]), Path(task["additionalRetainedSourceIndex"])] + [Path(path) for path in task["additionalRetainedSourceIndexes"]] + [Path(row["path"]) for row in prior_index_entries]
retained_indexes = []
seen_indexes = set()
for path in source_index_paths:
    absolute = str(path.resolve())
    if absolute in seen_indexes:
        continue
    seen_indexes.add(absolute)
    retained_indexes.append({"path": absolute, "sha256": file_digest(path)})

capture_provenance = {
    "sourceNativeId": NATIVE_ID,
    "nativeJournal": NATIVE_JOURNAL,
    "nativeRecordLine": source_capture["nativeRecordLine"],
    "nativeCallId": source_capture["originalRecord"]["payload"]["call_id"],
    "originalTool": "tools.web__run open",
    "pageLocator": "turn2view0 L37-L51",
    "personalReadBy": NATIVE_ID,
    "readAt": "2026-10-21",
    "personallyReadFullRelevantContext": True,
    "personalReadCoverage": "Personally read the complete returned body L0-L123. L37 gives the bibliographic title 'Судебники Иоанна III и Иоанна IV 1497 и 1555 [!1550] гг.'; L46-L48 identify the 1915 scholarly transcription and the Ivan III collection link. The page contains catalog metadata, not the law text or substantive support for all notes/explanation claims.",
}
source_binding = {
    "path": capture_relative,
    "url": source_capture["url"],
    "title": "Судебники Иоанна III и Иоанна IV 1497 и 1555 [!1550] гг. | Президентская библиотека имени Б.Н. Ельцина",
    "sha256": capture_sha,
    "fileSHA256": capture_sha,
    "completeOutputPointer": source_capture["completeOutputPointer"],
    "completeOutputSHA256": source_capture["completeOutputSHA256"],
    "captureReadProvenance": capture_provenance,
}
source_binding["originalSourceBinding"] = copy.deepcopy(source_binding)
raw_source = {
    "path": capture_relative,
    "sourceOutputLocator": "docs/content-audits/question-quality-wave-8/coordinator-01a15e8b/source-history-russia31/raw/native-web-attempts.json / calls[2] / resultRecord / payload / output / 1 / text; exact same output is bound in raw/prlib-sudebniki-ivan-iii-1497.json",
    "url": source_binding["url"],
    "title": source_binding["title"],
    "sha256": capture_sha,
    "fileSHA256": capture_sha,
    "completeOutputPointer": source_capture["completeOutputPointer"],
    "completeOutputSHA256": source_capture["completeOutputSHA256"],
    "captureReadProvenance": capture_provenance,
    "originalSourceBinding": source_binding,
}

literal_groundings = [
    {
        "group": "prompt_ordered_answers_key",
        "literal": field_literals["prompt_ordered_answers_key"],
        "literalSHA256": digest(field_literals["prompt_ordered_answers_key"]),
        "primaryGround": "Президентская библиотека называет в каталоге Судебники Иоанна III и Иоанна IV и относит издание к 1497 и 1555 [!1550] годам (L37, L46); это поддерживает ключевую связь Судебник 1497 года — Иван III. Однако запись не содержит текст документа, а сама библиографическая строка не подтверждает три остальных варианта и требуемые отдельные факты о них.",
        "locator": "turn2view0 L37, L46-L51; первичная ЭБИД попытка полного документа зафиксирована как timeout в raw/native-web-attempts.json calls[1].",
        "sourcePaths": [capture_relative],
    },
    {
        "group": "explanation",
        "literal": field_literals["explanation"],
        "literalSHA256": digest(field_literals["explanation"]),
        "primaryGround": "Вторая фраза объясняет унификацию судебных норм и ограничение перехода крестьян сроком вокруг Юрьева дня, но карточка Президентской библиотеки содержит только каталог издания, а не его содержание; источник не подтверждает ни одно из этих поясняющих утверждений. Группа HOLD.",
        "locator": "turn2view0 L37-L51; полное содержание недоступно в единственной разрешённой официальной альтернативе.",
        "sourcePaths": [capture_relative],
    },
]
for slot in range(4):
    group = f"note{slot}"
    if slot == 0:
        ground = "Заметка повторяет ответ и вопрос без нового факта об Иване III; официальный каталог подтверждает связь с Судебником, но не даёт дополнительного факта о правителе. Требование к полезной дополнительной заметке не выполнено."
        locator = "turn2view0 L37, L46-L51; body документального источника отсутствует."
    elif slot == 1:
        ground = "Заявление о правлении Василия II в XV веке в доступном контексте не подтверждено. Каталог Судебников не описывает Василия II; содержательная достоверность и полезность заметки остаются HOLD."
        locator = "turn2view0 L37-L51; источник о Василии II отсутствует в сохранённых релевантных полных контекстах."
    elif slot == 2:
        ground = "Заявления о XVI веке и введении опричнины при Иване IV в доступном контексте не подтверждены. Каталог различает Иоанна III и IV, но не подтверждает даты правления и опричнину; HOLD."
        locator = "turn2view0 L37, L46-L51; источник не раскрывает биографические утверждения об Иване IV."
    else:
        ground = "Заявление о вступлении Бориса Годунова на царский престол в 1598 году не подтверждено доступным контекстом; каталог Судебников не описывает Бориса Годунова. HOLD."
        locator = "turn2view0 L37-L51; факт о Борисе Годунове в доступном источнике отсутствует."
    literal_groundings.append({
        "group": group,
        "literal": field_literals[group],
        "literalSHA256": digest(field_literals[group]),
        "primaryGround": ground,
        "locator": locator,
        "sourcePaths": [capture_relative],
    })

full_variants = []
for slot, answer_obj in enumerate(proposed_card["answers"]):
    answer = answer_obj["text"]
    note = answer_obj["note"]
    if slot == 0:
        grammar = "После 'при каком правителе' предложный падеж 'Иване III' согласован; это правильный ключ по библиографическому заглавию источника."
        plausibility = "Категория едина: исторические правители. Иван III правдоподобен, но точное соотнесение Судебника 1497 года с ним требует конкретного знания. Уникальный ключ supported catalog title L37/L46; note0 повторяет ключ и не добавляет собственного полезного факта."
        locator = "turn2view0 L37, L46-L51; correct note lacks an additional fact."
    elif slot == 1:
        grammar = "Предложный падеж 'Василии II' грамматически согласован с вопросом."
        plausibility = "Правитель той же широкой категории и периода, потому вариант может сбить без точной хронологии. Заметка о XV веке отдельно не подтверждена доступным источником; её истинность и польза HOLD."
        locator = "turn2view0 L37-L51 does not discuss Vasily II."
    elif slot == 2:
        grammar = "Предложный падеж 'Иване IV' грамматически согласован с вопросом."
        plausibility = "Другой известный русский правитель, поэтому тематически правдоподобный дистрактор; его правление и введение опричнины относятся к иной эпохе. Утверждения заметки не подтверждены доступной записью каталога."
        locator = "turn2view0 L37, L46-L51 distinguishes Ivan III/IV titles but supplies no reign/oprichnina facts."
    else:
        grammar = "Предложный падеж 'Борисе Годунове' грамматически согласован с вопросом."
        plausibility = "Русский правитель, но его поздний период делает вариант исключимым для знающего хронологию; тематическая категория сохранена. Дата восшествия на престол в заметке не подтверждена доступным источником."
        locator = "turn2view0 L37-L51 does not discuss Boris Godunov."
    triple = {"prompt": proposed_card["prompt"], "answer": answer, "note": note}
    full_variants.append({
        "slot": slot,
        "fullPrompt": proposed_card["prompt"],
        "answer": answer,
        "note": note,
        "grammar": grammar,
        "plausibilityUniqueKeyAndNoteTruthUsefulness": plausibility,
        "sourcePaths": [capture_relative],
        "locator": locator,
        "tripleSHA256": digest(triple),
    })

candidate_entry = {
    "id": task["id"],
    "topicId": task["topicId"],
    "sourceOrder": task["sourceOrder"],
    "status": "HOLD",
    "beforeCard": before_card,
    "beforeHash": before_hash,
    "proposedCard": proposed_card,
    "afterHash": after_hash,
    "fieldGroups": field_groups,
    "proposedCardCanonicalSHA256": after_hash,
}

candidate_packet = {
    "owner": NATIVE_ID,
    "sourceNativeId": NATIVE_ID,
    "stage": "FRESH_PERSONAL_SOURCE31_COMPLETE",
    "cycle": 0,
    "qualityCredit": 0,
    "sourceInventoryPath": inventory_absolute,
    "sourceInventorySHA256": inventory_sha,
    "scope": {
        "id": task["id"],
        "topicId": task["topicId"],
        "sourceOrder": task["sourceOrder"],
        "frozen": {"id": task["id"], "topicId": task["topicId"], "sourceOrder": task["sourceOrder"], "difficulty": "hard", "correctIndex": 0},
    },
    "history": {
        "baselineCode": task["baselineCode"],
        "beforeHash": before_hash,
        "sourceInventoryPath": inventory_absolute,
        "sourceInventorySHA256": inventory_sha,
        "authorNativeId": NATIVE_ID,
        "reviewedAt": "2026-10-21",
        "decision": "HOLD: primary document open timed out and the one official alternative returned catalog metadata only. No unsupported text edits proposed.",
    },
    "entries": [candidate_entry],
}

sourceproof_entry = {
    "id": task["id"],
    "status": "HOLD",
    "beforeHash": before_hash,
    "literalGroups": literal_groundings,
    "fourFullPromptAnswerNoteAssessments": full_variants,
    "correctNoteNewFact": {
        "hasAdditionalFact": False,
        "fact": None,
        "locator": "The note exactly restates the prompt answer; turn2view0 L37/L46-L51 supports only that same Sudebnik/Ivan III association.",
        "sourcePaths": [capture_relative],
        "whyAdditional": "No distinct additional own-option fact is present in the current correct note. The available source's bibliographic title repeats the same association and cannot supply a new own-option fact.",
    },
    "absoluteDifficulty": {
        "level": "hard",
        "audienceGround": "For a general adult without focused knowledge of late-medieval Russian legal history, naming the ruler associated with the specific 1497 Sudebnik requires precise historical recall. The four options are rulers from different periods; chronology makes some eliminable, but the exact codification attribution is still niche factual knowledge rather than broad adult knowledge.",
        "judgment": "HARD retained as frozen. This is a reasoned audience judgment, not a source-derived difficulty statistic; the packet does not claim that every adult will find it hard.",
        "supportingEvidence": {"path": capture_relative, "sha256": capture_sha, "locator": "turn2view0 L37, L46 identify the 1497 Sudebnik with Ivan III; this supplies topic specificity only, not a population difficulty measurement."},
    },
}

sourceproof_packet = {
    "owner": NATIVE_ID,
    "sourceNativeId": NATIVE_ID,
    "stage": "FRESH_PERSONAL_SOURCE31_COMPLETE",
    "cycle": 0,
    "qualityCredit": 0,
    "sourceInventoryPath": inventory_absolute,
    "sourceInventorySHA256": inventory_sha,
    "scope": {
        "id": task["id"],
        "topicId": task["topicId"],
        "sourceOrder": task["sourceOrder"],
        "frozen": {"id": task["id"], "topicId": task["topicId"], "sourceOrder": task["sourceOrder"], "difficulty": "hard", "correctIndex": 0},
        "beforeHash": before_hash,
        "afterHash": after_hash,
    },
    "rawSources": [raw_source],
    "sourceIndex": {
        "retainedIndexesPersonallyReviewed": retained_indexes,
        "targetedSavedSourceSearch": {
            "claimTerms": ["Судебник 1497 Иван III", "https://www.britannica.com/biography/Ivan-III", "Василий II", "Иван IV опричнина", "Борис Годунов 1598"],
            "indexesInspected": len(retained_indexes),
            "result": "No retained full context for the target fact was found in the authorized source indexes. A targeted repository search found the Britannica URL only as a cited source in the earlier order-2 sourceproof; its rawSources are unrelated Kremlin/Presidential Library contexts and do not preserve that page. No retained body was reopened or copied.",
            "sourceIndexFilesSHA256BoundAbove": True,
        },
        "retainedContextSelection": {
            "selectedFullContext": capture_relative,
            "reason": "It is the sole official alternative actually opened in this slice; the primary ЭБИД document open timed out. Existing relevant full primary bodies were not present in the supplied indexes.",
            "notInherited": "No prior author's factual assessment or HOLD/PASS was adopted; the captured bibliographic context was personally read.",
        },
    },
    "inventoryBinding": {
        "path": inventory_absolute,
        "sha256": inventory_sha,
        "topicFiles": inventory["globalMAIN"]["topicFileCount"],
        "MAINRows": inventory["globalMAIN"]["questionCount"],
        "topicCards": len(inventory["sameTopicMAIN"]["questions"]),
        "rowsCanonicalSHA256": inventory["globalMAIN"]["rowsCanonicalSHA256"],
        "targetCardCanonicalSHA256": before_hash,
    },
    "entries": [sourceproof_entry],
    "networkCalls": [
        {"label": call["label"], "callId": call["callId"], "preservedIn": attempts_relative, "preservedInSHA256": attempts_sha, "requestOrdinal": call["requestRecord"]["ordinal"], "resultOrdinal": call["resultRecord"]["ordinal"], "targetUrl": (None if call["label"] == "discovery_search" else "https://www.docs.historyrussia.org/ru/nodes/344542-1497-sentyabrya-sudebnik-velikogo-knyazya-ioanna-vasilievicha" if call["label"] == "primary_document_open_failed_timeout" else source_capture["url"]), "nativeRequestCode": call["requestRecord"]["payload"]["input"]}
        for call in web_attempts["calls"]
    ],
    "networkAccounting": {
        "actualWebCalls": web_attempts["networkCallCount"],
        "discoveryCalls": 1,
        "targetDocumentAttempts": 2,
        "targetDocumentOutcome": "Primary ЭБИД open returned HTTP400 timeout. One official Presidential Library alternative opened as a bibliographic catalog page, not full legal text. No third request or retry.",
        "allOriginalCallRecordsPath": attempts_relative,
        "allOriginalCallRecordsSHA256": attempts_sha,
    },
    "limitations": [
        "The sole primary document open timed out; the single allowed official alternative is catalog metadata and does not expose the legal text.",
        "The key attribution is bibliographically visible, but the complete answer row, three distractor facts, explanatory claims, and useful additional fact for note0 are not fully grounded; remain HOLD.",
        "The planning root configured in workflow/project.json was not present at /Users/eaafonasev/Projects/mindbattle-planning during this slice, so the requested GAME_SPEC and question-catalog spec files could not be read. This did not expand source/network scope.",
        "One packet-preservation helper diagnostic found four matching journal wrappers because its own invocation contained the tool-name string; the exact failed diagnostic call/result is preserved separately. The retained web-attempt file contains exactly the three actual web calls and was relabeled by their exact native request ordinals.",
    ],
    "immutableFullOriginalToolOutputs": [
        {"path": attempts_relative, "sha256": attempts_sha, "purpose": "Exact request/result native records for all three original web calls, including complete search, timeout, and metadata-only responses."},
        {"path": capture_relative, "sha256": capture_sha, "completeOutputPointer": source_capture["completeOutputPointer"], "completeOutputSHA256": source_capture["completeOutputSHA256"], "purpose": "Exact captured official alternative response, bound to this author native session."},
        {"path": diagnostic_relative, "sha256": diagnostic_sha, "purpose": "Exact native wrapper request/result for the non-network preservation helper diagnostic."},
    ],
    "sourceInventoryPath": inventory_absolute,
    "sourceInventorySHA256": inventory_sha,
}

peer_candidate = {
    "id": task["id"],
    "topicId": task["topicId"],
    "sourceOrder": task["sourceOrder"],
    "beforeCard": copy.deepcopy(before_card),
    "beforeCardCanonicalSHA256": before_hash,
    "proposedCard": copy.deepcopy(proposed_card),
    "proposedCardCanonicalSHA256": after_hash,
    "frozen": {"id": task["id"], "topicId": task["topicId"], "sourceOrder": task["sourceOrder"], "difficulty": "hard", "correctIndex": 0},
    "semanticEntity": candidate_ervc["entity"],
    "semanticRelation": candidate_ervc["relation"],
    "semanticValue": candidate_ervc["value"],
    "sourceInventoryPath": inventory_absolute,
    "sourceInventorySHA256": inventory_sha,
}

global_main = copy.deepcopy(inventory["globalMAIN"])
global_main.update({"sourceInventoryPath": inventory_absolute, "sourceInventorySHA256": inventory_sha})
same_topic = {
    "path": inventory["sameTopicMAIN"]["path"],
    "topicId": inventory["sameTopicMAIN"]["topicId"],
    "fileSHA256": inventory["sameTopicMAIN"]["fileSHA256"],
    "questionCount": inventory["sameTopicMAIN"]["questionCount"],
    "questions": same_topic_questions,
    "sourceInventoryPath": inventory_absolute,
    "sourceInventorySHA256": inventory_sha,
}
peer_packet = {
    "owner": NATIVE_ID,
    "sourceNativeId": NATIVE_ID,
    "stage": "FRESH_PERSONAL_SOURCE31_COMPLETE",
    "cycle": 0,
    "qualityCredit": 0,
    "sourceInventoryPath": inventory_absolute,
    "sourceInventorySHA256": inventory_sha,
    "candidate": peer_candidate,
    "globalMAIN": global_main,
    "sameTopicMAIN": same_topic,
    "fullClosestCurrentPeers": relevant_peers,
    "currentGuardRows": {
        "currentTargetBeforeCard": {"card": copy.deepcopy(before_card), "sha256": before_hash, "sourceInventoryPath": inventory_absolute, "sourceInventorySHA256": inventory_sha},
        "frozenFields": {"id": task["id"], "topicId": task["topicId"], "sourceOrder": task["sourceOrder"], "difficulty": "hard", "correctIndex": 0},
    },
    "bilateralCurrentComparisons": comparisons,
    "globalLiteralRetrievalOnlyHits": global_hits,
    "genuineProposalPairs": [],
    "observedNonmatchingProposals": [],
    "proposalSearchLimitations": [
        "The fresh inventory contains the complete 110-file/11,000-row/100-card current catalog and no proposed-card workspace. The assignment's manifest names author31 as the only current source actor and currentSourceActors is empty; no separate concurrent relevant proposal was supplied for bilateral comparison.",
    ],
    "limitations": [
        "Main duplicate screen covers all current catalog rows and all 100 same-topic current cards; ten lexical/entity-adjacent peers were read in full and checked in both directions for MAIN ERVC/direct reverse.",
        "Lexical hits in other items are retrieval pointers only; no identity shared as a distractor or note is counted as duplicate MAIN.",
    ],
    "actualCurrentPeers": copy.deepcopy(inventory["actualCurrentPeers"]),
}

candidate_path = OWN / "candidate.json"
sourceproof_path = OWN / "sourceproof.json"
peer_path = OWN / "peer-snapshot.json"
write_json(candidate_path, candidate_packet)
write_json(sourceproof_path, sourceproof_packet)
write_json(peer_path, peer_packet)

# Parse persisted artifacts and bind every repeated invariant before handoff.
parsed = {path.name: json.loads(path.read_text()) for path in (candidate_path, sourceproof_path, peer_path)}
assert len(parsed["candidate.json"]["entries"]) == 1
assert len(parsed["sourceproof.json"]["entries"]) == 1
assert len(parsed["sourceproof.json"]["entries"][0]["literalGroups"]) == 6
assert len(parsed["sourceproof.json"]["entries"][0]["fourFullPromptAnswerNoteAssessments"]) == 4
assert parsed["sourceproof.json"]["sourceNativeId"] == parsed["candidate.json"]["sourceNativeId"] == parsed["peer-snapshot.json"]["sourceNativeId"] == NATIVE_ID
assert parsed["peer-snapshot.json"]["globalMAIN"]["topicFileCount"] == 110
assert parsed["peer-snapshot.json"]["globalMAIN"]["questionCount"] == 11000
assert parsed["peer-snapshot.json"]["sameTopicMAIN"]["questionCount"] == 100
assert len(parsed["peer-snapshot.json"]["actualCurrentPeers"]) == 100
assert parsed["sourceproof.json"]["sourceInventorySHA256"] == parsed["peer-snapshot.json"]["sourceInventorySHA256"] == inventory_sha
assert parsed["candidate.json"]["entries"][0]["beforeHash"] == before_hash
assert parsed["candidate.json"]["entries"][0]["afterHash"] == after_hash
assert all(len(answer["text"]) <= 140 for answer in proposed_card["answers"])
assert all(len(answer["note"].split()) <= 35 for answer in proposed_card["answers"])
assert len(candidate_packet["entries"][0]["fieldGroups"]) == 6
assert sourceproof_packet["entries"][0]["status"] == "HOLD"
assert peer_packet["candidate"]["beforeCard"] != peer_packet["candidate"]["proposedCard"] or before_hash == after_hash
print(json.dumps({"files": {name: {"path": str((OWN / name).resolve()), "sha256": file_digest(OWN / name)} for name in ("candidate.json", "sourceproof.json", "peer-snapshot.json")}, "status": "HOLD", "qualityCredit": 0, "ownIdCount": 1, "inventoryBounds": {"topicFiles": 110, "MAINRows": 11000, "topicCards": 100}, "networkCallCount": web_attempts["networkCallCount"], "actualCompactions": 0}, ensure_ascii=False))
