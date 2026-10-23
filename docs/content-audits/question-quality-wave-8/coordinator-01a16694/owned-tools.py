"""Owned exact-byte private saves; no quality credit."""
import pathlib,importlib.util,hashlib,json,datetime
C=pathlib.Path(__file__).resolve().parents[4]
P=pathlib.Path('/Users/eaafonasev/Projects/mindbattle/planning')
D=pathlib.Path(__file__).parent
O='01a16694-c910-7733-9153-75203048e97e'
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
 paths=sorted(set(str(pathlib.Path(p).relative_to(root)) for p in files));idx=root/h.git(root,'rev-parse','--git-path','index');expected=read(D/'manifest.json')['foreignIndexes']['planning' if root==P else 'code'];assert raw(idx)==expected, 'Foreign index differs from exact task boundary';return h.save(root,ref,paths,message,expected)
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


def alias_source83_clarified_literals(candidate,sp,ps,R):
 """Bind two author-clarified literal copies; original raw and grounds stay intact."""
 if candidate['entries'][0]['sourceOrder']!=83 or candidate.get('cycle')!=0:return
 R=pathlib.Path(R);assert R==D/'source-history-russia83'
 uid='01a1627c-8cb4-7b52-b8b1-7f6752217e7f'
 assert candidate['sourceNativeId']==sp['sourceNativeId']==ps['sourceNativeId']==uid
 cp=R/'literal-binding-clarification.json';clar=read(cp)
 assert clar['sourceNativeId']==uid and clar['networkCalls']==clar['cycle']==clar['qualityCredit']==0
 freeze='463701e1cb541566022b1f042f32981a6153b761'
 for name,proof in clar['originalPacketFiles'].items():
  p=R/name;assert raw(p)==proof['sha256']
  assert p.read_bytes()==__import__('subprocess').check_output(['git','-C',str(C),'show',freeze+':'+str(p.relative_to(C))])
 e=candidate['entries'][0];assert sha(e['proposedCard'])==e['afterHash']==clar['originalPacketFiles']['candidate.json']['afterHash']
 if isinstance(e['fieldGroups'],list):
  original=e['fieldGroups'];assert len(original)==6 and {g['group'] for g in original}=={'prompt_ordered_answers_key','explanation','note0','note1','note2','note3'}
  assert all(set(g)=={'group','beforeCanonicalSHA256','afterCanonicalSHA256'} for g in original)
  e['originalFieldGroupsList']=original
  e['fieldGroups']={g['group']:{k:v for k,v in g.items() if k!='group'} for g in original}
  e['technicalFieldGroupsListAlias']='Six explicit distinct named before/after hash entries projected to dictionary; original ordered list retained unchanged.'
 def pointer(value,path):
  for key in path.split('/')[1:]:value=value[int(key)] if isinstance(value,list) else value[key]
  return value
 assert {v['group'] for v in clar['bindings']}=={'explanation','note2'} and len(clar['bindings'])==2
 for b in clar['bindings']:
  g=pointer(sp,b['originalSourceproofPointer']);literal=pointer(candidate,b['existingCandidatePointer'])
  assert g['group']==b['group'] and g['literal']==b['originalLiteral'] and g['literalSHA256']==b['originalLiteralSHA256']==sha(g['literal'])
  assert g['primaryGround']==b['unchangedPrimaryGround'] and g['sourcePaths']==b['unchangedSourcePaths'] and g['locator']==b['unchangedLocator']
  assert literal==b['intendedLiteral'] and sha(literal)==b['intendedLiteralSHA256']==e['fieldGroups'][b['group']]['afterCanonicalSHA256']
  if b['group']=='note2':
   assert pointer(sp,b['existingVariantPointer'])['note']==literal
   assert pointer(sp,b['existingCorrectNoteNewFactPointer'])['newFact']==literal
  g['originalLiteralBindingBeforeClarification']={'literal':g['literal'],'literalSHA256':g['literalSHA256']}
  g.update(literal=literal,literalSHA256=sha(literal))
 sp['technicalAuthorClarifiedLiteralBinding']={'path':str(cp),'rawSHA256':raw(cp),'originalPacketFreeze':freeze,'temporalBoundary':clar['temporalBoundary'],'operation':'Two stale literal copies bound to already-emitted exact candidate and explicit author clarification. Original raw, all grounds/locators/source paths and judgments retained; no new source claim or quality credit.'}

