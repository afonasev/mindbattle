"""Preservation and native schema checks only; this script never assigns grades."""
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle')
BASE = ROOT / 'docs/content-audits/question-quality-wave-6'
OUT = BASE / 'coordinator-continuation-01a12f20'
assert subprocess.check_output(['git', '-C', str(ROOT), 'rev-parse', '--show-toplevel'], text=True).strip() == str(ROOT)
def sha(b): return hashlib.sha256(b).hexdigest()
def cj(v, sort=False): return json.dumps(v, ensure_ascii=False, separators=(',', ':'), sort_keys=sort).encode()
def read(p): return json.loads(p.read_text())
def git(rev, p): return subprocess.check_output(['git', '-C', str(ROOT), 'show', rev + ':' + str(p.relative_to(ROOT))])
errors, records, originals = [], [], {}
def check(ok, where):
    if not ok: errors.append(where)
def receipt(rel, rev):
    p = BASE / rel
    check(p.read_bytes() == git(rev, p), 'receipt bytes ' + rel)
    return read(p), p
def original(p, expected, blob, rev, label):
    raw = p.read_bytes()
    check(sha(raw) == expected, label + ' raw SHA')
    check(raw == git(rev, p) == git('HEAD', p), label + ' committed raw bytes')
    check(subprocess.check_output(['git', '-C', str(ROOT), 'hash-object', str(p)], text=True).strip() == blob, label + ' Git blob')
    originals[str(p.relative_to(ROOT))] = {'sha256': sha(raw), 'bytes': len(raw), 'gitBlob': blob}

