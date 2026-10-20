"""Preserve an already printed full web.open native result; never fetch or grade."""
import pathlib, json, hashlib, re, sys
C = pathlib.Path(__file__).resolve().parents[4]
uid, url, target = sys.argv[1:4]
out = pathlib.Path(target).resolve()
assert out.is_relative_to(C / 'docs/content-audits/question-quality-wave-8')
assert not out.exists(), 'Never overwrite original capture'
base = pathlib.Path('/Users/eaafonasev/.codex/sessions')
paths = list(base.rglob('*' + uid + '.jsonl'))
paths += list(pathlib.Path('/Users/eaafonasev/.codex/archived_sessions').rglob('*' + uid + '.jsonl'))
assert len(paths) == 1, 'Missing or ambiguous native session'
found = None
calls = {}
for line, raw in enumerate(paths[0].open(), 1):
    r = json.loads(raw)
    if r.get('type') == 'session_meta':
        assert r['payload']['id'] == uid
    p = r.get('payload', {})
    if r.get('type') == 'response_item' and p.get('type') in {
            'custom_tool_call', 'function_call'}:
        calls[p.get('call_id')] = p
    if r.get('type') != 'response_item' or p.get('type') not in {
            'custom_tool_call_output', 'function_call_output'}:
        continue
    if not isinstance(p.get('output'), list):
        continue
    call = calls.get(p.get('call_id'), {})
    name = call.get('name', '')
    code = call.get('input', call.get('arguments', ''))
    # Printed helper code or a later sourceproof dump is not a web response.
    direct_web = 'web' in name and ('run' in name or 'open' in name)
    wrapper_web = isinstance(code, str) and bool(re.search(r'tools\.web__run\s*\(', code))
    if not (direct_web or wrapper_web):
        continue
    for k, item in enumerate(p['output']):
        text = item.get('text', '')
        for document in re.split(r'\n-{20,}\n', text):
            first_line = re.search(r'(?:^|\n)L\d+(?:@P\d+)?:', document)
            if first_line is None:
                continue
            header = document[:first_line.start()]
            if url in header and 'Source: open(' in header and len(re.findall(r'L\d+(?:@P\d+)?:', document)) >= 2:
                found = (line, r, k, text)
assert found is not None, 'No full printed web.open body; metadata/snippet-only capture rejected'
line, record, k, text = found
pointer = f'/originalRecord/payload/output/{k}/text'
value = {'sourceNativeId': uid, 'url': url, 'nativeJournal': str(paths[0]),
         'nativeRecordLine': line, 'completeOutputPointer': pointer,
         'completeOutputSHA256': hashlib.sha256(text.encode()).hexdigest(),
         'originalRecord': record}
if '--verify-only' not in sys.argv:
    out.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'path': str(out), 'sha256': hashlib.sha256(out.read_bytes()).hexdigest() if out.exists() else None,
                  'mutations': '--verify-only' not in sys.argv,
                  'completeOutputPointer': pointer,
                  'completeOutputSHA256': value['completeOutputSHA256'],
                  'nativeRecordLine': line, 'qualityCredit': 0}))
