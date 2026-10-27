"""Pure read-only registered-successor barrier. No active helpers, writes or QA."""
import json, pathlib, hashlib, subprocess
D=pathlib.Path(__file__).parent
C=D.parents[3]
P=pathlib.Path('/Users/eaafonasev/Projects/mindbattle/planning')
O='01a17b9e-f725-7421-a651-61846e5475fa'
def read(p):return json.loads(pathlib.Path(p).read_text())
def raw(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def sha(v):return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def git(*args):return subprocess.check_output(['git','-C',str(C),*args],text=True).strip()
x=read(D/'handoff-next.json');v=read(D/'handoff-verification.json')
G=v['retainedReaderNativeId'];expected_reader_count=v['retainedReaderOwnReceiptCount']
n=v['CURRENT'];left=2000-n
assert x['CURRENT']==n and x['remaining']==left and x['fullGoal']==2000
assert v['allCurrentAcceptedHashesExact'] and v['all2000FrozenIdTopicOrderDifficultyNumericKey']
assert x['rootNativeAudit']['threadId']==O
assert x['successorStatus']=='READONLY_BOOTSTRAP_REGISTERED' and x['successorThreadId']
cp=read(x['canonicalCheckpoint']);st=read(P/'evidence/question-revision-process-v2/coordinator-state.json')
goal=read(P/'evidence/question-revision-process-v2/active-full2000-goal-01a1593a.json')
assert cp['owner']==cp['activeCoordinator']==st['owner']==goal['owner']==O
assert read(P/'.flow-leases.json')=={}
assert all(a['pendingSuccessor']==a['successorThreadId']==x['successorThreadId'] for a in [cp,st,goal])
assert all(w['owner']==O for w in cp['waves'] if w['changeId'] in x['claims'] and 'owner' in w)
claims=[read(P/'openspec/changes'/cid/'delivery.json') for cid in x['claims']]
assert len(claims)==4 and all(a['owner']==O for a in claims)
selected={a['questionId']:a for a in cp['selectedCards']}
done=set(cp['currentEligibleCompletedIds']);remaining=set(cp['currentRemainingIds'])
assert len(selected)==len(cp['selectedCards'])==2000 and len(done)==n and len(remaining)==left
assert not done&remaining and done|remaining==set(selected)
current={};base={};frozen=0
for tid in {a['topicId'] for a in selected.values()}:
 rel='src/content/topics/'+tid+'.json';a=read(C/rel);b=json.loads(git('show',cp['baselineSHA']+':'+rel))
 assert a['id']==b['id']==tid and [q['id'] for q in a['questions']]==[q['id'] for q in b['questions']]
 for q,z in zip(a['questions'],b['questions']):
  current[q['id']]=q;base[z['id']]=z
  if q['id'] in selected:
   f=selected[q['id']]
   assert f['topicId']==tid and f['difficulty']==q['difficulty']==z['difficulty']
   assert f['correctIndex']==q['correctIndex']==z['correctIndex'] and type(q['correctIndex']) is int
   assert sha(z)==f['baselineCanonicalSha256'];frozen+=1
assert frozen==2000 and len(cp['completedCardHashes'])==n
assert {a['questionId'] for a in cp['completedCardHashes']}==done
assert all(sha(current[a['questionId']])==a['cardCanonicalSha256'] for a in cp['completedCardHashes'])
reg_path=pathlib.Path(x['activeRoute']['sourceCheckpoint']);reg=read(reg_path)
assert subprocess.check_output(['git','-C',str(C),'show','HEAD:'+str(reg_path.relative_to(C))])==reg_path.read_bytes()
assert isinstance(reg['ownerNativeId'],str) and reg['ownerNativeId']
assert reg['sourceEditorialCompletedCards']==len(reg['cards'])
assert reg['sourceEditorialCompletedFields']==6*len(reg['cards']) and reg['latestBatch']['CURRENT']==n
accepted={a['questionId']:a['cardCanonicalSha256'] for a in cp['completedCardHashes']}
assert len({a['questionId'] for a in reg['cards']})==len(reg['cards'])
assert all(accepted[a['questionId']]==a['cardCanonicalSha256'] for a in reg['cards'])
head=git('rev-parse','HEAD');count=0
for p in D.rglob('*'):
 assert not p.is_symlink()
 if p.is_file():
  assert subprocess.check_output(['git','-C',str(C),'show',head+':'+str(p.relative_to(C))])==p.read_bytes(),str(p)
  count+=1
assert count==len(git('ls-tree','-r','--name-only',head,'--',str(D.relative_to(C))).splitlines())
push=[a['evidence']['remote_push'] for a in claims]
assert all(a==push[0] for a in push) and push[0]['CURRENT']==n and push[0]['remaining']==left
assert push[0]['commit']==head
refs={line.split()[1]:line.split()[0] for line in git('ls-remote','origin','refs/heads/'+x['codeBranch'],'refs/heads/main').splitlines()}
assert refs['refs/heads/'+x['codeBranch']]==head
for root,key in [(C,'code'),(P,'planning')]:
 index=subprocess.check_output(['git','-C',str(root),'rev-parse','--path-format=absolute','--git-path','index'],text=True).strip()
 assert raw(index)==x['foreignIndexes'][key]
fences=read(D/'own-consumed-source-fences.json')
assert fences['totalFences']==len(x['newAttemptFences'])==fences['inheritedFenceCount']+len(fences['ownClosedRecords'])
assert v['inheritedFencesByteExact'] and v['totalFences']==fences['totalFences']
inherited_handoff=read(x['predecessorHandoff'])
assert fences['inheritedPointer']==inherited_handoff['ownConsumedSourceFences']
assert x['newAttemptFences']==inherited_handoff['newAttemptFences']+fences['ownClosedRecords']
inherited_fences=pathlib.Path(fences['inheritedPointer'])
assert raw(inherited_fences)==fences['inheritedRawSHA256']
assert subprocess.check_output(['git','-C',str(C),'show',read(D/'takeover.json')['predecessorRemotePush']['commit']+':'+str(inherited_fences.relative_to(C))])==inherited_fences.read_bytes()
assert all(a.get('archived') for key,a in x['actors'].items() if key.startswith('author'))
assert not x['pendingReviews'] and not x['pendingBoundedWork'] and not x['readyQueue'] and not x.get('pendingBootstrapActors')
r=read(D/'retained-reader-handoff.json');a=x['actors']['reviewer']
assert a['threadId']==r['retainedIdleReader']['threadId']==G
assert r['readerOwnReceiptCount']==len(r['readerOwnReceipts'])==a['ownReceiptCount']==expected_reader_count
identity=read(x['currentReaderNativeIdentity']);assert identity['verifiedSessionMetaId']==identity['decodedResult']['threadId']==G and identity['nativeJournal']==a['nativeJournal']
seed=read(r['inheritedImmutable']);assert seed['retainedIdleReader']['threadId']==G and seed['readerOwnReceiptCount']==len(seed['readerOwnReceipts'])
retired=read(r['retiredReader32Own13']);assert retired['readerOwnReceiptCount']==len(retired['readerOwnReceipts'])==13 and retired['retainedIdleReader']['threadId']!=G
for path,binding in r['readerOwnReceipts'].items():
 assert raw(path)==binding['rawSHA256']
 receipt=read(path);entry=receipt['entries'][0]
 assert receipt.get('reviewerNativeId',receipt.get('readerNativeId'))==G
 assert entry['stage']==binding['stage'] and entry['status']==binding['status'] and entry['sourceOrder']==binding['sourceOrder']
 assert entry['currentCardCanonicalSHA256']==binding['currentCardCanonicalSHA256']
inherited=read(r['inheritedImmutable'])
assert all(path in r['readerOwnReceipts'] and r['readerOwnReceipts'][path]['rawSHA256']==binding['rawSHA256'] for path,binding in inherited['readerOwnReceipts'].items())
for path in D.glob('independent-*/receipt.json'):
 receipt=read(path)
 if receipt.get('reviewerNativeId',receipt.get('readerNativeId'))==G:assert str(path) in r['readerOwnReceipts']
rows=[json.loads(line) for line in pathlib.Path(a['nativeJournal']).open()]
assert [row['payload']['id'] for row in rows if row.get('type')=='session_meta']==[G]
assert sum(row.get('type')=='compacted' for row in rows)==a['actualCompactions']==0
assert next(row['payload']['type'] for row in reversed(rows) if row.get('payload',{}).get('type') in ['task_started','task_complete'])=='task_complete'
info=next(row['payload']['info'] for row in reversed(rows) if row.get('payload',{}).get('type')=='token_count')
assert info['last_token_usage']['input_tokens']==a['lastInput'] and info['model_context_window']==a['modelWindow']
qa=x['ownAffectedRuns'];assert qa and len(qa)==len(v['ownQAReports'])
for run in qa:
 report=read(run['path']);assert raw(run['path'])==run['rawSHA256']
 assert report['success'] and report['numPassedTests']==19 and report['numFailedTests']==report['numPendingTests']==0
files=list((C/'src/content/topics').glob('*.json'));assert len(files)==110
for path in files:
 assert subprocess.check_output(['git','-C',str(C),'show',qa[-1]['testedCatalogCommit']+':'+str(path.relative_to(C))])==path.read_bytes()
next_card=x['nextUntouched'];order=next_card['sourceOrder'];topic=next_card['topicId']
assert order==max(x['ownedSourceOrders'])+1 and topic==x['activeRoute']['topicId']
assert read(C/f'src/content/topics/{topic}.json')['questions'][order-1]['id']==next_card['id']
assert next_card['id'] in remaining and current[next_card['id']]==base[next_card['id']]
assert sha(current[next_card['id']])==next_card['hash']
assert current[next_card['id']]['correctIndex']==next_card['correctIndex'] and current[next_card['id']]['difficulty']==next_card['difficulty']
print(json.dumps({'READONLY_BARRIER':'PASS','CURRENT':n,'remaining':left,'owners':O,'exactClaims':4,'leaseEmpty':True,'all2000Frozen':True,'allAcceptedHashesExact':True,'canonicalHistoricalWriter':reg['ownerNativeId'],'canonicalCards':len(reg['cards']),'canonicalFields':reg['sourceEditorialCompletedFields'],'ownedFilesExactCurrentHEAD':count,'HEAD':head,'freshOriginFeature':refs['refs/heads/'+x['codeBranch']],'allFourRemotePushIdentical':True,'foreignIndexesExact':True,'actualQAReports':len(qa),'lastActualQA':qa[-1]['testedCatalogCommit'],'all110TopicFilesSameAsLastQA':True,'retainedReader':G,'readerOwnReceipts':r['readerOwnReceiptCount'],'readerActualCompactions':0,'readerRemaining':info['model_context_window']-info['last_token_usage']['input_tokens'],'fences':fences['totalFences'],'nextUntouched':next_card,'successorRegistered':x['successorThreadId'],'allDiagnosticsUncured':True,'noWritesOrQARerun':True},ensure_ascii=False))
