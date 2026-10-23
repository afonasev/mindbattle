"""Human-authorized supported release of exact four stopped-owner claims.
No catalog edits, QA, role resets, default indexes or force recovery.
"""
import json, hashlib, pathlib, importlib.util, subprocess, datetime
D=pathlib.Path(__file__).parent
S=D.with_name('coordinator-01a168bb')
O='01a16922-1822-7311-9f72-c6bd403573b8'
OLD='01a168bb-acce-7442-9c79-71e240771c35'
N=pathlib.Path('/Users/eaafonasev/.codex/sessions/2026/10/23/rollout-2026-10-23T19-20-04-01a16922-1822-7311-9f72-c6bd403573b8.jsonl')
def read(p):return json.loads(p.read_text())
def raw(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def mod(name,p):
 s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
h=read(S/'handoff-next.json');C=pathlib.Path(h['C']);P=pathlib.Path(h['P'])
flow=mod('flow_recovery',C/'tools/flow.py').Flow(P)
sv=mod('save_recovery',P/'evidence/question-revision-process-v2/private-save-helper-01a13cb1.py')
rows=[json.loads(l) for l in N.open()]
assert [r['payload']['id'] for r in rows if r['type']=='session_meta']==[O]
assert sum(r['type']=='compacted' for r in rows)==0
auth=[]
for i,r in enumerate(rows,1):
 p=r.get('payload',{})
 if r['type']=='response_item' and p.get('role')=='user':
  for c in p.get('content',[]):
   if c.get('type')=='input_text' and c.get('text','').startswith('Разрешаю восстановить и передать себе владение всеми четырьмя claim'):
    auth.append({'nativeLine':i,'originalUserMessage':r})
assert len(auth)==1
oldjournal=pathlib.Path(h['rootNativeAudit']['nativeJournal'])
if not oldjournal.exists():
 paths=list(pathlib.Path('/Users/eaafonasev/.codex/archived_sessions').glob('**/*'+OLD+'.jsonl'))
 assert len(paths)==1;oldjournal=paths[0]
oldrows=[json.loads(l) for l in oldjournal.open()]
assert [r['payload']['id'] for r in oldrows if r['type']=='session_meta']==[OLD]
assert next(r['payload']['type'] for r in reversed(oldrows) if r.get('payload',{}).get('type') in ['task_started','task_complete'])=='task_complete'
assert h['owner']==OLD and h['successorThreadId']==O and h['CURRENT']==1026 and h['remaining']==974
assert len(h['claims'])==4 and all(flow.get(cid)[1]['owner']==OLD for cid in h['claims'])
assert read(P/'.flow-leases.json')=={} and h.get('retainedIdleReviewer') is None
idx={r:pathlib.Path(sv.git(r,'rev-parse','--path-format=absolute','--git-path','index')) for r in [C,P]}
for r,k in [(C,'code'),(P,'planning')]:assert raw(idx[r])==h['foreignIndexes'][k]
cp_path=pathlib.Path(h['canonicalCheckpoint']);cp=read(cp_path)
assert cp['owner']==cp['activeCoordinator']==OLD
assert len(cp['currentEligibleCompletedIds'])==1026 and len(cp['currentRemainingIds'])==974
pushes=[flow.get(cid)[1]['evidence']['remote_push'] for cid in h['claims']]
assert all(v==pushes[0] for v in pushes)
assert sv.git(C,'ls-remote','origin','refs/heads/'+h['codeBranch']).split()[0]==pushes[0]['commit']
report={'owner':O,'predecessor':OLD,'authorization':auth[0],'parentTaskCompleteObserved':True,'actualParentJournal':str(oldjournal),'originalMissingHistoricalJournalPathFailureUncured':True,'method':'Flow.release with exact previous owner under own short planning lease; then unmodified takeover template','CURRENT':1026,'remaining':974,'fullGoal':2000,'claims':h['claims'],'foreignIndexes':h['foreignIndexes'],'preReleaseHandoffSHA256':raw(S/'handoff-next.json'),'preReleaseCPSHA256':raw(cp_path),'originalParentACKNotFabricated':True,'at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
write(D/'recovery-authorization.json',report)
phase='EXACT4_RELEASED_PENDING_SUCCESSOR_CLAIM'
with flow.locked():
 assert all(flow.get(cid)[1]['owner']==OLD for cid in h['claims'])
 flow.lease('acquire','planning',O)
try:
 with flow.locked():
  assert raw(idx[P])==h['foreignIndexes']['planning']
  for cid in h['claims']:flow.release(cid,OLD)
 cp.update(owner=None,activeCoordinator=None,phase=phase,successorStatus='RELEASED_PENDING_SUCCESSOR_CLAIM',ordinaryWorkActivated=False,oldRootStoppedControl=True)
 for w in cp['waves']:
  if w['changeId'] in h['claims'] and 'owner' in w:
   assert w['owner'] in {OLD,None};w['owner']=None
 cp['ownershipTransfer']={**{k:report[k] for k in ['predecessor','CURRENT','remaining','fullGoal','claims']},'successor':O,'status':phase,'authorization':str(D/'recovery-authorization.json'),'handoff':str(S/'handoff-next.json')}
 write(cp_path,cp)
 files=[cp_path]
 for name in ['coordinator-state.json','active-full2000-goal-01a1593a.json']:
  p=P/'evidence/question-revision-process-v2'/name;v=read(p);assert v['owner']==OLD
  v.update(owner=None,activeCoordinator=None,claimsOwner=None,phase=phase,ordinaryWorkActivated=False,oldRootStoppedControl=True,successorStatus='RELEASED_PENDING_SUCCESSOR_CLAIM',recoveryAuthorization=str(D/'recovery-authorization.json'));write(p,v);files.append(p)
 pp=P/'evidence/question-revision-process-v2/recovery-release-01a16922.json';write(pp,report);files.append(pp)
 files.extend(flow.get(cid)[0] for cid in h['claims'])
 pc=sv.save(P,'refs/heads/'+h['planningBranch'],[str(p.relative_to(P)) for p in files],'Record human-authorized supported exact4 release to verified successor',h['foreignIndexes']['planning'])
finally:
 with flow.locked():flow.lease('release','planning',O)
for p in [S/'manifest.json',S/'handoff-next.json']:
 v=read(p);v.update(owner=None,claimsOwner=None,heldOwn=[],phase=phase,successorStatus='RELEASED_PENDING_SUCCESSOR_CLAIM',oldRootStoppedControl=True,planningReleaseCommit=pc,supportedReleaseP=pc,leaseHeld=False,recoveryAuthorization=str(D/'recovery-authorization.json'));write(p,v)
cc=sv.save(C,'refs/heads/'+h['codeBranch'],[str(p.relative_to(C)) for p in [S/'manifest.json',S/'handoff-next.json',D/'recovery-authorization.json',pathlib.Path(__file__)]],'Preserve human-authorized exact4 release and original ownership lineage',h['foreignIndexes']['code'])
assert all(flow.get(cid)[1]['owner'] is None for cid in h['claims']) and read(P/'.flow-leases.json')=={}
for r,k in [(C,'code'),(P,'planning')]:assert raw(idx[r])==h['foreignIndexes'][k]
print({'phase':phase,'releasePlanning':pc,'releaseCode':cc,'leaseEmpty':True,'foreignIndexesPreserved':True})
