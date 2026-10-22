"""Close only already-started77/78 after terminal disposition; no new SOURCE."""
import pathlib,json,importlib.util
D=pathlib.Path(__file__).parent
s=importlib.util.spec_from_file_location('m',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
x=m.read(D/'manifest.json');assert not x['sourceActorKeys'] and not x.get('pendingFinal77Reviewer') and not any(a['stage'].startswith('START') for a in x['actors'].values())
assert all(x['actors']['author'+str(n)]['archived'] for n in range(71,79))
rr=[json.loads(l) for l in pathlib.Path(x['rootNativeAudit']['nativeJournal']).open()];comp=sum(r['type']=='compacted' for r in rr);assert comp==1
x['rootNativeAudit']['actualCompactions']=comp
rp=pathlib.Path(x['actors']['reviewer']['nativeJournal']);rrr=[json.loads(l) for l in rp.open()];assert next(r['payload']['id'] for r in rrr if r['type']=='session_meta')==x['actors']['reviewer']['threadId']
tok=[r['payload']['info'] for r in rrr if r.get('type')=='event_msg' and r['payload'].get('type')=='token_count'][-1]
x['actors']['reviewer'].update(actualCompactions=sum(r['type']=='compacted' for r in rrr),lastInput=tok['last_token_usage']['input_tokens'],modelWindow=tok['model_context_window'])
assert x['actors']['reviewer']['actualCompactions']==0
completion={}
for order in range(71,79):
 p=x['pendingHistoryRussia'+str(order)];a=x['actors']['author'+str(order)]
 completion[str(order)]={'status':p['status'],'qualityCredit':p['qualityCredit'],'authorArchived':True,'actualCompactions':1 if order==77 else 0,'threadId':a['threadId'],'uncuredSourceDeviation':p.get('sourceProvenanceDeviation')}
q=m.read(m.C/'src/content/topics/history-russia.json')['questions'][78]
assert q['id'] not in m.read(pathlib.Path(x['canonicalCheckpoint']))['currentEligibleCompletedIds']
nextmeta={'id':q['id'],'topicId':'history-russia','sourceOrder':79,'difficulty':q['difficulty'],'correctIndex':q['correctIndex'],'hash':m.sha(q)}
x.update(phase='READY_FOR_READONLY_SUCCESSOR_CURRENT'+str(x['CURRENT']),rootActualCompactions=comp,actualCompactions=comp,ownSourceCompletion=completion,retainedIdleReviewer=dict(x['actors']['reviewer']),noRetainedIdleReviewer=False,noRetainedIdleAuthor=True,retainedIdleAuthorsCurrentOwner=[],currentSourceActors=[],currentIndependentActors=[],currentSourceActorsCount=0,sourceActorKeys=[],pendingFinal77Reviewer=None,nextUntouched=nextmeta,takeoverTemplate=str(D/'takeover-template.py'),rootContextReason='First actual compaction: completed only already-started77/78; stop new SOURCE and transfer full2000 ownership through READONLY ACK then supported exact3 release then ACTIVATE.',next='Readonly successor ACK, supported exact3 release and ACTIVATE. Successor archives stopped root after durable takeover, then next untouched79. Full goal2000 unchanged.',currentWork={'stage':'READY_FOR_READONLY_SUCCESSOR','CURRENT':x['CURRENT'],'remaining':x['remaining'],'fullGoal':2000},handoffVerification=str(D/'handoff-verification.json'))
x['readScope']['nextUntouched']=nextmeta
for p in [D/'manifest.json',D/'handoff-next.json']:m.write(p,x)
v=m.read(D/'continuation-point.json');v.update(rootActualCompactionsAtPoint=comp,CURRENT=x['CURRENT'],remaining=x['remaining'],ownNew=x['newlyCertified'],source77=x['pendingHistoryRussia77'],source78=x['pendingHistoryRussia78'],reader=x['actors']['reviewer'],awaitingOwnDispositionAuthors={},next=x['next']);m.write(D/'continuation-point.json',v)
print('closingCode',m.savecode([D/'manifest.json',D/'handoff-next.json',D/'continuation-point.json',pathlib.Path(__file__)],f'Close current77-78 exact{x["CURRENT"]} bounded slice for supported replacement'))
idx=pathlib.Path(m.h.git(m.P,'rev-parse','--path-format=absolute','--git-path','index'));expected=x['foreignIndexes']['planning'];assert m.raw(idx)==expected
with m.flow.locked():m.flow.lease('acquire','planning',m.O)
try:
 paths=[pathlib.Path(x['canonicalCheckpoint']),m.P/'evidence/question-revision-process-v2/coordinator-state.json',m.P/'evidence/question-revision-process-v2/active-full2000-goal-01a1593a.json']
 for p in paths:
  obj=m.read(p);assert obj['owner']==m.O;obj.update(phase=x['phase'],rootActualCompactions=comp,coordinatorActualCompactions=comp,rootNativeAudit=x['rootNativeAudit'],currentSourceActors=[],currentIndependentActors=[],activeAuthors=[],idleAuthors=[],activeIndependentReview=None,pendingSuccessor=None,successorThreadId=None,retainedIdleReviewer=x['retainedIdleReviewer'],next=x['next'],handoffVerification=x['handoffVerification']);m.write(p,obj)
 print('closingPlanning',m.h.save(m.P,'refs/heads/'+x['planningBranch'],[str(p.relative_to(m.P)) for p in paths],f'Record exact{x["CURRENT"]} no-active-task readonly-successor boundary',expected))
finally:
 with m.flow.locked():m.flow.lease('release','planning',m.O)
print('nextMetadataOnly',nextmeta,'CURRENT',x['CURRENT'],'remaining',x['remaining'])
