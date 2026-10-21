"""Read-only exact handoff checks, followed by owned evidence preservation."""
import pathlib, json, importlib.util, subprocess
D = pathlib.Path(__file__).parent
s = importlib.util.spec_from_file_location('owned', D/'owned-tools.py')
m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
x = m.read(D/'manifest.json'); cp = m.read(pathlib.Path(x['canonicalCheckpoint']))
cat, orders = {}, {}
for p in (m.C/'src/content/topics').glob('*.json'):
    t = m.read(p)
    for n, q in enumerate(t['questions'], 1):
        cat[q['id']] = q; orders[q['id']] = (t['id'], n)
a, b = cp['currentEligibleCompletedIds'], cp['currentRemainingIds']
ids = [r['questionId'] for r in cp['selectedCards']]
assert len(a) == len(set(a)) == len(cp['completedCardHashes']) == 941
assert len(b) == len(set(b)) == 1059 and len(ids) == len(set(ids)) == 2000
assert set(a).isdisjoint(b) and set(a)|set(b) == set(ids)
assert all(m.sha(cat[e['questionId']]) == e['cardCanonicalSha256'] for e in cp['completedCardHashes'])
for topic in {r['topicId'] for r in cp['selectedCards']}:
    old = json.loads(subprocess.check_output(['git', '-C', str(m.C), 'show', cp['baselineSHA']+':src/content/topics/'+topic+'.json']))
    before = {q['id']:(n, q['difficulty'], q['correctIndex']) for n, q in enumerate(old['questions'], 1)}
    for e in (r for r in cp['selectedCards'] if r['topicId'] == topic):
        q = cat[e['questionId']]
        assert before[q['id']] == (orders[q['id']][1], q['difficulty'], q['correctIndex'])
        assert q['difficulty'] == e['difficulty'] and q['correctIndex'] == e['correctIndex']
polar = m.read(m.C/'src/content/topics/polar-regions.json')['questions']
protected = {}
for k, v in x['protectedHeldHashes'].items():
    assert k.isdecimal() and 1 <= int(k) <= len(polar)
    q = polar[int(k)-1]; assert m.sha(q) == v
    protected[k] = {'id':q['id'], 'sha256':v}
assert len(protected) == 9
history = m.read(m.C/'src/content/topics/history-russia.json')['questions']
for order, value in [(15, '4c8f7c263ae3cd883723e57af76d294c74ba9d08779caf5e4f97f528288fe072'), (16, '888699ac2579a55d82b092cc62d07d75e311874a7134210bd3421e2d7cc2d0f9'), (17, '3b71286d050150ff5a4810f62cf50f77cb58a28580864705ef413e26fe733542')]:
    assert m.sha(history[order-1]) == value
assert m.sha(history[21]) == x['pendingHistoryRussia22']['beforeHash']
ra = x['actors']['reviewer']
rows = [json.loads(l) for l in pathlib.Path(ra['nativeJournal']).open()]
assert next(r['payload']['id'] for r in rows if r['type'] == 'session_meta') == ra['threadId']
assert sum(r['type'] == 'compacted' for r in rows) == 0
assert next(r['payload']['type'] for r in reversed(rows) if r.get('payload', {}).get('type') in ['task_started', 'task_complete']) == 'task_complete'
info = next(r['payload']['info'] for r in reversed(rows) if r.get('payload', {}).get('type') == 'token_count')
assert info['last_token_usage']['input_tokens'] == 282377
root_rows = [json.loads(l) for l in pathlib.Path(x['rootNativeAudit']['nativeJournal']).open()]
assert next(r['payload']['id'] for r in root_rows if r['type'] == 'session_meta') == m.O
assert sum(r['type'] == 'compacted' for r in root_rows) == 0
for root, key in [(m.C, 'code'), (m.P, 'planning')]:
    assert m.raw(pathlib.Path(m.h.git(root, 'rev-parse', '--path-format=absolute', '--git-path', 'index'))) == x['foreignIndexes'][key]
