"""Save exact current independent-stage technical originals without semantic review."""
from pathlib import Path
import importlib.util,json,re,sys
D=Path(__file__).parent
s=importlib.util.spec_from_file_location('m',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
order=int(sys.argv[1]);stage=sys.argv[2];assert stage in ['initial','final']
x=m.read(D/'manifest.json');a=x['actors']['reviewer'];audit=m.read(D/f'reader{order}-{stage}-native-network-audit.json')
rows=[json.loads(l) for l in Path(a['nativeJournal']).open()]
assert audit['readerNativeId']==a['threadId'] and audit['lastTaskEvent']=='task_complete'
calls={r['payload']['call_id']:(i,r) for i,r in enumerate(rows,1) if r.get('payload',{}).get('type')=='custom_tool_call'}
def results(v):
 if isinstance(v,dict):
  if 'exit_code' in v and 'output' in v:yield v;return
  for z in v.values():yield from results(z)
 elif isinstance(v,list):
  for z in v:yield from results(z)
 elif isinstance(v,str):
  try:z=json.loads(v)
  except (ValueError,TypeError):return
  if z!=v:yield from results(z)
bad=[];trunc=[]
for i,r in enumerate(rows,1):
 p=r.get('payload',{})
 if i<=audit['taskStartLine'] or p.get('type')!='custom_tool_call_output' or p['call_id'] not in calls:continue
 line,c=calls[p['call_id']];v=list(results(p.get('output')));blocks=p.get('output',[]);texts=[z.get('text','') for z in blocks if isinstance(z,dict)] if isinstance(blocks,list) else []
 codes=[z['exit_code'] for z in v if z['exit_code'] not in [0,None]]
 proof={'callLine':line,'originalCall':c,'resultLine':i,'originalResult':r,'exitCodes':codes}
 if codes or any(t.startswith('Script failed') for t in texts):bad.append(proof)
 actual=any(t.startswith('Warning: truncated output') for t in texts)
 for z in v:
  match=re.match(r'Warning: truncated output \(original token count: (\d+)\)',z['output']) if isinstance(z['output'],str) else None
  if match and int(match[1])==z.get('original_token_count'):actual=True
 if actual:trunc.append(proof)
out=D/f'reader{order}-{stage}-procedural-diagnostics.json';assert not out.exists()
m.write(out,{'owner':m.O,'readerNativeId':a['threadId'],'taskStartLine':audit['taskStartLine'],'nonzeroOriginals':bad,'truncatedOriginals':trunc,'allUncured':True,'scope':'This exact stage only; old embedded error/warning content is data, not execution'})
if '--appendix-only' in sys.argv:
 assert (D/f'certification-cars-road-transport{order}.json').is_file()
 print(m.savecode([Path(__file__),out],'Preserve reader procedural appendix after certification without changing case or certificate'))
 print({'order':order,'stage':stage,'nonzeroOriginals':len(bad),'truncatedOriginals':len(trunc),'UNCURED':True,'caseUnchanged':True})
 raise SystemExit(0)
case=D/f'case-cars-road-transport{order}-{stage}-{audit["status"].lower()}.json';v=m.read(case)
v['reportBase']['readerProceduralDeviations']={'path':str(out),'rawSHA256':m.raw(out),'newNonzeroOriginals':len(bad),'newTruncatedOriginals':len(trunc),'uncured':True,'contentPASSAndQAdoNotAssertProceduralCompliance':True}
m.write(case,v)
print(m.savecode([Path(__file__),out,case],'Preserve exact independent-stage diagnostics without procedural cure'))
print({'order':order,'stage':stage,'nonzeroOriginals':len(bad),'truncatedOriginals':len(trunc),'UNCURED':True})
