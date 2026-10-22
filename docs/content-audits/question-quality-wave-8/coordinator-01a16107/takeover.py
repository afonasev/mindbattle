"""After ACTIVATE only: exact-native supported takeover, parameterized intake and identity.
Copy to successor ownD/takeover.py; run -B takeover.py EXACT_OWNER EXACT_NATIVE PREDECESSOR_HANDOFF.
Never obtain identity from environment or newest timestamps. No quality or QA replay.
"""
import pathlib,json,hashlib,importlib.util,ast,datetime,sys
D=pathlib.Path(__file__).parent;O=sys.argv[1];native=pathlib.Path(sys.argv[2]);hp=pathlib.Path(sys.argv[3]);S=hp.parent

def read(p):return json.loads(pathlib.Path(p).read_text())
def raw(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def sha(v):return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def mod(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
h=read(hp);C=pathlib.Path(h['C']);P=pathlib.Path(h['P']);OLD=h['rootNativeAudit']['threadId'];n=h['CURRENT'];oldIntake=h['ownIntakeCURRENT'];assert O!=OLD and D.parent==S.parent and D.name=='coordinator-'+O[:8]
rows=[json.loads(l) for l in native.open()];assert next(r['payload']['id'] for r in rows if r['type']=='session_meta')==O;assert sum(r['type']=='compacted' for r in rows)==0
assert h['successorThreadId']==O and h['phase']=='EXACT3_RELEASED_PENDING_SUCCESSOR_CLAIM' and h['fullGoal']==2000 and h['remaining']==2000-n
creation=read(h['successorCreationProof']);assert creation['returnedSuccessorThreadId']==creation['successorNativeSessionMetaId']==O and creation['successorNativeJournal']==str(native)
flow=mod('flow',C/'tools/flow.py').Flow(P);sv=mod('private',P/'evidence/question-revision-process-v2/private-save-helper-01a13cb1.py');expected={C:h['foreignIndexes']['code'],P:h['foreignIndexes']['planning']};idx={r:pathlib.Path(sv.git(r,'rev-parse','--path-format=absolute','--git-path','index')) for r in [C,P]}
for r in idx:assert raw(idx[r])==expected[r]
assert read(P/'.flow-leases.json')=={} and all(flow.get(cid)[1]['owner'] is None for cid in h['claims'])
cp_path=pathlib.Path(h['canonicalCheckpoint']);cp=read(cp_path);assert cp['owner'] is cp['activeCoordinator'] is None and len(cp['currentEligibleCompletedIds'])==n and len(cp['currentRemainingIds'])==2000-n
selected={v['questionId'] for v in cp['selectedCards']};done=set(cp['currentEligibleCompletedIds']);remaining=set(cp['currentRemainingIds']);assert len(selected)==2000 and len(done)==n and len(remaining)==2000-n and not done&remaining and done|remaining==selected
cat={}
for p in (C/'src/content/topics').glob('*.json'):cat.update({q['id']:q for q in read(p)['questions']})
assert len(cp['completedCardHashes'])==n and all(sha(cat[e['questionId']])==e['cardCanonicalSha256'] for e in cp['completedCardHashes'])
remote=flow.get(h['claims'][0])[1]['evidence']['remote_push'];assert all(flow.get(cid)[1]['evidence']['remote_push']==remote for cid in h['claims']);assert remote['CURRENT']==n and remote['remaining']==2000-n and remote['readbackVerified'];assert sv.git(C,'ls-remote','origin','refs/heads/'+h['codeBranch']).split()[0]==remote['commit']
def write(p,v):
 p=pathlib.Path(p)
 if P in p.parents:assert raw(idx[P])==expected[P] and read(P/'.flow-leases.json').get('planning',{}).get('owner')==O
 p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
clones=[]
for name in dict.fromkeys([*h['helpers'],'preserve-packet.py']):
 text=(S/name).read_text().replace("O='"+OLD+"'","O='"+O+"'").replace('-'+OLD[:8]+'.json','-'+O[:8]+'.json').replace("'ownIntakeCURRENT':"+str(oldIntake),"'ownIntakeCURRENT':"+str(n)).replace('n-'+str(oldIntake),'n-'+str(n))
 if name.endswith('.py'):ast.parse(text)
 (D/name).write_text(text);clones.append(D/name)
assert "O='"+O+"'" in (D/'owned-tools.py').read_text();assert "'ownIntakeCURRENT':"+str(n) in (D/'bind-current-receipt.py').read_text();assert 'n-'+str(n) in (D/'certification-common.py').read_text()
assert 'coordinator-01a15a0f/reader-polar46-initial-task.json' in (D/'prepare-initial.py').read_text() and 'packet_name = sys.argv[5]' in (D/'prepare-initial.py').read_text()
x=read(S/'manifest.json');priorRuns=x.get('inheritedAffectedRuns',[])+[v['path'] if isinstance(v,dict) else v for v in x.get('ownAffectedRuns',[])];reviewer=h.get('retainedIdleReviewer');actor=dict(reviewer or h['actors']['reviewer']);assert not actor['stage'].startswith('START')
x.update(owner=O,claimsOwner=O,heldOwn=list(h['claims']),phase='ACTIVE_TAKEOVER_CURRENT'+str(n),manifest=str(D/'manifest.json'),intakeCURRENT=n,ownIntakeCURRENT=n,newlyCertified=0,actualCompactions=0,rootActualCompactions=0,predecessorHandoff=str(hp),inheritedManifest=str(S/'manifest.json'),helpers={name:str(D/name) for name in h['helpers']},ownProgress={'intake':n,'newlyCertified':0,'accepted':[],'certificates':[]},ownAffectedRuns=[],inheritedAffectedRuns=priorRuns,sourceActorKeys=[],actors={'reviewer':actor},retainedIdleReviewer=dict(reviewer) if reviewer else None,noRetainedIdleReviewer=reviewer is None,noRetainedIdleAuthor=True,retainedIdleAuthorsCurrentOwner=[],createdNativeThreadsCurrentOwner=[],currentSourceActors=[],currentIndependentActors=[],currentSourceActorsCount=0,leaseHeld=False,pendingSuccessor=None,successor=None,successorThreadId=None,successorNativeJournal=None,successorCreationProof=None,successorACK=None,successorStatus='ACTIVE',rootStop=None,oldRootStoppedControl=True,rootContextReason='Fresh actual0 successor; previous bounded handoff actual0 preserved, no quality replay.',currentWork={'stage':'TAKEOVER_CURRENT'+str(n)+'_BEFORE_NEXT_UNTOUCHED','CURRENT':n,'remaining':2000-n},next='Archive stopped predecessor after durable takeover, then fill authorized max2authors/max1reviewer/readyqueue2 on next untouched IDs; fresh native/context budget before any retained reviewer INITIAL.',rootNativeAudit={'threadId':O,'nativeJournal':str(native),'actualCompactions':0},predecessorCleanup={'threadId':OLD,'archived':False,'afterDurableTakeoverRequired':True},handoffRestrictions='Predecessor read-only barrier explicitly passed by ACTIVATE; original SOURCE scope and all per-card/HOLD/attempt/session fences persist. No mainmerge/fulltests/runtime/browser/Player/build/deploy/release/OpenSpecarchive.',at=datetime.datetime.now(datetime.timezone.utc).isoformat())
x['readScope']={**h['readScope'],'ownD':str(D)};assert x['sourceIndex']==h['sourceIndex'] and x['additionalRetainedSourceIndexes']==h['additionalRetainedSourceIndexes'];write(D/'manifest.json',x)
report={'owner':O,'predecessor':OLD,'phase':'SUPPORTED_EXACT3_DURABLE_TAKEOVER','CURRENT':n,'remaining':2000-n,'fullGoal':2000,'intakeCURRENT':n,'newlyCertified':0,'predecessorRemotePush':remote,'foreignIndexes':h['foreignIndexes'],'handoffSHA256':raw(hp),'canonicalCheckpointBeforeSHA256':raw(cp_path),'claims':h['claims'],'coordinatorSlicesToPreserve':h['coordinatorSlicesToPreserve'],'helperClones':{p.name:raw(p) for p in clones},'identityReplacementOnly':{'oldOwner':OLD,'newOwner':O,'oldOwnIntake':oldIntake,'newOwnIntake':n},'noSemanticRereviewOrTest':True,'actualCompactions':0};write(D/'takeover.json',report)
cc=sv.save(C,'refs/heads/'+h['codeBranch'],[str(p.relative_to(C)) for p in [*clones,D/'manifest.json',D/'takeover.json',pathlib.Path(__file__)]],f'Preserve CURRENT{n} native successor and bounded helpers',expected[C]);print('code',cc)
assert raw(idx[P])==expected[P]
with flow.locked():
 assert raw(idx[P])==expected[P] and all(flow.get(cid)[1]['owner'] is None for cid in h['claims']);flow.lease('acquire','planning',O)
try:
 with flow.locked():
  for cid in h['claims']:assert raw(idx[P])==expected[P];flow.claim(cid,O)
 cp.update(owner=O,activeCoordinator=O,phase=x['phase'],currentManifest=str(D/'manifest.json'),pendingSuccessor=None,successorThreadId=None,successorStatus='ACTIVE',ordinaryWorkActivated=True,currentSourceActors=[],currentIndependentActors=[],currentSourceActiveCount=0,nativeActorsCurrent=[actor] if reviewer else [],next=x['next'],coordinatorActualCompactions=0,oldRootStoppedControl=True)
 cp['ownershipTransfer']={'predecessor':OLD,'successor':O,'status':'SUPPORTED_EXACT3_DURABLE_TAKEOVER','CURRENT':n,'remaining':2000-n,'fullGoal':2000,'claims':h['claims'],'handoff':str(hp),'rootActualCompactions':0};write(cp_path,cp)
 sp=P/'evidence/question-revision-process-v2/coordinator-state.json';st=read(sp);st.update(threadId=O,owner=O,activeCoordinator=O,claims=h['claims'],phase=x['phase'],status='ACTIVE_FULL2000',currentManifest=str(D/'manifest.json'),pendingSuccessor=None,successor=None,successorThreadId=None,successorStatus='ACTIVE',ownActualCompactions=0,rootActualCompactions=0,actualRootCompactions=0,coordinatorActualCompactions=0,ordinaryWorkActivated=True,counts={'CURRENT':n,'remaining':2000-n},ownedIntake={'CURRENT':n,'newlyCertified':0,'remaining':2000-n,'fullGoal':2000},coordinatorProgress={'intakeCURRENT':n,'CURRENT':n,'newlyCertified':0,'remaining':2000-n},currentWork=x['currentWork'],codeCommit=cc,next=x['next'],activeAuthors=[],idleAuthors=[],activeIndependentReview=None,currentSourceActors=[],currentIndependentActors=[],nativeActorsCurrent=cp['nativeActorsCurrent'],currentNativeActors={a['threadId']:a for a in cp['nativeActorsCurrent']},coordinatorSlicesToPreserve=h['coordinatorSlicesToPreserve'],activeGoal=f'Full SOURCE/editorial exact2000 waves6-9; own intake{n}; preserve prior HOLDs and user2author concurrency',asOf=x['at']);write(sp,st)
 gp=P/'evidence/question-revision-process-v2/active-full2000-goal-01a1593a.json';g=read(gp);g.update(owner=O,activeCoordinator=O,successorThreadId=None,intakeCURRENT=n,newlyCertified=0,CURRENT=n,remaining=2000-n,phase=x['phase'],manifest=str(D/'manifest.json'),latestCodeCommit=cc,pendingSuccessor=None,successor=None,successorStatus='ACTIVE',coordinatorSlicesToPreserve=h['coordinatorSlicesToPreserve']);write(gp,g)
 pp=P/f'evidence/question-revision-process-v2/takeover-{O[:8]}.json';write(pp,{**report,'codeCommit':cc});pc=sv.save(P,'refs/heads/'+h['planningBranch'],[str(p.relative_to(P)) for p in [cp_path,sp,gp,pp,*[flow.get(cid)[0] for cid in h['claims']]]],f'Record supported exact3 CURRENT{n} native takeover',expected[P]);print('planning',pc)
finally:
 with flow.locked():flow.lease('release','planning',O)
assert all(flow.get(cid)[1]['owner']==O for cid in h['claims']) and read(P/'.flow-leases.json')=={}
for r in idx:assert raw(idx[r])==expected[r]
print('exact3 owned; CP/state/goal durable; lease empty; both foreign indexes preserved; archive predecessor next',OLD)
