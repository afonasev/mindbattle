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
    report['actors'].update(m.read(D/'technical-native-diagnostics.json')['actors'])
for actor in [x['rootNativeAudit'], *x['actors'].values(), *x.get('retiredNativeReviewersCurrentOwner',[])]:
    native = pathlib.Path(actor['nativeJournal'])
    if not native.exists():
        matches = list(pathlib.Path('/Users/eaafonasev/.codex/archived_sessions').rglob('*'+actor['threadId']+'.jsonl'))
        assert len(matches)==1
        native = matches[0]
    rows = [json.loads(line) for line in native.open()]
    assert [r['payload']['id'] for r in rows if r['type']=='session_meta']==[actor['threadId']]
    calls = {r['payload']['call_id']:(i,r) for i,r in enumerate(rows,1) if r.get('payload',{}).get('type')=='custom_tool_call'}
    bad, truncated = [], []
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
        evidence = {'callLine':call_line,'originalCall':call,'resultLine':line,'originalResult':row,'exitCodes':codes,'legacyOutputOnlyExitCode':legacy,'scriptFailed':script_failed}
        if codes or script_failed:
            bad.append(evidence)
        outputs = [v['output'] for v in structured if isinstance(v.get('output'),str)]
        if any(t.startswith('Warning: truncated output') for t in texts+outputs):
            truncated.append(evidence)
    report['actors'][actor['threadId']] = {'native':str(native),'originalNativePath':actor['nativeJournal'],'actualCompactions':sum(r['type']=='compacted' for r in rows),'nonzeroOriginals':bad,'truncatedOriginals':truncated}
out = D/'technical-native-diagnostics.json'
m.write(out,report)
print(m.savecode([pathlib.Path(__file__),out],'Preserve exact structured and legacy native diagnostics without replay'))
print({sid:{'actualCompactions':a['actualCompactions'],'nonzero':len(a['nonzeroOriginals']),'truncated':len(a['truncatedOriginals'])} for sid,a in report['actors'].items()})
