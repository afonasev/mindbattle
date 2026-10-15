"""Bind exact independent FINAL5 and SOURCE EPUB completion; accept3, retain2HOLD."""
import pathlib,json,hashlib,importlib.util,subprocess
C=pathlib.Path(__file__).resolve().parents[4];D=pathlib.Path(__file__).parent;P=pathlib.Path('/Users/eaafonasev/Projects/mindbattle/planning');O='01a13f31-9224-7dd1-90e0-e5b0ea2e94a9'
def rd(p):return json.loads(pathlib.Path(p).read_text())
def sha(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def raw(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def wr(p,v):pathlib.Path(p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
s=importlib.util.spec_from_file_location('m',D/'certification-common-relocated.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.O=O
R=D/'independent-books8-initial/final-cycle1-ready5';rp=R/'receipt.json';r=rd(rp);sources=rd(R/'sources.json');peers=rd(R/'peers.json');a=rd(D/'apply-books5-cycle1.json');qa=rd(D/'qa-books5-cycle1.json');A=C/'docs/content-audits/question-quality-wave-8/process-v2-books7-cycle1-01a13f31/author';addp=A/'proof-completion-addendum.json';ad=rd(addp)
assert len(r['entries'])==5 and qa['numPassedTests']==19 and qa['numFailedTests']==qa['numPendingTests']==0
assert (C/'src/content/topics/books-publishing.json').read_bytes()==subprocess.check_output(['git','-C',str(C),'show','963cf73eb152ec9e2cc739aaba70d1f4b67d2d2e:src/content/topics/books-publishing.json'])
catalog={}
for t in {p['topicId'] for p in peers['actualCurrentPeers']}:catalog.update({q['id']:q for q in rd(C/f'src/content/topics/{t}.json')['questions']})
for p in peers['actualCurrentPeers']:assert p['card']==catalog[p['id']] and sha(p['card'])==p['canonicalSHA256']
for s in sources['entries']:assert raw(s['path'])==s['rawReadSHA256'] and s['personalReadEvidence'] and s['locator']
assert ad['currentCard']==catalog['books-publishing-ebook-form'] and sha(ad['currentCard'])==ad['currentCardCanonicalSHA256'] and not ad['cardTextChanged'];n=ad['newSourceEvidence'];assert raw(C/n['rawContextPath'])==n['rawContextSHA256'] and n['claimGround'] and n['exactLocators'];assert sha(ad['literalTarget']['literal'])==ad['literalTarget']['canonicalSHA256'] and ad['literalTarget']['literal']==ad['currentCard']['answers'][2]['note']
for v in ad['fourVariantDependencies']:
 k=v['slot'];q=ad['currentCard'];tr={'prompt':q['prompt'],'answer':q['answers'][k]['text'],'note':q['answers'][k]['note']};assert v['fullPrompt']==tr['prompt'] and v['answer']==tr['answer'] and v['note']==tr['note'] and sha(tr)==v['tripleCanonicalSHA256'] and v['variantTruthAndUsefulness'] and v['sourceDependency']
ag={(e['id'],e['group']):e for e in a['finalGroupBindings']};av={(e['id'],e['slot']):e for e in a['finalVariantBindings']};accepted=[]
for e in r['entries']:
 i=e['id'];q=catalog[i];assert e['currentCard']==q and sha(q)==e['currentCardCanonicalSHA256'];assert len(e['sixLiteralCanonicalGroups'])==6 and len(e['fourFullPromptAnswerNoteVariants'])==4
 gs={'prompt_ordered_answers_key':{'prompt':q['prompt'],'answers':[v['text'] for v in q['answers']],'correctIndex':q['correctIndex']},'explanation':q['explanation'],**{'note'+str(k):v['note'] for k,v in enumerate(q['answers'])}}
 for g in e['sixLiteralCanonicalGroups']:assert g['literal']==gs[g['group']]==ag[i,g['group']]['literal'] and sha(g['literal'])==g['canonicalSHA256']==ag[i,g['group']]['literalSHA256'] and g['individualGround'] and g['sourcesLocators']
 for v in e['fourFullPromptAnswerNoteVariants']:
  k=v['slot'];tr={'prompt':q['prompt'],'answer':q['answers'][k]['text'],'note':q['answers'][k]['note']};assert {x:v[x] for x in tr}==tr and sha(tr)==v['tripleCanonicalSHA256']==av[i,k]['bindingCanonicalSHA256'];assert all(v[x] for x in ['grammar','plausibility','truthUniqueKey','noteTruthUsefulness','sourcesLocators'])
 if e['status']=='PASS':
  assert e['sourceOrder'] in [1,7,9] and not e['defects'];accepted.append({'questionId':i,'cardCanonicalSha256':sha(q),'authorNativeId':a['author'],'authorReceipt':a['authorPacket']+'/sourceproof.json','authorFreeze':'d79af6ba3ebfc8d42d504a63700dee6bc212e286','sourceProofCompletion':str(addp.relative_to(C)) if e['sourceOrder']==7 else None,'readerNativeId':r['reader'],'independentReceipt':str(rp.relative_to(C)),'readerReceiptRawSHA256':raw(rp),'coordinatorDecision':'Accept exactFINAL PASS aftersolecycle1. SOURCE andindependent whole6/4 currentbindings match, LoCEpub gap personallycompletedbySOURCE+OTHER withouttextchange. FINALHOLD4/5 excluded, sourceHOLD3/6 excluded. Unappliedbook11–20 future MAINversions must be freshlycompared beforetheirapply/credit.'})
assert len(accepted)==3
report={'scope':'books original10 solecycle1 ready5 FINAL PASS3 HOLD2','acceptedOrders':[1,7,9],'terminalFINALHOLDOrders':[4,5],'retainedSOURCEHOLDOrders':[3,6],'genuineNewSourceFor3PendingSeparate':True,'qualityBasis':'SOURCEfullgrounded6/4 + independentFINALexactCURRENT PASS, requiredaffected19 androotbinding. SOURCE7 proofgap completedpersonally on officialLoCprimary preserved; noautomaticsecondcycle. Canonicalwrongnotesallowed.','verified':{'currentCards':5,'literalGroups':30,'wholeVariants':20,'currentPeers':len(peers['actualCurrentPeers']),'sourceEPUBCompletionBound':True,'oldINITIALReceiptPreserved':raw(C/r['INITIALHistoryPath'])==r['INITIALHistoryRawSHA256']},'QA':{'path':str((D/'qa-books5-cycle1.json').relative_to(C)),'pass':19,'fail':0,'pending':0,'testedCatalogCommit':'963cf73eb152ec9e2cc739aaba70d1f4b67d2d2e'},'simultaneousProposals':'Reader preserved exact11–14 v1 NOTCURRENT; SOURCE final11–20 versions awaitingcrosscatalogqualification. Beforeapply11–20 freshOTHER mustcompare theiractualproposals withnowCURRENT5. Nochangedfutureproposalqualitycredit.','actualCompactionAudit':{'root':1,'SOURCE':0,'OTHER':0,'method':'Actual nativejournals active+archived uniquelyfound; unavailable notzero'}}
files=[p for p in R.rglob('*') if p.is_file()]+[addp,pathlib.Path(__file__)];cc=m.certify(accepted,report,731,8,D/'certification-books5-final-pass3-hold2.json',files,'963cf73eb152ec9e2cc739aaba70d1f4b67d2d2e')
with m.flow.locked():m.flow.lease('acquire','planning',O)
try:
 sp=P/'evidence/question-revision-process-v2/coordinator-state.json';st=rd(sp);st['coordinatorProgress'].update(CURRENT=734,newlyCertified=27,remaining=1266);st['waveCURRENT']=[500,198,36,0];wr(sp,st)
 gp=P/'evidence/question-revision-process-v2/active-full2000-goal-01a13f31.json';g=rd(gp);g.update(CURRENT=734,remaining=1266,waveCURRENT=[500,198,36,0],latestCodeCommit=cc,latestCertification=str((D/'certification-books5-final-pass3-hold2.json').relative_to(C)));wr(gp,g)
 print('goalplanning',m.h.save(P,'refs/heads/codex/question-revision-resume-20261014',[str(p.relative_to(P)) for p in [sp,gp]],'Update fullgoal CURRENT734 remaining1266 rootdelta27; retainbookFINALHOLD4/5',raw(P/m.h.git(P,'rev-parse','--git-path','index'))))
finally:
 with m.flow.locked():m.flow.lease('release','planning',O)
