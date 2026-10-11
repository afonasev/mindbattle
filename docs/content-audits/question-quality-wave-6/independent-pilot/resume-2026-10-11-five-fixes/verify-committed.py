"""Verify independent receipt against working bytes AND preserved Git blobs."""
import hashlib,json,subprocess
from collections import Counter
from pathlib import Path
HERE=Path(__file__).resolve().parent
REPO=next(p for p in HERE.parents if (p/'src/content/topics').is_dir())
def git(*args): return subprocess.check_output(['git',*args],cwd=REPO)
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
r=json.loads((HERE/'independent-receipt.json').read_text()); errors=[]; sources=[]; seen=set(); cards=[];topics=[]
head=git('rev-parse','HEAD').decode().strip()
for c in r['cards']:
 for f in c['fields']:
  for p in f['proofs']:
   path=(HERE/p['rawCapture']).resolve();rel=str(path.relative_to(REPO))
   if rel in seen:continue
   seen.add(rel);working=path.read_bytes();blob=git('show',head+':'+rel)
   row=dict(path=rel,bytes=len(working),workingByteSha256=sha(working),gitBlobSha256=sha(blob),gitBlobOid=git('rev-parse',head+':'+rel).decode().strip(),receiptSha256=p['rawCaptureSha256'])
   row['allIdentical']=row['workingByteSha256']==row['gitBlobSha256']==row['receiptSha256']
   if not row['allIdentical']:errors.append('Source mismatch: '+rel)
   sources.append(row)
for topic in ['middle-ages','geology-earth']:
 rel=f'src/content/topics/{topic}.json';working=(REPO/rel).read_bytes();blob=git('show',head+':'+rel);baseline=git('show','c1ded1d:'+rel)
 qs=json.loads(working)['questions'];old=json.loads(baseline)['questions']
 counts=Counter(q['difficulty'] for q in qs);positions={d:[sum(q['difficulty']==d and q['correctIndex']==i for q in qs) for i in range(4)] for d in counts}
 row=dict(topic=topic,currentEqualsBaseline=working==baseline,currentEqualsGitBlob=working==blob,workingByteSha256=sha(working),gitBlobSha256=sha(blob),sameIdOrder=[q['id'] for q in qs]==[q['id'] for q in old],sameDifficultyAndIndex=[(q['difficulty'],q['correctIndex']) for q in qs]==[(q['difficulty'],q['correctIndex']) for q in old],counts=dict(counts),positions=positions)
 if not all(row[k] for k in ['currentEqualsBaseline','currentEqualsGitBlob','sameIdOrder','sameDifficultyAndIndex']):errors.append('Topic preservation mismatch: '+topic)
 if counts != Counter(easy=40,medium=40,hard=20) or any(positions[d]!=([5]*4 if d=='hard' else [10]*4) for d in positions):errors.append('Quota mismatch: '+topic)
 topics.append(row)
 for q in qs:
  receipt=next((c for c in r['cards'] if c['questionId']==q['id']),None)
  if receipt:
   actual=sha(canon(q));valid=actual==receipt['cardCanonicalSha256'];cards.append(dict(questionId=q['id'],cardCanonicalSha256=actual,receiptMatches=valid))
   if not valid:errors.append('Card mismatch: '+q['id'])
result=dict(role='independent',agentIdentity=r['agentIdentity'],verifiedCommit=head,branch=git('branch','--show-current').decode().strip(),sources=sources,cards=cards,topics=topics,errors=errors,mechanicallyValid=not errors,newSubstantiveVerdictsCreated=0,newCertifiedCards=0,cleanup=dict(ownedProcesses='No persistent process launched; curl and Python checks exited.',temporaryFiles='None outside the owned directory; failed SSL capture retained as provenance, not a successful source.',retained='Independent receipts, explicit decision serializer, source bytes/headers, mismatch history and verification reports retained for coordinator.',foreignWork='Other topic/author changes observed in shared worktree and left untouched; no clean/reset/revert/removal.'))
(HERE/'committed-preservation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(commit=head,sources=len(sources),cards=len(cards),errors=errors,newCertifiedCards=0)))
raise SystemExit(bool(errors))
