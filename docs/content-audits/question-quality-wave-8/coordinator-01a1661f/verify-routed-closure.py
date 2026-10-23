"""Closed owned slice: deterministic hashes/preservation only; never source/review/QA replay."""
import pathlib,json,hashlib,importlib.util,subprocess,re,datetime
D=pathlib.Path(__file__).parent
s=importlib.util.spec_from_file_location('m',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
x=m.read(D/'manifest.json');C=m.C;P=m.P;O=m.O;cp=m.read(pathlib.Path(x['canonicalCheckpoint']))
assert not any(a['stage'].startswith('START') for a in x['actors'].values())
assert all(m.flow.get(cid)[1]['owner']==O for cid in x['claims']) and m.read(P/'.flow-leases.json')=={}
assert cp['owner']==cp['activeCoordinator']==O
for name in ['coordinator-state.json','active-full2000-goal-01a1593a.json']:assert m.read(P/'evidence/question-revision-process-v2'/name)['owner']==O
sel={e['questionId']:e for e in cp['selectedCards']};done=set(cp['currentEligibleCompletedIds']);remaining=set(cp['currentRemainingIds']);n=len(done)
assert len(sel)==2000 and len(done)==len(cp['currentEligibleCompletedIds']) and len(remaining)==2000-n and not done&remaining and done|remaining==set(sel)
assert n==x['CURRENT'] and x['remaining']==2000-n and cp['baselineSHA']=='afe944c1a705edf5e2f435f17d109459ddecd365'
catalog={};old={};orders={}
for tid in sorted({e['topicId'] for e in sel.values()}):
 rel='src/content/topics/'+tid+'.json';now=m.read(C/rel);base=json.loads(m.h.git(C,'show',cp['baselineSHA']+':'+rel))
 assert now['id']==base['id']==tid and [q['id'] for q in now['questions']]==[q['id'] for q in base['questions']]
 for i,q in enumerate(now['questions'],1):catalog[q['id']]=q;orders[q['id']]=(tid,i)
 old.update({q['id']:q for q in base['questions']})
for qid,e in sel.items():
 q=catalog[qid];b=old[qid];assert orders[qid][0]==e['topicId'] and m.sha(b)==e['baselineCanonicalSha256']
 assert q['difficulty']==b['difficulty']==e['difficulty'] and q['correctIndex']==b['correctIndex']==e['correctIndex']
assert len(cp['completedCardHashes'])==n and {e['questionId'] for e in cp['completedCardHashes']}==done
assert all(m.sha(catalog[e['questionId']])==e['cardCanonicalSha256'] for e in cp['completedCardHashes'])
def bytes_at(ref,p):return subprocess.check_output(['git','-C',str(C),'show',ref+':'+str(p.relative_to(C))])
raw=[]
for key,item in x.items():
 if not re.fullmatch('pendingHumanMedicine[0-9]+',key):continue
 order=int(key.removeprefix('pendingHumanMedicine'))
 for suffix,field in [('', 'rawFreeze'),('-cycle1','cycle1RawFreeze')]:
  R=D/('source-human-medicine'+str(order)+suffix);freeze=item.get(field)
  if not freeze or not R.is_dir():continue
  proof=m.read(D/('human-medicine'+str(order)+suffix+'-native-proof.json'));bindings=proof['rawFileSHA256']
  assert {'candidate.json','sourceproof.json','peer-snapshot.json'}<=set(bindings)
  for rel,digest in bindings.items():
   p=R/rel;assert m.raw(p)==digest and bytes_at(freeze,p)==p.read_bytes(),str(p)
  raw.append({'order':order,'cycle':1 if suffix else 0,'freeze':freeze,'filesByteExact':len(bindings)})
qa=[]
for item in x['ownAffectedRuns']:
 p=pathlib.Path(item['path']);v=m.read(p);assert m.raw(p)==item['rawSHA256'] and bytes_at('HEAD',p)==p.read_bytes()
 assert v['success'] and v['numPassedTests']==19 and v['numFailedTests']==v['numPendingTests']==v.get('numTodoTests',0)==0
 qa.append(item)
assert qa
tested=qa[-1]['testedCatalogCommit']
for p in (C/'src/content/topics').glob('*.json'):assert bytes_at(tested,p)==p.read_bytes(),'Catalog drift after last actual affected19: '+str(p)
base=m.read(D/'takeover.json')['predecessorRemotePush']['commit']
changed=[p for p in m.h.git(C,'diff','--name-only',base,'HEAD','--','src/content/topics').splitlines() if p]
assert set(changed)<={'src/content/topics/'+x['activeRoute']['topicId']+'.json'},changed
original83=C/'docs/content-audits/question-quality-wave-8/coordinator-01a16254/source-history-russia83'
for name in ['candidate.json','sourceproof.json']:
 p=original83/name;assert bytes_at('463701e1cb541566022b1f042f32981a6153b761',p)==p.read_bytes()
for root,key in [(C,'code'),(P,'planning')]:assert m.raw(pathlib.Path(m.h.git(root,'rev-parse','--path-format=absolute','--git-path','index')))==x['foreignIndexes'][key]
actors=[]
for key,a in x['actors'].items():
 if a.get('archived',False) or a['stage'].startswith(('ARCHIVED','RETIRED')):continue
 p=pathlib.Path(a['nativeJournal']);rows=[json.loads(l) for l in p.open()]
 assert [r['payload']['id'] for r in rows if r.get('type')=='session_meta']==[a['threadId']]
 ev=next(r['payload']['type'] for r in reversed(rows) if r.get('payload',{}).get('type') in ['task_started','task_complete']);assert ev=='task_complete'
 info=next(r['payload']['info'] for r in reversed(rows) if r.get('payload',{}).get('type')=='token_count')
 actors.append({'key':key,'threadId':a['threadId'],'stage':a['stage'],'actualCompactions':sum(r.get('type')=='compacted' for r in rows),'lastTaskEvent':ev,'lastInput':info['last_token_usage']['input_tokens'],'window':info['model_context_window'],'remaining':info['model_context_window']-info['last_token_usage']['input_tokens']})
pushes=[m.flow.get(cid)[1]['evidence']['remote_push'] for cid in x['claims']];assert all(v==pushes[0] for v in pushes)
assert pushes[0]['CURRENT']==n and pushes[0]['remaining']==2000-n
refs={l.split()[1]:l.split()[0] for l in m.h.git(C,'ls-remote','origin','refs/heads/main','refs/heads/'+x['codeBranch']).splitlines()}
assert refs['refs/heads/'+x['codeBranch']]==pushes[0]['commit']
main=refs['refs/heads/main'];maincards={}
for tid in {e['topicId'] for e in sel.values()}:maincards.update({q['id']:q for q in json.loads(m.h.git(C,'show',main+':src/content/topics/'+tid+'.json'))['questions']})
ancestor=subprocess.run(['git','-C',str(C),'merge-base','--is-ancestor','HEAD',main]);assert ancestor.returncode in [0,1]
report={'owner':O,'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'CURRENT':n,'remaining':2000-n,'fullGoal':2000,'partitionCompleteDisjoint':True,'allCurrentAcceptedHashesExact':True,'all2000FrozenIdTopicOrderDifficultyNumericKey':True,'baseline':cp['baselineSHA'],'ownRawFreezes':raw,'ownQAReports':qa,'noSemanticRereviewOrQARerun':True,'source83OriginalByteExact':True,'allOldTopicFilesUnchangedSinceIntake':True,'ownChangedTopicPaths':changed,'claims':x['claims'],'leaseEmpty':True,'foreignIndexes':x['foreignIndexes'],'liveIdleActors':actors,'authoritativeRemotePushAtVerification':pushes[0],'originMain':main,'acceptedExactHashesOnMain':sum(m.sha(maincards[e['questionId']])==e['cardCanonicalSha256'] for e in cp['completedCardHashes']),'featureHeadAncestorOfMain':ancestor.returncode==0,'mainIntegrationPerformed':False,'codeBranch':x['codeBranch'],'codeHeadBeforeReport':m.h.git(C,'rev-parse','HEAD'),'planningManagedBranch':x['planningBranch'],'planningManagedSHA':m.h.git(P,'rev-parse','refs/heads/'+x['planningBranch']),'planningCheckout':m.h.git(P,'branch','--show-current'),'diagnostics':str(D/'own-procedural-diagnostics.json'),'originalSource1PreHoldMetadataByteGapUncured':True,'allHOLDQualityCredit':0,'goalComplete':False,'notRun':['full suite','runtime','browser','Player/build','deploy','release','OpenSpec archive','human/device acceptance']}
out=D/'handoff-verification.json';assert not out.exists();m.write(out,report)
print(m.savecode([out,pathlib.Path(__file__)],'Preserve closed exact current hashes raw freezes and bounded QA evidence'))
print({'CURRENT':n,'remaining':2000-n,'rawFreezes':len(raw),'QAReports':len(qa),'allFrozen2000':True,'acceptedHashesOnMain':report['acceptedExactHashesOnMain'],'idleActors':len(actors)})
