"""Bind the two named whole-card PASS decisions using unchanged native recipes."""
import json,hashlib,subprocess
from pathlib import Path
base=Path('docs/content-audits/question-quality-wave-6');ids=['winter-sports-007','winter-sports-008'];q={c['id']:c for c in json.loads(Path('src/content/topics/winter-sports.json').read_text())['questions']}
def sha(x):return hashlib.sha256(x).hexdigest()
def cj(x,sort=False):return json.dumps(x,ensure_ascii=False,sort_keys=sort,separators=(',',':')).encode()
def git(rev,p):return subprocess.check_output(['git','show',rev+':'+str(p)])
reads=[('author','01a12d03-dca8-7300-bb0f-e5feaef03cc0','d898e6c','winter-sports/resume-2026-10-12-safe-author4/author-current-repair-receipt.json'),('independent','01a12d0a-bc1d-7630-8097-fb6ea932a4dd','9ba64c2','independent-pilot/resume-2026-10-12-winter4-safe-current/reader-receipt.json')];records=[];originals={}
for role,identity,rev,rel in reads:
 p=base/rel;raw=git(rev,p);d=json.loads(raw);assert d['agentIdentity']==identity;cards={c['questionId']:c for c in d['cards']}
 for qid in ids:
  c=cards[qid];card=q[qid];assert c['verdict']=='PASS';assert c['cardCanonicalSha256']==sha(cj(card)) and c['sortedCardSha256']==sha(cj(card,True));fields={f['field']:f for f in c['fields']};lits={'prompt-key':cj([card['prompt'],card['correctIndex'],card['answers'][card['correctIndex']]['text']]).decode(),**{f'note{i}':a['note'] for i,a in enumerate(card['answers'])},'explanation':card['explanation']};assert set(lits)==set(fields)
  for key,lit in lits.items():
   f=fields[key];assert f['verdict']=='PASS' and f['substantiveRead'] and f['manualIndividualAnalysis'];assert f['currentLiteral']==lit and f['literalSha256']==sha(lit.encode());assert f['proofs']
   for proof in f['proofs']:
    capture=Path(proof['rawCapture'] if role=='author' else proof['independentRawCapture']);expected=proof['rawSha256'] if role=='author' else proof['independentRawSha256'];url=proof['actualUrl'] if role=='author' else proof['captureUrl'];assert proof['rawType'] and proof['captureFormat'] and url.startswith('https://') and proof['locator'];assert sha(cj(proof['locator'],True))==proof['locatorSha256'];assert sha(proof['quotedPassage'].encode())==proof['quotedPassageSha256'];assert sha(capture.read_bytes())==expected and sha(git('HEAD',capture))==expected;originals[str(capture)]=expected
   records.append({'questionId':qid,'cardCanonicalSha256':sha(cj(card,True)),'nativeInsertionOrderCardSha256':sha(cj(card)),'field':key,'literalSha256':f['literalSha256'],'actualRole':role,'actualNativeIdentity':identity,'receipt':str(p),'receiptCommit':rev,'receiptSha256':sha(raw),'sourcePointers':f['proofs']})
report={'method':'Explicit007/008 whole6 coordinator decisions only. Both native unsorted card and sorted registry recipes retained; source proof schema rawSha256/actualUrl vs independentRawCapture/captureUrl explicitly declared. No grade inferred.','cards':2,'roleFields':len(records),'records':records,'originals':originals,'errors':0};(base/'coordinator-continuation-01a12cda/winter-safe2-current-bindings.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print({'cards':2,'roleFields':len(records),'originals':len(originals),'errors':0})
