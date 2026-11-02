"""Verify original successful native bootstrap reads; no quality credit."""
import pathlib,json,hashlib,sys,importlib.util
D=pathlib.Path(__file__).parent;s=importlib.util.spec_from_file_location('m',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
sid=sys.argv[1];ps=list(pathlib.Path('/Users/eaafonasev/.codex/sessions').rglob('*'+sid+'.jsonl'));assert len(ps)==1;rs=[json.loads(l)for l in ps[0].open()];assert next(r['payload']['id']for r in rs if r['type']=='session_meta')==sid;assert sum(r['type']=='compacted'for r in rs)==0;assert next(r['payload']['type']for r in reversed(rs)if r.get('payload',{}).get('type')in ['task_started','task_complete'])=='task_complete'
def results(v):
 if isinstance(v,dict):
  if 'exit_code'in v and 'output'in v:yield v
  for a in v.values():yield from results(a)
 elif isinstance(v,list):
  for a in v:yield from results(a)
 elif isinstance(v,str):
  try:q=json.loads(v)
  except ValueError:return
  if q!=v:yield from results(q)
calls={r['payload']['call_id']:r for r in rs if r.get('payload',{}).get('type')=='custom_tool_call'};reads=[]
for rel in ['coordinator-01a14377/pinned-question-revision-12e5581b.md','coordinator-01a13f31/packet-contract.json','coordinator-01a1593a/method-pilot.md','coordinator-01a1593a/packet-format.md']:
 p=D.parent/rel;body=p.read_text().strip();found=[]
 for r in rs:
  d=r.get('payload',{})
  if d.get('type')!='custom_tool_call_output':continue
  for v in results(d.get('output')):
   if v['exit_code']==0 and body in v['output'] and 'Warning: truncated output'not in v['output']:found.append({'call_id':d['call_id'],'call':calls[d['call_id']],'result':r})
 assert found,('Missing full exit0 read',rel);reads.append({'path':str(p),'rawSHA256':m.raw(p),'exactReads':found})
inputs='\n'.join(r['payload'].get('input','')for r in calls.values())
identity_outputs=[]
for r in rs:
 if r.get('payload',{}).get('type')!='custom_tool_call_output':continue
 for v in results(r['payload'].get('output')):
  if v['exit_code']!=0:continue
  try:d=json.loads(v['output'])
  except (ValueError,TypeError):continue
  if isinstance(d,dict) and d.get('journal')==str(ps[0]) and d.get('nativeId')==sid and d.get('uniqueCompletedParentCreation') is True and d.get('session_meta')==[sid] and d.get('type_compacted')==0:identity_outputs.append({'call_id':r['payload']['call_id'],'result':r})
assert 'session_meta' in inputs and 'compacted' in inputs and (str(ps[0]) in inputs or identity_outputs), 'Need personally verified exact native path or original successful dynamic exact-ID identity proof'
assert 'AGENTS.md'in inputs and 'execution-policy.md'in inputs
info=next(r['payload']['info']for r in reversed(rs)if r.get('payload',{}).get('type')=='token_count');report={'owner':m.O,'sourceNativeId':sid,'native':str(ps[0]),'actualCompactions':0,'bootstrapFullFourDocuments':reads,'lastUsage':info,'qualityCredit':0};out=D/('bootstrap-'+sid+'.json');assert not out.exists();m.write(out,report);print(m.savecode([out,pathlib.Path(__file__)],'Preserve independent native full4doc bootstrap verification'));print({'native':str(ps[0]),'actualCompactions':0,'full4docs':True,'sourceNativeId':sid})
