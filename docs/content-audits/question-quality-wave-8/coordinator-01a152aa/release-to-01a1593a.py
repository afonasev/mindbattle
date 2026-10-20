"""Preservation and exact-three release only; no editorial operations."""
import importlib.util, json, subprocess, datetime
from pathlib import Path
D=Path(__file__).parent
s=importlib.util.spec_from_file_location('owned',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
S='01a1593a-ac89-7b22-9cdb-d59678b1d767'
claims=['question-quality-future-waves','question-quality-wave-7','question-quality-wave-8']
CP=m.P/'openspec/changes/question-quality-future-waves/current-checkpoint.json'
statepath=m.P/'evidence/question-revision-process-v2/coordinator-state.json'
PR='refs/heads/codex/question-revision-resume-20261014';CR='refs/heads/codex/question-quality-wave-6'
def git(root,*args):return subprocess.check_output(['git','-C',str(root),*args],text=True).strip()
def indices():return {k:m.raw(root/m.h.git(root,'rev-parse','--git-path','index')) for k,root in [('C',m.C),('P',m.P)]}
before=indices();cp=m.read(CP)
assert len(cp['selectedCards'])==2000 and len(cp['currentEligibleCompletedIds'])==890 and len(cp['currentRemainingIds'])==1110
assert m.read(m.P/'.flow-leases.json')=={}
assert git(m.P,'symbolic-ref','HEAD')=='refs/heads/main'
for cid in claims:assert m.flow.get(cid)[1]['owner']==m.O
canonical=[CP,statepath]+[m.P/f'openspec/changes/{cid}/delivery.json' for cid in claims]
for f in canonical:assert f.read_bytes()==subprocess.check_output(['git','-C',str(m.P),'show',PR+':'+str(f.relative_to(m.P))])
q=m.read(D/'queue.json')
q.update(phase='HANDOFF_ONLY_WAIT_SUCCESSOR_CLAIM',ordinaryWorkActivated=False,successor=S)
q['pendingParks31'].update(stage='RAW_READY_PREINITIAL_UNQUALIFIED_UNAPPLIED',rawCompletedFreeze='bd8cba929e11cff933293bfebae97d934b0fd262',candidate='b86b97ec6c5578fa1ea8003101ff0e3ca31c7711a4888027bb0396ab2c18be41',directory=str(D/'source-parks31-complete'))
q['pendingPolar41'].update(stage='RAW_READY_SAME_SOLE_SOURCE_CYCLE1_UNQUALIFIED_UNAPPLIED',noINITIALever=False,directory=str(D/'source-polar41-cycle1-fresh'),expectedCandidate='f9bc933ed67843a76a3d0df60d3a91547ac6360a811b13f526c131d9b7abf298')
q['activeSOURCE'][0].update(stage='IDLE_SOURCE31_RAW_READY',cursor='ee8e3e57-ef66-4fa4-b022-cac90d9f6652:19',actualCompactionsLastAudit=1)
q['activeSOURCE'][1].update(stage='SOURCE41_CYCLE1_RAW_READY_HANDOFF')
m.write(D/'queue.json',q)
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
packets={}
for name in ['source-parks31-complete','source-polar41-cycle1-fresh']:
 packets[name]={f.name:m.raw(f) for f in sorted((D/name).glob('*.json'))}
manifest=dict(at=now,predecessor=m.O,successor=S,status='PRESERVED_WAIT_EXACT3_RELEASE',fullGoal=2000,CURRENT=890,remaining=1110,waves=[500,198,192,0],fullGoalNotComplete=True,goalStatus='ACTIVE',ordinaryWorkActivated=False,actualNativeCompactions=2,exactClaims=claims,codeBranch=CR[11:],planningBranch=PR[11:],latestCertificate='6650fe076aa60f771869e2fdbfcd4d58d1bf756a',latestCertifiedPlanningProjection='3628fb7f4e1a430c38e5740ee0d1b13d8ca2ce25',codeBefore=git(m.C,'rev-parse',CR),planningBefore=git(m.P,'rev-parse',PR),foreignIndicesBefore=before,historicalPlanningIndex='bacce162eb1e17945aa0eb0d102c1c34d7c60c05b212b8e918d0ad554daf21d4',planningIndexChangedExternallyBeforeThisHandoff=True,canonicalCheckpoint=str(CP),queue=str(D/'queue.json'),rawPackets=packets,actors={k:q[k] for k in ['activeOTHER','activeSOURCE']},ownedActiveOperations=[],ownedBackgroundProcesses=[],cleanup={'deleted':[],'retained':'Shared active worktree and essential SOURCE/receipt evidence for successor; no owned disposable runtime/build resources'},fences=['FOREIGN default indexes; private CAS only','no main merge/runtime/browser/Player/build/full tests/deploy/archive','pinned process unchanged; same sole cycle1 FINAL41; no reset or ordinary cycle2','SOURCE42 BAS original challenge consumed; one official alternative remains; no retry/bypass','HOLD/READY/QA alone credit0; count only exact CURRENT strict certificate','successor methodology discussion does not alter existing pinned fences'],next='Successor CLAIM_NOW exact3, independently verify ownership, then follow its authorized flow-coordinate scope; no quality work by predecessor')
m.write(D/'handoff-manifest-01a1593a.json',manifest)
(D/'FULLGOAL-HANDOFF-01a1593a.md').write_text('''# Full exact2000 handoff

Successor: 01a1593a-ac89-7b22-9cdb-d59678b1d767. CURRENT 890/2000; remaining 1110 across all20 topics/waves6–9. Waves500/198/192/0. Full goal ACTIVE, unfinished. This predecessor has actual native compactions2 and performs preservation/release only.

Machine manifest: handoff-manifest-01a1593a.json; live actor/cycle routing: queue.json. These supersede older coordinator-state actor fields. Canonical checkpoint stays planning/openspec/changes/question-quality-future-waves/current-checkpoint.json. Selected scope, frozen key/difficulty and accepted hashes unchanged.

SOURCE31: source-parks31-complete critical3 raw READY; bd8cba929e11cff933293bfebae97d934b0fd262; candidate b86b97ec6c5578fa1ea8003101ff0e3ca31c7711a4888027bb0396ab2c18be41. No qualification/apply/QA/INITIAL, zero credit. Country primary/stable pointer completion must be checked by successor; existing source-parks31-fresh body capture points to native ordinal271 (one-based), not declared270. No prior independent cycle31 consumed.

SOURCE41: source-polar41-cycle1-fresh critical3 raw READY, preserved with this handoff. FIRSTINITIAL FIX raw75ab23f7901bf25bd21f71bcb0db09d517624a04 already consumed80280b907ad193056a15cadb9184f0f4100166f7. Same solecycle1 only: note1 replace final phrase with «в Восточно-Сибирское море и море Бофорта». Expected candidate f9bc933ed67843a76a3d0df60d3a91547ac6360a811b13f526c131d9b7abf298. Not qualified/applied/QA/FINAL; zero credit. Reviewer D1 idle awaiting samecycle1 FINAL. Keep MAIN31 unchanged during reader41 binding.

SOURCE42: old actor stopped2; no complete packet/noINITIAL. Original BAS Antarctic factsheet robot challenge consumed; no retry/bypass; one official alternative remains. Diagnostic source-captures/source52f1-42-bas-challenge-original.json preserved7a572a1749d148055454dc341139daaf1c3702d7.

Pinned process coordinator-01a14377/pinned-question-revision-12e5581b.md SHA8bc3b06d80b0aa94dbb8d375253c5074eda067615ab7e3a2c3845bbfabaff7b9 remains binding. Guard coordinator-01a13f31/planning-certification-guard.py unchanged. No quality inheritance, full6/4 personal judgments and whole primary/relevant peer bodies, no third full review. HOLDs remain zero, including polar13/21/22 and parks14/26, retained histories. Latest certificate6650fe076aa60f771869e2fdbfcd4d58d1bf756a, projection3628fb7f4e1a430c38e5740ee0d1b13d8ca2ce25. Existing minimal affected QA19 only after actual apply; no QA during this handoff.

Both default indexes FOREIGN. Planning physical main never switch. Private refs codex/question-quality-wave-6 and codex/question-revision-resume-20261014; private-save helper evidence/question-revision-process-v2/private-save-helper-01a13cb1.py. Acquire own planning lease before every planning mutation/save; release before waits. Historical P index changed externally before this handoff; preserve current bytes, never restore old index. No main merge, runtime, full suite, release/deploy or OpenSpec archive authorized. No new actors/messages by this predecessor.
''')
files=[D/'queue.json',D/'handoff-manifest-01a1593a.json',D/'FULLGOAL-HANDOFF-01a1593a.md',Path(__file__)]+list((D/'source-polar41-cycle1-fresh').glob('*.json'))
cc=m.savecode(files,'Preserve exact2000 CURRENT890 raw31 and solecycle1 raw41 for named successor; no quality work')
transfer=dict(at=now,predecessor=m.O,successor=S,status='CLAIMS_RELEASED_WAIT_SUCCESSOR_CLAIM_NOT_ACTIVATED',CURRENT=890,remaining=1110,fullGoal=2000,fullGoalNotComplete=True,ordinaryWorkActivated=False,exactClaims=claims,preservationCodeCommit=cc,manifest=str(D/'handoff-manifest-01a1593a.json'),actualNativeCompactions=2)
with m.flow.locked():m.flow.lease('acquire','planning',m.O)
try:
 with m.flow.locked():
  assert m.read(m.P/'.flow-leases.json')['planning']['owner']==m.O
  for cid in claims:assert m.flow.get(cid)[1]['owner']==m.O
  for cid in claims:m.flow.release(cid,m.O)
 cp.update(asOf=now,phase=transfer['status'],ownershipTransfer=transfer,ordinaryWorkActivated=False)
 m.write(CP,cp)
 state=m.read(statepath)
 state.update(asOf=now,status=transfer['status'],phase=transfer['status'],ordinaryWorkActivated=False,claims=[],fullGoalTransfer=transfer,currentNativeActors=manifest['actors'],activeAuthors=q['activeSOURCE'],activeIndependentReview=q['activeOTHER'],readyQueue=[q['pendingParks31'],q['pendingPolar41']],next='CLAIM_NOW exact3 by '+S,codeCommit=cc,rootActualCompactions=2)
 m.write(statepath,state)
 receipt=m.P/'evidence/question-revision-process-v2/handoff-01a152aa-to-01a1593a.json'
 m.write(receipt,dict(**transfer,foreignIndicesBefore=before,ownedActiveOperations=[]))
 pc=m.save(m.P,PR,canonical+[receipt],'Release exact3 from 01a152aa to named successor 01a1593a; preserve full2000 CURRENT890')
finally:
 with m.flow.locked():m.flow.lease('release','planning',m.O)
assert m.read(m.P/'.flow-leases.json')=={}
for cid in claims:assert m.flow.get(cid)[1]['owner'] is None
assert indices()==before
assert git(m.P,'symbolic-ref','HEAD')=='refs/heads/main'
transfer.update(planningReleaseCommit=pc,planningLeaseReleased=True,foreignIndicesBeforeAfter=before,claimNow=True)
m.write(D/'successor-release-handshake.json',transfer)
final=m.savecode([D/'successor-release-handshake.json'],'Record exact3 released CLAIM_NOW handshake for 01a1593a; full goal remains ACTIVE')
print(json.dumps(dict(**transfer,codeHandoffCommit=final),ensure_ascii=False))
