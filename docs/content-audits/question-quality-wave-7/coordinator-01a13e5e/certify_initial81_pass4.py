import pathlib,json,hashlib,importlib.util,datetime,subprocess
C=pathlib.Path(__file__).resolve().parents[4];P=pathlib.Path('/Users/eaafonasev/Projects/mindbattle-planning');O='01a13e5e-e7e9-7f33-8165-57a15db42e1c';B=C/'docs/content-audits/question-quality-wave-7/process-v2-maps81-90-01a13d50/independent-initial-01a13e5e';A=B.parent/'author-qualification-01a13e5e'
def read(p):return json.loads(p.read_text())
def sha(v):return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def raw(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def mod(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
h=mod('h',P/'evidence/question-revision-process-v2/private-save-helper-01a13cb1.py');f=mod('f',C/'tools/flow.py').Flow(P);R=B/'receipt.json';r=read(R);cp=P/'openspec/changes/question-quality-future-waves/current-checkpoint.json';checkpoint=read(cp);catalog={}
for t in set(e['topicId'] for e in checkpoint['selectedCards']):catalog.update({q['id']:q for q in read(C/f'src/content/topics/{t}.json')['questions']})
assert len(checkpoint['currentEligibleCompletedIds'])==686
for e in checkpoint['completedCardHashes']:assert sha(catalog[e['questionId']])==e['cardCanonicalSha256']
for e in checkpoint['selectedCards']:assert catalog[e['questionId']]['difficulty']==e['difficulty'] and catalog[e['questionId']]['correctIndex']==e['correctIndex']
assert r['counts']=={'PASS':4,'FIX':6,'HOLD':0};primary=read(B/'evidence/full-primary-index.json')
for e in primary['sources']:assert raw(C/e['path'])==e['rawSHA256'],e['path']
peers=read(B/'evidence/full-current-peers.json');assert raw(C/peers['catalogFile'])==peers['catalogRawSHA256']
for e in peers['questions']:assert e['card']==catalog[e['card']['id']] and sha(e['card'])==e['canonicalSHA256']
auth={x['id']:x for x in read(A/'candidate.json')['entries']};proof={x['id']:x for x in read(A/'remaining4-final/evidence-addendum-ready6.json')['cards']};applied={x['id']:x for x in read(C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-initial-81-90.json')['applied']};qa=C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/qa-cycle1-hard71-75-final.json';q=read(qa);assert q['success'] and q['numPassedTests']==19 and q['numFailedTests']==q['numPendingTests']==0
assert (C/'src/content/topics/maps-cartography.json').read_bytes()==subprocess.check_output(['git','-C',str(C),'show','0393b80cbed86a147cfc3b63aae95874a13101a5:src/content/topics/maps-cartography.json'])
accepted=[]
for e in r['entries']:
 c=catalog[e['id']];assert c==e['currentCard'] and sha(c)==e['currentCardCanonicalSHA256']
 groups={'prompt_ordered_answers_key':{'prompt':c['prompt'],'answers':[v['text'] for v in c['answers']],'correctIndex':c['correctIndex']},'explanation':c['explanation'],**{'note'+str(k):v['note'] for k,v in enumerate(c['answers'])}}
 assert len(e['literalCanonicalGroups'])==6 and {g['group'] for g in e['literalCanonicalGroups']}==set(groups)
 for g in e['literalCanonicalGroups']:assert g['literal']==groups[g['group']] and sha(g['literal'])==g['canonicalSHA256']
 assert len(e['fourFullPromptAnswerNoteAssessments'])==4 and {v['slot'] for v in e['fourFullPromptAnswerNoteAssessments']}==set(range(4))
 for v in e['fourFullPromptAnswerNoteAssessments']:
  k=v['slot'];assert v['fullPromptLiteral']==c['prompt'] and v['answerLiteral']==c['answers'][k]['text'] and v['noteLiteral']==c['answers'][k]['note'];assert v['bindingCanonicalSHA256']==sha({'prompt':c['prompt'],'answer':v['answerLiteral'],'note':v['noteLiteral']})
 if e['status']!='PASS':continue
 i=e['id'];assert i not in checkpoint['currentEligibleCompletedIds'];assert c==auth[i]['proposedCard']==applied[i]['proposedCard'] and sha(c)==auth[i]['afterHash']==applied[i]['proposedSHA256']
 for g in proof[i]['sixLiteralGroups']:assert g['literal']==groups[g['group']] and sha(g['literal'])==g['canonicalSHA256']
 accepted.append({'questionId':i,'cardCanonicalSha256':sha(c),'authorNativeId':'01a13e66-1c13-71d3-8c00-86ff1c5251b1','authorReceipt':str((A/'remaining4-final/evidence-addendum-ready6.json').relative_to(C)),'authorFreeze':'6d679c25615ed1a8a582fbc57113cb36d8be0a5f','readerNativeId':'01a13e84-63e8-7210-8e31-a933cf00aef8','independentReceipt':str(R.relative_to(C)),'readerReceiptRawSHA256':raw(R),'coordinatorDecision':'Accept exact INITIAL CURRENT PASS for source-backed map-use easy demand after explicit author/apply/reader fullcard/group/variant/primary/actual100peers binding. Reader independently confirms useful own notes/new fact, grammar/plausibility, unique key and frozen absoluteeasy. Six other FIX remain0credit, not implicitly accepted.'})
assert len(accepted)==4
out=C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/certification-initial81-pass4.json';now=datetime.datetime.now(datetime.timezone.utc).isoformat();report={'schemaVersion':1,'owner':O,'at':now,'accepted':accepted,'newQualityCredit':4,'CURRENT':690,'remaining':1310,'readerReceiptRawSHA256':raw(R),'initialFIX':[{'id':e['id'],'currentCardSHA256':e['currentCardCanonicalSHA256'],'fixDirection':e['fixDirection'],'absoluteDifficulty':e['absoluteFrozenDifficulty'],'qualityCredit':0} for e in r['entries'] if e['status']=='FIX'],'verified':{'prior686CurrentHashes':True,'frozen2000Metadata':True,'all10ReaderCurrentHashes':True,'reader60groups40variants':True,'PASS4authorApplyReaderExact':True,'fullPrimaryBytes':True,'actual100PeersExact':True},'QA':{'commit':'0393b80cbed86a147cfc3b63aae95874a13101a5','passed':19,'failed':0,'pending':0,'sourceBytesUnchanged':True},'fullGoalNotComplete':True,'mainIntegrated':False};write(out,report)
regp=C/'docs/content-audits/question-quality-wave-7/root-certified-source-checkpoint.json';reg=read(regp);assert len(reg['cards'])==186;reg['cards']+=accepted;reg.update(sourceEditorialCompletedCards=190,sourceEditorialCompletedFields=1140,wave7Remaining=310,ownerNativeId=O,latestBatch={'certification':str(out.relative_to(C)),'newQualityCredit':4,'CURRENT':690,'remaining':1310});write(regp,reg)
request=C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/fix-request-initial81-six-cycle1.json';write(request,{'cycle':1,'stage':'single authorized substantive authorfix afterINITIAL reader; not dispatched until author capacity frees','baselineCommit':h.git(C,'rev-parse','HEAD'),'reader':'01a13e84-63e8-7210-8e31-a933cf00aef8','readerReceipt':str(R.relative_to(C)),'scopeIds':[e['id'] for e in r['entries'] if e['status']=='FIX'],'entries':[{'id':e['id'],'sourceOrder':e['sourceOrder'],'beforeCard':e['currentCard'],'beforeSHA256':e['currentCardCanonicalSHA256'],'grammar':e['grammar'],'uniqueKey':e['uniqueKey'],'difficulty':e['absoluteFrozenDifficulty'],'correctNoteAdditionalFact':e['correctNoteAdditionalFact'],'fixDirection':e['fixDirection']} for e in r['entries'] if e['status']=='FIX'],'frozen':'ID/topic/order/originaldifficulty/numericcorrectIndex; alltextsemanticsmutable source-backed','ready4Frozen':'Do not modify certified81/82/83/85.90 may remaintextuallyunchanged if only88pairdependencyneedsrepair; exact final pair must be rechecked.','qualityCredit':0})
files=[str(p.relative_to(C)) for p in B.rglob('*') if p.is_file()]+[str(out.relative_to(C)),str(request.relative_to(C)),str(regp.relative_to(C)),str(pathlib.Path(__file__).resolve().relative_to(C))];idx=C/h.git(C,'rev-parse','--git-path','index');cc=h.save(C,'refs/heads/codex/question-quality-wave-6',files,'Certify initial maps81–90 PASS4 and preserve solecycle1 FIX6 request',raw(idx));print('code',cc)
with f.locked():f.lease('acquire','planning',O)
try:
 for e in accepted:
  i=e['questionId']
  for key in ['completedIds','currentEligibleCompletedIds']:checkpoint[key].append(i)
  for key in ['remainingIds','currentRemainingIds']:checkpoint[key].remove(i)
  checkpoint['completedCardHashes'].append({k:e[k] for k in ['questionId','cardCanonicalSha256']})
 checkpoint['owner']=checkpoint['activeCoordinator']=O;checkpoint['asOf']=now;sm=checkpoint['summary']
 for k in ['currentEligibleWholeCards','historicalUniqueCards','sourceCertifiedCurrentCards']:sm[k]=690
 for k in ['remainingInSelectedScope','remainingInSelectedScopeCurrentEligible','futureWavesRemaining']:sm[k]=1310
 for k in ['currentEligibleFields','historicalUniqueFields']:sm[k]=4140
 sm['wave7CurrentCertifiedCards']=190;checkpoint['latestBatch']={'certification':str(out.relative_to(C)),'codeCommit':cc,'newQualityCredit':4,'CURRENT':690,'remaining':1310};write(cp,checkpoint)
 sp=P/'evidence/question-revision-process-v2/coordinator-state.json';state=read(sp);state['coordinatorProgress'].update(CURRENT=690,newlyCertified=11,remaining=1310);state['latestBatch']=checkpoint['latestBatch'];state['currentNativeActors']['activeIndependent']=[];state['currentNativeActors']['retainedIdleReaders']=[{'threadId':'01a13e84-63e8-7210-8e31-a933cf00aef8','hostId':'local','scope':'solecycle1 FINAL84/86/87/88/89/90 after newauthorfix','cursor':'05e9f60d-c782-4eb5-b0e5-923325bd1140:2','status':'idle retained'}];state['appliedNotCertified']={'scope':'INITIAL81–90 FIX6 current','count':6,'qualityCredit':0,'next':'freshauthor singlecycle1 thenretained84reader','request':str(request.relative_to(C))};state['terminalHOLD71_73_74']['concreteNewRoute']='docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/concrete-new-solutions-terminal71-73-74.json';state['terminalHOLD71_73_74']['readerArchived']=True;write(sp,state)
 pp=P/'evidence/question-revision-process-v2/certification-initial81-pass4-01a13e5e.json';write(pp,{'codeBranch':'codex/question-quality-wave-6','codeCommit':cc,**report});idx=P/h.git(P,'rev-parse','--git-path','index');print('planning',h.save(P,'refs/heads/codex/question-revision-resume-20261014',[str(p.relative_to(P)) for p in [cp,sp,pp]],'Record CURRENT690 and pending solecycle1 FIX6',raw(idx)))
finally:
 with f.locked():f.lease('release','planning',O)
print('CURRENT690 remaining1310; fullgoal active')
