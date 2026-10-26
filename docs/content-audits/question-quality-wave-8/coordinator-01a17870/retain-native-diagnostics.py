"""Preserve exact immediate native failures, including output-only legacy calls."""
import importlib.util, json, pathlib, re
D = pathlib.Path(__file__).parent
s = importlib.util.spec_from_file_location('owned', D/'owned-tools.py')
m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
x = m.read(D/'manifest.json')

def command_results(value):
    if isinstance(value, dict):
        if 'exit_code' in value and 'output' in value:
            yield value
            return  # Returned source/diagnostic JSON is data, not another command.
        for item in value.values():
            yield from command_results(item)
    elif isinstance(value, list):
        for item in value:
            yield from command_results(item)
    elif isinstance(value, str):
        try:
            decoded = json.loads(value)
        except (ValueError, TypeError):
            return
        if decoded != value:
            yield from command_results(decoded)

report = {'owner':m.O, 'actors':{}, 'inheritedDiagnostics':str(pathlib.Path(x['predecessorHandoff']).parent/'technical-native-diagnostics.json'), 'meaning':'Exact original technical diagnostics only; no source retry or quality credit.'}
if (D/'technical-native-diagnostics.json').exists():
    report['priorDiagnosticPointer'] = str(D/'technical-native-diagnostics.json')
for actor in [x['rootNativeAudit'], *x['actors'].values(), *x.get('retiredNativeReviewersCurrentOwner',[])]:
    if isinstance(actor,str):
        matches=[m.read(p) for p in D.glob('reader*-retirement.json') if m.read(p).get('readerNativeId')==actor]
        assert len(matches)==1, 'Retired native ID requires unique exact retirement binding'
        actor={'threadId':actor,'nativeJournal':matches[0]['nativeJournal']}
    native = pathlib.Path(actor['nativeJournal'])
    if not native.exists():
        matches = list(pathlib.Path('/Users/eaafonasev/.codex/archived_sessions').rglob('*'+actor['threadId']+'.jsonl'))
        assert len(matches)==1
        native = matches[0]
    rows = [json.loads(line) for line in native.open()]
    assert [r['payload']['id'] for r in rows if r['type']=='session_meta']==[actor['threadId']]
    calls = {r['payload']['call_id']:(i,r) for i,r in enumerate(rows,1) if r.get('payload',{}).get('type')=='custom_tool_call'}
    bad, truncated, inherited_warning_data = [], [], []
    own_reader_starts = [m.read(p)['taskStartLine'] for p in D.glob('reader*-native-network-audit.json') if m.read(p).get('readerNativeId') == actor['threadId']]
    first_own_reader_start = min(own_reader_starts) if own_reader_starts else None
    created_here = actor['threadId'] == m.O or actor['threadId'] in x['createdNativeThreadsCurrentOwner']
    inherited_actor = not created_here and first_own_reader_start is None
    for line, row in enumerate(rows,1):
        p = row.get('payload',{})
        if p.get('type')!='custom_tool_call_output' or p['call_id'] not in calls:
            continue
        structured = list(command_results(p.get('output')))
        codes = [v['exit_code'] for v in structured if v['exit_code'] not in (0,None)]
        blocks = p.get('output',[])
        texts = [v.get('text','') for v in blocks if isinstance(v,dict)] if isinstance(blocks,list) else []
        legacy = [int(t.split('=',1)[1]) for t in texts if re.fullmatch(r'exit_code=-?\d+',t)]
        codes += [v for v in legacy if v!=0]
        script_failed = any(t.startswith('Script failed') for t in texts)
        call_line, call = calls[p['call_id']]
        evidence = {'nativeJournal':str(native),'callLine':call_line,'originalCallCanonicalSHA256':m.sha(call),'resultLine':line,'originalResultCanonicalSHA256':m.sha(row),'call_id':p['call_id'],'exitCodes':codes,'legacyOutputOnlyExitCode':legacy,'scriptFailed':script_failed,'inheritedBeforeCurrentOwner':inherited_actor or (not created_here and first_own_reader_start is not None and call_line < first_own_reader_start)}
        if codes or script_failed:
            bad.append(evidence)
        actual_truncation = any(t.startswith('Warning: truncated output') for t in texts)
        for result in structured:
            output = result.get('output','')
            if not isinstance(output,str):continue
            match = re.match(r'Warning: truncated output \(original token count: (\d+)\)',output)
            if match:
                if int(match[1]) == result.get('original_token_count'):actual_truncation = True
                else:inherited_warning_data.append({'nativeJournal':str(native),'resultLine':line,'currentOriginalTokenCount':result.get('original_token_count'),'inheritedWarningTokenCount':int(match[1]),'originalResultCanonicalSHA256':m.sha(row),'notNewTruncation':True})
        if actual_truncation:truncated.append(evidence)
    report['actors'][actor['threadId']] = {'native':str(native),'originalNativePath':actor['nativeJournal'],'actualCompactions':sum(r['type']=='compacted' for r in rows),'nonzeroOriginals':bad,'truncatedOriginals':truncated,'inheritedWarningData':inherited_warning_data,'newCurrentOwnerNonzero':sum(not v['inheritedBeforeCurrentOwner'] for v in bad),'newCurrentOwnerTruncated':sum(not v['inheritedBeforeCurrentOwner'] for v in truncated)}
out = D/'closed-slice-diagnostics.json'
assert not out.exists(), 'Closed original diagnostics are immutable; no overwrite'
report['originalResolution']='Exact journal/line/call_id and canonical record digests, no history copy. If a journal moves on archive, resolve only its exact native-ID filename and verify session_meta.id before reading.'
m.write(out,report)
summary = D/'own-procedural-diagnostics.json'
m.write(summary,{'owner':m.O,'closedOriginals':str(out),'closedOriginalsSHA256':m.raw(out),'earlierOriginalSnapshot':str(D/'technical-native-originals.json'),'earlierOriginalSnapshotSHA256':m.raw(D/'technical-native-originals.json'),'actors':{sid:{'actualCompactions':a['actualCompactions'],'nonzeroOriginals':len(a['nonzeroOriginals']),'truncatedOriginals':len(a['truncatedOriginals']),'newCurrentOwnerNonzero':a['newCurrentOwnerNonzero'],'newCurrentOwnerTruncated':a['newCurrentOwnerTruncated'],'inheritedWarningData':len(a['inheritedWarningData'])} for sid,a in report['actors'].items()},'allOriginalDiagnosticsUncured':True,'noEmbeddedHistoricalExecutionsCountedAsNew':True})
x.update(ownProceduralDiagnostics=str(summary),closingTechnicalDiagnostics=str(out),technicalNativeOriginals=str(D/'technical-native-originals.json'),technicalNativeOriginalsSHA256=m.raw(D/'technical-native-originals.json'))
m.write(D/'manifest.json',x)
print(m.savecode([pathlib.Path(__file__),out,summary,D/'manifest.json'],'Preserve exact structured and legacy native diagnostics without replay'))
print({sid:{'actualCompactions':a['actualCompactions'],'nonzero':len(a['nonzeroOriginals']),'truncated':len(a['truncatedOriginals'])} for sid,a in report['actors'].items()})
