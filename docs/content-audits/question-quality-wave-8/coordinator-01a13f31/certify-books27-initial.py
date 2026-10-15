"""Bind fresh independent INITIAL27 after originalSOURCE completion, credit1."""
import pathlib,json,hashlib,importlib.util,subprocess
C=pathlib.Path(__file__).resolve().parents[4];D=pathlib.Path(__file__).parent;P=pathlib.Path('/Users/eaafonasev/Projects/mindbattle/planning');O='01a13f31-9224-7dd1-90e0-e5b0ea2e94a9'
def rd(p):return json.loads(pathlib.Path(p).read_text())
def sha(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def raw(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def wr(p,j):pathlib.Path(p).write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('m',D/'certification-common-relocated.py');m.O=O;guard=load('guard',D/'planning-certification-guard.py')
R=D/'independent-books27-initial';rp=R/'receipt.json';r=rd(rp);src=rd(R/'sources.json');peers=rd(R/'peers.json');ver=rd(R/'verification.json');a=rd(D/'apply-books27-initial-completion.json');qa=rd(D/'qa-books27-initial-completion.json');assert len(r['entries'])==1 and qa['numPassedTests']==19 and qa['numFailedTests']==qa['numPendingTests']==0
tp=C/'src/content/topics/books-publishing.json';assert raw(tp)==ver['catalogRawSHA256'];assert tp.read_bytes()==subprocess.check_output(['git','-C',str(C),'show','9352f63b4fd3deb2716e0facbaaae1828b62b78d:src/content/topics/books-publishing.json'])
cat={}
for t in {p['topicId'] for p in peers['actualCurrentPeers']}:cat.update({q['id']:q for q in rd(C/f'src/content/topics/{t}.json')['questions']})
for p in peers['actualCurrentPeers']:assert p['card']==cat[p['id']] and sha(p['card'])==p['sha256']
for s in src['sources']:assert raw(C/s['path'])==s['rawReadSHA256'] and s['personalReadEvidence'] and s['locator']
e=r['entries'][0];i=e['id'];q=cat[i];assert i=='books-publishing-typesetter-role' and e['stage']=='INITIAL' and e['status']=='PASS' and not e['defects'];assert e['currentCard']==q and sha(q)==e['currentCardCanonicalSHA256'];ag={g['group']:g for g in a['finalGroupBindings']};av={v['slot']:v for v in a['finalVariantBindings']};assert len(e['sixLiteralCanonicalGroups'])==6 and len(e['fourFullPromptAnswerNoteVariants'])==4
gs={'prompt_ordered_answers_key':{'prompt':q['prompt'],'answers':[v['text'] for v in q['answers']],'correctIndex':q['correctIndex']},'explanation':q['explanation'],**{'note'+str(k):v['note'] for k,v in enumerate(q['answers'])}}
for g in e['sixLiteralCanonicalGroups']:assert g['literal']==gs[g['group']]==ag[g['group']]['literal'] and sha(g['literal'])==g['canonicalSHA256']==ag[g['group']]['literalSHA256'] and g['individualGround'] and g['sourcesLocators']
for v in e['fourFullPromptAnswerNoteVariants']:
 k=v['slot'];tr={'prompt':q['prompt'],'answer':q['answers'][k]['text'],'note':q['answers'][k]['note']};assert {x:v[x] for x in tr}==tr and sha(tr)==v['tripleCanonicalSHA256']==av[k]['bindingCanonicalSHA256'];assert all(v[x] for x in ['grammar','plausibility','truthUniqueKey','noteTruthUsefulness','sourcesLocators'])
accepted=[{'questionId':i,'cardCanonicalSha256':sha(q),'authorNativeId':a['author'],'authorReceipt':a['authorPacket']+'/sourceproof.json','authorFreeze':'5b639276914b141555f70b11f3bd0ff0bb141c3e','readerNativeId':'01a14007-6729-7142-a4c8-4b0d3c8627c5','independentReceipt':str(rp.relative_to(C)),'readerReceiptRawSHA256':raw(rp),'coordinatorDecision':'Accept freshexactINITIAL PASS. PriorSOURCEHOLDtermtypesetterreplacedgenuinepracticalgutterproblemwithSOURCEfullKDPprimary6/4; independentpersonallyreadandjudgedEASY/onekey/ownextra/current201peers, wholebookQAidentityrootverified. No countfrommetadataalone.'}]
report={'scope':'books27 INITIAL originalSOURCEcompletion','acceptedOrders':[27],'qualityBasis':'SOURCE+freshindependent wholeCURRENT PRIMARY/editorialPASS, literal6/fullvariant4andactual/proposedMAINbindings, targetandWHOLEbookQAidentityverified. Sourceauthorfirstcompclosedoriginal10; newOTHER0review.','verified':{'currentCards':1,'literalGroups':6,'wholeVariants':4,'actualPeers':len(peers['actualCurrentPeers']),'bilateralMainPairs':len(peers['bilateralMainComparisons'])},'QA':{'path':str((D/'qa-books27-initial-completion.json').relative_to(C)),'pass':19,'fail':0,'pending':0,'testedCatalogCommit':'9352f63b4fd3deb2716e0facbaaae1828b62b78d'},'preleaseGuard':True,'actualCompactionAudit':{'root':1,'SOURCE':1,'OTHER':'freshfirstslice; auditbeforefurtherwork','missingNotZero':True}}
files=[p for p in R.rglob('*') if p.is_file()]+[pathlib.Path(__file__)];cc=guard.certify_preleased(m,accepted,report,753,8,D/'certification-books27-initial-pass1.json',files,'9352f63b4fd3deb2716e0facbaaae1828b62b78d')
with m.flow.locked():m.flow.lease('acquire','planning',O)
try:
 sp=P/'evidence/question-revision-process-v2/coordinator-state.json';st=rd(sp);st['coordinatorProgress'].update(CURRENT=754,newlyCertified=47,remaining=1246);st['waveCURRENT']=[500,198,56,0];wr(sp,st)
 gp=P/'evidence/question-revision-process-v2/active-full2000-goal-01a13f31.json';g=rd(gp);g.update(CURRENT=754,remaining=1246,waveCURRENT=[500,198,56,0],latestCodeCommit=cc,latestCertification=str((D/'certification-books27-initial-pass1.json').relative_to(C)));wr(gp,g)
 print('goalplanning',m.h.save(P,'refs/heads/codex/question-revision-resume-20261014',[str(p.relative_to(P)) for p in [sp,gp]],'Update fullgoal CURRENT754 remaining1246 rootdelta47; SOURCEoriginal27closed',raw(P/m.h.git(P,'rev-parse','--git-path','index'))))
finally:
 with m.flow.locked():m.flow.lease('release','planning',O)
