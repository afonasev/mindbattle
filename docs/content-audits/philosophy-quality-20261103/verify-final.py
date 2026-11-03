"""Deterministic binding check for this philosophy100 revision; no semantic review."""
import json,hashlib,subprocess
from pathlib import Path
B=Path('docs/content-audits/philosophy-quality-20261103')
H=lambda q:hashlib.sha256(json.dumps(q,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
F=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
topic=Path('src/content/topics/philosophy.json');cur=json.load(open(topic));old=json.load(open(B/'before.json'));prior=json.load(open(B/'mechanical-02.json'))
assert subprocess.check_output(['git','show','ce4e62ab99abc3a9deb4ff2c038320673482fcea:'+str(B/'mechanical-02.json')])==(B/'mechanical-02.json').read_bytes()
assert cur['id']==old['id']=='philosophy' and len(cur['questions'])==100
out={'baseline':'1c049c04e0dfcd4cd7f8fe4bfb134bb55b43238c','topicSHA256':F(topic),'cards':[],'inheritedCheckpoint50':{'file':str(B/'mechanical-02.json'),'sha256':F(B/'mechanical-02.json'),'committedCheckpoint':'ce4e62ab99abc3a9deb4ff2c038320673482fcea','unchanged':'PASS'},'newReceiptFileBindings':[]}
for i,(q,before) in enumerate(zip(cur['questions'],old['questions']),1):
 assert q['id']==before['id'] and type(q['correctIndex']) is int and q['correctIndex']==before['correctIndex'];assert len(q['answers'])==4 and all(len(a['note'].split())<=35 for a in q['answers']) and len(q['explanation'].split())<=70
 if i<=50:
  priorrow=prior['cards'][i-1];assert priorrow['id']==q['id'] and priorrow['currentSHA256']==H(q);out['cards'].append({'order':i,'id':q['id'],'currentSHA256':H(q),'binding':priorrow['binding'],'receiptEvidence':'mechanical-02.json unchanged checkpoint50, with immutable reviewer dispositions','status':'PASS'})
for packet,version in [('51-60',1),('61-70',2),('71-75',1),('76-85',1),('86-95',1),('96-100',1)]:
 cp=B/f'cards-{packet}-v{version}.json';bp=B/f'bindings-{packet}-v{version}.json';rp=B/f'reviewer/final-{packet}-v{version}.json';cards=json.load(open(cp));bd=json.load(open(bp));r=json.load(open(rp));assert F(cp)==r['candidateFileSHA256'] and F(bp)==r['bindingsFileSHA256'];assert F(r['sourceIndexFile'])==r['sourceIndexSHA256'];out['newReceiptFileBindings'].append({'receipt':str(rp),'sha256':F(rp),'candidateSHA256':F(cp),'bindingsSHA256':F(bp),'sourceIndexSHA256':r['sourceIndexSHA256'],'status':'PASS'})
 for q,bi,rc in zip(cards,bd['cards'],r['cards']):
  n=bi['order'];assert q['id']==cur['questions'][n-1]['id'];assert H(q)==bi['candidateSHA256']==rc['currentSHA256'];assert rc['verdict']=='PASS_FINAL';assert H(old['questions'][n-1])==bi['preimageSHA256']
  if n!=80:assert H(cur['questions'][n-1])==H(q)
  out['cards'].append({'order':n,'id':q['id'],'currentSHA256':H(q),'binding':bp.name,'receipt':str(rp),'status':'PASS'})
  for contexts in [bi['mainContexts'],*bi['noteContexts'].values()]:
   for name,ranges in contexts.items():
    source=json.load(open(B/'sources'/(name+'-body.json')));assert len(ranges)%2==0 and all(0<=a<=z<source['totalLines'] for a,z in zip(ranges[::2],ranges[1::2]))
# The one directed note fix for80 chains to its already-reviewed v1 preimage.
bp=B/'bindings-80-directed-v2.json';cp=B/'cards-80-directed-v2.json';rp=B/'reviewer/final-80-directed-v2.json';bd=json.load(open(bp));q=json.load(open(cp))[0];r=json.load(open(rp));v1=json.load(open(B/'cards-76-85-v1.json'))[4];assert bd['cards'][0]['preimageSHA256']==H(v1);assert H(q)==H(cur['questions'][79])==r['card']['currentSHA256']==bd['cards'][0]['candidateSHA256'];assert r['card']['verdict']=='PASS_FINAL';assert F(cp)==r['candidateFileSHA256'] and F(bp)==r['bindingsFileSHA256'];assert F(r['sourceIndexFile'])==r['sourceIndexSHA256'];out['cards'][79].update(currentSHA256=H(q),binding=bp.name,receipt=str(rp),preimageChain='v1FINAL -> one directed note fix -> v2FINAL PASS');out['newReceiptFileBindings'].append({'receipt':str(rp),'sha256':F(rp),'status':'PASS'})
assert [c['order'] for c in out['cards']]==list(range(1,101))
out['sourceBodies']=[];bodybyurl={}
for p in (B/'sources').glob('*-body.json'):
 d=json.load(open(p));assert hashlib.sha256(d['text'].encode()).hexdigest()==d['bodySHA256'] and len(d['text'].splitlines())==d['totalLines'];bodybyurl[d['url']]=d['bodySHA256'];out['sourceBodies'].append({'path':str(p),'bodySHA256':d['bodySHA256'],'status':'PASS'})
out['immutableSourceIndexes']=[]
for p in (B/'sources').glob('index-*.json'):
 assert F(p)==p.stem[6:]
 for d in json.load(open(p)):assert bodybyurl[d['url']]==d['bodySHA256']
 out['immutableSourceIndexes'].append({'path':str(p),'sha256':F(p),'status':'PASS'})
counts={d:[sum(q['difficulty']==d and q['correctIndex']==i for q in cur['questions']) for i in range(4)] for d in ['easy','medium','hard']};assert counts=={'easy':[10]*4,'medium':[10]*4,'hard':[5]*4};out['quotaAndKeys']=counts;out['frozenFields']='100 ID/topic/order/integer correctIndex PASS';out['status']='PASS';out['freshIndependentFinalCount']=100;out['semanticReview']='Sole independent reviewer immutable INITIAL/FINAL receipts, not inferred from hashes';out['humanAcceptance']='NotRun; separate human decision';(B/'mechanical-final.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print('PASS100exactbindings/frozen/quotas;',len(out['sourceBodies']),'fullsourcebodies;',len(out['immutableSourceIndexes']),'immutableindexes')
