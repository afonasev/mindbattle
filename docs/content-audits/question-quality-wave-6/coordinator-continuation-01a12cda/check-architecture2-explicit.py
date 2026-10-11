"""Mechanical bindings for explicit current Sydney/Summer decisions; retain receipt schema."""
import hashlib,json,subprocess
from pathlib import Path
base=Path('docs/content-audits/question-quality-wave-6');ids=['architecture-sydney-opera-house-country','architecture-summer-palace'];cards={c['id']:c for c in json.loads(Path('src/content/topics/architecture.json').read_text())['questions']}
def sha(b):return hashlib.sha256(b).hexdigest()
def canonical(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def git(rev,p):return subprocess.check_output(['git','show',rev+':'+str(p)])
readings=[('author','01a12cc1-a1d0-75e1-9145-70e564a68e5b','3cc178a','architecture/resume-2026-10-12-rework21/author-receipt.json'),('independent','01a12ceb-6680-7223-9c45-a486ef64f089','daf2b0a','independent-pilot/resume-2026-10-12-architecture2-repair-current/independent-receipt.json')];records=[];originals={}
for role,identity,revision,rel in readings:
 p=base/rel;raw=git(revision,p);receipt=json.loads(raw);assert receipt['agentIdentity']==identity;byid={c['questionId']:c for c in receipt['cards']}
 for qid in ids:
  q=cards[qid];c=byid[qid];assert c['cardCanonicalSha256']==sha(canonical(q));assert c['currentCard']==q
  if role=='author':assert c['verdict']=='PASS'
  else:assert c['sourceVerdict']==c['editorialVerdict']=='PASS'
  fields={f['field']:f for f in c['fields']};lits={'prompt-key':canonical([q['prompt'],q['correctIndex'],q['answers'][q['correctIndex']]['text']]).decode(),**{f'note{i}':a['note'] for i,a in enumerate(q['answers'])},'explanation':q['explanation']};assert set(fields)==set(lits)
  for key,lit in lits.items():
   f=fields[key];assert f['literal']==lit and f['literalSha256']==sha(lit.encode());assert f['proofs']
   if role=='author':assert f['verdict']=='PASS' and f['substantiveRead'] and f['claimAnalysis']
   else:assert f['sourceVerdict']==f['editorialVerdict']=='PASS' and f['manualIndividualAnalysis'] and f['readerIdentity']==identity
   for proof in f['proofs']:
    assert proof['sourceClass'] and proof['locator'] and proof['captureFormat'];assert (proof['url'] if role=='author' else proof['sourceUrl']).startswith('https://');assert sha(proof['passage'].encode())==proof['passageSha256'];capture=Path(proof['rawCapture']);capture=capture if str(capture).startswith('docs/') else p.parent/capture;capture=capture.resolve().relative_to(Path.cwd());expected=proof['rawCaptureSha256'];assert sha(capture.read_bytes())==expected and sha(git('HEAD',capture))==expected
    if role=='independent':assert proof['manualIndividualRead'] and proof['readerIdentity']==identity;original=Path(proof['originalPath']);assert sha(git(proof['frozenRevision'],original))==expected;assert subprocess.check_output(['git','rev-parse',proof['frozenRevision']+':'+str(original)],text=True).strip()==proof['originalGitBlob']
    originals[str(capture)]=expected
   records.append({'questionId':qid,'cardCanonicalSha256':sha(canonical(q)),'field':key,'literalSha256':f['literalSha256'],'actualRole':role,'actualNativeIdentity':identity,'receipt':str(p),'receiptCommit':revision,'receiptSha256':sha(raw),'proofs':f['proofs']})
report={'method':'Named Sydney/Summer source/editorial PASS coordinator decisions. Independent original schema has separate source/editorial verdict, manualIndividualAnalysis and proof manualIndividualRead/sourceUrl. Metadata retained unchanged; no inferred grade.','cards':2,'roleFields':len(records),'records':records,'originals':originals,'errors':0};(base/'coordinator-continuation-01a12cda/architecture2-current-bindings.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print({'cards':2,'roleFields':len(records),'originals':len(originals),'errors':0})
