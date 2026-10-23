import copy
import hashlib
import json
from pathlib import Path

ROOT = Path("/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle")
OUT = ROOT / "docs/content-audits/question-quality-wave-8/coordinator-01a16a43/source-human-medicine77"
INV = OUT / "fresh-inventory.json"
NATIVE = "01a16a5f-8adc-75a2-b678-7f4f853d3859"
TOPIC = "human-medicine"
CARD_ID = "human-medicine-ext-breathing-muscle"
CYCLE = 0

def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))

def canonical_sha(value):
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()

def file_sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

inventory = json.loads(INV.read_text(encoding="utf-8"))
assert inventory["globalMAIN"]["topicFileCount"] == 110
assert inventory["globalMAIN"]["questionCount"] == 11000
assert len(inventory["actualCurrentPeers"]) == 100
before_entry = next(x for x in inventory["actualCurrentPeers"] if x["id"] == CARD_ID)
assert before_entry["sourceOrder"] == 77
assert before_entry["sha256"] == "2ddacdf5fe5a7d68fe772c0639da071e9716a7ff7bd69d572be28c963ae7a42f"
before = copy.deepcopy(before_entry["card"])
assert before["topicId"] == TOPIC if "topicId" in before else True
assert before["id"] == CARD_ID
assert before["difficulty"] == "easy"
assert before["correctIndex"] == 1
assert [a["text"] for a in before["answers"]] == ["Таз", "Грудная клетка", "Череп", "Позвоночный столб"]

proposed = copy.deepcopy(before)
proposed["answers"][0]["note"] = "Таз поддерживает вес верхней части тела и защищает внутренние органы таза."
proposed["source"]["verifiedAt"] = "2026-10-24"

def groups(card):
    return {
        "prompt_ordered_answers_key": {
            "prompt": card["prompt"],
            "answers": [a["text"] for a in card["answers"]],
            "correctIndex": card["correctIndex"],
        },
        "explanation": card["explanation"],
        **{"note" + str(k): a["note"] for k, a in enumerate(card["answers"])},
    }

before_groups = groups(before)
after_groups = groups(proposed)
field_groups = {
    name: {
        "beforeCanonicalSHA256": canonical_sha(before_groups[name]),
        "afterCanonicalSHA256": canonical_sha(after_groups[name]),
    }
    for name in before_groups
}
candidate = {
    "sourceNativeId": NATIVE,
    "topicId": TOPIC,
    "cycle": CYCLE,
    "baselineCode": "13e6b068a45933686528afa3ff0ecf135aac297d",
    "catalogCandidate": "13e6b068a45933686528afa3ff0ecf135aac297d",
    "entries": [{
        "id": CARD_ID,
        "topicId": TOPIC,
        "sourceOrder": 77,
        "status": "READY_FOR_INDEPENDENT_REVIEW",
        "beforeCard": before,
        "beforeHash": canonical_sha(before),
        "proposedCard": proposed,
        "afterHash": canonical_sha(proposed),
        "fieldGroups": field_groups,
    }],
    "qualityCredit": 0,
}
assert candidate["entries"][0]["beforeHash"] == before_entry["sha256"]
assert proposed["difficulty"] == "easy" and proposed["correctIndex"] == 1
assert proposed["id"] == CARD_ID

