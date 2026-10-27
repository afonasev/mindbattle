"""Deterministic network accounting; exact stored native recovery only, no quality credit."""
import pathlib,json,re,importlib.util,sys,subprocess
D=pathlib.Path(__file__).parent
def source_exec_body(value):
 value=re.sub(r'^// @exec:[^\n]*\n','',value.lstrip())
 return re.sub(r'^const url\s*=\s*"[^"\n]*";\s*','',value)
s=importlib.util.spec_from_file_location('owned',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
order=int(sys.argv[1]);R=D/sys.argv[2];proof_path=D/(sys.argv[3] if len(sys.argv)>3 and not sys.argv[3].startswith('--') else f'cars-road-transport{order}-native-proof.json');proof=m.read(proof_path);uid=proof['sourceNativeId'];include_prior='--include-prior-tasks' in sys.argv
p=pathlib.Path(proof['nativeJournal']);matches=[p] if p.exists() else list(pathlib.Path('/Users/eaafonasev/.codex/archived_sessions').glob('*'+uid+'.jsonl'));assert len(matches)==1
native=matches[0];rows=[json.loads(l) for l in native.open()];assert rows[0]['payload']['id']==uid
start=proof['currentTaskStartLine']
# The same native may already be on its next authorized card. Account only
# originals up to the completed task that produced this immutable proof.
last_turn_start=proof.get('currentTaskLastTurnStartLine',start);assert last_turn_start>=start
ends=[n for n,row in enumerate(rows,1) if n>last_turn_start and row.get('type')=='event_msg' and row.get('payload',{}).get('type')=='task_complete']
assert ends, 'SOURCE proof requires an actually completed task'
end=min(ends);rows=rows[:end];calls=[]
for n,row in enumerate(rows,1):
 p=row.get('payload',{})
 if (include_prior or n>start) and p.get('type')=='custom_tool_call' and re.match(r'^(?:(?:const|let|var)\s+\w+\s*=\s*|text\(\s*)?await\s+tools\.web__run\s*\(', re.sub(r'^const urls\s*=\s*\[(?:\s*"[^"\\]*(?:\\.[^"\\]*)*"\s*,?)*\s*\];\s*', '', re.sub(r'^// @exec:[^\n]*\n', '', source_exec_body(p.get('input',''))))):calls.append((n,p))
assert len(calls)==len(proof['networkCalls'])+ (len(proof.get('priorTaskNetworkCalls',[])) if include_prior else 0)
wrappers=[]
for p in R.rglob('*.json'):
 z=m.read(p)
 if isinstance(z,dict) and 'originalRecord' in z:
  if z.get('sourceNativeId') != uid:
   prior=pathlib.Path(z['nativeJournal']);prior_id=z['sourceNativeId']
   if not prior.exists():
    prior_paths=list(pathlib.Path('/Users/eaafonasev/.codex/archived_sessions').glob('*'+prior_id+'.jsonl'));assert len(prior_paths)==1;prior=prior_paths[0]
   prior_rows=[json.loads(line) for line in prior.open()]
   assert [r['payload']['id'] for r in prior_rows if r.get('type')=='session_meta']==[prior_id]
   assert prior_rows[z['nativeRecordLine']-1]==z['originalRecord']
   continue  # retained foreign-native source is not a new request by this actor
  if 'nativeRecordLine' in z:
   line=z['nativeRecordLine']
  elif 'callId' in z:
   assert z['sourceNativeId']==uid
   exact=[n for n,r in enumerate(rows,1) if r.get('payload',{}).get('type')=='custom_tool_call_output' and r['payload'].get('call_id')==z['callId']]
   assert len(exact)==1 and exact[0]==z['nativeOutputLine']
   assert rows[z['nativeCallLine']-1]['payload']['type']=='custom_tool_call'
   assert rows[z['nativeCallLine']-1]['payload']['call_id']==z['callId']
   assert any(n==z['nativeCallLine'] and call['call_id']==z['callId'] for n,call in calls)
   line=exact[0]
  else:
   assert z['sourceNativeId']==uid
   exact=[n for n,r in enumerate(rows,1) if r.get('payload',{}).get('type')=='custom_tool_call_output' and r['payload'].get('call_id')==z['nativeCallId']]
   assert len(exact)==1;line=exact[0]
  assert rows[line-1]==z['originalRecord'];wrappers.append((p,z))
network=[];owned=[];missing=[];pre_dispatch=[]
for ordinal,(line,call) in enumerate(calls,1):
 results=[(n,r) for n,r in enumerate(rows,1) if r.get('payload',{}).get('type')=='custom_tool_call_output' and r['payload'].get('call_id')==call['call_id']]
 if not results and uid=='01a168c9-82b2-7091-b910-c5dd4ba2ab3d' and order==47 and call['call_id']=='call_29707dd8e2b548f9983025c6e83bc93d':
  assert include_prior and line==231 and 'search_query' in call['input'] and 'open:' not in call['input']
  network.append({'ordinalOneBased':ordinal,'call_id':call['call_id'],'callLine':line,'call':call['input'],'originalCallRecord':rows[line-1],'resultLine':None,'originalResultMissingAtENOSPC':True,'uncured':True,'notPrimaryProof':True,'noRetryOrReset':True,'meaning':'One actual dispatched discovery preserved with missing original result, never reconstructed or promoted to source proof'})
  continue
 assert len(results)==1
 resultline,result=results[0];found=[(p,z) for p,z in wrappers if z['originalRecord']==result]
 if not found:
  p=D/f'cars-road-transport{order}-stored-native-result-{resultline}.json';z={'sourceNativeId':uid,'nativeJournalActual':str(native),'nativeRecordLine':resultline,'call_id':call['call_id'],'originalRecord':result,'operation':'Exact full stored native original recovered network0; author raw immutable. Not primary quality adoption.'}
  if p.exists():assert m.read(p)==z
  else:m.write(p,z)
  found=[(p,z)];owned.append(p);missing.append(resultline)
 identical_aliases=[]
 if len(found)>1:
  # Distinct URL captures may retain the same full multi-URL native result.
  # Every wrapper was already verified against the exact unique native output.
  assert all(z['originalRecord']==result for p,z in found)
  identical_aliases=[{'path':str(p),'fileSHA256':m.raw(p),'nativeExact':True} for p,z in sorted(found,key=lambda v:str(v[0]))]
  found=[sorted(found,key=lambda v:str(v[0]))[0]]
 assert len(found)==1;p,z=found[0]
 blocks=result['payload'].get('output',[])
 if isinstance(blocks,list) and blocks and blocks[0].get('text','').startswith('Script failed') and any(b.get('text','').startswith('Script error:\nSyntaxError:') for b in blocks if isinstance(b,dict)):
  check=subprocess.run(['node','--input-type=module','--check'],input=call['input'],text=True,capture_output=True)
  if check.returncode!=0:
   pre_dispatch.append({'call_id':call['call_id'],'callLine':line,'resultLine':resultline,'originalResult':str(p),'fileSHA256':m.raw(p),'nativeExact':True,'actualWebCalls':0,'reason':'Entire exec module rejected before execution; exact input fails compile-only Node syntax check. No source request dispatched.','compileOnlyExitCode':check.returncode,'compileOnlyStderr':check.stderr})
   continue
 network.append({'ordinalOneBased':ordinal,'call_id':call['call_id'],'callLine':line,'resultLine':resultline,'call':call['input'],'originalResult':str(p),'fileSHA256':m.raw(p),'nativeExact':True,'identicalOriginalResultAliases':identical_aliases})
report={'owner':m.O,'sourceNativeId':uid,'nativeJournalActual':str(native),'sourceOrder':order,'actualWebCalls':len(network),'candidateExecModules':len(calls),'preDispatchCompilationFailures':pre_dispatch,'includePriorTasks':include_prior,'proof':str(proof_path),'taskStartLine':start,'taskCompleteLine':end,'calls':network,'exactStoredRecoveryNetworkCalls':0,'missingAuthorResultLinesRecovered':missing,'rawPacketUnchanged':True,'qualityCredit':0}
assert proof_path.name.endswith('-native-proof.json')
default_report_name=proof_path.name.removesuffix('-native-proof.json')+'-network-accounting.json'
report_name=next((arg.split('=',1)[1] for arg in sys.argv if arg.startswith('--report-name=')),default_report_name);assert pathlib.Path(report_name).name==report_name
rp=D/report_name
assert not rp.exists(), 'Existing stage report is immutable; use an explicit new report name for revised evidence'
m.write(rp,report)
print(m.savecode([rp,pathlib.Path(__file__),*owned],f'Account SOURCE{order} exact stored native network results without quality credit'))
print(json.dumps({'actualWebCalls':len(network),'preDispatchCompilationFailures':len(pre_dispatch),'recoveredMissingOriginals':missing,'qualityCredit':0}))
