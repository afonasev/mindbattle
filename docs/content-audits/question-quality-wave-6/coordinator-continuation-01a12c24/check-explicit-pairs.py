"""Validate bindings for explicitly supplied decisions; never choose IDs or infer a verdict."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], text=True).strip())
CONFIG = Path(sys.argv[1]).resolve()
config = json.loads(CONFIG.read_text())
cards = {}
for topic in config['topics']:
    cards.update({q['id']: q for q in json.loads((ROOT / f'src/content/topics/{topic}.json').read_text())['questions']})

def sha(value):
    return hashlib.sha256(value).hexdigest()

def canonical(value):
    return sha(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode())

def literal_hash(value, algorithm):
    assert algorithm in ('canonical-json', 'utf8-strings-canonical-arrays')
    return sha(value.encode()) if algorithm == 'utf8-strings-canonical-arrays' and isinstance(value, str) else canonical(value)

records, originals, role_bindings = [], {}, []
for group in config['explicitGroups']:
    identities = []
    for reading in group['pairedReceipts']:
        path = ROOT / reading['path']
        receipt = json.loads(subprocess.check_output(['git', 'show', reading['commit'] + ':' + reading['path']]))
        identity = receipt['agentIdentity']
        assert identity == reading['actualNativeIdentity'], 'actual role identity'
        identities.append(identity)
        by_id = {c['questionId']: c for c in receipt['cards']}
        for qid in group['explicitApprovedIds']:
            read, card = by_id[qid], cards[qid]
            digest = canonical(card)
            assert read['cardCanonicalSha256'] == digest, (qid, 'whole card hash')
            assert read['verdict'] == 'PASS', (qid, 'explicit paired verdict')
            fields = {f['field']: f for f in read['fields']}
            literals = {'prompt-key': [card['prompt'], card['correctIndex'], card['answers'][card['correctIndex']]['text']],
                        **{f'note{n}': a['note'] for n, a in enumerate(card['answers'])}, 'explanation': card['explanation']}
            assert set(fields) == set(literals), (qid, 'six indexed fields')
            for key, field in fields.items():
                assert field['verdict'] == 'PASS' and field['substantiveRead'], (qid, key, 'recorded read/verdict')
                if 'literal' in field:
                    assert field['literal'] == literals[key], (qid, key, 'indexed literal')
                assert field['literalSha256'] == literal_hash(literals[key], reading['literalHashAlgorithm']), (qid, key, 'literal hash')
                assert field['claimAnalysis'] and field['proofs'], (qid, key, 'recorded analysis/proof')
                for proof in field['proofs']:
                    if 'reader' in proof:
                        assert proof['reader'] == identity, (qid, key, 'proof role')
                    assert proof['passageSha256'] == sha(proof['passage'].encode()), (qid, key, 'quoted passage hash')
                    assert proof['locator'] and proof['sourceClass'] and proof['captureFormat']
                    assert proof['url'].startswith('https://')
                    capture = proof['rawCapture']
                    # A repository-root path is explicit; otherwise paths are receipt-relative.
                    raw = ((ROOT if capture.startswith('docs/') else path.parent) / capture).resolve()
                    relative_raw = str(raw.relative_to(ROOT))
                    expected = proof['rawCaptureSha256']
                    assert sha(raw.read_bytes()) == expected, (qid, key, 'working original', relative_raw)
                    assert sha(subprocess.check_output(['git', 'show', 'HEAD:' + relative_raw])) == expected, (qid, key, 'Git original', relative_raw)
                    originals[relative_raw] = expected
                    role_bindings.append({'questionId': qid, 'cardCanonicalSha256': digest, 'field': key,
                                          'fieldLiteralSha256': field['literalSha256'], 'actualRole': reading['actualRole'],
                                          'actualNativeIdentity': identity, 'sourceClass': proof['sourceClass'],
                                          'rawPath': relative_raw, 'rawSha256': expected, 'fieldLocator': proof['locator']})
            records.append({'questionId': qid, 'role': reading['actualRole'], 'cardCanonicalSha256': digest, 'fields': 6})
    assert len(set(identities)) == 2, 'actual distinct roles'
report = {'method': 'Mechanical bindings for explicitly supplied coordinator decisions; no substantive verdict generated.',
          'config': str(CONFIG.relative_to(ROOT)), 'records': records, 'actualRoleFieldSourceBindings': role_bindings,
          'workingAndCommittedOriginals': originals, 'errors': 0}
output = CONFIG.parent / config['bindingReport']
output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'roleCardRecords': len(records), 'exactOriginals': len(originals), 'errors': 0}))