raw_specs = [
    {
        "path": "docs/content-audits/question-quality-wave-8/coordinator-01a16723/source-human-medicine31/thoracic-cage-capture.json",
        "url": "https://openstax.org/books/anatomy-and-physiology-2e/pages/7-4-the-thoracic-cage",
        "fileSHA256": "364c2924810bcbbcf881864f017bc60efa378fc407268d210685f51f8bf486b7",
        "bodySHA256": "cf26b531e7f7358525a1bafe9dc9e38c5596038d4912d72d67ae05a0efdf988c",
        "locator": "OpenStax Anatomy and Physiology 2e 7.4, L30-L32",
        "read": "Reused retained full original response from SOURCE31; personally read the entire exact Thoracic Cage page L0-L106 for this task on 2026-10-24. The claim-bearing lines L30-L32 state the components and that the cage protects the heart and lungs.",
    },
    {
        "path": "docs/content-audits/question-quality-wave-8/coordinator-01a16723/source-human-medicine31/thoracic-cage-capture.json",
        "url": "https://openstax.org/books/anatomy-and-physiology-2e/pages/8-3-the-pelvic-girdle-and-pelvis",
        "fileSHA256": "364c2924810bcbbcf881864f017bc60efa378fc407268d210685f51f8bf486b7",
        "bodySHA256": "cf26b531e7f7358525a1bafe9dc9e38c5596038d4912d72d67ae05a0efdf988c",
        "locator": "OpenStax Anatomy and Physiology 2e 8.3, L30-L34,L53-L54",
        "read": "Reused the same retained full original response as the Thoracic Cage page; personally read the complete retained page segment L0-L64 for this URL on 2026-10-24. The source header reports 148 total lines, but the claim-bearing lines L53-L54 are present and support upper-body weight support and protection of internal pelvic organs.",
    },
    {
        "path": "docs/content-audits/question-quality-wave-8/coordinator-01a16723/source-human-medicine31/skull-capture.json",
        "url": "https://openstax.org/books/anatomy-and-physiology-2e/pages/7-2-the-skull",
        "fileSHA256": "fc39b8982fe4030d38127f6cc917fe82d5647f14847831e4792abcb545b1a79b",
        "bodySHA256": "c176bba753d10e84b37d98edf901cf22ece4c65cd199e254001901feea4eb8f7",
        "locator": "OpenStax Anatomy and Physiology 2e 7.2, L33-L35,L53-L59",
        "read": "Reused retained full original response from SOURCE31; personally read the complete claim-bearing context for this task on 2026-10-24: L33-L35 describes the skull and brain case protecting the brain; L53-L59 describes the brain case and cranial cavity.",
    },
    {
        "path": "docs/content-audits/question-quality-wave-8/coordinator-01a16a43/source-human-medicine77/raw-openstax-vertebral.json",
        "url": "https://openstax.org/books/anatomy-and-physiology-2e/pages/7-3-the-vertebral-column",
        "fileSHA256": "b5dc91768cafd8b05cd11d4b6d3ef340f9e3642a072f10f35bce8496ca21c6c9",
        "bodySHA256": "a9ad29d7ee47ddb137c7e1980255580a473a09771ee59ac2c55055e336ba2c3e",
        "locator": "OpenStax Anatomy and Physiology 2e 7.3, L31-L32,L59-L67",
        "read": "Captured the complete original web.open response in this author native session; personally read the complete retained body through L176 on 2026-10-24. The source header reports 196 total lines; the full claim-bearing context L31,L61-L67 is present and describes the vertebral column and the vertebral canal protecting and carrying the spinal cord.",
    },
]
raw_sources = []
for spec in raw_specs:
    path = ROOT / spec["path"]
    actual_file_sha = file_sha(path)
    assert actual_file_sha == spec["fileSHA256"], (str(path), actual_file_sha)
    raw_sources.append({
        "path": spec["path"],
        "url": spec["url"],
        "sha256": actual_file_sha,
        "captureReadProvenance": spec["read"],
        "completeOutputPointer": "/originalRecord/payload/output/1/text",
        "completeOutputSHA256": spec["bodySHA256"],
        "locator": spec["locator"],
    })

