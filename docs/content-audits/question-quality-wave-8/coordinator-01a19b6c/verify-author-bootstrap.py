"""Verify original completed creation and four separate full-read native results."""
import json, pathlib, sys, importlib.util
D=pathlib.Path(__file__).parent
s=importlib.util.spec_from_file_location('owned',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
uid,title,order=sys.argv[1:4]; reader='--reader' in sys.argv[4:]
paths=list(pathlib.Path('/Users/eaafonasev/.codex/sessions').rglob('*'+uid+'.jsonl'));assert len(paths)==1
rows=[json.loads(l) for l in paths[0].open()]
assert [r['payload']['id'] for r in rows if r['type']=='session_meta']==[uid]
assert sum(r['type']=='compacted' for r in rows)==0
items=[(i,r['payload']) for i,r in enumerate(rows,1) if r['type']=='response_item']
def decode(v):
 if isinstance(v,str):
  try:yield from decode(json.loads(v))
  except (ValueError,TypeError):
   # Some original create results encode content.text as an escaped JSON object.
   # Decode that one quoting layer only; original native output remains immutable.
   if v.startswith('{\\"'):
    try:yield from decode(json.loads(v.replace('\\"','"')))
    except (ValueError,TypeError):pass
 elif isinstance(v,dict):
  yield v
  for x in v.values():yield from decode(x)
 elif isinstance(v,list):
  for x in v:yield from decode(x)
checks=[]; rejected=[]
for name in ['pinned-question-revision-12e5581b.md','packet-contract.json','method-pilot.md','packet-format.md']:
 calls=[(i,p) for i,p in items if p.get('type')=='custom_tool_call' and name in p.get('input','') and 'cat ' in p.get('input','')]
 successful=[]
 for line,call in calls:
  outputs=[(i,p) for i,p in items if p.get('type')=='custom_tool_call_output' and p.get('call_id')==call['call_id']];assert len(outputs)==1
  results=[x for x in decode(outputs[0][1]['output']) if 'exit_code' in x]
  proof={'path':name,'callLine':line,'resultLine':outputs[0][0],'call_id':call['call_id']}
  invocation=call.get('input','').strip()
  exactWholeInvocation=any(invocation.startswith('text(await tools.exec_command({cmd:'+quote+'cat ') and invocation.endswith(quote+',max_output_tokens:12000}));') for quote in ["'",'"'])
  if exactWholeInvocation and len(results)==1 and results[0]['exit_code']==0 and 'Warning: truncated output' not in results[0]['output']:
   successful.append({**proof,'exit_code':0})
  else:rejected.append({**proof,'structuredResultCount':len(results),'qualifiedFullRead':False,'originalOutputPreservedInNative':True})
 assert len(successful)==1, (name,'exactly one successful whole structured read required',len(successful))
 checks.extend(successful)
root=pathlib.Path(m.read(D/'manifest.json')['rootNativeAudit']['nativeJournal'])
items_root=[r['payload'] for l in root.open() if (r:=json.loads(l))['type']=='response_item']
calls=[p for p in items_root if p.get('type')=='custom_tool_call' and 'tools.mcp__codex_app__create_thread({' in p.get('input','') and 'title:'+json.dumps(title,ensure_ascii=False) in p.get('input','')]
assert len(calls)==1
outputs=[p for p in items_root if p.get('type')=='custom_tool_call_output' and p.get('call_id')==calls[0]['call_id']];assert len(outputs)==1
decoded=list(decode(outputs[0]['output']));assert not any(x.get('isError') for x in decoded)
created=[x for x in decoded if isinstance(x.get('threadId'),str) and isinstance(x.get('hostId'),str)]
assert len(created)==1 and created[0]['threadId']==uid
report={'owner':m.O,('readerNativeId' if reader else 'sourceNativeId'):uid,'nativeJournal':str(paths[0]),'actualCompactions':0,'fourSeparateFullReads':checks,'rejectedOriginalReadAttempts':rejected,'noRetrocompliance':True,'originalCreationCallId':calls[0]['call_id'],'originalCreationResultId':outputs[0]['id'],'exactCreatedResult':created[0],'otherReturnedThreadIds':sorted({x['threadId'] for x in decoded if isinstance(x.get('threadId'),str)}-{uid}),'creationResultSelector':'Unique create response with threadId+hostId, distinct from any explicit archive response in same sequential exec output.','qualityCredit':0}
p=D/f'{"reader" if reader else "source"}{order}-bootstrap-proof.json';assert not p.exists();m.write(p,report)
print(m.savecode([p,pathlib.Path(__file__)],'Verify original native author bootstrap without quality credit'))
print(json.dumps(report,ensure_ascii=False))
