"""Verify actual whole original bootstrap outputs; no semantic quality credit."""
import json, pathlib, hashlib, sys
D = pathlib.Path(__file__).parent
identity = json.loads((D / sys.argv[1]).read_text())
native = pathlib.Path(identity['nativeJournal'])
rows = [json.loads(line) for line in native.open()]
uid = identity['verifiedSessionMetaId']
assert [r['payload']['id'] for r in rows if r['type'] == 'session_meta'] == [uid]
calls = [(i, r['payload']) for i, r in enumerate(rows, 1)
         if r['type'] == 'response_item' and r['payload'].get('type') == 'custom_tool_call']
outputs = {r['payload']['call_id']: (i, r['payload']) for i, r in enumerate(rows, 1)
           if r['type'] == 'response_item' and r['payload'].get('type') == 'custom_tool_call_output'}
C = pathlib.Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle')
P = pathlib.Path('/Users/eaafonasev/Projects/mindbattle/planning')
primary = pathlib.Path('/Users/eaafonasev/Projects/mindbattle')
first = [C / ('docs/content-audits/question-quality-wave-8/' + part) for part in [
    'coordinator-01a14377/pinned-question-revision-12e5581b.md',
    'coordinator-01a13f31/packet-contract.json',
    'coordinator-01a1593a/method-pilot.md', 'coordinator-01a1593a/packet-format.md']]
required = [primary/'AGENTS.md', C/'AGENTS.md',
    *[primary/('.agents/references/'+n+'.md') for n in ['context-efficiency','model-routing','execution-policy']],
    *[pathlib.Path('/Users/eaafonasev/.codex/references')/(n+'.md') for n in ['session-efficiency','game-execution','task-cleanup']],
    C/'docs/content-audits/question-authoring-guide-2026-09-02.md', D/'native-bootstrap-identity-readonly.py']
expected = [(str(p), p.read_text()) for p in first + required]
for p, start, end in [(P/'docs/GAME_SPEC.md',135,285), (P/'openspec/specs/question-catalog/spec.md',21,33)]:
    body = ''.join(line for i,line in enumerate(p.open(),1) if start <= i <= end)
    expected.append((str(p)+':'+str(start)+'-'+str(end),body))
valid = []
for line, call in calls:
    result = outputs.get(call['call_id'])
    if result is None: continue
    output_line, output = result
    blocks = output.get('output', [])
    if not isinstance(blocks,list): continue
    for index, block in enumerate(blocks):
        if not isinstance(block,dict) or not isinstance(block.get('text'),str): continue
        try: value = json.loads(block['text'])
        except json.JSONDecodeError: continue
        if isinstance(value,dict) and value.get('exit_code') == 0 and isinstance(value.get('output'),str):
            if 'Warning: truncated output' in value['output'] or 'tokens truncated' in value['output']: continue
            valid.append({'callLine':line,'resultLine':output_line,'callId':call['call_id'],
                          'input':call.get('input',''),'body':value['output'],'block':index})
proof = []
missing = []
for path, body in expected:
    base = path.split(':')[0]
    found = [v for v in valid if v['body'] == body and base in v['input']]
    if not found: missing.append(path); continue
    v = found[0]
    proof.append({'path':path,'callLine':v['callLine'],'resultLine':v['resultLine'],'callId':v['callId'],
                  'originalBodySHA256':hashlib.sha256(body.encode()).hexdigest(),'exitCode':0,'wholeUntruncated':True})
literal = []
for (line, call), p in zip(calls,first):
    exact = "text(await tools.exec_command({cmd:'cat " + str(p) + "',max_output_tokens:12000}));"
    literal.append({'callLine':line,'exact':call.get('input','').strip()==exact})
own_identity = []
for v in valid:
    try: payload = json.loads(v['body'])
    except json.JSONDecodeError: continue
    if isinstance(payload,dict) and payload.get('verifiedSessionMetaId') == uid:
        own_identity.append({'callLine':v['callLine'],'resultLine':v['resultLine'],'callId':v['callId'],
            'actualCompactions':payload.get('actualCompactions'),'originalCreateCallLine':payload.get('originalCreateCallLine'),
            'originalCreateOutputLine':payload.get('originalCreateOutputLine')})
complete = [i for i,r in enumerate(rows,1) if r['type']=='event_msg' and r['payload'].get('type')=='task_complete']
report = {'owner':json.loads((D/'manifest.json').read_text())['owner'],'nativeId':uid,'nativeJournal':str(native),
    'actualCompactions':sum(r['type']=='compacted' for r in rows),'firstFourExact':literal,
    'wholeReadProofs':proof,'missingWholeOriginals':missing,'identityOriginalProofs':own_identity,
    'taskCompleteOriginalLines':complete,'qualityCredit':0}
report['pass'] = not missing and len(literal)==4 and all(v['exact'] for v in literal) and bool(own_identity) and report['actualCompactions']==0 and bool(complete)
if '--prospective-before-start-correction' in sys.argv:
    # Explicit same-native SOURCE19 correction, preserving the original failure.
    # This is not a replay or waiver of a finished content attempt.
    deviation_path = D/'source19-bootstrap-original-deviation.json'
    deviation = json.loads(deviation_path.read_text())
    manifest = json.loads((D/'manifest.json').read_text())
    assert deviation['sourceNativeId']==uid and deviation['originalFirstFourExact'] is False
    assert deviation['uncured'] and 19 not in manifest['ownedSourceOrders']
    assert manifest['actors']['author19']['stage']=='READONLY_BOOTSTRAP_LITERAL_CORRECTION_REQUIRED'
    assert rows[deviation['originalFirstCombinedCallLine']-1]==deviation['originalFirstCombinedCall']
    sequences = []
    for position in range(len(calls)-3):
        block = [calls[position+i] for i in range(4)]
        exact = all(call.get('input','').strip()=="text(await tools.exec_command({cmd:'cat "+str(p)+"',max_output_tokens:12000}));" for (_,call),p in zip(block,first))
        if not exact: continue
        checks=[]
        for (line,call),p in zip(block,first):
            bodies=[v for v in valid if v['callId']==call['call_id'] and v['body']==p.read_text()]
            if len(bodies)!=1:break
            v=bodies[0];checks.append({'path':str(p),'callLine':line,'resultLine':v['resultLine'],'callId':call['call_id'],'wholeExit0':True})
        if len(checks)==4 and any(i<checks[0]['callLine'] for i in complete) and any(i>checks[-1]['resultLine'] for i in complete):sequences.append(checks)
    report.update(originalFirstFourExact=False,originalDeviation=str(deviation_path),originalDeviationUncured=True,
                  prospectiveSeparateExactFourSequences=sequences,
                  qualificationBasis='Same native prospective exact reads BEFORE any SOURCE19 START; original combined call and premature ACK stay uncured; explicit inherited SOURCE12 precedent.')
    report['pass']=not missing and len(sequences)==1 and bool(own_identity) and report['actualCompactions']==0
out = D / sys.argv[2]
out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'pass':report['pass'],'wholeReads':len(proof),'missing':missing,'firstFourExact':all(v['exact'] for v in literal),
                  'identityProofCount':len(own_identity),'taskCompleteCount':len(complete),'proof':str(out)},ensure_ascii=False))
