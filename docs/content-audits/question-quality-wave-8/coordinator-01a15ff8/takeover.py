"""ACTIVATE: supported exact3 takeover at CURRENT956; preservation and identity only."""
import pathlib,json,hashlib,importlib.util,ast,datetime
D=pathlib.Path(__file__).parent;C=D.parents[3];P=pathlib.Path('/Users/eaafonasev/Projects/mindbattle/planning');O='01a15ff8-512c-7111-9672-67fe234a3746';OLD='01a15fba-af2a-7e12-a7cc-fa59edc595b7';S=D.with_name('coordinator-01a15fba')
def read(p):return json.loads(p.read_text())
def write(p,v):
 if P in p.parents:
  assert raw(idx[P])==expected[P]
  assert read(P/'.flow-leases.json').get('planning',{}).get('owner')==O
 p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def raw(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def mod(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
native=pathlib.Path('/Users/eaafonasev/.codex/sessions/2026/10/22/rollout-2026-10-22T00-37-51-'+O+'.jsonl');records=[json.loads(l) for l in native.open()];assert next(r['payload']['id'] for r in records if r['type']=='session_meta')==O;assert sum(r['type']=='compacted' for r in records)==0
h=read(S/'handoff-next.json');assert h['successorThreadId']==O and h['phase']=='EXACT3_RELEASED_PENDING_SUCCESSOR_CLAIM'
flow=mod('flow',C/'tools/flow.py').Flow(P);sv=mod('private',P/'evidence/question-revision-process-v2/private-save-helper-01a13cb1.py')
expected={C:h['foreignIndexes']['code'],P:h['foreignIndexes']['planning']};idx={r:pathlib.Path(sv.git(r,'rev-parse','--path-format=absolute','--git-path','index')) for r in [C,P]}
for r in idx:assert raw(idx[r])==expected[r]
assert all(flow.get(cid)[1]['owner'] is None for cid in h['claims']) and read(P/'.flow-leases.json')=={}
cp_path=pathlib.Path(h['canonicalCheckpoint']);cp=read(cp_path);assert cp['owner'] is None and len(cp['currentEligibleCompletedIds'])==956 and len(cp['currentRemainingIds'])==1044
remote=flow.get(h['claims'][0])[1]['evidence']['remote_push'];assert remote['commit']=='5508df6f6873d38d08539b2cee1ae488d223cc0d';assert sv.git(C,'ls-remote','origin','refs/heads/codex/question-quality-wave-6').split()[0]==remote['commit']
clones=[]
for name in dict.fromkeys([*h['helpers'],'preserve-packet.py']):
 s=(S/name).read_text().replace("O='"+OLD+"'", "O='"+O+"'").replace('-01a15fba.json','-01a15ff8.json').replace("'ownIntakeCURRENT':952", "'ownIntakeCURRENT':956").replace('n-952','n-956')
 if name.endswith('.py'):ast.parse(s)
 (D/name).write_text(s);clones.append(D/name)
assert 'coordinator-01a15a0f/reader-polar46-initial-task.json' in (D/'prepare-initial.py').read_text()
assert 'packet_name = sys.argv[5]' in (D/'prepare-initial.py').read_text()
assert "D/('reader-history-russia'+str(order)+'-initial-task.json')" in (D/'prepare-final.py').read_text()
x=read(S/'manifest.json');priorRuns=x.get('inheritedAffectedRuns',[])+[v['path'] if isinstance(v,dict) else v for v in x.get('ownAffectedRuns',[])]
x.update(owner=O,claimsOwner=O,phase='ACTIVE_TAKEOVER_CURRENT956',manifest=str(D/'manifest.json'),intakeCURRENT=956,ownIntakeCURRENT=956,newlyCertified=0,actualCompactions=0,rootActualCompactions=0,predecessorHandoff=str(S/'handoff-next.json'),inheritedManifest=str(S/'manifest.json'),helpers={n:str(D/n) for n in h['helpers']},ownProgress={'intake':956,'newlyCertified':0,'accepted':[],'certificates':[]},ownAffectedRuns=[],inheritedAffectedRuns=priorRuns,currentWork={'stage':'TAKEOVER_CURRENT956_BEFORE_HISTORY_RUSSIA49','CURRENT':956,'remaining':1044},next='Prepare one untouched SOURCE49 retained-sources first; preserve all inherited HOLD and certified45-48 fences; retained live idle reviewer before INITIAL49 after fresh native/context whole-card plus possible-fix budget preflight',rootContextReason='Fresh successor actual0; predecessor preventive bounded handoff actual0; preserve all fences',successorThreadId=None,successorNativeJournal=None,successorCreationProof=None,successorACK=None,sourceActorKeys=[],createdNativeThreadsCurrentOwner=[],oldRootStoppedControl=True,at=datetime.datetime.now(datetime.timezone.utc).isoformat())
x['actors']={'reviewer':dict(h['retainedIdleReviewer'])};x['retainedIdleReviewer']=h['retainedIdleReviewer'];x['noRetainedIdleReviewer']=False;x.update(successorStatus='ACTIVE',currentSourceActors=[],currentIndependentActors=[],currentSourceActorsCount=0,noRetainedIdleAuthor=True,leaseHeld=False)
x['readScope']={**h['readScope'],'ownD':str(D)};x['helperInstanceVerification']='Identity fba->ff8; own intake952->956; AST parsed; zero active authors/review tasks; live idle reviewer retained. Historical46/83 templates and retained SOURCE19/20/21/22/23-27 accounting paths unchanged; sourceIndex/additional indexes remain actual old roots.';x['rootNativeAudit']={'threadId':O,'nativeJournal':str(native),'actualCompactions':0}; x['retainedIdleReviewer']['stage']='IDLE_AFTER_FINAL47_SOLE_CYCLE1_PASS_AVAILABLE_FOR_INITIAL49_AFTER_PREFLIGHT'; x['actors']['reviewer']['stage']=x['retainedIdleReviewer']['stage']
assert x['actors']['reviewer']['threadId']=='01a15f88-378e-72f1-a9a5-16c2bfa437c7' and not x['actors']['reviewer'].get('archived',False)
assert x['sourceIndex']==h['sourceIndex'] and x['additionalRetainedSourceIndexes']==h['additionalRetainedSourceIndexes'] and len(x['coordinatorSlicesToPreserve'])==34
write(D/'manifest.json',x)
report={'owner':O,'predecessor':OLD,'phase':'SUPPORTED_EXACT3_DURABLE_TAKEOVER','CURRENT':956,'remaining':1044,'fullGoal':2000,'intakeCURRENT':956,'newlyCertified':0,'predecessorRemotePush':remote,'readScope':x['readScope'],'foreignIndexes':h['foreignIndexes'],'handoffSHA256':raw(S/'handoff-next.json'),'manifestSHA256':raw(S/'manifest.json'),'canonicalCheckpointBeforeSHA256':raw(cp_path),'claims':h['claims'],'coordinatorSlicesToPreserve':h['coordinatorSlicesToPreserve'],'helperClones':{f.name:raw(f) for f in clones},'noSemanticRereviewOrTest':True,'actualCompactions':0,'at':x['at']};write(D/'takeover.json',report)
cc=sv.save(C,'refs/heads/codex/question-quality-wave-6',[str(p.relative_to(C)) for p in clones+[D/'manifest.json',D/'takeover.json',pathlib.Path(__file__)]],'Preserve CURRENT956 successor identity and bounded helpers',expected[C]);print('code',cc)
freshPIndex=raw(idx[P]);assert freshPIndex==expected[P]
with flow.locked():
 assert raw(idx[P])==freshPIndex
 assert all(flow.get(cid)[1]['owner'] is None for cid in h['claims']);flow.lease('acquire','planning',O)
try:
 assert raw(idx[P])==freshPIndex
 with flow.locked():
  for cid in h['claims']:flow.claim(cid,O)
 cp.update(owner=O,activeCoordinator=O,phase=x['phase'],currentManifest=str(D/'manifest.json'),pendingSuccessor=None,successorThreadId=None,successorStatus='ACTIVE',ordinaryWorkActivated=True,currentSourceActors=[],currentIndependentActors=[],currentSourceActiveCount=0,nativeActorsCurrent=cp['nativeActorsCurrent'],next=x['next'],coordinatorActualCompactions=0)
 cp['ownershipTransfer']={'predecessor':OLD,'successor':O,'status':'SUPPORTED_EXACT3_DURABLE_TAKEOVER','CURRENT':956,'remaining':1044,'fullGoal':2000,'claims':h['claims'],'handoff':str(S/'handoff-next.json'),'rootActualCompactions':0};write(cp_path,cp)
 sp=P/'evidence/question-revision-process-v2/coordinator-state.json';st=read(sp);st.update(threadId=O,owner=O,activeCoordinator=O,claims=h['claims'],phase=x['phase'],status='ACTIVE_FULL2000',currentManifest=str(D/'manifest.json'),pendingSuccessor=None,successor=None,successorThreadId=None,successorStatus='ACTIVE',ownActualCompactions=0,rootActualCompactions=0,actualRootCompactions=0,coordinatorActualCompactions=0,ordinaryWorkActivated=True,counts={'CURRENT':956,'remaining':1044},ownedIntake={'CURRENT':956,'newlyCertified':0,'remaining':1044,'fullGoal':2000},coordinatorProgress={'intakeCURRENT':956,'CURRENT':956,'newlyCertified':0,'remaining':1044},currentWork=x['currentWork'],codeCommit=cc,next=x['next'],activeAuthors=[],idleAuthors=[],activeIndependentReview=None,currentSourceActors=[],currentIndependentActors=[],nativeActorsCurrent=cp['nativeActorsCurrent'],currentNativeActors={a['threadId']:a for a in cp['nativeActorsCurrent']},coordinatorSlicesToPreserve=h['coordinatorSlicesToPreserve'],activeGoal='Full SOURCE/editorial exact2000 waves6-9; own intake956; preserve all prior HOLDs',asOf=x['at']);write(sp,st)
 gp=P/'evidence/question-revision-process-v2/active-full2000-goal-01a1593a.json';g=read(gp);g.update(owner=O,activeCoordinator=O,successorThreadId=None,intakeCURRENT=956,newlyCertified=0,CURRENT=956,remaining=1044,manifest=str(D/'manifest.json'),latestCodeCommit=cc,pendingSuccessor=None,successor=None,successorStatus='ACTIVE',coordinatorSlicesToPreserve=h['coordinatorSlicesToPreserve']);write(gp,g)
 pp=P/'evidence/question-revision-process-v2/takeover-01a15ff8.json';write(pp,{**report,'codeCommit':cc})
 pc=sv.save(P,'refs/heads/codex/question-revision-resume-20261014',[str(p.relative_to(P)) for p in [cp_path,sp,gp,pp]+[flow.get(cid)[0] for cid in h['claims']]],'Record supported exact3 CURRENT956 takeover',expected[P]);print('planning',pc)
finally:
 with flow.locked():flow.lease('release','planning',O)
assert all(flow.get(cid)[1]['owner']==O for cid in h['claims']) and read(P/'.flow-leases.json')=={}
for r in idx:assert raw(idx[r])==expected[r]
print('exact3 owned; lease empty; both foreign indexes preserved')
