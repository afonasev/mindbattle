"""Bind exact native create result and register one readonly successor, no ownership transfer."""
import pathlib,json,importlib.util,hashlib
D=pathlib.Path(__file__).parent
s=importlib.util.spec_from_file_location('m',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
S='01a15f2c-15a4-76b0-bc94-c39a412225c1';native=pathlib.Path('/Users/eaafonasev/.codex/sessions/2026/10/21/rollout-2026-10-21T20-19-29-01a15f0b-c787-7633-949f-a78a69b9de2d.jsonl');rr=[json.loads(l) for l in native.open()]
c=[(n,r['payload']) for n,r in enumerate(rr,1) if r.get('payload',{}).get('type')=='custom_tool_call' and r['payload'].get('input','').startswith('text(await tools.mcp__codex_app__create_thread({title:"coordinate: ревизия вопросов exact2000"')];assert len(c)==1
line,call=c[0];outs=[(n,r) for n,r in enumerate(rr,1) if r.get('payload',{}).get('type')=='custom_tool_call_output' and r['payload'].get('call_id')==call['call_id']];assert len(outs)==1
ids=[]
def walk(v):
 if isinstance(v,dict):
  for k,a in v.items():
   if k=='threadId':ids.append(a)
   else:walk(a)
 elif isinstance(v,list):
  for a in v:walk(a)
 elif isinstance(v,str):
  try:walk(json.loads(v))
  except (ValueError,TypeError):pass
walk(outs[0][1]['payload']['output']);assert set(ids)=={S}
ps=list(pathlib.Path('/Users/eaafonasev/.codex/sessions').rglob('*'+S+'.jsonl'));assert len(ps)==1;sr=[json.loads(l) for l in ps[0].open()];assert next(r['payload']['id'] for r in sr if r['type']=='session_meta')==S
proof=D/'successor-create-native-proof.json';m.write(proof,{'parent':m.O,'parentNative':str(native),'createCallLine':line,'createCallId':call['call_id'],'createInputSHA256':hashlib.sha256(call['input'].encode()).hexdigest(),'exactOriginalResultLine':outs[0][0],'exactOriginalResultRecord':outs[0][1],'returnedSuccessorThreadId':S,'successorNativeJournal':str(ps[0]),'successorNativeSessionMetaId':S,'noEnvOrTimestampGuess':True})
x=m.read(D/'manifest.json');assert all(m.flow.get(cid)[1]['owner']==m.O for cid in x['claims']);x.update(successorThreadId=S,successorNativeJournal=str(ps[0]),successorCreationProof=str(proof),successorNativeProof=str(proof),successorStatus='READONLY_BOOTSTRAP_REGISTERED')
for p in [D/'manifest.json',D/'handoff-next.json']:m.write(p,x)
cc=m.savecode([D/'manifest.json',D/'handoff-next.json',proof,pathlib.Path(__file__)],'Register exact returned readonly successor CURRENT949');print('code',cc)
with m.flow.locked():m.flow.lease('acquire','planning',m.O)
try:
 paths=[pathlib.Path(x['canonicalCheckpoint']),m.P/'evidence/question-revision-process-v2/coordinator-state.json',m.P/'evidence/question-revision-process-v2/active-full2000-goal-01a1593a.json']
 for p in paths:
  d=m.read(p);assert d['owner']==m.O;d.update(phase=x['phase'],pendingSuccessor=S,successorThreadId=S,successorStatus='READONLY_BOOTSTRAP_REGISTERED',successorCreationProof=str(proof));m.write(p,d)
 print('planning',m.h.save(m.P,'refs/heads/'+x['planningBranch'],[str(p.relative_to(m.P)) for p in paths],'Register exact CURRENT949 readonly successor without ownership transfer',x['foreignIndexes']['planning']))
finally:
 with m.flow.locked():m.flow.lease('release','planning',m.O)
for p in [D/'handoff-next.json',D/'manifest.json',pathlib.Path(x['canonicalCheckpoint'])]:assert m.read(p)['successorThreadId']==S
assert m.read(m.P/'.flow-leases.json')=={}
print('registeredSuccessor',S,'call_id',call['call_id'],'callLine',line,'ownersRemain',m.O,'leaseHeld',False)
