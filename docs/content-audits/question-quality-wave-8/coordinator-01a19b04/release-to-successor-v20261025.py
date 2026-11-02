"""Supported exact4 release after personally verified readonly successor ACK."""
import pathlib,json,importlib.util
D=pathlib.Path(__file__).parent
s=importlib.util.spec_from_file_location('m',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
x=m.read(D/'manifest.json');ack=m.read(D/'successor-ack.json');S=x['successorThreadId'];assert ack['successor']==S and ack['rootPersonallyVerifiedExactNativeACK']
rootRows=[json.loads(l) for l in pathlib.Path(x['rootNativeAudit']['nativeJournal']).open()];assert next(r['payload']['id'] for r in rootRows if r['type']=='session_meta')==m.O
rootCompactions=sum(r['type']=='compacted' for r in rootRows)
assert not any(a['stage'].startswith('START') for a in x['actors'].values())
assert ack['processRevision']=='2026-10-25' and ack['rootPersonallyVerifiedSupportedACK']
assert ack['supportedCompletion']['threadId']==S and ack['supportedCompletion']['status']=='completed'
assert ack['CURRENT']==x['CURRENT'] and ack['remaining']==x['remaining'] and ack['readOnlyIntakeGuard']=='PASS'
assert all(m.flow.get(cid)[1]['owner']==m.O for cid in x['claims']) and m.read(m.P/'.flow-leases.json')=={}
precp=m.read(pathlib.Path(x['canonicalCheckpoint']));assert precp['owner']==m.O
assert all(w['owner'] in {m.O,None} for w in precp['waves'] if w['changeId'] in x['claims'] and 'owner' in w)
for root,key in [(m.C,'code'),(m.P,'planning')]:assert m.raw(pathlib.Path(m.h.git(root,'rev-parse','--path-format=absolute','--git-path','index')))==x['foreignIndexes'][key]
print('preReleaseCode',m.savecode([pathlib.Path(__file__),D/'successor-ack.json'],'Preserve supported exact4 release procedure and successful native ACK verification'))
phase='EXACT4_RELEASED_PENDING_SUCCESSOR_CLAIM'
planningIndex=pathlib.Path(m.h.git(m.P,'rev-parse','--path-format=absolute','--git-path','index'));expectedPlanningIndex=m.raw(planningIndex)
assert expectedPlanningIndex==x['foreignIndexes']['planning']
with m.flow.locked():m.flow.lease('acquire','planning',m.O)
try:
 assert m.raw(planningIndex)==expectedPlanningIndex
 with m.flow.locked():
  livecp=m.read(pathlib.Path(x['canonicalCheckpoint']));assert livecp['owner']==m.O
  assert all(w['owner'] in {m.O,None} for w in livecp['waves'] if w['changeId'] in x['claims'] and 'owner' in w)
  for cid in x['claims']:
   assert m.raw(planningIndex)==expectedPlanningIndex and m.read(m.P/'.flow-leases.json').get('planning',{}).get('owner')==m.O
   m.flow.release(cid,m.O)
 cp_path=pathlib.Path(x['canonicalCheckpoint']);cp=m.read(cp_path);assert cp['owner']==m.O;cp.update(owner=None,activeCoordinator=None,phase=phase,successorStatus='RELEASED_PENDING_SUCCESSOR_CLAIM',ordinaryWorkActivated=False,oldRootStoppedControl=True,successorACK=str(D/'successor-ack.json'))
 for w in cp['waves']:
  if w['changeId'] in x['claims'] and 'owner' in w:
   assert w['owner'] in {m.O,None}, 'Never release a foreign per-wave owner'
   w['owner']=None
 cp['ownershipTransfer']={'predecessor':m.O,'successor':S,'status':phase,'claims':x['claims'],'CURRENT':x['CURRENT'],'remaining':x['remaining'],'handoff':str(D/'handoff-next.json'),'rootActualCompactions':rootCompactions};m.write(cp_path,cp)
 sp=m.P/'evidence/question-revision-process-v2/coordinator-state.json';st=m.read(sp);st.update(owner=None,activeCoordinator=None,claimsOwner=None,phase=phase,status=phase,successorStatus='RELEASED_PENDING_SUCCESSOR_CLAIM',ordinaryWorkActivated=False,oldRootStoppedControl=True,activeAuthors=[],idleAuthors=[],activeIndependentReview=None,successorACK=str(D/'successor-ack.json'));m.write(sp,st)
 gp=m.P/'evidence/question-revision-process-v2/active-full2000-goal-01a1593a.json';g=m.read(gp);g.update(owner=None,activeCoordinator=None,phase=phase,oldRootStoppedControl=True,successorStatus='RELEASED_PENDING_SUCCESSOR_CLAIM',successorACK=str(D/'successor-ack.json'));m.write(gp,g)
 files=[cp_path,sp,gp]+[m.flow.get(cid)[0] for cid in x['claims']]
 pc=m.h.save(m.P,'refs/heads/'+x['planningBranch'],[str(p.relative_to(m.P)) for p in files],f'Release exact4 CURRENT{x["CURRENT"]} claims to verified readonly successor',expectedPlanningIndex);print('releasePlanning',pc)
finally:
 with m.flow.locked():m.flow.lease('release','planning',m.O)
x.update(owner=None,claimsOwner=None,heldOwn=[],phase=phase,successorStatus='RELEASED_PENDING_SUCCESSOR_CLAIM',oldRootStoppedControl=True,planningReleaseCommit=pc,supportedReleaseP=pc,leaseHeld=False)
for p in [D/'manifest.json',D/'handoff-next.json']:m.write(p,x)
print('releaseCode',m.savecode([D/'manifest.json',D/'handoff-next.json'],'Record supported exact4 release and stopped predecessor control'))
assert all(m.flow.get(cid)[1]['owner'] is None for cid in x['claims']) and m.read(m.P/'.flow-leases.json')=={}
for root,key in [(m.C,'code'),(m.P,'planning')]:assert m.raw(pathlib.Path(m.h.git(root,'rev-parse','--path-format=absolute','--git-path','index')))==x['foreignIndexes'][key]
print('exact4Released',S,'leaseHeld',False,'foreignIndexesPreserved',True)
