"""Append actual coordinator originals; never interpret embedded stdout as execution."""
import pathlib,json,importlib.util
D=pathlib.Path(__file__).parent
s=importlib.util.spec_from_file_location('m',D/'owned-tools.py')
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
x=m.read(D/'manifest.json');p=D/'technical-native-originals.json';a=m.read(p)
assert a['owner']==a['threadId']==x['rootNativeAudit']['threadId']==m.O
rows=[json.loads(l) for l in pathlib.Path(a['nativeJournal']).open()]
assert [r['payload']['id'] for r in rows if r['type']=='session_meta']==[m.O]
last=a['journalLinesThrough']
a['actualOriginals'] += [{'journalLine':i,'original':r} for i,r in enumerate(rows,1)
    if i>last and r['type']=='response_item' and r.get('payload',{}).get('type')
    in ['custom_tool_call','custom_tool_call_output']]
a['journalLinesThrough']=len(rows)
a['actualCompactions']=sum(r['type']=='compacted' for r in rows)
calls={r['payload']['call_id']:(i,r) for i,r in enumerate(rows,1)
       if r.get('payload',{}).get('type')=='custom_tool_call'}
bad=[];cut=[]
for i,r in enumerate(rows,1):
    q=r.get('payload',{});c=calls.get(q.get('call_id'))
    if q.get('type')!='custom_tool_call_output' or not c:continue
    codes=[];tr=False
    for b in q.get('output',[]):
        t=b.get('text','') if isinstance(b,dict) else b
        if not isinstance(t,str):continue
        if t.startswith('Warning: truncated output'):tr=True
        try:v=json.loads(t)
        except ValueError:continue
        candidates=[v] if isinstance(v,dict) else []
        if isinstance(v,dict) and isinstance(v.get('result'),dict):
            val=v['result'].get('value')
            if isinstance(val,dict):candidates.append(val)
        for z in candidates:
            if 'exit_code' in z and 'output' in z:
                if z['exit_code'] not in [None,0]:codes.append(z['exit_code'])
                if z['output'].startswith('Warning: truncated output'):tr=True
    ref={'callLine':c[0],'resultLine':i,'call_id':q['call_id'],
         'callCanonicalSHA256':m.sha(c[1]),'resultCanonicalSHA256':m.sha(r),'uncured':True}
    if codes:bad.append({**ref,'exitCodes':codes})
    if tr:cut.append(ref)
assert {v['call_id'] for v in a['nonzeroOriginalRefs']}<={v['call_id'] for v in bad}
assert {v['call_id'] for v in a['truncatedOriginalRefs']}<={v['call_id'] for v in cut}
a.update(observedStructuredNonzero=sum(len(v['exitCodes']) for v in bad),
         nonzeroOriginalRefs=bad,observedOuterOrStructuredTruncations=len(cut),truncatedOriginalRefs=cut)
m.write(p,a)
x['technicalNativeOriginalsSHA256']=m.raw(p);m.write(D/'manifest.json',x)
diag=D/'own-procedural-diagnostics.json'
m.write(diag,{'owner':m.O,'nativeJournal':a['nativeJournal'],'actualCompactions':a['actualCompactions'],
    'structuredNonzeroExec':a['observedStructuredNonzero'],'failingCustomToolCalls':len(bad),
    'explicitProjectedExecStatusGapOriginals':a.get('explicitProjectedExecStatusGapOriginals',[]),
    'explicitProjectedExecStatusGapCount':len(a.get('explicitProjectedExecStatusGapOriginals',[])),
    'fullFailureTotal':'UNKNOWN',
    'truncatedToolCalls':len(cut),'nonzeroOriginals':bad,'truncatedOriginals':cut,
    'readScopeDeviations':a['readScopeDeviations'],'allUncured':True,
    'bootstrapSnapshotHistoricalImmutable':x['bootstrapOriginalsImmutable'],
    'cumulativeOriginals':str(p),'rootFailuresAreNotAuthorFailures':True,
    'sourceOrReaderStdoutEmbeddedExitCodesAreData':True})
x['ownProceduralDiagnostics']=str(diag);m.write(D/'manifest.json',x)
print(m.savecode([p,diag,D/'manifest.json',pathlib.Path(__file__)],'Preserve cumulative own native originals without curing failures'))
print({'actualCompactions':a['actualCompactions'],'structuredNonzero':a['observedStructuredNonzero'],
       'truncatedCalls':len(cut),'readScopeDeviations':len(a['readScopeDeviations'])})
