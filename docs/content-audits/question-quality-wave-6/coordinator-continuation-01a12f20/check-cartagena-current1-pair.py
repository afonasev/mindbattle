"""Preserve native binding recipes; manual coordinator judgment is separate."""
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle')
BASE = ROOT / 'docs/content-audits/question-quality-wave-6'
OUT = BASE / 'coordinator-continuation-01a12f20'
def sha(b): return hashlib.sha256(b).hexdigest()
def cj(v): return json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()
def git(rev, path): return subprocess.check_output(['git', '-C', str(ROOT), 'show', rev + ':' + str(path.relative_to(ROOT))])
q = next(c for c in json.loads((ROOT / 'src/content/topics/architecture.json').read_text())['questions'] if c['id'] == 'architecture-cartagena')
binding = json.loads((OUT / 'cartagena-author-native-role.json').read_text())
aid = binding['authorNativeIdentity']
reads = [('author', aid, '066dd11', 'architecture/resume-2026-10-12-cartagena-source-modifier-fix1/author-receipt.json'), ('reader', '01a12f3a-7ca2-7132-b4aa-9c0bce8f8722', '0640651', 'independent-pilot/resume-2026-10-12-cartagena-initial-system-current1/independent-receipt.json')]
records, originals = [], {}
for role, identity, rev, rel in reads:
    path = BASE / rel; raw = path.read_bytes(); assert raw == git(rev, path)
    d = json.loads(raw)
    if role == 'author':
        assert sha(raw) == binding['receiptSha256'] and d['wholeCardAfterCanonicalSha256'] == sha(cj(q))
    else:
        assert d['readerNativeIdentity'] == identity != aid == d['authorNativeIdentity']
        assert d['currentCard'] == q and d['wholeCardCurrentSha256'] == sha(cj(q))
    src = d['sourceOriginal']; capture = ROOT / src.get('ownedCapturePath', src['capturePath'])
    original = capture.read_bytes(); assert original == git(rev, capture) == git('HEAD', capture)
    assert sha(original) == src['rawSHA256'] and len(original) == src['byteLength']
    assert subprocess.check_output(['git', '-C', str(ROOT), 'hash-object', str(capture)], text=True).strip() == src['gitBlob']
    assert src['actualFullCaptureURL'].startswith('https://') and src['originalType']
    text = json.loads(original)['results'][0]['justification_en']
    literals = {'prompt-key': {'prompt': q['prompt'], 'answers': [a['text'] for a in q['answers']], 'correctIndex': q['correctIndex'], 'key': q['answers'][q['correctIndex']]['text']}, 'explanation': q['explanation'], **{f'answer{i}-note': a['note'] for i, a in enumerate(q['answers'])}}
    assert {f['field'] for f in d['fields']} == literals.keys()
    for f in d['fields']:
        lit = literals[f['field']]
        assert f['currentLiteral'] == lit and f['currentLiteralSha256'] == sha(cj(lit))
        if role == 'author':
            assert f['nativeLiteralSha256'] == sha(cj(lit)) and f['manualAnalysis']
        else:
            native = cj(lit) if f['field'] == 'prompt-key' else lit.encode()
            assert f['readerNativeLiteralSha256'] == sha(native) and f['individualManualAnalysis']
        for proof in f['sourceProofs']:
            quote = proof['exactQuote']; offset = proof['characterOffset']
            assert text[offset:offset + proof['characterLength']] == quote
            assert sha(quote.encode()) == proof.get('quoteSha256', proof.get('exactQuoteSHA256'))
            assert text[proof['contextStart']:proof['contextEnd']] == proof['context']
        records.append({'questionId':q['id'], 'field':f['field'], 'actualRole':role, 'actualIdentity':identity, 'receipt':str(path.relative_to(ROOT)), 'receiptCommit':rev, 'receiptSha256':sha(raw), 'nativeField':f, 'sourceOriginal':src})
    originals[str(capture.relative_to(ROOT))] = src
result = {'purpose':'Native recipes/literals/committed original bytes and quote locations only. No generated quality grade.', 'cards':1, 'roleFields':12, 'currentCardSha256':sha(cj(q)), 'records':records, 'originals':originals, 'errors':0}
(OUT / 'cartagena-current1-pair-bindings.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print({'cards':1, 'roleFields':12, 'originals':len(originals), 'errors':0, 'cardSha256':sha(cj(q))})