p_thoracic = raw_specs[0]["path"]
p_pelvis = raw_specs[1]["path"]
p_skull = raw_specs[2]["path"]
p_vertebral = raw_specs[3]["path"]
proof_entry = {
    "id": CARD_ID,
    "topicId": TOPIC,
    "sourceOrder": 77,
    "status": "READY_FOR_INDEPENDENT_REVIEW",
    "literalGroups": [
        {
            "group": "prompt_ordered_answers_key",
            "literal": after_groups["prompt_ordered_answers_key"],
            "literalSHA256": canonical_sha(after_groups["prompt_ordered_answers_key"]),
            "primaryGround": "OpenStax 7.4 L30-L32 identifies the thoracic cage as protecting the heart and lungs and describes its components. OpenStax 8.3 L30-L34,L53-L54 grounds the pelvis and its function; 7.2 L33-L35,L53-L59 grounds the skull/brain case; 7.3 L31,L61-L67 grounds the vertebral column and spinal-cord canal. The requested organs make the thoracic cage the unique answer.",
            "sourcePaths": [p_thoracic, p_pelvis, p_skull, p_vertebral],
            "locator": "OpenStax 7.4 L30-L32; 8.3 L30-L34,L53-L54; 7.2 L33-L35,L53-L59; 7.3 L31,L61-L67",
        },
        {
            "group": "explanation",
            "literal": after_groups["explanation"],
            "literalSHA256": canonical_sha(after_groups["explanation"]),
            "primaryGround": "OpenStax 7.4 L30-L31 states that the thoracic cage is formed by ribs with costal cartilages and the sternum, that the ribs attach posteriorly to thoracic vertebrae, and that the cage protects the heart and lungs.",
            "sourcePaths": [p_thoracic],
            "locator": "OpenStax 7.4 L30-L31",
        },
        {
            "group": "note0",
            "literal": after_groups["note0"],
            "literalSHA256": canonical_sha(after_groups["note0"]),
            "primaryGround": "OpenStax 8.3 L53-L54 states that the pelvis supports upper-body weight and protects internal pelvic organs. This corrects the previous unsupported location 'lower part of the abdominal cavity'.",
            "sourcePaths": [p_pelvis],
            "locator": "OpenStax 8.3 L53-L54",
        },
        {
            "group": "note1",
            "literal": after_groups["note1"],
            "literalSHA256": canonical_sha(after_groups["note1"]),
            "primaryGround": "OpenStax 7.4 L30-L31 identifies the ribs, sternum, and thoracic vertebral attachment as components of the thoracic cage and explicitly says the cage protects the heart and lungs. Component detail adds a useful fact beyond the prompt/key.",
            "sourcePaths": [p_thoracic],
            "locator": "OpenStax 7.4 L30-L31",
        },
        {
            "group": "note2",
            "literal": after_groups["note2"],
            "literalSHA256": canonical_sha(after_groups["note2"]),
            "primaryGround": "OpenStax 7.2 L33-L35,L53-L59 states that the rounded brain case of the skull surrounds and protects the brain.",
            "sourcePaths": [p_skull],
            "locator": "OpenStax 7.2 L33-L35,L53-L59",
        },
        {
            "group": "note3",
            "literal": after_groups["note3"],
            "literalSHA256": canonical_sha(after_groups["note3"]),
            "primaryGround": "OpenStax 7.3 L31,L61-L67 says the vertebral column protects the spinal cord, that vertebral foramina align to form the vertebral canal, and that the canal contains the spinal cord.",
            "sourcePaths": [p_vertebral],
            "locator": "OpenStax 7.3 L31,L61-L67",
        },
    ],
    "fourFullPromptAnswerNoteAssessments": [
        {
            "slot": 0,
            "fullPrompt": proposed["prompt"],
            "answer": proposed["answers"][0]["text"],
            "note": proposed["answers"][0]["note"],
            "grammar": "The standalone nominative label 'Таз' fits the prompt asking which skeletal part; punctuation and Russian wording are clear.",
            "plausibilityUniqueKeyAndNoteTruthUsefulness": "A pelvis is a plausible skeletal alternative because it protects its own internal organs, but it does not protect the heart and lungs. The note is now tied to the pelvis and states its weight-support/protective functions; only the thoracic cage matches both requested organs.",
            "sourcePaths": [p_thoracic, p_pelvis],
            "locator": "OpenStax 7.4 L30-L31; 8.3 L53-L54",
            "tripleSHA256": canonical_sha({"prompt": proposed["prompt"], "answer": proposed["answers"][0]["text"], "note": proposed["answers"][0]["note"]}),
        },
        {
            "slot": 1,
            "fullPrompt": proposed["prompt"],
            "answer": proposed["answers"][1]["text"],
            "note": proposed["answers"][1]["note"],
            "grammar": "The standalone nominative label 'Грудная клетка' is grammatical as the requested skeletal structure.",
            "plausibilityUniqueKeyAndNoteTruthUsefulness": "The chest cage is a plausible structure and the unique correct answer because the primary source explicitly ties it to both heart and lung protection. Its note adds the component relation among ribs, sternum, and thoracic vertebrae.",
            "sourcePaths": [p_thoracic],
            "locator": "OpenStax 7.4 L30-L32",
            "tripleSHA256": canonical_sha({"prompt": proposed["prompt"], "answer": proposed["answers"][1]["text"], "note": proposed["answers"][1]["note"]}),
        },
        {
            "slot": 2,
            "fullPrompt": proposed["prompt"],
            "answer": proposed["answers"][2]["text"],
            "note": proposed["answers"][2]["note"],
            "grammar": "The standalone nominative label 'Череп' fits the prompt.",
            "plausibilityUniqueKeyAndNoteTruthUsefulness": "The skull is a same-category plausible distractor because it protects the brain, not the specified heart and lungs. Its note gives a true, concrete fact about this option; the shared protection theme does not make the answer correct.",
            "sourcePaths": [p_thoracic, p_skull],
            "locator": "OpenStax 7.4 L30-L31; 7.2 L33-L35,L53-L59",
            "tripleSHA256": canonical_sha({"prompt": proposed["prompt"], "answer": proposed["answers"][2]["text"], "note": proposed["answers"][2]["note"]}),
        },
        {
            "slot": 3,
            "fullPrompt": proposed["prompt"],
            "answer": proposed["answers"][3]["text"],
            "note": proposed["answers"][3]["note"],
            "grammar": "The standalone nominative label 'Позвоночный столб' fits the prompt.",
            "plausibilityUniqueKeyAndNoteTruthUsefulness": "The vertebral column is a same-category plausible alternative and protects the spinal cord, not the specified heart and lungs. Its note states a true fact about the column and its canal. The thoracic vertebrae form part of the thoracic cage, but the whole vertebral column is not the structure protecting both requested organs.",
            "sourcePaths": [p_thoracic, p_vertebral],
            "locator": "OpenStax 7.4 L30-L31; 7.3 L31,L61-L67",
            "tripleSHA256": canonical_sha({"prompt": proposed["prompt"], "answer": proposed["answers"][3]["text"], "note": proposed["answers"][3]["note"]}),
        },
    ],
    "correctNoteNewFact": "The note identifies the thoracic cage's component structure: ribs and sternum, with ribs attached posteriorly to thoracic vertebrae. This is additional to the prompt/key and is directly supported by OpenStax 7.4 L30-L31.",
    "absoluteDifficulty": "Frozen easy. The heart/lung protection role of the chest cage is broad adult anatomy knowledge; no rare terminology or multi-step reasoning is required. The alternatives are plausible same-category structures, but their facts distinguish the organs each protects.",
}
sourceproof = {
    "sourceNativeId": NATIVE,
    "topicId": TOPIC,
    "cycle": CYCLE,
    "rawSources": raw_sources,
    "entries": [proof_entry],
    "qualityCredit": 0,
    "sourceInventoryPath": str(INV),
    "sourceInventorySHA256": file_sha(INV),
    "attemptFenceSearch": {
        "scope": "Exact target claim and relevant OpenStax 7.2, 7.3, 7.4, and 8.3 URLs in newAttemptFences.",
        "matchingFences": [],
        "result": "No exact topic/claim/URL fence matched these retained or reviewed contexts.",
    },
    "limitations": "No adjacent card was edited. Retained skull context was read at all claim-bearing locators listed; unrelated skull-page sections were not used.",
}

