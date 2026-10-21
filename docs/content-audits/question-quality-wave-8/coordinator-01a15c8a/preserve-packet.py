"""Mechanical preservation of one native SOURCE packet, without quality credit."""
import pathlib, json, importlib.util, sys
D=pathlib.Path(__file__).parent
s=importlib.util.spec_from_file_location('owned',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
order=int(sys.argv[1]);actor_key=sys.argv[2];name=sys.argv[3] if len(sys.argv)>3 else f'source-polar{order}'
R=D/name;x=m.read(D/'manifest.json');actor=x['actors'][actor_key];uid=actor['threadId'];native=pathlib.Path(actor['nativeJournal']);journal=[json.loads(l) for l in native.open()]
assert journal[0]['payload']['id']==uid
comp=sum(o['type']=='compacted' for o in journal);last=next(o['payload']['info'] for o in reversed(journal) if o.get('payload',{}).get('type')=='token_count')
a,sp,ps=[m.read(R/f) for f in ['candidate.json','sourceproof.json','peer-snapshot.json']]
assert all(v['sourceNativeId']==uid for v in [a,sp,ps]);assert len(a['entries'])==len(sp['entries'])==1
e=a['entries'][0];q=m.read(m.C/'src/content/topics/polar-regions.json')['questions'][order-1]
assert e['sourceOrder']==order and e['beforeCard']==q and m.sha(q)==e['beforeHash'] and m.sha(e['proposedCard'])==e['afterHash']
assert e['id']==q['id'] and e['status'] in ['HOLD','READY_FOR_INDEPENDENT_REVIEW','READY_FOR_SAME_READER_FINAL']
cp=m.read(pathlib.Path(x['canonicalCheckpoint']));f=next(z for z in cp['selectedCards'] if z['questionId']==e['id']);assert q['difficulty']==e['proposedCard']['difficulty']==f['difficulty'] and q['correctIndex']==e['proposedCard']['correctIndex']==f['correctIndex']
def groups(c):return {'prompt_ordered_answers_key':{'prompt':c['prompt'],'answers':[v['text'] for v in c['answers']],'correctIndex':c['correctIndex']},'explanation':c['explanation'],**{'note'+str(k):v['note'] for k,v in enumerate(c['answers'])}}
bg,ag=groups(q),groups(e['proposedCard']);entry=sp['entries'][0];assert entry['id']==e['id'] and len(entry['literalGroups'])==6 and len(entry['fourFullPromptAnswerNoteAssessments'])==4
for g in entry['literalGroups']:assert g['literal']==ag[g['group']] and g['literalSHA256']==m.sha(g['literal'])
for k,fg in e['fieldGroups'].items():assert fg['beforeCanonicalSHA256']==m.sha(bg[k]) and fg['afterCanonicalSHA256']==m.sha(ag[k])
for v in entry['fourFullPromptAnswerNoteAssessments']:
 k=v['slot'];tr={'prompt':e['proposedCard']['prompt'],'answer':e['proposedCard']['answers'][k]['text'],'note':e['proposedCard']['answers'][k]['note']};assert tr=={'prompt':v['fullPrompt'],'answer':v['answer'],'note':v['note']} and m.sha(tr)==v['tripleSHA256']
raw_checks=[]
for source in sp['rawSources']:
 p=pathlib.Path(source['path']);p=p if p.is_absolute() else m.C/p;assert m.raw(p)==source['sha256'];cap=m.read(p) if p.suffix=='.json' else None
 if isinstance(cap,dict) and 'originalRecord' in cap:
  jp=pathlib.Path(cap['nativeJournal'])
  if not jp.exists():
   matches=list(pathlib.Path('/Users/eaafonasev/.codex/archived_sessions').glob('*'+cap['sourceNativeId']+'.jsonl'));assert len(matches)==1;jp=matches[0]
  record=json.loads(jp.read_text().splitlines()[cap['nativeRecordLine']-1]);assert record==cap['originalRecord']
  raw_checks.append({'path':str(p),'nativeId':cap['sourceNativeId'],'nativeLine':cap['nativeRecordLine'],'originalRecordExact':True})
cat={};rows=[]
for path in sorted((m.C/'src/content/topics').glob('*.json')):
 t=m.read(path)
 for card in t['questions']:
  cat[card['id']]=card;rows.append({'topicId':t['id'],'id':card['id'],'prompt':card['prompt'],'answers':[a['text'] for a in card['answers']],'correctIndex':card['correctIndex']})
assert len(rows)==11000 and m.sha(rows)==ps['globalMAIN']['rowsCanonicalSHA256']
for b in ps['globalMAIN']['allCurrentFileByteBindings']:assert m.raw(m.C/b['path'])==b['sha256']
assert ps['sameTopicMAIN']['questions']==m.read(m.C/'src/content/topics/polar-regions.json')['questions']
for p in ps['actualCurrentPeers']:assert m.sha(p['card'])==p.get('sha256',p.get('canonicalSHA256')) and p['card']==cat[p['id']]

proof={'owner':m.O,'sourceNativeId':uid,'nativeJournal':str(native),'actualCompactions':comp,'lastInput':last['last_token_usage']['input_tokens'],'modelWindow':last['model_context_window'],'packet':str(R),'rawFileSHA256':{str(p.relative_to(R)):m.raw(p) for p in R.rglob('*') if p.is_file()},'status':e['status'],'beforeHash':e['beforeHash'],'afterHash':e['afterHash'],'sixGroups':6,'fourVariants':4,'nativeCaptureBindings':raw_checks,'qualityCredit':0,'networkCalls':[]}
for i,o in enumerate(journal,1):
 p=o.get('payload',{})
 if o['type']=='response_item' and p.get('type')=='custom_tool_call' and 'await tools.web__run(' in p.get('input',''):
  callid=p['call_id'];result=next(((j,z) for j,z in enumerate(journal,1) if z.get('payload',{}).get('type')=='custom_tool_call_output' and z['payload'].get('call_id')==callid),None)
  proof['networkCalls'].append({'callLine':i,'call':p['input'],'resultLine':result[0] if result else None})
actor.update(actualCompactions=comp,lastInput=proof['lastInput'],modelWindow=proof['modelWindow'],lastTaskEvent='task_complete',stage=f'IDLE_AFTER_SOURCE{order}_{e["status"]}',nativePreflightVerifiedBy=m.O)
proof_path=D/(name.replace('source-','')+'-native-proof.json');m.write(proof_path,proof);m.write(D/'manifest.json',x)
print(m.savecode([p for p in R.rglob('*') if p.is_file()]+[proof_path,D/'manifest.json',pathlib.Path(__file__)],f'Preserve native SOURCE{order} {e["status"]} exact packet without quality credit'))
print(json.dumps({k:proof[k] for k in ['status','actualCompactions','lastInput','modelWindow','networkCalls']},ensure_ascii=False))
