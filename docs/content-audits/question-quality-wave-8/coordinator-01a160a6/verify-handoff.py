"""Read-only CURRENT975 closing snapshot; no QA replay or successor claim."""
import pathlib,json,hashlib,subprocess
D=pathlib.Path(__file__).parent
rd=lambda p:json.loads(pathlib.Path(p).read_text())
raw=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
sha=lambda v:hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
x=rd(D/'manifest.json');C=pathlib.Path(x['C']);P=pathlib.Path(x['P']);O=x['rootNativeAudit']['threadId']
def git(root,*args):return subprocess.check_output(['git','--no-optional-locks','-C',str(root),*args],text=True).strip()
assert x['owner']==x['claimsOwner']==O and x['CURRENT']==975 and x['remaining']==1025 and x['ownIntakeCURRENT']==967 and x['newlyCertified']==8
assert x['phase']=='READY_FOR_READONLY_SUCCESSOR_CURRENT975' and not any(a['stage'].startswith('START') for a in x['actors'].values())
cp=rd(x['canonicalCheckpoint']);a=cp['currentEligibleCompletedIds'];b=cp['currentRemainingIds'];sel=cp['selectedCards'];bound=cp['completedCardHashes'];cat={};orders={};topics={}
for p in sorted((C/'src/content/topics').glob('*.json')):
 t=rd(p);topics[t['id']]=t
 for i,q in enumerate(t['questions'],1):assert q['id'] not in cat;cat[q['id']]=q;orders[q['id']]=i
assert len(topics)==110 and len(cat)==11000
assert len(a)==len(set(a))==len(bound)==975 and len(b)==len(set(b))==1025 and len(sel)==len({e['questionId'] for e in sel})==2000
assert set(a).isdisjoint(b) and set(a)|set(b)=={e['questionId'] for e in sel} and {e['questionId'] for e in bound}==set(a)
assert all(sha(cat[e['questionId']])==e['cardCanonicalSha256'] for e in bound)
for topic in {e['topicId'] for e in sel}:
 old=rd_json=json.loads(git(C,'show',cp['baselineSHA']+':src/content/topics/'+topic+'.json'))
 frozen={q['id']:(i,q['difficulty'],q['correctIndex']) for i,q in enumerate(old['questions'],1)}
 for e in (e for e in sel if e['topicId']==topic):
  q=cat[e['questionId']];assert type(q['correctIndex']) is int
  assert frozen[q['id']]==(orders[q['id']],q['difficulty'],q['correctIndex']) and (e['difficulty'],e['correctIndex'])==(q['difficulty'],q['correctIndex'])
history=topics['history-russia']['questions'];base=json.loads(git(C,'show','144ff6582ad357ec81e3a7803c1278dcb7266732:src/content/topics/history-russia.json'))['questions']
assert [i for i,(l,r) in enumerate(zip(base,history),1) if l!=r]==list(range(63,71))
assert set(x['ownProgress']['accepted'])=={history[o-1]['id'] for o in range(63,71)} and x['ownProgress']['newlyCertified']==8
for o in range(63,71):
 c=rd(D/f'certification-history-russia{o}.json');assert c['newQualityCredit']==1 and len(c['accepted'])==1 and c['accepted'][0]['questionId']==history[o-1]['id'] and c['accepted'][0]['cardCanonicalSha256']==sha(history[o-1])
 assert x[f'pendingHistoryRussia{o}']['qualityCredit']==1
for o in [49,55,62]:assert history[o-1]==base[o-1] and x[f'pendingHistoryRussia{o}']['qualityCredit']==0 and not x[f'pendingHistoryRussia{o}']['applied']
assert x['ownHeldThisSlice']==[62]
freezes={'62':'3bdac82cca8210d6a8efc929c5edccc827f4f3c1','63':'0cf7f8d7330f353d489625f4a741cff4fa018181','64':'b047305b5bf2255fb4bacf39b70b581d6f8c187f','65':'4b6fa547cf77e84cc63f89b5f1edd7b776ac64f6','66':'a8a3f10ccae4af2ab7414bac70f532637aec4ffb','67':'d0d8f45f990ee7ad1b2eae7e1ebb77c96f603a6b','68':'09f11d0bac446b7bfc66a1c2cd4688d2480e5fd9','69':'372ff78caf2c1d1ecaa8867ed7d8e1cd9cc355a9','69-cycle1':'35ff3911b9bca2617746c0c016f87c8576d1c467','70':'4ba92d648787c2aa5ed5fe3cec8908f753b6f6dc'}
for label,freeze in freezes.items():
 for n in ['candidate.json','sourceproof.json','peer-snapshot.json']:
  p=D/('source-history-russia'+label)/n;assert p.read_bytes()==subprocess.check_output(['git','--no-optional-locks','-C',str(C),'show',freeze+':'+str(p.relative_to(C))])
