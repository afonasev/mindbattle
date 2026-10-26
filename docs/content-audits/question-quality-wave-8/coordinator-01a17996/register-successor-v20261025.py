"""Bind exact native create result and register one readonly successor, no ownership transfer."""
import pathlib,json,importlib.util,hashlib,sys
D=pathlib.Path(__file__).parent
s=importlib.util.spec_from_file_location('m',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
x=m.read(D/'manifest.json');assert x['phase'].startswith('READY_FOR_READONLY_SUCCESSOR') and not any(a['stage'].startswith('START') for a in x['actors'].values())
S=sys.argv[1];result_path=pathlib.Path(sys.argv[2]);result=m.read(result_path)
assert not result.get('isError');created=json.loads(result['content'][0]['text'])
assert created['threadId']==S and created['hostId']=='local'
ps=list(pathlib.Path('/Users/eaafonasev/.codex/sessions').glob('**/*'+S+'.jsonl'));assert len(ps)==1
sr=[json.loads(l) for l in ps[0].open()];assert [r['payload']['id'] for r in sr if r.get('type')=='session_meta']==[S]
proof=D/'successor-create-native-proof.json'
m.write(proof,{'parent':m.O,'processRevision':'2026-10-25','supportedCreateResult':str(result_path),'supportedCreateResultSHA256':m.raw(result_path),'returnedSuccessorThreadId':S,'successorNativeJournal':str(ps[0]),'successorNativeSessionMetaId':S,'identityBasis':'Supported create_thread returned ID plus one exact matching runtime session metadata; no manual create journal reconstruction.'})
x=m.read(D/'manifest.json');assert all(m.flow.get(cid)[1]['owner']==m.O for cid in x['claims']);x.update(successorThreadId=S,successorNativeJournal=str(ps[0]),successorCreationProof=str(proof),successorNativeProof=str(proof),successorStatus='READONLY_BOOTSTRAP_REGISTERED')
for p in [D/'manifest.json',D/'handoff-next.json']:m.write(p,x)
cc=m.savecode([D/'manifest.json',D/'handoff-next.json',proof,result_path,pathlib.Path(__file__)],f'Register exact returned readonly successor CURRENT{x["CURRENT"]}');print('code',cc)
planningIndex=pathlib.Path(m.h.git(m.P,'rev-parse','--path-format=absolute','--git-path','index'));expectedPlanningIndex=m.raw(planningIndex)
assert expectedPlanningIndex==x['foreignIndexes']['planning']
with m.flow.locked():m.flow.lease('acquire','planning',m.O)
try:
 assert m.raw(planningIndex)==expectedPlanningIndex
 paths=[pathlib.Path(x['canonicalCheckpoint']),m.P/'evidence/question-revision-process-v2/coordinator-state.json',m.P/'evidence/question-revision-process-v2/active-full2000-goal-01a1593a.json']
 for p in paths:
  d=m.read(p);assert d['owner']==m.O;d.update(phase=x['phase'],pendingSuccessor=S,successorThreadId=S,successorStatus='READONLY_BOOTSTRAP_REGISTERED',successorCreationProof=str(proof));m.write(p,d)
 print('planning',m.h.save(m.P,'refs/heads/'+x['planningBranch'],[str(p.relative_to(m.P)) for p in paths],f'Register exact CURRENT{x["CURRENT"]} readonly successor without ownership transfer',expectedPlanningIndex))
finally:
 with m.flow.locked():m.flow.lease('release','planning',m.O)
for p in [D/'handoff-next.json',D/'manifest.json',pathlib.Path(x['canonicalCheckpoint'])]:assert m.read(p)['successorThreadId']==S
assert m.read(m.P/'.flow-leases.json')=={}
print('registeredSuccessor',S,'supportedIdentity',True,'ownersRemain',m.O,'leaseHeld',False)
