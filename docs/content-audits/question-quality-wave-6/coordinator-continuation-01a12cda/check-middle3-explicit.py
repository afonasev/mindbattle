"""Mechanical proof binding of exactly three manually adjudicated cards. No grading."""
import json,hashlib,subprocess
from pathlib import Path
base=Path('docs/content-audits/question-quality-wave-6')
ids=['middle-ages-precaria','middle-ages-dowry','middle-ages-serf']
readings=[('author','01a12ca5-97a5-7860-9e4a-789a3f6bdcab','7ec5109','middle-ages/resume-2026-10-12-rework28/author-pilot4-repair-receipt.json','agentIdentity','claimAnalysis'),('independent','01a12cdb-bf10-7ab2-a2fa-d7b3926e06b6','d13ff9f','independent-pilot/resume-2026-10-12-middle4-current/reader-receipt.json','readerIdentity','individualReaderAnalysis')]
def digest(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def git(rev,path):return subprocess.check_output(['git','show',rev+':'+str(path)])
cards={q['id']:q for q in json.loads(Path('src/content/topics/middle-ages.json').read_text())['questions']}
records=[];originals={}
for role,identity,commit,relative,idkey,analysiskey in readings:
 path=base/relative;raw=git(commit,path);receipt=json.loads(raw);assert receipt[idkey]==identity
 byid={c['questionId']:c for c in receipt['cards']}
 for qid in ids:
  q=cards[qid];c=byid[qid];assert c['verdict']=='PASS';assert c['cardCanonicalSha256']==digest(canon(q)),qid
  fields={f['field']:f for f in c['fields']};literals={'prompt-key':[q['prompt'],q['correctIndex'],q['answers'][q['correctIndex']]['text']],**{f'note{i}':a['note'] for i,a in enumerate(q['answers'])},'explanation':q['explanation']};assert set(fields)==set(literals)
  for key,lit in literals.items():
   f=fields[key];assert f['verdict']=='PASS' and f['substantiveRead'];assert f[analysiskey] and f['proofs'];assert f['literalSha256']==digest(lit.encode() if isinstance(lit,str) else canon(lit)),(qid,key)
   if 'literalText' in f:assert f['literalText']==lit
   for proof in f['proofs']:
    assert proof['sourceClass'] and proof['url'].startswith('https://') and proof['locator'];capture=Path(proof['rawCapture']);capture=capture if str(capture).startswith('docs/') else path.parent/capture;expected=proof['rawCaptureSha256'];assert digest(capture.read_bytes())==expected;assert digest(git('HEAD',capture))==expected
    if 'passage' in proof:assert digest(proof['passage'].encode())==proof['passageSha256']
    if 'gitBlob' in proof:assert subprocess.check_output(['git','rev-parse',proof['frozenCommit']+':'+str(capture)],text=True).strip()==proof['gitBlob']
    originals[str(capture)]=expected
   records.append({'questionId':qid,'cardCanonicalSha256':digest(canon(q)),'field':key,'literalSha256':f['literalSha256'],'role':role,'actualNativeIdentity':identity,'receipt':str(path),'receiptCommit':commit,'receiptSha256':digest(raw),'sourcePointers':f['proofs']})
report={'method':'Explicit coordinator decisions precaria/dowry/serf only; format adapter preserves immutable original receipts. Reader uses native readerIdentity, individualReaderAnalysis and locator objects. No verdict inferred.','records':records,'originals':originals,'cards':len(ids),'roleFields':len(records),'errors':0}
(base/'coordinator-continuation-01a12cda/middle3-current-bindings.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print({'cards':len(ids),'roleFields':len(records),'originals':len(originals),'errors':0})
