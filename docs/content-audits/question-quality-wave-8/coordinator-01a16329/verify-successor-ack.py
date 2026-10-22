"""Parent's deterministic audit of exact native readonly ACK and full successful document reads."""
import pathlib,json,importlib.util,hashlib
D=pathlib.Path(__file__).parent
s=importlib.util.spec_from_file_location('m',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
x=m.read(D/'manifest.json');S=x['successorThreadId'];native=pathlib.Path(x['successorNativeJournal']);rows=[json.loads(l) for l in native.open()]
assert next(r['payload']['id'] for r in rows if r['type']=='session_meta')==S
assert sum(r['type']=='compacted' for r in rows)==0
assert next(r['payload']['type'] for r in reversed(rows) if r.get('payload',{}).get('type') in ['task_started','task_complete'])=='task_complete'
def command_results(v):
 if isinstance(v,dict):
  if 'exit_code' in v and 'output' in v:yield v
  for a in v.values():yield from command_results(a)
 elif isinstance(v,list):
  for a in v:yield from command_results(a)
 elif isinstance(v,str):
  try:a=json.loads(v)
  except (ValueError,TypeError):return
  if a!=v:yield from command_results(a)
calls={r['payload']['call_id']:(i,r) for i,r in enumerate(rows,1) if r.get('payload',{}).get('type')=='custom_tool_call'}
success=[];bad=[];bodies=[]
for i,r in enumerate(rows,1):
 p=r.get('payload',{})
 if p.get('type')!='custom_tool_call_output':continue
 results=list(command_results(p.get('output')))
 if not results:continue
 line,call=calls[p['call_id']];entry={'callLine':line,'call':call,'resultLine':i,'result':r}
 if any(v['exit_code'] not in [None,0] for v in results):bad.append(entry);continue
 if not all(v['exit_code']==0 for v in results):continue
 success.append(entry)
 for v in results:
  if 'Warning: truncated output' not in v['output'] and 'Output exceeded available model context' not in v['output']:bodies.append((p['call_id'],v['output']))
docs=[m.C/'docs/content-audits/question-quality-wave-8'/p for p in ['coordinator-01a14377/pinned-question-revision-12e5581b.md','coordinator-01a13f31/packet-contract.json','coordinator-01a1593a/method-pilot.md','coordinator-01a1593a/packet-format.md']]
reads=[]
for p in docs:
 content=p.read_text().strip();matches=[cid for cid,b in bodies if content in b];assert matches,('No complete successful untruncated read',str(p));reads.append({'path':str(p),'rawSHA256':m.raw(p),'exactSuccessfulCallIds':matches})
finals=[(i,r) for i,r in enumerate(rows,1) if r.get('payload',{}).get('type')=='message' and r['payload'].get('role')=='assistant' and r['payload'].get('phase')=='final_answer']
assert finals
last=finals[-1];text='\n'.join(a.get('text','') for a in last[1]['payload']['content'] if isinstance(a,dict));assert 'ACK' in text and str(x['CURRENT']) in text and str(x['remaining']) in text and 'STOP' in text
assert all(m.flow.get(cid)[1]['owner']==m.O for cid in x['claims']) and m.read(m.P/'.flow-leases.json')=={}
for root,key in [(m.C,'code'),(m.P,'planning')]:assert m.raw(pathlib.Path(m.h.git(root,'rev-parse','--path-format=absolute','--git-path','index')))==x['foreignIndexes'][key]
report={'successor':S,'native':str(native),'rootPersonallyVerifiedExactNativeACK':True,'exactNativeVerificationCallsAndResults':success,'diagnosticFailuresPreservedSeparately':bad,'fullFourDocumentsSuccessfulUntruncatedReads':reads,'actualCompactions':0,'exactFinalACKLine':last[0],'exactFinalACKRecord':last[1],'CURRENT':x['CURRENT'],'remaining':x['remaining'],'claimsOwnerBeforeRelease':m.O,'leaseEmpty':True,'foreignIndexes':x['foreignIndexes'],'noQualityReplay':True}
m.write(D/'successor-ack.json',report)
print(m.savecode([pathlib.Path(__file__),D/'successor-ack.json'],'Preserve personally audited exact native readonly successor ACK'))
print({'successor':S,'actualCompactions':0,'successfulVerificationCalls':len(success),'diagnosticFailedCalls':len(bad),'fullDocuments':len(reads),'finalACK':text})
