"""Freeze exact current author procedural originals; no quality judgment."""
import pathlib,json,importlib.util,sys,re
D=pathlib.Path(__file__).parent
s=importlib.util.spec_from_file_location('m',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
order=int(sys.argv[1]);suffix=sys.argv[2] if len(sys.argv)>2 else '';assert suffix in ['', '-cycle1'];x=m.read(D/'manifest.json');actor_key=sys.argv[3] if len(sys.argv)>3 else 'author'+str(order);a=x['actors'][actor_key];p=pathlib.Path(a['nativeJournal'])
assert m.read(D/f'source-cars-road-transport{order}-task.json')['authorNativeId']==a['threadId']
if not p.exists():
 matches=list(pathlib.Path('/Users/eaafonasev/.codex/archived_sessions').glob('*'+a['threadId']+'.jsonl'));assert len(matches)==1;p=matches[0]
rs=[json.loads(l) for l in p.open()];assert [r['payload']['id'] for r in rs if r['type']=='session_meta']==[a['threadId']]
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
calls={r['payload']['call_id']:(i,r) for i,r in enumerate(rs,1) if r.get('payload',{}).get('type')=='custom_tool_call'};bad=[];trunc=[]
for i,r in enumerate(rs,1):
 a=r.get('payload',{})
 if a.get('type')!='custom_tool_call_output' or a['call_id'] not in calls:continue
 line,c=calls[a['call_id']];v=list(results(a.get('output')));blocks=a.get('output',[]);texts=[z.get('text','') for z in blocks if isinstance(z,dict)] if isinstance(blocks,list) else []
 codes=[z['exit_code'] for z in v if z['exit_code'] not in [0,None]];failed=any(t.startswith('Script failed') for t in texts)
 raw={'callLine':line,'originalCall':c,'resultLine':i,'originalResult':r,'exitCodes':codes,'scriptFailed':failed}
 if codes or failed:bad.append(raw)
 actual=any(t.startswith('Warning: truncated output') for t in texts)
 for z in v:
  b=z.get('output','');match=re.match(r'Warning: truncated output \(original token count: (\d+)\)',b) if isinstance(b,str) else None
  if match and int(match[1])==z.get('original_token_count'):actual=True
 if actual:trunc.append(raw)
lastTurnStart=max(i for i,r in enumerate(rs,1) if r['type']=='event_msg' and r.get('payload',{}).get('type')=='task_started');taskStart=lastTurnStart
continuation=x.get('pendingCarsRoadTransport'+str(order),{}).get('cycle1Continuation') if suffix else None
if continuation:
 continued=m.read(continuation);assert continued['sourceNativeId']==x['actors'][actor_key]['threadId']
 taskStart=continued['firstTaskStartLine'];assert taskStart<=lastTurnStart and rs[taskStart-1]==continued['originalFirstTaskStarted']
out=D/f'source{order}{suffix}-procedural-diagnostics.json';assert not out.exists();m.write(out,{'taskStartLine':taskStart,'lastTaskTurnStartLine':lastTurnStart,'sameCycleContinuation':continuation,'newTaskNonzero':sum(z['callLine']>taskStart for z in bad),'newTaskTruncated':sum(z['callLine']>taskStart for z in trunc),'owner':m.O,'sourceNativeId':x['actors'][actor_key]['threadId'],'nativeJournalActual':str(p),'actualCompactions':sum(r['type']=='compacted' for r in rs),'nonzeroOriginals':bad,'truncatedOriginals':trunc,'allUncured':True,'noEmbeddedHistoricalExecutionsCountedAsNew':True})
entry=x['pendingCarsRoadTransport'+str(order)];entry['cycle1ProceduralDeviations' if suffix else 'proceduralDeviations']={'path':str(out),'rawSHA256':m.raw(out),'uncured':True,'nonzeroOriginals':len(bad),'truncatedOriginals':len(trunc),'contentPASSAndQAdoNotAssertProceduralCompliance':True};m.write(D/'manifest.json',x)
print(m.savecode([pathlib.Path(__file__),out,D/'manifest.json'],'Preserve exact author procedural originals separately from content credit'))
print({'order':order,'nonzeroOriginals':len(bad),'truncatedOriginals':len(trunc),'UNCURED':True})
