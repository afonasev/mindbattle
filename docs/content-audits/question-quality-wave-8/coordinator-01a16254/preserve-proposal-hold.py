"""Preserve an unqualified HOLD proposal unchanged; never apply or qualify it."""
import pathlib, json, re, sys, importlib.util
D = pathlib.Path(__file__).parent
s = importlib.util.spec_from_file_location('owned', D/'owned-tools.py')
m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
order = int(sys.argv[1]); key = sys.argv[2]
x = m.read(D/'manifest.json'); actor = x['actors'][key]
R = D/f'source-history-russia{order}'
native = pathlib.Path(actor['nativeJournal'])
rows = [json.loads(line) for line in native.open()]
assert next(r['payload']['id'] for r in rows if r['type']=='session_meta') == actor['threadId']
assert next(r['payload']['type'] for r in reversed(rows) if r.get('payload',{}).get('type') in ['task_started','task_complete']) == 'task_complete'
candidate, sp, ps = [m.read(R/name) for name in ['candidate.json','sourceproof.json','peer-snapshot.json']]
assert all(v['sourceNativeId']==actor['threadId'] for v in [candidate,sp,ps])
e = candidate['entries'][0]
q = m.read(m.C/'src/content/topics/history-russia.json')['questions'][order-1]
assert e['status']=='HOLD' and e['sourceOrder']==order and e['id']==q['id']
assert e['beforeCard']==q and m.sha(q)==e['beforeHash'] and m.sha(e['proposedCard'])==e['afterHash']
cp = m.read(pathlib.Path(x['canonicalCheckpoint']))
assert q['id'] in cp['currentRemainingIds'] and q['id'] not in cp['currentEligibleCompletedIds']
start = max(i for i,r in enumerate(rows,1) if r['type']=='event_msg' and r.get('payload',{}).get('type')=='task_started')
calls = []
for i,r in enumerate(rows,1):
    p=r.get('payload',{}); text=re.sub(r'^// @exec:[^\n]*\n','',p.get('input','').lstrip())
    if p.get('type')=='custom_tool_call' and re.match(r'^(?:(?:const|let|var)\s+\w+\s*=\s*|text\(\s*)?await\s+tools\.web__run\s*\(',text):
        outputs=[j for j,z in enumerate(rows,1) if z.get('payload',{}).get('type')=='custom_tool_call_output' and z['payload'].get('call_id')==p['call_id']]
        assert len(outputs)==1
        calls.append({'callLine':i,'call':p['input'],'resultLine':outputs[0]})
info=next(r['payload']['info'] for r in reversed(rows) if r.get('payload',{}).get('type')=='token_count')
comp=sum(r['type']=='compacted' for r in rows)
proof={'owner':m.O,'sourceNativeId':actor['threadId'],'nativeJournal':str(native),'actualCompactions':comp,'lastInput':info['last_token_usage']['input_tokens'],'modelWindow':info['model_context_window'],'currentTaskStartLine':start,'networkCalls':[c for c in calls if c['callLine']>start],'priorTaskNetworkCalls':[c for c in calls if c['callLine']<start],'rawFileSHA256':{str(p.relative_to(R)):m.raw(p) for p in R.rglob('*') if p.is_file()},'status':'HOLD','qualityCredit':0,'noQualification':True,'unapplied':True,'noIndependentInitial':True,'beforeHash':e['beforeHash'],'unappliedProposalHash':e['afterHash'],'limitations':'Proposal retained as author raw only. Original preservation failure retained; projected rows are not full-card sameTopic questions. No normalization or quality adoption.'}
pp=D/f'history-russia{order}-native-proof.json';m.write(pp,proof)
actor.update(stage=f'IDLE_AFTER_SOURCE{order}_AUTHORHOLD_UNQUALIFIED',actualCompactions=comp,lastTaskEvent='task_complete',lastInput=proof['lastInput'],modelWindow=proof['modelWindow'])
x[f'pendingHistoryRussia{order}']={'id':q['id'],'status':'AUTHORHOLD_UNQUALIFIED_UNAPPLIED','qualityCredit':0,'applied':False,'beforeHash':e['beforeHash'],'unappliedProposalHash':e['afterHash'],'rawPacket':str(R),'nativeProof':str(pp),'noIndependentInitial':True,'noQA':True,'sourceNetworkAccounting':str(D/f'history-russia{order}-network-accounting.json')}
x['sourceActorKeys']=[k for k in x['sourceActorKeys'] if k!=key]
m.write(D/'manifest.json',x)
files=[D/'manifest.json',pp,pathlib.Path(__file__),D/f'source{order}-original-format-diagnostics.json',*[p for p in R.rglob('*') if p.is_file()]]
print(m.savecode(files,f'Preserve SOURCE{order} unqualified HOLD proposal and original diagnostics without application'))
print(json.dumps({'sourceOrder':order,'qualityCredit':0,'unapplied':True,'rawUnchanged':True,'actualCompactions':comp}))
