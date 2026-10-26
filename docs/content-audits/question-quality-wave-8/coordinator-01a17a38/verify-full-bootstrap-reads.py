"""Bind actual whole policy results before START; no content review or compliance cure."""
import pathlib, json, importlib.util, sys
D = pathlib.Path(__file__).parent
s = importlib.util.spec_from_file_location('m', D/'owned-tools.py')
m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
key, label, cursor = sys.argv[1:4]
x = m.read(D/'manifest.json'); actor = x['actors'][key]
native = pathlib.Path(actor['nativeJournal'])
rows = [json.loads(line) for line in native.open()]
assert [r['payload']['id'] for r in rows if r.get('type') == 'session_meta'] == [actor['threadId']]
assert sum(r.get('type') == 'compacted' for r in rows) == 0
calls = {r['payload']['call_id']: (i, r['payload']['input']) for i, r in enumerate(rows, 1)
         if r.get('type') == 'response_item' and r.get('payload', {}).get('type') == 'custom_tool_call'}
primary = pathlib.Path('/Users/eaafonasev/Projects/mindbattle')
expected = [(primary/p, None) for p in ['AGENTS.md', '.agents/references/context-efficiency.md',
    '.agents/references/model-routing.md', '.agents/references/execution-policy.md']]
expected += [(m.C/'AGENTS.md', None), (m.C/'docs/content-audits/question-authoring-guide-2026-09-02.md', None)]
expected += [(pathlib.Path('/Users/eaafonasev/.codex/references')/p, None)
             for p in ['session-efficiency.md', 'game-execution.md', 'task-cleanup.md']]
expected += [(m.P/'docs/GAME_SPEC.md', (135, 285)),
             (m.P/'openspec/specs/question-catalog/spec.md', (21, 33))]
proof = []
for path, span in expected:
    body = path.read_text(); needle = 'cat '+str(path)
    if span:
        body = ''.join(body.splitlines(keepends=True)[span[0]-1:span[1]])
        needle = "sed -n '"+str(span[0])+','+str(span[1])+"p' "+str(path)
    needles = [needle]
    if span:
        needles.append("cat "+str(path)+" | sed -n "+chr(39)+str(span[0])+","+str(span[1])+"p"+chr(39))
    matches = []
    for line, row in enumerate(rows, 1):
        p = row.get('payload', {}); call = calls.get(p.get('call_id'))
        # JS single-quoted command strings escape the sed apostrophes. This is
        # only a locator comparison; exact output bytes remain authoritative.
        invocation = call[1].replace("\\'", "'") if call else ''
        if row.get('type') != 'response_item' or p.get('type') != 'custom_tool_call_output' or not call or not any(n in invocation for n in needles):
            continue
        blocks = p.get('output', [])
        if not isinstance(blocks, list):
            blocks = [blocks]
        for block in blocks:
            value = block.get('text', '') if isinstance(block, dict) else block
            if not isinstance(value, str):
                continue
            try:
                result = json.loads(value)
            except ValueError:
                continue
            if isinstance(result, dict) and result.get('exit_code') == 0 and result.get('output', '').strip() == body.strip():
                matches.append({'path': str(path), 'span': span, 'callLine': call[0], 'resultLine': line,
                                'resultCanonicalSHA256': m.sha(row)})
    assert matches, ('No actual complete exit0 policy read', str(path))
    proof.extend(matches)
event = next(r['payload']['type'] for r in reversed(rows) if r.get('type') == 'event_msg'
             and r.get('payload', {}).get('type') in ['task_started', 'task_complete'])
assert event == 'task_complete'
info = next(r['payload']['info'] for r in reversed(rows) if r.get('payload', {}).get('type') == 'token_count')
out = D/(label+'-full-bootstrap-read-proof.json'); assert not out.exists()
m.write(out, {'owner': m.O, 'nativeId': actor['threadId'], 'wholeMandatoryAndCanonicalReads': proof,
              'actualCompactions': 0, 'qualityCredit': 0, 'noOriginalComplianceCure': True})
actor.update(stage='IDLE_BOOTSTRAP_ACK_VERIFIED', lastTaskEvent=event, nativePreflightVerifiedBy=m.O,
             lastInput=info['last_token_usage']['input_tokens'], modelWindow=info['model_context_window'], cursor=cursor)
x['bootstrapQueueCurrentOwner'] = [v for v in x['bootstrapQueueCurrentOwner'] if v['threadId'] != actor['threadId']]
m.write(D/'manifest.json', x)
print(m.savecode([out, D/'manifest.json', pathlib.Path(__file__)], 'Bind actual whole bootstrap policy reads before START'))
print({'nativeId': actor['threadId'], 'actualCompactions': 0, 'lastInput': actor['lastInput'],
       'window': actor['modelWindow'], 'remaining': actor['modelWindow']-actor['lastInput']})
