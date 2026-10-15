import pathlib,json,hashlib,subprocess,importlib.util,datetime
C=pathlib.Path(__file__).resolve().parents[4];P=pathlib.Path('/Users/eaafonasev/Projects/mindbattle-planning');O='01a13e5e-e7e9-7f33-8165-57a15db42e1c';B=C/'docs/content-audits/question-quality-wave-7/process-v2-maps71-80-01a13d50/independent-initial7-01a13d50';A=B.parent/'author-cycle1-01a13e5e'
def read(p):return json.loads(p.read_text())
def sha(v):return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def raw(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def mod(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
h=mod('h',P/'evidence/question-revision-process-v2/private-save-helper-01a13cb1.py');f=mod('f',C/'tools/flow.py').Flow(P);R=B/'receipt-cycle1-current5hard-01a13e5e.json';r=read(R);assert raw(R)=='e17a525785a4187f1986dd4733a89ad8122ba9c5f1e187744e603114ccd64cb6'
cp=P/'openspec/changes/question-quality-future-waves/current-checkpoint.json';checkpoint=read(cp);catalog={};topics={}
for t in set(e['topicId'] for e in checkpoint['selectedCards']):
 topics[t]=read(C/f'src/content/topics/{t}.json')['questions'];catalog.update({q['id']:q for q in topics[t]})
assert len(checkpoint['currentEligibleCompletedIds'])==684
for e in checkpoint['completedCardHashes']:assert sha(catalog[e['questionId']])==e['cardCanonicalSha256']
for e in checkpoint['selectedCards']:assert catalog[e['questionId']]['difficulty']==e['difficulty'] and catalog[e['questionId']]['correctIndex']==e['correctIndex']
assert len(checkpoint['selectedCards'])==2000
qa=C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/qa-cycle1-hard71-75-final.json';q=read(qa);assert q['success'] and q['numPassedTests']==19 and q['numFailedTests']==q['numPendingTests']==0
assert (C/'src/content/topics/maps-cartography.json').read_bytes()==subprocess.check_output(['git','-C',str(C),'show','0393b80cbed86a147cfc3b63aae95874a13101a5:src/content/topics/maps-cartography.json'])
primary=read(B/'evidence-cycle1-current5hard/primary-manifest.json')
def checkraw(x):
 if isinstance(x,dict):
  if 'path'in x and ('byteSHA256'in x or 'rawByteSHA256'in x):assert raw(C/x['path'])==x.get('byteSHA256',x.get('rawByteSHA256')),x['path']
  for v in x.values():checkraw(v)
 elif isinstance(x,list):
  for v in x:checkraw(v)
checkraw(primary)
peerVersions=read(B/'evidence-cycle1-current5hard/peer-versions.json')
for v in peerVersions['versions']:
 assert sha(v['card'])==v['canonicalSHA256']
 if any(o['stage'].startswith('actual FINALCURRENT') for o in v['origins']):assert v['card']==catalog[v['id']]
a={e['id']:e for e in read(A/'candidate.json')['entries']};source={e['id']:e for e in read(A/'sourceproof.json')['cards']};applied={e['id']:e for e in read(C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-cycle1-hard71-75.json')['applied']};accepted=[]
for e in [v for v in r['entries'] if v['status']=='PASS']:
 i=e['id'];c=catalog[i];assert e['status']=='PASS' and c==e['currentCard']==a[i]['proposedCard']==applied[i]['proposedCard'];assert sha(c)==e['cardCanonicalSHA256']==a[i]['proposedSHA256']==source[i]['proposedCardSHA256'];assert i not in checkpoint['currentEligibleCompletedIds'];assert topics['maps-cartography'][e['sourceOrder']-1]['id']==i
 groups={'prompt_ordered_answers_key':{'prompt':c['prompt'],'answers':[x['text'] for x in c['answers']],'correctIndex':c['correctIndex']},'explanation':c['explanation'],**{'note'+str(k):v['note'] for k,v in enumerate(c['answers'])}}
 for gs,hkey in [(e['fieldGroups'],'canonicalSHA256'),(source[i]['sixLiteralGroups'],'sha256')]:
  assert len(gs)==6 and {g['group'] for g in gs}==set(groups)
  for g in gs:assert g['literal']==groups[g['group']] and sha(g['literal'])==g[hkey]
 assert len(e['assessments'])==4 and {v['answerIndex'] for v in e['assessments']}==set(range(4))
 for v in e['assessments']:
  k=v['answerIndex'];assert v['fullPrompt']==c['prompt'] and v['answerText']==c['answers'][k]['text'] and v['noteText']==c['answers'][k]['note'];assert v['grammarAssessment'] and v['ownNoteUsefulnessAndTruth'] and v['truthKeyAndPlausibility']
 accepted.append({'questionId':i,'cardCanonicalSha256':sha(c),'authorNativeId':'01a13e63-3568-70d1-bc76-88e6628dcb42','authorReceipt':str((A/'sourceproof.json').relative_to(C)),'authorFreeze':'fda00931c11d854e210c03a21d23dbf9e2663b57','readerNativeId':'01a13e36-756e-77b2-8a1e-af5b0428e68a','independentReceipt':str(R.relative_to(C)),'readerFreezeSHA256':raw(R),'coordinatorDecision':'Accept solecycle1 exact HARD CURRENT PASS: LAEA metadata/ellipsoid processing and intended-dead-end exception plus bounded Extend have independent decision dimensions; full Esri source contexts,12groups8individual variants, actual and proposed peers, own notes/additional correct fact and unique key2 verified by independent. Three other entries explicitly terminalHOLD0, no unchanged second cycle.'})
assert len(accepted)==2
now=datetime.datetime.now(datetime.timezone.utc).isoformat();out=C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/certification-hard72-75.json';report={'schemaVersion':1,'owner':O,'at':now,'accepted':accepted,'newQualityCredit':2,'CURRENT':686,'remaining':1314,'verified':{'prior684CurrentHashes':True,'frozen2000Metadata':True,'literalGroups':12,'variantAssessments':8,'primaryRawBytes':True,'actualPeerVersionsExact':True},'QA':{'commit':'0393b80cbed86a147cfc3b63aae95874a13101a5','path':str(qa.relative_to(C)),'passed':19,'failed':0,'pending':0,'catalogBytesUnchanged':True},'fullGoalNotComplete':True,'mainIntegrated':False,'terminalHOLD':[{'id':e['id'],'currentCardSHA256':e['cardCanonicalSHA256'],'defects':e['defects'],'qualityCredit':0,'next':'Only concrete new source/solution route; no unchanged automatic second cycle'} for e in r['entries'] if e['status']=='HOLD']};write(out,report)
regp=C/'docs/content-audits/question-quality-wave-7/root-certified-source-checkpoint.json';reg=read(regp);assert len(reg['cards'])==184;reg['cards']+=accepted;reg.update(sourceEditorialCompletedCards=186,sourceEditorialCompletedFields=1116,wave7Remaining=314,ownerNativeId=O,latestBatch={'certification':str(out.relative_to(C)),'newQualityCredit':2,'CURRENT':686,'remaining':1314});write(regp,reg)
files=[str(R.relative_to(C))]+[str(p.relative_to(C)) for p in (B/'evidence-cycle1-current5hard').rglob('*') if p.is_file()]+[str(out.relative_to(C)),str(regp.relative_to(C)),str(pathlib.Path(__file__).resolve().relative_to(C))];idx=C/h.git(C,'rev-parse','--git-path','index');cc=h.save(C,'refs/heads/codex/question-quality-wave-6',files,'Certify exact solecycle1 hard72 and75, retain terminalHOLD3',raw(idx));print('code',cc)
with f.locked():f.lease('acquire','planning',O)
try:
 for e in accepted:
  i=e['questionId']
  for key in ['completedIds','currentEligibleCompletedIds']:checkpoint[key].append(i)
  for key in ['remainingIds','currentRemainingIds']:checkpoint[key].remove(i)
  checkpoint['completedCardHashes'].append({k:e[k] for k in ['questionId','cardCanonicalSha256']})
 checkpoint['owner']=checkpoint['activeCoordinator']=O;checkpoint['asOf']=now;sm=checkpoint['summary']
 for k in ['currentEligibleWholeCards','historicalUniqueCards','sourceCertifiedCurrentCards']:sm[k]=686
 for k in ['remainingInSelectedScope','remainingInSelectedScopeCurrentEligible','futureWavesRemaining']:sm[k]=1314
 for k in ['currentEligibleFields','historicalUniqueFields']:sm[k]=4116
 sm['wave7CurrentCertifiedCards']=186;checkpoint['latestBatch']={'certification':str(out.relative_to(C)),'codeCommit':cc,'newQualityCredit':2,'CURRENT':686,'remaining':1314};write(cp,checkpoint)
 sp=P/'evidence/question-revision-process-v2/coordinator-state.json';state=read(sp);state['coordinatorProgress'].update(CURRENT=686,newlyCertified=7,remaining=1314);state['latestBatch']=checkpoint['latestBatch'];state['createdNativeThreads']=['01a13e63-3568-70d1-bc76-88e6628dcb42','01a13e66-1c13-71d3-8c00-86ff1c5251b1','01a13e77-59ef-7673-a3dc-32a4f701f292','01a13e80-549f-78c1-9129-44030f2f9072','01a13e84-63e8-7210-8e31-a933cf00aef8'];state['currentNativeActors']['activeIndependent']=[{'threadId':'01a13e84-63e8-7210-8e31-a933cf00aef8','hostId':'local','scope':'INITIALCURRENT81–90','status':'active'}];state['appliedNotCertified']=[{'scope':'INITIAL81–90','count':10,'qualityCredit':0,'applyCommit':'6d679c25615ed1a8a582fbc57113cb36d8be0a5f','formatAmendment':'2a3f5951c3aed1b0e80b4e5c85baab2351487684','qaCommit':'0393b80cbed86a147cfc3b63aae95874a13101a5'}];state['readyIndependentQueue']=[];state['terminalHOLD71_73_74']={'receipt':str(R.relative_to(C)),'certification':str(out.relative_to(C)),'qualityCredit':0,'reason':'Missingcenterlatitude71; decorativearea73; thresholdonly74. Only new concrete source/solution, no unchangedretry'};state['qaLatestCurrent']={'commit':'0393b80cbed86a147cfc3b63aae95874a13101a5','passCount':19,'fail':0,'pending':0,'sourceBytesUnchangedSinceQA':True,'runtimeBuildAudio':False};write(sp,state)
 pp=P/'evidence/question-revision-process-v2/certification-hard72-75-01a13e5e.json';write(pp,{'codeBranch':'codex/question-quality-wave-6','codeCommit':cc,**report});idx=P/h.git(P,'rev-parse','--git-path','index');print('planning',h.save(P,'refs/heads/codex/question-revision-resume-20261014',[str(p.relative_to(P)) for p in [cp,sp,pp]],'Record CURRENT686 hard PASS2 terminalHOLD3',raw(idx)))
finally:
 with f.locked():f.lease('release','planning',O)
print('CURRENT686 remaining1314; terminalHOLD3 zero; fullgoal active')
