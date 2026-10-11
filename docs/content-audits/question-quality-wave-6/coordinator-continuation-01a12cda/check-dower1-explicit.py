"""Exact frozen single-card receipts; literal/source bindings only, no editorial grading."""
import json,hashlib,subprocess
from pathlib import Path
b=Path('docs/content-audits/question-quality-wave-6');qid='middle-ages-dower';q=next(c for c in json.loads(Path('src/content/topics/middle-ages.json').read_text())['questions'] if c['id']==qid)
def sha(x):return hashlib.sha256(x).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def git(rev,p):return subprocess.check_output(['git','show',rev+':'+str(p)])
readings=[('author','01a12ca5-97a5-7860-9e4a-789a3f6bdcab','2dbcf0f','middle-ages/resume-2026-10-12-rework28/author-dower-repair2-receipt.json'),('independent','01a12ced-520a-78e3-a277-0bc5a9443656','7637b76','independent-pilot/resume-2026-10-12-dower-repair2-current/reader-receipt.json')];records=[];originals={}
for role,identity,rev,rel in readings:
 p=b/rel;raw=git(rev,p);d=json.loads(raw);assert d['questionId']==qid and d['verdict']=='PASS' and d['agentIdentity']==identity;assert d['cardCanonicalSha256']==sha(canon(q));fields={f['field']:f for f in d['fields']};lits={'prompt-key':[q['prompt'],q['correctIndex'],q['answers'][q['correctIndex']]['text']],**{f'note{i}':a['note'] for i,a in enumerate(q['answers'])},'explanation':q['explanation']};assert set(lits)==set(fields)
 for key,lit in lits.items():
  f=fields[key];assert f['verdict']=='PASS' and f['substantiveRead'];assert f['claimAnalysis'] if role=='author' else f['manualIndividualAnalysis'];assert f['literalSha256']==sha(lit.encode() if isinstance(lit,str) else canon(lit));assert f['proofs'];proofs=list(f['proofs']);supplement=[]
  if role=='author' and key in ['prompt-key','explanation']:
   # Explicit support for the Douaire clause from the SAME frozen author's current
   # six-field reading: note0 already quotes the definition supporting this clause.
   supplement=fields['note0']['proofs'];proofs+=supplement
  for proof in proofs:
   assert proof['sourceClass'] and proof['locator'] and proof['captureFormat'] and proof['url'].startswith('https://');capture=Path(proof['rawCapture']);capture=capture if str(capture).startswith('docs/') else p.parent/capture;expected=proof['rawCaptureSha256'];assert sha(capture.read_bytes())==expected and sha(git('HEAD',capture))==expected;passage=proof['passage'] if role=='author' else proof['quotedPassage'];phash=proof['passageSha256'] if role=='author' else proof['quotedPassageSha256'];assert sha(passage.encode())==phash;originals[str(capture)]=expected
  records.append({'questionId':qid,'cardCanonicalSha256':sha(canon(q)),'field':key,'literalSha256':f['literalSha256'],'role':role,'actualNativeIdentity':identity,'receipt':str(p),'receiptCommit':rev,'receiptSha256':sha(raw),'nativeProofs':f['proofs'],'sharedSameReceiptSourceSupport':supplement,'sharedSourceSupportMeaning':'Exact current author note0 definition supports the repeated Douaire clause in prompt/explanation; no new reading/verdict claimed, original receipt untouched.' if supplement else None})
report={'method':'Named Dower1 whole6 source/editorial coordinator PASS. Single-card root schema and independent manualIndividualAnalysis/quotedPassage preserved. Shared same-author current note0 source support declared separately for prompt/explanation; no normalized original or invented read.','cards':1,'roleFields':len(records),'records':records,'originals':originals,'errors':0};(b/'coordinator-continuation-01a12cda/dower1-current-bindings.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print({'cards':1,'roleFields':len(records),'originals':len(originals),'errors':0})
