"""Exact-three successor claim/intake only; no ordinary editorial stages."""
import datetime
import hashlib
import importlib.util
import json
import pathlib
import subprocess

C = pathlib.Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle')
P = pathlib.Path('/Users/eaafonasev/Projects/mindbattle/planning')
D = pathlib.Path(__file__).resolve().parent
OLD = D.parent / 'coordinator-01a14508'
O = '01a152aa-06d8-74f0-994a-dd8e4b3cd5dd'
J = pathlib.Path('/Users/eaafonasev/.codex/sessions/2026/10/19/rollout-2026-10-19T10-37-17-01a152aa-06d8-74f0-994a-dd8e4b3cd5dd.jsonl')
E = P / 'evidence/question-revision-process-v2'
CP = P / 'openspec/changes/question-quality-future-waves/current-checkpoint.json'
CLAIMS = ['question-quality-future-waves', 'question-quality-wave-7', 'question-quality-wave-8']
CR = 'refs/heads/codex/question-quality-wave-6'
PR = 'refs/heads/codex/question-revision-resume-20261014'


def read(p):
    return json.loads(p.read_text())


def write(p, value):
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def raw(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def sha(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], text=True).strip()


def index(root):
    return root / git(root, 'rev-parse', '--git-path', 'index')


def mod(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def native():
    rows = [json.loads(line) for line in J.open()]
    assert rows[0]['type'] == 'session_meta' and rows[0]['payload']['id'] == O
    assert sum(row.get('type') == 'compacted' for row in rows) == 0
    context = [row['payload'] for row in rows if row.get('type') == 'turn_context'][-1]
    assert context['model'] == 'gpt-6.1-sol' and context['effort'] == 'medium'


def validate(cp):
    catalog = {}
    for topic in {e['topicId'] for e in cp['selectedCards']}:
        catalog.update({q['id']: q for q in read(C / f'src/content/topics/{topic}.json')['questions']})
    selected = {e['questionId'] for e in cp['selectedCards']}
    done = set(cp['currentEligibleCompletedIds'])
    remaining = set(cp['currentRemainingIds'])
    assert len(selected) == len(cp['selectedCards']) == 2000
    assert len(done) == len(cp['currentEligibleCompletedIds']) == 881
    assert len(remaining) == 1119 and not done & remaining and done | remaining == selected
    assert len(cp['completedCardHashes']) == 881
    assert {e['questionId'] for e in cp['completedCardHashes']} == done
    for e in cp['completedCardHashes']:
        assert sha(catalog[e['questionId']]) == e['cardCanonicalSha256']
    for e in cp['selectedCards']:
        assert all(catalog[e['questionId']][k] == e[k] for k in ['difficulty', 'correctIndex'])
    assert [len(done.intersection(w['selectedIds'])) for w in cp['waves']] == [500, 198, 183, 0]


native()
helper = mod('private_save_successor', E / 'private-save-helper-01a13cb1.py')
flow = mod('flow_successor', C / 'tools/flow.py').Flow(P)
before = {'C': raw(index(C)), 'P': raw(index(P))}
assert before == {'C': '260b8d32f27dba2372fe570515b44cb6c39dfa1646ea9a1a23c3762de47c9f65', 'P': 'bacce162eb1e17945aa0eb0d102c1c34d7c60c05b212b8e918d0ad554daf21d4'}
assert git(P, 'symbolic-ref', 'HEAD') == 'refs/heads/main'
assert read(P / '.flow-leases.json') == {}
release = read(OLD / 'successor-release-handshake.json')
assert release['successor'] == O and release['status'] == 'CLAIMS_RELEASED_WAIT_SUCCESSOR_CLAIM_NOT_ACTIVATED'
assert git(P, 'rev-parse', PR) == release['planningReleaseCommit']
cp = read(CP)
validate(cp)
state_path = E / 'coordinator-state.json'
paths = [CP, state_path] + [P / f'openspec/changes/{cid}/delivery.json' for cid in CLAIMS]
for path in paths:
    assert path.read_bytes() == subprocess.check_output(['git', '-C', str(P), 'show', PR + ':' + str(path.relative_to(P))])
for cid in CLAIMS:
    assert flow.get(cid)[1]['owner'] is None
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
queue_old = read(OLD / 'queue.json')
actors = {k: queue_old[k] for k in ['activeOTHER', 'activeSOURCE']}
base_code = git(C, 'rev-parse', CR)
goal = dict(at=now, owner=O, actualCompactions=0, nativeJournal=str(J), model='gpt-6.1-sol', effort='medium',
            phase='CLAIMED_WAIT_ACTIVATE', goalStatus='ACTIVE', fullGoal=2000, fullGoalNotComplete=True,
            intakeCURRENT=881, CURRENT=881, remaining=1119, newlyCertified=0, waves=[500, 198, 183, 0],
            predecessorIntakeCURRENT=871, predecessorNewlyCertified=10, ordinaryWorkActivated=False,
            exactClaims=CLAIMS, C=str(C), P=str(P), D=str(D), CP=str(CP),
            codeBranch=CR.removeprefix('refs/heads/'), privatePlanningBranch=PR.removeprefix('refs/heads/'),
            noMainIntegration=True, frozenScopeAndPerCardHashesUnchanged=True, HOLD_READY_QA_credit=0,
            predecessor=release['predecessor'], predecessorHandoff=str(OLD / 'FULLGOAL-HANDOFF-root2.md'),
            latestCodeCommit=base_code, indexBefore=before, actorPointers=actors,
            pendingOriginal36={'status': 'FIRSTINITIAL_PASS_RAW_NOT_CERTIFIED', 'rawFreeze': 'd7e697206c37ae8750d073004bceb586aa1e3bea', 'SOURCEqualified': 'f6609839b6088ba9f31199e8e4c2ebcd772c6570', 'nextAfterActivate': 'strict bind and certify exact881->882'},
            pendingParks27={'status': 'SOLE_CYCLE1_QUALIFIED_NOT_APPLIED_NOQA_NOFINAL', 'qualified': 'e0f7052d87750506b88a8983619b8c6443202801', 'ordinaryCycle2': False},
            parks26={'status': 'FINAL_HOLD0', 'ordinaryCycle2': False},
            source37={'status': 'READ_ONLY_ACK_NO_START', 'threadId': '01a1510b-a2de-73e3-ae86-b18b1d2d9827'})
goal_path = E / 'active-full2000-goal-01a152aa.json'
transfer = dict(at=now, predecessor=release['predecessor'], successor=O, status='CLAIMED_WAIT_ACTIVATE',
                CURRENT=881, remaining=1119, fullGoal=2000, ordinaryWorkActivated=False, fullGoalNotComplete=True,
                exactClaims=CLAIMS, ownD=str(D), nativeJournal=str(J), actualCompactions=0)
with flow.locked():
    assert read(P / '.flow-leases.json') == {}
    flow.lease('acquire', 'planning', O)
try:
    with flow.locked():
        assert read(P / '.flow-leases.json')['planning']['owner'] == O
        for cid in CLAIMS:
            assert flow.get(cid)[1]['owner'] is None
        for cid in CLAIMS:
            flow.claim(cid, O)
    cp.update(owner=O, activeCoordinator=O, asOf=now, phase='CLAIMED_WAIT_ACTIVATE', ownershipTransfer=transfer)
    write(CP, cp)
    state = read(state_path)
    state.update(threadId=O, owner=O, activeCoordinator=O, phase='CLAIMED_WAIT_ACTIVATE', status='CLAIMED_WAIT_ACTIVATE',
                 ordinaryWorkActivated=False, ownActualCompactions=0, rootActualCompactions=0, asOf=now,
                 counts={'CURRENT': 881, 'remaining': 1119}, claims=CLAIMS, fullGoalTransfer=transfer,
                 coordinatorProgress={'intakeCURRENT': 881, 'CURRENT': 881, 'newlyCertified': 0, 'remaining': 1119},
                 currentWork={'owner': O, 'CURRENT': 881, 'remaining': 1119, 'ownD': str(D.relative_to(C)), 'phase': 'CLAIMED_WAIT_ACTIVATE', 'actorQueue': str((D / 'queue.json').relative_to(C))},
                 activeFullGoal=str(goal_path), currentNativeActors=actors)
    write(state_path, state)
    write(goal_path, goal)
    assert read(P / '.flow-leases.json')['planning']['owner'] == O
    pc = helper.save(P, PR, [str(p.relative_to(P)) for p in paths + [goal_path]], 'Claim exact3 for successor full2000 intake881; wait ACTIVATE', before['P'])
finally:
    with flow.locked():
        flow.lease('release', 'planning', O)
goal.update(planningClaimCommit=pc, planningLeaseReleased=True)
write(D / 'intake.json', goal)
write(D / 'queue.json', dict(owner=O, fullGoal=2000, intakeCURRENT=881, CURRENT=881, remaining=1119,
    newlyCertified=0, fullGoalNotComplete=True, ordinaryWorkActivated=False, phase='CLAIMED_WAIT_ACTIVATE',
    predecessorQueue=str(OLD / 'queue.json'), waveCURRENT=[500,198,183,0], **actors,
    pendingOriginal36=goal['pendingOriginal36'], pendingParks27=goal['pendingParks27'],
    parks26=goal['parks26'], source37=goal['source37']))
write(D / 'remaining-routing-intake881.json', dict(selectedCards=cp['selectedCards'],
    currentEligibleCompletedIds=cp['currentEligibleCompletedIds'], completedCardHashes=cp['completedCardHashes'],
    currentRemainingIds=cp['currentRemainingIds'], fullGoal=2000, CURRENT=881, remaining=1119, all20topicsRetained=True))
files = [path for path in D.iterdir() if path.is_file()]
cc = helper.save(C, CR, [str(p.relative_to(C)) for p in files], 'Preserve successor exact2000 intake881 and claim handshake; wait ACTIVATE', before['C'])
receipt = dict(**transfer, intakeCodeCommit=cc, planningClaimCommit=pc, indicesBeforeAfter=before,
               planningLeaseReleased=True, all881AcceptedHashesVerified=True, all2000FrozenBindingsVerified=True)
receipt_path = E / 'successor-01a152aa-claimed-wait-activate.json'
with flow.locked():
    assert read(P / '.flow-leases.json') == {}
    flow.lease('acquire', 'planning', O)
try:
    assert read(P / '.flow-leases.json')['planning']['owner'] == O
    write(receipt_path, receipt)
    final_pc = helper.save(P, PR, [str(receipt_path.relative_to(P))], 'Record successor code and planning intake linkage; wait ACTIVATE', before['P'])
finally:
    with flow.locked():
        flow.lease('release', 'planning', O)
validate(read(CP))
for cid in CLAIMS:
    assert flow.get(cid)[1]['owner'] == O
assert read(P / '.flow-leases.json') == {}
assert {'C': raw(index(C)), 'P': raw(index(P))} == before
assert git(P, 'symbolic-ref', 'HEAD') == 'refs/heads/main'
native()
print(json.dumps(dict(status='CLAIMED_WAIT_ACTIVATE', owner=O, exactClaims=CLAIMS, leaseFree=True,
                     intakeCodeCommit=cc, planningClaimCommit=pc, planningReceiptCommit=final_pc,
                     indices=before, CURRENT=881, remaining=1119, fullGoal=2000, actualCompactions=0)))
