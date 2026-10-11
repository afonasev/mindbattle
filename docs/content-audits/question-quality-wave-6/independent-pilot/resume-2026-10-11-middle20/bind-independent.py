"""Bind manually written independent judgments; never generate a judgment."""
import hashlib
import json
import os
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
AUTHOR = REPO / 'docs/content-audits/question-quality-wave-6/middle-ages/resume-2026-10-11-batch20'
IDENTITY = '01a12b59-563f-7102-816b-105461e96a3c'
def digest(value): return hashlib.sha256(value).hexdigest()
def canonical(value): return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()
manual = json.loads((HERE / 'manual-decisions.json').read_text())
remaining = HERE / 'manual-remaining-decisions.json'
if remaining.exists():
    manual += json.loads(remaining.read_text())
frozen = {c['id']: c for c in json.loads((HERE / 'freeze.json').read_text())['snapshot']}
source_index = {c['questionId']: c for c in json.loads((AUTHOR / 'author-current.json').read_text())['cards']}
additional = json.loads((HERE / 'additional-proof-locators.json').read_text())
receipt = {'role': 'independent', 'agentIdentity': IDENTITY,
           'method': 'Own literal readings and decisions in manual-decisions.json. Author receipt reused solely as source/quote index; no author judgment imported. Existing committed originals read independently. Mechanical binding creates no verdict.', 'cards': []}
for decision in manual:
    qid = decision['questionId']; card = frozen[qid]
    row = {k: decision[k] for k in ('questionId', 'verdict', 'editorialAnalysis')}
    row['cardCanonicalSha256'] = digest(canonical(card)); row['fields'] = []
    original_fields = {f['field']: f for f in source_index[qid]['fields']}
    for name, verdict, analysis in decision['fields']:
        scalar = canonical([card['prompt'], card['correctIndex'], card['answers'][card['correctIndex']]['text']]) if name == 'prompt-key' else (card['explanation'] if name == 'explanation' else card['answers'][int(name[-1])]['note']).encode()
        literal_hash = digest(scalar); proofs = []
        indexed = list(original_fields[name]['proofs'])
        for add_id, add_field, add_source, line_number in additional:
            if (add_id, add_field) != (qid, name):
                continue
            template = next(p for c in source_index.values() for f in c['fields'] for p in f['proofs'] if p['rawCapture'] == add_source)
            original_text = (AUTHOR / add_source).read_text()
            match = re.search(r'^L' + str(line_number) + r': (.*)$', original_text, re.M)
            assert match, (add_source, line_number)
            quote = match.group(1)
            indexed.append({**template, 'passage': quote, 'passageSha256': digest(quote.encode()), 'locator': 'L' + str(line_number)})
        for original in indexed:
            proof = {k: v for k, v in original.items() if k not in ('readerRole', 'readerIdentity', 'boundCardCanonicalSha256', 'boundFieldLiteralSha256')}
            raw = (AUTHOR / proof['rawCapture']).resolve()
            proof['rawCapture'] = os.path.relpath(raw, HERE)
            assert digest(raw.read_bytes()) == proof['rawCaptureSha256']
            assert digest(proof['passage'].encode()) == proof['passageSha256']
            proof.update(readerRole='independent', readerIdentity=IDENTITY, boundCardCanonicalSha256=row['cardCanonicalSha256'], boundFieldLiteralSha256=literal_hash)
            proofs.append(proof)
        row['fields'].append({'field': name, 'literalSha256': literal_hash, 'verdict': verdict, 'substantiveRead': True, 'claimAnalysis': analysis, 'proofs': proofs})
    assert {f['field'] for f in row['fields']} == {'prompt-key', 'note0', 'note1', 'note2', 'note3', 'explanation'}
    receipt['cards'].append(row)
(HERE / 'independent-current.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n')
print('Bound existing manual decisions:', len(receipt['cards']))
