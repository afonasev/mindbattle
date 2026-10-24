"""Read only the exact original create call/result and returned-ID journal."""
import json
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
title = sys.argv[2]
rows = [json.loads(line) for line in root.open()]
prefix = 'text(await tools.mcp__codex_app__create_thread({title:' + json.dumps(title, ensure_ascii=False)
calls = [(i, row) for i, row in enumerate(rows, 1)
         if row.get('type') == 'response_item'
         and row.get('payload', {}).get('type') == 'custom_tool_call'
         and any(line.startswith(prefix) for line in row['payload'].get('input', '').splitlines())]
assert len(calls) == 1
call_line, call = calls[0]
call_id = call['payload']['call_id']
outputs = [(i, row) for i, row in enumerate(rows, 1)
           if row.get('type') == 'response_item'
           and row.get('payload', {}).get('type') == 'custom_tool_call_output'
           and row['payload'].get('call_id') == call_id]
assert len(outputs) == 1
output_line, output = outputs[0]
found, errors = [], []

def decode(value, pointer=''):
    if isinstance(value, str):
        text = value.strip()
        if not text.startswith(('{', '[')):
            return
        try:
            child = json.loads(text)
        except json.JSONDecodeError as error:
            errors.append({'pointer': pointer, 'error': str(error)})
            if not text.startswith('{\\"'):
                return
            child = json.loads(text.replace('\\"', '"'))
        decode(child, pointer + '/decoded')
    elif isinstance(value, dict):
        if 'exit_code' in value and 'output' in value:
            return
        assert not value.get('isError')
        if isinstance(value.get('threadId'), str) and isinstance(value.get('hostId'), str):
            found.append((pointer, value))
            return
        for key, child in value.items():
            decode(child, pointer + '/' + str(key))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            decode(child, pointer + '/' + str(index))

decode(output['payload']['output'])
assert len(found) == 1
pointer, created = found[0]
uid = created['threadId']
paths = list(pathlib.Path('/Users/eaafonasev/.codex/sessions').glob('**/*' + uid + '.jsonl'))
if not paths:
    paths = list(pathlib.Path('/Users/eaafonasev/.codex/archived_sessions').glob('**/*' + uid + '.jsonl'))
assert len(paths) == 1
native = [json.loads(line) for line in paths[0].open()]
assert [row['payload']['id'] for row in native if row.get('type') == 'session_meta'] == [uid]
compactions = sum(row.get('type') == 'compacted' for row in native)
assert compactions == 0
print(json.dumps({'originalCreateCallLine': call_line, 'originalCreateCall': call,
                  'originalCreateOutputLine': output_line, 'originalCreateOutput': output,
                  'decodedResultPointer': pointer, 'decodedResult': created,
                  'decodeErrorsPreserved': errors, 'nativeJournal': str(paths[0]),
                  'verifiedSessionMetaId': uid, 'actualCompactions': compactions}, ensure_ascii=False))