def alias_source83_cycle1_redundant_snapshot(candidate,sp,ps,R):
 """Reconcile exact known shared apply; preserve historical full snapshot."""
 if candidate['entries'][0]['sourceOrder']!=83 or candidate.get('cycle')!=1:return
 R=pathlib.Path(R);assert R==D/'source-history-russia83-cycle1'
 uid='01a1627c-8cb4-7b52-b8b1-7f6752217e7f'
 assert candidate['sourceNativeId']==sp['sourceNativeId']==ps['sourceNativeId']==uid
 freeze='f2941aeffbcbc0757507313f92b0ff8bcc57599c'
 for name in ['candidate.json','sourceproof.json','peer-snapshot.json']:
  p=R/name;assert p.read_bytes()==__import__('subprocess').check_output(['git','-C',str(C),'show',freeze+':'+str(p.relative_to(C))])
 topic_path=C/'src/content/topics/history-russia.json';topic=read(topic_path);live=topic['questions']
 full=ps['actualCurrentPeers'];assert len(full)==6 and [v['sourceOrder'] for v in full]==[50,64,70,74,85,96]
 assert all(v['card']==live[v['sourceOrder']-1] for v in full)
 assert all(v['topicId']=='history-russia' and v['id']==v['card']['id'] and sha(v['card'])==v['sha256'] for v in full)
 assert len(ps['fullClosestCurrentPeers'])==6 and all(v['card']==next(q for q in live if q['id']==v['id']) for v in ps['fullClosestCurrentPeers'])
 batch=read(D/'source83-84-shared-apply.json')
 oldbytes=__import__('subprocess').check_output(['git','-C',str(C),'show',batch['baseline']+':src/content/topics/history-russia.json'])
 old=json.loads(oldbytes)['questions'];assert ps['sameTopicMAIN']['questions']==old
 assert ps['sameTopicMAIN']['fileSHA256']==hashlib.sha256(oldbytes).hexdigest()
 assert [i for i,(a,b) in enumerate(zip(old,live),1) if a!=b]==[83,84]
 derived=__import__('copy').deepcopy(old);applied_bindings=[]
 for order in [83,84]:
  app=read(D/f'qualified-source-history-russia{order}-apply.json')['applied'][0]
  assert old[order-1]==app['beforeCard'] and live[order-1]==app['proposedCard']
  derived[order-1]=app['proposedCard']
  applied_bindings.append({'path':str(D/f'qualified-source-history-russia{order}-apply.json'),'rawSHA256':raw(D/f'qualified-source-history-russia{order}-apply.json'),'beforeCanonicalSHA256':sha(app['beforeCard']),'afterCanonicalSHA256':sha(app['proposedCard'])})
 assert derived==live
 e=candidate['entries'][0];assert e['beforeCard']==live[82] and e['beforeHash']==sha(live[82])
 assert ps['candidate']['beforeCard']==live[82] and ps['candidate']['proposedCard']==e['proposedCard']
 bindings=ps['globalMAIN']['allCurrentFileByteBindings'];files=sorted((C/'src/content/topics').glob('*.json'));assert len(bindings)==len(files)==110
 assert [b['path'] for b in bindings]==[str(f.relative_to(C)) for f in files]
 rows=[]
 for b,f in zip(bindings,files):
  if f==topic_path:assert b['sha256']==hashlib.sha256(oldbytes).hexdigest()
  else:assert b['sha256']==raw(f)
  t=read(f);rows.extend({'topicId':t['id'],'id':q['id'],'prompt':q['prompt'],'answers':[a['text'] for a in q['answers']],'correctIndex':q['correctIndex']} for q in t['questions'])
 assert len(rows)==11000 and sha(rows)==ps['globalMAIN']['rowsCanonicalSHA256']
 proof={'originalRaw':str(R/'peer-snapshot.json'),'rawSHA256':raw(R/'peer-snapshot.json'),'rawFreeze':freeze,'historicalQuestionsPointer':'/sameTopicMAIN/questions','originalQuestionsCanonicalSHA256':sha(old),'explicitFreshRelevantPeersPointer':'/actualCurrentPeers','explicitFreshRelevantPeersCount':6,'currentQuestionsCanonicalSHA256':sha(derived),'oldTopicFileSHA256':hashlib.sha256(oldbytes).hexdigest(),'currentTopicFileSHA256':raw(topic_path),'knownSharedApply':str(D/'source83-84-shared-apply.json'),'exactAppliedBodyBindings':applied_bindings,'changedOrders':[83,84],'preapplicationOnly':True,'inventoryFileHydration':False,'operation':'Original cycle1 retains historical100 full bodies plus6 unchanged fresh relevant peers. Project only exact known applied83/84 before-to-after bodies into the historical full snapshot. All other98 bodies and110 file bindings proven unchanged. Original raw,6 relevant peer bodies and semantic comparisons/grounds remain unchanged. Original full100 is explicitly historical, not called fresh.'}
 ps['sameTopicMAIN']['questions']=derived
 ps['sameTopicMAIN']['fileSHA256']=raw(topic_path)
 next(b for b in bindings if b['path']=='src/content/topics/history-russia.json')['sha256']=raw(topic_path)
 ps['technicalRedundantSnapshotStageBinding']=proof;sp['technicalRedundantSnapshotStageBinding']=proof