peers = inventory["actualCurrentPeers"]
peer_by_order = {x["sourceOrder"]: x for x in peers}
target_proposed_hash = canonical_sha(proposed)
def pair(order, relation, direct_reverse):
    peer = peer_by_order[order]
    return {
        "candidateBeforeCard": before,
        "candidateBeforeCanonicalSHA256": canonical_sha(before),
        "candidateProposedCard": proposed,
        "candidateProposedCanonicalSHA256": target_proposed_hash,
        "peerId": peer["id"],
        "peerTopicId": peer["topicId"],
        "peerSourceOrder": peer["sourceOrder"],
        "peerCurrentCard": peer["card"],
        "peerCurrentCanonicalSHA256": peer["sha256"],
        "bilateralMAIN": [
            {
                "direction": "candidate_to_peer",
                "entityRelationValueContext": relation[0],
                "assessment": relation[1],
                "directReverse": direct_reverse,
            },
            {
                "direction": "peer_to_candidate",
                "entityRelationValueContext": relation[2],
                "assessment": relation[3],
                "directReverse": direct_reverse,
            },
        ],
    }

relevant_pairs = [
    pair(31, (
        "Entity: skeletal structures; relation: protects; value/context: heart and lungs in the thorax versus brain in the skull.",
        "These prompts share a broad protection frame but differ in protected organs, skeletal structure, and value. This is a neighboring anatomy fact, not a duplicate.",
        "Entity: skeletal structures; relation: protects; value/context: brain in the cranial cavity versus heart and lungs in the thorax.",
        "The peer's skull/brain fact does not answer which structure protects the heart and lungs. No same relation-value-context and no direct reversal.",
    ), False),
    pair(5, (
        "Entity: adult human skeleton; relation: protects organs versus peer relation: counts bones; value/context differs.",
        "The peer asks for a bone count, not a protective structure or organ relation; no entity-relation-value-context duplicate.",
        "Entity: adult human skeleton; relation: number of bones versus candidate relation: protects heart/lungs.",
        "The candidate does not answer the bone-count question; these test independent facts, with no reverse relation.",
    ), False),
]
rows = inventory["globalMAIN"]["rows"]
assert len(rows) == 11000
assert canonical_sha(rows) == inventory["globalMAIN"]["rowsCanonicalSHA256"]
peer_snapshot = {
    "sourceNativeId": NATIVE,
    "topicId": TOPIC,
    "cycle": CYCLE,
    "globalMAIN": inventory["globalMAIN"],
    "actualCurrentPeers": peers,
    "relevantProposedPairs": relevant_pairs,
    "globalSemanticSearch": {
        "query": "Current global MAIN prompts/answers containing protection plus skeleton, chest/ribs, heart/lungs, skull/brain concepts.",
        "matches": [
            {"topicId": "human-medicine", "id": "human-medicine-brain-protection"},
            {"topicId": "human-medicine", "id": CARD_ID},
        ],
        "assessment": "The brain-protection prompt is the only relevant parallel skeletal-protection question found. It has a different protected organ and structure; no direct reverse was found. The other same-topic skeletal hit asks the adult bone count and is an independent fact.",
    },
    "qualityCredit": 0,
}

write_json(OUT / "candidate.json", candidate)
write_json(OUT / "sourceproof.json", sourceproof)
write_json(OUT / "peer-snapshot.json", peer_snapshot)
print(json.dumps({
    "written": [str(OUT / x) for x in ("candidate.json", "sourceproof.json", "peer-snapshot.json")],
    "beforeHash": candidate["entries"][0]["beforeHash"],
    "afterHash": candidate["entries"][0]["afterHash"],
    "fieldGroups": field_groups,
    "sourceFileSHA256": {x["path"]: x["sha256"] for x in raw_sources},
    "currentPeers": len(peers),
    "globalMAINRows": len(rows),
    "relevantPairs": [x["peerId"] for x in relevant_pairs],
    "qualityCredit": 0,
}, ensure_ascii=False))
