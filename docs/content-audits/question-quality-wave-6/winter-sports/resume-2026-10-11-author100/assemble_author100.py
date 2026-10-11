"""Assemble already explicit author decisions by current literal hash. No editorial verdict creation."""
import json,hashlib,subprocess,copy
from pathlib import Path
from collections import Counter
R=Path(__file__).parent;REPO=R.parents[4];TOPIC=REPO/'src/content/topics/winter-sports.json'
def canonical(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def sha(x):return hashlib.sha256(canonical(x)).hexdigest()
def save(name,data):(R/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
t=json.loads(TOPIC.read_text())['questions'];current={c['id']:c for c in t};m={}
order=['pilot6-revised','snow16','sliding3','subset01-author25','hockey9','repairs6','repairs3b','resolved3','subset01-v2-author25','curling9','skate-biathlon8-v2','massstart-v3','alpine12','sport12','general14','technical9','final-refinement5','final-scope2']
for name in order:
 for c in json.loads((R/(name+'-receipt.json')).read_text())['cards']:
  if c['cardCanonicalSha256']==sha(current[c['questionId']]):m[c['questionId']]=(name,c)
assert len(m)==len(t)==100
assert all(c['verdict']=='PASS' and len(c['fields'])==6 and all(f['verdict']=='PASS' and f['substantiveRead'] is True for f in c['fields']) for _,c in m.values())
# Editorial actors are explicit: correcting the source-provider label does not change a claim or verdict.
rows=[];corrections=[]
for q in t:
 c=copy.deepcopy(m[q['id']][1])
 for fld in c['fields']:
  for proof in fld['proofs']:
   if any(host in proof['url'] for host in ['bauer.com','zamboni.com','technoalpin.com']) and proof['sourceClass']!='primary equipment manufacturer':
    corrections.append({'questionId':c['questionId'],'field':fld['field'],'url':proof['url'],'oldLabel':proof['sourceClass'],'newLabel':'primary equipment manufacturer','scope':'Provider classification only; raw bytes, passage and substantive verdict unchanged; old frozen receipt retained as immutable history.'});proof['sourceClass']='primary equipment manufacturer'
 rows.append(c)
save('source-classification-corrections.json',corrections)
save('author100-receipt.json',{'role':'author','agentIdentity':'01a12ba2-6af8-79b3-96c4-14a4e60812b6','decisionSource':'author100-manifest.json mapping; explicit decisions retained in versioned files','providerLabelCorrections':'source-classification-corrections.json','cards':rows})
save('author100-cards.json',t)
base=json.loads(subprocess.check_output(['git','show','98c3a2b8f77315c96fafb3857aa9c9d0f0eb496c:src/content/topics/winter-sports.json'],cwd=REPO))['questions']
assert len(base)==100
for old,new in zip(base,t):
 for k in ['id','difficulty','correctIndex']:assert old[k]==new[k],(new['id'],k)
 for a in new['answers']:assert 0<len(a['note'].split())<=35,(new['id'],'note')
 assert len(new['answers'])==4 and len(set(a['text'] for a in new['answers']))==4
 assert 0<len(new['explanation'].split())<=70
 assert new['source']['url'].startswith('https://') and new['source']['verifiedAt']=='2026-10-11'
quotas={d:dict(Counter(c['correctIndex'] for c in t if c['difficulty']==d)) for d in ['easy','medium','hard']}
assert all(quotas[d]=={0:n,1:n,2:n,3:n} for d,n in [('easy',10),('medium',10),('hard',5)])
prior=[]
for name in ['subset01-v2','subset02']:
 manifest=json.loads((R/(name+'-freeze.json')).read_text())
 for k,v in manifest['cardHashes'].items():assert sha(current[k])==v,(name,k,'frozen changed')
 prior+=manifest['ids']
remaining=[c['id'] for c in t if c['id'] not in prior];assert len(remaining)==50
for name,ids in [('subset03',remaining[:25]),('subset04',remaining[25:])]:
 subsetrows=[next(c for c in rows if c['questionId']==k) for k in ids]
 save(name+'-author25-receipt.json',{'role':'author','agentIdentity':'01a12ba2-6af8-79b3-96c4-14a4e60812b6','decisionSource':name+'-freeze.json sourceReceipts map; no automated substantive decisions','cards':subsetrows})
 save(name+'-cards.json',[current[k] for k in ids])
 save(name+'-freeze.json',{'subset':name,'status':'AUTHOR_PASS_ONLY_FROZEN_FOR_DISTINCT_READER','ids':ids,'cardHashes':{k:sha(current[k]) for k in ids},'sourceReceipts':{k:m[k][0]+'-receipt.json' for k in ids},'receipt':name+'-author25-receipt.json','snapshot':name+'-cards.json','authorPass':25,'authorHold':0,'newCertified':0,'globalDuplicateReview':'global-duplicate-review-author100.json; actual author comparison separate from search mechanics'})
save('author100-manifest.json',{'status':'AUTHOR_PASS_ONLY_COMPLETE_AWAITING_DISTINCT_READER','role':'author','agentIdentity':'01a12ba2-6af8-79b3-96c4-14a4e60812b6','baselineCommit':'98c3a2b8f77315c96fafb3857aa9c9d0f0eb496c','cards':100,'fields':600,'authorPass':100,'authorHold':0,'independentCertified':0,'sourceReceipts':{c['id']:m[c['id']][0]+'-receipt.json' for c in t},'currentCardHashes':{c['id']:sha(c) for c in t},'receipt':'author100-receipt.json','snapshot':'author100-cards.json','frozenSubsets':['subset01-v2-freeze.json','subset02-freeze.json','subset03-freeze.json','subset04-freeze.json'],'priorFrozenCardsUnchanged':True,'preservation':{'idOrderDifficultyCorrectIndex':True,'quotas':quotas,'size':100,'noteWordsMax':35,'explanationWordsMax':70},'notCertification':'Every PASS here is an author judgment. A different identity must read each field/source and certify the exact card hash.'})
print(json.dumps({'authorCards':len(rows),'authorFields':sum(len(c['fields']) for c in rows),'quotas':quotas,'prior50Unchanged':True,'newSubsets':2,'providerLabelCorrections':len(corrections),'independentCertified':0}))
