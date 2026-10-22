"""Preserve unchanged AUTHOR HOLD raw and native attempts; never qualify or credit."""
import pathlib,json,re,sys,importlib.util
D=pathlib.Path(__file__).parent
spec=importlib.util.spec_from_file_location('m',D/'owned-tools.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
order=int(sys.argv[1]);key=sys.argv[2];R=D/f'source-history-russia{order}';x=m.read(D/'manifest.json');actor=x['actors'][key]
native=pathlib.Path(actor['nativeJournal']);rows=[json.loads(l) for l in native.open()];assert rows[0]['payload']['id']==actor['threadId']
lastEvent=next(r['payload']['type'] for r in reversed(rows) if r.get('payload',{}).get('type') in ['task_started','task_complete']);assert lastEvent=='task_complete'
comp=sum(r['type']=='compacted' for r in rows);info=next(r['payload']['info'] for r in reversed(rows) if r.get('payload',{}).get('type')=='token_count')
a,sp,ps=[m.read(R/f) for f in ['candidate.json','sourceproof.json','peer-snapshot.json']];assert all(z['sourceNativeId']==actor['threadId'] for z in [a,sp,ps]);e=a['entries'][0]
q=m.read(m.C/'src/content/topics/history-russia.json')['questions'][order-1];assert e['status']=='HOLD' and e['beforeCard']==e['proposedCard']==q and m.sha(q)==e['beforeHash']==e['afterHash'] and e['sourceOrder']==order
v=sp['entries'][0]['fourFullPromptAnswerNoteAssessments'];assert len(v)==4
for z in v:
 answer=q['answers'][z['slot']];assert z['fullPrompt']==q['prompt'] and z['answer']==answer['text'] and z['note']==answer['note']
start=max(i for i,r in enumerate(rows,1) if r['type']=='event_msg' and r.get('payload',{}).get('type')=='task_started');calls=[]
for i,r in enumerate(rows,1):
 p=r.get('payload',{});s=re.sub(r'^// @exec:[^\n]*\n','',p.get('input','').lstrip())
 if p.get('type')=='custom_tool_call' and re.match(r'^(?:(?:const|let|var)\s+\w+\s*=\s*|text\(\s*)?await\s+tools\.web__run\s*\(',s):
  outputs=[(n,z) for n,z in enumerate(rows,1) if z.get('payload',{}).get('type')=='custom_tool_call_output' and z['payload'].get('call_id')==p['call_id']];assert len(outputs)==1;calls.append({'callLine':i,'call':p['input'],'resultLine':outputs[0][0]})
proof={'owner':m.O,'sourceNativeId':actor['threadId'],'nativeJournal':str(native),'actualCompactions':comp,'lastInput':info['last_token_usage']['input_tokens'],'modelWindow':info['model_context_window'],'packet':str(R),'rawFileSHA256':{str(p.relative_to(R)):m.raw(p) for p in R.rglob('*') if p.is_file()},'status':'HOLD','beforeHash':e['beforeHash'],'afterHash':e['afterHash'],'currentTaskStartLine':start,'networkCalls':[z for z in calls if z['callLine']>start],'priorTaskNetworkCalls':[z for z in calls if z['callLine']<start],'qualityCredit':0,'noQualification':True,'unapplied':True,'noIndependentInitial':True,'originalPreservationFailureRetained':str(D/f'source{order}-original-format-diagnostics.json'),'missingTripleHashes':[z['slot'] for z in v if 'tripleSHA256' not in z]}
actor.update(actualCompactions=comp,lastTaskEvent=lastEvent,lastInput=proof['lastInput'],modelWindow=proof['modelWindow'],stage=f'IDLE_AFTER_SOURCE{order}_AUTHORHOLD_UNQUALIFIED',nativePreflightVerifiedBy=m.O)
p=D/f'history-russia{order}-native-proof.json';m.write(p,proof);m.write(D/'manifest.json',x);print(m.savecode([p,D/'manifest.json',pathlib.Path(__file__),D/f'source{order}-original-format-diagnostics.json',*[p for p in R.rglob('*') if p.is_file()]],f'Preserve SOURCE{order} unchanged unqualified AUTHORHOLD and original format FAIL'))
print(json.dumps({k:proof[k] for k in ['actualCompactions','lastInput','missingTripleHashes','qualityCredit']},ensure_ascii=False))
