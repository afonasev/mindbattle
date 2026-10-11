"""Mechanical freeze/preservation only. Never assigns substantive verdicts."""
import json,hashlib,subprocess,collections,os
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parents[4]
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def save(name,value):(B/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
receipt=json.loads((B/'receipt.json').read_text());baseline=json.loads((B/'baseline.json').read_text());topic=json.loads((ROOT/'src/content/topics/winter-sports.json').read_text());old={c['id']:c for c in baseline['topic']['questions']};scope=set(baseline['scope']);current={c['id']:c for c in topic['questions']}
assert list(old)==list(current)
assert {r['questionId'] for r in receipt['cards']}==scope
changed=[];frozen=[]
for qid,c in current.items():
 assert(c['difficulty'],c['correctIndex'])==(old[qid]['difficulty'],old[qid]['correctIndex'])
 if old[qid]!=c:assert qid in scope;changed.append(qid)
 if qid not in scope:assert old[qid]==c;frozen.append({'id':qid,'sha256':sha(canon(c))})
quotas={l:[sum(c['difficulty']==l and c['correctIndex']==n for c in current.values()) for n in range(4)] for l in ['easy','medium','hard']}
assert quotas=={'easy':[10]*4,'medium':[10]*4,'hard':[5]*4}
raws={B/p['rawCapture']:p['rawCaptureSha256'] for c in receipt['cards'] for f in c['fields'] for p in f['proofs']};rawreport=[]
for path,h in raws.items():
 body=path.read_bytes();assert sha(body)==h
 blob=subprocess.check_output(['git','hash-object','-w','--path='+str(path.relative_to(ROOT)),str(path)],cwd=ROOT,text=True).strip();gitbody=subprocess.check_output(['git','cat-file','blob',blob],cwd=ROOT);assert gitbody==body
 rawreport.append({'path':str(path.relative_to(ROOT)),'sha256':h,'gitBlob':blob,'workingEqualsFilteredGitBlob':True})
freeze=[]
for c in sorted(receipt['cards'],key=lambda r:r['questionId']):
 assert c['cardCanonicalSha256']==sha(canon(current[c['questionId']]))
 freeze.append({'questionId':c['questionId'],'cardCanonicalSha256':c['cardCanonicalSha256'],'authorVerdict':c['verdict'],'literalHashes':{f['field']:f['literalSha256'] for f in c['fields']}})
bytehash=sha((ROOT/'src/content/topics/winter-sports.json').read_bytes())
save('preservation.json',{'baseline':baseline['head'],'changedIds':changed,'changedCount':len(changed),'fixedIdOrderDifficultyCorrectIndex':True,'frozen81':frozen,'positionQuotas':quotas,'topicByteSha256':bytehash})
save('freeze19.json',{'agentIdentity':receipt['agentIdentity'],'role':'author','topicByteSha256':bytehash,'receiptSha256':sha((B/'receipt.json').read_bytes()),'cards':freeze,'newCertified':0})
save('working-git-roundtrip.json',rawreport)
save('READY.json',{'readyForIndependentRead':[c['questionId'] for c in receipt['cards'] if c['verdict']=='PASS'],'authorHolds':[c['questionId'] for c in receipt['cards'] if c['verdict']!='PASS'],'sourceFieldsRead':sum(len(c['fields']) for c in receipt['cards']),'newCertified':0,'role':'author','agentIdentity':receipt['agentIdentity'],'receipt':'receipt.json','freeze':'freeze19.json','history':['pilot5-receipt.json','receipt-before-final-refinement.json','receipt-before-boundary-review.json'],'supersedesForThese19Only':['../resume-2026-10-11-author100/author100-receipt.json'],'independentBaselineStillHistorical':'../../independent-pilot/resume-2026-10-11-winter-first25/receipt.json','requires':'Fresh independent six-field current-hash reading; coordinator alone certifies paired records','limits':['5 author HOLD are not ready or certified','Preserved other81 including independentPASS009/011/012/013/014/025','No wave completion, root certification, main integration, deployment or archive']})
save('summary.json',{'baselineHead':baseline['head'],'snapshotHead':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'branch':subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip(),'authorIdentity':os.environ['CODEX_THREAD_ID'],'counts':dict(collections.Counter(c['verdict'] for c in receipt['cards'])),'cardsRead':19,'fieldsRead':114,'topicByteSha256':bytehash,'rawOriginals':len(raws),'mechanicallyValid':json.loads((B/'roundtrip-final19.json').read_text())['mechanicallyValid'],'qa':{'typecheckFinalExit':0,'finalAffectedTests':{'passed':19,'failed':0,'skipped':0},'initialCatalogPlusConsumers':{'passed':19,'failed':1,'failure':'architecture current review byte hash mismatch in catalog-full.test.ts; outside ownership; no stamps changed'},'catalogReviewGate':'OPEN, including no completed winter topic certificate','fullSuiteBuildDeployRun':False},'specSha256':sha(Path('/Users/eaafonasev/Projects/mindbattle-planning/docs/GAME_SPEC.md').read_bytes()),'certifiedByThisAuthor':0})
print('freeze preserved19; frozen81; originals',len(raws),'author decisions',collections.Counter(c['verdict'] for c in receipt['cards']))
