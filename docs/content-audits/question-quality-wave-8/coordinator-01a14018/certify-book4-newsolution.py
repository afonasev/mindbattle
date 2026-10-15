"""Bind independent exact INITIAL PASS for genuine new function route."""
import pathlib,json,hashlib,importlib.util,subprocess
C=pathlib.Path(__file__).resolve().parents[4];D=pathlib.Path(__file__).parent
P=pathlib.Path('/Users/eaafonasev/Projects/mindbattle/planning');O='01a14018-7b8d-7301-ad28-95ee8d812e97'
def rd(p):return json.loads(pathlib.Path(p).read_text())
def sha(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def raw(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def wr(p,d):pathlib.Path(p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('cert',D/'certification-common.py');m.O=O;m.P=P
guard=load('guard',D.parent/'coordinator-01a13f31/planning-certification-guard.py')
R=D/'independent-book4-newsolution-initial';rp=R/'receipt.json';r=rd(rp);ver=rd(R/'verification.json');peers=rd(R/'peers.json');sources=rd(R/'sources.json');a=rd(D/'apply-book4-newsolution.json');qaPath=D/'qa-book4-newsolution.json';qa=rd(qaPath)
assert len(r['entries'])==1 and qa['success'] and qa['numPassedTests']==19 and qa['numFailedTests']==qa['numPendingTests']==0
assert raw(qaPath)==ver['existingQA19']['rawSHA256']
tp=C/'src/content/topics/books-publishing.json';qaCommit='039bb7f76b7d1fff02d8b61baec03a77cdcb3ee1'
assert raw(tp)==ver['catalogRawSHA256'] and tp.read_bytes()==subprocess.check_output(['git','-C',str(C),'show',qaCommit+':src/content/topics/books-publishing.json'])
cat={}
for t in {p['topicId'] for p in peers['actualCurrentPeers']}:cat.update({q['id']:q for q in rd(C/f'src/content/topics/{t}.json')['questions']})
for p in peers['actualCurrentPeers']:assert p['card']==cat[p['id']] and sha(p['card'])==p['sha256']
for pair in peers['bilateralMainComparisons']:
 assert pair['leftToRight'] and pair['rightToLeft']
 for side in ['left','right']:
  p=pair[side];assert p['card']==cat[p['id']] and sha(p['card'])==p['sha256']
for s in sources['sources']:assert raw(C/s['path'])==s['rawReadSHA256'] and s['personalReadEvidence'] and s['locator']
e=r['entries'][0];i=e['id'];q=cat[i];assert i=='books-publishing-endpaper-part' and e['stage']=='INITIAL' and e['status']=='PASS' and not e['defects']
assert q==e['currentCard'] and sha(q)==e['currentCardCanonicalSHA256']
ag={g['group']:g for g in a['finalGroupBindings']};av={v['slot']:v for v in a['finalVariantBindings']}
assert len(e['sixLiteralCanonicalGroups'])==6 and len(e['fourFullPromptAnswerNoteVariants'])==4
gs={'prompt_ordered_answers_key':{'prompt':q['prompt'],'answers':[v['text'] for v in q['answers']],'correctIndex':q['correctIndex']},'explanation':q['explanation'],**{'note'+str(k):v['note'] for k,v in enumerate(q['answers'])}}
for g in e['sixLiteralCanonicalGroups']:
 assert g['literal']==gs[g['group']]==ag[g['group']]['literal'] and sha(g['literal'])==g['canonicalSHA256']==ag[g['group']]['literalSHA256']
 assert g['individualGround'] and g['sourcesLocators']
for v in e['fourFullPromptAnswerNoteVariants']:
 k=v['slot'];tr={'prompt':q['prompt'],'answer':q['answers'][k]['text'],'note':q['answers'][k]['note']}
 assert {x:v[x] for x in tr}==tr and sha(tr)==v['tripleCanonicalSHA256']==av[k]['bindingCanonicalSHA256']
 assert all(v[x] for x in ['grammar','plausibility','truthUniqueKey','noteTruthUsefulness','sourcesLocators'])
accepted=[{'questionId':i,'cardCanonicalSha256':sha(q),'authorNativeId':a['author'],'authorReceipt':a['authorPacket']+'/sourceproof.json','authorFreeze':'36cf1f6bfac11ad4a66da958ff5b7eb2bac444d7','readerNativeId':'01a14007-6729-7142-a4c8-4b0d3c8627c5','independentReceipt':str(rp.relative_to(C)),'readerReceiptRawSHA256':raw(rp),'coordinatorDecision':'Accept exact INITIAL PASS for genuine new function route after prior term-route terminal HOLD, which remains historical. SOURCE repaired swapped proof bindings; independent personally read complete relevant CIEP/Bodleian/PeaceCorps, assessed full6/4/EASY/ownextra/plausibility and20bilateralMAIN143CURRENTpeers. Required19 exact catalog unchanged. No quality credit from previous HOLD or metadata.'}]
report={'scope':'book4 genuine new function solution INITIAL PASS1','acceptedOrders':[4],'qualityBasis':'Substantive SOURCE and exactCURRENT independent INITIAL PASS, root actual bindings and affected19. Prior term-route terminal HOLD retained; new concrete function solution qualified independently.','verified':{'currentCards':1,'literalGroups':6,'wholeVariants':4,'actualPeers':len(peers['actualCurrentPeers']),'bilateralMainPairs':len(peers['bilateralMainComparisons'])},'QA':{'path':str(qaPath.relative_to(C)),'pass':19,'fail':0,'pending':0,'testedCatalogCommit':qaCommit,'reportCommit':'36cf1f6bfac11ad4a66da958ff5b7eb2bac444d7'},'preleaseGuard':True,'ownIntakeCURRENT':754,'actualCompactionAudit':{'root':0,'SOURCE':0,'OTHER':0,'missingNotZero':True}}
cc=guard.certify_preleased(m,accepted,report,756,8,D/'certification-book4-newsolution-initial-pass1.json',[p for p in R.iterdir() if p.is_file()]+[pathlib.Path(__file__)],qaCommit)
with m.flow.locked():m.flow.lease('acquire','planning',O)
try:
 sp=P/'evidence/question-revision-process-v2/coordinator-state.json';st=rd(sp);st['waveCURRENT']=[500,198,59,0];st['pendingBook4NewSolution'].update(status='CERTIFIED_CURRENT',qualityCredit=1,codeCommit=cc);st['currentNativeActors']['OTHER'].update(status='IDLE retained book4 INITIALcertified',cursor='589f93ab-4337-4d86-a1a0-de433fa8df3b:14');st['currentWork'].update(independentActive=0,readyCurrentQueue=0,next='Preserve/archive completed SOURCEbook4 and dispatch nextbooks51-70 when SOURCEcapacity; originalSOURCE31-50 completion active.');wr(sp,st)
 gp=P/'evidence/question-revision-process-v2/active-full2000-goal-01a14018.json';g=rd(gp);g.update(CURRENT=757,remaining=1243,newlyCertified=3,waveCURRENT=[500,198,59,0],latestCodeCommit=cc,latestCertification=str((D/'certification-book4-newsolution-initial-pass1.json').relative_to(C)));wr(gp,g)
 print('projection',m.h.save(P,'refs/heads/codex/question-revision-resume-20261014',[str(p.relative_to(P)) for p in [sp,gp]],'Record fullgoal CURRENT757 delta3; genuine new function source/INITIAL complete',raw(P/m.h.git(P,'rev-parse','--git-path','index'))))
finally:
 with m.flow.locked():m.flow.lease('release','planning',O)
