"""Owned exact-byte private saves; no quality credit."""
import pathlib,importlib.util,hashlib,json,datetime
C=pathlib.Path(__file__).resolve().parents[4]
P=pathlib.Path('/Users/eaafonasev/Projects/mindbattle/planning')
D=pathlib.Path(__file__).parent
O='01a160a6-2f23-7d91-84b9-0ec38f7a34b1'
def mod(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
h=mod('private_save',P/'evidence/question-revision-process-v2/private-save-helper-01a13cb1.py')
flow=mod('owned_flow',C/'tools/flow.py').Flow(P)
def read(p):return json.loads(pathlib.Path(p).read_text())
def write(p,v):
 p=pathlib.Path(p)
 if P in p.parents:
  assert read(P/'.flow-leases.json').get('planning',{}).get('owner')==O
  index=pathlib.Path(h.git(P,'rev-parse','--path-format=absolute','--git-path','index'))
  assert raw(index)==read(D/'manifest.json')['foreignIndexes']['planning']
 p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def raw(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def sha(v):return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def save(root,ref,files,message):
 paths=sorted(set(str(pathlib.Path(p).relative_to(root)) for p in files));idx=root/h.git(root,'rev-parse','--git-path','index');return h.save(root,ref,paths,message,raw(idx))
def savecode(files,message):return save(C,'refs/heads/codex/question-quality-wave-6',files,message)
def saveplan(files,message):
 with flow.locked():flow.lease('acquire','planning',O)
 try:return save(P,'refs/heads/codex/question-revision-resume-20261014',files,message)
 finally:
  with flow.locked():flow.lease('release','planning',O)

def alias_full_prompt_answer_concatenation(candidate,sp):
 e=candidate['entries'][0];q=e['proposedCard'];entry=sp['entries'][0]
 variants=entry['fourFullPromptAnswerNoteAssessments']
 if all(v['fullPrompt']==q['prompt'] for v in variants):return
 assert len(variants)==4 and {v['slot'] for v in variants}==set(range(4))
 assert sha(q)==e['afterHash']
 group={'prompt':q['prompt'],'answers':[a['text'] for a in q['answers']],'correctIndex':q['correctIndex']}
 assert e['fieldGroups']['prompt_ordered_answers_key']['afterCanonicalSHA256']==sha(group)
 literal=next(g for g in entry['literalGroups'] if g['group']=='prompt_ordered_answers_key')
 assert literal['literal']==group and literal['literalSHA256']==sha(group)
 for v in variants:
  a=q['answers'][v['slot']]
  assert v['answer']==a['text'] and v['note']==a['note']
  triple={'prompt':q['prompt'],'answer':a['text'],'note':a['note']}
  assert v['tripleSHA256']==sha(triple)
  assert v['fullPrompt']==q['prompt']+' '+a['text']
  v['originalPromptAnswerConcatenationLiteral']=v['fullPrompt']
  v['technicalRedundantPromptAnswerDecomposition']={'originalCanonicalSHA256':sha(v['fullPrompt']),'candidatePromptCanonicalSHA256':sha(q['prompt']),'alreadyDeclaredTripleSHA256':v['tripleSHA256'],'operation':'Exact prompt + one ASCII space + exact separately bound answer; invertible redundant serialization decomposition only. Original literal retained; no answer, note, hash, primary ground or assessment changed.'}
  v['fullPrompt']=q['prompt']

def alias_explicit_nested_inventory(candidate,sp,ps,R):
 """Lossless derived view of explicit SHA-bound inventory and original100 peers."""
 if 'globalMAIN' in ps or 'globalMAINRetrieval' not in ps:return
 assert candidate['sourceNativeId']==sp['sourceNativeId']==ps['sourceNativeId']
 assert candidate['cycle']==sp['cycle']==ps['cycle']
 g=ps['globalMAINRetrieval'];b=sp['freshInventoryBinding'];i=ps['immutableInventoryRaw']
 assert g['path']==b['path']==i['path'] and g['inventoryFileSHA256']==b['sha256']==i['sha256']
 path=pathlib.Path(g['path']);path=path if path.is_absolute() else C/path
 assert path.is_relative_to(R) and raw(path)==i['sha256']
 inv=read(path);full=inv['globalMAIN'];same=ps['sameTopicMAIN'];retained=same['actualCurrentPeers']
 assert g['topicFileCount']==full['topicFileCount']==110 and g['questionCount']==full['questionCount']==11000
 assert g['rowsCanonicalSHA256']==full['rowsCanonicalSHA256']==b['globalRowsCanonicalSHA256']
 assert len(full['allCurrentFileByteBindings'])==110
 rows=[]
 for f in full['allCurrentFileByteBindings']:
  assert raw(C/f['path'])==f['sha256']
  t=read(C/f['path']);rows.extend({'topicId':t['id'],'id':q['id'],'prompt':q['prompt'],'answers':[a['text'] for a in q['answers']],'correctIndex':q['correctIndex']} for q in t['questions'])
 assert len(rows)==11000 and sha(rows)==full['rowsCanonicalSHA256']
 topic=read(C/same['path']);assert len(retained)==same['questionCount']==100
 assert [e['sourceOrder'] for e in retained]==list(range(1,101))
 assert [e['card'] for e in retained]==inv['sameTopicMAIN']['questions']==topic['questions']
 assert all(e['topicId']==topic['id'] and e['id']==e['card']['id'] and sha(e['card'])==e['sha256'] for e in retained)
 assert same['fileSHA256']==inv['sameTopicMAIN']['fileSHA256']==b['sameTopicFileSHA256']==raw(C/same['path'])
 ps['globalMAIN']={**full,'sourceInventoryPath':str(path),'sourceInventorySHA256':raw(path)}
 ps['actualCurrentPeers']=retained
 same.update(questions=[e['card'] for e in retained],sourceInventoryPath=str(path),sourceInventorySHA256=raw(path))
 sp.update(sourceInventoryPath=str(path),sourceInventorySHA256=raw(path))
 ps['technicalExplicitNestedInventoryAlias']={'originalPeerSnapshot':str(R/'peer-snapshot.json'),'rawPeerSHA256':raw(R/'peer-snapshot.json'),'inventoryPath':str(path),'inventorySHA256':raw(path),'operation':'Exact explicit three-way path/SHA and live110/11000/100 bindings; nested original full peers aliased only, no new semantic assessment. Original relevantPairs retained.'}

def alias_single_sourceproof_entry(candidate,sp):
 """Alias a native-bound singular entry without changing author raw or grounds."""
 if 'entries' in sp:return
 if 'entry' not in sp:return
 assert len(candidate['entries'])==1 and isinstance(sp['entry'],dict)
 assert candidate['sourceNativeId']==sp['sourceNativeId'] and candidate['cycle']==sp['cycle']
 c=candidate['entries'][0];e=sp['entry'];q=c['proposedCard']
 assert e['id']==c['id']==q['id'] and e['topicId']==c['topicId']==sp['topicId']==candidate['topicId']
 assert e['sourceOrder']==c['sourceOrder'] and e['status']==c['status']
 assert len(e['literalGroups'])==6 and len(e['fourFullPromptAnswerNoteAssessments'])==4
 assert {v['slot'] for v in e['fourFullPromptAnswerNoteAssessments']}==set(range(4))
 for v in e['fourFullPromptAnswerNoteAssessments']:
  a=q['answers'][v['slot']];assert v['fullPrompt']==q['prompt'] and v['answer']==a['text'] and v['note']==a['note']
 sp['entries']=[json.loads(json.dumps(e,ensure_ascii=False))]
 assert sp['entries'][0]==e
 sp['technicalSingleEntryContainerAlias']={'originalKey':'entry','originalEntryCanonicalSHA256':sha(e),'sourceNativeId':sp['sourceNativeId'],'cycle':sp['cycle'],'operation':'Exact native/cycle/ID/topic/order/status and original six/four literals bound to candidate; singular original entry retained unchanged, deep-copied as entries[0]. No hydration, new ground, or raw edit.'}

def alias_serialized_prompt_group(candidate,sp):
 """Decode only exact canonical JSON serializations of the six bound literals."""
 alias_single_sourceproof_entry(candidate,sp)
 e=candidate['entries'][0];q=e['proposedCard'];expected={'prompt_ordered_answers_key':{'prompt':q['prompt'],'answers':[v['text'] for v in q['answers']],'correctIndex':q['correctIndex']},'explanation':q['explanation'],**{'note'+str(k):v['note'] for k,v in enumerate(q['answers'])}}
 for g in sp['entries'][0].get('literalGroups',[]):
  target=expected[g['group']]
  if g['literal']==target or not isinstance(g['literal'],str) or not g['literal'].startswith(('{','"')):continue
  original=g['literal'];assert json.loads(original)==target
  assert original==json.dumps(target,ensure_ascii=False,sort_keys=True,separators=(',',':'))
  assert hashlib.sha256(original.encode()).hexdigest()==g['literalSHA256']==e['fieldGroups'][g['group']]['afterCanonicalSHA256']==sha(target)
  g.update(originalSerializedLiteral=original,originalSerializedLiteralSHA256=g['literalSHA256'],literal=target,literalSHA256=sha(target),technicalSerializedGroupAlias='Canonical JSON serialization of exact bound literal decoded to identical object/string; raw immutable, all values/grounds unchanged.')

def alias_full_body_wrapper_digests(ps,R):
 same=ps.get('sameTopicMAIN',{});wrappers=same.get('questions',[])
 if len(wrappers)!=100 or not all(isinstance(w,dict) and 'card' in w for w in wrappers):return
 if all('sha256' in w for w in wrappers):return
 path=C/same['path'];topic=read(path)
 assert same['questionCount']==100 and same['fileSHA256']==raw(path)
 assert [w['sourceOrder'] for w in wrappers]==list(range(1,101))
 assert [w['card'] for w in wrappers]==topic['questions']
 assert all(w['id']==w['card']['id'] and w['topicId']==topic['id'] for w in wrappers)
 for w in wrappers:
  if 'sha256' in w:assert w['sha256']==sha(w['card'])
  else:w.update(sha256=sha(w['card']),technicalDerivedBodyDigest='Exact original full card body, id, sourceOrder, topic path and fileSHA verified against live entire100; digest computed, raw untouched.')
 ps['technicalFullBodyWrapperDigestAlias']={'rawPeerSnapshot':str(R/'peer-snapshot.json'),'rawSHA256':raw(R/'peer-snapshot.json'),'topicFileSHA256':raw(path),'orderedFullBodiesVerified':100,'operation':'Deterministic digest of explicit unchanged full bodies; no new peer assessment or unbound hydration.'}

def alias_explicit_peer_inventory_projection(candidate,sp,ps,R):
 """Recover only explicit SHA-bound full bodies behind author MAIN projections."""
 if not isinstance(ps.get('actualCurrentPeers'),int):return
 if not all(k in ps for k in ['freshInventoryPath','freshInventorySHA256','fullClosestCurrentPeers']):return
 assert candidate['cycle']==sp['cycle']==ps['cycle']==0
 assert candidate['sourceNativeId']==sp['sourceNativeId']==ps['sourceNativeId']
 e=candidate['entries'][0];same=ps['sameTopicMAIN'];global_audit=ps['globalMAIN']
 path=pathlib.Path(ps['freshInventoryPath']);path=path if path.is_absolute() else C/path
 assert path.is_relative_to(R) and raw(path)==ps['freshInventorySHA256']
 inv=read(path);full=inv['sameTopicMAIN']['questions'];topic=read(C/same['path'])
 assert inv['sameTopicMAIN']['topicId']==same['topicId']==e['topicId']==topic['id']
 assert ps['actualCurrentPeers']==same['questionCount']==len(full)==len(topic['questions'])==100
 assert full==topic['questions']
 assert same['fileSHA256']==inv['sameTopicMAIN']['fileSHA256']==raw(C/same['path'])
 def projection(q):return {'topicId':topic['id'],'id':q['id'],'prompt':q['prompt'],'answers':[a['text'] for a in q['answers']],'correctIndex':q['correctIndex']}
 assert same['questions']==[projection(q) for q in full]
 assert global_audit['topicFileCount']==inv['globalMAIN']['topicFileCount']==110
 assert global_audit['questionCount']==inv['globalMAIN']['questionCount']==11000
 assert global_audit['rowsCanonicalSHA256']==inv['globalMAIN']['rowsCanonicalSHA256']
 assert global_audit['allCurrentFileByteBindings']==inv['globalMAIN']['allCurrentFileByteBindings']
 assert len(global_audit['allCurrentFileByteBindings'])==110
 for f in global_audit['allCurrentFileByteBindings']:assert raw(C/f['path'])==f['sha256']
 mapping={q['id']:q for q in full};relevant=ps['fullClosestCurrentPeers'];assert relevant
 for peer in relevant:
  assert peer['topicId']==topic['id'] and peer['card']==mapping[peer['id']]
  assert peer['card']==full[peer['sourceOrder']-1] and sha(peer['card'])==peer['sha256']
 same['originalMAINProjectionQuestions']=same['questions'];same['questions']=json.loads(json.dumps(full,ensure_ascii=False))
 ps['originalActualCurrentPeerInventoryCount']=ps['actualCurrentPeers'];ps['actualCurrentPeers']=json.loads(json.dumps(relevant,ensure_ascii=False))
 global_audit.update(sourceInventoryPath=str(path),sourceInventorySHA256=raw(path))
 same.update(sourceInventoryPath=str(path),sourceInventorySHA256=raw(path))
 sp.update(sourceInventoryPath=str(path),sourceInventorySHA256=raw(path))
 ps['technicalExplicitProjectedTopicSnapshotAlias']={'rawPeerSnapshot':str(R/'peer-snapshot.json'),'rawPeerSHA256':raw(R/'peer-snapshot.json'),'inventoryPath':str(path),'inventorySHA256':raw(path),'operation':'Exact original top-level path/SHA,100MAIN projections,110filebindings,11000rowdigest and same-topic fileSHA bind the full100 bodies already retained by this author. Inventory count100 is not assessed-peer credit; only original fullClosestCurrentPeers are substantive peers. No unbound hydration, new peer assessment, literal or source ground.'}
