"""Supported exact3 release after verified readonly successor ACK."""
import pathlib,importlib.util,datetime
D=pathlib.Path(__file__).parent;s=importlib.util.spec_from_file_location('m',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
x=m.read(D/'manifest.json');tid='01a15c46-b8ad-7813-89bc-93f2b35e9c2d';assert x['successorThreadId']==tid
assert all(m.flow.get(cid)[1]['owner']==m.O for cid in x['claims']);assert m.read(m.P/'.flow-leases.json')=={}
for label,root in [('code',m.C),('planning',m.P)]:assert m.raw(pathlib.Path(m.h.git(root,'rev-parse','--path-format=absolute','--git-path','index')))==x['foreignIndexes'][label]
ack={'successorThreadId':tid,'hostId':'local','actualCompactions':0,'verifiedInitialCreateOutputAndSessionMeta':True,'CURRENT':923,'remaining':1077,'fullGoal':2000,'verified923Hashes':True,'verified2000Frozen':True,'exactPartition':True,'exact3OwnerAtACK':m.O,'leaseAtACK':{},'ownPermanentFilesByteEqual':58,'FOREIGNIndexesPreserved':True,'slices':16,'nativeACKTurn':'01a15c46-bb07-7ed3-a366-1dda2ddca79d','cursor':'e4f8773e-5539-4ec9-9189-fb78d988b9f2:6','readonlyACK':True}
m.write(D/'successor-ack.json',ack)
with m.flow.locked():m.flow.lease('acquire','planning',m.O)
try:
 with m.flow.locked():
  for cid in x['claims']:m.flow.release(cid,m.O)
 cpPath=pathlib.Path(x['canonicalCheckpoint']);cp=m.read(cpPath);assert cp['owner']==m.O;cp.update(owner=None,activeCoordinator=None,phase='EXACT3_RELEASED_PENDING_SUCCESSOR_CLAIM',pendingSuccessor=tid,ordinaryWorkActivated=False,next='Verified successor ACTIVATE, supported exact3 claim and durable takeover only');m.write(cpPath,cp)
 sp=m.P/'evidence/question-revision-process-v2/coordinator-state.json';st=m.read(sp);st.update(owner=None,activeCoordinator=None,phase='EXACT3_RELEASED_PENDING_SUCCESSOR_CLAIM',status='RELEASED_WAIT_SUCCESSOR_TAKEOVER',pendingSuccessor=tid,successorThreadId=tid,oldRootStoppedControl=True,ordinaryWorkActivated=False);m.write(sp,st)
 gp=m.P/'evidence/question-revision-process-v2/active-full2000-goal-01a1593a.json';g=m.read(gp);g.update(owner=None,pendingSuccessor=tid);m.write(gp,g)
 pp=m.P/'evidence/question-revision-process-v2/handoff-01a15c27.json';h=m.read(pp);h.update(phase='EXACT3_RELEASED_PENDING_SUCCESSOR_CLAIM',successorThreadId=tid,supportedExact3Released=True,oldRootStoppedControl=True,successorACK=ack);m.write(pp,h)
 paths=[cpPath,sp,gp,pp]+[m.flow.get(cid)[0] for cid in x['claims']];pc=m.h.save(m.P,'refs/heads/codex/question-revision-resume-20261014',[str(p.relative_to(m.P)) for p in paths],'Release exact3 claims after verified CURRENT923 successor readonly ACK',x['foreignIndexes']['planning']);print('RELEASE_P',pc)
finally:
 with m.flow.locked():m.flow.lease('release','planning',m.O)
assert all(m.flow.get(cid)[1]['owner'] is None for cid in x['claims']);assert m.read(m.P/'.flow-leases.json')=={}
for name in ['manifest.json','handoff-next.json']:
 h=m.read(D/name);h.update(phase='EXACT3_RELEASED_PENDING_SUCCESSOR_CLAIM',claimsOwner=None,leaseHeld=False,supportedReleaseP=pc,oldRootStoppedControl=True,successorStatus='VERIFIED_READONLY_ACK_PENDING_ACTIVATE');m.write(D/name,h)
print('RELEASE_C',m.savecode([D/'manifest.json',D/'handoff-next.json',D/'successor-ack.json',pathlib.Path(__file__)],'Preserve verified successor ACK and supported exact3 release; stop old control'))
for label,root in [('code',m.C),('planning',m.P)]:assert m.raw(pathlib.Path(m.h.git(root,'rev-parse','--path-format=absolute','--git-path','index')))==x['foreignIndexes'][label]
print('EXACT3_RELEASED_LEASE_EMPTY_FOREIGN_PRESERVED')
