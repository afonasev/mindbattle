"""Closed active cars-road-transport SOURCE slice only: prepare one readonly successor barrier, keep ownership."""
import pathlib,json,re,datetime,importlib.util
D=pathlib.Path(__file__).parent
s=importlib.util.spec_from_file_location('m',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
x=m.read(D/'manifest.json');cp_path=pathlib.Path(x['canonicalCheckpoint']);cp=m.read(cp_path);n=len(cp['currentEligibleCompletedIds'])
assert n==x['CURRENT'] and x['remaining']==2000-n and cp['owner']==cp['activeCoordinator']==m.O
assert all(m.flow.get(cid)[1]['owner']==m.O for cid in x['claims']) and len(x['claims'])==4
assert m.read(m.P/'.flow-leases.json')=={} and not any(a['stage'].startswith('START') for a in x['actors'].values())
assert all(a.get('archived',False) for k,a in x['actors'].items() if k.startswith('author'))
own={int(k.removeprefix('pendingCarsRoadTransport')):v for k,v in x.items() if re.fullmatch('pendingCarsRoadTransport[0-9]+',k) and int(k.removeprefix('pendingCarsRoadTransport')) in x['ownedSourceOrders']}
assert own
for order,p in own.items():
 if p['qualityCredit']==1:assert p['status'].startswith('CERTIFIED_')
 else:assert 'HOLD' in p['status'] and not any(t in p['status'] for t in ['PENDING','START','READY'])
verification=m.read(D/'handoff-verification.json');assert verification['CURRENT']==n and verification['allCurrentAcceptedHashesExact'] and verification['all2000FrozenIdTopicOrderDifficultyNumericKey']
rows=[json.loads(l) for l in pathlib.Path(x['rootNativeAudit']['nativeJournal']).open()]
assert [r['payload']['id'] for r in rows if r.get('type')=='session_meta']==[m.O]
parent_turn=next(r['payload']['turn_id'] for r in reversed(rows) if r.get('payload',{}).get('type')=='task_started')
info=next(r['payload']['info'] for r in reversed(rows) if r.get('payload',{}).get('type')=='token_count');comp=sum(r.get('type')=='compacted' for r in rows)
next_order=max(own)+1;topic=x['activeRoute']['topicId'];topic_cards=m.read(m.C/f'src/content/topics/{topic}.json')['questions'];route_frontier=False
if next_order<=len(topic_cards):
 q=topic_cards[next_order-1]
 assert q['id'] not in cp['currentEligibleCompletedIds'];f=next(v for v in cp['selectedCards'] if v['questionId']==q['id']);assert f['topicId']==topic and f['difficulty']==q['difficulty'] and f['correctIndex']==q['correctIndex']
 nextcard={'id':q['id'],'topicId':topic,'sourceOrder':next_order,'difficulty':q['difficulty'],'correctIndex':q['correctIndex'],'hash':m.sha(q)}
else:
 # Canonical topic boundary, never index101 into a100-card topic or reopen its HOLDs.
 assert next_order==len(topic_cards)+1 and x['routeFrontier']['requiresSupportedBinding']
 frontier=m.read(D/'route-frontier.json');assert frontier['owner']==m.O and frontier['CURRENT']==n and frontier['remaining']==2000-n
 assert frontier['closedTopic']==topic and frontier['requiresSupportedNewOwnerRouteBindingBeforeSOURCE']
 wave=next(w for w in cp['waves'] if w['changeId']==x['activeRoute']['waveChangeId']);selection={e['questionId']:e for e in cp['selectedCards']}
 topic_order=list(dict.fromkeys(selection[qid]['topicId'] for qid in wave['selectedIds']));assert topic_order==frontier['topicOrderFromOriginalSelectedIds']
 nextcard=frontier['nextUntouched'];assert nextcard['topicId']==topic_order[topic_order.index(topic)+1]
 next_cards=m.read(m.C/f"src/content/topics/{nextcard['topicId']}.json")['questions'];matches=[(i,q) for i,q in enumerate(next_cards,1) if q['id']==nextcard['id']];assert len(matches)==1
 position,q=matches[0];assert position==nextcard['sourceOrder']==1 and q['id'] not in cp['currentEligibleCompletedIds']
 f=selection[q['id']];assert f['topicId']==nextcard['topicId'] and f['difficulty']==q['difficulty']==nextcard['difficulty'] and f['correctIndex']==q['correctIndex']==nextcard['correctIndex']
 assert m.sha(q)==nextcard['hash']==f['baselineCanonicalSha256'];route_frontier=True
a=x['actors']['reviewer'];retained=None
if not a.get('archived',False):
 assert a['stage'].startswith('IDLE_') and a['lastTaskEvent']=='task_complete'
 retained=dict(a)
reason={'actualCompactions':comp,'lastInput':info['last_token_usage']['input_tokens'],'window':info['model_context_window'],'remaining':info['model_context_window']-info['last_token_usage']['input_tokens'],'meaning':'Real remaining context before new-card routing, not a summary reset; closed owned slice preserved for one replacement coordinator.'}
next_action='One READONLY native successor ACK, supported EXACT4 release then ACTIVATE. Successor takes all4/CP/state/full2000goal under private CAS and short P lease, archives stopped predecessor, continues full2000 autonomously without new human GO. Fresh actual native/context budget before next SOURCE or reader assignment; all old/new HOLD0 and attempt/fix/alias fences persist.'
if route_frontier:
 reason['meaning']='Actual remaining native context at the canonical topic frontier; preserve the single-topic owned range and intake before a new bounded route. No compaction/context reset and no broad multi-topic helper rewrite.'
 next_action+=' At this frontier personally read route-frontier.json; existing helpers remain bound to cars-road-transport. Only after durable takeover and parent archive bind own activeRoute/readScope/templates/paths/narrow helpers to exact canonical cars-road-transport/wave9, then start untouched1. No SOURCE via legacy cars-road-transport paths; no old HOLD reopening.'
x.update(phase='READY_FOR_READONLY_SUCCESSOR_CURRENT'+str(n),claimsOwner=m.O,heldOwn=list(x['claims']),nextUntouched=nextcard,currentWork={'stage':'CLOSED_OWNED_SLICE_CURRENT'+str(n),'CURRENT':n,'remaining':2000-n,'fullGoal':2000},next=next_action,pendingBoundedWork=[],pendingReviews=[],sourceActorKeys=[],currentSourceActors=[],currentIndependentActors=[],currentSourceActorsCount=0,readyQueue=[],retainedIdleReviewer=retained,noRetainedIdleReviewer=retained is None,noRetainedIdleAuthor=True,retainedIdleAuthorsCurrentOwner=[],rootContextReason=reason,actualCompactions=comp,rootActualCompactions=comp,currentOwnedHandoffHelper=str(pathlib.Path(__file__)),closingVerificationCode=str(D/'verify-routed-closure.py'),closingVerificationPassed=True,handoffVerification=str(D/'handoff-verification.json'),continuationPoint=str(D/'continuation-point.json'),technicalDiagnosticsAuthority=str(D/'technical-native-diagnostics.json'),pendingSuccessor=None,successor=None,successorThreadId=None,successorStatus='AWAITING_READONLY_BOOTSTRAP',ordinaryWorkActivated=False,leaseHeld=False,at=datetime.datetime.now(datetime.timezone.utc).isoformat())
x['readScope']={**x['readScope'],'ownD':str(D),'nextUntouched':nextcard}
x['parentCurrentActiveTurnId']=parent_turn
x['rootNativeAudit'].update(actualCompactions=comp,lastInput=reason['lastInput'],modelWindow=reason['window'])
x['helpers'][pathlib.Path(__file__).name]=str(pathlib.Path(__file__))
diagnostics={'rootCounts':reason,'actorCounts':{'archivedAuthors':sum(k.startswith('author') and a.get('archived',False) for k,a in x['actors'].items()),'activeAuthors':0,'activeIndependentReviews':0,'retainedIdleReaders':1 if retained else 0},'retainedReaderCounts':{k:retained.get(k) for k in ['threadId','actualCompactions','lastInput','modelWindow','lastTaskEvent']} if retained else None,'evidencePointers':{'ownProceduralDiagnostics':str(D/'own-procedural-diagnostics.json'),'closedVerification':str(D/'handoff-verification.json'),'inheritedContinuation':str(pathlib.Path(x['predecessorHandoff']).parent/'continuation-point.json')},'scope':'Technical counts and pointers only; no quality credit or procedural cure.'}
m.write(D/'technical-native-diagnostics.json',diagnostics)
for p in [D/'manifest.json',D/'handoff-next.json']:m.write(p,x)
cc=m.savecode([D/'manifest.json',D/'handoff-next.json',D/'technical-native-diagnostics.json',pathlib.Path(__file__)],'Preserve closed CURRENT and one readonly exact4 successor barrier');print('code',cc)
idx=pathlib.Path(m.h.git(m.P,'rev-parse','--path-format=absolute','--git-path','index'));expected=x['foreignIndexes']['planning'];assert m.raw(idx)==expected
with m.flow.locked():m.flow.lease('acquire','planning',m.O)
try:
 assert m.raw(idx)==expected and all(m.flow.get(cid)[1]['owner']==m.O for cid in x['claims'])
 cp=m.read(cp_path);assert cp['owner']==m.O and len(cp['currentEligibleCompletedIds'])==n
 cp.update(phase=x['phase'],currentManifest=str(D/'manifest.json'),next=next_action,currentSourceActors=[],currentSourceActiveCount=0,currentIndependentActors=[],nativeActorsCurrent=[retained] if retained else [],pendingSuccessor=None,successorThreadId=None,successorStatus='AWAITING_READONLY_BOOTSTRAP',ordinaryWorkActivated=False,coordinatorActualCompactions=comp)
 m.write(cp_path,cp)
 sp=m.P/'evidence/question-revision-process-v2/coordinator-state.json';st=m.read(sp);assert st['owner']==m.O
 st.update(phase=x['phase'],currentManifest=str(D/'manifest.json'),currentWork=x['currentWork'],activeAuthors=[],idleAuthors=[],activeIndependentReview=None,nativeActorsCurrent=[retained] if retained else [],currentNativeActors={retained['threadId']:retained} if retained else {},currentSourceActors=[],currentIndependentActors=[],ownActualCompactions=comp,rootActualCompactions=comp,actualRootCompactions=comp,coordinatorActualCompactions=comp,next=next_action,codeCommit=cc,pendingSuccessor=None,successorThreadId=None,successorStatus='AWAITING_READONLY_BOOTSTRAP',ordinaryWorkActivated=False,counts={'CURRENT':n,'remaining':2000-n})
 m.write(sp,st)
 gp=m.P/'evidence/question-revision-process-v2/active-full2000-goal-01a1593a.json';g=m.read(gp);assert g['owner']==m.O
 g.update(phase=x['phase'],manifest=str(D/'manifest.json'),CURRENT=n,remaining=2000-n,pendingSuccessor=None,successorThreadId=None,successorStatus='AWAITING_READONLY_BOOTSTRAP',latestCodeCommit=cc)
 m.write(gp,g)
 pp=m.P/f'evidence/question-revision-process-v2/closed-handoff-{m.O[:8]}.json';m.write(pp,{'owner':m.O,'CURRENT':n,'remaining':2000-n,'fullGoal':2000,'ownIntake':x['ownIntakeCURRENT'],'ownNewlyCertified':n-x['ownIntakeCURRENT'],'claims':x['claims'],'codeCommit':cc,'handoff':str(D/'handoff-next.json'),'nextUntouched':nextcard,'retainedIdleReviewer':retained,'rootContext':reason,'noNewHumanGORequired':True,'ordinaryParentSourceStopped':True})
 pc=m.h.save(m.P,'refs/heads/'+x['planningBranch'],[str(p.relative_to(m.P)) for p in [cp_path,sp,gp,pp]],'Preserve closed exact2000 successor barrier without releasing claims',expected);print('planning',pc)
finally:
 with m.flow.locked():m.flow.lease('release','planning',m.O)
x['planningHandoffCommit']=pc
for p in [D/'manifest.json',D/'handoff-next.json']:m.write(p,x)
print('finalCode',m.savecode([D/'manifest.json',D/'handoff-next.json'],'Bind planning handoff commit to preserved readonly barrier'))
print({'CURRENT':n,'remaining':2000-n,'fullGoal':2000,'nextUntouched':nextcard,'claimsStillOwned':4,'actualCompactions':comp,'rootRemainingContext':reason['remaining'],'ordinarySourceStoppedUntilSuccessorTakeover':True})
