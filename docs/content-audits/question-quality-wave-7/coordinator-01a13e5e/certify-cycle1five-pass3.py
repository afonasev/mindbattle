import pathlib,json,hashlib,importlib.util,datetime,subprocess
C=pathlib.Path(__file__).resolve().parents[4];P=pathlib.Path('/Users/eaafonasev/Projects/mindbattle-planning');O='01a13e5e-e7e9-7f33-8165-57a15db42e1c';D=pathlib.Path(__file__).parent;B=C/'docs/content-audits/question-quality-wave-7/process-v2-maps81-90-01a13d50/independent-initial-01a13e5e';A=B.parent/'author-cycle1-01a13e5e/final'
read=lambda p:json.loads(p.read_text())
def sha(v):return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def raw(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def mod(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
h=mod('h',P/'evidence/question-revision-process-v2/private-save-helper-01a13cb1.py');f=mod('f',C/'tools/flow.py').Flow(P);cp=P/'openspec/changes/question-quality-future-waves/current-checkpoint.json';checkpoint=read(cp);catalog={}
for t in {e['topicId'] for e in checkpoint['selectedCards']}:catalog.update({q['id']:q for q in read(C/f'src/content/topics/{t}.json')['questions']})
assert len(checkpoint['currentEligibleCompletedIds'])==692
for e in checkpoint['completedCardHashes']:assert sha(catalog[e['questionId']])==e['cardCanonicalSha256']
for e in checkpoint['selectedCards']:assert catalog[e['questionId']]['difficulty']==e['difficulty'] and catalog[e['questionId']]['correctIndex']==e['correctIndex']
R=B/'receipt-cycle1-current5-01a13e5e.json';r=read(R);assert r['counts']=={'PASS':3,'HOLD':2,'separateAuthorTerminalHOLD88':1};assert raw(C/'src/content/topics/maps-cartography.json')==r['catalogRawSHA256']
for s in read(B/'evidence-cycle1/full-primary-index.json')['sources']:assert raw(C/s['path'])==s['sha256']==s['rawBytesSHA256VerifiedNow']
for p in read(B/'evidence-cycle1/full-actual-current-peers.json')['cards']:assert p['card']==catalog[p['card']['id']] and sha(p['card'])==p['canonicalSHA256']
auth={e['id']:e for e in read(A/'candidate.json')['entries']};proof={e['id']:e for e in read(A/'sourceproof.json')['entries']};apply=read(D/'apply-cycle1five-newthree.json');applied={e['id']:e for e in apply['bundles'][0]['applied']};q=read(D/'qa-cycle1five-newthree.json');assert q['success'] and q['numPassedTests']==19 and q['numFailedTests']==q['numPendingTests']==0
assert (C/'src/content/topics/maps-cartography.json').read_bytes()==subprocess.check_output(['git','-C',str(C),'show','f238ee339002f63c481da1aabd997cceb448141e:src/content/topics/maps-cartography.json'])
accepted=[]
for e in r['entries']:
 c=catalog[e['id']];i=e['id'];assert c==e['currentCard']==auth[i]['proposedCard']==applied[i]['proposedCard'];assert sha(c)==e['currentCardCanonicalSHA256']==auth[i]['afterHash']==applied[i]['proposedSHA256'];gs={'prompt_ordered_answers_key':{'prompt':c['prompt'],'answers':[v['text'] for v in c['answers']],'correctIndex':c['correctIndex']},'explanation':c['explanation'],**{'note'+str(k):v['note'] for k,v in enumerate(c['answers'])}}
 for gl,key in [(e['sixLiteralCanonicalJSONGroups'],'canonicalSHA256'),(proof[i]['literalGroups'],'literalSHA256')]:
  assert len(gl)==6 and {g['group'] for g in gl}==set(gs)
  for g in gl:assert g['literal']==gs[g['group']] and sha(g['literal'])==g[key]
 vl=e['fourFullPromptAnswerNoteAssessments'];assert len(vl)==4 and {v['slot'] for v in vl}==set(range(4))
 for v in vl:
  k=v['slot'];tr={'prompt':c['prompt'],'answer':c['answers'][k]['text'],'note':c['answers'][k]['note']};assert v['fullPromptLiteral']==tr['prompt'] and v['answerLiteral']==tr['answer'] and v['noteLiteral']==tr['note'] and v['bindingCanonicalSHA256']==sha(tr)
 if e['status']!='PASS':continue
 assert i not in checkpoint['currentEligibleCompletedIds'];accepted.append({'questionId':i,'cardCanonicalSha256':sha(c),'authorNativeId':'01a13e9d-1924-76d2-b2ce-91137ee914f1','authorReceipt':str((A/'sourceproof.json').relative_to(C)),'authorFreeze':'0708bbfcf00bc2fd52df17dd0c19c364f5154e19','readerNativeId':'01a13e84-63e8-7210-8e31-a933cf00aef8','independentReceipt':str(R.relative_to(C)),'readerReceiptRawSHA256':raw(R),'coordinatorDecision':'Accept exact FINALsolecycle1 CURRENT source/editorial PASS, author+apply+reader fullcard/6groups/4variants/sourcebytes/actualpeers+frozenlevel verified. No third editorial rereview. Other HOLD remain0.'})
assert len(accepted)==3;now=datetime.datetime.now(datetime.timezone.utc).isoformat();out=D/'certification-cycle1five-pass3.json';report={'owner':O,'at':now,'accepted':accepted,'newQualityCredit':3,'CURRENT':695,'remaining':1305,'terminalHOLD':[{'id':e['id'],'hash':e['currentCardCanonicalSHA256'],'reason':e['conclusion'],'qualityCredit':0} for e in r['entries'] if e['status']=='HOLD'],'separateTerminal88':r['separateTerminal88'],'verified':{'previous692CURRENT':True,'frozen2000':True,'reader30groups20variants':True,'authorApplyReaderExact':True,'fullPrimarySourceBytes':True,'actualRelevantPeersAndJointNEW3':True},'QA':{'commit':'f238ee339002f63c481da1aabd997cceb448141e','passed':19,'failed':0,'pending':0,'sourceBytesUnchanged':True},'mainIntegrated':False,'fullGoalNotComplete':True};write(out,report);rp=C/'docs/content-audits/question-quality-wave-7/root-certified-source-checkpoint.json';reg=read(rp);assert len(reg['cards'])==190;reg['cards']+=accepted;reg.update(sourceEditorialCompletedCards=193,sourceEditorialCompletedFields=1158,wave7Remaining=307,ownerNativeId=O,latestBatch={'certification':str(out.relative_to(C)),'newQualityCredit':3,'CURRENT':695,'remaining':1305});write(rp,reg)
files=[str(R.relative_to(C))]+[str(p.relative_to(C)) for p in (B/'evidence-cycle1').rglob('*') if p.is_file()]+[str(p.relative_to(C)) for p in [out,rp,pathlib.Path(__file__).resolve()]];cc=h.save(C,'refs/heads/codex/question-quality-wave-6',files,'Certify FINAL maps84 87 89 PASS3 and preserve terminal HOLD86 88 90',raw(C/h.git(C,'rev-parse','--git-path','index')));print('code',cc)
with f.locked():f.lease('acquire','planning',O)
try:
 for e in accepted:
  i=e['questionId']
  for k in ['completedIds','currentEligibleCompletedIds']:checkpoint[k].append(i)
  for k in ['remainingIds','currentRemainingIds']:checkpoint[k].remove(i)
  checkpoint['completedCardHashes'].append({k:e[k] for k in ['questionId','cardCanonicalSha256']})
 checkpoint['owner']=checkpoint['activeCoordinator']=O;checkpoint['asOf']=now;sm=checkpoint['summary']
 for k in ['currentEligibleWholeCards','historicalUniqueCards','sourceCertifiedCurrentCards']:sm[k]=695
 for k in ['remainingInSelectedScope','remainingInSelectedScopeCurrentEligible','futureWavesRemaining']:sm[k]=1305
 for k in ['currentEligibleFields','historicalUniqueFields']:sm[k]=4170
 sm['wave7CurrentCertifiedCards']=193
 done=set(checkpoint['currentEligibleCompletedIds'])
 for w in checkpoint['waves']:w['currentSourceEditorialCards']=len(done.intersection(w['selectedIds']))
 assert sum(w['currentSourceEditorialCards'] for w in checkpoint['waves'])==695
 checkpoint['latestBatch']={'certification':str(out.relative_to(C)),'codeCommit':cc,'newQualityCredit':3,'CURRENT':695,'remaining':1305};write(cp,checkpoint)
 sp=P/'evidence/question-revision-process-v2/coordinator-state.json';state=read(sp);state['counts']={'CURRENT':695,'remaining':1305};state['coordinatorProgress'].update(CURRENT=695,newlyCertified=16,remaining=1305);state['currentWork'].update(CURRENT=695,remaining=1305,codeCommit=cc,readyCurrentQueue=0);state['latestBatch']=checkpoint['latestBatch'];state['currentNativeActors']['activeIndependent']=[{'threadId':'01a13ec9-88e6-7423-84d0-2026dbfcffb1','hostId':'local','scope':'concreteNEW71/73/74INITIAL3'}];state['readyIndependentQueue']=[];state['terminalHOLD86_88_90']={'receipt':str(R.relative_to(C)),'qualityCredit':0,'newUnchangedFixCycleForbidden':True};state['createdNativeThreads'].append('01a13ec9-88e6-7423-84d0-2026dbfcffb1');write(sp,state);pp=P/'evidence/question-revision-process-v2/certification-cycle1five-pass3-01a13e5e.json';write(pp,{'codeBranch':'codex/question-quality-wave-6','codeCommit':cc,**report});print('planning',h.save(P,'refs/heads/codex/question-revision-resume-20261014',[str(p.relative_to(P)) for p in [cp,sp,pp]],'Record exact CURRENT695 and terminal solecycle1 HOLD3',raw(P/h.git(P,'rev-parse','--git-path','index'))))
finally:
 with f.locked():f.lease('release','planning',O)