def alias_source84_cycle1_variant_names(candidate,sp,ps,R):
 """Expose exact existing prompt and SHA-bound locator lists under contract names."""
 if candidate['entries'][0]['sourceOrder']!=84 or candidate.get('cycle')!=1:return
 R=pathlib.Path(R);assert R==D/'source-history-russia84-cycle1'
 uid='01a16282-713c-7aa3-b66b-ca02fb99d0e1'
 assert candidate['sourceNativeId']==sp['sourceNativeId']==ps['sourceNativeId']==uid
 for name in ['candidate.json','sourceproof.json','peer-snapshot.json']:
  p=R/name;assert p.read_bytes()==__import__('subprocess').check_output(['git','-C',str(C),'show','d0baf3be7a148345b6dca8f9363b706338353c88:'+str(p.relative_to(C))])
 q=candidate['entries'][0]['proposedCard'];sources={}
 for source in sp['rawSources']:
  p=pathlib.Path(source['path']);p=p if p.is_absolute() else C/p
  assert raw(p)==source['sha256'];sources[str(p)]=source['sha256']
 for v in sp['entries'][0]['fourFullPromptAnswerNoteAssessments']:
  a=q['answers'][v['slot']];assert v['prompt']==q['prompt'] and v['answer']==a['text'] and v['note']==a['note']
  assert v['tripleSHA256']==sha({'prompt':v['prompt'],'answer':v['answer'],'note':v['note']})
  assert 'fullPrompt' not in v and 'sourcePaths' not in v and 'locator' not in v
  paths=[];locators=[]
  for loc in v['sourcesLocators']:
   p=pathlib.Path(loc['path']);p=p if p.is_absolute() else C/p
   assert sources[str(p)]==loc['fileSHA256']==raw(p)
   paths.append(loc['path']);locators.append(loc['locator'])
  assert paths
  v.update(fullPrompt=v['prompt'],sourcePaths=list(dict.fromkeys(paths)),locator=' | '.join(locators))
 sp['technicalVariantFieldNameAlias']={'rawSourceproof':str(R/'sourceproof.json'),'rawSHA256':raw(R/'sourceproof.json'),'operation':'Exact existing prompt literal and explicit original SHA-bound source locator paths exposed as fullPrompt/sourcePaths/locator. Original prompt/sourcesLocators and every judgment retained unchanged. Unchanged INITIAL reader judgments remain attributed to original reader, not claimed as new independent author review.'}

