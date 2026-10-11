"""Serialize explicit reader decisions and rebind existing proofs; no implicit PASS."""
import json,hashlib,os,copy,sys
from pathlib import Path
P=Path(__file__).resolve().parent; ROOT=P.parents[4]
A=ROOT/'docs/content-audits/question-quality-wave-6/architecture/resume-2026-10-11-author100'
canon=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
hash=lambda x:hashlib.sha256(x).hexdigest()
C={c['id']:c for c in json.loads((ROOT/'src/content/topics/architecture.json').read_text())['questions']}
R={c['questionId']:c for n in ('batch02-receipt.json','pilot-arch-fix1-receipt.json') for c in json.loads((A/n).read_text())['cards']}
D=json.loads((P/'decisions.json').read_text()); out=[]
for qid,d in D.items():
 c=C[qid]; assert hash(canon(c))==R[qid]['cardCanonicalSha256']
 row={'questionId':qid,'cardCanonicalSha256':hash(canon(c)),'verdict':d['verdict'],'editorialAnalysis':d['editorialAnalysis'],'fields':[]}
 literals={'prompt-key':canon([c['prompt'],c['correctIndex'],c['answers'][c['correctIndex']]['text']]),**{f'note{i}':a['note'].encode() for i,a in enumerate(c['answers'])},'explanation':c['explanation'].encode()}
 assert set(d['fields'])==set(literals)
 for name,fd in d['fields'].items():
  proofs=copy.deepcopy(next(f['proofs'] for f in R[qid]['fields'] if f['field']==name))
  extra={
   ('architecture-prambanan','prompt-key'):('642','justification_en','These compounds are located on the border between the two provinces of Yogyakarta and Central Java on Java Island.'),
   ('architecture-lalibela','prompt-key'):('18','description_en',"The 11 medieval monolithic cave churches of this 13th-century 'New Jerusalem' are situated in a mountainous region in the heart of Ethiopia near a traditional village with circular-shaped dwellings."),
   ('architecture-temple-heaven','prompt-key'):('881','name_en','Temple of Heaven: an Imperial Sacrificial Altar in Beijing')}
  if (qid,name) in extra:
   num,key,decoded=extra[(qid,name)];raw=A/f'sources/unesco-{num}.json';scalar=json.loads(raw.read_text())['results'][0][key];assert decoded in scalar
   p=copy.deepcopy(proofs[0]);p.update(rawCapture=f'sources/unesco-{num}.json',rawCaptureSha256=hash(raw.read_bytes()),locator={'jsonPointer':'/results/0/'+key},passage=decoded,decodedPassage=decoded,passageSha256=hash(decoded.encode()))
   proofs.append(p)
  for proof in proofs:
   raw=A/proof['rawCapture']
   if proof['rawCapture']=='sources/pitt-apse.htm': raw=P/'originals/pitt-apse.htm'
   assert hash(raw.read_bytes())==proof['rawCaptureSha256'];proof['rawCapture']=os.path.relpath(raw,P)
   proof['independentRead']='Original file opened in this native reader session; JSON scalar decoded at pointer / HTML parsed from original bytes; source context read with literal. Proof metadata reused, author verdict not reused.'
  row['fields'].append({'field':name,'literalSha256':hash(literals[name]),'verdict':fd['verdict'],'substantiveRead':True,'claimAnalysis':fd['claimAnalysis'],'proofs':proofs})
 out.append(row)
result={'role':'independent','agentIdentity':os.environ['CODEX_THREAD_ID'],'authorIdentity':'01a12b8c-3c77-72a2-92f1-6717fad11b74','cards':out,'limits':['Explicit manually written decisions; adapter only binds already read originals and current hashes.','Not root certification or wave completion.']}
assert result['agentIdentity']!=result['authorIdentity']
(P/(sys.argv[1] if len(sys.argv)>1 else 'receipt.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
(P/'current-reviewed-cards.json').write_text(json.dumps([C[qid] for qid in D],ensure_ascii=False,indent=2)+'\n')
