"""Mechanical freeze of explicit reviewed receipts; creates no editorial verdict."""
import json,pathlib,sys,hashlib,collections,subprocess
P=pathlib.Path(__file__).resolve().parent;R=P.parents[4];name=sys.argv[1]
def load(p):return json.loads(p.read_text())
def h(o):return hashlib.sha256(json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
b=load(P/'baseline.json');c=load(R/'src/content/topics/architecture.json');r=load(P/(name+'-receipt.json'));byid={x['id']:x for x in c['questions']};checks=load(P/(name+'-roundtrip.json'));assert checks['mechanicallyValid']
assert [(q['id'],q['difficulty'],q['correctIndex']) for q in b['questions']]==[(q['id'],q['difficulty'],q['correctIndex']) for q in c['questions']]
for f in P.glob('*-freeze.json'):
 for row in load(f)['cards']:assert row['cardCanonicalSha256']==h(byid[row['questionId']])
for row in r['cards']:assert row['cardCanonicalSha256']==h(byid[row['questionId']])
manifest={'batch':name,'state':'READY_FOR_INDEPENDENT','role':'author','agentIdentity':r['agentIdentity'],'count':len(r['cards']),'fieldCount':sum(len(x['fields']) for x in r['cards']),'receipt':name+'-receipt.json','roundtrip':name+'-roundtrip.json','cards':[{'questionId':x['questionId'],'cardCanonicalSha256':x['cardCanonicalSha256'],'authorVerdict':x['verdict']} for x in r['cards']],'sourceByteHashes':{x['rawCapture']:x['rawCaptureSha256'] for row in r['cards'] for f in row['fields'] for x in f['proofs']},'immutableFrozen':True,'independentVerdicts':0,'rootCertified':False}
(P/(name+'-freeze.json')).write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
fs=sorted(P.glob('*-freeze.json'));ids=[row['questionId'] for f in fs for row in load(f)['cards']];assert len(ids)==len(set(ids));assert all(x==y for x,y in zip(c['questions'],b['questions']) if x['id'] not in ids)
(P/'READY.json').write_text(json.dumps({'authorReadyBatches':[f.name for f in fs],'authorCards':len(ids),'authorFields':len(ids)*6,'remainingIds':[q['id'] for q in c['questions'] if q['id'] not in ids],'noIndependentOrRootCertification':True},ensure_ascii=False,indent=2)+'\n')
(P/(name+'-preservation.json')).write_text(json.dumps({'idsOrderDifficultyCorrectIndexPreserved':True,'allPriorFrozenHashesUnchanged':True,'otherArchitectureSlotsUnchanged':True,'difficultyCounts':dict(collections.Counter(q['difficulty'] for q in c['questions'])),'keyPositions':{d:dict(collections.Counter(q['correctIndex'] for q in c['questions'] if q['difficulty']==d)) for d in ['easy','medium','hard']},'fullTestsNotRun':True},indent=2)+'\n')
print(name,len(r['cards']),len(ids),'author only')
