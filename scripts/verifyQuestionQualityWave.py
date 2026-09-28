"""Verify the exact delivered wave against its field-bound audit; no truth inference."""
import collections
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sha = lambda value: hashlib.sha256(value).hexdigest()
canonical = lambda value: sha(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode())

def read(relative):
    return json.loads((ROOT / relative).read_text())


def verify():
    audit = read("docs/content-audits/question-quality-wave-1.json")
    topics = {path.stem: json.loads(path.read_text()) for path in (ROOT / "src/content/topics").glob("*.json")}
    assert len(topics) == 110
    cards = {card["id"]: card for topic in topics.values() for card in topic["questions"]}
    assert len(cards) == 11000
    count = 0
    assert len(audit["topics"]) == 5
    for reviewed in audit["topics"]:
        topic_id = reviewed["topicId"]
        path = ROOT / f"src/content/topics/{topic_id}.json"
        questions = topics[topic_id]["questions"]
        assert sha(path.read_bytes()) == reviewed["topicFileBytesSha256"], topic_id
        assert len(questions) == len(reviewed["cards"]) == 100
        assert collections.Counter(q["difficulty"] for q in questions) == {"easy": 40, "medium": 40, "hard": 20}
        for difficulty, expected in [("easy", 10), ("medium", 10), ("hard", 5)]:
            assert collections.Counter(q["correctIndex"] for q in questions if q["difficulty"] == difficulty) == {i: expected for i in range(4)}
        for row in reviewed["cards"]:
            card = questions[row["index"]]
            assert canonical(card) == row["cardCanonicalSha256"], card["id"]
            fields = {"prompt-key": card["prompt"] + "\n" + card["answers"][card["correctIndex"]]["text"], "explanation": card["explanation"], **{f"note{i}": answer["note"] for i, answer in enumerate(card["answers"])}}
            assert len(row["claims"]) == 6
            assert {claim["field"] for claim in row["claims"]} == set(fields)
            for claim in row["claims"]:
                assert claim["literalClaim"] == fields[claim["field"]]
                assert sha(claim["literalClaim"].encode()) == claim["literalClaimSha256"]
                assert claim["provenance"]["sources"]
                assert all(source["url"].startswith("https://") and source["locator"] for source in claim["provenance"]["sources"])
                count += 1
    assert count == 3000
    pilot = read("docs/content-audits/question-quality-batch-1.json")
    assert len(pilot["cards"]) == 20
    for entry in pilot["cards"]:
        accepted = entry["candidate"]
        assert cards[accepted["id"]] == accepted, accepted["id"]
    extra = audit["outsideWaveCompensation"]
    assert sha((ROOT / "src/content/topics/human-medicine.json").read_bytes()) == extra["topicFileBytesSha256"]
    card = cards[extra["questionId"]]
    fields = {"prompt-key": card["prompt"] + "\n" + card["answers"][card["correctIndex"]]["text"], "explanation": card["explanation"], **{f"note{i}": answer["note"] for i, answer in enumerate(card["answers"])}}
    assert len(extra["claims"]) == 6
    for claim in extra["claims"]:
        assert claim["literalClaim"] == fields[claim["field"]]
        assert sha(claim["literalClaim"].encode()) == claim["literalClaimSha256"]
    print("PASS: exact500/3000 bindings, joint quotas,20 accepted whole cards,1 external CDC/6 bindings. Source reads remain provenance evidence, not inferred by this check.")


if __name__ == "__main__":
    verify()
