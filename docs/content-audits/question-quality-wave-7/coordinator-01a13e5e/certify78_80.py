import json,pathlib,hashlib,subprocess,importlib.util,datetime
C=pathlib.Path(__file__).resolve().parents[4];P=pathlib.Path('/Users/eaafonasev/Projects/mindbattle-planning');OWNER='01a13e5e-e7e9-7f33-8165-57a15db42e1c'
def read(p):return json.loads(p.read_text())
def sha(x):return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def byte(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def mod(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
h=mod('private',P/'evidence/question-revision-process-v2/private-save-helper-01a13cb1.py');f=mod('flow',C/'tools/flow.py').Flow(P)
B=C/'docs/content-audits/question-quality-wave-7/process-v2-maps71-80-01a13d50';R=B/'independent-source-hold78-80-new-solution-01a13d50/receipt.json';A=B/'source-hold78-80-new-solution-author-01a13d50/candidate.json';S=B/'source-hold78-80-new-solution-author-01a13d50/sourceproof.json';E=B/'exact-apply-source-hold78-80-new-solution-01a13d50.json';Q=B/'qa-source-hold78-80-new-solution-01a13d50.json';r,a,s,ap,q=map(read,[R,A,S,E,Q]);cp=P/'openspec/changes/question-quality-future-waves/current-checkpoint.json';checkpoint=read(cp)
assert byte(R)=='4a65ad43553cd92893adae2a0bbd354997ab19ad8122db15849dfb27a353f37e'
assert q['success'] and q['numPassedTests']==19 and q['numFailedTests']==q['numPendingTests']==0
catalog={};topics={}
for t in set(e['topicId'] for e in checkpoint['selectedCards']):
 topics[t]=read(C/f'src/content/topics/{t}.json')['questions'];catalog.update({x['id']:x for x in topics[t]})
selected={e['questionId']:e for e in checkpoint['selectedCards']};assert len(selected)==2000
for e in checkpoint['selectedCards']:
 c=catalog[e['questionId']];assert c['difficulty']==e['difficulty'] and c['correctIndex']==e['correctIndex']
for e in checkpoint['completedCardHashes']:assert sha(catalog[e['questionId']])==e['cardCanonicalSha256']
assert len(checkpoint['currentEligibleCompletedIds'])==679
assert all((C/f'src/content/topics/{t}.json').read_bytes()==subprocess.check_output(['git','-C',str(C),'show','3f1ebd1ce5f16cb7d37dd0a25476863fa0c6f130:src/content/topics/'+t+'.json']) for t in topics)
auth={x['id']:x for x in a['entries']};proof={x['id']:x for x in s['cards']};applied={x['id']:x for x in ap['applied']}
sources=set()
def rawcheck(x):
 if isinstance(x,dict):
  if 'path'in x and 'byteSHA256'in x:
   p=C/x['path'];assert p.is_file(),p;assert byte(p)==x['byteSHA256'],p;sources.add(str(p.relative_to(C)))
  for v in x.values():rawcheck(v)
 elif isinstance(x,list):
  for v in x:rawcheck(v)
rawcheck(r);rawcheck(s)
peers=read(C/r['peerEvidence']);rawcheck(peers)
for p in peers['actualCurrent']:
 assert p['card']==catalog[p['card']['id']] and sha(p['card'])==p['cardSHA256']
accepted=[]
for e in r['entries']:
 i=e['id'];c=catalog[i];ae=auth[i];pe=proof[i];assert e['status']=='PASS' and not e['unresolvedDefects']
 assert c==e['actualCurrentCard']==ae['proposedCard']==applied[i]['proposedCard'];assert sha(c)==e['actualCurrentCardSHA256']==ae['afterHash']==pe['proposedSHA256']
 assert sha(ae['beforeCard'])==ae['beforeHash'];assert topics['maps-cartography'][e['sourceOrder']-1]['id']==i
 assert i not in checkpoint['currentEligibleCompletedIds']
 groups={'prompt_ordered_answers_key':{'prompt':c['prompt'],'answers':[v['text'] for v in c['answers']],'correctIndex':c['correctIndex']},'explanation':c['explanation'],**{'note'+str(k):v['note'] for k,v in enumerate(c['answers'])}}
 for gs,key in [(e['fieldGroups'],'group'),(ae['fieldGroups'],'group'),(pe['evidence'],'fieldGroup')]:
  assert len(gs)==6 and {g[key] for g in gs}==set(groups)
  for g in gs:assert g['literal']==groups[g[key]] and g['literalSHA256']==sha(g['literal'])
 for assessments in [e['assessments'],ae['assessments']]:
  assert len(assessments)==4 and {v['answerIndex'] for v in assessments}==set(range(4))
  for v in assessments:
   k=v['answerIndex'];assert v['fullPrompt']==c['prompt'] and v['answer']==c['answers'][k]['text'] and v['note']==c['answers'][k]['note'] and v['isKey']==(k==c['correctIndex'])
   if 'tripleSHA256'in v:assert v['tripleSHA256']==sha({'prompt':c['prompt'],'answer':v['answer'],'note':v['note']})
 assert e['easyAssessment'] and e['correctNoteAddsUsefulNewFact'] and e['peerComparison']['decision'].startswith('PASS')
 accepted.append({'questionId':i,'cardCanonicalSha256':sha(c),'authorNativeId':'01a13e32-1076-7d13-b329-a1aab08cd3fd','authorReceipt':str(A.relative_to(C)),'authorSourceProof':str(S.relative_to(C)),'authorFreeze':'f9ac6144ba852f5d98a59308db6b7c3d45672d53','readerNativeId':'01a13e47-d40f-7113-b45e-b874fa9d04da','independentReceipt':str(R.relative_to(C)),'readerFreeze':'69d1f9402912fed661bbb7c4fee788a2f8eed130','coordinatorDecision':'Accept exact CURRENT PASS: independently checked fictional coverage plus scale selection, N/W conjunction, and print enlargement;18 literal groups12variants complete primary bytes plus actual/proposed peers. Useful own notes and absolute easy explicitly assessed. Original sourceHOLD retained; no third full semantic rereview.'})
assert len(accepted)==3
now=datetime.datetime.now(datetime.timezone.utc).isoformat();out=C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/certification78-80.json';report={'schemaVersion':1,'at':now,'owner':OWNER,'accepted':accepted,'newQualityCredit':3,'CURRENT':682,'remaining':1318,'QA':{'path':str(Q.relative_to(C)),'commit':'3f1ebd1ce5f16cb7d37dd0a25476863fa0c6f130','passed':19,'fail':0,'pending':0,'allSelectedTopicBytesUnchanged':True},'verified':{'prior679Hashes':True,'frozen2000Metadata':True,'authorApplyReader3Exact':True,'literalGroups':18,'variantBindings':12,'rawSourcesAndPeers':sorted(sources),'actualCurrentPeers':len(peers['actualCurrent'])},'fullGoalNotComplete':True,'mainIntegrated':False};write(out,report)
regp=C/'docs/content-audits/question-quality-wave-7/root-certified-source-checkpoint.json';reg=read(regp);assert len(reg['cards'])==179;reg['cards']+=accepted;reg['sourceEditorialCompletedCards']=182;reg['sourceEditorialCompletedFields']=1092;reg['wave7Remaining']=318;reg['ownerNativeId']=OWNER;reg['latestBatch']={'certification':str(out.relative_to(C)),'newQualityCredit':3,'CURRENT':682,'remaining':1318};write(regp,reg)
idx=C/h.git(C,'rev-parse','--git-path','index');codecommit=h.save(C,'refs/heads/codex/question-quality-wave-6',[str(out.relative_to(C)),str(regp.relative_to(C)),str(pathlib.Path(__file__).resolve().relative_to(C))],'Certify three exact CURRENT map-use cards',byte(idx));print('codeCommit',codecommit)
with f.locked():
 assert all(f.get(cid)[1]['owner']==OWNER for cid in ['question-quality-future-waves','question-quality-wave-7']);f.lease('acquire','planning',OWNER)
try:
 for e in accepted:
  i=e['questionId']
  for key in ['completedIds','currentEligibleCompletedIds']:checkpoint[key].append(i)
  for key in ['remainingIds','currentRemainingIds']:checkpoint[key].remove(i)
  checkpoint['completedCardHashes'].append({k:e[k] for k in ['questionId','cardCanonicalSha256']})
 checkpoint['owner']=checkpoint['activeCoordinator']=OWNER;checkpoint['asOf']=now
 sm=checkpoint['summary']
 for k in ['currentEligibleWholeCards','historicalUniqueCards','sourceCertifiedCurrentCards']:sm[k]=682
 for k in ['remainingInSelectedScope','remainingInSelectedScopeCurrentEligible','futureWavesRemaining']:sm[k]=1318
 for k in ['currentEligibleFields','historicalUniqueFields']:sm[k]=4092
 sm['wave7CurrentCertifiedCards']=182
 checkpoint['latestBatch']={'certification':str(out.relative_to(C)),'codeCommit':codecommit,'newQualityCredit':3,'CURRENT':682,'remaining':1318};write(cp,checkpoint)
 statep=P/'evidence/question-revision-process-v2/coordinator-state.json';state=read(statep);state['threadId']=state['activeCoordinator']=OWNER;state['coordinatorProgress'].update(CURRENT=682,newlyCertified=3,remaining=1318);state['currentNativeActors']['savedIndependentInputs']=[];state['currentNativeActors']['activeAuthors']=[{'threadId':'01a13e63-3568-70d1-bc76-88e6628dcb42','hostId':'local','scope':'maps71–77 sole cycle1','output':'docs/content-audits/question-quality-wave-7/process-v2-maps71-80-01a13d50/author-cycle1-01a13e5e','status':'active'}];state['createdNativeThreads']=['01a13e63-3568-70d1-bc76-88e6628dcb42'];state['latestBatch']=checkpoint['latestBatch'];write(statep,state)
 pp=P/'evidence/question-revision-process-v2/certification78-80-01a13e5e.json';write(pp,{'codeBranch':'codex/question-quality-wave-6','codeCommit':codecommit,**report})
 pi=P/h.git(P,'rev-parse','--git-path','index');planningcommit=h.save(P,'refs/heads/codex/question-revision-resume-20261014',[str(p.relative_to(P)) for p in [cp,statep,pp]],'Record CURRENT682 exact-bound certification',byte(pi));print('planningCommit',planningcommit)
finally:
 with f.locked():f.lease('release','planning',OWNER)
print('CURRENT682 remaining1318; fullgoal active; no catalog changes; indexes preserved')
