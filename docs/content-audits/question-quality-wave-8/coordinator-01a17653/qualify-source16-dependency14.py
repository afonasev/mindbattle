"""Exact raw16 plus its same-author14 addendum; no new editorial judgment."""
import pathlib,json,importlib.util,subprocess,copy
D=pathlib.Path(__file__).parent;s=importlib.util.spec_from_file_location('m',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
x=m.read(D/'manifest.json');R=D/'source-cars-road-transport16';B=D/'qualified-source-cars-road-transport16';assert not B.exists()
proof=m.read(D/'cars-road-transport16-native-proof.json');freeze='a1b7ce30b69131666a2b910660cd2f1aee915325'
for name,digest in proof['rawFileSHA256'].items():
 p=R/name;assert m.raw(p)==digest and p.read_bytes()==subprocess.check_output(['git','-C',str(m.C),'show',freeze+':'+str(p.relative_to(m.C))])
ca,sp,ps=[m.read(R/n) for n in ['candidate.json','sourceproof.json','peer-snapshot.json']];e=ca['entries'][0];clarpath=R/'dependency14-addendum.json';c=m.read(clarpath);uid=x['actors']['author15']['threadId']
assert ca['sourceNativeId']==sp['sourceNativeId']==ps['sourceNativeId']==proof['sourceNativeId']==c['authorNativeId']==uid
assert ca['cycle']==sp['cycle']==ps['cycle']==0 and e['sourceOrder']==c['assignedSourceOrder']==16
assert c['assignedCardId']==e['id'] and c['originalReadyRawFilesRemainFrozen'] and c['originalReadyCandidatePacketSHA256']==m.raw(R/'candidate.json') and c['originalReadyCandidateCardSHA256']==e['afterHash']==m.sha(e['proposedCard'])
rp=D/'qualified-source-cars-road-transport14-cycle1-apply.json';app=m.read(rp)['applied'][0];dep=c['catalogDependency'];tp=m.C/'src/content/topics/cars-road-transport.json';live=m.read(tp)
assert dep['applyReport']==str(rp) and dep['applyReportSHA256']==m.raw(rp) and dep['appliedFullCard']==app['proposedCard']==live['questions'][13]
assert dep['canonicalCardSHA256']==m.sha(dep['appliedFullCard'])
for side in ['source14','source16']:assert all(c['bilateralMAINComparison'][side][k] for k in ['entity','relation','value','context'])
assert c['bilateralMAINComparison']['distinctness'] and c['bilateralMAINComparison']['directReverseCheck'] and c['noSourceOrCycleChange']
assert c['proposedSource16Main']['prompt']==e['proposedCard']['prompt'] and c['proposedSource16Main']['correctAnswer']==e['proposedCard']['answers'][e['proposedCard']['correctIndex']]['text']
task=m.read(D/'source-cars-road-transport16-task.json');oldbytes=subprocess.check_output(['git','-C',str(m.C),'show',task['baselineCode']+':'+str(tp.relative_to(m.C))]);before=json.loads(oldbytes)
assert [v['card'] for v in ps['actualCurrentPeers']]==before['questions'] and [v['sourceOrder'] for v in ps['actualCurrentPeers']]==list(range(1,101))
assert all(v['id']==v['card']['id'] and v['sha256']==m.sha(v['card']) for v in ps['actualCurrentPeers'])
assert [i for i,(a,b) in enumerate(zip(before['questions'],live['questions']),1) if a!=b]==[14]
assert before['questions'][13]==app['beforeCard'] and live['questions'][15]==e['beforeCard'] and m.sha(e['beforeCard'])==e['beforeHash']
invpath=pathlib.Path(c['freshInventory']['path']);assert invpath.is_relative_to(R) and m.raw(invpath)==c['freshInventory']['fileSHA256'];inv=m.read(invpath)
assert inv['sameTopicMAIN']['questions']==live['questions'] and inv['sameTopicMAIN']['fileSHA256']==m.raw(tp)
oldrows=[];nowrows=[];bindings=ps['globalMAIN']['allCurrentFileByteBindings'];assert len(bindings)==110
for b in bindings:
 p=m.C/b['path'];now=m.read(p);old=before if p==tp else now
 assert b['sha256']==(__import__('hashlib').sha256(oldbytes).hexdigest() if p==tp else m.raw(p))
 oldrows.extend({'topicId':old['id'],'id':q['id'],'prompt':q['prompt'],'answers':[a['text'] for a in q['answers']],'correctIndex':q['correctIndex']} for q in old['questions'])
 nowrows.extend({'topicId':now['id'],'id':q['id'],'prompt':q['prompt'],'answers':[a['text'] for a in q['answers']],'correctIndex':q['correctIndex']} for q in now['questions'])
assert len(oldrows)==len(nowrows)==11000 and oldrows==ps['globalMAIN']['rows'] and m.sha(oldrows)==ps['globalMAIN']['rowsCanonicalSHA256']
assert nowrows==inv['globalMAIN']['rows'] and m.sha(nowrows)==inv['globalMAIN']['rowsCanonicalSHA256']
for b in inv['globalMAIN']['allCurrentFileByteBindings']:assert m.raw(m.C/b['path'])==b['sha256']
for v in ps['actualCurrentPeers']:
 if v['sourceOrder']==14:v.update(card=copy.deepcopy(app['proposedCard']),sha256=m.sha(app['proposedCard']))
ps['globalMAIN']=copy.deepcopy(inv['globalMAIN']);ps['sameTopicMAIN']=copy.deepcopy(inv['sameTopicMAIN'])
binding={'owner':m.O,'targetOrder':16,'changedOrder':14,'authorNativeId':uid,'rawFreeze':freeze,'rawAllFilesSHA256':proof['rawFileSHA256'],'authorClarification':str(clarpath),'authorClarificationSHA256':m.raw(clarpath),'knownApplyReport':str(rp),'knownApplyReportSHA256':m.raw(rp),'originalCatalogBaseline':task['baselineCode'],'originalInventoryExplicitlyHistorical':True,'allOther99CardsAnd109FilesExact':True,'originalRelevantPeerAssessmentsRetained':True,'newAuthorBilateralAssessmentPointer':'/bilateralMAINComparison','newCurrent14BodyPointer':'/catalogDependency/appliedFullCard','historicalBeforeAfterHashListNotInvented':True,'noRootSemanticJudgment':True,'qualityCredit':0,'operation':'Exact single14 dependency body/hash and full-current technical inventory overlay, signed by same original author. Rawcritical files and all source bytes unchanged. Expose existing mutual distinctness and directreverse alongside original old14 assessment.'}
ps['technicalConcurrentDependencyAlias']=binding;ps['sameAuthorCurrent14DependencyAssessment']=copy.deepcopy(c);sp['technicalConcurrentDependencyAlias']=binding
m.assert_retained_source_admissibility(sp)
B.mkdir()
for name,v in [('candidate.json',ca),('sourceproof.json',sp),('peer-snapshot.json',ps)]:m.write(B/name,v)
s=importlib.util.spec_from_file_location('apply',m.C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a=importlib.util.module_from_spec(s);s.loader.exec_module(a);a.P=m.P
report=a.apply(B,uid,[16],D/'source-cars-road-transport16-apply.json',D/'qa-qualified-source-cars-road-transport16.json',pathlib.Path(__file__),qualifyOnly=True,peerSnapshot={'actualCurrentPeers':ps['actualCurrentPeers']});report.update(status='MECHANICAL_CONCURRENT_DELTA_INTAKE_PASS_PENDING_INDEPENDENT_REVIEW',qualityCredit=0,concurrentDependencyAlias=binding)
rp=D/'source-cars-road-transport16-intake.json';bp=D/'source16-current14-dependency-binding.json';m.write(rp,report);m.write(bp,binding)
x['pendingCarsRoadTransport16']={'id':e['id'],'actorKey':'author15','status':'QUALIFIED_READY_CURRENT14_BOUND','qualityCredit':0,'beforeHash':e['beforeHash'],'afterHash':e['afterHash'],'rawPacket':str(R),'rawFreeze':freeze,'qualifiedPacket':str(B),'actualWebCalls':2,'sourceActualCompactions':proof['actualCompactions'],'sourceNativeProof':str(D/'cars-road-transport16-native-proof.json'),'sourceNetworkAccounting':str(D/'cars-road-transport16-network-accounting.json'),'sameAuthorDependencyClarification':str(clarpath),'actualPeerDependencyBinding':str(bp)}
x['actors']['author15']['cursor']='8935f8dc-2634-44e1-b9f3-dce0f59eddf6:20';x['sourceActorKeys']=[k for k in x['sourceActorKeys'] if k!='author15'];x['readyQueue']=[{'id':e['id'],'sourceOrder':16,'packet':str(B)}];m.write(D/'manifest.json',x)
print(m.savecode([*B.glob('*.json'),rp,bp,D/'manifest.json',pathlib.Path(__file__)],'Qualify unchanged16 raw with exact same-author current14 dependency addendum'))
