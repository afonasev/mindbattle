"""Preserve supplemental original evidence without curing earlier diagnostics."""
import pathlib,json,importlib.util
D=pathlib.Path(__file__).parent
s=importlib.util.spec_from_file_location('m',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
x=m.read(D/'manifest.json');rows=[json.loads(l) for l in pathlib.Path(x['successorNativeJournal']).open()]
root=[json.loads(l) for l in pathlib.Path(x['rootNativeAudit']['nativeJournal']).open()]
def results(v):
 if isinstance(v,dict):
  if 'exit_code' in v and 'output' in v:yield v;return
  for a in v.values():yield from results(a)
 elif isinstance(v,list):
  for a in v:yield from results(a)
 elif isinstance(v,str):
  try:a=json.loads(v)
  except ValueError:return
  if a!=v:yield from results(a)
calls={r['payload']['call_id']:(i,r) for i,r in enumerate(rows,1) if r.get('payload',{}).get('type')=='custom_tool_call'}
supp=[];failed=[]
for i,r in enumerate(rows,1):
 p=r.get('payload',{})
 if p.get('type')!='custom_tool_call_output':continue
 rr=list(results(p.get('output')))
 if not rr:continue
 cl,call=calls[p['call_id']];e={'callLine':cl,'call':call,'resultLine':i,'result':r}
 if any(v['exit_code'] not in [0,None] for v in rr):failed.append(e)
 if cl>=214:supp.append((e,rr))
assert len(supp)==4 and len(failed)==3
for e,rr in supp:assert len(rr)==1 and rr[0]['exit_code']==0 and not any(t in rr[0]['output'] for t in ['Warning: truncated output','Output exceeded available model context'])
identity=json.loads(supp[0][1][0]['output'])
assert identity['verifiedSessionMetaId']==x['successorThreadId'] and identity['actualCompactions']==0
for key in ['originalCreateCall','originalCreateOutput']:
 assert identity[key]==root[identity[key+'Line']-1]
assert identity['originalCreateCall']['payload']['call_id']==identity['originalCreateOutput']['payload']['call_id']
for (e,rr),name in zip(supp[1:],['session-efficiency.md','game-execution.md','task-cleanup.md']):
 p=pathlib.Path('/Users/eaafonasev/.codex/references')/name
 assert rr[0]['output']==p.read_text()
 assert e['call']['payload']['input'].strip()=="text(await tools.exec_command({cmd:'cat "+str(p)+"',max_output_tokens:12000}));"
assert sum(r['type']=='compacted' for r in rows)==0
assert not (D.parent/('coordinator-'+x['successorThreadId'][:8])).exists()
deviations={'successor':x['successorThreadId'],'native':x['successorNativeJournal'],'originalFailedCalls':failed,'initialOriginalTruncationCallLines':[17,44,75],'initialOriginalTruncationRecords':[{'callLine':n,'call':rows[n-1],'matchedOutputs':[r for r in rows if r.get('payload',{}).get('type')=='custom_tool_call_output' and r['payload']['call_id']==rows[n-1]['payload']['call_id']]} for n in [17,44,75]],'otherUncuredDeviations':{'filteredIdentityCallLine':111,'excessKeysHelperPointersCallLines':[44,118,125],'excessHistoricalFenceOutputCallLines':[134,139],'batchTruncationCallLine':75},'allOriginalDeviationsUncured':True,'laterSuccessfulReadsAreProspectiveEvidenceOnly':True}
m.write(D/'successor-bootstrap-procedural-deviations.json',deviations)
audit={'successor':x['successorThreadId'],'native':x['successorNativeJournal'],'initialPersonallyAuditedExecCalls':26,'initialActualExecCommandDispatches':41,'supplementalWholeOriginalCalls':[e for e,rr in supp],'supplementalSuccessfulExecCommandDispatches':4,'actualCompactions':0,'originalIdentityPairPersonallyCompared':True,'commonThreeWholeOriginalBodiesEqualFiles':True,'initialCodeReview':'All 26 initial exec inputs personally inspected before handoff. Python imports and subprocess targets read-only; controlled reexecution inspected as read-only. No mutation APIs or shell writes. Supplemental exact four inputs are read-only.','actualFileMutations':0,'claimsLeasesMutations':0,'newActorsSOURCEQA':0,'successorOwnedDirectoryAbsent':True,'originalDiagnosticsUncured':str(D/'successor-bootstrap-procedural-deviations.json')}
m.write(D/'successor-readonly-supplemental-audit.json',audit)
comp=[{'line':i,'record':r} for i,r in enumerate(root,1) if r['type']=='compacted']
late={'owner':m.O,'actualCompactions':len(comp),'compactionRecords':comp,'contextTruncationObservation':'Original wait_threads output exceeded available model context during supplemental ACK wait; first compaction occurred after closed SOURCE43..46 slice. This is output/context truncation, not an exec_command failure.','closedSliceActualCompactions':0,'originalDiagnosticsUncured':True,'noNewSOURCEAfterClosedSlice':True,'oneReplacementOnly':x['successorThreadId']}
m.write(D/'handoff-first-compaction.json',late)
diag=m.read(D/'own-procedural-diagnostics.json');diag.update(handoffFirstCompaction=str(D/'handoff-first-compaction.json'),handoffFirstCompactionSHA256=m.raw(D/'handoff-first-compaction.json'),currentRootActualCompactions=len(comp),laterContextOutputTruncationObserved=True);m.write(D/'own-procedural-diagnostics.json',diag)
for p in [D/'manifest.json',D/'handoff-next.json']:
 a=m.read(p);a['rootNativeAudit']['actualCompactions']=len(comp);a['rootNativeAudit']['closedSliceActualCompactions']=0;a['handoffFirstCompaction']=str(D/'handoff-first-compaction.json');a['successorSupplementalAudit']=str(D/'successor-readonly-supplemental-audit.json');m.write(p,a)
paths=[pathlib.Path(__file__)]+[D/n for n in ['successor-bootstrap-procedural-deviations.json','successor-readonly-supplemental-audit.json','handoff-first-compaction.json','own-procedural-diagnostics.json','manifest.json','handoff-next.json']]
print(m.savecode(paths,'Preserve successor supplemental readonly evidence and first handoff compaction'))
print({'supplementalWholeOriginalReads':4,'successorActualCompactions':0,'parentActualCompactions':len(comp),'originalFailuresUncured':3,'originalTruncationsUncured':3})
