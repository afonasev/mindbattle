"""ACTIVATE: supported exact3 takeover at CURRENT938; preservation and identity only."""
import pathlib,json,hashlib,importlib.util,ast,datetime
D=pathlib.Path(__file__).parent;C=D.parents[3];P=pathlib.Path('/Users/eaafonasev/Projects/mindbattle/planning');O='01a15df2-2a17-71c1-aecd-3cc11add3160';OLD='01a15db1-757e-7dd1-a924-d215c9a8608d';S=D.with_name('coordinator-01a15db1')
def read(p):return json.loads(p.read_text())
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def raw(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def mod(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
native=pathlib.Path('/Users/eaafonasev/.codex/sessions/2026/10/21/rollout-2026-10-21T15-11-54-'+O+'.jsonl');records=[json.loads(l) for l in native.open()];assert next(r['payload']['id'] for r in records if r['type']=='session_meta')==O;assert sum(r['type']=='compacted' for r in records)==0
h=read(S/'handoff-next.json');assert h['successorThreadId']==O and h['phase']=='EXACT3_RELEASED_PENDING_SUCCESSOR_CLAIM'
flow=mod('flow',C/'tools/flow.py').Flow(P);sv=mod('private',P/'evidence/question-revision-process-v2/private-save-helper-01a13cb1.py')
expected={C:h['foreignIndexes']['code'],P:h['foreignIndexes']['planning']};idx={r:pathlib.Path(sv.git(r,'rev-parse','--path-format=absolute','--git-path','index')) for r in [C,P]}
for r in idx:assert raw(idx[r])==expected[r]
assert all(flow.get(cid)[1]['owner'] is None for cid in h['claims']) and read(P/'.flow-leases.json')=={}
cp_path=pathlib.Path(h['canonicalCheckpoint']);cp=read(cp_path);assert cp['owner'] is None and len(cp['currentEligibleCompletedIds'])==938 and len(cp['currentRemainingIds'])==1062
remote=flow.get(h['claims'][0])[1]['evidence']['remote_push'];assert remote['commit']=='400b5c8e39eb5951ee554f0a1307ac769cd84ebf';assert sv.git(C,'ls-remote','origin','refs/heads/codex/question-quality-wave-6').split()[0]==remote['commit']
clones=[]
for name in dict.fromkeys([*h['helpers'],'preserve-packet.py']):
 s=(S/name).read_text().replace(OLD,O).replace('-01a15db1.json','-01a15df2.json').replace("'ownIntakeCURRENT':937","'ownIntakeCURRENT':938").replace('"ownIntakeCURRENT":937','"ownIntakeCURRENT":938').replace('n-937','n-938')
 if name.endswith('.py'):ast.parse(s)
 (D/name).write_text(s);clones.append(D/name)
assert 'coordinator-01a15a0f/reader-polar46-initial-task.json' in (D/'prepare-initial.py').read_text()
assert 'packet_name = sys.argv[5]' in (D/'prepare-initial.py').read_text()
assert "D/('reader-history-russia'+str(order)+'-initial-task.json')" in (D/'prepare-final.py').read_text()
x=read(S/'manifest.json');priorRuns=x.get('inheritedAffectedRuns',[])+[v['path'] if isinstance(v,dict) else v for v in x.get('ownAffectedRuns',[])]
x.update(owner=O,claimsOwner=O,phase='ACTIVE_TAKEOVER_CURRENT938',manifest=str(D/'manifest.json'),intakeCURRENT=938,ownIntakeCURRENT=938,newlyCertified=0,actualCompactions=0,rootActualCompactions=0,predecessorHandoff=str(S/'handoff-next.json'),inheritedManifest=str(S/'manifest.json'),helpers={n:str(D/n) for n in h['helpers']},ownProgress={'intake':938,'newlyCertified':0,'accepted':[],'certificates':[]},ownAffectedRuns=[],inheritedAffectedRuns=priorRuns,currentWork={'stage':'TAKEOVER_CURRENT938_BEFORE_HISTORY_RUSSIA19','CURRENT':938,'remaining':1062},next='Apply inherited qualified SOURCE19 to exact preimage; affected QA19 then retained reviewer INITIAL19 after fresh native preflight',rootContextReason='Fresh successor actual0; predecessor preventive bounded handoff actual0; preserve all fences',successorThreadId=None,sourceActorKeys=[],createdNativeThreadsCurrentOwner=[],oldRootStoppedControl=True,at=datetime.datetime.now(datetime.timezone.utc).isoformat())
x['actors']={'reviewer':h['actors']['reviewer']};x['retainedIdleReviewer']=h['retainedIdleReviewer'];x['noRetainedIdleReviewer']=False;x.update(successorStatus='ACTIVE',currentSourceActors=[],currentIndependentActors=[],currentSourceActorsCount=0,noRetainedIdleAuthor=True,leaseHeld=False)
x['readScope']={**h['readScope'],'ownD':str(D)};x['helperInstanceVerification']='Identity db1->df2; own intake937->938; AST parsed; zero active authors/review tasks; live idle reviewer retained. Historical46/83 templates and retained SOURCE10 accounting paths unchanged; sourceIndex/additional indexes remain actual old roots.';x['rootNativeAudit']={'threadId':O,'nativeJournal':str(native),'actualCompactions':0}
assert x['actors']['reviewer']['threadId']=='01a15db8-e016-7662-988d-1fd4eedccf31' and not x['actors']['reviewer'].get('archived',False)
assert x['sourceIndex']==h['sourceIndex'] and x['additionalRetainedSourceIndexes']==h['additionalRetainedSourceIndexes'] and len(x['coordinatorSlicesToPreserve'])==25
write(D/'manifest.json',x)
report={'owner':O,'predecessor':OLD,'phase':'SUPPORTED_EXACT3_DURABLE_TAKEOVER','CURRENT':938,'remaining':1062,'fullGoal':2000,'intakeCURRENT':938,'newlyCertified':0,'predecessorRemotePush':remote,'readScope':x['readScope'],'foreignIndexes':h['foreignIndexes'],'handoffSHA256':raw(S/'handoff-next.json'),'manifestSHA256':raw(S/'manifest.json'),'canonicalCheckpointBeforeSHA256':raw(cp_path),'claims':h['claims'],'coordinatorSlicesToPreserve':h['coordinatorSlicesToPreserve'],'helperClones':{f.name:raw(f) for f in clones},'noSemanticRereviewOrTest':True,'actualCompactions':0,'at':x['at']};write(D/'takeover.json',report)
cc=sv.save(C,'refs/heads/codex/question-quality-wave-6',[str(p.relative_to(C)) for p in clones+[D/'manifest.json',D/'takeover.json',pathlib.Path(__file__)]],'Preserve CURRENT938 successor identity and bounded helpers',expected[C]);print('code',cc)
with flow.locked():
 assert all(flow.get(cid)[1]['owner'] is None for cid in h['claims']);flow.lease('acquire','planning',O)
try:
 with flow.locked():
  for cid in h['claims']:flow.claim(cid,O)
 cp.update(owner=O,activeCoordinator=O,phase=x['phase'],currentManifest=str(D/'manifest.json'),pendingSuccessor=None,successorThreadId=None,successorStatus='ACTIVE',ordinaryWorkActivated=True,currentSourceActors=[],currentIndependentActors=[],currentSourceActiveCount=0,nativeActorsCurrent=cp['nativeActorsCurrent'],next=x['next'],coordinatorActualCompactions=0)
 cp['ownershipTransfer']={'predecessor':OLD,'successor':O,'status':'SUPPORTED_EXACT3_DURABLE_TAKEOVER','CURRENT':938,'remaining':1062,'fullGoal':2000,'claims':h['claims'],'handoff':str(S/'handoff-next.json'),'rootActualCompactions':0};write(cp_path,cp)
 sp=P/'evidence/question-revision-process-v2/coordinator-state.json';st=read(sp);st.update(threadId=O,owner=O,activeCoordinator=O,claims=h['claims'],phase=x['phase'],status='ACTIVE_FULL2000',currentManifest=str(D/'manifest.json'),pendingSuccessor=None,successor=None,successorThreadId=None,successorStatus='ACTIVE',ownActualCompactions=0,rootActualCompactions=0,actualRootCompactions=0,coordinatorActualCompactions=0,ordinaryWorkActivated=True,counts={'CURRENT':938,'remaining':1062},ownedIntake={'CURRENT':938,'newlyCertified':0,'remaining':1062,'fullGoal':2000},coordinatorProgress={'intakeCURRENT':938,'CURRENT':938,'newlyCertified':0,'remaining':1062},currentWork=x['currentWork'],codeCommit=cc,next=x['next'],activeAuthors=[],idleAuthors=[],activeIndependentReview=None,currentSourceActors=[],currentIndependentActors=[],nativeActorsCurrent=cp['nativeActorsCurrent'],currentNativeActors=st.get('currentNativeActors',{}),coordinatorSlicesToPreserve=h['coordinatorSlicesToPreserve'],activeGoal='Full SOURCE/editorial exact2000 waves6-9; own intake938; preserve all prior HOLDs',asOf=x['at']);write(sp,st)
 gp=P/'evidence/question-revision-process-v2/active-full2000-goal-01a1593a.json';g=read(gp);g.update(owner=O,intakeCURRENT=938,newlyCertified=0,CURRENT=938,remaining=1062,manifest=str(D/'manifest.json'),latestCodeCommit=cc,pendingSuccessor=None,successor=None,successorStatus='ACTIVE',coordinatorSlicesToPreserve=h['coordinatorSlicesToPreserve']);write(gp,g)
 pp=P/'evidence/question-revision-process-v2/takeover-01a15df2.json';write(pp,{**report,'codeCommit':cc})
 pc=sv.save(P,'refs/heads/codex/question-revision-resume-20261014',[str(p.relative_to(P)) for p in [cp_path,sp,gp,pp]+[flow.get(cid)[0] for cid in h['claims']]],'Record supported exact3 CURRENT938 takeover',expected[P]);print('planning',pc)
finally:
 with flow.locked():flow.lease('release','planning',O)
assert all(flow.get(cid)[1]['owner']==O for cid in h['claims']) and read(P/'.flow-leases.json')=={}
for r in idx:assert raw(idx[r])==expected[r]
print('exact3 owned; lease empty; both foreign indexes preserved')
