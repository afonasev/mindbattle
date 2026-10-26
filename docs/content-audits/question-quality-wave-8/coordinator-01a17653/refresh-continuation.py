"""Compact projection of canonical state; no quality decision, history dump or QA."""
import pathlib,importlib.util,json,datetime,re
D=pathlib.Path(__file__).parent
s=importlib.util.spec_from_file_location('m',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
x=m.read(D/'manifest.json');cp=m.read(pathlib.Path(x['canonicalCheckpoint']));n=len(cp['currentEligibleCompletedIds'])
assert cp['owner']==m.O and x['CURRENT']==n and x['remaining']==2000-n
assert all(m.flow.get(cid)[1]['owner']==m.O for cid in x['claims'])
assert m.read(m.P/'.flow-leases.json')=={}
def native(a):
 p=pathlib.Path(a['nativeJournal']);r=[json.loads(l) for l in p.open()]
 assert [v['payload']['id'] for v in r if v.get('type')=='session_meta']==[a['threadId']]
 info=next(v['payload']['info'] for v in reversed(r) if v.get('payload',{}).get('type')=='token_count')
 ev=next(v['payload']['type'] for v in reversed(r) if v.get('payload',{}).get('type') in ['task_started','task_complete'])
 return {'threadId':a['threadId'],'nativeJournal':str(p),'actualCompactions':sum(v.get('type')=='compacted' for v in r),'lastTaskEvent':ev,'lastInput':info['last_token_usage']['input_tokens'],'window':info['model_context_window'],'remaining':info['model_context_window']-info['last_token_usage']['input_tokens']}
root=native(x['rootNativeAudit']);actors=[]
for k,a in x['actors'].items():
 if a.get('archived',False) or a['stage'].startswith(('ARCHIVED','RETIRED')):continue
 actors.append({'key':k,'stage':a['stage'],'task':a.get('task'),'cursor':a.get('cursor'),'model':a['model'],'thinking':a['thinking'],'native':native(a)})
fields=['id','status','qualityCredit','applied','beforeHash','afterHash','appliedCurrentHash','appliedCommit','initialAppliedCurrentHash','unappliedProposalHash','rawFreeze','qualifiedFreeze','catalogCommit','qa','certification','certificationCodeCommit','actualWebCalls','sourceActualCompactions','sourceNetworkAccounting','cycle1RawFreeze','cycle1QualifiedFreeze','cycle1AfterHash','cycle1Status','cycle1CatalogCommit','cycle1QA','ordinaryCycle2Prohibited','noQA','noIndependentInitial','noQualificationApplyQAInitial','sourceProvenanceDeviation']
owned_orders=set(x['ownedSourceOrders'])
own={k.removeprefix('pendingCarsRoadTransport'):{f:v[f] for f in fields if f in v} for k,v in x.items() if re.fullmatch('pendingCarsRoadTransport[0-9]+',k) and int(k.removeprefix('pendingCarsRoadTransport')) in owned_orders}
push=[m.flow.get(cid)[1]['evidence'].get('remote_push') for cid in x['claims']]
assert all(v==push[0] for v in push)
point={'owner':m.O,'asOf':datetime.datetime.now(datetime.timezone.utc).isoformat(),'CURRENT':n,'remaining':2000-n,'fullGoal':2000,'goalComplete':False,'ownIntake':x['ownIntakeCURRENT'],'ownNewlyCertified':n-x['ownIntakeCURRENT'],'manifest':str(D/'manifest.json'),'canonicalCheckpoint':x['canonicalCheckpoint'],'codeBranch':x['codeBranch'],'codeHeadBeforeProjection':m.h.git(m.C,'rev-parse','HEAD'),'planningManagedBranch':x['planningBranch'],'planningManagedSHA':m.h.git(m.P,'rev-parse','refs/heads/'+x['planningBranch']),'planningCheckoutBranch':m.h.git(m.P,'branch','--show-current'),'claimSet':x['claims'],'activeRoute':x['activeRoute'],'rootNative':root,'liveActors':actors,'ownCards':own,'readyQueue':x.get('readyQueue',[]),'pendingBoundedWork':[v for v in actors if v['key'].startswith('author') and v['stage'].startswith('START')],'pendingReviews':[v for v in actors if v['key']=='reviewer' and v['stage'].startswith('START')],'qaReports':x['ownAffectedRuns'],'diagnostics':str(D/'own-procedural-diagnostics.json'),'remoteAuthority':{'lastRecordedAllClaims':push[0],'freshReadbackNotPerformedByThisProjection':True,'rule':'Only all-claims delivery.evidence.remote_push plus fresh origin readback is current remote authority; historical code snapshots are not.'},'foreignIndexes':x['foreignIndexes'],'leaseEmpty':True,'mainIntegrationPerformed':False,'inheritedContinuation':str(pathlib.Path(x['predecessorHandoff']).parent/'continuation-point.json'),'allInheritedFencesPreservedInManifest':['/fences','/newAttemptFences','/readScope'],'allHOLDQualityCredit':0,'scope':'Full exact2000 continues. No ordinarycycle2/newINITIAL/reset/oldHOLD adoption, alias replay or finished-card qualification/apply/QA replay. No mainmerge/fullsuite/runtime/browser/Player/build/deploy/release/OpenSpecarchive; max2authors/max1reader/READYqueue2. First actual compaction finishes current started result only, never nextcard; second preservation/handoffSTOP.','next':x['next']}
for root_path,key in [(m.C,'code'),(m.P,'planning')]:assert m.raw(pathlib.Path(m.h.git(root_path,'rev-parse','--path-format=absolute','--git-path','index')))==x['foreignIndexes'][key]
m.write(D/'continuation-point.json',point)
print(m.savecode([D/'continuation-point.json',pathlib.Path(__file__)],'Refresh compact canonical continuation without quality or QA replay'))
print({'CURRENT':n,'remaining':2000-n,'ownNewlyCertified':point['ownNewlyCertified'],'rootActualCompactions':root['actualCompactions'],'liveActors':len(actors),'pendingSource':len(point['pendingBoundedWork']),'pendingReader':len(point['pendingReviews'])})
