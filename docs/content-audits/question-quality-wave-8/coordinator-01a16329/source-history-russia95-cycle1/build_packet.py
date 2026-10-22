import copy
import hashlib
import json
import re
from pathlib import Path


OUT = Path(__file__).resolve().parent
C = Path("/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle")
TASK = C / "docs/content-audits/question-quality-wave-8/coordinator-01a16329/source-history-russia95-cycle1-task.json"
ORIGINAL = C / "docs/content-audits/question-quality-wave-8/coordinator-01a16329/source-history-russia95"
INV = OUT / "fresh-inventory.json"
NATIVE_ID = "01a16531-58a4-72d2-ab7c-dc2b20b02e77"
TODAY = "2026-10-23"


def canonical_sha(value):
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def file_sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_json(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


task = json.loads(TASK.read_text(encoding="utf-8"))
original_sourceproof = json.loads((ORIGINAL / "sourceproof.json").read_text(encoding="utf-8"))
inventory = json.loads(INV.read_text(encoding="utf-8"))
before = copy.deepcopy(task["beforeCard"])
before_hash = canonical_sha(before)
assert before_hash == task["beforeHash"] == "eadd41444acfaca9bf12723c614aecd2bfbe92ff72b6599ef8462db57e6816d8"
current = next(x for x in inventory["actualCurrentPeers"] if x["id"] == task["id"])
assert current["sha256"] == before_hash
assert task["frozen"] == {
    "id": before["id"],
    "topicId": "history-russia",
    "sourceOrder": 95,
    "difficulty": "hard",
    "correctIndex": 2,
}

proposed = copy.deepcopy(before)
proposed["prompt"] = (
    "Сколько гласных, помимо городского головы, входило в постоянно действующую "
    "общую градскую думу по Жалованной грамоте городам 1785 года?"
)
proposed["answers"] = [
    {"text": "14", "note": "Жалованная грамота городам состояла из четырнадцати разделов."},
    {"text": "7", "note": "В первый состав Верховного тайного совета входило семь человек."},
    {
        "text": "6",
        "note": "Собрание «градского общества» созывалось раз в три года и включало наиболее состоятельных горожан.",
    },
    {"text": "92", "note": "Жалованная грамота дворянству состояла из 92 статей в четырёх разделах."},
]
proposed["correctIndex"] = 2
proposed["explanation"] = (
    "Постоянно действующей общей градской думой руководили городской голова и шесть гласных. "
    "Собрание «градского общества» было отдельным органом: оно созывалось раз в три года."
)
proposed["source"] = {
    "title": "Екатерина II подписала два законодательных акта: «Жалованная грамота городам» и «Жалованная грамота дворянству» | Президентская библиотека имени Б. Н. Ельцина",
    "url": "https://www.prlib.ru/node/619213",
    "verifiedAt": TODAY,
}

groups = {
    "prompt_ordered_answers_key": {
        "prompt": proposed["prompt"],
        "answers": [x["text"] for x in proposed["answers"]],
        "correctIndex": proposed["correctIndex"],
    },
    "explanation": proposed["explanation"],
    **{f"note{i}": answer["note"] for i, answer in enumerate(proposed["answers"])},
}
before_groups = {
    "prompt_ordered_answers_key": {
        "prompt": before["prompt"],
        "answers": [x["text"] for x in before["answers"]],
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

source_urls = {
    "https://www.prlib.ru/node/619213",
    "https://www.prlib.ru/history/619038",
}
raw_sources = [copy.deepcopy(x) for x in original_sourceproof["rawSources"] if x["url"] in source_urls]
assert {x["url"] for x in raw_sources} == source_urls
source_by_url = {x["url"]: x for x in raw_sources}
city_url = "https://www.prlib.ru/node/619213"
council_url = "https://www.prlib.ru/history/619038"

literal_claims = {
    "prompt_ordered_answers_key": (
        "Полный контекст Президентской библиотеки указывает, что общая градская дума была постоянно действующим городским органом и состояла из городского головы и шести гласных (L51). В L48 датирована Жалованная грамота городам 1785 годом.",
        [city_url],
    ),
    "explanation": (
        "Строка L51 прямо описывает состав и постоянную функцию общей градской думы; далее там же отличает от неё собрание градского общества, созывавшееся раз в три года.",
        [city_url],
    ),
    "note0": (
        "В L48-L49 сказано, что грамота городам состояла из вводного манифеста и четырнадцати разделов.",
        [city_url],
    ),
    "note1": (
        "В L46 полного контекста о Верховном тайном совете перечислены семь участников его первого состава.",
        [council_url],
    ),
    "note2": (
        "В L51 описано собрание градского общества: его созывали раз в три года, в него входили наиболее состоятельные горожане.",
        [city_url],
    ),
    "note3": (
        "В L45 сказано, что Жалованная грамота дворянству состояла из четырёх разделов и 92 статей.",
        [city_url],
    ),
}
literal_groups = []
for name, literal in groups.items():
    ground, urls = literal_claims[name]
    literal_groups.append(
        {
            "group": name,
            "literal": literal,
            "literalSHA256": canonical_sha(literal),
            "primaryGround": ground,
            "sourcePaths": [source_by_url[url]["path"] for url in urls],
            "locator": " | ".join(source_by_url[url]["locator"] for url in urls),
        }
    )

variant_grounds = [
    {
        "grammar": "Числительное отвечает на вопрос «Сколько гласных?»; все четыре варианта даны в одинаковой форме числа.",
        "plausibility": "Число четырнадцать встречается в том же источнике как количество разделов грамоты городам; оно правдоподобно как возможная численность органа, но это другой объект счёта.",
        "truthUniqueKey": "Для Общей градской думы источник указывает шесть гласных; четырнадцать обозначает число разделов Жалованной грамоты городам, не членов думы.",
        "noteTruthUsefulness": "Справка сообщает, что именно число четырнадцать считает в самом документе — его разделы; это конкретный факт о собственном варианте.",
        "sourceUrls": [city_url],
        "locator": "Президентская библиотека L48-L49.",
    },
    {
        "grammar": "Числительное отвечает на вопрос «Сколько гласных?»; форма ряда едина.",
        "plausibility": "Семь — реальная численность первого состава другого высшего государственного органа; число правдоподобно как оценка размера думы, но относится к Верховному тайному совету.",
        "truthUniqueKey": "Полный контекст называет семь участников первого состава Верховного тайного совета; для городской думы он указывает шесть гласных.",
        "noteTruthUsefulness": "Справка сообщает собственный исторический факт о числе участников первого состава Верховного тайного совета.",
        "sourceUrls": [council_url],
        "locator": "Президентская библиотека L46.",
    },
    {
        "grammar": "Числительное отвечает на вопрос «Сколько гласных?»; форма ряда едина.",
        "plausibility": "Число шесть — точная численность гласных, указанная для постоянно действующей общей градской думы; ни один другой вариант не соответствует её составу.",
        "truthUniqueKey": "L51 прямо устанавливает состав Общей градской думы: городской голова и шесть гласных. Это единственный ключ.",
        "noteTruthUsefulness": "Справка добавляет самостоятельную норму о другом городском институте из той же грамоты: состоятельные горожане собирались в общество раз в три года.",
        "sourceUrls": [city_url],
        "locator": "Президентская библиотека L51.",
    },
    {
        "grammar": "Числительное отвечает на вопрос «Сколько гласных?»; форма ряда едина.",
        "plausibility": "Девяносто два — число статей другого акта, подписанного Екатериной II в тот же день; это заметно больше, но остаётся правдоподобной численной альтернативой при незнании состава думы.",
        "truthUniqueKey": "Полный контекст отличает 92 статьи Жалованной грамоты дворянству от шести гласных общей градской думы.",
        "noteTruthUsefulness": "Справка называет, что именно обозначает девяносто два, и характеризует структуру акта о дворянстве.",
        "sourceUrls": [city_url],
        "locator": "Президентская библиотека L45.",
    },
]
assessments = []
for slot, answer in enumerate(proposed["answers"]):
    ground = variant_grounds[slot]
    assessments.append(
        {
            "slot": slot,
            "fullPrompt": proposed["prompt"],
            "answer": answer["text"],
            "note": answer["note"],
            "grammar": ground["grammar"],
            "plausibilityUniqueKeyAndNoteTruthUsefulness": " ".join(
                (ground["plausibility"], ground["truthUniqueKey"], ground["noteTruthUsefulness"])
            ),
            "sourcePaths": [source_by_url[url]["path"] for url in ground["sourceUrls"]],
            "locator": ground["locator"],
            "tripleSHA256": canonical_sha(
                {"prompt": proposed["prompt"], "answer": answer["text"], "note": answer["note"]}
            ),
        }
    )

assert proposed["difficulty"] == "hard" and proposed["correctIndex"] == 2
assert len(assessments) == 4
assert len(proposed["explanation"].split()) <= 70
assert 2 <= len([s for s in re.split(r"(?<=[.!?])\s+", proposed["explanation"].strip()) if s]) <= 4
assert all(len(a["note"].split()) <= 35 for a in proposed["answers"])
assert all(len(a["text"].encode("utf-16-le")) // 2 <= 140 for a in proposed["answers"])

candidate_entry = {
    "id": before["id"],
    "topicId": "history-russia",
    "sourceOrder": 95,
    "status": "READY_FOR_SAME_READER_FINAL",
    "beforeCard": before,
    "beforeHash": before_hash,
    "proposedCard": proposed,
    "afterHash": after_hash,
    "fieldGroups": field_groups,
}
candidate = {
    "owner": task["owner"],
    "sourceNativeId": NATIVE_ID,
    "topicId": "history-russia",
    "cycle": 1,
    "catalogCommit": task["catalogCommit"],
    "entries": [candidate_entry],
}
write_json("candidate.json", candidate)

sourceproof_entry = {
    "id": before["id"],
    "topicId": "history-russia",
    "sourceOrder": 95,
    "status": "READY_FOR_SAME_READER_FINAL",
    "literalGroups": literal_groups,
    "fourFullPromptAnswerNoteAssessments": assessments,
    "correctNoteNewFact": {
        "fact": "Собрание градского общества созывалось раз в три года и включало лишь наиболее состоятельных горожан.",
        "primaryLocator": "Президентская библиотека L51.",
    },
    "absoluteDifficulty": {
        "level": "hard",
        "ground": "Кандидат требует знать точный состав конкретного исторического органа: шесть гласных сверх городского головы. Варианты не называют город, орган или дату, а дают числовые альтернативы, взятые из сохранённых исторических контекстов; простое совпадение слова «город» или исключение даты из label больше не решает вопрос. Это точное специфическое знание, не арифметическая задача.",
    },
}
deviation = task["sourceProvenanceDeviation"]
sourceproof = {
    "owner": task["owner"],
    "sourceNativeId": NATIVE_ID,
    "nativeJournalActual": task["authorNativeJournal"],
    "actualCompactions": 0,
    "stage": "SOURCE_CYCLE1",
    "cycle": 1,
    "catalogCommit": task["catalogCommit"],
    "qualityCredit": 0,
    "id": before["id"],
    "topicId": "history-russia",
    "sourceOrder": 95,
    "beforeHash": before_hash,
    "afterHash": after_hash,
    "rawSources": raw_sources,
    "sourceIndex": [
        str(ORIGINAL / "sourceproof.json"),
        str(ORIGINAL / "candidate.json"),
        str(task["initialReceipt"]),
    ],
    "sourceNetworkCalls": 0,
    "entries": [sourceproof_entry],
    "sourceProvenanceDeviation": deviation,
    "limitations": [
        "Network calls: 0. Only the two previously retained, personally read primary-context outputs at exact pointers were reused; raw bodies were not duplicated into this packet.",
        "The two read-scope overruns and coordinator short-assignment conflict remain uncured under the task's sourceProvenanceDeviation pointer and SHA. This packet and any later QA do not assert procedural compliance.",
        "Cycle 1 preserves frozen HARD and zero-based correctIndex 2; quality credit remains 0 pending same-reader FINAL and coordinator gates.",
    ],
    "initialReceipt": task["initialReceipt"],
    "initialReceiptSHA256": task["initialReceiptSHA256"],
    "peerSnapshot": "peer-snapshot.json",
}
write_json("sourceproof.json", sourceproof)

peer_specs = {
    "history-russia-charter-to-nobility": {
        "candidateToCurrent": "Предложение спрашивает состав Общей градской думы по Жалованной грамоте городам; peer спрашивает судебное условие Жалованной грамоты дворянству. Общая дата и связанные акты не превращают разные институты и нормы в повтор.",
        "currentToCandidate": "Peer проверяет условие лишения дворянина чести, жизни или имущества; он не спрашивает состав городской думы или число гласных.",
        "directReverse": "Нет общего entity-relation-value-context и нет обратной пары.",
    },
    "history-russia-military-settlements": {
        "candidateToCurrent": "Предложение проверяет точный состав городской думы XVIII века; peer — имя руководителя военных поселений начала XIX века.",
        "currentToCandidate": "Военные поселения и их руководитель не входят в факт о городской думе.",
        "directReverse": "Нет общей проверяемой связи или обратной пары.",
    },
    "history-russia-anna-conditions": {
        "candidateToCurrent": "Предложение проверяет численность гласных в думе 1785 года; peer — название ограничительных условий для Анны Иоанновны в 1730 году.",
        "currentToCandidate": "Peer не проверяет состав городского органа; варианты и даты в двух вопросах отличаются по тестируемой связи.",
        "directReverse": "Нет entity-relation-value-context дубликата или обратной формулировки.",
    },
    "history-russia-universal-conscription": {
        "candidateToCurrent": "Предложение спрашивает численность гласных в городской думе; peer спрашивает акт о всесословной воинской повинности. Его дистрактор Жалованная грамота городам не является тестируемым фактом.",
        "currentToCandidate": "Устав 1874 года и воинская повинность не связаны с составом думы по акту 1785 года.",
        "directReverse": "Нет общей проверяемой связи или обратной пары.",
    },
}
relevant_ids = set(peer_specs)
relevant_peers = [copy.deepcopy(x) for x in inventory["actualCurrentPeers"] if x["id"] in relevant_ids]
assert {x["id"] for x in relevant_peers} == relevant_ids
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
            "bilateralMAIN": peer_specs[peer["id"]],
        }
    )

peer_snapshot = {
    "owner": task["owner"],
    "sourceNativeId": NATIVE_ID,
    "topicId": "history-russia",
    "sourceOrder": 95,
    "cycle": 1,
    "beforeHash": before_hash,
    "proposedHash": after_hash,
    "globalMAIN": inventory["globalMAIN"],
    "sameTopicMAIN": inventory["sameTopicMAIN"],
    "actualCurrentPeers": inventory["actualCurrentPeers"],
    "relevantProposedPairs": proposed_pairs,
    "freshInventoryPath": str(INV),
    "freshInventorySHA256": file_sha(INV),
}
write_json("peer-snapshot.json", peer_snapshot)

print(json.dumps({
    "candidate": str(OUT / "candidate.json"),
    "sourceproof": str(OUT / "sourceproof.json"),
    "peerSnapshot": str(OUT / "peer-snapshot.json"),
    "beforeHash": before_hash,
    "afterHash": after_hash,
    "frozen": {k: proposed[k] for k in ("id", "difficulty", "correctIndex")},
    "currentMAINRows": inventory["globalMAIN"]["questionCount"],
    "actualCurrentPeers": len(inventory["actualCurrentPeers"]),
    "sourceNetworkCalls": 0,
}))
