"""Private-index preservation and exact CURRENT bookkeeping for already-bound reader PASS."""
import pathlib,json,hashlib,importlib.util,datetime,subprocess
C=pathlib.Path(__file__).resolve().parents[4];P=pathlib.Path('/Users/eaafonasev/Projects/mindbattle/planning');O='01a18898-1b03-79b3-a710-b853b6a8b519'
def read(p):return json.loads(pathlib.Path(p).read_text())
def sha(v):return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def raw(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def write(p,v):
 p=pathlib.Path(p)
 if P in p.parents:
  assert read(P/'.flow-leases.json').get('planning',{}).get('owner')==O
  idx=pathlib.Path(h.git(P,'rev-parse','--path-format=absolute','--git-path','index'))
  assert raw(idx)==read(pathlib.Path(__file__).parent/'manifest.json')['foreignIndexes']['planning']
 p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def mod(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
h=mod('private_save',P/'evidence/question-revision-process-v2/private-save-helper-01a13cb1.py');flow=mod('owned_flow',C/'tools/flow.py').Flow(P)
def certify(accepted,report,expected,wave,out,files,qaCommit):
 cp=P/'openspec/changes/question-quality-future-waves/current-checkpoint.json';ck=read(cp);catalog={}
 for t in {e['topicId'] for e in ck['selectedCards']}:catalog.update({q['id']:q for q in read(C/f'src/content/topics/{t}.json')['questions']})
 done=set(ck['currentEligibleCompletedIds']);assert len(done)==expected and len(done)==len(ck['currentEligibleCompletedIds']);assert len(ck['completedCardHashes'])==expected
 for e in ck['completedCardHashes']:assert sha(catalog[e['questionId']])==e['cardCanonicalSha256']
 for e in ck['selectedCards']:assert catalog[e['questionId']]['difficulty']==e['difficulty'] and catalog[e['questionId']]['correctIndex']==e['correctIndex']
 assert accepted and len({e['questionId'] for e in accepted})==len(accepted)
 for e in accepted:assert e['questionId'] not in done and sha(catalog[e['questionId']])==e['cardCanonicalSha256']
 for t in ['maps-cartography','engineering-machines']:assert (C/f'src/content/topics/{t}.json').read_bytes()==subprocess.check_output(['git','-C',str(C),'show',qaCommit+f':src/content/topics/{t}.json'])
 n=expected+len(accepted);now=datetime.datetime.now(datetime.timezone.utc).isoformat();report.update(owner=O,at=now,accepted=accepted,newQualityCredit=len(accepted),CURRENT=n,remaining=2000-n,mainIntegrated=False,fullGoalNotComplete=True);write(out,report);rp=C/f'docs/content-audits/question-quality-wave-{wave}/root-certified-source-checkpoint.json';reg=read(rp);before=len(reg['cards']);reg['cards']+=accepted;reg.update(sourceEditorialCompletedCards=before+len(accepted),sourceEditorialCompletedFields=6*(before+len(accepted)),ownerNativeId=O,latestBatch={'certification':str(pathlib.Path(out).relative_to(C)),'newQualityCredit':len(accepted),'CURRENT':n,'remaining':2000-n});reg[f'wave{wave}Remaining']=500-len(reg['cards']);write(rp,reg);files=list(dict.fromkeys([str(pathlib.Path(p).relative_to(C)) for p in files+[out,rp,pathlib.Path(__file__).resolve()]]));cc=h.save(C,'refs/heads/codex/question-quality-wave-6',files,f'Certify exact CURRENT{n} bound independent PASS{len(accepted)} wave{wave}',raw(C/h.git(C,'rev-parse','--git-path','index')));print('code',cc)
 planningIndex=pathlib.Path(h.git(P,'rev-parse','--path-format=absolute','--git-path','index'))
 expectedPlanningIndex=globals().get('_preleasePlanningIndex',raw(planningIndex))
 assert raw(planningIndex)==expectedPlanningIndex, 'Foreign planning index advanced before certificate writes'
 with flow.locked():flow.lease('acquire','planning',O)
 try:
  assert raw(planningIndex)==expectedPlanningIndex
  for e in accepted:
   i=e['questionId']
   for k in ['completedIds','currentEligibleCompletedIds']:ck[k].append(i)
   for k in ['remainingIds','currentRemainingIds']:ck[k].remove(i)
   ck['completedCardHashes'].append({k:e[k] for k in ['questionId','cardCanonicalSha256']})
  ck['owner']=ck['activeCoordinator']=O;ck['asOf']=now;sm=ck['summary']
  for k in ['currentEligibleWholeCards','historicalUniqueCards','sourceCertifiedCurrentCards']:sm[k]=n
  for k in ['remainingInSelectedScope','remainingInSelectedScopeCurrentEligible','futureWavesRemaining']:sm[k]=2000-n
  for k in ['currentEligibleFields','historicalUniqueFields']:sm[k]=6*n
  sm[f'wave{wave}CurrentCertifiedCards']=len(reg['cards']);done=set(ck['currentEligibleCompletedIds'])
  for w in ck['waves']:w['currentSourceEditorialCards']=len(done.intersection(w['selectedIds']))
  assert sum(w['currentSourceEditorialCards'] for w in ck['waves'])==n;ck['latestBatch']={'certification':str(pathlib.Path(out).relative_to(C)),'codeCommit':cc,'newQualityCredit':len(accepted),'CURRENT':n,'remaining':2000-n};write(cp,ck);sp=P/'evidence/question-revision-process-v2/coordinator-state.json';st=read(sp);st['counts']={'CURRENT':n,'remaining':2000-n};st['coordinatorProgress'].update(CURRENT=n,newlyCertified=n-1183,remaining=2000-n);st['currentWork'].update(CURRENT=n,remaining=2000-n,codeCommit=cc);st['latestBatch']=ck['latestBatch'];write(sp,st);pp=P/f'evidence/question-revision-process-v2/{pathlib.Path(out).stem}-01a18898.json';write(pp,{'codeBranch':'codex/question-quality-wave-6','codeCommit':cc,**report});print('planning',h.save(P,'refs/heads/codex/question-revision-resume-20261014',[str(p.relative_to(P)) for p in [cp,sp,pp]],f'Record CURRENT{n} exact independent PASS and retained residual gates',expectedPlanningIndex))
 finally:
  with flow.locked():flow.lease('release','planning',O)
 return cc
