#!/usr/bin/env python3
"""Verify exactly-one-card audit evidence and native raw Git byte preservation."""
import hashlib
import json
import subprocess
from html.parser import HTMLParser
from pathlib import Path

HERE = Path(__file__).parent
R = json.loads((HERE / "reader-receipt.json").read_text())
def sha(b):
    return hashlib.sha256(b).hexdigest()
def canonical(v):
    return json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
def git_bytes(rev, p):
    return subprocess.check_output(["git", "show", rev + ":" + str(p)])
class Text(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
    def handle_data(self, value):
        self.parts.append(value)
def text(value):
    parser = Text()
    parser.feed(value)
    return "".join(parser.parts)
card = json.loads((HERE / "current-card.json").read_bytes())
assert sha(canonical(card)) == R["cardCanonicalSha256"]
assert card["id"] == R["questionId"]
assert card["difficulty"] == "medium" and card["correctIndex"] == 0
frozen = git_bytes(R["frozenEvidenceCommit"], R["sourceFrozenPath"])
assert sha(frozen) == R["topicFileSha256"]
current = Path(R["sourceFrozenPath"]).read_bytes()
assert current == frozen
for rev in [R["frozenEvidenceCommit"], "HEAD"]:
    questions = json.loads(git_bytes(rev, R["sourceFrozenPath"]))["questions"]
    c = next(c for c in questions if c["id"] == R["questionId"])
    assert canonical(c) == canonical(card)
assert len(R["fields"]) == 6
assert {f["field"] for f in R["fields"]} == {"prompt-key", "note0", "note1", "note2", "note3", "explanation"}
for field in R["fields"]:
    name = field["field"]
    literal = (json.dumps([card["prompt"], card["correctIndex"], card["answers"][0]["text"]], ensure_ascii=False, separators=(",", ":")).encode() if name == "prompt-key" else (card["explanation"] if name == "explanation" else card["answers"][int(name[-1])]["note"]).encode())
    assert sha(literal) == field["literalSha256"]
    assert literal.decode() == field["literalUtf8"]
    for proof in field["proofs"]:
        source = next(s for s in R["sources"] if s["rawCapture"] == proof["rawCapture"])
        raw = Path(source["rawCapture"]).read_bytes()
        assert sha(raw) == source["rawCaptureSha256"] == proof["rawCaptureSha256"]
        decoded = raw.decode(source["encoding"])
        if source["rawType"] == "json":
            decoded = json.loads(decoded)["content"][0]["content"][0]
        assert proof["quotedPassage"] in text(decoded)
        assert sha(proof["quotedPassage"].encode()) == proof["quotedPassageSha256"]
rows = []
for source in R["sources"]:
    p = source["rawCapture"]
    working = Path(p).read_bytes()
    original = git_bytes(R["frozenEvidenceCommit"], source["originalGitPath"])
    staged = git_bytes("", p)  # git show :path
    assert working == original == staged
    attr = subprocess.check_output(["git", "check-attr", "text", "--", p]).decode().strip()
    assert attr.endswith(": unset"), attr
    rows.append({"path": p, "sha256": sha(working), "bytes": len(working), "gitIndexRoundtrip": True, "textAttribute": "unset"})
print(json.dumps({"questionId": R["questionId"], "cardCanonicalSha256": R["cardCanonicalSha256"], "counts": R["counts"], "rawRoundtrip": rows}, ensure_ascii=False, indent=2))
