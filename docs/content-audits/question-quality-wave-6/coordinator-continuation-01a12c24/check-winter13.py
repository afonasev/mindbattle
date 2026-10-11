"""Mechanical checks only; the explicit thirteen decisions were made by the coordinator."""
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], text=True).strip())
AUDIT = ROOT / 'docs/content-audits/question-quality-wave-6'
IDS = ['winter-sports-010', 'winter-sports-016', 'winter-sports-018', 'winter-sports-020',
       'winter-sports-001', 'winter-sports-002', 'winter-sports-003', 'winter-sports-004',
       'winter-sports-005', 'winter-sports-015', 'winter-sports-021', 'winter-sports-006', 'winter-sports-022']
PAIRS = [('43004f5', 'winter-sports/resume-2026-10-11-fix19/receipt.json'),
         ('51a9d53', 'independent-pilot/resume-2026-10-11-winter-current89/receipt.json')]

def sha(value):
    return hashlib.sha256(value).hexdigest()

def canonical(value):
    return sha(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode())

def literal_hash(value):
    return sha(value.encode()) if isinstance(value, str) else canonical(value)

cards = {q['id']: q for q in json.loads((ROOT / 'src/content/topics/winter-sports.json').read_text())['questions']}
records, sources, identities = [], {}, []
for revision, relative in PAIRS:
    path = AUDIT / relative
    receipt = json.loads(subprocess.check_output(['git', 'show', revision + ':' + str(path.relative_to(ROOT))]))
    identities.append(receipt['agentIdentity'])
    indexed = {c['questionId']: c for c in receipt['cards']}
    for qid in IDS:
        read, card = indexed[qid], cards[qid]
        digest = canonical(card)
        assert read['cardCanonicalSha256'] == digest, (qid, 'card hash')
        assert read['verdict'] == 'PASS', (qid, 'card verdict')
        fields = {f['field']: f for f in read['fields']}
        literals = {'prompt-key': [card['prompt'], card['correctIndex'], card['answers'][card['correctIndex']]['text']],
                    **{f'note{n}': a['note'] for n, a in enumerate(card['answers'])}, 'explanation': card['explanation']}
        assert set(fields) == set(literals), (qid, 'six fields')
        for key, field in fields.items():
            assert field['verdict'] == 'PASS' and field['substantiveRead'], (qid, key, 'verdict')
            assert field['literal'] == literals[key], (qid, key, 'literal')
            assert field['literalSha256'] == literal_hash(literals[key]), (qid, key, 'literal hash')
            assert field['claimAnalysis'] and field['proofs'], (qid, key, 'analysis/proofs')
            for proof in field['proofs']:
                assert proof['reader'] == receipt['agentIdentity'], (qid, key, 'reader')
                assert proof['passageSha256'] == sha(proof['passage'].encode()), (qid, key, 'passage hash')
                assert proof['locator'] and proof['sourceClass'] and proof['captureFormat']
                assert proof['url'].startswith('https://')
                raw = (path.parent / proof['rawCapture']).resolve()
                relative_raw = raw.relative_to(ROOT)
                declared = proof['rawCaptureSha256']
                assert sha(raw.read_bytes()) == declared, (qid, key, 'disk original', str(relative_raw))
                blob = subprocess.check_output(['git', 'show', 'HEAD:' + str(relative_raw)])
                assert sha(blob) == declared, (qid, key, 'Git original', str(relative_raw))
                sources[str(relative_raw)] = declared
                if receipt['role'] == 'independent':
                    assert proof['boundCardCanonicalSha256'] == digest
                    assert proof['boundFieldLiteralSha256'] == field['literalSha256']
                    assert proof['readerRole'] == 'independent'
        records.append({'questionId': qid, 'role': receipt['role'], 'cardCanonicalSha256': digest, 'fields': 6})
assert len(set(identities)) == 2
report = {'owner': '01a12c24-1e62-75d0-a2f9-7f8de2851311',
          'method': 'Mechanical identity/raw-byte/literal checks only. Frozen receipts read from Git. No substantive PASS inferred.',
          'explicitApprovedIds': IDS, 'frozenReceipts': PAIRS, 'actualRoleIdentities': identities,
          'records': records, 'workingAndGitRawBindings': sources, 'errors': 0,
          'excluded': {'winter-sports-019': 'Independent difficulty HOLD; not certified'}}
(Path(__file__).parent / 'winter13-binding-and-bytes.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'roleCardRecords': len(records), 'exactOriginals': len(sources), 'explicitCards': 13, 'errors': 0}))
