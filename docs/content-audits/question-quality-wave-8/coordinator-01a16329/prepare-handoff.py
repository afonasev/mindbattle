"""Close this bounded slice and prepare one supported successor; no claim transfer or content edits."""
import pathlib,importlib.util,json,datetime
D=pathlib.Path(__file__).parent
s=importlib.util.spec_from_file_location('m',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
x=m.read(D/'manifest.json');cp_path=pathlib.Path(x['canonicalCheckpoint']);cp=m.read(cp_path);n=len(cp['currentEligibleCompletedIds'])
assert cp['owner']==m.O and n==x['CURRENT'] and x['remaining']==2000-n
assert all(a.get('archived') for k,a in x['actors'].items() if k.startswith('author'))
a=x['actors']['reviewer'];assert not a['stage'].startswith('START') and x.get('pendingFinal87Reviewer') is None and x.get('pendingFinal88Reviewer') is None
rows=[json.loads(l) for l in open(x['rootNativeAudit']['nativeJournal'])];assert next(r['payload']['id'] for r in rows if r['type']=='session_meta')==m.O
comp=sum(r['type']=='compacted' for r in rows);assert comp==1
info=next(r['payload']['info'] for r in reversed(rows) if r.get('payload',{}).get('type')=='token_count')
x['rootNativeAudit'].update(actualCompactions=comp,lastInput=info['last_token_usage']['input_tokens'],modelWindow=info['model_context_window'])
q=m.read(m.C/'src/content/topics/history-russia.json')['questions'][88]
assert q['id'] in cp['currentRemainingIds']
nextcard={'id':q['id'],'topicId':'history-russia','sourceOrder':89,'difficulty':q['difficulty'],'correctIndex':q['correctIndex'],'hash':m.sha(q)}
retained=None if a.get('archived') else dict(a)
x.update(phase=f'READY_FOR_READONLY_SUCCESSOR_CURRENT{n}',rootActualCompactions=comp,actualCompactions=comp,nextUntouched=nextcard,retainedIdleReviewer=retained,noRetainedIdleReviewer=retained is None,noRetainedIdleAuthor=True,retainedIdleAuthorsCurrentOwner=[],currentSourceActors=[],currentIndependentActors=[],currentSourceActorsCount=0,sourceActorKeys=[],currentWork={'stage':'BOUNDED87_88_COMPLETE_PENDING_SUPPORTED_HANDOFF','CURRENT':n,'remaining':2000-n},next='One READONLY successor bootstrap ACK, supported exact3 release, ACTIVATE exact native successor; predecessor then stops. Successor continues full2000 from untouched89 without new GO.',takeoverTemplate=str(D/'takeover-template.py'),continuationPoint=str(D/'continuation-point.json'),handoffVerification=str(D/'handoff-verification.json'),handoffVerificationNative=str(D/'technical-native-diagnostics.json'),at=datetime.datetime.now(datetime.timezone.utc).isoformat())
x['readScope'].update(nextUntouched=nextcard,ownD=str(D))
x['takeoverUsage']='After ACTIVATE only copy this own tracked template to successor ownD/takeover.py, inspect exact old982 to new'+str(n)+' substitutions and native identity, execute supported exact3 takeover. No SOURCE alias/intake/QA replay.'
x['handoffRestrictions']='Root first actualcomp1: no new SOURCE89 here. One supported successor continues full2000 without new human GO after READONLY ACK -> exact3 release -> ACTIVATE. Preserve original FAIL/raw83, all HOLD0 and exhausted attempts, no ordinarycycle2/reset/newINITIAL for consumed fixes, max2SOURCE/max1reader/readyqueue2. No mainmerge/fulltests/runtime/browser/Player/build/deploy/release/OpenSpecarchive. Potential peer73 observation remains unassessed, not fixed or credited via87.'
x['helpers'].update({p.name:str(p) for p in [D/'refresh-native-diagnostics.py',D/'verify-closure.py',pathlib.Path(__file__)]})
point={'owner':m.O,'CURRENT':n,'remaining':2000-n,'fullGoal':2000,'ownIntake':982,'ownNewlyCertified':n-988,'manifest':str(D/'manifest.json'),'nextUntouched':nextcard,'pendingReviews':[],'handoff':'READONLY successor ACK then supported release and ACTIVATE; no quality/control after predecessor release','source83':'Original mechanical FAIL/raw and literal clarification preserved; original INITIALFIX retained; independent same-reader FINALPASS before credit1','source87':x['pendingHistoryRussia87'],'source88':x['pendingHistoryRussia88'],'observation73':x['scopeLimitedObservationFromInitial87'],'scope':x['handoffRestrictions']}
m.write(D/'continuation-point.json',point)
for p in [D/'manifest.json',D/'handoff-next.json']:m.write(p,x)
cc=m.savecode([D/'manifest.json',D/'handoff-next.json',D/'continuation-point.json',pathlib.Path(__file__)],'Preserve bounded source87-88 closure and exact full2000 successor handoff')
idx=pathlib.Path(m.h.git(m.P,'rev-parse','--path-format=absolute','--git-path','index'));expected=m.raw(idx);assert expected==x['foreignIndexes']['planning']
with m.flow.locked():m.flow.lease('acquire','planning',m.O)
try:
 assert m.raw(idx)==expected and all(m.flow.get(cid)[1]['owner']==m.O for cid in x['claims'])
 paths=[cp_path,m.P/'evidence/question-revision-process-v2/coordinator-state.json',m.P/'evidence/question-revision-process-v2/active-full2000-goal-01a1593a.json']
 for p in paths:
  d=m.read(p);assert d['owner']==m.O;d.update(phase=x['phase'],currentManifest=str(D/'manifest.json'),next=x['next'],rootNativeAudit=x['rootNativeAudit'],rootActualCompactions=comp,coordinatorActualCompactions=comp,handoffVerification=x['handoffVerification'],handoffVerificationNative=x['handoffVerificationNative'],currentSourceActors=[],currentIndependentActors=[],currentSourceActiveCount=0,nativeActorsCurrent=[retained] if retained else [],retainedIdleReviewer=retained,activeAuthors=[],idleAuthors=[],activeIndependentReview=None)
  d['boundedSource87_88Closure']={'owner':m.O,'CURRENT':n,'remaining':2000-n,'source87':x['pendingHistoryRussia87'],'source88':x['pendingHistoryRussia88'],'codeCommit':cc,'nextUntouched':nextcard,'observation73':x['scopeLimitedObservationFromInitial87']}
  m.write(p,d)
 pc=m.h.save(m.P,'refs/heads/'+x['planningBranch'],[str(p.relative_to(m.P)) for p in paths],'Preserve bounded source87-88 terminal status and full2000 continuation',expected)
finally:
 with m.flow.locked():m.flow.lease('release','planning',m.O)
assert m.read(m.P/'.flow-leases.json')=={}
print({'code':cc,'planning':pc,'CURRENT':n,'remaining':2000-n,'rootActualCompactions':comp,'nextUntouched':nextcard,'retainedReviewer':retained['threadId'] if retained else None})
