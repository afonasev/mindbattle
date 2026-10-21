"""Owned exact-byte private saves; no quality credit."""
import pathlib,importlib.util,hashlib,json,datetime
C=pathlib.Path(__file__).resolve().parents[4]
P=pathlib.Path('/Users/eaafonasev/Projects/mindbattle/planning')
D=pathlib.Path(__file__).parent
O='01a15f65-e74b-74f1-be7c-22e19ea029e9'
def mod(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
h=mod('private_save',P/'evidence/question-revision-process-v2/private-save-helper-01a13cb1.py')
flow=mod('owned_flow',C/'tools/flow.py').Flow(P)
def read(p):return json.loads(pathlib.Path(p).read_text())
def write(p,v):pathlib.Path(p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
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

def alias_serialized_prompt_group(candidate,sp):
 e=candidate['entries'][0];q=e['proposedCard'];expected={'prompt':q['prompt'],'answers':[v['text'] for v in q['answers']],'correctIndex':q['correctIndex']}
 for g in sp['entries'][0].get('literalGroups',[]):
  if g['group']!='prompt_ordered_answers_key' or not isinstance(g['literal'],str) or not g['literal'].startswith('{'):continue
  original=g['literal'];assert json.loads(original)==expected
  assert original==json.dumps(expected,ensure_ascii=False,sort_keys=True,separators=(',',':'))
  assert hashlib.sha256(original.encode()).hexdigest()==g['literalSHA256']==e['fieldGroups'][g['group']]['afterCanonicalSHA256']==sha(expected)
  g.update(originalSerializedLiteral=original,originalSerializedLiteralSHA256=g['literalSHA256'],literal=expected,literalSHA256=sha(expected),technicalSerializedGroupAlias='Canonical JSON string of the exact entire ordered prompt/answers/key decoded to identical object; raw immutable, all literal values/grounds unchanged.')
