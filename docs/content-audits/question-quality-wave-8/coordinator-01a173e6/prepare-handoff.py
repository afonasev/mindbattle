"""Preserve this bounded 89..95 slice for one supported successor; no transfer/content edits."""
import pathlib,importlib.util,json,datetime
D=pathlib.Path(__file__).parent
s=importlib.util.spec_from_file_location('m',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
x=m.read(D/'manifest.json');cp_path=pathlib.Path(x['canonicalCheckpoint']);cp=m.read(cp_path);n=len(cp['currentEligibleCompletedIds'])
assert cp['owner']==cp['activeCoordinator']==m.O and n==x['CURRENT'] and x['remaining']==2000-n
assert all(a.get('archived') for k,a in x['actors'].items() if k.startswith('author'))
a=x['actors']['reviewer'];assert not a['stage'].startswith('START')
rows=[json.loads(l)for l in open(x['rootNativeAudit']['nativeJournal'])];assert next(r['payload']['id']for r in rows if r['type']=='session_meta')==m.O
comp=sum(r['type']=='compacted'for r in rows);assert comp in (0,1,2)
info=next(r['payload']['info']for r in reversed(rows)if r.get('payload',{}).get('type')=='token_count')
x['rootNativeAudit'].update(actualCompactions=comp,lastInput=info['last_token_usage']['input_tokens'],modelWindow=info['model_context_window'])
q=m.read(m.C/'src/content/topics/history-russia.json')['questions'][95];assert q['id'] in cp['currentRemainingIds'] and 'pendingHistoryRussia96' not in x
nextcard={'id':q['id'],'topicId':'history-russia','sourceOrder':96,'difficulty':q['difficulty'],'correctIndex':q['correctIndex'],'hash':m.sha(q)}
own={str(i):x.get('pendingHistoryRussia'+str(i),{}) for i in range(89,96)}
pending=[{'order':int(k),'state':v} for k,v in own.items() if v and v.get('qualityCredit')!=1 and 'HOLD' not in v.get('status','')]
retained=None if a.get('archived') else dict(a)
if retained:assert retained['actualCompactions']==0 and retained['lastTaskEvent']=='task_complete'
restrictions='Full SOURCE/editorial exact2000 remains active. Preserve original SOURCE83 FAIL/raw and all old/new HOLD0, exhausted claims, preapplication-only aliases and actual compaction fences. No ordinarycycle2/newINITIAL/reset or oldHOLD/failed-source adoption. No finished-card qualification/reapply/QA replay. max2authors/max1reader/READYqueue2. No mainmerge/fulltests/runtime/browser/Player/build/deploy/release/OpenSpecarchive. Mixed frozen difficulties and numeric keys: use exact task/selection/live fields, never assume MEDIUM/index3; SOURCE95 is HARD/index2 and its wrong short START plus two readscope overruns remain uncured. Source87 terminal14.5grammar HOLD and potential peer73 observation remain untouched.'
nextaction='One READONLY successor native ACK, supported exact3 release then ACTIVATE; predecessor stops. Successor first resumes preserved bounded pending phases if any, otherwise untouched96, and continues full2000 without new human GO.'
x.update(phase=f'READY_FOR_READONLY_SUCCESSOR_CURRENT{n}',rootActualCompactions=comp,actualCompactions=comp,nextUntouched=nextcard,retainedIdleReviewer=retained,noRetainedIdleReviewer=retained is None,noRetainedIdleAuthor=True,retainedIdleAuthorsCurrentOwner=[],currentSourceActors=[],currentIndependentActors=[],currentSourceActorsCount=0,sourceActorKeys=[],currentWork={'stage':'BOUNDED89_95_PRESERVED_PENDING_SUPPORTED_HANDOFF' if pending else 'BOUNDED89_95_COMPLETE_PENDING_SUPPORTED_HANDOFF','CURRENT':n,'remaining':2000-n},next=nextaction,takeoverTemplate=str(D/'takeover-template.py'),continuationPoint=str(D/'continuation-point.json'),handoffVerification=str(D/'handoff-verification.json'),handoffVerificationNative=str(D/'technical-native-diagnostics.json'),pendingBoundedWork=pending,handoffRestrictions=restrictions,at=datetime.datetime.now(datetime.timezone.utc).isoformat())
x['readScope'].update(nextUntouched=nextcard,ownD=str(D))
x['takeoverUsage']='After ACTIVATE only copy this own tracked template to successor ownD/takeover.py; inspect old ownIntake '+str(x['ownIntakeCURRENT'])+' -> new '+str(n)+' identity/intake replacements, execute exact native supported takeover. Preserve pendingBoundedWork before any untouched96. No SOURCE/QA replay.'
x['helpers'].update({p.name:str(p) for p in [D/'refresh-native-diagnostics.py',D/'verify-closure.py',D/'verify-successor-ack.py',D/'audit-bootstrap.py',pathlib.Path(__file__)]})
point={'owner':m.O,'CURRENT':n,'remaining':2000-n,'fullGoal':2000,'ownIntake':x['ownIntakeCURRENT'],'ownNewlyCertified':n-x['ownIntakeCURRENT'],'manifest':str(D/'manifest.json'),'nextUntouched':nextcard,'pendingBoundedWork':pending,'pendingReviews':[],'retainedIdleReviewer':retained,'coordinatorSlices':len(x['coordinatorSlicesToPreserve']),'ownOrders89through95':own,'source95ProceduralDeviations':x.get('source95CombinedProceduralDeviations'),'source91OriginalMechanicalFAIL':str(D/'source91-original-format-diagnostics.json'),'source91Cycle1ENOSPC':str(D/'source91-cycle1-save-diagnostics.json'),'releaseRecovery':str(D/'release-recovery.json'),'takeover':str(D/'takeover.json'),'source83':'Original raw candidate/sourceproof byteexact at463701e1 in predecessor directory; original mechanicalFAIL/literalclarification/INITIALFIX retained, credited only after SAME-reader solecycle1FINALPASS. No alias replay.','source87':x['pendingHistoryRussia87'],'source88':x['pendingHistoryRussia88'],'observation73':x['scopeLimitedObservationFromInitial87'],'scope':restrictions,'handoff':nextaction}
m.write(D/'continuation-point.json',point)
for p in [D/'manifest.json',D/'handoff-next.json']:m.write(p,x)
cc=m.savecode([D/'manifest.json',D/'handoff-next.json',D/'continuation-point.json',pathlib.Path(__file__)],f'Preserve bounded89-95 CURRENT{n} full2000 successor handoff')
idx=pathlib.Path(m.h.git(m.P,'rev-parse','--path-format=absolute','--git-path','index'));expected=m.raw(idx);assert expected==x['foreignIndexes']['planning']
with m.flow.locked():m.flow.lease('acquire','planning',m.O)
try:
 assert m.raw(idx)==expected and all(m.flow.get(cid)[1]['owner']==m.O for cid in x['claims'])
 paths=[cp_path,m.P/'evidence/question-revision-process-v2/coordinator-state.json',m.P/'evidence/question-revision-process-v2/active-full2000-goal-01a1593a.json']
 for p in paths:
  d=m.read(p);assert d['owner']==m.O;d.update(phase=x['phase'],currentManifest=str(D/'manifest.json'),next=x['next'],rootNativeAudit=x['rootNativeAudit'],rootActualCompactions=comp,coordinatorActualCompactions=comp,handoffVerification=x['handoffVerification'],handoffVerificationNative=x['handoffVerificationNative'],currentSourceActors=[],currentIndependentActors=[],currentSourceActiveCount=0,nativeActorsCurrent=[retained] if retained else [],retainedIdleReviewer=retained,activeAuthors=[],idleAuthors=[],activeIndependentReview=None)
  d['boundedSource89_95Closure']={'owner':m.O,'CURRENT':n,'remaining':2000-n,'ownIntake':x['ownIntakeCURRENT'],'ownNewlyCertified':n-x['ownIntakeCURRENT'],'ownResults':own,'pendingBoundedWork':pending,'codeCommit':cc,'nextUntouched':nextcard,'source95ProceduralDeviations':x.get('source95CombinedProceduralDeviations'),'observation73':x['scopeLimitedObservationFromInitial87']}
  m.write(p,d)
 pc=m.h.save(m.P,'refs/heads/'+x['planningBranch'],[str(p.relative_to(m.P))for p in paths],f'Preserve bounded89-95 CURRENT{n} full2000 continuation',expected)
finally:
 with m.flow.locked():m.flow.lease('release','planning',m.O)
assert m.read(m.P/'.flow-leases.json')=={}
print({'code':cc,'planning':pc,'CURRENT':n,'remaining':2000-n,'actualCompactions':comp,'nextUntouched':nextcard,'pendingBoundedWork':len(pending),'retainedReviewer':retained['threadId']if retained else None})
