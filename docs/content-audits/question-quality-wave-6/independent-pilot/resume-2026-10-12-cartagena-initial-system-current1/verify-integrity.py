"""Evidence integrity only; does not decide source/editorial verdicts."""
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[5]
assert subprocess.check_output(["git", "rev-parse", "--show-toplevel"], cwd=ROOT).decode().strip() == str(ROOT)
OWN = Path(__file__).resolve().parent
r = json.loads((OWN / "independent-receipt.json").read_text())

def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()

raw = (ROOT / r["sourceOriginal"]["ownedCapturePath"]).read_bytes()
assert len(raw) == r["sourceOriginal"]["byteLength"]
assert sha(raw) == r["sourceOriginal"]["rawSHA256"]
assert raw == git("cat-file", "blob", r["sourceOriginal"]["gitBlob"])
text = json.loads(raw)["results"][0]["justification_en"]
source = (ROOT / r["currentSourceFile"]).read_bytes()
assert sha(source) == r["currentSourceFileSHA256"]
assert source == git("show", r["authorSourceCommit"] + ":" + r["currentSourceFile"])
assert git("hash-object", r["currentSourceFile"]).decode().strip() == r["currentSourceGitBlob"]
topic = json.loads(source)
card = next(q for q in topic["questions"] if q["id"] == "architecture-cartagena")
assert card == r["currentCard"]
assert sha(canonical(card)) == r["wholeCardCurrentSha256"]
parent = json.loads(git("show", r["authorParent"] + ":" + r["currentSourceFile"]))
protected = [q for q in topic["questions"] if q["id"] != card["id"]]
assert protected == [q for q in parent["questions"] if q["id"] != card["id"]]
assert len(protected) == 99 and len(topic["questions"]) == 100
assert sha(canonical(protected)) == r["invariants"]["protected99CanonicalSHA256"]
assert [(q["id"], q["difficulty"], q["correctIndex"]) for q in topic["questions"]] == [(q["id"], q["difficulty"], q["correctIndex"]) for q in parent["questions"]]
assert sha((ROOT / r["authorReceiptPath"]).read_bytes()) == r["authorReceiptSHA256"]
for i, field in enumerate(r["fields"]):
    literal = ({"prompt": card["prompt"], "answers": [a["text"] for a in card["answers"]], "correctIndex": card["correctIndex"], "key": card["answers"][card["correctIndex"]]["text"]} if i == 0 else card["answers"][i-1]["note"] if i < 5 else card["explanation"])
    assert literal == field["currentLiteral"]
    assert sha(canonical(literal)) == field["currentLiteralSha256"] == field["authorDeclaredNativeLiteralSha256"]
    assert sha(canonical(literal) if i == 0 else literal.encode()) == field["readerNativeLiteralSha256"]
    for proof in field["sourceProofs"]:
        quote = text[proof["characterOffset"]:proof["characterOffset"] + proof["characterLength"]]
        assert quote == proof["exactQuote"] and sha(quote.encode()) == proof["exactQuoteSHA256"]
        context = text[proof["contextStart"]:proof["contextEnd"]]
        assert context == proof["context"] and sha(context.encode()) == proof["contextSHA256"]
review = (ROOT / r["invariants"]["reviewPath"]).read_bytes()
assert sha(review) == r["invariants"]["reviewSHA256"]
assert review == git("show", r["authorParent"] + ":" + r["invariants"]["reviewPath"])
assert r["readerNativeIdentity"] != r["authorNativeIdentity"]
print("Integrity PASS: six literal/native bindings; raw/source/quotes; protected99; review counters unchanged.")
