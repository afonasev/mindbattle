"""Read-only exact checkpoint/immutable packet/QA/index/native verification; save own evidence only."""
import pathlib, json, importlib.util, subprocess, hashlib, datetime
D=pathlib.Path(__file__).parent
s=importlib.util.spec_from_file_location('m',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
x=m.read(D/'manifest.json');cp=m.read(pathlib.Path(x['canonicalCheckpoint']))
n=len(cp['currentEligibleCompletedIds']);assert n==x['CURRENT'] and n+x['remaining']==2000
selected={e['questionId']:e for e in cp['selectedCards']};done=set(cp['currentEligibleCompletedIds']);remaining=set(cp['currentRemainingIds'])
assert len(selected)==2000 and len(done)==n and len(remaining)==2000-n and not done&remaining and done|remaining==set(selected)
assert len(cp['completedCardHashes'])==n and {e['questionId'] for e in cp['completedCardHashes']}==done
catalog={};topics={};baseline={}
for tid in sorted({e['topicId'] for e in selected.values()}):
 p=m.C/'src/content/topics'/f'{tid}.json';cur=m.read(p);old=json.loads(m.h.git(m.C,'show',cp['baselineSHA']+':'+str(p.relative_to(m.C))))
 assert [q['id'] for q in cur['questions']]==[q['id'] for q in old['questions']],tid
 topics[tid]=cur;baseline[tid]={q['id']:q for q in old['questions']}
 for q in cur['questions']:assert q['id'] not in catalog;catalog[q['id']]=q
for qid,e in selected.items():
 q=catalog[qid];b=baseline[e['topicId']][qid]
 assert m.sha(b)==e['baselineCanonicalSha256'] and q['difficulty']==b['difficulty']==e['difficulty'] and q['correctIndex']==b['correctIndex']==e['correctIndex'],qid
assert all(m.sha(catalog[e['questionId']])==e['cardCanonicalSha256'] for e in cp['completedCardHashes'])
original83=m.h.git(m.C,'rev-parse','463701e1^{commit}')
S=m.C/'docs/content-audits/question-quality-wave-8/coordinator-01a16254'
raw83=S/'source-history-russia83'
for name in ['candidate.json','sourceproof.json']:
 p=raw83/name;old=subprocess.check_output(['git','-C',str(m.C),'show',original83+':'+str(p.relative_to(m.C))]);assert old==p.read_bytes(),name
assert m.read(S/'source83-original-format-diagnostics.json')['reason']
assert x['pendingHistoryRussia83']['status']=='CERTIFIED_SAME_READER_FINAL_PASS' and x['pendingHistoryRussia83']['qualityCredit']==1
for root,key in [(m.C,'code'),(m.P,'planning')]:assert m.raw(pathlib.Path(m.h.git(root,'rev-parse','--path-format=absolute','--git-path','index')))==x['foreignIndexes'][key]
assert m.read(m.P/'.flow-leases.json')=={} and all(m.flow.get(cid)[1]['owner']==m.O for cid in x['claims'])
assert cp['owner']==cp['activeCoordinator']==m.O
assert m.read(m.P/'evidence/question-revision-process-v2/coordinator-state.json')['owner']==m.O
assert m.read(m.P/'evidence/question-revision-process-v2/active-full2000-goal-01a1593a.json')['owner']==m.O
qa=[]
for item in x['ownAffectedRuns']:
 path=item['path'] if isinstance(item,dict) else item
 p=pathlib.Path(path);v=m.read(p);assert v['success'] and v['numPassedTests']==19 and v['numFailedTests']==v['numPendingTests']==v.get('numTodoTests',0)==0
 if isinstance(item,dict):assert m.raw(p)==item['rawSHA256']
 assert m.h.git(m.C,'show','HEAD:'+str(p.relative_to(m.C))).encode()==p.read_bytes().rstrip(b'\n')
 qa.append({'path':str(p),'rawSHA256':m.raw(p),'passed':19,'failed':0,'pending':0})
packets=[]
for order in range(96,101):
 pending=x.get(f'pendingHistoryRussia{order}',{})
 for suffix,key in [('', 'rawFreeze'),('-cycle1','cycle1RawFreeze')]:
  freeze=pending.get(key);p=D/('source-history-russia'+str(order)+suffix)
  if not freeze or not p.is_dir():continue
  files=[f for f in p.rglob('*') if f.is_file()]
  checked=[]
  for f in files:
   rel=str(f.relative_to(m.C));result=subprocess.run(['git','-C',str(m.C),'show',freeze+':'+rel],capture_output=True)
   if result.returncode==0:
    assert result.stdout==f.read_bytes(),str(f);checked.append(str(f.relative_to(p)))
  assert 'candidate.json' in checked and 'sourceproof.json' in checked,(order,suffix)
  packets.append({'order':order,'suffix':suffix,'freeze':freeze,'exactFrozenFiles':checked})
native=[]
for key,a in [('root',x['rootNativeAudit']),*x['actors'].items(),*[(f'retired-reader-{i}',a) for i,a in enumerate(x.get('retiredNativeReviewersCurrentOwner',[]))]]:
 p=pathlib.Path(a['nativeJournal'])
 if not p.exists():
  matches=list(pathlib.Path('/Users/eaafonasev/.codex/archived_sessions').rglob('*'+a['threadId']+'.jsonl'));assert len(matches)==1;p=matches[0]
 rows=[json.loads(l) for l in p.open()];sid=next(r['payload']['id'] for r in rows if r['type']=='session_meta');assert sid==a['threadId']
 comp=sum(r['type']=='compacted' for r in rows);info=next(r['payload']['info'] for r in reversed(rows) if r.get('payload',{}).get('type')=='token_count')
 last=next(r['payload']['type'] for r in reversed(rows) if r.get('payload',{}).get('type') in ['task_started','task_complete'])
 if key!='root':assert last=='task_complete' and not a['stage'].startswith('START'),key
 native.append({'actor':key,'threadId':sid,'nativeJournal':str(p),'actualCompactions':comp,'lastTaskEvent':last,'lastInput':info['last_token_usage']['input_tokens'],'modelWindow':info['model_context_window']})
remote=dict(line.split()[::-1] for line in m.h.git(m.C,'ls-remote','origin','refs/heads/main','refs/heads/'+x['codeBranch']).splitlines());main=remote['refs/heads/main'];feature=remote['refs/heads/'+x['codeBranch']]
pushes=[m.flow.get(cid)[1]['evidence']['remote_push'] for cid in x['claims']];assert all(v==pushes[0] for v in pushes) and pushes[0]['CURRENT']==n and pushes[0]['remaining']==2000-n and pushes[0]['readbackVerified'] and pushes[0]['commit']==feature
assert subprocess.run(['git','-C',str(m.C),'cat-file','-e',main+'^{commit}'],capture_output=True).returncode==0,'Fresh origin main object missing; inspect before any fetch, no guessed main evidence'
maincards={}
for tid in topics:
 p='src/content/topics/'+tid+'.json';v=json.loads(m.h.git(m.C,'show',main+':'+p));maincards.update({q['id']:q for q in v['questions']})
exactmain=sum(m.sha(maincards.get(e['questionId']))==e['cardCanonicalSha256'] for e in cp['completedCardHashes'])
def ancestor(a,b):
 r=subprocess.run(['git','-C',str(m.C),'merge-base','--is-ancestor',a,b]);assert r.returncode in [0,1];return r.returncode==0
status={}
for root in [m.C,m.P]:
 r=subprocess.run(['git','-C',str(root),'--no-optional-locks','status','--porcelain=v1','--untracked-files=all','--ignored'],text=True,capture_output=True)
 # --no-optional-locks is a Git global flag, preserve any diagnostic instead of silently ignoring it.
 assert r.returncode==0,r.stderr
 status[str(root)]={'lines':len(r.stdout.splitlines()),'rawSHA256':hashlib.sha256(r.stdout.encode()).hexdigest(),'unknownResourcesRemoved':False}
report={'owner':m.O,'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'CURRENT':n,'remaining':2000-n,'selected':2000,'partitionCompleteDisjoint':True,'allCurrentAcceptedHashesExact':True,'frozenBaselineDifficultyKeyTopicOrder':True,'baseline':cp['baselineSHA'],'ownScopeOrders':list(range(96,101)),'remotePushAuthoritySnapshot':pushes[0],'branches':{'code':{'branch':x['codeBranch'],'commit':m.h.git(m.C,'rev-parse','refs/heads/'+x['codeBranch'])},'planning':{'branch':x['planningBranch'],'commit':m.h.git(m.P,'rev-parse','refs/heads/'+x['planningBranch']),'checkoutBranch':m.h.git(m.P,'branch','--show-current')}},'source95ProceduralDeviations':x.get('source95CombinedProceduralDeviations'),'source83OriginalRawExactAtFirstFAIL':{'commit':original83,'files':['candidate.json','sourceproof.json'],'originalFAILPreserved':True,'creditOnlyAfterSameReaderFINALPASS':True},'foreignIndexes':x['foreignIndexes'],'claimsExactOwner':m.O,'leaseEmpty':True,'qa':qa,'rawPackets':packets,'native':native,'origin':{'main':main,'feature':feature,'acceptedHashesOnMain':exactmain,'acceptedCount':n,'featureAncestorOfMain':ancestor(feature,main),'mainAncestorOfFeature':ancestor(main,feature),'integrationPerformed':False},'status':status,'noSemanticRereviewOrQARerun':True,'notRun':['full suite','runtime','browser','Player/build','deploy','release','human/device acceptance']}
m.write(D/'handoff-verification.json',report)
print(m.savecode([pathlib.Path(__file__),D/'handoff-verification.json'],'Preserve exact current checkpoint hashes and bounded closure verification'))
print({'CURRENT':n,'remaining':2000-n,'QAReports':len(qa),'rawPackets':len(packets),'nativeActors':len(native),'acceptedHashesOnMain':exactmain,'originMain':main,'foreignIndexesPreserved':True})
