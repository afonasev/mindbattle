"""Preserve raw READY against exact original baseline and one known applied delta.
No normalization, qualification, catalog write or semantic decision.
"""
import pathlib,json,importlib.util,sys,re,subprocess
D=pathlib.Path(__file__).parent
s=importlib.util.spec_from_file_location('m',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
order,changed=map(int,sys.argv[1:3]);x=m.read(D/'manifest.json');topic=x['activeRoute']['topicId'];R=D/f'source-{topic}{order}';task=m.read(D/f'source-{topic}{order}-task.json');a=x['actors'][f'author{order}'];uid=a['threadId']
native=pathlib.Path(a['nativeJournal']);nr=[json.loads(l) for l in native.open()]
assert [r['payload']['id'] for r in nr if r['type']=='session_meta']==[uid]
assert next(r['payload']['type'] for r in reversed(nr) if r.get('payload',{}).get('type') in ['task_started','task_complete'])=='task_complete'
ca,sp,ps=[m.read(R/n) for n in ['candidate.json','sourceproof.json','peer-snapshot.json']];assert all(v['sourceNativeId']==uid and v['cycle']==0 for v in [ca,sp,ps]);e=ca['entries'][0]
assert e['status']=='READY_FOR_INDEPENDENT_REVIEW' and e['sourceOrder']==order and m.sha(e['beforeCard'])==e['beforeHash'] and m.sha(e['proposedCard'])==e['afterHash']
report_name=sys.argv[3] if len(sys.argv)>3 else f'qualified-source-{topic}{changed}-apply.json'
assert pathlib.Path(report_name).name==report_name
tp=m.C/f'src/content/topics/{topic}.json';before_bytes=subprocess.check_output(['git','-C',str(m.C),'show',task['baselineCode']+':'+str(tp.relative_to(m.C))]);old=json.loads(before_bytes);live=m.read(tp);app=m.read(D/report_name)['applied'][0]
assert [i for i,(b,q) in enumerate(zip(old['questions'],live['questions']),1) if b!=q]==[changed]
assert old['questions'][changed-1]==app['beforeCard'] and live['questions'][changed-1]==app['proposedCard']
assert old['questions'][order-1]==live['questions'][order-1]==e['beforeCard']
same=ps.get('sameTopicMAIN')
inventory_alias=None
if same is None:
 ip=pathlib.Path(ps['sourceInventoryPath']);assert ip.is_relative_to(R) and str(ip)==sp['sourceInventoryPath']
 assert m.raw(ip)==ps['sourceInventorySHA256']==sp['sourceInventorySHA256']
 inv=m.read(ip);same=inv['sameTopicMAIN']
 assert inv['globalMAIN']==ps['globalMAIN'] and inv['actualCurrentPeers']==ps['actualCurrentPeers']
 inventory_alias={'path':str(ip),'rawSHA256':m.raw(ip),'originalSameTopicContainerAbsent':True,'operation':'Read original same-author explicitly SHA-bound complete inventory; no raw hydration or new judgment.'}
assert same['questions']==old['questions']
assert same['fileSHA256']==__import__('hashlib').sha256(before_bytes).hexdigest()
assert len(ps['actualCurrentPeers'])==100 and [p['sourceOrder'] for p in ps['actualCurrentPeers']]==list(range(1,101))
assert [p['card'] for p in ps['actualCurrentPeers']]==old['questions']
assert all(p['id']==p['card']['id'] and p['topicId']==topic and m.sha(p['card'])==p['sha256'] for p in ps['actualCurrentPeers'])
bindings=ps['globalMAIN']['allCurrentFileByteBindings'];files=sorted((m.C/'src/content/topics').glob('*.json'));assert len(bindings)==len(files)==110
rows=[]
for p,b in zip(files,bindings):
 assert b['path']==str(p.relative_to(m.C))
 assert b['sha256']==(__import__('hashlib').sha256(before_bytes).hexdigest() if p==tp else m.raw(p))
 t=old if p==tp else m.read(p)
 rows.extend({'topicId':t['id'],'id':q['id'],'prompt':q['prompt'],'answers':[v['text'] for v in q['answers']],'correctIndex':q['correctIndex']} for q in t['questions'])
assert len(rows)==11000 and rows==ps['globalMAIN']['rows'] and m.sha(rows)==ps['globalMAIN']['rowsCanonicalSHA256']
for src in sp['rawSources']:assert m.raw(m.C/src['path'])==src['sha256']
info=next(r['payload']['info'] for r in reversed(nr) if r.get('payload',{}).get('type')=='token_count');calls=[]
for i,r in enumerate(nr,1):
 p=r.get('payload',{});inp=re.sub(r'^// @exec:[^\n]*\n','',p.get('input','').lstrip())
 if p.get('type')=='custom_tool_call' and re.match(r'^(?:(?:const|let|var)\s+\w+\s*=\s*|text\(\s*)?await\s+tools\.web__run\s*\(',inp):
  outputs=[j for j,z in enumerate(nr,1) if z.get('payload',{}).get('type')=='custom_tool_call_output' and z['payload'].get('call_id')==p['call_id']];assert len(outputs)==1;calls.append({'callLine':i,'call':p['input'],'resultLine':outputs[0]})
start=max(i for i,r in enumerate(nr,1) if r['type']=='event_msg' and r.get('payload',{}).get('type')=='task_started')
proof={'owner':m.O,'sourceNativeId':uid,'nativeJournal':str(native),'actualCompactions':sum(r['type']=='compacted' for r in nr),'lastInput':info['last_token_usage']['input_tokens'],'modelWindow':info['model_context_window'],'packet':str(R),'rawFileSHA256':{str(p.relative_to(R)):m.raw(p) for p in R.rglob('*') if p.is_file()},'status':e['status'],'beforeHash':e['beforeHash'],'afterHash':e['afterHash'],'currentTaskStartLine':start,'networkCalls':[c for c in calls if c['callLine']>start],'priorTaskNetworkCalls':[c for c in calls if c['callLine']<start],'qualityCredit':0,'knownConcurrentDeltaPreservationOnly':{'changedOrder':changed,'baseline':task['baselineCode'],'actualBeforeBody':app['beforeCard'],'actualAppliedBody':app['proposedCard'],'allOtherCardsAnd109BindingsExact':True,'noQualification':True,'noSemanticJudgment':True}}
proof['explicitInventoryReadBinding']=inventory_alias
proof['knownConcurrentDeltaPreservationOnly']['applyReport']=str(D/report_name)
p=D/f'{topic}{order}-native-proof.json';assert not p.exists();m.write(p,proof);a.update(stage=f'IDLE_AFTER_SOURCE{order}_READY_PENDING_CONCURRENT_ALIAS',actualCompactions=proof['actualCompactions'],lastTaskEvent='task_complete',lastInput=proof['lastInput'],modelWindow=proof['modelWindow']);m.write(D/'manifest.json',x)
print(m.savecode([p,D/'manifest.json',pathlib.Path(__file__),*[p for p in R.rglob('*') if p.is_file()]],f'Freeze raw SOURCE{order} against exact baseline and known concurrent{changed} delta'))
print({'rawReadyPreserved':True,'networkTotalCalls':len(calls),'qualityCredit':0,'unqualified':True})
