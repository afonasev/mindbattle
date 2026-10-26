"""Closed active cars-road-transport SOURCE slice only: prepare one readonly successor barrier, keep ownership."""
import pathlib,json,re,datetime,importlib.util,sys
D=pathlib.Path(__file__).parent
s=importlib.util.spec_from_file_location('m',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
x=m.read(D/'manifest.json');cp_path=pathlib.Path(x['canonicalCheckpoint']);cp=m.read(cp_path);n=len(cp['currentEligibleCompletedIds'])
if '--inventory-only' in sys.argv:
 assert cp['owner']==cp['activeCoordinator']==m.O and all(m.flow.get(c)[1]['owner']==m.O for c in x['claims']) and m.read(m.P/'.flow-leases.json')=={}
 assert not any(a['stage'].startswith('START') for a in x['actors'].values()) and not x.get('readyQueue')
 parent=m.read(pathlib.Path(x['predecessorHandoff']));base=parent['newAttemptFences'];assert x['newAttemptFences'][:len(base)]==base
 inherited=pathlib.Path(parent['ownConsumedSourceFences']);assert m.raw(inherited)
 fp=D/'own-consumed-source-fences.json';m.write(fp,{'owner':m.O,'inheritedPointer':str(inherited),'inheritedRawSHA256':m.raw(inherited),'inheritedFenceCount':len(base),'ownClosedRecords':x['newAttemptFences'][len(base):],'totalFences':len(x['newAttemptFences']),'allUncured':True,'qualityCredit':0})
 x['ownConsumedSourceFences']=str(fp)
 def snapshot(a):
  p=pathlib.Path(a['nativeJournal'])
  if not p.exists():
   paths=list(pathlib.Path('/Users/eaafonasev/.codex/archived_sessions').glob('*'+a['threadId']+'.jsonl'));assert len(paths)==1;p=paths[0]
  rows=[json.loads(l) for l in p.open()];assert [r['payload']['id'] for r in rows if r.get('type')=='session_meta']==[a['threadId']]
  event=next(r['payload']['type'] for r in reversed(rows) if r.get('payload',{}).get('type') in ['task_started','task_complete']);assert event=='task_complete'
  info=next(r['payload']['info'] for r in reversed(rows) if r.get('payload',{}).get('type')=='token_count')
  a.update(nativeJournal=str(p),actualCompactions=sum(r['type']=='compacted' for r in rows),lastTaskEvent=event,lastInput=info['last_token_usage']['input_tokens'],modelWindow=info['model_context_window'])
  return a
 reader=snapshot(x['actors']['reviewer']);assert not reader.get('archived') and reader['actualCompactions']==0
 G=reader['threadId'];seedpath=pathlib.Path(x['predecessorHandoff']).parent/'retained-reader-handoff.json';seed=m.read(seedpath);receipts={};inherited_reader=None
 if seed['retainedIdleReader']['threadId']==G:receipts.update(seed['readerOwnReceipts']);inherited_reader=str(seedpath)
 for path in D.glob('independent-*/receipt.json'):
  r=m.read(path)
  if r.get('reviewerNativeId',r.get('readerNativeId'))!=G:continue
  e=r['entries'][0];receipts[str(path)]={'rawSHA256':m.raw(path),'stage':e['stage'],'status':e['status'],'sourceOrder':e['sourceOrder'],'currentCardCanonicalSHA256':e['currentCardCanonicalSHA256']}
 assert len(receipts)>=reader.get('ownReceiptCount',0)
 reader['ownReceiptCount']=len(receipts)
 retired=list(m.read(D/'retained-reader-handoff.json').get('retiredReaderPointers',[]))
 for p in D.glob('reader*-retirement*.json'):
  if not any(v['path']==str(p) for v in retired):retired.append({'path':str(p),'rawSHA256':m.raw(p)})
 rp=D/'retained-reader-handoff.json';m.write(rp,{'owner':m.O,'retainedIdleReader':dict(reader),'readerOwnReceiptCount':len(receipts),'readerOwnReceipts':receipts,'inheritedImmutable':inherited_reader,'retiredReaderPointers':retired,'scope':'Current native reader exact receipt inventory only; closed retired histories stay pointers, no repeated content/bootstrap audit.'})
 x['currentReaderNativeIdentity']=reader.get('identityProof',x.get('currentReaderNativeIdentity'));assert x['currentReaderNativeIdentity']
 retained=[];unspent=[]
 for key,a in x['actors'].items():
  if not key.startswith('author') or a.get('archived'):continue
  snapshot(a);assert a['stage'].startswith('IDLE_') and (a['actualCompactions']==0 or key=='author60'), 'Archive completed saturated author; preserve protected60'
  batch=x.get('activeAuthorBatches',{}).get(key,{})
  orders=[v for v in batch.get('orders',[]) if not x.get('pendingCarsRoadTransport'+str(v))]
  if a['actualCompactions']==0:unspent+=orders
  retained.append({'actorKey':key,'actor':dict(a),'scope':'Protected inherited actual1 idle; no new card/reset/archive.' if key=='author60' else 'Retained actual0 authorized bounded author; continue unspent or next batch only after real budget check, no rebootstrap/newhumanGO.'})
 x.update(retainedIdleAuthorsForSuccessor=retained,retainedIdleReviewer=dict(reader),unfinishedAuthorBatchOrders=sorted(set(unspent)),fullUserGoal={'target':2000,'CURRENT':n,'remaining':2000-n,'complete':False,'scope':'Full exact2000 remainder; not batch completion'},pendingBoundedWork=[],pendingReviews=[],readyQueue=[])
 x['helpers'][pathlib.Path(__file__).name]=str(pathlib.Path(__file__));m.write(D/'manifest.json',x)
 print(m.savecode([fp,rp,D/'manifest.json',pathlib.Path(__file__)],'Prepare current closed-slice fences, retained native roles and fullgoal handoff inventory'))
 print({'inventoryPrepared':True,'CURRENT':n,'remaining':2000-n,'reader':G,'readerOwn':len(receipts),'fences':len(x['newAttemptFences']),'unspent':x['unfinishedAuthorBatchOrders']})
 raise SystemExit(0)
assert n==x['CURRENT'] and x['remaining']==2000-n and cp['owner']==cp['activeCoordinator']==m.O
assert all(m.flow.get(cid)[1]['owner']==m.O for cid in x['claims']) and len(x['claims'])==4
assert m.read(m.P/'.flow-leases.json')=={} and not any(a['stage'].startswith('START') for a in x['actors'].values())
retained_authors=x.get('retainedIdleAuthorsForSuccessor',[])
assert all(a.get('archived',False) or any(v['actor']['threadId']==a['threadId'] for v in retained_authors) for k,a in x['actors'].items() if k.startswith('author'))
assert all(v['actor']['stage'].startswith('IDLE_') and v['actor']['lastTaskEvent']=='task_complete' for v in retained_authors)
own={int(k.removeprefix('pendingCarsRoadTransport')):v for k,v in x.items() if re.fullmatch('pendingCarsRoadTransport[0-9]+',k) and int(k.removeprefix('pendingCarsRoadTransport')) in x['ownedSourceOrders']}
assert own
for order,p in own.items():
 if p['qualityCredit']==1:
  assert p['id'] in cp['currentEligibleCompletedIds']
  certificate=m.read(p['certification']);assert certificate['newQualityCredit']==1 and any(e['questionId']==p['id'] for e in certificate['accepted'])
 else:assert 'HOLD' in p['status'] and not any(t in p['status'] for t in ['PENDING','START','READY'])
verification=m.read(D/'handoff-verification.json');assert verification['CURRENT']==n and verification['allCurrentAcceptedHashesExact'] and verification['all2000FrozenIdTopicOrderDifficultyNumericKey']
rows=[json.loads(l) for l in pathlib.Path(x['rootNativeAudit']['nativeJournal']).open()]
assert [r['payload']['id'] for r in rows if r.get('type')=='session_meta']==[m.O]
parent_turn=next(r['payload']['turn_id'] for r in reversed(rows) if r.get('payload',{}).get('type')=='task_started')
info=next(r['payload']['info'] for r in reversed(rows) if r.get('payload',{}).get('type')=='token_count');comp=sum(r.get('type')=='compacted' for r in rows)
next_order=min(x.get('unfinishedAuthorBatchOrders') or [max(own)+1]);topic=x['activeRoute']['topicId'];topic_cards=m.read(m.C/f'src/content/topics/{topic}.json')['questions'];route_frontier=False
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
next_action=(f'Continue FULL exact2000 CURRENT{n}, remaining{2000-n}, next untouched {nextcard["topicId"]}/{nextcard["sourceOrder"]}; never shrink to pilot/batch. One compact READONLY intake/checker after INTAKE READY, then supported exact4 release/ACTIVATE/takeover, durable CP/state/fullgoal/per-wave ownership, parent latest exact task_complete/archive. Use current retained actor native IDs/models/budgets from manifest, never stale historical role names. If existing bounded orders are exhausted, prepare next bounded assignments within fullgoal using retained actual0 roles only after real budget assessment; no rebootstrap/newhumanGO. Fresh roles only budget/compaction need with immutable old native/receipts, no existingmodel switch. Same reader INITIAL+sole directed FINAL percard, max1fix/no third full review. Max2activeauthors/1reviewer/READYqueue2. Minimal affected19 per realcatalogdiff, shared whenpossible; no metadata rerun. Preserve all closed HOLD/FAIL/attempt/cycle fences and explicit inadmissible captures, no exhaustedclaim route-around. Author edits all necessary coherent texts; frozen onlyID/topic/order/difficulty/integerkey. Saved full primary contexts before network, primary+oneofficialalt includes discovery, JSON nativeoriginals, no .content assumption/slice+refetch. READY/HOLD immediately freezes ALL raw files even before Git; changes use separateaddendum only. Keep all concrete historical caveats in own-procedural-diagnostics and certificates, no retroactive cure or repeated finished-card processing. Firstcompaction finishes only already-started card, second preservationSTOP. No mainmerge/fullsuite/runtime/browser/Player/build/deploy/release/OpenSpecarchive. At saturation transfer ONE coordinator with fullgoal and stop old control; original active goal gets only actualfullcompletion evidence report.')
if route_frontier:
 reason['meaning']='Actual remaining native context at the canonical topic frontier; preserve the single-topic owned range and intake before a new bounded route. No compaction/context reset and no broad multi-topic helper rewrite.'
 next_action+=' At this frontier personally read route-frontier.json; existing helpers remain bound to cars-road-transport. Only after durable takeover and parent archive bind own activeRoute/readScope/templates/paths/narrow helpers to exact canonical cars-road-transport/wave9, then start untouched1. No SOURCE via legacy cars-road-transport paths; no old HOLD reopening.'
x.update(phase='READY_FOR_READONLY_SUCCESSOR_CURRENT'+str(n),claimsOwner=m.O,heldOwn=list(x['claims']),nextUntouched=nextcard,currentWork={'stage':'CLOSED_OWNED_SLICE_CURRENT'+str(n),'CURRENT':n,'remaining':2000-n,'fullGoal':2000},next=next_action,pendingBoundedWork=[],pendingReviews=[],sourceActorKeys=[],currentSourceActors=[],currentIndependentActors=[],currentSourceActorsCount=0,readyQueue=[],retainedIdleReviewer=retained,noRetainedIdleReviewer=retained is None,noRetainedIdleAuthor=not retained_authors,retainedIdleAuthorsCurrentOwner=[v['actor']['threadId'] for v in retained_authors],rootContextReason=reason,actualCompactions=comp,rootActualCompactions=comp,currentOwnedHandoffHelper=str(pathlib.Path(__file__)),closingVerificationCode=str(D/'verify-current-handoff.py'),closingVerificationPassed=True,handoffVerification=str(D/'handoff-verification.json'),continuationPoint=str(D/'continuation-point.json'),technicalDiagnosticsAuthority=str(D/'technical-native-diagnostics.json'),pendingSuccessor=None,successor=None,successorThreadId=None,successorStatus='AWAITING_READONLY_BOOTSTRAP',ordinaryWorkActivated=False,leaseHeld=False,at=datetime.datetime.now(datetime.timezone.utc).isoformat())
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
 cp.update(phase=x['phase'],currentManifest=str(D/'manifest.json'),next=next_action,currentSourceActors=[],currentSourceActiveCount=0,currentIndependentActors=[],nativeActorsCurrent=([retained] if retained else [])+[v['actor'] for v in retained_authors],pendingSuccessor=None,successorThreadId=None,successorStatus='AWAITING_READONLY_BOOTSTRAP',ordinaryWorkActivated=False,coordinatorActualCompactions=comp)
 m.write(cp_path,cp)
 sp=m.P/'evidence/question-revision-process-v2/coordinator-state.json';st=m.read(sp);assert st['owner']==m.O
 st.update(phase=x['phase'],currentManifest=str(D/'manifest.json'),currentWork=x['currentWork'],activeAuthors=[],idleAuthors=[v['actor'] for v in retained_authors],activeIndependentReview=None,nativeActorsCurrent=([retained] if retained else [])+[v['actor'] for v in retained_authors],currentNativeActors={a['threadId']:a for a in ([retained] if retained else [])+[v['actor'] for v in retained_authors]},currentSourceActors=[],currentIndependentActors=[],ownActualCompactions=comp,rootActualCompactions=comp,actualRootCompactions=comp,coordinatorActualCompactions=comp,next=next_action,codeCommit=cc,pendingSuccessor=None,successorThreadId=None,successorStatus='AWAITING_READONLY_BOOTSTRAP',ordinaryWorkActivated=False,counts={'CURRENT':n,'remaining':2000-n})
 m.write(sp,st)
 gp=m.P/'evidence/question-revision-process-v2/active-full2000-goal-01a1593a.json';g=m.read(gp);assert g['owner']==m.O
 g.update(phase=x['phase'],manifest=str(D/'manifest.json'),CURRENT=n,remaining=2000-n,pendingSuccessor=None,successorThreadId=None,successorStatus='AWAITING_READONLY_BOOTSTRAP',latestCodeCommit=cc)
 m.write(gp,g)
 pp=m.P/f'evidence/question-revision-process-v2/closed-handoff-{m.O[:8]}.json';m.write(pp,{'owner':m.O,'CURRENT':n,'remaining':2000-n,'fullGoal':2000,'ownIntake':x['ownIntakeCURRENT'],'ownNewlyCertified':n-x['ownIntakeCURRENT'],'claims':x['claims'],'codeCommit':cc,'handoff':str(D/'handoff-next.json'),'nextUntouched':nextcard,'retainedIdleReviewer':retained,'retainedIdleAuthorsForSuccessor':retained_authors,'processRevision':'2026-10-25','rootContext':reason,'noNewHumanGORequired':True,'ordinaryParentSourceStopped':True})
 pc=m.h.save(m.P,'refs/heads/'+x['planningBranch'],[str(p.relative_to(m.P)) for p in [cp_path,sp,gp,pp]],'Preserve closed exact2000 successor barrier without releasing claims',expected);print('planning',pc)
finally:
 with m.flow.locked():m.flow.lease('release','planning',m.O)
x['planningHandoffCommit']=pc
for p in [D/'manifest.json',D/'handoff-next.json']:m.write(p,x)
print('finalCode',m.savecode([D/'manifest.json',D/'handoff-next.json'],'Bind planning handoff commit to preserved readonly barrier'))
print({'CURRENT':n,'remaining':2000-n,'fullGoal':2000,'nextUntouched':nextcard,'claimsStillOwned':4,'actualCompactions':comp,'rootRemainingContext':reason['remaining'],'ordinarySourceStoppedUntilSuccessorTakeover':True})
