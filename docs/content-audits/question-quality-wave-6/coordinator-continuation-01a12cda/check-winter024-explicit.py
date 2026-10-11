"""Bind explicitly adjudicated Winter024, retaining both original hash recipes/schema."""
import json,hashlib,subprocess
from pathlib import Path
root=Path.cwd();base=Path('docs/content-audits/question-quality-wave-6');qid='winter-sports-024';q=next(x for x in json.loads(Path('src/content/topics/winter-sports.json').read_text())['questions'] if x['id']==qid)
def sha(x):return hashlib.sha256(x).hexdigest()
def compact(x,sort=False):return json.dumps(x,ensure_ascii=False,sort_keys=sort,separators=(',',':')).encode()
def git(rev,p):return subprocess.check_output(['git','show',rev+':'+str(p)])
readings=[('author','01a12cc1-9d5d-74a1-99ba-6377bdfaed21','54fbf71','winter-sports/resume-2026-10-12-rework33/followup2/author-current024-receipt.json'),('independent','01a12ce3-9a06-7a40-970a-0b9c72b3f5db','8442e92','independent-pilot/resume-2026-10-12-winter5-repair-current/reader-receipt.json')]
records=[];originals={}
for role,identity,rev,rel in readings:
 p=base/rel;raw=git(rev,p);d=json.loads(raw);assert d['agentIdentity']==identity;c=next(x for x in d['cards'] if x['questionId']==qid);assert c['verdict']=='PASS';assert c['cardCanonicalSha256']==sha(compact(q));assert c['sortedCardSha256']==sha(compact(q,True));fields={f['field']:f for f in c['fields']};lits={'prompt-key':compact([q['prompt'],q['correctIndex'],q['answers'][q['correctIndex']]['text']]).decode(),**{f'note{i}':a['note'] for i,a in enumerate(q['answers'])},'explanation':q['explanation']};assert set(fields)==set(lits)
 for key,lit in lits.items():
  f=fields[key];assert f['verdict']=='PASS' and f['substantiveRead'] and f['claimAnalysis'];assert f['literal']==lit and f['literalSha256']==sha(lit.encode());assert f['proofs']
  for proof in f['proofs']:
   # Explicit native reader aliases, not rewriting the frozen receipt.
   sourceclass=proof['sourceClass'] if role=='author' else proof['sourceType'];expected=proof['rawCaptureSha256'] if role=='author' else proof['rawSha256'];passage=proof['passage'] if role=='author' else proof['quotedPassage'];phash=proof['passageSha256'] if role=='author' else proof['quotedPassageSha256'];capture=Path(proof['rawCapture']);capture=capture.relative_to(root) if capture.is_absolute() else capture
   assert sourceclass and proof['url'].startswith('https://') and proof['locator'] and proof['captureFormat'];assert sha(passage.encode())==phash;assert sha(capture.read_bytes())==expected;assert sha(git('HEAD',capture))==expected
   if role=='independent':assert subprocess.check_output(['git','rev-parse','HEAD:'+str(capture)],text=True).strip()==proof['originalGitBlob'];assert proof['supportsCurrentClaim']
   originals[str(capture)]=expected
  records.append({'questionId':qid,'sortedCardSha256':sha(compact(q,True)),'insertionOrderCardSha256':sha(compact(q)),'field':key,'fieldLiteralSha256':f['literalSha256'],'actualRole':role,'actualNativeIdentity':identity,'receiptPath':str(p),'receiptCommit':rev,'receiptSha256':sha(raw),'proofs':f['proofs']})
report={'method':'Explicit current Winter024 coordinator decision; original unsorted/sorted recipes retained, reader sourceType/rawSha256/quotedPassage aliases declared; no grading or regenerated author read.','cards':1,'roleFields':len(records),'records':records,'originals':originals,'errors':0}
(base/'coordinator-continuation-01a12cda/winter024-current-bindings.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print({'cards':1,'roleFields':len(records),'originals':len(originals),'errors':0})
