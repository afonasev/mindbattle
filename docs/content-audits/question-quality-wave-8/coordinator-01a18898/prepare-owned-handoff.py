"""Closed96..100 preservation only; ownership release and SOURCE remain separate."""
import pathlib,importlib.util,json,datetime
D=pathlib.Path(__file__).parent
s=importlib.util.spec_from_file_location('m',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
x=m.read(D/'manifest.json');cp_path=pathlib.Path(x['canonicalCheckpoint']);cp=m.read(cp_path);n=len(cp['currentEligibleCompletedIds'])
assert cp['owner']==cp['activeCoordinator']==m.O and n==x['CURRENT'] and x['remaining']==2000-n and n<2000
assert all(a.get('archived')for k,a in x['actors'].items()if k.startswith('author'))
assert not x['actors']['reviewer']['stage'].startswith('START') and not x.get('pendingBootstrapActors') and not x.get('readyQueue')
own={str(i):x['pendingHistoryRussia'+str(i)]for i in range(96,101)}
assert all(v.get('qualityCredit')==1 or 'HOLD'in v.get('status','')for v in own.values())
rows=[json.loads(l)for l in open(x['rootNativeAudit']['nativeJournal'])];assert [r['payload']['id']for r in rows if r['type']=='session_meta']==[m.O]
comp=sum(r['type']=='compacted'for r in rows);assert comp in (0,1,2)
info=next(r['payload']['info']for r in reversed(rows)if r.get('payload',{}).get('type')=='token_count')
x['rootNativeAudit'].update(actualCompactions=comp,lastInput=info['last_token_usage']['input_tokens'],modelWindow=info['model_context_window'])
nextcard=m.read(x['nextTopicSelectionEvidence'])['nextAfterCurrentHistoryRussia100Only']
q=m.read(m.C/f"src/content/topics/{nextcard['topicId']}.json")['questions'][nextcard['sourceOrder']-1]
f=next(e for e in cp['selectedCards']if e['questionId']==q['id'])
assert q['id']==nextcard['id'] and m.sha(q)==nextcard['hash']==f['baselineCanonicalSha256']
assert q['difficulty']==nextcard['difficulty']==f['difficulty'] and q['correctIndex']==nextcard['correctIndex']==f['correctIndex']
assert q['id']in cp['currentRemainingIds'] and q['id']not in {v['id']for v in own.values()}
a=x['actors']['reviewer'];retained=None
if not a.get('archived'):
    rr=[json.loads(l)for l in open(a['nativeJournal'])]
    assert [r['payload']['id']for r in rr if r['type']=='session_meta']==[a['threadId']]
    assert sum(r['type']=='compacted'for r in rr)==0
    last=next(r['payload']['type']for r in reversed(rr)if r.get('payload',{}).get('type')in ['task_started','task_complete']);assert last=='task_complete'
    ri=next(r['payload']['info']for r in reversed(rr)if r.get('payload',{}).get('type')=='token_count')
    a.update(actualCompactions=0,lastTaskEvent=last,lastInput=ri['last_token_usage']['input_tokens'],modelWindow=ri['model_context_window'],nativePreflightVerifiedBy=m.O);retained=dict(a)
prior=pathlib.Path(x['predecessorHandoff']).parent/'continuation-point.json'
restrictions='Full exact2000 remains active. Preserve ALL manifest fences/newAttemptFences/readScope and inherited continuation '+str(prior)+'. All original FAIL/HOLD0, exhausted claims, solecycle/no-reset fences remain. No finished-card qualification/apply/QA replay, mainmerge/fullsuite/runtime/browser/Player/build/deploy/release/OpenSpecarchive. max2authors/max1reader/READYqueue2. SOURCE98 contentPASS never cures readscope/latepolicy/preimage gaps or ordinalFAIL; its alias is preapplication-only, never replay. Next medicine1 is EASY/key0; never assume uniform level/key.'
nextaction='One READONLY successor ACK, supported exact3 release then ACTIVATE; predecessor stops. Continue full2000 without new human GO. Before next untouched medicine1, parameterize OWN bounded topic helpers without changing schema/source/peer/frozen/CAS/QA contracts.'
x.update(phase=f'READY_FOR_READONLY_SUCCESSOR_CURRENT{n}',rootActualCompactions=comp,actualCompactions=comp,nextUntouched=nextcard,retainedIdleReviewer=retained,noRetainedIdleReviewer=retained is None,noRetainedIdleAuthor=True,retainedIdleAuthorsCurrentOwner=[],currentSourceActors=[],currentIndependentActors=[],currentSourceActorsCount=0,sourceActorKeys=[],currentWork={'stage':'OWN96_100_CLOSED_PENDING_SUPPORTED_HANDOFF','CURRENT':n,'remaining':2000-n},next=nextaction,takeoverTemplate=str(D/'takeover-template.py'),continuationPoint=str(D/'continuation-point.json'),handoffVerification=str(D/'handoff-verification.json'),handoffVerificationNative=str(D/'technical-native-diagnostics.json'),pendingBoundedWork=[],handoffRestrictions=restrictions,at=datetime.datetime.now(datetime.timezone.utc).isoformat())
x['readScope'].update(nextUntouched=nextcard,ownD=str(D))
x['takeoverUsage']='After ACTIVATE copy tracked template to ownD/takeover.py; inspect owner/intake '+str(x['ownIntakeCURRENT'])+' -> '+str(n)+'. Exact3 claim under short P lease/private CAS before SOURCE/code writes. No old interrupted-release recovery or completed evidence replay.'
point={'owner':m.O,'CURRENT':n,'remaining':2000-n,'fullGoal':2000,'ownIntake':x['ownIntakeCURRENT'],'ownNewlyCertified':n-x['ownIntakeCURRENT'],'manifest':str(D/'manifest.json'),'nextUntouched':nextcard,'nextTopicSelectionEvidence':x['nextTopicSelectionEvidence'],'pendingBoundedWork':[],'pendingReviews':[],'retainedIdleReviewer':retained,'coordinatorSlices':len(x['coordinatorSlicesToPreserve']),'ownOrders96through100':own,'inheritedContinuation':str(prior),'source98ProceduralDeviations':x['source98ProceduralDeviations'],'source98InitialOrdinalAlias':x['pendingHistoryRussia98']['initialOrdinalAlias'],'technicalDiagnostics':x['technicalDiagnosticsAuthority'],'takeover':str(D/'takeover.json'),'scope':restrictions,'handoff':nextaction,'rootNative':x['rootNativeAudit']}
m.write(D/'continuation-point.json',point)
for p in [D/'manifest.json',D/'handoff-next.json']:m.write(p,x)
cc=m.savecode([D/'manifest.json',D/'handoff-next.json',D/'continuation-point.json',pathlib.Path(__file__)],f'Preserve owned96-100 CURRENT{n} exact2000 continuation')
idx=pathlib.Path(m.h.git(m.P,'rev-parse','--path-format=absolute','--git-path','index'));expected=m.raw(idx);assert expected==x['foreignIndexes']['planning']
with m.flow.locked():m.flow.lease('acquire','planning',m.O)
try:
    assert m.raw(idx)==expected and all(m.flow.get(cid)[1]['owner']==m.O for cid in x['claims'])
    paths=[cp_path,m.P/'evidence/question-revision-process-v2/coordinator-state.json',m.P/'evidence/question-revision-process-v2/active-full2000-goal-01a1593a.json'];report=m.P/f'evidence/question-revision-process-v2/handoff-{m.O[:8]}.json'
    m.write(report,{'owner':m.O,'CURRENT':n,'remaining':2000-n,'ownIntake':x['ownIntakeCURRENT'],'ownNewlyCertified':n-x['ownIntakeCURRENT'],'manifest':str(D/'manifest.json'),'continuation':str(D/'continuation-point.json'),'codeCommit':cc,'nextUntouched':nextcard,'fullGoal':2000})
    for p in paths:
        d=m.read(p);assert d['owner']==m.O
        d.update(phase=x['phase'],currentManifest=str(D/'manifest.json'),next=x['next'],rootNativeAudit=x['rootNativeAudit'],rootActualCompactions=comp,coordinatorActualCompactions=comp,handoffVerification=x['handoffVerification'],handoffVerificationNative=x['handoffVerificationNative'],currentSourceActors=[],currentIndependentActors=[],currentSourceActiveCount=0,nativeActorsCurrent=[retained]if retained else[],retainedIdleReviewer=retained,activeAuthors=[],idleAuthors=[],activeIndependentReview=None,currentHandoff=str(report));m.write(p,d)
    pc=m.h.save(m.P,'refs/heads/'+x['planningBranch'],[str(p.relative_to(m.P))for p in [*paths,report]],f'Preserve CURRENT{n} current full2000 handoff pointer',expected)
finally:
    with m.flow.locked():m.flow.lease('release','planning',m.O)
assert m.read(m.P/'.flow-leases.json')=={}
print({'code':cc,'planning':pc,'CURRENT':n,'remaining':2000-n,'actualCompactions':comp,'nextUntouched':nextcard,'pendingBoundedWork':0,'retainedReviewer':retained['threadId']if retained else None})
