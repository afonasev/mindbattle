"""Check delivered identities and review coverage; never infer factual truth from hashes."""
import collections
import hashlib
import json
import re
from pathlib import Path
from functools import lru_cache

ROOT = Path(__file__).resolve().parents[1]
TOPICS = {"racket-sports", "sports", "chess", "geography-russia", "landmarks-wonders"}


def sha(value):
    return hashlib.sha256(value).hexdigest()


def canonical(value):
    return sha(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode())


@lru_cache(maxsize=None)
def file_bytes(path):
    return Path(path).read_bytes()


@lru_cache(maxsize=None)
def file_json(path):
    return json.loads(file_bytes(path))


def read(path):
    return file_json(ROOT / path)


def fields(card):
    return {"prompt-key": card["prompt"] + "\n" + card["answers"][card["correctIndex"]]["text"],
            "explanation": card["explanation"],
            **{f"note{i}": answer["note"] for i, answer in enumerate(card["answers"])}}


def verify():
    audit = read("docs/content-audits/question-quality-wave-3.json")
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
                    assert capture.is_file() and sha(file_bytes(capture)) == source["bodySha256"]
                review = claim["independentReview"]
                assert review["verdict"] == "PASS" and review["reviewer"] not in row["authors"]
                assert review["literalClaimSha256"] == claim["literalClaimSha256"]
                assert review["substantiveRead"] is True
                assert review["artifact"] and review["artifactSha256"]
                artifact = ROOT / "docs/content-audits/question-quality-wave-3" / review["artifact"]
                assert sha(file_bytes(artifact)) == review["artifactSha256"]
                reviewed = file_json(artifact)["currentCardCoverage"][card["id"]]
                assert reviewed["cardCanonicalSha256"] == row["cardCanonicalSha256"]
                assert reviewed["fieldSha256"][claim["field"]] == claim["literalClaimSha256"]
                assert reviewed["verdict"] == "PASS"
                decision = reviewed["editorialDecision"]
                assert decision["independentOfAuthor"] is True
                assert decision["decision"] == "PASS" and decision["reviewer"] == review["reviewer"]
                assert decision["difficultyAndDistractors"]["decision"] == "PASS"
                assert decision["mainFactRelation"]["decision"] == "PASS"
                independent_claim = next(c for c in decision["claims"] if c["field"] == claim["field"])
                assert independent_claim["decision"] == "PASS"
                assert independent_claim["literalClaim"] == claim["literalClaim"]
                assert independent_claim["independentAssessment"]["rationale"]
                for source in independent_claim["provenance"]["sources"]:
                    body = file_bytes(Path(source["durableCapture"]))
                    assert sha(body) == source["bodySha256"]
                    scope = source["independentReadScope"]
                    assert scope["reviewer"] == review["reviewer"] and scope["scope"]
                    passage = file_bytes(Path(scope["independentPassageCapture"]))
                    hashes = source["passageSha256"]
                    if isinstance(hashes, str):
                        hashes = [hashes]
                    assert sha(passage) in hashes, "Independent passage bytes do not match recorded excerpt SHA"
                    locator = source["locator"]
                    if isinstance(locator, dict) and locator.get("lineRanges"):
                        text_lines = Path(locator["textCapture"]).read_text().splitlines()
                        reconstructed = "\n".join(
                            f"{i}: {text_lines[i - 1]}"
                            for start, end in locator["lineRanges"]
                            for i in range(start, end + 1)
                        ) + "\n"
                        assert passage == reconstructed.encode(), "Numbered excerpt differs from retained text body"
                    else:
                        assert passage in body, "Independent excerpt is not contained in retained source body"
                binding_count += 1
    assert binding_count == 3000
    # Whole previous wave1+wave2 cards, including source metadata, are immutable.
    for name in ["question-quality-wave-1", "question-quality-wave-2"]:
        previous = read(f"docs/content-audits/{name}.json")
        for topic in previous["topics"]:
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
    print("PASS: exact500/3000 review bindings;110/11000;IDs/quotas;whole protected1000+20;105 untouched files. Factual truth and difficulty remain substantive editor evidence, not hash inference.")


if __name__ == "__main__":
    verify()
