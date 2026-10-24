"""Pure read-only pre-ACTIVATE barrier; no active helper imports or index access through Git status."""
import json,pathlib,hashlib,subprocess
D=pathlib.Path(__file__).parent;C=D.parents[3];P=pathlib.Path('/Users/eaafonasev/Projects/mindbattle/planning');O='01a16d13-f6ee-71f1-879b-5737c83b4e1a'
def read(p):return json.loads(pathlib.Path(p).read_text())
def raw(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def sha(v):return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def git(*args):return subprocess.check_output(['git','-C',str(C),*args],text=True).strip()
x=read(D/'handoff-next.json');assert x['CURRENT']==1081 and x['remaining']==919 and x['rootNativeAudit']['threadId']==O
assert x['successorStatus']=='READONLY_BOOTSTRAP_REGISTERED' and x['successorThreadId'];cp=read(x['canonicalCheckpoint']);st=read(P/'evidence/question-revision-process-v2/coordinator-state.json');goal=read(P/'evidence/question-revision-process-v2/active-full2000-goal-01a1593a.json')
assert cp['owner']==cp['activeCoordinator']==st['owner']==goal['owner']==O and read(P/'.flow-leases.json')=={}
assert all(v['pendingSuccessor']==v['successorThreadId']==x['successorThreadId'] for v in [cp,st,goal]);assert all(w['owner']==O for w in cp['waves'] if w['changeId'] in x['claims'] and 'owner' in w)
claims=[read(P/'openspec/changes'/cid/'delivery.json') for cid in x['claims']];assert len(claims)==4 and all(v['owner']==O for v in claims)
selected={v['questionId']:v for v in cp['selectedCards']};done=set(cp['currentEligibleCompletedIds']);remaining=set(cp['currentRemainingIds']);assert len(selected)==2000 and len(done)==1081 and len(remaining)==919 and not done&remaining and done|remaining==set(selected)
current={};base={};frozen=0
for tid in {v['topicId'] for v in selected.values()}:
 rel='src/content/topics/'+tid+'.json';a=read(C/rel);b=json.loads(git('show',cp['baselineSHA']+':'+rel));assert a['id']==b['id']==tid and [v['id'] for v in a['questions']]==[v['id'] for v in b['questions']]
 for q,z in zip(a['questions'],b['questions']):
  current[q['id']]=q;base[z['id']]=z
  if q['id'] in selected:
   f=selected[q['id']];assert f['topicId']==tid and f['difficulty']==q['difficulty']==z['difficulty'] and f['correctIndex']==q['correctIndex']==z['correctIndex'] and type(q['correctIndex']) is int and sha(z)==f['baselineCanonicalSha256'];frozen+=1
assert frozen==2000 and len(cp['completedCardHashes'])==1081 and {v['questionId'] for v in cp['completedCardHashes']}==done
assert all(sha(current[v['questionId']])==v['cardCanonicalSha256'] for v in cp['completedCardHashes'])
reg=read(x['activeRoute']['sourceCheckpoint']);assert reg['ownerNativeId']==O and reg['sourceEditorialCompletedCards']==len(reg['cards'])==87 and reg['sourceEditorialCompletedFields']==522 and reg['latestBatch']['CURRENT']==1081
accepted={v['questionId']:v['cardCanonicalSha256'] for v in cp['completedCardHashes']};assert len({v['questionId'] for v in reg['cards']})==87 and all(accepted[v['questionId']]==v['cardCanonicalSha256'] for v in reg['cards'])
head=git('rev-parse','HEAD');count=0
for p in D.rglob('*'):
 assert not p.is_symlink()
 if p.is_file():
  assert subprocess.check_output(['git','-C',str(C),'show',head+':'+str(p.relative_to(C))])==p.read_bytes(),str(p);count+=1
assert count==len(git('ls-tree','-r','--name-only',head,'--',str(D.relative_to(C))).splitlines())
push=[v['evidence']['remote_push'] for v in claims];assert all(v==push[0] for v in push) and push[0]['CURRENT']==1081 and push[0]['remaining']==919 and push[0]['commit']==head
refs={l.split()[1]:l.split()[0] for l in git('ls-remote','origin','refs/heads/'+x['codeBranch'],'refs/heads/main').splitlines()};assert refs['refs/heads/'+x['codeBranch']]==head
for root,k in [(C,'code'),(P,'planning')]:
 path=subprocess.check_output(['git','-C',str(root),'rev-parse','--path-format=absolute','--git-path','index'],text=True).strip();assert raw(path)==x['foreignIndexes'][k]
assert len(x['newAttemptFences'])==134 and read(D/'own-consumed-source-fences.json')['totalFences']==134
assert all(a.get('archived') for k,a in x['actors'].items() if k.startswith('author')) and not x['pendingReviews'] and not x['pendingBoundedWork'] and not x['readyQueue'] and not x.get('pendingBootstrapActors')
r=read(D/'retained-reader-handoff.json');a=x['actors']['reviewer'];assert r['readerOwnReceiptCount']==len(r['readerOwnReceipts'])==5 and a['threadId']=='01a16d2b-da45-79f0-8979-dd4a2a9e4a06'
for p,v in r['readerOwnReceipts'].items():assert raw(p)==v['rawSHA256']
rows=[json.loads(l) for l in pathlib.Path(a['nativeJournal']).open()];assert [v['payload']['id'] for v in rows if v.get('type')=='session_meta']==[a['threadId']] and sum(v.get('type')=='compacted' for v in rows)==0
assert next(v['payload']['type'] for v in reversed(rows) if v.get('payload',{}).get('type') in ['task_started','task_complete'])=='task_complete'
info=next(v['payload']['info'] for v in reversed(rows) if v.get('payload',{}).get('type')=='token_count');assert info['last_token_usage']['input_tokens']==245826 and info['model_context_window']==475000
qa=x['ownAffectedRuns'];assert len(qa)==5 and qa[-1]['testedCatalogCommit']=='b27c8d23b86a885ec55d57eae200ea8415805754'
for p in (C/'src/content/topics').glob('*.json'):assert subprocess.check_output(['git','-C',str(C),'show',qa[-1]['testedCatalogCommit']+':'+str(p.relative_to(C))])==p.read_bytes()
n=x['nextUntouched'];assert n['sourceOrder']==23 and n['id']=='video-game-history-brown-box-licensee' and n['id'] in remaining and current[n['id']]==base[n['id']] and sha(current[n['id']])==n['hash'] and n['correctIndex']==3 and n['difficulty']=='hard'
print(json.dumps({'READONLY_BARRIER':'PASS','CURRENT':1081,'remaining':919,'owners':O,'exactClaims':4,'leaseEmpty':True,'all2000Frozen':True,'allAcceptedHashesExact':True,'canonicalCards':87,'canonicalFields':522,'ownedFilesExactCurrentHEAD':count,'HEAD':head,'freshOriginFeature':refs['refs/heads/'+x['codeBranch']],'allFourRemotePushIdentical':True,'foreignIndexesExact':True,'lastActualQA':qa[-1]['testedCatalogCommit'],'all110TopicFilesSameAsLastQA':True,'retainedReader':a['threadId'],'readerOwnReceipts':5,'readerActualCompactions':0,'readerRemaining':229174,'fences':134,'nextUntouched':n,'successorRegistered':x['successorThreadId'],'allDiagnosticsUncured':True,'noWritesOrQARerun':True},ensure_ascii=False))
