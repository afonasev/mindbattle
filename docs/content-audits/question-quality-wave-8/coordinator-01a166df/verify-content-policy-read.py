"""Bind actual complete Content section read before new SOURCE START; no quality credit."""
import pathlib,json,re,sys,importlib.util
D=pathlib.Path(__file__).parent
s=importlib.util.spec_from_file_location('m',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
order=int(sys.argv[1]);uid=sys.argv[2];reader='--reader' in sys.argv[3:];role='reader' if reader else 'source'
proof=m.read(D/f'{role}{order}-bootstrap-proof.json');assert proof['readerNativeId' if reader else 'sourceNativeId']==uid
native=pathlib.Path(proof['nativeJournal']);rows=[json.loads(l) for l in native.open()]
assert [r['payload']['id'] for r in rows if r['type']=='session_meta']==[uid]
assert sum(r['type']=='compacted' for r in rows)==0
def strings(v):
 if isinstance(v,str):
  yield v
  try:yield from strings(json.loads(v))
  except (ValueError,TypeError):pass
 elif isinstance(v,dict):
  for q in v.values():yield from strings(q)
 elif isinstance(v,list):
  for q in v:yield from strings(q)
path=m.P/'docs/GAME_SPEC.md';lines=path.read_text().splitlines();start=lines.index('## Контент вопросов');end=next((i for i in range(start+1,len(lines)) if lines[i].startswith(('## ','# '))),len(lines));section='\n'.join(lines[start:end]).strip()
matches=[{'resultLine':i,'call_id':r['payload']['call_id'],'originalResultRecordCanonicalSHA256':m.sha(r)} for i,r in enumerate(rows,1) if r['type']=='response_item' and r.get('payload',{}).get('type')=='custom_tool_call_output' and any(section in re.sub(r'^\d+: ?', '', b,flags=re.M) for b in strings(r['payload'].get('output',[])))]
assert matches,'Full current canonical section not found in original native output; no SOURCE START'
whole=[]
for check in proof['fourSeparateFullReads']:
 target=next((m.C/'docs/content-audits/question-quality-wave-8').rglob(check['path']));result=rows[check['resultLine']-1]['payload'];assert target.read_text() in list(strings(result['output']))
 whole.append({**check,'fileSHA256':m.raw(target),'originalWholeOutputEqualsFile':True})
p=D/f'{role}{order}-content-policy-proof.json';assert not p.exists()
m.write(p,{'owner':m.O,('readerNativeId' if reader else 'sourceNativeId'):uid,'actualNative':str(native),'fourExactWholeReadBytes':whole,'fullContentSection':{'path':str(path),'fileSHA256':m.raw(path),'lines':[start+1,end],'originalOutputs':matches},'verifiedBeforeSOURCEStart':not reader,'verifiedBeforeAssignedStageStart':True,'qualityCredit':0})
print(m.savecode([p,pathlib.Path(__file__)],f'Bind exact full Content policy and pinned bytes before SOURCE{order} start'))
