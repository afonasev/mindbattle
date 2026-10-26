"""Bind known non-MAIN deltas without changing a qualified packet or its judgments."""
import pathlib,json,subprocess,importlib.util,sys,hashlib
D=pathlib.Path(__file__).parent
s=importlib.util.spec_from_file_location('m',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
order=int(sys.argv[1]);report_names=sys.argv[2:];assert report_names
x=m.read(D/'manifest.json');topic=x['activeRoute']['topicId'];B=D/f'qualified-source-{topic}{order}';R=D/f'source-{topic}{order}'
assert all(m.flow.get(cid)[1]['owner']==m.O for cid in x['claims']) and m.read(m.P/'.flow-leases.json')=={}
ca=m.read(B/'candidate.json');ps=m.read(B/'peer-snapshot.json');rawps=m.read(R/'peer-snapshot.json');e=ca['entries'][0]
assert e['sourceOrder']==order and ca['cycle']==0
peers=ps['actualCurrentPeers'];assert len(peers)==100 and [p['sourceOrder'] for p in peers]==list(range(1,101))
assert all(p['id']==p['card']['id'] and p['topicId']==topic and p['sha256']==m.sha(p['card']) for p in peers)
old=[p['card'] for p in peers];tp=m.C/f'src/content/topics/{topic}.json';live=m.read(tp)
assert live['questions'][order-1]==e['beforeCard'] and m.sha(e['beforeCard'])==e['beforeHash']
def main(q):return {'id':q['id'],'prompt':q['prompt'],'answers':[a['text'] for a in q['answers']],'correctIndex':q['correctIndex']}
assert [main(q) for q in old]==[main(q) for q in live['questions']], 'Any MAIN delta requires author dependency assessment'
changed=[i for i,(a,b) in enumerate(zip(old,live['questions']),1) if a!=b];assert changed and order not in changed
assessment_ids=set()
def ids(v):
 if isinstance(v,dict):
  for k,w in v.items():
   if k in ['id','questionId'] and isinstance(w,str):assessment_ids.add(w)
   else:ids(w)
 elif isinstance(v,list):
  for w in v:ids(w)
for k,v in rawps.items():
 if k not in ['actualCurrentPeers','globalMAIN','sameTopicMAIN','inventoryBinding']:ids(v)
assert not {old[i-1]['id'] for i in changed}&assessment_ids, 'Changed substantively assessed peer needs same-author clarification'
known={};reports=[]
for name in report_names:
 assert pathlib.Path(name).name==name
 p=D/name;a=m.read(p);assert len(a['applied'])==1;z=a['applied'][0];i=z['sourceOrder']
 assert i in changed and i not in known
 assert z['beforeCard']==old[i-1] and z['proposedCard']==live['questions'][i-1]
 assert main(z['beforeCard'])==main(z['proposedCard'])
 assert all(z['beforeCard'][k]==z['proposedCard'][k] for k in ['id','difficulty','correctIndex'])
 known[i]=z;reports.append({'path':str(p),'rawSHA256':m.raw(p),'sourceOrder':i,'beforeCardSHA256':m.sha(z['beforeCard']),'afterCardSHA256':m.sha(z['proposedCard'])})
assert sorted(known)==changed
task=m.read(D/f'source-{topic}{order}-task.json');oldbytes=subprocess.check_output(['git','-C',str(m.C),'show',task['baselineCode']+':'+str(tp.relative_to(m.C))])
assert json.loads(oldbytes)['questions']==old
bindings=ps['globalMAIN']['allCurrentFileByteBindings'];assert len(bindings)==110
rows=[]
for b in bindings:
 p=m.C/b['path'];t=m.read(p)
 if p==tp:assert b['sha256']==hashlib.sha256(oldbytes).hexdigest()
 else:assert b['sha256']==m.raw(p)
 rows.extend({'topicId':t['id'],**main(q)} for q in t['questions'])
assert len(rows)==11000 and m.sha(rows)==ps['globalMAIN']['rowsCanonicalSHA256']
proof=D/f'source{order}-unaffected-main-peer-binding.json';delta=D/f'source{order}-current-peer-addendum.json';assert not proof.exists() and not delta.exists()
m.write(proof,{'owner':m.O,'sourceOrder':order,'rawPacket':str(R),'rawPeerSHA256':m.raw(R/'peer-snapshot.json'),'qualifiedPacket':str(B),'qualifiedCriticalSHA256':{n:m.raw(B/n) for n in ['candidate.json','sourceproof.json','peer-snapshot.json']},'originalCatalogCommit':task['baselineCode'],'knownApplyReports':reports,'changedOrders':changed,'all100MAINProjectionsUnchanged':True,'all11000MAINRowsUnchanged':True,'all109OtherFileBindingsExact':True,'changedPeersOutsideOriginalSubstantivePairs':True,'rawAndQualifiedUnchanged':True,'qualityCredit':0,'operation':'Existing peerAddendum API overlays only exact known applied non-MAIN peer bodies. Original inventory stays explicitly historical; full original relevant pair bodies and judgments unchanged. No new semantic assessment or source adoption.'})
m.write(delta,{'actualCurrentPeers':[{'id':live['questions'][i-1]['id'],'topicId':topic,'sourceOrder':i,'card':live['questions'][i-1],'sha256':m.sha(live['questions'][i-1])} for i in changed],'dependencyBinding':str(proof),'dependencyBindingSHA256':m.raw(proof)})
print(m.savecode([proof,delta,pathlib.Path(__file__)],f'Bind unchanged MAIN peer deltas for preserved SOURCE{order}'))
print(json.dumps({'sourceOrder':order,'changedOrders':changed,'MAINRowsUnchanged':11000,'rawAndQualifiedUntouched':True,'qualityCredit':0}))