assert set(d['id'] for p, d in m.flow.records().values() if d['owner'] == m.O) == set(x['claims'])
assert cp['owner'] == m.O and m.read(m.P/'.flow-leases.json') == {}
assert all(x['actors'][k]['archived'] for k in ['author20', 'author21', 'author20cycle1', 'author22'])
assert not x['sourceActorKeys'] and not cp['currentSourceActors'] and not cp['currentIndependentActors']
mainsha = m.h.git(m.C, 'ls-remote', 'origin', 'refs/heads/main').split()[0]
main = json.loads(subprocess.check_output(['git', '-C', str(m.C), 'show', mainsha+':src/content/topics/history-russia.json']))
mq = {q['id']:q for q in main['questions']}
presence = {history[o-1]['id']:m.sha(mq[history[o-1]['id']]) == m.sha(history[o-1]) for o in [13, 14, 18, 19, 20, 21]}
assert not any(presence.values())
files = [p for p in D.rglob('*') if p.is_file()]
tracked = m.h.git(m.C, 'ls-tree', '-r', '--name-only', 'HEAD', '--', str(D.relative_to(m.C))).splitlines()
assert set(tracked) == {str(p.relative_to(m.C)) for p in files}
assert all(subprocess.check_output(['git', '-C', str(m.C), 'show', 'HEAD:'+p]) == (m.C/p).read_bytes() for p in tracked)
report = {'CURRENT':941, 'remaining':1059, 'fullGoal':2000, 'all941CurrentHashes':True, 'exact941and1059Partition':True, 'all2000FrozenOrderDifficultyNumericKey':True, 'protectedHeldBindings':protected, 'priorVerificationFAIL':str(D/'handoff-verification-attempt1.json'), 'ownIntakeCURRENT':938, 'ownNewlyCertified':3, 'ownCertificates':x['ownProgress']['certificates'], 'source22AUTHORHOLD0UnappliedNoQAOrINITIAL':True, 'source22NetworkCalls':3, 'affectedContentRuns':len(x['ownAffectedRuns']), 'each':'19PASS/0FAIL/0pending', 'typecheck':'NotRun JSON-only', 'runtime':'NotRun prohibited', 'foreignIndexesPreserved':x['foreignIndexes'], 'claimsExact3Owner':m.O, 'leaseHeld':False, 'coordinatorSlicesCount':len(x['coordinatorSlicesToPreserve']), 'ownTrackedPermanentDiskToHEADBeforeVerificationMetadata':len(tracked), 'ownDrift':[], 'ownExtras':[], 'mainRemoteSHA':mainsha, 'mainAcceptedHashesPresent':presence, 'mainIntegrated':False, 'rootActualCompactions':0, 'rootLastInputBeforeHandoffMetadata':x['rootNativeAudit']['lastInput'], 'noActiveAuthorsOrReview':True, 'noRetainedIdleAuthor':True, 'retainedIdleReviewer':{'threadId':ra['threadId'], 'actualCompactions':0, 'lastInput':282377, 'window':475000, 'taskComplete':True, 'cursor':ra['cursor']}}
m.write(D/'handoff-verification.json', report)
x['handoffVerification'] = str(D/'handoff-verification.json')
x['verifiedNow'].update(all941CurrentHashes=True, exact941and1059Partition=True, all2000FrozenOrderDifficultyNumericKey=True)
m.write(D/'manifest.json', x)
h = m.read(D/'handoff-next.json'); h.update(handoffVerification=x['handoffVerification'], verifiedNow=x['verifiedNow']); m.write(D/'handoff-next.json', h)
print(m.savecode([D/'handoff-verification.json', D/'manifest.json', D/'handoff-next.json'], 'Verify CURRENT941 exact2000 and preserved idle reviewer before handoff'))
print('Verified941/1059; frozen2000; protected9; foreign indexes; lease0; no MAIN integration; owned files', len(tracked))
