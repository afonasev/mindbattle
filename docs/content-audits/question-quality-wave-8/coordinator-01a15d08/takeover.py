"""Authorized exact3 takeover CURRENT931; no quality credit or source mutation."""
import pathlib,json,hashlib,importlib.util,ast,datetime,subprocess
D=pathlib.Path(__file__).parent;C=D.parents[3];P=pathlib.Path('/Users/eaafonasev/Projects/mindbattle/planning')
O='01a15d08-0990-7462-9e13-0006dbd6aad8';OLD='01a15cdf-657f-7b93-bbce-9cb12b398c70';S=D.with_name('coordinator-01a15cdf')
def read(p):return json.loads(p.read_text())
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def raw(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def mod(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
native=pathlib.Path('/Users/eaafonasev/.codex/sessions/2026/10/21/rollout-2026-10-21T10-56-10-'+O+'.jsonl');records=[json.loads(l) for l in native.open()];assert next(r['payload']['id'] for r in records if r['type']=='session_meta')==O;assert sum(r['type']=='compacted' for r in records)==0
h=read(S/'handoff-next.json');assert h['successorThreadId']==O and h['phase']=='EXACT3_RELEASED_PENDING_SUCCESSOR_CLAIM'
flow=mod('flow',C/'tools/flow.py').Flow(P);sv=mod('private',P/'evidence/question-revision-process-v2/private-save-helper-01a13cb1.py')
idx={p:pathlib.Path(sv.git(p,'rev-parse','--path-format=absolute','--git-path','index')) for p in [C,P]};expected={C:h['foreignIndexes']['code'],P:h['foreignIndexes']['planning']}
for p in idx:assert raw(idx[p])==expected[p]
assert all(flow.get(cid)[1]['owner'] is None for cid in h['claims']);assert read(P/'.flow-leases.json')=={}
cp_path=pathlib.Path(h['canonicalCheckpoint']);cp=read(cp_path);assert cp['owner'] is None and len(cp['currentEligibleCompletedIds'])==931 and len(cp['currentRemainingIds'])==1069
remote=flow.get(h['claims'][0])[1]['evidence']['remote_push'];assert remote['commit']=='3af4773dbcc341d0d1db6a25e9d1a543c0622a7f'
assert sv.git(C,'ls-remote','origin','refs/heads/codex/question-quality-wave-6').split()[0]==remote['commit']
clones=[]
for name in list(dict.fromkeys(list(h['helpers'])+['preserve-packet.py'])):
 original=(S/name).read_text();s=original.replace(OLD,O).replace('coordinator-01a15cdf','coordinator-01a15d08').replace('-01a15cdf.json','-01a15d08.json')
 s=s.replace("'ownIntakeCURRENT':929","'ownIntakeCURRENT':931").replace('"ownIntakeCURRENT":929','"ownIntakeCURRENT":931').replace('n-929','n-931')
 if name.endswith('.py'):ast.parse(s)
 (D/name).write_text(s);clones.append(D/name)
assert "coordinator-01a15a0f/reader-polar46-initial-task.json" in (D/'prepare-initial.py').read_text()
assert "packet_name = sys.argv[5]" in (D/'prepare-initial.py').read_text()
assert "D/('reader-history-russia'+str(order)+'-initial-task.json')" in (D/'prepare-final.py').read_text()
x=read(S/'manifest.json');priorRuns=x.get('inheritedAffectedRuns',[])+[v['path'] if isinstance(v,dict) else v for v in x.get('ownAffectedRuns',[])]
x.update(owner=O,claimsOwner=O,phase='ACTIVE_TAKEOVER_CURRENT931',manifest=str(D/'manifest.json'),intakeCURRENT=931,ownIntakeCURRENT=931,newlyCertified=0,actualCompactions=0,rootActualCompactions=0,predecessorHandoff=str(S/'handoff-next.json'),inheritedManifest=str(S/'manifest.json'),helpers={n:str(D/n) for n in h['helpers']},ownProgress={'intake':931,'newlyCertified':0,'accepted':[],'certificates':[]},ownAffectedRuns=[],inheritedAffectedRuns=priorRuns,currentWork={'stage':'TAKEOVER_CURRENT931_BEFORE_HISTORY_RUSSIA7','CURRENT':931,'remaining':1069},next='Narrow prior source7 attempts before fresh author bootstrap/START; preflight reviewer budget',rootContextReason='Fresh successor actual0; predecessor preventive bounded handoff actual0; all fences preserved',successorThreadId=None,sourceActorKeys=[],createdNativeThreadsCurrentOwner=[],oldRootStoppedControl=True,at=datetime.datetime.now(datetime.timezone.utc).isoformat())
x['actors']={'reviewer':x['retainedIdleReviewer']};x.update(successorStatus='ACTIVE',currentSourceActors=[],currentIndependentActors=[],currentSourceActorsCount=0,noRetainedIdleAuthor=True)
x['readScope']={**h['readScope'],'ownD':str(D)};x['helperInstanceVerification']='Identity-only cdf->d08; own intake929->931; AST parsed; historical46/83 paths preserved. Dynamic sourceIndex/additional indexes preserved under actual old roots.'
x['rootNativeAudit']={'threadId':O,'nativeJournal':str(native),'actualCompactions':0}
assert x['sourceIndex']==h['sourceIndex'] and x['additionalRetainedSourceIndexes']==h['additionalRetainedSourceIndexes'] and len(x['coordinatorSlicesToPreserve'])==20
write(D/'manifest.json',x)
report={'owner':O,'predecessor':OLD,'phase':'SUPPORTED_EXACT3_DURABLE_TAKEOVER','CURRENT':931,'remaining':1069,'fullGoal':2000,'intakeCURRENT':931,'newlyCertified':0,'predecessorRemotePush':remote,'readScope':x['readScope'],'foreignIndexes':h['foreignIndexes'],'handoffSHA256':raw(S/'handoff-next.json'),'manifestSHA256':raw(S/'manifest.json'),'canonicalCheckpointBeforeSHA256':raw(cp_path),'claims':h['claims'],'coordinatorSlicesToPreserve':h['coordinatorSlicesToPreserve'],'helperClones':{f.name:raw(f) for f in clones},'noSemanticRereviewOrTest':True,'actualCompactions':0,'at':x['at']}
write(D/'takeover.json',report)
files=clones+[D/'manifest.json',D/'takeover.json',pathlib.Path(__file__)]
cc=sv.save(C,'refs/heads/codex/question-quality-wave-6',[str(p.relative_to(C)) for p in files],'Preserve CURRENT931 successor and identity-bound helpers',expected[C]);print('code',cc)
with flow.locked():
 assert all(flow.get(cid)[1]['owner'] is None for cid in h['claims']);flow.lease('acquire','planning',O)
try:
 with flow.locked():
  for cid in h['claims']:flow.claim(cid,O)
 cp.update(owner=O,activeCoordinator=O,phase=x['phase'],currentManifest=str(D/'manifest.json'),pendingSuccessor=None,successorStatus='ACTIVE',ordinaryWorkActivated=True,currentSourceActors=[],currentIndependentActors=[],currentSourceActiveCount=0,nativeActorsCurrent=[x['actors']['reviewer']],next=x['next'],coordinatorActualCompactions=0)
 cp['ownershipTransfer']={'predecessor':OLD,'successor':O,'status':'SUPPORTED_EXACT3_DURABLE_TAKEOVER','CURRENT':931,'remaining':1069,'fullGoal':2000,'claims':h['claims'],'handoff':str(S/'handoff-next.json'),'rootActualCompactions':0};write(cp_path,cp)
 sp=P/'evidence/question-revision-process-v2/coordinator-state.json';st=read(sp);st.update(threadId=O,owner=O,activeCoordinator=O,claims=h['claims'],phase=x['phase'],status='ACTIVE_FULL2000',currentManifest=str(D/'manifest.json'),pendingSuccessor=None,successor=None,successorThreadId=None,successorStatus='ACTIVE',ownActualCompactions=0,rootActualCompactions=0,actualRootCompactions=0,coordinatorActualCompactions=0,ordinaryWorkActivated=True,counts={'CURRENT':931,'remaining':1069},ownedIntake={'CURRENT':931,'newlyCertified':0,'remaining':1069,'fullGoal':2000},coordinatorProgress={'intakeCURRENT':931,'CURRENT':931,'newlyCertified':0,'remaining':1069},currentWork=x['currentWork'],codeCommit=cc,next=x['next'],activeAuthors=[],idleAuthors=[],activeIndependentReview=None,currentSourceActors=[],currentIndependentActors=[],nativeActorsCurrent=[x['actors']['reviewer']],currentNativeActors={a['threadId']:a for a in [x['actors']['reviewer']]},coordinatorSlicesToPreserve=h['coordinatorSlicesToPreserve'],activeGoal='Full SOURCE/editorial exact2000 waves6-9; own intake931; preserve all prior HOLDs',asOf=x['at']);write(sp,st)
 gp=P/'evidence/question-revision-process-v2/active-full2000-goal-01a1593a.json';g=read(gp);g.update(owner=O,intakeCURRENT=931,newlyCertified=0,CURRENT=931,remaining=1069,manifest=str(D/'manifest.json'),latestCodeCommit=cc,pendingSuccessor=None,successor=None,successorStatus='ACTIVE',coordinatorSlicesToPreserve=h['coordinatorSlicesToPreserve']);write(gp,g)
 pp=P/'evidence/question-revision-process-v2/takeover-01a15d08.json';write(pp,{**report,'codeCommit':cc})
 pfiles=[cp_path,sp,gp,pp]+[flow.get(cid)[0] for cid in h['claims']]
 pc=sv.save(P,'refs/heads/codex/question-revision-resume-20261014',[str(p.relative_to(P)) for p in pfiles],'Record supported exact3 CURRENT931 successor takeover',expected[P]);print('planning',pc)
finally:
 with flow.locked():flow.lease('release','planning',O)
assert all(flow.get(cid)[1]['owner']==O for cid in h['claims']) and read(P/'.flow-leases.json')=={}
for p in idx:assert raw(idx[p])==expected[p]
print('exact3 owned; lease empty; foreign indexes unchanged')
