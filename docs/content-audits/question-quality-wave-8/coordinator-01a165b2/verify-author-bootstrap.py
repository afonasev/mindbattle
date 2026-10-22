"""Read exact original creation and four native structured reads; preserve compact proof."""
import pathlib,json,sys,importlib.util
D=pathlib.Path(__file__).parent
s=importlib.util.spec_from_file_location('m',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
order=int(sys.argv[1]);expected=sys.argv[2]
root=pathlib.Path(m.read(D/'manifest.json')['rootNativeAudit']['nativeJournal'])
rows=[json.loads(l) for l in root.open()]
prefix='text(await tools.mcp__codex_app__create_thread({title:"source: medicine'+str(order)+' exact2000"'
calls=[(i,r['payload']) for i,r in enumerate(rows,1) if r.get('type')=='response_item' and r.get('payload',{}).get('type')=='custom_tool_call' and r['payload'].get('input','').startswith(prefix)]
assert len(calls)==1
line,call=calls[0];outs=[(i,r) for i,r in enumerate(rows,1) if r.get('payload',{}).get('type')=='custom_tool_call_output' and r['payload'].get('call_id')==call['call_id']];assert len(outs)==1
def objects(v):
 if isinstance(v,str):
  try:yield from objects(json.loads(v))
  except ValueError:pass
 elif isinstance(v,list):
  for q in v:yield from objects(q)
 elif isinstance(v,dict):
  yield v
  for q in v.values():yield from objects(q)
obs=list(objects(outs[0][1]['payload']['output']));assert {v['threadId'] for v in obs if 'threadId' in v}=={expected} and not any(v.get('isError') for v in obs)
paths=list(pathlib.Path('/Users/eaafonasev/.codex/sessions').rglob('*'+expected+'.jsonl'));assert len(paths)==1
ar=[json.loads(l) for l in paths[0].open()];assert [r['payload']['id'] for r in ar if r.get('type')=='session_meta']==[expected];comp=sum(r.get('type')=='compacted' for r in ar);assert comp==0
checks=[]
for doc in ['coordinator-01a14377/pinned-question-revision-12e5581b.md','coordinator-01a13f31/packet-contract.json','coordinator-01a1593a/method-pilot.md','coordinator-01a1593a/packet-format.md']:
 cs=[(i,r['payload']) for i,r in enumerate(ar,1) if r.get('payload',{}).get('type')=='custom_tool_call' and doc in r['payload'].get('input','') and 'cat ' in r['payload'].get('input','')]
 assert len(cs)==1,(doc,len(cs))
 i,c=cs[0];rs=[(j,r) for j,r in enumerate(ar,1) if r.get('payload',{}).get('type')=='custom_tool_call_output' and r['payload'].get('call_id')==c['call_id']];assert len(rs)==1
 structured=[v for v in objects(rs[0][1]['payload']['output']) if 'exit_code' in v];assert len(structured)==1 and structured[0]['exit_code']==0 and 'truncated' not in structured[0]['output'].lower()
 checks.append({'document':doc,'callLine':i,'resultLine':rs[0][0],'structuredExitCode':0,'fullSuccessfulRead':True})
assert len({v['callLine'] for v in checks})==4
out=D/f'author{order}-bootstrap-proof.json';assert not out.exists()
m.write(out,{'sourceNativeId':expected,'nativeJournal':str(paths[0]),'rootCreationCallLine':line,'rootCreationCallId':call['call_id'],'rootOriginalResultLine':outs[0][0],'rootOriginalResultId':outs[0][1]['payload']['id'],'rootOriginalResultSHA256':m.sha(outs[0][1]),'fourSuccessfulFullReads':checks,'actualCompactions':comp,'scope':'READONLY ACK before START'})
print(m.savecode([out,pathlib.Path(__file__)],f'Verify source{order} exact native bootstrap and four full reads'))
print({'sourceNativeId':expected,'fullReads':4,'actualCompactions':comp})
