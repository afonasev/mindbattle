"""ACTIVATE: supported exact3 takeover at CURRENT943; preservation and identity only."""
import pathlib,json,hashlib,importlib.util,ast,datetime
D=pathlib.Path(__file__).parent;C=D.parents[3];P=pathlib.Path('/Users/eaafonasev/Projects/mindbattle/planning');O='01a15e52-f8e3-7292-9930-bdc893b19882';OLD='01a15e25-ed2b-7cc0-a466-b43bc5cecb52';S=D.with_name('coordinator-01a15e25')
def read(p):return json.loads(p.read_text())
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def raw(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def mod(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
native=pathlib.Path('/Users/eaafonasev/.codex/sessions/2026/10/21/rollout-2026-10-21T16-57-38-'+O+'.jsonl');records=[json.loads(l) for l in native.open()];assert next(r['payload']['id'] for r in records if r['type']=='session_meta')==O;assert sum(r['type']=='compacted' for r in records)==0
h=read(S/'handoff-next.json');assert h['successorThreadId']==O and h['phase']=='EXACT3_RELEASED_PENDING_SUCCESSOR_CLAIM'
flow=mod('flow',C/'tools/flow.py').Flow(P);sv=mod('private',P/'evidence/question-revision-process-v2/private-save-helper-01a13cb1.py')
expected={C:h['foreignIndexes']['code'],P:h['foreignIndexes']['planning']};idx={r:pathlib.Path(sv.git(r,'rev-parse','--path-format=absolute','--git-path','index')) for r in [C,P]}
for r in idx:assert raw(idx[r])==expected[r]
assert all(flow.get(cid)[1]['owner'] is None for cid in h['claims']) and read(P/'.flow-leases.json')=={}
cp_path=pathlib.Path(h['canonicalCheckpoint']);cp=read(cp_path);assert cp['owner'] is None and len(cp['currentEligibleCompletedIds'])==943 and len(cp['currentRemainingIds'])==1057
remote=flow.get(h['claims'][0])[1]['evidence']['remote_push'];assert remote['commit']=='8f877a5b89bd21297615c48c9558cd2360bad9bd';assert sv.git(C,'ls-remote','origin','refs/heads/codex/question-quality-wave-6').split()[0]==remote['commit']
clones=[]
for name in dict.fromkeys([*h['helpers'],'preserve-packet.py']):
 s=(S/name).read_text().replace("O='"+OLD+"'", "O='"+O+"'").replace('-01a15e25.json','-01a15e52.json').replace("'ownIntakeCURRENT':941", "'ownIntakeCURRENT':943").replace('n-941','n-943')
 if name.endswith('.py'):ast.parse(s)
 (D/name).write_text(s);clones.append(D/name)
assert 'coordinator-01a15a0f/reader-polar46-initial-task.json' in (D/'prepare-initial.py').read_text()
assert 'packet_name = sys.argv[5]' in (D/'prepare-initial.py').read_text()
assert "D/('reader-history-russia'+str(order)+'-initial-task.json')" in (D/'prepare-final.py').read_text()
x=read(S/'manifest.json');priorRuns=x.get('inheritedAffectedRuns',[])+[v['path'] if isinstance(v,dict) else v for v in x.get('ownAffectedRuns',[])]
x.update(owner=O,claimsOwner=O,phase='ACTIVE_TAKEOVER_CURRENT943',manifest=str(D/'manifest.json'),intakeCURRENT=943,ownIntakeCURRENT=943,newlyCertified=0,actualCompactions=0,rootActualCompactions=0,predecessorHandoff=str(S/'handoff-next.json'),inheritedManifest=str(S/'manifest.json'),helpers={n:str(D/n) for n in h['helpers']},ownProgress={'intake':943,'newlyCertified':0,'accepted':[],'certificates':[]},ownAffectedRuns=[],inheritedAffectedRuns=priorRuns,currentWork={'stage':'TAKEOVER_CURRENT943_BEFORE_HISTORY_RUSSIA28','CURRENT':943,'remaining':1057},next='Prepare one untouched SOURCE28 retained-sources first; preserve all HOLDs including23/24/25; retained live idle reviewer before INITIAL28 after fresh native/context preflight',rootContextReason='Fresh successor actual0; predecessor preventive bounded handoff actual0; preserve all fences',successorThreadId=None,successorNativeJournal=None,successorCreationProof=None,successorACK=None,sourceActorKeys=[],createdNativeThreadsCurrentOwner=[],oldRootStoppedControl=True,at=datetime.datetime.now(datetime.timezone.utc).isoformat())
x['actors']={'reviewer':h['actors']['reviewer']};x['retainedIdleReviewer']=h['retainedIdleReviewer'];x['noRetainedIdleReviewer']=False;x.update(successorStatus='ACTIVE',currentSourceActors=[],currentIndependentActors=[],currentSourceActorsCount=0,noRetainedIdleAuthor=True,leaseHeld=False)
x['readScope']={**h['readScope'],'ownD':str(D)};x['helperInstanceVerification']='Identity e25->e52; own intake941->943; AST parsed; zero active authors/review tasks; live idle reviewer retained. Historical46/83 templates and retained SOURCE19/20/21/22/23-27 accounting paths unchanged; sourceIndex/additional indexes remain actual old roots.';x['rootNativeAudit']={'threadId':O,'nativeJournal':str(native),'actualCompactions':0}; x['retainedIdleReviewer']['stage']='IDLE_AFTER_INITIAL27_PASS_AVAILABLE_FOR_INITIAL28_AFTER_PREFLIGHT'; x['actors']['reviewer']['stage']=x['retainedIdleReviewer']['stage']
assert x['actors']['reviewer']['threadId']=='01a15db8-e016-7662-988d-1fd4eedccf31' and not x['actors']['reviewer'].get('archived',False)
assert x['sourceIndex']==h['sourceIndex'] and x['additionalRetainedSourceIndexes']==h['additionalRetainedSourceIndexes'] and len(x['coordinatorSlicesToPreserve'])==27
write(D/'manifest.json',x)
report={'owner':O,'predecessor':OLD,'phase':'SUPPORTED_EXACT3_DURABLE_TAKEOVER','CURRENT':943,'remaining':1057,'fullGoal':2000,'intakeCURRENT':943,'newlyCertified':0,'predecessorRemotePush':remote,'readScope':x['readScope'],'foreignIndexes':h['foreignIndexes'],'handoffSHA256':raw(S/'handoff-next.json'),'manifestSHA256':raw(S/'manifest.json'),'canonicalCheckpointBeforeSHA256':raw(cp_path),'claims':h['claims'],'coordinatorSlicesToPreserve':h['coordinatorSlicesToPreserve'],'helperClones':{f.name:raw(f) for f in clones},'noSemanticRereviewOrTest':True,'actualCompactions':0,'at':x['at']};write(D/'takeover.json',report)
cc=sv.save(C,'refs/heads/codex/question-quality-wave-6',[str(p.relative_to(C)) for p in clones+[D/'manifest.json',D/'takeover.json',pathlib.Path(__file__)]],'Preserve CURRENT943 successor identity and bounded helpers',expected[C]);print('code',cc)
with flow.locked():
 assert all(flow.get(cid)[1]['owner'] is None for cid in h['claims']);flow.lease('acquire','planning',O)
try:
 with flow.locked():
  for cid in h['claims']:flow.claim(cid,O)
 cp.update(owner=O,activeCoordinator=O,phase=x['phase'],currentManifest=str(D/'manifest.json'),pendingSuccessor=None,successorThreadId=None,successorStatus='ACTIVE',ordinaryWorkActivated=True,currentSourceActors=[],currentIndependentActors=[],currentSourceActiveCount=0,nativeActorsCurrent=cp['nativeActorsCurrent'],next=x['next'],coordinatorActualCompactions=0)
 cp['ownershipTransfer']={'predecessor':OLD,'successor':O,'status':'SUPPORTED_EXACT3_DURABLE_TAKEOVER','CURRENT':943,'remaining':1057,'fullGoal':2000,'claims':h['claims'],'handoff':str(S/'handoff-next.json'),'rootActualCompactions':0};write(cp_path,cp)
 sp=P/'evidence/question-revision-process-v2/coordinator-state.json';st=read(sp);st.update(threadId=O,owner=O,activeCoordinator=O,claims=h['claims'],phase=x['phase'],status='ACTIVE_FULL2000',currentManifest=str(D/'manifest.json'),pendingSuccessor=None,successor=None,successorThreadId=None,successorStatus='ACTIVE',ownActualCompactions=0,rootActualCompactions=0,actualRootCompactions=0,coordinatorActualCompactions=0,ordinaryWorkActivated=True,counts={'CURRENT':943,'remaining':1057},ownedIntake={'CURRENT':943,'newlyCertified':0,'remaining':1057,'fullGoal':2000},coordinatorProgress={'intakeCURRENT':943,'CURRENT':943,'newlyCertified':0,'remaining':1057},currentWork=x['currentWork'],codeCommit=cc,next=x['next'],activeAuthors=[],idleAuthors=[],activeIndependentReview=None,currentSourceActors=[],currentIndependentActors=[],nativeActorsCurrent=cp['nativeActorsCurrent'],currentNativeActors={a['threadId']:a for a in cp['nativeActorsCurrent']},coordinatorSlicesToPreserve=h['coordinatorSlicesToPreserve'],activeGoal='Full SOURCE/editorial exact2000 waves6-9; own intake943; preserve all prior HOLDs',asOf=x['at']);write(sp,st)
 gp=P/'evidence/question-revision-process-v2/active-full2000-goal-01a1593a.json';g=read(gp);g.update(owner=O,intakeCURRENT=943,newlyCertified=0,CURRENT=943,remaining=1057,manifest=str(D/'manifest.json'),latestCodeCommit=cc,pendingSuccessor=None,successor=None,successorStatus='ACTIVE',coordinatorSlicesToPreserve=h['coordinatorSlicesToPreserve']);write(gp,g)
 pp=P/'evidence/question-revision-process-v2/takeover-01a15e52.json';write(pp,{**report,'codeCommit':cc})
 pc=sv.save(P,'refs/heads/codex/question-revision-resume-20261014',[str(p.relative_to(P)) for p in [cp_path,sp,gp,pp]+[flow.get(cid)[0] for cid in h['claims']]],'Record supported exact3 CURRENT943 takeover',expected[P]);print('planning',pc)
finally:
 with flow.locked():flow.lease('release','planning',O)
assert all(flow.get(cid)[1]['owner']==O for cid in h['claims']) and read(P/'.flow-leases.json')=={}
for r in idx:assert raw(idx[r])==expected[r]
print('exact3 owned; lease empty; both foreign indexes preserved')
