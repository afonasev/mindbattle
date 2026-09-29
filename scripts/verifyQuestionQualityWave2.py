"""Check delivered identities and review coverage; never infer factual truth from hashes."""
import collections
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOPICS = {"russian-music", "world-pop-music", "math-logic", "world-history", "world-geography"}


def sha(value):
    return hashlib.sha256(value).hexdigest()


def canonical(value):
    return sha(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode())


def read(path):
    return json.loads((ROOT / path).read_text())


def fields(card):
    return {"prompt-key": card["prompt"] + "\n" + card["answers"][card["correctIndex"]]["text"],
            "explanation": card["explanation"],
            **{f"note{i}": answer["note"] for i, answer in enumerate(card["answers"])}}


def verify():
    audit = read("docs/content-audits/question-quality-wave-2.json")
    topics = {p.stem: json.loads(p.read_text()) for p in (ROOT / "src/content/topics").glob("*.json")}
    assert len(topics) == 110
    cards = {c["id"]: c for topic in topics.values() for c in topic["questions"]}
    assert len(cards) == 11000
    assert {t["topicId"] for t in audit["topics"]} == TOPICS
    assert audit["technicalStatus"] == "all500-substantively-reviewed"
    assert audit["unresolvedFindings"] == []
    binding_count = 0
    for topic in audit["topics"]:
        topic_id = topic["topicId"]
        questions = topics[topic_id]["questions"]
        assert sha((ROOT / f"src/content/topics/{topic_id}.json").read_bytes()) == topic["topicFileBytesSha256"]
        assert len(questions) == len(topic["cards"]) == 100
        assert [c["id"] for c in questions] == topic["originalOrderedIds"]
        assert collections.Counter(c["difficulty"] for c in questions) == {"easy": 40, "medium": 40, "hard": 20}
        for level, count in [("easy", 10), ("medium", 10), ("hard", 5)]:
            assert collections.Counter(c["correctIndex"] for c in questions if c["difficulty"] == level) == {i: count for i in range(4)}
        assert {r["index"] for r in topic["cards"]} == set(range(100))
        for row in topic["cards"]:
            card = questions[row["index"]]
            assert row["questionId"] == card["id"]
            assert canonical(card) == row["cardCanonicalSha256"]
            assert sha(card["prompt"].encode()) == row["promptSha256"]
            assert [sha(a["text"].encode()) for a in card["answers"]] == row["optionTextSha256"]
            assert len(card["explanation"].split()) <= 70
            assert 2 <= len(re.findall(r"[.!?](?:\s|$)", card["explanation"])) <= 4
            expected = fields(card)
            assert len(row["claims"]) == 6
            assert {c["field"] for c in row["claims"]} == set(expected)
            for claim in row["claims"]:
                assert claim["literalClaim"] == expected[claim["field"]]
                assert sha(claim["literalClaim"].encode()) == claim["literalClaimSha256"]
                assert claim["provenance"]["sources"]
                for source in claim["provenance"]["sources"]:
                    assert source["url"].startswith("https://") and source["locator"]
                    assert source["bodySha256"] and len(source["bodySha256"]) == 64
                    capture = Path(source["durableCapture"])
                    assert capture.is_file() and sha(capture.read_bytes()) == source["bodySha256"]
                review = claim["independentReview"]
                assert review["verdict"] == "PASS" and review["reviewer"] not in row["authors"]
                assert review["literalClaimSha256"] == claim["literalClaimSha256"]
                assert review["substantiveRead"] is True
                assert review["artifact"] and review["artifactSha256"]
                artifact = ROOT / "docs/content-audits/question-quality-wave-2" / review["artifact"]
                assert sha(artifact.read_bytes()) == review["artifactSha256"]
                reviewed = json.loads(artifact.read_text())["currentCardCoverage"][card["id"]]
                assert reviewed["cardCanonicalSha256"] == row["cardCanonicalSha256"]
                assert reviewed["fieldSha256"][claim["field"]] == claim["literalClaimSha256"]
                assert reviewed["verdict"] == "PASS"
                binding_count += 1
    assert binding_count == 3000
    # Whole accepted wave1 cards, including source metadata, are immutable.
    wave1 = read("docs/content-audits/question-quality-wave-1.json")
    for topic in wave1["topics"]:
        for row in topic["cards"]:
            assert canonical(cards[row["questionId"]]) == row["cardCanonicalSha256"], row["questionId"]
    pilot = read("docs/content-audits/question-quality-batch-1.json")
    assert len(pilot["cards"]) == 20
    for row in pilot["cards"]:
        assert cards[row["candidate"]["id"]] == row["candidate"]
    assert len(audit["outsideWaveTopicFileHashes"]) == 105
    for topic_id, digest in audit["outsideWaveTopicFileHashes"].items():
        assert topic_id not in TOPICS
        assert sha((ROOT / f"src/content/topics/{topic_id}.json").read_bytes()) == digest, topic_id
    assert audit["catalogReview"]["topicCount"] == 110
    assert audit["catalogReview"]["questionCount"] == 11000
    assert audit["catalogReview"]["confirmedRemainingDuplicates"] == []
    print("PASS: exact500/3000 review bindings;110/11000;IDs/quotas;whole accepted500+20;105 untouched files. Factual truth and difficulty remain substantive editor evidence, not hash inference.")


if __name__ == "__main__":
    verify()
