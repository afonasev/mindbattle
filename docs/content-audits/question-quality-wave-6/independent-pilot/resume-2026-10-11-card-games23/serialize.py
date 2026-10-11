"""Serialize explicit independent decisions; never infers PASS from a match."""
import copy,hashlib,json,os,sys
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parents[4]
A=ROOT/'docs/content-audits/question-quality-wave-6/card-games/resume-2026-10-11-remaining23'
identity='01a12b6a-9843-75e0-bbdb-efba3c97e0bc'
assert os.environ['CODEX_THREAD_ID']==identity
extras=json.loads((B/'supplemental-proofs.json').read_text())
r=json.loads((A/'author23.json').read_text());dec=json.loads((B/'decisions.json').read_text());cards=[]
for a in r['cards']:
 if a['questionId'] not in dec:continue
 d=dec[a['questionId']];assert len(d['fields'])==6
 row={'questionId':a['questionId'],'cardCanonicalSha256':a['cardCanonicalSha256'],'verdict':d['verdict'],'editorialAnalysis':d['editorial'],'fields':[]}
 byname={f['field']:f for f in a['fields']}
 for name,(verdict,analysis) in zip(['prompt-key','note0','note1','note2','note3','explanation'],d['fields']):
  f=byname[name];proofs=copy.deepcopy(f['proofs'])
  for p in proofs:
   p['rawCapture']=os.path.relpath((A/p['rawCapture']).resolve(),B)
   p.update(role='independent',agentIdentity=identity,authorIdentity=r['agentIdentity'],independentRead='Original raw context actually read; inherited capture metadata is transport provenance, not inherited author verdict.')
  for extra in extras.get(a['questionId']+':'+name,[]):
   extra=copy.deepcopy(extra);extra.update(role='independent',agentIdentity=identity,authorIdentity=r['agentIdentity'],currentCardSha256=a['cardCanonicalSha256'],fieldLiteralSha256=f['literalSha256']);proofs.append(extra)
  row['fields'].append({'field':name,'literalSha256':f['literalSha256'],'verdict':verdict,'substantiveRead':True,'claimAnalysis':analysis,'proofs':proofs})
 cards.append(row)
out={'role':'independent','agentIdentity':identity,'authorIdentity':r['agentIdentity'],'authorFreezeCommit':'ab97f85','date':'2026-10-11','sourcePolicy':'Shared immutable original captures reused by hash after actual independent reading. Full extracted originals accepted only in declared proof-format mode. No author verdict is inherited.','cards':cards}
(B/sys.argv[1]).write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print('serialized explicit decisions',len(cards))
