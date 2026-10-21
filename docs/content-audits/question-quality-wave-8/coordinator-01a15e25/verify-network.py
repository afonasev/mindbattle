"""Deterministic network accounting; exact stored native recovery only, no quality credit."""
import pathlib,json,re,importlib.util,sys
D=pathlib.Path(__file__).parent
s=importlib.util.spec_from_file_location('owned',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
order=int(sys.argv[1]);R=D/sys.argv[2];proof_path=D/(sys.argv[3] if len(sys.argv)>3 and not sys.argv[3].startswith('--') else f'history-russia{order}-native-proof.json');proof=m.read(proof_path);uid=proof['sourceNativeId'];include_prior='--include-prior-tasks' in sys.argv
p=pathlib.Path(proof['nativeJournal']);matches=[p] if p.exists() else list(pathlib.Path('/Users/eaafonasev/.codex/archived_sessions').glob('*'+uid+'.jsonl'));assert len(matches)==1
native=matches[0];rows=[json.loads(l) for l in native.open()];assert rows[0]['payload']['id']==uid
start=proof['currentTaskStartLine'];calls=[]
for n,row in enumerate(rows,1):
 p=row.get('payload',{})
 if (include_prior or n>start) and p.get('type')=='custom_tool_call' and re.search(r'await\s+tools\.web__run\s*\(',p.get('input','')):calls.append((n,p))
assert len(calls)==len(proof['networkCalls'])+ (len(proof.get('priorTaskNetworkCalls',[])) if include_prior else 0)
wrappers=[]
for p in R.rglob('*.json'):
 z=m.read(p)
 if isinstance(z,dict) and 'originalRecord' in z:
  line=z['nativeRecordLine'];assert rows[line-1]==z['originalRecord'];wrappers.append((p,z))
network=[];owned=[];missing=[]
for ordinal,(line,call) in enumerate(calls,1):
 results=[(n,r) for n,r in enumerate(rows,1) if r.get('payload',{}).get('type')=='custom_tool_call_output' and r['payload'].get('call_id')==call['call_id']];assert len(results)==1
 resultline,result=results[0];found=[(p,z) for p,z in wrappers if z['originalRecord']==result]
 if not found:
  p=D/f'history-russia{order}-stored-native-result-{resultline}.json';z={'sourceNativeId':uid,'nativeJournalActual':str(native),'nativeRecordLine':resultline,'call_id':call['call_id'],'originalRecord':result,'operation':'Exact full stored native original recovered network0; author raw immutable. Not primary quality adoption.'}
  if p.exists():assert m.read(p)==z
  else:m.write(p,z)
  found=[(p,z)];owned.append(p);missing.append(resultline)
 assert len(found)==1;p,z=found[0]
 network.append({'ordinalOneBased':ordinal,'call_id':call['call_id'],'callLine':line,'resultLine':resultline,'call':call['input'],'originalResult':str(p),'fileSHA256':m.raw(p),'nativeExact':True})
report={'owner':m.O,'sourceNativeId':uid,'nativeJournalActual':str(native),'sourceOrder':order,'actualWebCalls':len(calls),'includePriorTasks':include_prior,'proof':str(proof_path),'calls':network,'exactStoredRecoveryNetworkCalls':0,'missingAuthorResultLinesRecovered':missing,'rawPacketUnchanged':True,'qualityCredit':0}
rp=D/f'history-russia{order}-network-accounting.json';m.write(rp,report)
print(m.savecode([rp,pathlib.Path(__file__),*owned],f'Account SOURCE{order} exact stored native network results without quality credit'))
print(json.dumps({'actualWebCalls':len(calls),'recoveredMissingOriginals':missing,'qualityCredit':0}))
