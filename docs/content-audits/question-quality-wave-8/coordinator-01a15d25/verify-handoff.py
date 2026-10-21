"""Fresh deterministic preservation facts; no source quality assessment or tests."""
import pathlib,importlib.util,json,hashlib
D=pathlib.Path(__file__).parent
s=importlib.util.spec_from_file_location('m',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
x=m.read(D/'manifest.json');cp=m.read(pathlib.Path(x['canonicalCheckpoint']))
assert cp['owner']==m.O and x['CURRENT']==934 and x['remaining']==1066
cards={};topics={}
for t in {s['topicId'] for s in cp['selectedCards']}:
 topics[t]=m.read(m.C/f'src/content/topics/{t}.json')['questions']
 for q in topics[t]:cards[q['id']]=q
selected=cp['selectedCards'];ids={s['questionId'] for s in selected};done=set(cp['currentEligibleCompletedIds']);remaining=set(cp['currentRemainingIds'])
assert len(ids)==len(selected)==2000 and len(done)==934 and len(remaining)==1066 and done.isdisjoint(remaining) and done|remaining==ids
hashes={s['questionId']:s['cardCanonicalSha256'] for s in cp['completedCardHashes']};assert set(hashes)==done and all(m.sha(cards[i])==h for i,h in hashes.items())
assert all(cards[s['questionId']]['difficulty']==s['difficulty'] and type(cards[s['questionId']]['correctIndex']) is int and cards[s['questionId']]['correctIndex']==s['correctIndex'] for s in selected)
assert all([s['questionId'] for s in selected if s['topicId']==t]==[q['id'] for q in topics[t]] for t in topics)
for root,label in [(m.C,'code'),(m.P,'planning')]:
 idx=pathlib.Path(m.h.git(root,'rev-parse','--path-format=absolute','--git-path','index'));assert m.raw(idx)==x['foreignIndexes'][label]
assert all(m.flow.get(cid)[1]['owner']==m.O for cid in x['claims']) and m.read(m.P/'.flow-leases.json')=={}
rs=[json.loads(l) for l in pathlib.Path(x['rootNativeAudit']['nativeJournal']).open()];assert rs[0]['payload']['id']==m.O;comp=sum(r['type']=='compacted' for r in rs);assert comp==0
last=next(r['payload']['info'] for r in reversed(rs) if r.get('payload',{}).get('type')=='token_count');x['rootNativeAudit'].update(actualCompactions=comp,lastInput=last['last_token_usage']['input_tokens'],modelWindow=last['model_context_window'])
tracked=m.h.git(m.C,'ls-tree','-r','--name-only','HEAD','--',str(D.relative_to(m.C))).splitlines()
for f in tracked:assert m.h.git(m.C,'hash-object',f)==m.h.git(m.C,'rev-parse','HEAD:'+f),f
extras=[str(p.relative_to(m.C)) for p in D.rglob('*') if p.is_file() and str(p.relative_to(m.C)) not in tracked];assert not extras,extras
for run in x['ownAffectedRuns']:
 qa=m.read(run['path']);assert qa['success'] and qa['numPassedTests']==19 and qa['numFailedTests']==qa['numPendingTests']==0
assert len(x['ownAffectedRuns'])==4 and len(x['coordinatorSlicesToPreserve'])==22
main=m.h.git(m.C,'ls-remote','origin','refs/heads/main').split()[0]
remoteTopic=json.loads(m.h.git(m.C,'show',main+':src/content/topics/history-russia.json'));remoteCards={q['id']:q for q in remoteTopic['questions']}
assert all(m.sha(remoteCards[x['pendingHistoryRussia'+str(o)]['id']])!=x['pendingHistoryRussia'+str(o)]['cardHash'] for o in [9,10])
report={'CURRENT':934,'remaining':1066,'fullGoal':2000,'all934CurrentHashes':True,'exact934and1066Partition':True,'all2000FrozenOrderDifficultyNumericKey':True,'source9and10SameReaderFINALsolecycle1PASS':[x['pendingHistoryRussia'+str(o)]['certificate'] for o in [9,10]],'priorHOLDsPreserved':True,'affectedContentRuns':4,'each':'19PASS/0FAIL/0pending','typecheck':'NotRun JSON-only','runtime':'NotRun','foreignIndexesPreserved':x['foreignIndexes'],'claimsExact3Owner':m.O,'leaseHeld':False,'ownTrackedPermanentDiskToHEAD':len(tracked),'ownExtras':extras,'mainRemoteSHA':main,'mainAccepted9and10HashPresent':False,'mainIntegrated':False,'ownActualCompactions':comp,'nativeAudit':x['rootNativeAudit']}
x.update(handoffVerification=str(D/'handoff-verification.json'),helperIdentityFence='Owned helpers bound d08/intake931 -> d25/intake932; prepare-source forwards current order priorSourceAttemptMetadata plus old8 captureloss and previousSource9NetworkAccounting. Historical46INITIAL/83source template immutable. Dynamic sourceIndex10cycle1 and additional9/10initial/old7 indexes remain actual saved paths.',actors={'reviewer':x['actors']['reviewer']},retainedIdleReviewer=x['actors']['reviewer'],currentSourceActorsCount=0,sourceActorKeys=[],noRetainedIdleAuthor=True)
m.write(D/'manifest.json',x);m.write(D/'handoff-next.json',x);m.write(D/'handoff-verification.json',report)
print(m.savecode([D/'manifest.json',D/'handoff-next.json',D/'handoff-verification.json',pathlib.Path(__file__)],'Preserve verified CURRENT934 compact successor handoff'))
print(json.dumps(report,ensure_ascii=False))
