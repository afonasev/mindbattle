"""Mechanical preservation/identity only; no substantive decisions are created."""
import collections,hashlib,json,subprocess
from pathlib import Path
B=Path(__file__).resolve().parent;R=B.parents[4]
def canonical(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def sha(x):return hashlib.sha256(x).hexdigest()
def git(*args):return subprocess.check_output(['git',*args],cwd=R).decode().strip()
p='src/content/topics/card-games.json';current=json.loads((R/p).read_text())['questions'];frozen=json.loads(git('show','ab97f85:'+p))['questions'];before=json.loads(git('show','d60ebd4fe38071e92b0ab03b6983b2f8a4a4a296:'+p))['questions'];receipt=json.loads((B/'independent23.json').read_text());author=json.loads((R/'docs/content-audits/question-quality-wave-6/card-games/resume-2026-10-11-remaining23/author23.json').read_text())
byid={c['id']:c for c in current};owned=[x['questionId'] for x in author['cards']];shapes=lambda cs:[(c['id'],c['difficulty'],c['correctIndex']) for c in cs]
assert len(owned)==23 and [c['questionId'] for c in receipt['cards']]==owned
assert receipt['agentIdentity']!=author['agentIdentity']
assert shapes(current)==shapes(before)
assert all(c==byid[c['id']] for c in frozen)
assert all(c==byid[c['id']] for c in before if c['id'] not in owned)
fieldcounts=collections.Counter(f['verdict'] for c in receipt['cards'] for f in c['fields']);cardcounts=collections.Counter(c['verdict'] for c in receipt['cards'])
quotas=dict(collections.Counter(c['difficulty'] for c in current));positions={d:[sum(c['difficulty']==d and c['correctIndex']==i for c in current) for i in range(4)] for d in ['easy','medium','hard']}
assert quotas=={'easy':40,'medium':40,'hard':20};assert positions=={'easy':[10]*4,'medium':[10]*4,'hard':[5]*4}
rows=[];inventory={}
for c in receipt['cards']:
 assert c['cardCanonicalSha256']==sha(canonical(byid[c['questionId']]))
 rows.append({'questionId':c['questionId'],'cardCanonicalSha256':c['cardCanonicalSha256'],'verdict':c['verdict'],'fieldVerdicts':{f['field']:f['verdict'] for f in c['fields']}})
 for f in c['fields']:
  for s in f['proofs']:
   raw=(B/s['rawCapture']).resolve();assert raw.is_file() and sha(raw.read_bytes())==s['rawCaptureSha256']
   assert s['role']=='independent' and s['agentIdentity']==receipt['agentIdentity'] and s['authorIdentity']==author['agentIdentity']
   assert s['currentCardSha256']==c['cardCanonicalSha256'] and s['fieldLiteralSha256']==f['literalSha256']
   k=str(raw.relative_to(R));item=inventory.setdefault(k,{'sha256':s['rawCaptureSha256'],'captureFormat':s['captureFormat'],'sourceUrls':[],'bindings':[]})
   if s['url'] not in item['sourceUrls']:item['sourceUrls'].append(s['url'])
   item['bindings'].append({'questionId':c['questionId'],'currentCardSha256':c['cardCanonicalSha256'],'field':f['field'],'fieldLiteralSha256':f['literalSha256'],'role':'independent','agentIdentity':receipt['agentIdentity']})
report={'scope':'Only exact23 identity, source binding and unchanged catalog preservation','headAtCheck':git('rev-parse','HEAD'),'branch':git('branch','--show-current'),'authorFreezeCommit':git('rev-parse','ab97f85'),'authorIdentity':author['agentIdentity'],'independentIdentity':receipt['agentIdentity'],'cards':rows,'cardVerdicts':dict(cardcounts),'fieldVerdicts':dict(fieldcounts),'fieldCount':sum(fieldcounts.values()),'fullTopicUnchangedFromAuthorFreeze':True,'unowned77UnchangedFromAuthorBaseline':True,'idOrderDifficultyCorrectIndexPreserved':True,'quotas':quotas,'positions':positions,'pilotFileSha256':sha((B/'pilot5-independent.json').read_bytes()),'pilotRoundtripSha256':sha((B/'pilot5-roundtrip.json').read_bytes()),'finalReceiptSha256':sha((B/'independent23.json').read_bytes()),'mechanicallyValid':True,'newCertifiedCards':0,'certificationOwner':'coordinator; independent verdicts alone do not certify'}
(B/'full-binding.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');(B/'source-inventory.json').write_text(json.dumps(inventory,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:report[k] for k in ['cardVerdicts','fieldVerdicts','fieldCount','fullTopicUnchangedFromAuthorFreeze','unowned77UnchangedFromAuthorBaseline','mechanicallyValid','newCertifiedCards']},ensure_ascii=False))