configs = [
    ('middle-ages', 'independent-pilot/resume-2026-10-12-middle19-current/reader-receipt.json', '9885636'),
    ('winter-sports', 'independent-pilot/resume-2026-10-12-winter30-current/independent-receipt.json', '54a4900'),
    ('architecture', 'independent-pilot/resume-2026-10-12-architecture5-repaired-current/independent-receipt.json', 'a73fa2b'),
]
mi = read(BASE / 'independent-pilot/resume-2026-10-12-middle19-current/source-index.json')
mi = {x['path']: x for x in mi['originals']}
for topic, reader_rel, reader_rev in configs:
    qs = {q['id']: q for q in read(ROOT / ('src/content/topics/' + topic + '.json'))['questions']}
    rd, rp = receipt(reader_rel, reader_rev)
    for rc in rd['cards']:
        if rc.get('verdict', rc.get('independentVerdict', rc.get('wholeCardVerdict'))) != 'PASS': continue
        qid = rc.get('questionId', rc.get('id')); q = qs[qid]
        if topic == 'middle-ages':
            ar = ROOT / rc['authorRecordPath']; av = '08e4ee3' if 'fresh-unreviewed10' in str(ar) else '0d6f492'
            ad, ap = receipt(str(ar.relative_to(BASE)), av)
            ac = next(x for x in ad['cards'] if x['questionId'] == qid)
            aid = rc['authorThreadId']; rid = rd['readerThreadId']; sort = av == '0d6f492'
            check(ac['cardCanonicalSha256'] == sha(cj(q, sort)), qid + ' author card hash')
            check(rc['currentCard'] == q and rc['currentCanonicalSha256'] == sha(cj(q)), qid + ' reader card hash')
        elif topic == 'winter-sports':
            av = 'b31dc20'; ad, ap = receipt('winter-sports/resume-2026-10-12-fresh-author30/final-current-author-receipt.json', av)
            ac = next(x for x in ad['cards'] if x['questionId'] == qid)
            aid = ad['authorThreadId']; rid = rd['readerThreadId']
            check(ac['cardCanonicalSha256'] == sha(cj(q, True)), qid + ' author sorted card hash')
            check(rc['wholeCardSha256'] == sha(cj(q)), qid + ' reader insertion-order card hash')
        else:
            av = '26ac144'; ad, ap = receipt('architecture/resume-2026-10-12-current-fix5/author-receipt.json', av)
            ac = next(x for x in ad['cards'] if x['questionId'] == qid)
            md, mp = receipt('architecture/resume-2026-10-12-current-fix5/manual-analysis.json', av)
            mc = next(x for x in md['cards'] if x['questionId'] == qid)
            aid = ad['agentIdentity']; rid = rd['readerNativeIdentity']
            check(ac['currentCard'] == mc['currentCard'] == rc['currentCard'] == q, qid + ' three current literals')
            check(ac['cardCanonicalSha256'] == rc['wholeCardCurrentSha256'] == sha(cj(q, True)), qid + ' paired card hash')
        check(aid != rid, qid + ' distinct roles')
        check(len(ac['fields']) == len(rc['fields']) == 6, qid + ' whole6')
        for role, c, p, rev in [('author', ac, ap, av), ('reader', rc, rp, reader_rev)]:
            for f in c['fields']:
                name = f['field']; note = q['answers'][int(name[-1])]['note'] if name.startswith('note') else None
                key = q['answers'][q['correctIndex']]['text']
                if topic == 'middle-ages':
                    lit = ({'prompt': q['prompt'], **({'answers': q['answers']} if role == 'reader' else {}), 'correctIndex': q['correctIndex'], 'key': key} if name == 'prompt-key' else ({'answer': q['answers'][int(name[-1])]['text'], 'note': note} if name.startswith('note') else q['explanation']))
                    check(f['currentLiteral'] == lit, qid + role + name + ' literal')
                    check(f.get('currentLiteralSha256', f.get('literalSha256')) == sha(cj(lit, role == 'author' and av == '0d6f492')), qid + role + name + ' native literal hash')
                    proofs = f['proofs']
                elif topic == 'winter-sports':
                    lit = ([q['prompt'], q['correctIndex'], key] if role == 'author' else {'prompt': q['prompt'], 'options': [a['text'] for a in q['answers']], 'correctIndex': q['correctIndex'], 'key': key}) if name == 'prompt-key' else (note if name.startswith('note') else q['explanation'])
                    check(f['literal'] == lit, qid + role + name + ' literal')
                    check(f['literalSha256'] == sha(cj(lit) if name == 'prompt-key' else lit.encode()), qid + role + name + ' native literal hash')
                    proofs = f['proofBindings']
                else:
                    lit = {'prompt': q['prompt'], 'answers': [a['text'] for a in q['answers']], 'correctIndex': q['correctIndex'], 'key': key} if name == 'prompt-key' else (note if name.startswith('note') else q['explanation'])
                    if role == 'author':
                        mf = next(x for x in mc['fields'] if x['field'] == name)
                        check(mf['currentLiteral'] == lit and mf['literalSha256'] == f['literalSha256'], qid + name + ' author manual literal')
                        native = cj([q['prompt'], q['correctIndex'], key]) if name == 'prompt-key' else lit.encode()
                        check(f['literalSha256'] == sha(native), qid + name + ' author native list/raw recipe')
                    else:
                        check(f['currentLiteral'] == lit and f['currentLiteralSha256'] == sha(cj(lit, True)), qid + name + ' reader canonical literal')
                    proofs = f['sourceProofs']
                check(bool(proofs), qid + role + name + ' proofs')
                for z in proofs:
                    if topic == 'middle-ages':
                        if role == 'author':
                            path = ROOT / z['fullCapturePath']; expected=z['nativeSha256']; blob=z['gitBlob']; url=z['captureUrl']; fmt=z['captureFormat']
                        else:
                            m=mi[z['sourceRef']];path=ROOT/z['sourceRef'];expected=m['sha256'];blob=m['gitBlob'];url=m['captureUrl'];fmt=m['format']
                        quote=z['quote']; qsha=z['quoteSha256']
                    elif topic == 'winter-sports':
                        path=ROOT/z['rawCapture' if role=='author' else 'path'];expected=z['rawSha256' if role=='author' else 'sha256'];blob=z['gitBlobCandidate' if role=='author' else 'gitBlob'];url=z['url' if role=='author' else 'captureUrl'];fmt=z['rawFormat'];quote=z['exactQuote'];qsha=z['exactQuoteSha256']
                    else:
                        path=ROOT/z['rawCaptureRepoPath'];expected=z['rawCaptureSha256'];blob=z['frozenGitBlob'];url=z['actualCaptureUrl'];fmt=z['rawFormat'];quote=z['quotedPassage'];qsha=z['quotedPassageSha256']
                    original(path, expected, blob, rev, qid+role+name)
                    check(sha(quote.encode()) == qsha, qid+role+name+' quote hash')
                    check(url.startswith('https://') and fmt and z['locator'], qid+role+name+' provenance')
                records.append({'questionId':qid,'role':role,'identity':aid if role=='author' else rid,'receipt':str(p.relative_to(ROOT)),'receiptCommit':rev,'receiptSha256':sha(p.read_bytes()),'field':name,'proofs':proofs})
result={'purpose':'Native serialization and committed byte preservation only; NO factual/editorial grading or certification. Manual findings in candidate14-adjudication.json remain authoritative.','candidateCards':len(records)//12,'roleFields':len(records),'records':records,'originals':originals,'errors':errors}
(OUT/'candidate14-preservation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print({'candidateCards':result['candidateCards'],'roleFields':len(records),'originals':len(originals),'errors':errors})