e=rd(D/'source-history-russia69-cycle1/candidate.json')['entries'][0];v=json.loads(json.dumps(e['proposedCard']));v['answers'][2]['note']=e['beforeCard']['answers'][2]['note'];assert v==e['beforeCard'];assert rd(D/'history-russia69-cycle1-network-accounting.json')['actualWebCalls']==0 and rd(D/'history-russia69-network-accounting.json')['actualWebCalls']==2
reuse=rd(D/'verification-history-russia69-final-own-initial-reuse.json');assert len(reuse['checks'])==10 and all(v['allOriginalFieldsTextEqual'] for v in reuse['checks'])
for o in [69,70]:
 c=rd(D/f'certification-history-russia{o}.json');dev=c['sourceProvenanceDeviation'];assert dev['uncured'] and dev['contentPASSAndQAdoNotAssertProceduralCompliance'] and raw(dev['rawClarification'])==dev['rawSHA256']
c61=rd(D.parent/'coordinator-01a1605d/certification-history-russia61.json');assert c61['sourceProvenanceDeviation']['contentPASSAndQAdoNotAssertProceduralCompliance'] and not c61['sourceProvenanceDeviation']['failedBodyUsedAsProof']
assert [rd(D/f'history-russia{o}-network-accounting.json')['actualWebCalls'] for o in range(62,71)]==[3,2,3,4,0,0,0,2,7]
assert len(rd(D/'history-russia70-network-accounting.json')['preDispatchCompilationFailures'])==1
sl=x['coordinatorSlicesToPreserve'];assert len(sl)==37 and sl[-1]=={'intakeCURRENT':967,'newlyCertified':8} and cp['coordinatorSlicesToPreserve']==sl
assert all(r['intakeCURRENT']==l['intakeCURRENT']+l['newlyCertified'] for l,r in zip(sl,sl[1:])) and sl[-1]['intakeCURRENT']+sl[-1]['newlyCertified']==975
for root,key in [(C,'code'),(P,'planning')]:assert raw(git(root,'rev-parse','--path-format=absolute','--git-path','index'))==x['foreignIndexes'][key]
assert git(P,'branch','--show-current')=='main' and git(P,'rev-parse','HEAD')=='01e3cb6f1195ac1b3b5b16be458a3428ee89e6bd'
records=[rd(p) for p in (P/'openspec/changes').glob('*/delivery.json')]+[rd(p) for p in (P/'openspec/changes/archive').glob('*/delivery.json')]
assert {r['id'] for r in records if r.get('owner')==O}==set(x['claims']) and cp['owner']==cp['activeCoordinator']==O and rd(P/'.flow-leases.json')=={}
for p in [pathlib.Path(x['canonicalCheckpoint']),P/'evidence/question-revision-process-v2/coordinator-state.json',P/'evidence/question-revision-process-v2/active-full2000-goal-01a1593a.json']:
 d=rd(p);assert d['owner']==O and d['phase']==x['phase']
assert not cp['currentSourceActors'] and not cp['currentIndependentActors'] and not x['sourceActorKeys'] and x['pendingFinal69Reviewer'] is None

def native(actor):
 uid=actor['threadId'];fs=list(pathlib.Path('/Users/eaafonasev/.codex/sessions').rglob('*'+uid+'.jsonl'))+list(pathlib.Path('/Users/eaafonasev/.codex/archived_sessions').rglob('*'+uid+'.jsonl'));assert len(fs)==1
 r=[json.loads(l) for l in fs[0].open()];assert r[0]['payload']['id']==uid;count=sum(v['type']=='compacted' for v in r);event=next(v['payload']['type'] for v in reversed(r) if v.get('payload',{}).get('type') in ['task_started','task_complete']);info=next(v['payload']['info'] for v in reversed(r) if v.get('payload',{}).get('type')=='token_count');return fs[0],count,event,info
ac={}
for o in range(62,71):
 actor=x['actors']['author'+str(o)];p,count,event,info=native(actor);assert actor['archived'] and count==actor['actualCompactions'] and count<2 and event=='task_complete';ac[str(o)]=count
