"""ACTIVATE: supported exact3 takeover at CURRENT937; preservation and identity only."""
import pathlib,json,hashlib,importlib.util,ast,datetime
D=pathlib.Path(__file__).parent;C=D.parents[3];P=pathlib.Path('/Users/eaafonasev/Projects/mindbattle/planning');O='01a15db1-757e-7dd1-a924-d215c9a8608d';OLD='01a15d80-0fba-7452-81f6-ce117a86dd4a';S=D.with_name('coordinator-01a15d80')
def read(p):return json.loads(p.read_text())
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def raw(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def mod(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
native=pathlib.Path('/Users/eaafonasev/.codex/sessions/2026/10/21/rollout-2026-10-21T14-01-13-'+O+'.jsonl');records=[json.loads(l) for l in native.open()];assert next(r['payload']['id'] for r in records if r['type']=='session_meta')==O;assert sum(r['type']=='compacted' for r in records)==0
h=read(S/'handoff-next.json');assert h['successorThreadId']==O and h['phase']=='EXACT3_RELEASED_PENDING_SUCCESSOR_CLAIM'
flow=mod('flow',C/'tools/flow.py').Flow(P);sv=mod('private',P/'evidence/question-revision-process-v2/private-save-helper-01a13cb1.py')
expected={C:h['foreignIndexes']['code'],P:h['foreignIndexes']['planning']};idx={r:pathlib.Path(sv.git(r,'rev-parse','--path-format=absolute','--git-path','index')) for r in [C,P]}
for r in idx:assert raw(idx[r])==expected[r]
assert all(flow.get(cid)[1]['owner'] is None for cid in h['claims']) and read(P/'.flow-leases.json')=={}
cp_path=pathlib.Path(h['canonicalCheckpoint']);cp=read(cp_path);assert cp['owner'] is None and len(cp['currentEligibleCompletedIds'])==937 and len(cp['currentRemainingIds'])==1063
remote=flow.get(h['claims'][0])[1]['evidence']['remote_push'];assert remote['commit']=='8c971cc46f5f15dcb9a0f21e3eca445f75f77698';assert sv.git(C,'ls-remote','origin','refs/heads/codex/question-quality-wave-6').split()[0]==remote['commit']
clones=[]
for name in dict.fromkeys([*h['helpers'],'preserve-packet.py']):
 s=(S/name).read_text().replace(OLD,O).replace('-01a15d80.json','-01a15db1.json').replace("'ownIntakeCURRENT':935","'ownIntakeCURRENT':937").replace('"ownIntakeCURRENT":935','"ownIntakeCURRENT":937').replace('n-935','n-937')
 if name.endswith('.py'):ast.parse(s)
 (D/name).write_text(s);clones.append(D/name)
assert 'coordinator-01a15a0f/reader-polar46-initial-task.json' in (D/'prepare-initial.py').read_text()
assert 'packet_name = sys.argv[5]' in (D/'prepare-initial.py').read_text()
assert "D/('reader-history-russia'+str(order)+'-initial-task.json')" in (D/'prepare-final.py').read_text()
x=read(S/'manifest.json');priorRuns=x.get('inheritedAffectedRuns',[])+[v['path'] if isinstance(v,dict) else v for v in x.get('ownAffectedRuns',[])]
x.update(owner=O,claimsOwner=O,phase='ACTIVE_TAKEOVER_CURRENT937',manifest=str(D/'manifest.json'),intakeCURRENT=937,ownIntakeCURRENT=937,newlyCertified=0,actualCompactions=0,rootActualCompactions=0,predecessorHandoff=str(S/'handoff-next.json'),inheritedManifest=str(S/'manifest.json'),helpers={n:str(D/n) for n in h['helpers']},ownProgress={'intake':937,'newlyCertified':0,'accepted':[],'certificates':[]},ownAffectedRuns=[],inheritedAffectedRuns=priorRuns,currentWork={'stage':'TAKEOVER_CURRENT937_BEFORE_HISTORY_RUSSIA16','CURRENT':937,'remaining':1063},next='SOURCE16 retained sources first; fresh Luna author readonly bootstrap then specific START; reviewer native preflight before INITIAL',rootContextReason='Fresh successor actual0; predecessor preventive bounded handoff actual0; preserve all fences',successorThreadId=None,sourceActorKeys=[],createdNativeThreadsCurrentOwner=[],oldRootStoppedControl=True,at=datetime.datetime.now(datetime.timezone.utc).isoformat())
x['actors']={'reviewer':h['actors']['reviewer']};x['retainedIdleReviewer']=None;x['noRetainedIdleReviewer']=True;x.update(successorStatus='ACTIVE',currentSourceActors=[],currentIndependentActors=[],currentSourceActorsCount=0,noRetainedIdleAuthor=True,leaseHeld=False)
x['readScope']={**h['readScope'],'ownD':str(D)};x['helperInstanceVerification']='Identity d80->db1; own intake935->937; AST parsed; zero active/idle authors and reviewers. Historical46/83 templates and retained SOURCE10 accounting paths unchanged; sourceIndex/additional indexes remain actual old roots.';x['rootNativeAudit']={'threadId':O,'nativeJournal':str(native),'actualCompactions':0}
assert x['retainedIdleReviewer'] is None and x['actors']['reviewer']['archived'] is True
assert x['sourceIndex']==h['sourceIndex'] and x['additionalRetainedSourceIndexes']==h['additionalRetainedSourceIndexes'] and len(x['coordinatorSlicesToPreserve'])==24
write(D/'manifest.json',x)
report={'owner':O,'predecessor':OLD,'phase':'SUPPORTED_EXACT3_DURABLE_TAKEOVER','CURRENT':937,'remaining':1063,'fullGoal':2000,'intakeCURRENT':937,'newlyCertified':0,'predecessorRemotePush':remote,'readScope':x['readScope'],'foreignIndexes':h['foreignIndexes'],'handoffSHA256':raw(S/'handoff-next.json'),'manifestSHA256':raw(S/'manifest.json'),'canonicalCheckpointBeforeSHA256':raw(cp_path),'claims':h['claims'],'coordinatorSlicesToPreserve':h['coordinatorSlicesToPreserve'],'helperClones':{f.name:raw(f) for f in clones},'noSemanticRereviewOrTest':True,'actualCompactions':0,'at':x['at']};write(D/'takeover.json',report)
cc=sv.save(C,'refs/heads/codex/question-quality-wave-6',[str(p.relative_to(C)) for p in clones+[D/'manifest.json',D/'takeover.json',pathlib.Path(__file__)]],'Preserve CURRENT937 successor identity and bounded helpers',expected[C]);print('code',cc)
with flow.locked():
 assert all(flow.get(cid)[1]['owner'] is None for cid in h['claims']);flow.lease('acquire','planning',O)
try:
 with flow.locked():
  for cid in h['claims']:flow.claim(cid,O)
 cp.update(owner=O,activeCoordinator=O,phase=x['phase'],currentManifest=str(D/'manifest.json'),pendingSuccessor=None,successorThreadId=None,successorStatus='ACTIVE',ordinaryWorkActivated=True,currentSourceActors=[],currentIndependentActors=[],currentSourceActiveCount=0,nativeActorsCurrent=[],next=x['next'],coordinatorActualCompactions=0)
 cp['ownershipTransfer']={'predecessor':OLD,'successor':O,'status':'SUPPORTED_EXACT3_DURABLE_TAKEOVER','CURRENT':937,'remaining':1063,'fullGoal':2000,'claims':h['claims'],'handoff':str(S/'handoff-next.json'),'rootActualCompactions':0};write(cp_path,cp)
 sp=P/'evidence/question-revision-process-v2/coordinator-state.json';st=read(sp);st.update(threadId=O,owner=O,activeCoordinator=O,claims=h['claims'],phase=x['phase'],status='ACTIVE_FULL2000',currentManifest=str(D/'manifest.json'),pendingSuccessor=None,successor=None,successorThreadId=None,successorStatus='ACTIVE',ownActualCompactions=0,rootActualCompactions=0,actualRootCompactions=0,coordinatorActualCompactions=0,ordinaryWorkActivated=True,counts={'CURRENT':937,'remaining':1063},ownedIntake={'CURRENT':937,'newlyCertified':0,'remaining':1063,'fullGoal':2000},coordinatorProgress={'intakeCURRENT':937,'CURRENT':937,'newlyCertified':0,'remaining':1063},currentWork=x['currentWork'],codeCommit=cc,next=x['next'],activeAuthors=[],idleAuthors=[],activeIndependentReview=None,currentSourceActors=[],currentIndependentActors=[],nativeActorsCurrent=[],currentNativeActors={},coordinatorSlicesToPreserve=h['coordinatorSlicesToPreserve'],activeGoal='Full SOURCE/editorial exact2000 waves6-9; own intake937; preserve all prior HOLDs',asOf=x['at']);write(sp,st)
 gp=P/'evidence/question-revision-process-v2/active-full2000-goal-01a1593a.json';g=read(gp);g.update(owner=O,intakeCURRENT=937,newlyCertified=0,CURRENT=937,remaining=1063,manifest=str(D/'manifest.json'),latestCodeCommit=cc,pendingSuccessor=None,successor=None,successorStatus='ACTIVE',coordinatorSlicesToPreserve=h['coordinatorSlicesToPreserve']);write(gp,g)
 pp=P/'evidence/question-revision-process-v2/takeover-01a15db1.json';write(pp,{**report,'codeCommit':cc})
 pc=sv.save(P,'refs/heads/codex/question-revision-resume-20261014',[str(p.relative_to(P)) for p in [cp_path,sp,gp,pp]+[flow.get(cid)[0] for cid in h['claims']]],'Record supported exact3 CURRENT937 takeover',expected[P]);print('planning',pc)
finally:
 with flow.locked():flow.lease('release','planning',O)
assert all(flow.get(cid)[1]['owner']==O for cid in h['claims']) and read(P/'.flow-leases.json')=={}
for r in idx:assert raw(idx[r])==expected[r]
print('exact3 owned; lease empty; both foreign indexes preserved')
