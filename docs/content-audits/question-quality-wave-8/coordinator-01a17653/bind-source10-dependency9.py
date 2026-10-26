"""Bind the exact same-author10 clarification to applied9; no semantic decision."""
import pathlib,importlib.util,json,subprocess
D=pathlib.Path(__file__).parent
s=importlib.util.spec_from_file_location('m',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
x=m.read(D/'manifest.json');P=D/'source10-current9-dependency';clar=P/'clarification.json';c=m.read(clar);R=D/'source-cars-road-transport10';B=D/'qualified-source-cars-road-transport10'
e=m.read(R/'candidate.json')['entries'][0];native=m.read(D/'cars-road-transport10-native-proof.json');uid=x['actors']['author8']['threadId']
assert c['sourceNativeId']==native['sourceNativeId']==uid and c['cycle']==0 and c['status']=='DEPENDENCY_CLEAR' and c['sourceRequests']==0 and c['rawUntouched']
for name,digest in native['rawFileSHA256'].items():
 assert m.raw(R/name)==digest and (R/name).read_bytes()==subprocess.check_output(['git','-C',str(m.C),'show',x['pendingCarsRoadTransport10']['rawFreeze']+':'+str((R/name).relative_to(m.C))])
for name in ['candidate.json','sourceproof.json','peer-snapshot.json']:
 assert c['rawCriticalSHA256']['before']['files'][name]==c['rawCriticalSHA256']['after']['files'][name]==m.raw(R/name)
 assert (B/name).read_bytes()==subprocess.check_output(['git','-C',str(m.C),'show',x['pendingCarsRoadTransport10']['qualifiedFreeze']+':'+str((B/name).relative_to(m.C))])
assert c['unchangedTarget10']['originalProposedCard']==e['proposedCard'] and c['unchangedTarget10']['proposedAfterHash']==e['afterHash']==m.sha(e['proposedCard'])
rp=D/'qualified-source-cars-road-transport9-cycle1-apply.json';app=m.read(rp)['applied'][0];changed=c['changedCurrent9'];live=m.read(m.C/'src/content/topics/cars-road-transport.json')
assert changed['applyReport']==str(rp) and changed['applyReportSHA256']==m.raw(rp)
assert changed['body']==app['proposedCard']==live['questions'][8] and changed['canonicalSHA256']==m.sha(changed['body'])
assert c['unchangedTarget10']['actualCurrentBody']==e['beforeCard']==live['questions'][9]
for group in ['actual10AgainstNew9','originalProposal10AgainstNew9']:
 for direction in ['source10ToCurrent9','current9ToSource10']:
  assert all(c['bilateralSemanticAssessment'][group][direction][k] for k in ['entity','relation','value','context','finding','directReverseCheck'])
invpath=pathlib.Path(c['freshInventory']['path']);assert invpath.is_relative_to(P) and m.raw(invpath)==c['freshInventory']['sha256'];inv=m.read(invpath)
assert inv['sameTopicMAIN']['questions']==live['questions'] and inv['sameTopicMAIN']['fileSHA256']==m.raw(m.C/'src/content/topics/cars-road-transport.json')
old=m.read(B/'peer-snapshot.json');assert len(old['actualCurrentPeers'])==100
before=[v['card'] for v in old['actualCurrentPeers']];assert [i for i,(a,b) in enumerate(zip(before,live['questions']),1) if a!=b]==[9]
assert before[8]==app['beforeCard']
assert len(inv['globalMAIN']['allCurrentFileByteBindings'])==110
for b in inv['globalMAIN']['allCurrentFileByteBindings']:assert m.raw(m.C/b['path'])==b['sha256']
rows=[]
for b in inv['globalMAIN']['allCurrentFileByteBindings']:
 t=m.read(m.C/b['path']);rows.extend({'topicId':t['id'],'id':q['id'],'prompt':q['prompt'],'answers':[v['text'] for v in q['answers']],'correctIndex':q['correctIndex']} for q in t['questions'])
assert len(rows)==11000 and rows==inv['globalMAIN']['rows'] and m.sha(rows)==inv['globalMAIN']['rowsCanonicalSHA256']
for oldb,newb in zip(old['globalMAIN']['allCurrentFileByteBindings'],inv['globalMAIN']['allCurrentFileByteBindings']):
 assert oldb['path']==newb['path']
 if oldb['path']!='src/content/topics/cars-road-transport.json':assert oldb==newb
proof=D/'source10-current9-dependency-binding.json';delta=D/'source10-current-peer-addendum.json'
m.write(proof,{'owner':m.O,'sourceNativeId':uid,'cycle':0,'targetOrder':10,'changedOrder':9,'clarification':str(clar),'clarificationSHA256':m.raw(clar),'rawFreeze':x['pendingCarsRoadTransport10']['rawFreeze'],'qualifiedFreeze':x['pendingCarsRoadTransport10']['qualifiedFreeze'],'knownApplyReport':str(rp),'knownApplyReportSHA256':m.raw(rp),'allRawAndQualifiedUnchanged':True,'exactSingleAppliedPeerDelta':9,'currentInventory':str(invpath),'currentInventorySHA256':m.raw(invpath),'noRootSemanticDecision':True,'qualityCredit':0})
m.write(delta,{'actualCurrentPeers':[{'id':changed['body']['id'],'topicId':'cars-road-transport','sourceOrder':9,'card':changed['body'],'sha256':changed['canonicalSHA256']}],'dependencyBinding':str(proof),'dependencyBindingSHA256':m.raw(proof)})
x['pendingCarsRoadTransport10'].update(actualPeerDependencyAddendum=str(delta),actualPeerDependencyBinding=str(proof),sameAuthorDependencyClarification=str(clar))
a=x['actors']['author8'];nr=[json.loads(l) for l in pathlib.Path(a['nativeJournal']).open()];assert next(r['payload']['type'] for r in reversed(nr) if r.get('payload',{}).get('type') in ['task_started','task_complete'])=='task_complete';info=next(r['payload']['info'] for r in reversed(nr) if r.get('payload',{}).get('type')=='token_count');a.update(stage='IDLE_AFTER_SOURCE10_DEPENDENCY9',lastTaskEvent='task_complete',actualCompactions=sum(r['type']=='compacted' for r in nr),lastInput=info['last_token_usage']['input_tokens'],modelWindow=info['model_context_window'],cursor='8ddd7317-2c7e-4647-9e02-5b0f9acee3bd:50');x['sourceActorKeys']=[];m.write(D/'manifest.json',x)
print(m.savecode([proof,delta,*[p for p in P.rglob('*') if p.is_file()],D/'manifest.json',pathlib.Path(__file__)],'Bind same-author CARS10 assessment of exact revised CARS9 dependency'))
