"""Serialize the independently written decisions; no generated substantive verdicts."""
import hashlib, json, os, re, subprocess
from pathlib import Path

BASE = Path(__file__).resolve().parent
REPO = next(p for p in BASE.parents if (p / 'src/content/topics').is_dir())
AUTHOR = REPO / 'docs/content-audits/question-quality-wave-6/architecture/resume-2026-10-11-author100'
DECISIONS = json.loads((BASE / 'decisions.json').read_text())
assert os.environ['CODEX_THREAD_ID'] == DECISIONS['agentIdentity']
def canonical(v): return json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()
def sha(v): return hashlib.sha256(v).hexdigest()
def save(name, v): (BASE / name).write_text(json.dumps(v, ensure_ascii=False, indent=2) + '\n')
freeze = json.loads((AUTHOR / 'batch01-pilot5-freeze.json').read_text())
author = json.loads((AUTHOR / 'batch01-pilot5-receipt.json').read_text())
all_cards = [(p, c) for p in (REPO / 'src/content/topics').glob('*.json') for c in json.loads(p.read_text())['questions']]
catalog = {c['id']: c for _, c in all_cards}
expected = {r['questionId']: r['cardCanonicalSha256'] for r in freeze['cards']}
assert set(expected) == {r['questionId'] for r in DECISIONS['cards']}
source_index = []
for name, digest in freeze['sourceByteHashes'].items():
    raw = AUTHOR / name
    assert sha(raw.read_bytes()) == digest
    meta = json.loads(Path(str(raw) + '.http.json').read_text())
    assert meta['status'] == '200' and meta['exitCode'] == 0 and meta['sha256'] == digest
    source_index.append({'rawCapture': os.path.relpath(raw, BASE), 'sha256': digest, 'captureFormat': 'html original bytes', 'originalAcquisitionReceipt': os.path.relpath(Path(str(raw) + '.http.json'), BASE), 'role': 'independent', 'agentIdentity': DECISIONS['agentIdentity'], 'reading': 'Complete original HTML text extracted with HTMLParser and read; no image claim made.'})
rows = []
for decision in DECISIONS['cards']:
    qid = decision['questionId']; card = catalog[qid]
    assert sha(canonical(card)) == expected[qid]
    author_row = next(r for r in author['cards'] if r['questionId'] == qid)
    values = {'prompt-key': [card['prompt'], card['correctIndex'], card['answers'][card['correctIndex']]['text']], **{f'note{i}': a['note'] for i, a in enumerate(card['answers'])}, 'explanation': card['explanation']}
    row = {k: decision[k] for k in ('questionId', 'verdict', 'editorialAnalysis')}
    row.update(cardCanonicalSha256=expected[qid], difficulty=card['difficulty'], correctIndex=card['correctIndex'], indexedOptionTexts=[a['text'] for a in card['answers']], fields=[])
    for field, (verdict, analysis) in decision['fields'].items():
        original = next(f for f in author_row['fields'] if f['field'] == field)
        proofs = json.loads(json.dumps(original['proofs']))
        if qid == 'architecture-corinthian-capital-motif' and field == 'note2':
            proofs += json.loads(json.dumps(next(f for f in author_row['fields'] if f['field'] == 'note0')['proofs']))
        if qid == 'architecture-corinthian-capital-motif' and field == 'prompt-key':
            extra = dict(proofs[0]); extra.update(passage='A capital used originally by the Greeks in a system of supports called the Corinthian order.', locator='Corinthian capital / first definition sentence')
            extra['passageSha256'] = sha(extra['passage'].encode()); proofs.append(extra)
        for proof in proofs:
            proof['rawCapture'] = os.path.relpath(AUTHOR / proof['rawCapture'], BASE)
            proof['independentReading'] = 'Original complete captured HTML read directly; passage checked in context, not accepted from author verdict.'
        literal = values[field]
        row['fields'].append({'field': field, 'literal': literal, 'literalSha256': sha(canonical(literal) if field == 'prompt-key' else literal.encode()), 'verdict': verdict, 'substantiveRead': True, 'claimAnalysis': analysis, 'proofs': proofs})
    rows.append(row)
receipt = {'schemaVersion': 1, 'role': 'independent', 'agentIdentity': DECISIONS['agentIdentity'], 'authorIdentity': author['agentIdentity'], 'date': '2026-10-11', 'baselineCommit': '77eff048e9ddc6dcd1eb5c9d9e019d278f266ab5', 'freeze': os.path.relpath(AUTHOR / 'batch01-pilot5-freeze.json', BASE), 'readMethod': DECISIONS['readMethod'], 'mechanicalSerializationOnly': True, 'rootCertification': False, 'cards': rows}
assert receipt['agentIdentity'] != receipt['authorIdentity']
retry = BASE / 'sources/nps-materials-retry.html'
if retry.exists() and retry.read_bytes().rstrip().endswith(b'</html>'):
    passage = 'The legs have double walls of steel 3 feet apart at ground level and 7-3/4 inches apart above the 400-foot level.'
    # Extra proof is used only when the full downloaded original has been read.
    reviewed = BASE / 'nps-reviewed.json'
    if reviewed.exists():
        review = json.loads(reviewed.read_text()); assert review['sha256'] == sha(retry.read_bytes()) and review['substantiveRead'] is True
        rows[-1]['fields'][-1]['proofs'].append({'sourceClass': 'primary official site operator technical history', 'title': 'National Park Service: Materials and Techniques', 'url': 'https://home.nps.gov/jeff/planyourvisit/materials-and-techniques.htm', 'rawCapture': 'sources/nps-materials-retry.html', 'rawCaptureSha256': sha(retry.read_bytes()), 'captureFormat': 'html original bytes', 'captureMethod': 'curl --http1.1 --compressed -L full HTTP response body; see nps-reviewed.json', 'locator': 'Construction of the Arch / paragraph beginning It takes the shape of an inverted catenary curve', 'passage': passage, 'passageSha256': sha(passage.encode())})
save('receipt.json', receipt)
save('cards-read.json', [catalog[qid] for qid in expected])
save('originals-read-index.json', source_index)
pattern = r'коринфск|акант|капител|пандатив|пандантив|куполь|купол|полусфер|колонн|цилиндрическ.{0,25}опор|\bарк[аиу]?\b|арочн|проём|проем'
regex = re.compile(pattern, re.I)
candidates = [{'topic': p.stem, 'questionId': c['id'], 'prompt': c['prompt'], 'key': c['answers'][c['correctIndex']]['text']} for p, c in all_cards if regex.search(c['prompt'] + ' ' + c['answers'][c['correctIndex']]['text'])]
save('duplicate-candidates.json', {'selectionPattern': pattern, 'scope': 'Read-only prompt/key candidate scan across current catalog, not rereview or certification of other cards.', 'catalogCards': len(all_cards), 'candidates': candidates, 'pilotPrimaryFacts': ['Corinthian/acanthus decoration', 'pendentive square-to-circle transition', 'column cylindrical support term', 'dome hemispherical vault term', 'arch curved opening-spanning member'], 'manualConclusion': 'No competing primary fact for these five cards in inspected candidates. Shape of Gothic arch, Pantheon oculus, entasis, Villa Savoye pilotis, named monument authors/materials/locations ask distinct facts. Other-card quality is outside this receipt.'})
print(json.dumps({'cards': len(rows), 'fields': sum(len(r['fields']) for r in rows), 'cardVerdicts': {v: sum(r['verdict'] == v for r in rows) for v in ('PASS', 'FIX_REQUIRED', 'HOLD')}, 'role': receipt['role'], 'identity': receipt['agentIdentity']}, ensure_ascii=False))
