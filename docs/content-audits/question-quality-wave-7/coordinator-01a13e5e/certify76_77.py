import pathlib,json,hashlib,subprocess,importlib.util,datetime
C=pathlib.Path(__file__).resolve().parents[4];P=pathlib.Path('/Users/eaafonasev/Projects/mindbattle-planning');O='01a13e5e-e7e9-7f33-8165-57a15db42e1c';B=C/'docs/content-audits/question-quality-wave-7/process-v2-maps71-80-01a13d50/independent-initial7-01a13d50';A=B.parent/'author-cycle1-01a13e5e'
def read(p):return json.loads(p.read_text())
def sha(v):return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def raw(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def mod(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
h=mod('h',P/'evidence/question-revision-process-v2/private-save-helper-01a13cb1.py');f=mod('f',C/'tools/flow.py').Flow(P);R=B/'receipt-cycle1-current2-01a13e5e.json';D=B/'receipt-cycle1-current2-peer84-format-01a13e5e.json';r=read(R);delta=read(D);assert raw(R)=='3130a65e1b349d212f7aaaef55b819fc69645f4b84e5af3e1bda196daebed760' and raw(D)=='48fd78a7549f0a1f0612d0398c2ee4edc4b9e3894daed864cc9210bd6256657c'
cp=P/'openspec/changes/question-quality-future-waves/current-checkpoint.json';checkpoint=read(cp);catalog={};topics={}
for t in set(e['topicId'] for e in checkpoint['selectedCards']):
 topics[t]=read(C/f'src/content/topics/{t}.json')['questions'];catalog.update({q['id']:q for q in topics[t]})
assert len(checkpoint['currentEligibleCompletedIds'])==682
for e in checkpoint['completedCardHashes']:assert sha(catalog[e['questionId']])==e['cardCanonicalSha256']
for e in checkpoint['selectedCards']:assert catalog[e['questionId']]['difficulty']==e['difficulty'] and catalog[e['questionId']]['correctIndex']==e['correctIndex']
assert len(checkpoint['selectedCards'])==2000
qa=C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/qa-cycle1-hard71-75-final.json';q=read(qa);assert q['success'] and q['numPassedTests']==19 and q['numFailedTests']==q['numPendingTests']==0
assert (C/'src/content/topics/maps-cartography.json').read_bytes()==subprocess.check_output(['git','-C',str(C),'show','0393b80cbed86a147cfc3b63aae95874a13101a5:src/content/topics/maps-cartography.json'])
primary=read(C/r['evidence']['primary'])
def checkraw(x):
 if isinstance(x,dict):
  if 'path'in x and 'byteSHA256'in x:assert raw(C/x['path'])==x['byteSHA256'],x['path']
  for v in x.values():checkraw(v)
 elif isinstance(x,list):
  for v in x:checkraw(v)
checkraw(primary)
for e in delta['immutableBaseReceipts']:assert raw(C/e['path'])==e['rawByteSHA256']
assert delta['peer84']['afterCard']==catalog['maps-cartography-read-coordinates'] and sha(delta['peer84']['afterCard'])==delta['peer84']['afterCanonicalSHA256']
stage=read(B/'receipt-cycle1-current2-peer-stage81-90-01a13e5e.json');checkraw(stage);stagepeers=read(C/stage['supplement']['path'])
for e in stagepeers['currentPeers']:
 card=e['currentCard'];i=card['id']
 if i==delta['peer84']['id']:assert card==delta['peer84']['beforeCard']
 else:assert card==catalog[i]
a={e['id']:e for e in read(A/'candidate.json')['entries']};source={e['id']:e for e in read(A/'sourceproof.json')['cards']};applied={e['id']:e for e in read(C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-cycle1-76-77.json')['applied']};accepted=[]
for e in r['entries']:
 i=e['id'];c=catalog[i];assert e['status']=='PASS' and c==e['currentCard']==a[i]['proposedCard']==applied[i]['proposedCard'];assert sha(c)==e['cardCanonicalSHA256']==a[i]['proposedSHA256']==source[i]['proposedCardSHA256'];assert i not in checkpoint['currentEligibleCompletedIds'];assert topics['maps-cartography'][e['sourceOrder']-1]['id']==i
 groups={'prompt_ordered_answers_key':{'prompt':c['prompt'],'answers':[x['text'] for x in c['answers']],'correctIndex':c['correctIndex']},'explanation':c['explanation'],**{'note'+str(k):v['note'] for k,v in enumerate(c['answers'])}}
 for gs,hkey in [(e['fieldGroups'],'canonicalSHA256'),(source[i]['sixLiteralGroups'],'sha256')]:
  assert len(gs)==6 and {g['group'] for g in gs}==set(groups)
  for g in gs:assert g['literal']==groups[g['group']] and sha(g['literal'])==g[hkey]
 assert len(e['assessments'])==4 and {v['answerIndex'] for v in e['assessments']}==set(range(4))
 for v in e['assessments']:
  k=v['answerIndex'];assert v['fullPrompt']==c['prompt'] and v['answerText']==c['answers'][k]['text'] and v['noteText']==c['answers'][k]['note'];assert v['grammarAssessment'] and v['ownNoteUsefulness'] and v['keyAndPlausibilityJudgement']
 dv=next(x for x in delta['unchangedTargets'] if x['id']==i);assert dv['status']=='PASS' and dv['cardCanonicalSHA256']==sha(c)
 accepted.append({'questionId':i,'cardCanonicalSha256':sha(c),'authorNativeId':'01a13e63-3568-70d1-bc76-88e6628dcb42','authorReceipt':str((A/'sourceproof.json').relative_to(C)),'authorFreeze':'fda00931c11d854e210c03a21d23dbf9e2663b57','readerNativeId':'01a13e36-756e-77b2-8a1e-af5b0428e68a','independentReceipt':str(R.relative_to(C)),'readerPeerStageReceipt':str((B/'receipt-cycle1-current2-peer-stage81-90-01a13e5e.json').relative_to(C)),'readerPeerFormatReceipt':str(D.relative_to(C)),'readerFreezeSHA256':raw(R),'coordinatorDecision':'Accept solecycle1 exact CURRENT independent PASS:12groups8individual variants, full USGS/OS primary/text/figures, useful own notes/extra correct fact, absoluteeasy/key3 and both-direction peer criterion checked. Source/apply/author/reader hashes exact; live81–90stage and84format deltas retained. Later hard projection/GIS inputs differ from these terrain-pattern demands, and were already available as proposals; no new full-key cue introduced.'})
assert len(accepted)==2
now=datetime.datetime.now(datetime.timezone.utc).isoformat();out=C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/certification76-77.json';report={'schemaVersion':1,'owner':O,'at':now,'accepted':accepted,'newQualityCredit':2,'CURRENT':684,'remaining':1316,'verified':{'prior682CurrentHashes':True,'frozen2000Metadata':True,'literalGroups':12,'variantAssessments':8,'primaryRawBytes':True,'peerStageAnd84FormatExact':True},'QA':{'commit':'0393b80cbed86a147cfc3b63aae95874a13101a5','path':str(qa.relative_to(C)),'passed':19,'failed':0,'pending':0,'catalogBytesUnchanged':True},'fullGoalNotComplete':True,'mainIntegrated':False};write(out,report)
regp=C/'docs/content-audits/question-quality-wave-7/root-certified-source-checkpoint.json';reg=read(regp);assert len(reg['cards'])==182;reg['cards']+=accepted;reg.update(sourceEditorialCompletedCards=184,sourceEditorialCompletedFields=1104,wave7Remaining=316,ownerNativeId=O,latestBatch={'certification':str(out.relative_to(C)),'newQualityCredit':2,'CURRENT':684,'remaining':1316});write(regp,reg)
files=[str(p.relative_to(C)) for p in B.glob('receipt-cycle1-current2*.json')]+[str(p.relative_to(C)) for p in (B/'evidence-cycle1-current2').rglob('*') if p.is_file()]+[str(out.relative_to(C)),str(regp.relative_to(C)),str(pathlib.Path(__file__).resolve().relative_to(C))];idx=C/h.git(C,'rev-parse','--git-path','index');cc=h.save(C,'refs/heads/codex/question-quality-wave-6',files,'Certify exact solecycle1 hill valley CURRENT2 after independent',raw(idx));print('code',cc)
with f.locked():f.lease('acquire','planning',O)
try:
 for e in accepted:
  i=e['questionId']
  for key in ['completedIds','currentEligibleCompletedIds']:checkpoint[key].append(i)
  for key in ['remainingIds','currentRemainingIds']:checkpoint[key].remove(i)
  checkpoint['completedCardHashes'].append({k:e[k] for k in ['questionId','cardCanonicalSha256']})
 checkpoint['owner']=checkpoint['activeCoordinator']=O;checkpoint['asOf']=now;sm=checkpoint['summary']
 for k in ['currentEligibleWholeCards','historicalUniqueCards','sourceCertifiedCurrentCards']:sm[k]=684
 for k in ['remainingInSelectedScope','remainingInSelectedScopeCurrentEligible','futureWavesRemaining']:sm[k]=1316
 for k in ['currentEligibleFields','historicalUniqueFields']:sm[k]=4104
 sm['wave7CurrentCertifiedCards']=184;checkpoint['latestBatch']={'certification':str(out.relative_to(C)),'codeCommit':cc,'newQualityCredit':2,'CURRENT':684,'remaining':1316};write(cp,checkpoint)
 sp=P/'evidence/question-revision-process-v2/coordinator-state.json';state=read(sp);state['coordinatorProgress'].update(CURRENT=684,newlyCertified=5,remaining=1316);state['latestBatch']=checkpoint['latestBatch'];state['createdNativeThreads']=['01a13e63-3568-70d1-bc76-88e6628dcb42','01a13e66-1c13-71d3-8c00-86ff1c5251b1','01a13e77-59ef-7673-a3dc-32a4f701f292'];state['currentNativeActors']['activeAuthors']=[{'threadId':'01a13e77-59ef-7673-a3dc-32a4f701f292','hostId':'local','scope':'INITIALmaps91–100','status':'active'}];state['currentNativeActors']['activeIndependent']=[{'threadId':'01a13e36-756e-77b2-8a1e-af5b0428e68a','hostId':'local','scope':'solecycle1CURRENT5hard71–75','cursor':'e9edbbc2-283a-4bba-abdd-a2746c7b64f0:6','status':'active'}];state['appliedNotCertified']=[{'scope':'hard71–75solecycle1','count':5,'qualityCredit':0,'applyCommit':'a3fa2e99f327e3917734739dd3a12d05941d7022','formatAmendment':'7cc8b3c0c31c6fa623f549035c3b92e0c950a0aa','qaCommit':'0393b80cbed86a147cfc3b63aae95874a13101a5'},{'scope':'INITIAL81–90','count':10,'qualityCredit':0,'applyCommit':'6d679c25615ed1a8a582fbc57113cb36d8be0a5f','formatAmendment':'2a3f5951c3aed1b0e80b4e5c85baab2351487684','qaCommit':'187dda45eb0322ad966420e160dc5deb011ac85c','independent':'queued, newSol6.1medium afteractivefinal5'}];state['qaLatestCurrent']={'commit':'0393b80cbed86a147cfc3b63aae95874a13101a5','passCount':19,'fail':0,'pending':0,'sourceBytesUnchangedSinceQA':True,'runtimeBuildAudio':False};write(sp,state)
 pp=P/'evidence/question-revision-process-v2/certification76-77-01a13e5e.json';write(pp,{'codeBranch':'codex/question-quality-wave-6','codeCommit':cc,**report});idx=P/h.git(P,'rev-parse','--git-path','index');print('planning',h.save(P,'refs/heads/codex/question-revision-resume-20261014',[str(p.relative_to(P)) for p in [cp,sp,pp]],'Record CURRENT684 and active exact remaining queues',raw(idx)))
finally:
 with f.locked():f.lease('release','planning',O)
print('CURRENT684 remaining1316; fullgoal active')
