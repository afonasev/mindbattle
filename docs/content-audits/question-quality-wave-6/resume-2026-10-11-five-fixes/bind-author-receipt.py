"""Bind manually authored decisions to exact current literals and original captures.

This adapter does not decide any substantive verdict or create coverage. Human
verdicts and analyses are read from manual-decisions.json; checks are limited to
identity, current hashes, raw byte hashes, and passage existence.
"""
import hashlib
import json
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[3]


class VisibleText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
        self.hidden = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.hidden += 1

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.hidden = max(0, self.hidden - 1)

    def handle_data(self, data):
        if not self.hidden:
            self.parts.append(data)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode("utf-8")


def visible_text(path, raw):
    if path.suffix.lower() in (".html", ".htm"):
        parser = VisibleText()
        parser.feed(raw.decode("utf-8"))
        return " ".join(parser.parts)
    return raw.decode("utf-8")


def card_fields(card):
    return {
        "prompt-key": canonical([
            card["prompt"], card["correctIndex"],
            card["answers"][card["correctIndex"]]["text"],
        ]),
        **{f"note{i}": answer["note"].encode("utf-8")
           for i, answer in enumerate(card["answers"])},
        "explanation": card["explanation"].encode("utf-8"),
    }


def main():
    manual = json.loads((ROOT / "manual-decisions.json").read_text())
    proof_index = json.loads((ROOT / "proof-index.json").read_text())["proofs"]
    catalog = {}
    for path in (REPO / "src/content/topics").glob("*.json"):
        topic = json.loads(path.read_text())
        catalog.update({card["id"]: card for card in topic["questions"]})

    errors = []
    output_cards = []
    for decision in manual["cards"]:
        qid = decision["questionId"]
        card = catalog.get(qid)
        if card is None:
            errors.append(f"unknown question ID: {qid}")
            continue
        expected = card_fields(card)
        if sorted(row["field"] for row in decision["fields"]) != sorted(expected):
            errors.append(f"{qid}: manual decisions do not contain exactly six fields")
        output_fields = []
        for row in decision["fields"]:
            name = row["field"]
            if name not in expected:
                errors.append(f"{qid}/{name}: unexpected field")
                continue
            output_proofs = []
            for proof_id in row["proofIds"]:
                spec = proof_index.get(proof_id)
                if spec is None:
                    errors.append(f"{qid}/{name}: unknown proof ID {proof_id}")
                    continue
                source = (ROOT / spec["rawCapture"]).resolve()
                if not source.is_file():
                    errors.append(f"{qid}/{name}: missing original {source}")
                    continue
                raw = source.read_bytes()
                passage = spec["passage"]
                extracted = visible_text(source, raw)
                if passage not in extracted and " ".join(passage.split()) not in " ".join(extracted.split()):
                    errors.append(f"{qid}/{name}: passage is absent from {spec['rawCapture']}")
                    continue
                output_proofs.append({
                    key: spec[key] for key in (
                        "sourceClass", "title", "url", "rawCapture",
                        "captureFormat", "captureMethod", "locator", "passage",
                    )
                } | {
                    "rawCaptureSha256": sha(raw),
                    "passageSha256": sha(passage.encode("utf-8")),
                })
            output_fields.append({
                "field": name,
                "literalSha256": sha(expected[name]),
                "verdict": row["verdict"],
                "substantiveRead": row["substantiveRead"],
                "claimAnalysis": row["claimAnalysis"],
                "proofs": output_proofs,
            })
        output_cards.append({
            "questionId": qid,
            "cardCanonicalSha256": sha(canonical(card)),
            "verdict": decision["verdict"],
            "editorialAnalysis": decision["editorialAnalysis"],
            "fields": output_fields,
        })

    if errors:
        (ROOT / "binding-errors.json").write_text(json.dumps(errors, ensure_ascii=False, indent=2) + "\n")
        raise SystemExit("Receipt binding failed; see binding-errors.json")

    receipt = {
        "role": manual["role"],
        "agentIdentity": manual["agentIdentity"],
        "cards": output_cards,
        "bindingLimits": [
            "Manual decisions were copied from manual-decisions.json; this adapter creates no substantive verdicts.",
            "Only current-card hashes, literal hashes, source byte hashes, and passage existence are checked.",
            "Independent review and coordinator certification remain separate.",
        ],
    }
    (ROOT / "author-receipt.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({
        "role": receipt["role"],
        "agentIdentity": receipt["agentIdentity"],
        "cards": len(receipt["cards"]),
        "fields": sum(len(row["fields"]) for row in receipt["cards"]),
        "manualVerdictsCopied": True,
        "newSubstantiveVerdictsCreated": 0,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
