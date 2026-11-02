"""Preserve unchanged AUTHOR HOLD raw and native attempts; never qualify or credit."""
import pathlib,json,re,sys,importlib.util
D=pathlib.Path(__file__).parent
spec=importlib.util.spec_from_file_location('m',D/'owned-tools.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
order=int(sys.argv[1]);key=sys.argv[2];R=D/f'source-fashion{order}';x=m.read(D/'manifest.json');actor=x['actors'][key]
native=pathlib.Path(actor['nativeJournal']);rows=[json.loads(l) for l in native.open()];assert rows[0]['payload']['id']==actor['threadId']
lastEvent=next(r['payload']['type'] for r in reversed(rows) if r.get('payload',{}).get('type') in ['task_started','task_complete']);assert lastEvent=='task_complete'
comp=sum(r['type']=='compacted' for r in rows);info=next(r['payload']['info'] for r in reversed(rows) if r.get('payload',{}).get('type')=='token_count')
a,sp,ps=[m.read(R/f) for f in ['candidate.json','sourceproof.json','peer-snapshot.json']];e=a['entries'][0]
assert all(z['sourceNativeId']==actor['threadId'] for z in [a,sp])
missing_peer_headers=[key for key in ['sourceNativeId','topicId','cycle'] if key not in ps]
for key in ['sourceNativeId','topicId','cycle']:
 if key in ps:assert ps[key]==a[key]
if missing_peer_headers:
 assert '--unqualified-peer-inventory' in sys.argv[3:] and e['status']=='HOLD', 'Missing peer headers cannot qualify a SOURCE packet'
q=m.read(m.C/'src/content/topics/fashion.json')['questions'][order-1]
assert e['status']=='HOLD' and e['beforeCard']==q and m.sha(q)==e['beforeHash'] and e['sourceOrder']==order
metadata_only='--metadata-proposal-only' in sys.argv[3:]
if metadata_only:
 proposed=json.loads(json.dumps(e['proposedCard'],ensure_ascii=False));assert set(proposed)==set(q) and proposed['source']!=q['source'] and m.sha(proposed)==e['afterHash']
 proposed['source']=q['source'];assert proposed==q, 'Explicit unqualified metadata-only proposal preservation cannot alter any text or frozen field'
else:assert e['proposedCard']==q and e['afterHash']==e['beforeHash']
v=sp['entries'][0]['fourFullPromptAnswerNoteAssessments'];assert len(v)==4
for z in v:
 answer=q['answers'][z['slot']];assert z['fullPrompt']==q['prompt'] and z['answer']==answer['text'] and z['note']==answer['note']
start=max(i for i,r in enumerate(rows,1) if r['type']=='event_msg' and r.get('payload',{}).get('type')=='task_started');calls=[]
for i,r in enumerate(rows,1):
 p=r.get('payload',{});s=re.sub(r'^// @exec:[^\n]*\n','',p.get('input','').lstrip())
 if p.get('type')=='custom_tool_call' and re.match(r'^(?:(?:const|let|var)\s+\w+\s*=\s*|text\(\s*)?await\s+tools\.web__run\s*\(',s):
  outputs=[(n,z) for n,z in enumerate(rows,1) if z.get('payload',{}).get('type')=='custom_tool_call_output' and z['payload'].get('call_id')==p['call_id']];assert len(outputs)==1;calls.append({'callLine':i,'call':p['input'],'resultLine':outputs[0][0]})
proof={'owner':m.O,'sourceNativeId':actor['threadId'],'nativeJournal':str(native),'actualCompactions':comp,'lastInput':info['last_token_usage']['input_tokens'],'modelWindow':info['model_context_window'],'packet':str(R),'rawFileSHA256':{str(p.relative_to(R)):m.raw(p) for p in R.rglob('*') if p.is_file()},'status':'HOLD','beforeHash':e['beforeHash'],'afterHash':e['afterHash'],'currentTaskStartLine':start,'networkCalls':[z for z in calls if z['callLine']>start],'priorTaskNetworkCalls':[z for z in calls if z['callLine']<start],'qualityCredit':0,'noQualification':True,'metadataOnlyUnappliedProposalPreserved':metadata_only,'unapplied':True,'noIndependentInitial':True,'originalPreservationFailureRetained':str(D/f'source{order}-original-format-diagnostics.json'),'missingTripleHashes':[z['slot'] for z in v if 'tripleSHA256' not in z]}
actor.update(actualCompactions=comp,lastTaskEvent=lastEvent,lastInput=proof['lastInput'],modelWindow=proof['modelWindow'],stage=f'IDLE_AFTER_SOURCE{order}_AUTHORHOLD_UNQUALIFIED',nativePreflightVerifiedBy=m.O)
proof.update(missingPeerHeaderFields=missing_peer_headers,unqualifiedPeerInventoryOnly=bool(missing_peer_headers),rawPeerHeaderNotInvented=True)
diagnostic=D/f'source{order}-original-format-diagnostics.json'
if not diagnostic.exists():proof['originalPreservationFailureRetained']=None
p=D/f'fashion{order}-native-proof.json';m.write(p,proof);m.write(D/'manifest.json',x);print(m.savecode([p,D/'manifest.json',pathlib.Path(__file__),*([diagnostic] if diagnostic.exists() else []),*[p for p in R.rglob('*') if p.is_file()]],f'Preserve SOURCE{order} unchanged unqualified AUTHORHOLD'))
print(json.dumps({k:proof[k] for k in ['actualCompactions','lastInput','missingTripleHashes','qualityCredit']},ensure_ascii=False))
