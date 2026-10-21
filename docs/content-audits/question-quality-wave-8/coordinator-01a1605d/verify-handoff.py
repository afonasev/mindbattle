"""Read-only CURRENT967/own56-61 snapshot; not a successor takeover route."""
import pathlib,json,hashlib,subprocess,importlib.util
D=pathlib.Path(__file__).parent
s=importlib.util.spec_from_file_location('m',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
x=m.read(D/'manifest.json');cp=m.read(pathlib.Path(x['canonicalCheckpoint']))
assert x['owner']==m.O and x['CURRENT']==967 and x['remaining']==1033 and x['ownIntakeCURRENT']==961 and x['newlyCertified']==6
cat={};orders={};total=0
for p in sorted((m.C/'src/content/topics').glob('*.json')):
 for i,q in enumerate(m.read(p)['questions'],1):cat[q['id']]=q;orders[q['id']]=i;total+=1
assert total==len(cat)==11000
a=cp['currentEligibleCompletedIds'];b=cp['currentRemainingIds'];sel=cp['selectedCards'];bound=cp['completedCardHashes']
assert len(a)==len(set(a))==len(bound)==967 and len(b)==len(set(b))==1033
assert len(sel)==len({e['questionId'] for e in sel})==2000 and set(a).isdisjoint(b) and set(a)|set(b)=={e['questionId'] for e in sel}
assert {e['questionId'] for e in bound}==set(a) and all(m.sha(cat[e['questionId']])==e['cardCanonicalSha256'] for e in bound)
for t in {e['topicId'] for e in sel}:
 old=json.loads(m.h.git(m.C,'show',cp['baselineSHA']+':src/content/topics/'+t+'.json'))
 frozen={q['id']:(i,q['difficulty'],q['correctIndex']) for i,q in enumerate(old['questions'],1)}
 for e in (v for v in sel if v['topicId']==t):
  q=cat[e['questionId']];assert frozen[q['id']]==(orders[q['id']],q['difficulty'],q['correctIndex'])
  assert (e['difficulty'],e['correctIndex'])==(q['difficulty'],q['correctIndex'])
history=m.read(m.C/'src/content/topics/history-russia.json')['questions']
old=json.loads(m.h.git(m.C,'show','65b64849e139ec657380a7496dcc711f34405a2a:src/content/topics/history-russia.json'))['questions']
assert [i for i,(l,r) in enumerate(zip(old,history),1) if l!=r]==list(range(56,62))
assert set(x['ownProgress']['accepted'])=={history[o-1]['id'] for o in range(56,62)} and x['ownProgress']['newlyCertified']==6
for o in range(56,62):
 c=m.read(D/f'certification-history-russia{o}.json');assert c['newQualityCredit']==1 and len(c['accepted'])==1
 assert c['accepted'][0]['questionId']==history[o-1]['id'] and c['accepted'][0]['cardCanonicalSha256']==m.sha(history[o-1])
 assert x[f'pendingHistoryRussia{o}']['qualityCredit']==1
assert x['ownHeldThisSlice']==[] and x['inheritedHeldSliceFromPredecessor']==[49,55]
for o in [49,55]:assert history[o-1]==old[o-1] and x[f'pendingHistoryRussia{o}']['qualityCredit']==0 and not x[f'pendingHistoryRussia{o}']['applied']
freezes={'56':'c55029319e62a815f223b994d81f463e84d74b05','57':'45a5f993c18cbd52e06d30db90f1fc2e1f6a5902','57-cycle1':'8411082bd54f7c63f52b6c3becd18a90097d9223','58':'9265f1c815f88bdb9df782694d12e1996c82ec86','58-cycle1':'95767f69d427abe85f1ae2b46c225c0672f07852','59':'a9b09b87a39300e604404fb4b4bf5d4cbdcf2635','60':'a1c7b4dfada83e4f23a01814778d522a172ce481','61':'251adae9912816320ba62b7a19b9ddd1db154bf4'}
for name,freeze in freezes.items():
 for name2 in ['candidate.json','sourceproof.json','peer-snapshot.json']:
  p=D/('source-history-russia'+name)/name2
  assert p.read_bytes()==subprocess.check_output(['git','--no-optional-locks','-C',str(m.C),'show',freeze+':'+str(p.relative_to(m.C))])
for o,k in [(57,1),(58,3)]:
 c=m.read(D/f'source-history-russia{o}-cycle1/candidate.json')['entries'][0];v=json.loads(json.dumps(c['proposedCard']));v['answers'][k]['note']=c['beforeCard']['answers'][k]['note'];assert v==c['beforeCard']
 assert m.read(D/f'history-russia{o}-cycle1-network-accounting.json')['actualWebCalls']==0
 reuse=m.read(D/f'verification-history-russia{o}-final-own-initial-reuse.json');assert len(reuse['checks'])==10 and all(z['allOriginalFieldsTextEqual'] for z in reuse['checks'])
assert [m.read(D/f'history-russia{o}-network-accounting.json')['actualWebCalls'] for o in range(56,62)]==[5,2,5,5,2,1]
assert m.read(D/'history-russia61-network-accounting.json')['includePriorTasks']
dev=m.read(D/'source61-duplicate-primary-clarification.json');assert dev['notZeroButOneForbiddenCrossSessionRepeat'] and dev['priorExactNativeEquality'] and dev['chronology']['originalOfficialSource60Captured']<dev['chronology']['source61DuplicateFailed']
c61=m.read(D/'certification-history-russia61.json');assert c61['sourceProvenanceDeviation']['contentPASSAndQAdoNotAssertProceduralCompliance'] and not c61['sourceProvenanceDeviation']['failedBodyUsedAsProof']
assert m.raw(D/'source61-duplicate-primary-clarification.json')==c61['sourceProvenanceDeviation']['rawSHA256']
sl=x['coordinatorSlicesToPreserve'];assert len(sl)==36 and sl[-1]=={'intakeCURRENT':961,'newlyCertified':6} and cp['coordinatorSlicesToPreserve']==sl
assert all(r['intakeCURRENT']==l['intakeCURRENT']+l['newlyCertified'] for l,r in zip(sl,sl[1:])) and sl[-1]['intakeCURRENT']+sl[-1]['newlyCertified']==967
assert {d['id'] for p,d in m.flow.records().values() if d['owner']==m.O}==set(x['claims']) and cp['owner']==cp['activeCoordinator']==m.O and m.read(m.P/'.flow-leases.json')=={}
assert not cp['currentSourceActors'] and not cp['currentIndependentActors'] and not x['sourceActorKeys'] and x['pendingFinal58Reviewer'] is None and x['retainedNativeReviewers']==[]
def native(actor):
 uid=actor['threadId'];ps=list(pathlib.Path('/Users/eaafonasev/.codex/sessions').rglob('*'+uid+'.jsonl'))+list(pathlib.Path('/Users/eaafonasev/.codex/archived_sessions').rglob('*'+uid+'.jsonl'));assert len(ps)==1
 rows=[json.loads(l) for l in ps[0].open()];assert rows[0]['payload']['id']==uid
 count=sum(r['type']=='compacted' for r in rows);event=next(r['payload']['type'] for r in reversed(rows) if r.get('payload',{}).get('type') in ['task_started','task_complete'])
 info=next(r['payload']['info'] for r in reversed(rows) if r.get('payload',{}).get('type')=='token_count')
 return count,event,info
authorCounts={}
for o in range(56,62):
 actor=x['actors']['author'+str(o)];assert actor['archived'];count,event,info=native(actor);assert count==actor['actualCompactions'] and count<2 and event=='task_complete';authorCounts[str(o)]=count
reader=x['actors']['reviewer'];count,event,info=native(reader);assert count==0 and event=='task_complete' and info['last_token_usage']['input_tokens']==reader['lastInput']==169447 and info['model_context_window']==475000 and not reader.get('archived',False)
assert cp['nativeActorsCurrent']==[reader] and x['retainedIdleReviewer']==reader
retired=x['retiredReviewerCurrentOwnerAfter58'];count,event,ri=native(retired);assert retired['archived'] and count==0 and event=='task_complete' and ri['last_token_usage']['input_tokens']==431783
root=[json.loads(l) for l in pathlib.Path(x['rootNativeAudit']['nativeJournal']).open()];assert root[0]['payload']['id']==m.O;rootCount=sum(r['type']=='compacted' for r in root);rootInfo=next(r['payload']['info'] for r in reversed(root) if r.get('payload',{}).get('type')=='token_count');assert rootCount==0
for r,k in [(m.C,'code'),(m.P,'planning')]:assert m.raw(pathlib.Path(m.h.git(r,'rev-parse','--path-format=absolute','--git-path','index')))==x['foreignIndexes'][k]
assert m.h.git(m.P,'rev-parse','HEAD')=='01e3cb6f1195ac1b3b5b16be458a3428ee89e6bd' and m.h.git(m.P,'branch','--show-current')=='main'
assert len(x['ownAffectedRuns'])==5
for p in x['ownAffectedRuns']:
 qa=m.read(p);assert qa['success'] and qa['numPassedTests']==19 and qa['numFailedTests']==qa['numPendingTests']==qa.get('numTodoTests',0)==0
q=x['nextUntouched'];assert q['sourceOrder']==62 and q['hash']==m.sha(history[61]) and not (D/'source-history-russia62-task.json').exists() and not (D/'source-history-russia62').exists()
remote=m.flow.get(x['claims'][0])[1]['evidence']['remote_push'];assert remote['CURRENT']==967 and remote['remaining']==1033 and remote['readbackVerified'] and all(m.flow.get(cid)[1]['evidence']['remote_push']==remote for cid in x['claims'])
assert m.h.git(m.C,'ls-remote','origin','refs/heads/'+x['codeBranch']).split()[0]==remote['commit']
main=m.h.git(m.C,'ls-remote','origin','refs/heads/main').split()[0];mc={}
for t in {e['topicId'] for e in sel}:mc.update({q['id']:q for q in json.loads(m.h.git(m.C,'show',main+':src/content/topics/'+t+'.json'))['questions']})
presence={e['questionId']:m.sha(mc[e['questionId']])==e['cardCanonicalSha256'] for e in bound};assert sum(presence.values())==0
tracked=m.h.git(m.C,'ls-tree','-r','--name-only','HEAD','--',str(D.relative_to(m.C))).splitlines();disk=[p for p in D.rglob('*') if p.is_file()]
assert set(tracked)=={str(p.relative_to(m.C)) for p in disk}
assert all(subprocess.check_output(['git','--no-optional-locks','-C',str(m.C),'show','HEAD:'+p])==(m.C/p).read_bytes() for p in tracked)
tp=m.C/'src/content/topics/history-russia.json';assert tp.read_bytes()==subprocess.check_output(['git','--no-optional-locks','-C',str(m.C),'show','HEAD:src/content/topics/history-russia.json'])
subprocess.check_output(['git','--no-optional-locks','-C',str(m.C),'diff','--check','65b64849e139ec657380a7496dcc711f34405a2a','HEAD'])
print(json.dumps({'CURRENT':967,'remaining':1033,'fullGoal':2000,'all967CurrentHashes':True,'exact967and1033Partition':True,'all2000FrozenOrderDifficultyNumericKey':True,'ownIntakeCURRENT':961,'ownNewlyCertified':6,'ownCatalogDeltaOnly56to61':True,'coordinatorSlicesCount':36,'ownSOURCEStatuses':{str(o):x[f'pendingHistoryRussia{o}']['status'] for o in range(56,62)},'affectedContentRuns':5,'each':'19PASS/0FAIL/0pending','typecheck':'NotRun JSON-only','runtime':'NotRun prohibited','foreignIndexesPreserved':x['foreignIndexes'],'claimsExact3Owner':m.O,'leaseHeld':False,'ownTrackedPermanentDiskToHEADBeforeVerificationMetadata':len(tracked),'ownDrift':[],'ownExtras':[],'authorArchiveConfirmed':6,'allAuthorsActualCompactions':authorCounts,'noActiveSourceOrReviewTask':True,'retainedIdleReviewer':reader,'reviewerRemaining':305553,'oldOwnReader11ArchivedAfterFinal58':True,'rootActualCompactions':rootCount,'rootLastInputAtVerification':rootInfo['last_token_usage']['input_tokens'],'rootWindow':rootInfo['model_context_window'],'mainRemoteSHA':main,'mainCurrentEligibleExactHashMatches':sum(presence.values()),'mainCurrentEligibleExactHashMissing':len(presence)-sum(presence.values()),'ownAcceptedOnMain':{i:presence[i] for i in x['ownProgress']['accepted']},'mainIntegrated':False,'remotePushAuthority':remote,'nextUntouched':q,'source57and58SoleCycleOnlyOneNoteSameReaderFINALPASS':True,'source61UncuredDuplicateRequestExcludedFromPrimaryProof':True,'source59LimitedPravencWindowAndRestoredNotesPreserved':True,'noNewHumanGoForRemaining':True},ensure_ascii=False))