reader=x['actors']['reviewer'];p,count,event,info=native(reader);assert not reader.get('archived',False) and count==0 and event=='task_complete' and info['last_token_usage']['input_tokens']==385521 and info['model_context_window']==475000;assert cp['nativeActorsCurrent']==[reader] and x['retainedIdleReviewer']==reader
root=[json.loads(l) for l in pathlib.Path(x['rootNativeAudit']['nativeJournal']).open()];assert root[0]['payload']['id']==O;rc=sum(v['type']=='compacted' for v in root);ri=next(v['payload']['info'] for v in reversed(root) if v.get('payload',{}).get('type')=='token_count');assert rc==0
assert len(x['ownAffectedRuns'])==8
for p in x['ownAffectedRuns']:
 q=rd(p);assert q['success'] and q['numPassedTests']==19 and q['numFailedTests']==q['numPendingTests']==q.get('numTodoTests',0)==0
assert git(C,'diff','--name-only','4991a8e7fc4c73e24bbb4577a64d4701e9b9bdd2','HEAD','--','src/content/topics')==''
q=x['nextUntouched'];assert q['sourceOrder']==71 and q['hash']==sha(history[70]) and not (D/'source-history-russia71-task.json').exists()
cleanup=rd(D/'owned-temporary-generators-cleanup.json');assert cleanup['removed'] and all(not pathlib.Path(p).exists() for p in cleanup['removedPaths'])
for v in cleanup['copies']:assert raw(v['permanentCopy'])==v['sha256']
remote=[r['evidence']['remote_push'] for r in records if r['id'] in x['claims']];assert len(remote)==3 and all(r==remote[0] for r in remote);remote=remote[0];assert remote['CURRENT']==975 and remote['remaining']==1025 and remote['readbackVerified'] and git(C,'ls-remote','origin','refs/heads/'+x['codeBranch']).split()[0]==remote['commit']
main=git(C,'ls-remote','origin','refs/heads/main').split()[0];mc={}
for topic in {e['topicId'] for e in sel}:mc.update({q['id']:q for q in json.loads(git(C,'show',main+':src/content/topics/'+topic+'.json'))['questions']})
presence={e['questionId']:sha(mc[e['questionId']])==e['cardCanonicalSha256'] for e in bound}
tracked=git(C,'ls-tree','-r','--name-only','HEAD','--',str(D.relative_to(C))).splitlines();disk=[p for p in D.rglob('*') if p.is_file()];assert set(tracked)=={str(p.relative_to(C)) for p in disk};assert all(subprocess.check_output(['git','--no-optional-locks','-C',str(C),'show','HEAD:'+p])==(C/p).read_bytes() for p in tracked)
tp=C/'src/content/topics/history-russia.json';assert tp.read_bytes()==subprocess.check_output(['git','--no-optional-locks','-C',str(C),'show','HEAD:src/content/topics/history-russia.json']);subprocess.check_output(['git','--no-optional-locks','-C',str(C),'diff','--check','144ff6582ad357ec81e3a7803c1278dcb7266732','HEAD'])
print(json.dumps({'CURRENT':975,'remaining':1025,'fullGoal':2000,'all975CurrentHashes':True,'exact975and1025Partition':True,'all2000FrozenOrderDifficultyNumericKey':True,'ownIntakeCURRENT':967,'ownNewlyCertified':8,'ownCatalogDeltaOnly63to70':True,'ownHOLD62UnqualifiedUnapplied':True,'coordinatorSlicesCount':37,'affectedContentRuns':8,'each':'19PASS/0FAIL/0pending','typecheck':'NotRun JSON-only','runtime':'NotRun prohibited','foreignIndexesPreserved':x['foreignIndexes'],'claimsExact3Owner':O,'leaseHeld':False,'ownTrackedPermanentDiskToHEADBeforeVerificationMetadata':len(tracked),'ownDrift':[],'ownExtras':[],'authorArchiveConfirmed':9,'allAuthorsActualCompactions':ac,'noActiveSourceOrReviewTask':True,'retainedIdleReviewer':reader,'reviewerRemaining':89479,'retainedReaderConditionalWholeNextAndPossibleFixPreflightRequired':True,'rootActualCompactions':rc,'rootLastInputAtVerification':ri['last_token_usage']['input_tokens'],'rootWindow':ri['model_context_window'],'mainRemoteSHA':main,'mainCurrentEligibleExactHashMatches':sum(presence.values()),'mainCurrentEligibleExactHashMissing':975-sum(presence.values()),'ownAcceptedOnMain':{i:presence[i] for i in x['ownProgress']['accepted']},'mainIntegrated':False,'remotePushAuthority':remote,'nextUntouched':q,'source69SoleCycle1OnlyNote2SameReaderFINALPASS':True,'source69OwnInitialExactReuseChecks':10,'source61UncuredDuplicateNotCured':True,'source69And70OutsideOutputWritesUncured':True,'ownedTemporaryGeneratorsPreservedThenRemoved':True,'noVerificationOrQAReplay':True},ensure_ascii=False))
