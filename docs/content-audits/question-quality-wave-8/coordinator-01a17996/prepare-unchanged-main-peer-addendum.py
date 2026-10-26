"""Exact actual peer addendum when only non-MAIN fields changed; no semantic judgment."""
from pathlib import Path
import importlib.util,json,sys,subprocess,hashlib
D=Path(__file__).parent
s=importlib.util.spec_from_file_location('m',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
order,changed=map(int,sys.argv[1:3]);raw_freeze,qualified_freeze,report_name=sys.argv[3:6]
assert Path(report_name).name==report_name and order!=changed
x=m.read(D/'manifest.json');topic=x['activeRoute']['topicId'];R=D/f'source-{topic}{order}';B=D/f'qualified-source-{topic}{order}'
assert x['owner']==m.O and all(m.flow.get(cid)[1]['owner']==m.O for cid in x['claims']) and m.read(m.P/'.flow-leases.json')=={}
ca=m.read(B/'candidate.json');e=ca['entries'][0];ps=m.read(B/'peer-snapshot.json');native=m.read(D/f'{topic}{order}-native-proof.json')
assert ca['cycle']==0 and e['status']=='READY_FOR_INDEPENDENT_REVIEW' and e['sourceOrder']==order and e['topicId']==topic
assert ca['sourceNativeId']==native['sourceNativeId']==x['actors'][x[f'pendingCarsRoadTransport{order}']['actorKey']]['threadId']
def at(ref,p):return subprocess.check_output(['git','-C',str(m.C),'show',ref+':'+str(p.relative_to(m.C))])
for name in ['candidate.json','sourceproof.json','peer-snapshot.json']:assert (B/name).read_bytes()==at(qualified_freeze,B/name)
for name,digest in native['rawFileSHA256'].items():assert m.raw(R/name)==digest and (R/name).read_bytes()==at(raw_freeze,R/name)
report=D/report_name;app=m.read(report)['applied'];assert len(app)==1;app=app[0];old,new=app['beforeCard'],app['proposedCard']
assert app['sourceOrder']==changed and old['id']==new['id']
def main(q):return {'id':q['id'],'prompt':q['prompt'],'answers':[a['text'] for a in q['answers']],'correctIndex':q['correctIndex']}
assert main(old)==main(new) and old['difficulty']==new['difficulty'] and old!=new, 'Only a verified non-MAIN delta may be overlaid without a new semantic peer judgment'
tp=m.C/f'src/content/topics/{topic}.json';live=m.read(tp);task=m.read(D/f'source-{topic}{order}-task.json');oldbytes=at(task['baselineCode'],tp);before=json.loads(oldbytes)
assert [q['id'] for q in before['questions']]==[q['id'] for q in live['questions']]
assert [i for i,(a,b) in enumerate(zip(before['questions'],live['questions']),1) if a!=b]==[changed]
assert before['questions'][changed-1]==old and live['questions'][changed-1]==new
assert live['questions'][order-1]==e['beforeCard'] and m.sha(e['beforeCard'])==e['beforeHash']
peers=ps['actualCurrentPeers'];assert len(peers)==100 and [p['sourceOrder'] for p in peers]==list(range(1,101)) and [p['card'] for p in peers]==before['questions']
assert all(p['topicId']==topic and p['id']==p['card']['id'] and p['sha256']==m.sha(p['card']) for p in peers)
files=sorted((m.C/'src/content/topics').glob('*.json'));bindings=ps['globalMAIN']['allCurrentFileByteBindings'];assert len(files)==len(bindings)==110
rows=[]
for p,b in zip(files,bindings):
 assert b['path']==str(p.relative_to(m.C));assert b['sha256']==(hashlib.sha256(oldbytes).hexdigest() if p==tp else m.raw(p))
 t=m.read(p);rows.extend({'topicId':t['id'],**main(q)} for q in t['questions'])
assert len(rows)==11000 and m.sha(rows)==ps['globalMAIN']['rowsCanonicalSHA256']
if 'rows' in ps['globalMAIN']:assert ps['globalMAIN']['rows']==rows
proof=D/f'source{order}-unchanged-main-dependency-binding.json';delta=D/f'source{order}-current-peer-addendum.json';assert not proof.exists() and not delta.exists()
m.write(proof,{'owner':m.O,'targetOrder':order,'changedOrder':changed,'changedId':new['id'],'rawOriginalFreeze':raw_freeze,'originalQualifiedFreeze':qualified_freeze,'knownApplyReport':str(report),'knownApplyReportSHA256':m.raw(report),'beforePeerSHA256':m.sha(old),'actualPeerSHA256':m.sha(new),'oldAndActualMAINIdentical':True,'frozenIdDifficultyNumericKeyIdentical':True,'allOther99TopicCardsAnd109FilesExact':True,'all11000MAINRowsUnchanged':True,'originalRawAndQualifiedSnapshotsRemainImmutableHistorical':True,'liveTopicFileSHA256':m.raw(tp),'noNewSourceCycleSemanticJudgmentOrQualityCredit':True,'operation':'Existing standard apply peerAddendum API overlays only exact actual non-MAIN changed body. Original author bilateral MAIN grounds remain attributed to author; independent reviewer must personally read relevant actual CURRENT peers.'})
m.write(delta,{'actualCurrentPeers':[{'id':new['id'],'topicId':topic,'sourceOrder':changed,'card':new,'sha256':m.sha(new)}],'dependencyBinding':str(proof),'dependencyBindingSHA256':m.raw(proof)})
print(m.savecode([proof,delta,Path(__file__)],f'Bind exact unchanged-MAIN peer{changed} addendum for READY{order} without new judgment'))
print({'order':order,'changed':changed,'MAINUnchanged':True,'rawAndQualifiedUntouched':True,'peerAddendum':str(delta)})
