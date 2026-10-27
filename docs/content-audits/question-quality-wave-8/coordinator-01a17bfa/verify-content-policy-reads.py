"""Bind exact separate whole successful native policy reads before SOURCE START."""
import pathlib,json,importlib.util,sys
D=pathlib.Path(__file__).parent
s=importlib.util.spec_from_file_location('m',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
order=sys.argv[1];uid=sys.argv[2];role='reader' if '--reader' in sys.argv[3:] else 'source'
p=pathlib.Path(m.read(D/f'{role}{order}-bootstrap-proof.json')['nativeJournal'])
rows=[json.loads(l) for l in p.open()]
assert [v['payload']['id'] for v in rows if v.get('type')=='session_meta']==[uid]
assert sum(v.get('type')=='compacted' for v in rows)==0
def results(v):
 if isinstance(v,dict):
  if 'exit_code' in v and 'output' in v:yield v;return
  if v.get('type') in ['text','input_text']:yield from results(v.get('text'))
 elif isinstance(v,list):
  for a in v:yield from results(a)
 elif isinstance(v,str) and v.lstrip().startswith(('{','[')):
  try:a=json.loads(v)
  except ValueError:return
  yield from results(a)
outs=[]
for i,v in enumerate(rows,1):
 if v.get('payload',{}).get('type')=='custom_tool_call_output':
  for r in results(v['payload']['output']):outs.append((i,v['payload']['call_id'],r))
primary=pathlib.Path('/Users/eaafonasev/Projects/mindbattle')
files=[primary/'AGENTS.md',m.C/'AGENTS.md',*[primary/'.agents/references'/n for n in ['execution-policy.md','context-efficiency.md','model-routing.md']],*[pathlib.Path('/Users/eaafonasev/.codex/references')/n for n in ['session-efficiency.md','game-execution.md','task-cleanup.md']],m.C/'docs/content-audits/question-authoring-guide-2026-09-02.md']
expected=[(str(f),f.read_text().strip()) for f in files]
for label,f,lo,hi in [('fullContent135-285',m.P/'docs/GAME_SPEC.md',134,285),('spec21-33',m.P/'openspec/specs/question-catalog/spec.md',20,33)]:
 expected.append((label,'\n'.join(f.read_text().splitlines()[lo:hi]).strip()))
proof=[]
for label,body in expected:
 hits=[{'line':i,'call_id':cid} for i,cid,r in outs if r['exit_code']==0 and r['output'].strip()==body]
 proof.append({'path':label,'separateWholeReadCount':len(hits),'originalResults':hits})
print(json.dumps({'sourceNativeId':uid,'requiredReads':proof},ensure_ascii=False))
assert all(v['separateWholeReadCount']>=1 for v in proof)
identity=[]
for i,cid,r in outs:
 if r['exit_code']!=0:continue
 try:a=json.loads(r['output'])
 except ValueError:continue
 if isinstance(a,dict) and a.get('verifiedSessionMetaId')==uid and a.get('actualCompactions')==0 and 'originalCreateCall' in a and 'originalCreateOutput' in a:
  identity.append({'line':i,'call_id':cid,'originalIdentityResultCanonicalSHA256':m.sha(a)})
assert identity
out=D/f'{role}{order}-content-policy-proof.json';assert not out.exists()
m.write(out,{'owner':m.O,('readerNativeId' if role=='reader' else 'sourceNativeId'):uid,'nativeJournal':str(p),'requiredReads':proof,'identityOriginalResults':identity,'fullContentReadBeforeSTART':True,'qualityCredit':0,'nonzeroExecs':sum(r['exit_code']!=0 for i,cid,r in outs),'truncatedToolCalls':len({cid for i,cid,r in outs if 'Warning: truncated output' in r['output']})})
print(m.savecode([out,pathlib.Path(__file__)],'Bind exact separate original SOURCE policy and Content reads before START'))
