"""Current native and source preservation only; no quality grades generated."""
import hashlib
import json
import subprocess
from pathlib import Path
ROOT = Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle')
BASE = ROOT / 'docs/content-audits/question-quality-wave-6'
OUT = BASE / 'coordinator-continuation-01a12f20'
def sha(b): return hashlib.sha256(b).hexdigest()
def cj(v, sort=False): return json.dumps(v, ensure_ascii=False, sort_keys=sort, separators=(',', ':')).encode()
def git(rev, p): return subprocess.check_output(['git', '-C', str(ROOT), 'show', rev + ':' + str(p.relative_to(ROOT))])
ar = BASE / 'middle-ages/resume-2026-10-12-current15-repair/turn1-first5-author-receipt.json'
rr = BASE / 'independent-pilot/resume-2026-10-12-middle-current15-pilot5/current3-0be3147/reader-receipt.json'
rawa, rawr = git('0be3147', ar), git('b04eef6', rr)
a, rd = json.loads(rawa), json.loads(rawr)
assert a['authorIdentity']['nativeThreadId'] == rd['authorIdentity']['nativeThreadId'] == '01a12f31-8ab0-7182-b063-0654e1f3e895'
assert rd['readerIdentity']['nativeThreadId'] == '01a12f3d-8ec1-78b3-b153-5f2a62967421' != rd['authorIdentity']['nativeThreadId']
qs = {q['id']:q for q in json.loads((ROOT / 'src/content/topics/middle-ages.json').read_text())['questions']}
originals = {s['sourceRef']:s for s in a['sourceOriginals']}
ids = ['middle-ages-homage', 'middle-ages-melee', 'middle-ages-chivalry']
records, paths = [], set()
for qid in ids:
    q = qs[qid]; ac = next(c for c in a['cards'] if c['id'] == qid); rc = next(c for c in rd['cards'] if c['id'] == qid)
    assert ac['currentCard'] == q
    assert ac['cardSHA256'] == rc['currentCardNativeSHA256'] == sha(cj(q))
    assert rc['currentCardSortedRegistrySHA256'] == sha(cj(q, True))
    lits = {'prompt-key':{'prompt':q['prompt'],'answers':q['answers'],'correctIndex':q['correctIndex'],'key':q['answers'][q['correctIndex']]['text']},'explanation':q['explanation'], **{f'note{i}':{'answer':x['text'],'note':x['note']} for i,x in enumerate(q['answers'])}}
    for role, c, receipt, raw, rev in [('author',ac,ar,rawa,'0be3147'),('reader',rc,rr,rawr,'b04eef6')]:
        assert len(c['fields']) == 6
        for f in c['fields']:
            name = f['field']; assert f['currentLiteral'] == lits[name]
            assert f['literalSHA256' if role == 'author' else 'nativeLiteralSHA256'] == sha(cj(lits[name]))
            if role == 'author': assert f['sourceReason'] and f['editorialReason']
            else: assert f['sourceVerdict'] == f['editorialVerdict'] == f['verdict'] == 'PASS'
            for p in f['rawProofs' if role == 'author' else 'actualProofs']:
                path = p['sourceRef' if role == 'author' else 'rawPath']; capture = ROOT / path
                src = originals[path] if role == 'author' else p
                captured = capture.read_bytes(); assert captured == git(rev, capture) == git('HEAD', capture)
                assert sha(captured) == src['rawSHA256']
                assert subprocess.check_output(['git','-C',str(ROOT),'hash-object',str(capture)],text=True).strip() == src['gitBlob']
                assert sha(p['quote' if role == 'author' else 'exactQuote'].encode()) == p['quoteSHA256']
                assert p['locator']; paths.add(path)
            records.append({'questionId':qid,'cardCanonicalSortedSha256':sha(cj(q,True)),'actualRole':role,'actualIdentity':a['authorIdentity'] if role=='author' else rd['readerIdentity'],'receipt':str(receipt.relative_to(ROOT)),'receiptCommit':rev,'receiptSha256':sha(raw),'field':name,'nativeRecipe':'compact insertionJSON ensurefalse; notes{answer,note}; strings JSON-encoded','nativeField':f})
result = {'purpose':'Current native/card/field and raw frozenGit/SHA/blob/quote preservation only; no automated quality decision','cards':3,'roleFields':36,'originals':sorted(paths),'authorProvenanceIndex':a['sourceOriginals'],'records':records,'errors':0}
(OUT / 'middle-pilot3-current-pair-bindings.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print({'cards':3,'roleFields':36,'originals':len(paths),'errors':0})
