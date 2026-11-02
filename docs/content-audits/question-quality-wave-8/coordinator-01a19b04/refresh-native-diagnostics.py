"""Retain exact original nonzero command results, without replay or weakened assertions."""
import pathlib,json,importlib.util
D=pathlib.Path(__file__).parent
s=importlib.util.spec_from_file_location('m',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
x=m.read(D/'manifest.json');d=m.read(D/'technical-native-diagnostics.json')
def results(v):
 if isinstance(v,dict):
  if 'exit_code' in v:yield v
  for a in v.values():yield from results(a)
 elif isinstance(v,list):
  for a in v:yield from results(a)
 elif isinstance(v,str):
  try:a=json.loads(v)
  except (ValueError,TypeError):return
  if a!=v:yield from results(a)
for a in [x['rootNativeAudit'],*x['actors'].values()]:
 native=pathlib.Path(a['nativeJournal'])
 if not native.exists():
  matches=list(pathlib.Path('/Users/eaafonasev/.codex/archived_sessions').rglob('*'+a['threadId']+'.jsonl'));assert len(matches)==1;native=matches[0]
 rows=[json.loads(l) for l in native.open()];assert next(r['payload']['id'] for r in rows if r['type']=='session_meta')==a['threadId']
 calls={r['payload']['call_id']:(i,r) for i,r in enumerate(rows,1) if r.get('payload',{}).get('type')=='custom_tool_call'}
 bad=[]
 for i,r in enumerate(rows,1):
  p=r.get('payload',{})
  if p.get('type')!='custom_tool_call_output':continue
  nonzero=[v['exit_code'] for v in results(p.get('output')) if v['exit_code'] not in [None,0]]
  if not nonzero:continue
  line,call=calls[p['call_id']];bad.append({'callLine':line,'originalCall':call,'resultLine':i,'originalResult':r,'exitCodes':nonzero})
 d['actors'][a['threadId']]={'native':str(native),'originalNativePath':a['nativeJournal'],'actualCompactions':sum(r['type']=='compacted' for r in rows),'nonzeroOriginals':bad}
m.write(D/'technical-native-diagnostics.json',d)
print(m.savecode([pathlib.Path(__file__),D/'technical-native-diagnostics.json'],'Preserve original native nonzero diagnostics through bounded closure'))
print({k:len(v['nonzeroOriginals']) for k,v in d['actors'].items()})
