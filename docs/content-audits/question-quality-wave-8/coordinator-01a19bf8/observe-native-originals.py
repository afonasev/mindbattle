"""Bounded cumulative native originals, stopping at actual structured exec results."""
import pathlib, json, importlib.util, sys, re
D = pathlib.Path(__file__).parent
s = importlib.util.spec_from_file_location('m', D/'owned-tools.py')
m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
x = m.read(D/'manifest.json'); name = sys.argv[1]
predecessor = pathlib.Path(x['predecessorHandoff']).parent
previous=m.read(x['predecessorHandoff'])
assert pathlib.Path(previous['technicalNativeOriginals']).is_file()
assert pathlib.Path(name).name == name and name.endswith('.json')
out = D/name; assert not out.exists()
actors = {}
for actor in [x['rootNativeAudit'], *x['actors'].values()]:
    uid = actor['threadId']; p = pathlib.Path(actor['nativeJournal'])
    if not p.is_file():
        matches = list(pathlib.Path('/Users/eaafonasev/.codex/archived_sessions').glob('**/*'+uid+'.jsonl'))
        assert len(matches) == 1; p = matches[0]
    rows = [json.loads(line) for line in p.open()]
    assert [r['payload']['id'] for r in rows if r.get('type') == 'session_meta'] == [uid]
    calls = {r['payload']['call_id']: (i, r) for i, r in enumerate(rows, 1)
             if r.get('type') == 'response_item' and r.get('payload', {}).get('type') == 'custom_tool_call'}
    bad, truncated, projected = [], [], []
    for line, row in enumerate(rows, 1):
        payload = row.get('payload', {}); call = calls.get(payload.get('call_id'))
        if row.get('type') != 'response_item' or payload.get('type') != 'custom_tool_call_output' or not call:
            continue
        ref = {'journal': str(p), 'callLine': call[0], 'resultLine': line,
               'call_id': payload['call_id'], 'callCanonicalSHA256': m.sha(call[1]),
               'resultCanonicalSHA256': m.sha(row), 'uncured': True}
        value = payload.get('output'); blocks = value if isinstance(value, list) else [value]
        call_input=call[1]['payload'].get('input','')
        # Ignore quoted shell programs/comments; retain real same-line projections.
        # Earlier snapshots stay immutable, including their regex false positives.
        outer_js=re.sub(r"'(?:\\.|[^'\\])*'|\"(?:\\.|[^\"\\])*\"|`(?:\\.|[^`\\])*`",' ',call_input,flags=re.S)
        outer_js=re.sub(r'//[^\n]*|/\*.*?\*/',' ',outer_js,flags=re.S)
        projected_exec='tools.exec_command(' in outer_js and bool(re.search(r'\btext\(\s*[A-Za-z_$][A-Za-z0-9_$]*\.output\s*\)',outer_js))
        if projected_exec:projected.append(ref)
        codes, cut = [], False
        for block in blocks:
            text = block.get('text', '') if isinstance(block, dict) else block
            if not isinstance(text, str):
                continue
            if text.startswith('Warning: truncated output'):
                cut = True; continue
            if projected_exec:continue  # Projected stdout has no original exec status.
            try:
                result = json.loads(text)
            except (ValueError, TypeError):
                continue
            if not isinstance(result, dict) or 'exit_code' not in result or 'output' not in result:
                continue
            # stdout is arbitrary data. Never recursively decode it as execution.
            if result['exit_code'] not in [0, None]:
                codes.append(result['exit_code'])
            if result.get('output', '').startswith('Warning: truncated output'):
                cut = True
        if codes:
            bad.append({**ref, 'exitCodes': codes})
        if cut:
            truncated.append(ref)
    info = next(r['payload']['info'] for r in reversed(rows)
                if r.get('payload', {}).get('type') == 'token_count')
    event = next(r['payload']['type'] for r in reversed(rows)
                 if r.get('type') == 'event_msg' and r.get('payload', {}).get('type') in ['task_started', 'task_complete'])
    actors[uid] = {'nativeJournal': str(p), 'originalNativePath': actor['nativeJournal'],
                   'actualCompactions': sum(r.get('type') == 'compacted' for r in rows),
                   'nonzeroExecResults': sum(len(v['exitCodes']) for v in bad),
                   'failingCustomToolCalls': len(bad), 'truncatedToolCalls': len(truncated),
                   'nonzeroOriginals': bad, 'truncatedOriginals': truncated,
                   'projectedExecStatusGaps': projected,
                   'projectedExecStatusGapCount': len(projected),
                   'lastTaskEvent': event, 'lastInput': info['last_token_usage']['input_tokens'],
                   'window': info['model_context_window'],
                   'remaining': info['model_context_window']-info['last_token_usage']['input_tokens']}
m.write(out, {'owner': m.O, 'actors': actors,
              'bootstrapSnapshotImmutable': x['bootstrapOriginalsImmutable'],
              'cumulativeTechnicalOriginals': str(D/'technical-native-originals.json'),
              'priorOwnSnapshotImmutable': x.get('latestOwnOriginalsSnapshot'),
              'inheritedRootAccountingImmutable': previous['technicalNativeOriginals'],
              'inheritedRootProceduralDiagnosticsImmutable': str(predecessor/'own-procedural-diagnostics.json') if (predecessor/'own-procedural-diagnostics.json').exists() else None,
              'inheritedLateOriginalsImmutable': str(predecessor/'late-handoff-compaction-caveat.json') if (predecessor/'late-handoff-compaction-caveat.json').exists() else None,
              'rootReadScopeDeviationUNCURED': m.read(D/'technical-native-originals.json')['readScopeDeviations'],
              'ownRootProceduralAppendices': x['ownRootProceduralAppendices'],
              'stdoutEmbeddedExitCodesAreDataNotExecutions': True,
              'allOriginalsUncured': True, 'noReplayOrIdentityModelBudgetReset': True})
print(m.savecode([out, pathlib.Path(__file__)], 'Preserve cumulative exact own native originals without replay'))
print({k: {field: v[field] for field in ['actualCompactions', 'nonzeroExecResults',
        'failingCustomToolCalls', 'truncatedToolCalls', 'projectedExecStatusGapCount', 'lastTaskEvent', 'lastInput', 'remaining']}
       for k, v in actors.items()})
