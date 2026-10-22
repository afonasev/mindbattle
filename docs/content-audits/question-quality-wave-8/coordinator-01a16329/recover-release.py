"""Explicit human ACTIVATE: recover interrupted predecessor release through Flow.release, no identity impersonation."""
import pathlib,json,hashlib,importlib.util,subprocess
D=pathlib.Path(__file__).parent;S=D.parent/'coordinator-01a16254';O='01a16329-04c9-75f0-806f-091bcec4b169';OLD='01a16254-5cb1-7583-924e-f17339344af7'
def read(p):return json.loads(pathlib.Path(p).read_text())
def raw(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def mod(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
h=read(S/'handoff-next.json');C=pathlib.Path(h['C']);P=pathlib.Path(h['P']);flow=mod('flow',C/'tools/flow.py').Flow(P);sv=mod('sv',P/'evidence/question-revision-process-v2/private-save-helper-01a13cb1.py')
native=pathlib.Path('/Users/eaafonasev/.codex/sessions/2026/10/22/rollout-2026-10-22T15-29-55-01a16329-04c9-75f0-806f-091bcec4b169.jsonl');rs=[json.loads(l)for l in native.open()];assert next(r['payload']['id']for r in rs if r['type']=='session_meta')==O and sum(r['type']=='compacted'for r in rs)==0
assert h['successorThreadId']==O and h['phase']=='READY_FOR_READONLY_SUCCESSOR_CURRENT988'
parent=pathlib.Path('/Users/eaafonasev/.codex/archived_sessions/rollout-2026-10-22T11-37-38-01a16254-5cb1-7583-924e-f17339344af7.jsonl');pr=[json.loads(l)for l in parent.open()];assert next(r['payload']['id']for r in pr if r['type']=='session_meta')==OLD and pr[-1]['payload']['type']=='turn_aborted'
ack=read(S/'successor-ack.json');assert ack['successor']==O and ack['rootPersonallyVerifiedExactNativeACK'] and len(ack['fullFourDocumentsSuccessfulUntruncatedReads'])==4
out=next(r for r in pr if r.get('payload',{}).get('call_id')=='call_8d3b98fa91ca4c26a80420ba8522901a' and r['payload']['type']=='custom_tool_call_output');assert any('exit_code' in b.get('text','') and json.loads(b['text'])['exit_code']==0 for b in out['payload']['output'])
expected=h['foreignIndexes'];idx={r:pathlib.Path(sv.git(r,'rev-parse','--path-format=absolute','--git-path','index')) for r in [C,P]}
for r,k in [(C,'code'),(P,'planning')]:assert raw(idx[r])==expected[k]
assert read(P/'.flow-leases.json')=={} and all(flow.get(cid)[1]['owner']==OLD for cid in h['claims'])
recovery={'actor':O,'predecessor':OLD,'reason':'Predecessor archived after successful native ACK verification, turn_aborted before supported release; exact3 still owned by predecessor. Explicit human ACTIVATE in successor authorizes recovery and continuation.','authorization':'Current human message ACTIVATE: verify supported release all3, take ownership and continue all2000 from89 preserving fences.','policy':'flow/lifecycle.md interrupted ownership: inspect resources, explicit release using previous owner ID, log recovery, then claim new session.','parentNative':str(parent),'parentVerificationCall':'call_8d3b98fa91ca4c26a80420ba8522901a','parentVerificationExitCode':0,'originalACK':str(S/'successor-ack.json'),'CURRENT':988,'remaining':1012,'claims':h['claims'],'foreignIndexes':expected}
def write(p,v):
 p=pathlib.Path(p)
 if P in p.parents:assert read(P/'.flow-leases.json').get('planning',{}).get('owner')==O and raw(idx[P])==expected['planning']
 p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
write(D/'release-recovery.json',recovery)
print('recoveryCode',sv.save(C,'refs/heads/'+h['codeBranch'],[str(p.relative_to(C))for p in [pathlib.Path(__file__),D/'release-recovery.json']],'Preserve explicit ACTIVATE interrupted ownership recovery',expected['code']))
phase='EXACT3_RELEASED_PENDING_SUCCESSOR_CLAIM'
with flow.locked():flow.lease('acquire','planning',O)
try:
 with flow.locked():
  for cid in h['claims']:
   assert raw(idx[P])==expected['planning'];flow.release(cid,OLD);p,d=flow.get(cid);flow.save(p,d,'interrupted-ownership-recovered',actor=O,previousOwner=OLD,evidence=str(D/'release-recovery.json'),authorization=recovery['authorization'])
 cp_path=pathlib.Path(h['canonicalCheckpoint']);cp=read(cp_path);assert cp['owner']==cp['activeCoordinator']==OLD;cp.update(owner=None,activeCoordinator=None,phase=phase,successorStatus='RELEASED_PENDING_SUCCESSOR_CLAIM',ordinaryWorkActivated=False,oldRootStoppedControl=True,successorACK=str(S/'successor-ack.json'));cp['ownershipTransfer']={'predecessor':OLD,'successor':O,'status':phase,'claims':h['claims'],'CURRENT':988,'remaining':1012,'handoff':str(S/'handoff-next.json'),'rootActualCompactions':1,'recovery':recovery};write(cp_path,cp)
 sp=P/'evidence/question-revision-process-v2/coordinator-state.json';st=read(sp);assert st['owner']==OLD;st.update(owner=None,activeCoordinator=None,claimsOwner=None,phase=phase,status=phase,successorStatus='RELEASED_PENDING_SUCCESSOR_CLAIM',ordinaryWorkActivated=False,oldRootStoppedControl=True,activeAuthors=[],idleAuthors=[],activeIndependentReview=None,successorACK=str(S/'successor-ack.json'));write(sp,st)
 gp=P/'evidence/question-revision-process-v2/active-full2000-goal-01a1593a.json';g=read(gp);assert g['owner']==OLD;g.update(owner=None,activeCoordinator=None,phase=phase,oldRootStoppedControl=True,successorStatus='RELEASED_PENDING_SUCCESSOR_CLAIM');write(gp,g)
 pp=P/'evidence/question-revision-process-v2/release-recovery-01a16329.json';write(pp,recovery);paths=[cp_path,sp,gp,pp,*[flow.get(cid)[0]for cid in h['claims']]];pc=sv.save(P,'refs/heads/'+h['planningBranch'],[str(p.relative_to(P))for p in paths],'Recover interrupted exact3 release to ACTIVATE successor',expected['planning']);print('releasePlanning',pc)
finally:
 with flow.locked():flow.lease('release','planning',O)
h.update(owner=None,claimsOwner=None,heldOwn=[],phase=phase,successorStatus='RELEASED_PENDING_SUCCESSOR_CLAIM',oldRootStoppedControl=True,planningReleaseCommit=pc,supportedReleaseP=pc,leaseHeld=False,interruptedReleaseRecovery=recovery)
for p in [S/'manifest.json',S/'handoff-next.json']:write(p,h)
print('releaseCode',sv.save(C,'refs/heads/'+h['codeBranch'],[str(p.relative_to(C))for p in [S/'manifest.json',S/'handoff-next.json']],'Record recovered supported exact3 release and stopped predecessor',expected['code']))
assert all(flow.get(cid)[1]['owner'] is None for cid in h['claims']) and read(P/'.flow-leases.json')=={}
for r,k in [(C,'code'),(P,'planning')]:assert raw(idx[r])==expected[k]
print('exact3 released via supported Flow.release; actual recovery actor recorded; lease empty; indexes exact')
