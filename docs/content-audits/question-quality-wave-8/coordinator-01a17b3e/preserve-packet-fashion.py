"""Mechanical preservation of one native SOURCE packet, without quality credit."""
import pathlib, json, importlib.util, sys, re
D=pathlib.Path(__file__).parent
s=importlib.util.spec_from_file_location('owned',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
order=int(sys.argv[1]);actor_key=sys.argv[2];name=sys.argv[3] if len(sys.argv)>3 else f'source-fashion{order}'
baseline=sys.argv[sys.argv.index('--baseline')+1] if '--baseline' in sys.argv else None
def topic_read(path):
 if baseline and str(path).startswith(str(m.C/'src/content/topics')):
  return json.loads(m.h.git(m.C,'show',baseline+':'+str(path.relative_to(m.C))))
 return m.read(path)
R=D/name;x=m.read(D/'manifest.json');actor=x['actors'][actor_key];uid=actor['threadId'];native=pathlib.Path(actor['nativeJournal']);journal=[json.loads(l) for l in native.open()]
assert journal[0]['payload']['id']==uid
comp=sum(o['type']=='compacted' for o in journal);last=next(o['payload']['info'] for o in reversed(journal) if o.get('payload',{}).get('type')=='token_count')
a,sp,ps=[m.read(R/f) for f in ['candidate.json','sourceproof.json','peer-snapshot.json']]
m.alias_source80_cycle1_single_peer_entry(a,sp,ps,R)
m.alias_source26_cycle1_canonical_readiness(a,sp,ps,R)
m.alias_source23_cycle1_self_preimage(a,sp,ps,R)
m.alias_source22_peer_header(a,sp,ps,R)
m.alias_source9_global_field_names(a,sp,ps,R)
m.alias_source86_single_peer_entry(a,sp,ps,R)
m.alias_source83_cycle1_copied_same_topic(a,sp,ps,R)
m.alias_source74_cycle1_own_global_metadata(a,sp,ps,R)
m.alias_explicit_global_inventory_file(a,sp,ps,R)
m.alias_explicit_owned_packet_source_paths(a,sp,R)
m.alias_source96_distinct99_preimage(a,sp,ps,R)
m.alias_explicit_fresh_inventory_context(a,sp,ps,R)
m.alias_exact_videogame2_distinct_peers(a,sp,ps,R)
m.alias_explicit_inventory_binding(a,sp,ps,R)
m.alias_explicit_complete_inventory_paths(a,sp,ps,R)
m.alias_same_topic_current_peer_container(a,sp,ps,R)
m.alias_explicit_root_candidate(a,sp,ps,R)
assert all(v['sourceNativeId']==uid for v in [a,sp,ps])
m.alias_source77_own_prior_application(a,sp,ps,R)
m.alias_source83_clarified_literals(a,sp,ps,R)
m.alias_source83_cycle1_redundant_snapshot(a,sp,ps,R)
m.alias_source84_cycle1_variant_names(a,sp,ps,R)
m.alias_single_sourceproof_entry(a,sp)
m.alias_source31_root_entry_identity(a,sp,R)
m.alias_explicit_peer_inventory_projection(a,sp,ps,R)
assert len(a['entries'])==len(sp['entries'])==1
m.alias_serialized_prompt_group(a,sp)
m.alias_full_prompt_answer_concatenation(a,sp)
m.alias_full_body_wrapper_digests(ps,R)
e=a['entries'][0];q=topic_read(m.C/'src/content/topics/fashion.json')['questions'][order-1]
assert e['sourceOrder']==order and e['beforeCard']==q and m.sha(q)==e['beforeHash'] and m.sha(e['proposedCard'])==e['afterHash']
assert e['id']==q['id'] and e['status'] in ['HOLD','READY_FOR_INDEPENDENT_REVIEW','READY_FOR_SAME_READER_FINAL']
cp=m.read(pathlib.Path(x['canonicalCheckpoint']));f=next(z for z in cp['selectedCards'] if z['questionId']==e['id']);assert q['difficulty']==e['proposedCard']['difficulty']==f['difficulty'] and q['correctIndex']==e['proposedCard']['correctIndex']==f['correctIndex']
def groups(c):return {'prompt_ordered_answers_key':{'prompt':c['prompt'],'answers':[v['text'] for v in c['answers']],'correctIndex':c['correctIndex']},'explanation':c['explanation'],**{'note'+str(k):v['note'] for k,v in enumerate(c['answers'])}}
bg,ag=groups(q),groups(e['proposedCard']);entry=sp['entries'][0];literal_groups=entry.get('literalGroups',entry.get('sixLiteralGroups'));assert entry['id']==e['id'] and len(literal_groups)==6 and len(entry['fourFullPromptAnswerNoteAssessments'])==4
for g in literal_groups:
 if g['group']=='prompt_ordered_answers_key' and isinstance(g['literal'],str):
  assert g['literal']==e['proposedCard']['prompt']
  assert g['literalSHA256'] in [m.sha(g['literal']),__import__('hashlib').sha256(g['literal'].encode()).hexdigest()]
  assert e['fieldGroups'][g['group']]['afterCanonicalSHA256']==m.sha(ag[g['group']])
 else:assert g['literal']==ag[g['group']] and g['literalSHA256']==m.sha(g['literal'])
for k,fg in e['fieldGroups'].items():assert fg['beforeCanonicalSHA256']==m.sha(bg[k]) and fg['afterCanonicalSHA256']==m.sha(ag[k])
triple_checks=[]
for v in entry['fourFullPromptAnswerNoteAssessments']:
 k=v['slot'];tr={'prompt':e['proposedCard']['prompt'],'answer':e['proposedCard']['answers'][k]['text'],'note':e['proposedCard']['answers'][k]['note']};assert tr=={'prompt':v['fullPrompt'],'answer':v['answer'],'note':v['note']}
 if m.sha(tr)!=v['tripleSHA256']:
  alternatives={'fullPromptKey':{'fullPrompt':tr['prompt'],'answer':tr['answer'],'note':tr['note']},'orderedThreeLiteralList':[tr['prompt'],tr['answer'],tr['note']]}
  matched=[name for name,value in alternatives.items() if m.sha(value)==v['tripleSHA256']]
  assert len(matched)==1
  triple_checks.append({'slot':k,'originalTripleSHA256':v['tripleSHA256'],'originalRepresentation':matched[0],'canonicalPromptKeyTripleSHA256':m.sha(tr),'operation':'Verified exact same ordered full prompt/answer/note literals against candidate and six groups; representation only, immutable raw and grounds unchanged'})
raw_checks=[]
for source in sp['rawSources']:
 p=pathlib.Path(source['path']);p=p if p.is_absolute() else m.C/p
 if not p.exists():
  assert source['path'].startswith('content-audits/')
  alt=m.C/'docs'/source['path'];assert alt.is_file() and alt.is_relative_to(R/'raw')
  assert m.raw(alt)==source['sha256']
  exact=m.read(alt);assert exact['sourceNativeId']==uid and exact['url']==source['url']
  assert journal[exact['nativeRecordLine']-1]==exact['originalRecord']
  body=exact
  for key in source['completeOutputPointer'].split('/')[1:]:body=body[int(key)] if isinstance(body,list) else body[key]
  assert isinstance(body,str) and source['url'] in body
  assert __import__('hashlib').sha256(body.encode()).hexdigest()==source['completeOutputSHA256']==exact['completeOutputSHA256']
  raw_checks.append({'originalMissingDocsPath':str(p),'resolvedOriginalCapture':str(alt),'fileSHA256':m.raw(alt),'nativeRecordExact':True,'bodyURLAndSHAExact':True,'operation':'Read-only path alias for missing docs prefix; original author sourceproof unchanged.'})
  p=alt
 if 'sha256' not in source:
  assert 'fileSHA256' in source and m.raw(p)==source['fileSHA256']
  source['sha256']=source['fileSHA256']
  raw_checks.append({'path':str(p),'originalFileSHA256':source['fileSHA256'],'operation':'Exact declared immutable file digest name alias only; no invented hash/body or raw edit.'})
 assert m.raw(p)==source['sha256'];cap=m.read(p) if p.suffix=='.json' else None
 if isinstance(cap,dict) and 'originalRecord' in cap:
  jp=pathlib.Path(cap.get('nativeJournal') or cap['nativeJournalActual'])
  if not jp.exists():
   matches=list(pathlib.Path('/Users/eaafonasev/.codex/archived_sessions').glob('*'+cap['sourceNativeId']+'.jsonl'));assert len(matches)==1;jp=matches[0]
  record=json.loads(jp.read_text().split('\n')[cap['nativeRecordLine']-1]);assert record==cap['originalRecord']
  raw_checks.append({'path':str(p),'nativeId':cap['sourceNativeId'],'nativeLine':cap['nativeRecordLine'],'originalRecordExact':True})
m.alias_explicit_nested_inventory(a,sp,ps,R)
cat={};rows=[]
for path in sorted((m.C/'src/content/topics').glob('*.json')):
 t=topic_read(path)
 for card in t['questions']:
  cat[card['id']]=card;rows.append({'topicId':t['id'],'id':card['id'],'prompt':card['prompt'],'answers':[a['text'] for a in card['answers']],'correctIndex':card['correctIndex']})
assert len(rows)==11000 and m.sha(rows)==ps['globalMAIN']['rowsCanonicalSHA256']
inventory_read_binding=None
file_bindings=ps['globalMAIN'].get('allCurrentFileByteBindings',ps['globalMAIN'].get('currentFileByteBindings'))
if file_bindings is None:
 # Equivalent explicit author SHA-bound inventory; raw packet remains untouched.
 inv_path=pathlib.Path(sp['sourceInventoryPath']);inv_path=inv_path if inv_path.is_absolute() else m.C/inv_path
 assert str(inv_path)==ps['globalMAIN']['inventoryPath']==ps['sameTopicMAIN']['inventoryPath']
 assert m.raw(inv_path)==sp['sourceInventorySHA256']==ps['globalMAIN']['inventorySHA256']==ps['sameTopicMAIN']['inventorySHA256']
 inv=m.read(inv_path);assert inv['globalMAIN']['rowsCanonicalSHA256']==ps['globalMAIN']['rowsCanonicalSHA256']==m.sha(rows)
 assert inv['globalMAIN']['topicFileCount']==110 and inv['globalMAIN']['questionCount']==11000
 assert inv['sameTopicMAIN']['questions']==topic_read(m.C/'src/content/topics/fashion.json')['questions']
 file_bindings=inv['globalMAIN']['allCurrentFileByteBindings'];assert len(file_bindings)==110
 inventory_read_binding={'path':str(inv_path),'fileSHA256':m.raw(inv_path),'operation':'Read exact original sourceproof+peer SHA-bound inventory; all existing rows11000/topic100/files110 assertions retained, raw untouched.'}
for b in file_bindings:assert (__import__('hashlib').sha256(__import__('subprocess').check_output(['git','-C',str(m.C),'show',baseline+':'+b['path']])).hexdigest() if baseline else m.raw(m.C/b['path']))==b.get('sha256',b.get('fileSHA256',b.get('fileSha256')))
if 'questions' in ps.get('sameTopicMAIN',{}):
 saved_questions=ps['sameTopicMAIN']['questions']
 if len(saved_questions)==100 and all(isinstance(p,dict) and 'card' in p for p in saved_questions):
  assert [p['sourceOrder'] for p in saved_questions]==list(range(1,101))
  assert all(p['topicId']=='fashion' and p['id']==p['card']['id'] and m.sha(p['card'])==p['sha256'] for p in saved_questions)
  saved_questions=[p['card'] for p in saved_questions]
 assert saved_questions==topic_read(m.C/'src/content/topics/fashion.json')['questions']
else:
 # Preservation only: all100 exact ordered peer bodies are an equivalent
 # retained full topic snapshot. Do not hydrate or qualify the raw packet.
 topic_cards=topic_read(m.C/'src/content/topics/fashion.json')['questions']
 full_peers=[p for p in ps['actualCurrentPeers'] if p['topicId']=='fashion']
 assert len(full_peers)==100 and [p['sourceOrder'] for p in full_peers]==list(range(1,101))
 assert [p['card'] for p in full_peers]==topic_cards
for p in ps['actualCurrentPeers']:assert m.sha(p['card'])==p.get('sha256',p.get('canonicalSHA256')) and p['card']==cat[p['id']]

proof={'owner':m.O,'sourceNativeId':uid,'nativeJournal':str(native),'actualCompactions':comp,'lastInput':last['last_token_usage']['input_tokens'],'modelWindow':last['model_context_window'],'packet':str(R),'rawFileSHA256':{str(p.relative_to(R)):m.raw(p) for p in R.rglob('*') if p.is_file()},'status':e['status'],'preservedCatalogBaseline':baseline,'beforeHash':e['beforeHash'],'afterHash':e['afterHash'],'sixGroups':6,'fourVariants':4,'nativeCaptureBindings':raw_checks,'qualityCredit':0,'networkCalls':[],'technicalTripleHashRepresentationChecks':triple_checks,'explicitInventoryReadBinding':inventory_read_binding}
for i,o in enumerate(journal,1):
 p=o.get('payload',{})
 if o['type']=='response_item' and p.get('type')=='custom_tool_call' and re.match(r'^(?:(?:const|let|var)\s+\w+\s*=\s*|text\(\s*)?await\s+tools\.web__run\s*\(', re.sub(r'^const urls\s*=\s*\[(?:\s*"[^"\\]*(?:\\.[^"\\]*)*"\s*,?)*\s*\];\s*', '', re.sub(r'^// @exec:[^\n]*\n', '', p.get('input','').lstrip()))):
  callid=p['call_id'];result=next(((j,z) for j,z in enumerate(journal,1) if z.get('payload',{}).get('type')=='custom_tool_call_output' and z['payload'].get('call_id')==callid),None)
  proof['networkCalls'].append({'callLine':i,'call':p['input'],'resultLine':result[0] if result else None})
last_turn_start=max(i for i,o in enumerate(journal,1) if o['type']=='event_msg' and o.get('payload',{}).get('type')=='task_started')
task_start=last_turn_start
continuation=x.get('pendingFashion'+str(order),{}).get('cycle1Continuation' if a['cycle']==1 else 'initialContinuation')
if continuation:
 continued=m.read(continuation);original_task=m.read(actor['task'])
 assert continued['owner']==m.O and continued['sourceNativeId']==uid
 assert continued['originalTask']==actor['task'] and m.raw(actor['task'])==continued['originalTaskSHA256']
 assert original_task['cycle']==a['cycle'] and original_task['sourceOrder']==order and original_task.get('authorNativeId',original_task.get('sourceNativeId'))==uid
 task_start=continued['firstTaskStartLine']
 assert task_start<=last_turn_start and journal[task_start-1]==continued['originalFirstTaskStarted']
 proof['sameCycleContinuation']={'path':continuation,'rawSHA256':m.raw(continuation),'noCycleReset':True}
proof['currentTaskStartLine']=task_start
proof['currentTaskLastTurnStartLine']=last_turn_start
proof['priorTaskNetworkCalls']=[v for v in proof['networkCalls'] if v['callLine']<task_start]
proof['networkCalls']=[v for v in proof['networkCalls'] if v['callLine']>task_start]
actor.update(actualCompactions=comp,lastInput=proof['lastInput'],modelWindow=proof['modelWindow'],lastTaskEvent='task_complete',stage=f'IDLE_AFTER_SOURCE{order}_{e["status"]}',nativePreflightVerifiedBy=m.O)
proof_path=D/(name.replace('source-','').replace('/','-')+'-native-proof.json');m.write(proof_path,proof);m.write(D/'manifest.json',x)
print(m.savecode([p for p in R.rglob('*') if p.is_file()]+[proof_path,D/'manifest.json',pathlib.Path(__file__)],f'Preserve native SOURCE{order} {e["status"]} exact packet without quality credit'))
print(json.dumps({k:proof[k] for k in ['status','actualCompactions','lastInput','modelWindow','networkCalls']},ensure_ascii=False))