def alias_source77_own_prior_application(candidate,sp,ps,R):
 """Exact own77 preapplication bookkeeping delta; no inventory-file hydration."""
 if candidate.get('cycle')!=1 or candidate['entries'][0]['sourceOrder']!=77:return
 R=pathlib.Path(R);assert R.parent==D and R.name=='source-history-russia77-cycle1'
 assert candidate['sourceNativeId']==sp['sourceNativeId']==ps['sourceNativeId'] and sp['cycle']==ps['cycle']==1
 import copy
 files=sorted((C/'src/content/topics').glob('*.json'));assert len(files)==110
 live={};live_rows=[]
 def project(t,q):return {'topicId':t,'id':q['id'],'prompt':q['prompt'],'answers':[a['text'] for a in q['answers']],'correctIndex':q['correctIndex']}
 for f in files:
  t=read(f);live[t['id']]=t;live_rows.extend(project(t['id'],q) for q in t['questions'])
 assert len(live_rows)==11000
 if ps['globalMAIN']['rowsCanonicalSHA256']==sha(live_rows):return
 I=R.with_name('source-history-russia77');initial=read(I/'candidate.json');oldps=read(I/'peer-snapshot.json');e0=initial['entries'][0];e=candidate['entries'][0]
 assert initial['sourceNativeId']==candidate['sourceNativeId'] and initial['cycle']==0
 assert e['id']==e0['id']=='history-russia-constitution-1993-method' and e['beforeCard']==e0['proposedCard'] and sha(e['beforeCard'])==e0['afterHash']
 only=copy.deepcopy(e['proposedCard']);assert only['answers'][2]['text']=='Всенародным голосованием';only['answers'][2]['text']='Всенародное голосование';assert only==e['beforeCard']
 assert ps['candidate']['beforeCard']==e['beforeCard'] and ps['candidate']['proposedCard']==e['proposedCard']
 assert ps['globalMAIN']==oldps['globalMAIN'] and ps['sameTopicMAIN']==oldps['sameTopicMAIN'] and ps['actualCurrentPeers']==oldps['actualCurrentPeers'] and ps['fullClosestCurrentPeers']==oldps['fullClosestCurrentPeers'] and ps['currentGuardRows']==oldps['currentGuardRows']
 oldtask=read(D/'source-history-russia77-task.json');oldbytes=__import__('subprocess').check_output(['git','--no-optional-locks','-C',str(C),'show',oldtask['baselineCode']+':src/content/topics/history-russia.json']);oldtopic=json.loads(oldbytes);now=live['history-russia']
 assert oldtopic['questions'][76]==e0['beforeCard'] and now['questions'][76]==e0['proposedCard']
 assert [i for i,(a,b) in enumerate(zip(oldtopic['questions'],now['questions']),1) if a!=b]==[77]
 prior=read(D/'qualified-source-history-russia77-apply.json');assert prior['author']==candidate['sourceNativeId'] and prior['applied'][0]['beforeCard']==e0['beforeCard'] and prior['applied'][0]['proposedCard']==e['beforeCard']
 binding=ps['globalMAIN']['allCurrentFileByteBindings'];assert len(binding)==110 and [v['path'] for v in binding]==[str(f.relative_to(C)) for f in files]
 old_rows=[];history_field=None
 for b,f in zip(binding,files):
  key=next(k for k in ['sha256','fileSHA256','fileSha256','rawSHA256'] if k in b)
  if f.name=='history-russia.json':assert b[key]==hashlib.sha256(oldbytes).hexdigest();t=oldtopic;history_field=key
  else:assert b[key]==raw(f);t=live[f.stem]
  old_rows.extend(project(t['id'],q) for q in t['questions'])
 assert len(old_rows)==11000 and sha(old_rows)==ps['globalMAIN']['rowsCanonicalSHA256']
 assert ps['sameTopicMAIN']['questions']==oldtopic['questions'] and ps['sameTopicMAIN']['fileSHA256']==hashlib.sha256(oldbytes).hexdigest()
 peers=ps['actualCurrentPeers'];assert len(peers)==100 and [v['sourceOrder'] for v in peers]==list(range(1,101)) and [v['card'] for v in peers]==oldtopic['questions']
 for v in peers:assert v['id']==v['card']['id'] and v['topicId']=='history-russia' and v['sha256']==sha(v['card'])
 assert all(v['id']!=e['id'] for v in ps['fullClosestCurrentPeers'])
 guard=ps['currentGuardRows']['currentTargetBeforeCard'];assert guard['card']==e0['beforeCard'] and guard['sha256']==e0['beforeHash']
 proof={'rawPeerPath':str(R/'peer-snapshot.json'),'rawPeerSHA256':raw(R/'peer-snapshot.json'),'ownInitialCandidatePath':str(I/'candidate.json'),'ownInitialCandidateSHA256':raw(I/'candidate.json'),'ownInitialPeerPath':str(I/'peer-snapshot.json'),'ownInitialPeerSHA256':raw(I/'peer-snapshot.json'),'originalCatalogCommit':oldtask['baselineCode'],'oldGlobalRowSHA256':sha(old_rows),'currentGlobalRowSHA256':sha(live_rows),'oldSelfHash':e0['beforeHash'],'currentSelfHash':e['beforeHash'],'newGrammarProposalHash':e['afterHash'],'allOtherCardsAnd110FileBindingsProven':True,'inventoryFileHydration':False,'selfIsDistinctPeer':False,'operation':'Only exact own prior77 application replaces historical self-preimage in full100/110/11000 bookkeeping. Original raw unchanged; no literal, primaryGround or distinct-peer assessment changed.'}
 ps['globalMAIN']['rowsCanonicalSHA256']=sha(live_rows)
 for b in binding:
  if b['path']=='src/content/topics/history-russia.json':b[history_field]=raw(C/b['path'])
 ps['sameTopicMAIN']['questions']=copy.deepcopy(now['questions']);ps['sameTopicMAIN']['fileSHA256']=raw(C/'src/content/topics/history-russia.json')
 for v in peers:
  if v['id']==e['id']:v.update(card=copy.deepcopy(e['beforeCard']),sha256=e['beforeHash'])
 guard.update(card=copy.deepcopy(e['beforeCard']),sha256=e['beforeHash'])
 ps['technicalOwnPrior77SelfPreimageAlias']=proof;sp['technicalOwnPrior77SelfPreimageAlias']=proof
