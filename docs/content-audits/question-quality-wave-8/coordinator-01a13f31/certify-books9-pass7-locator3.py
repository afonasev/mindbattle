"""Bind independent INITIAL9 PASS7 with personally completed SOURCE locator3 repair."""
import pathlib,json,hashlib,importlib.util,subprocess
C=pathlib.Path(__file__).resolve().parents[4];D=pathlib.Path(__file__).parent;P=pathlib.Path('/Users/eaafonasev/Projects/mindbattle/planning');O='01a13f31-9224-7dd1-90e0-e5b0ea2e94a9'
def rd(p):return json.loads(pathlib.Path(p).read_text())
def sha(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def raw(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def wr(p,j):pathlib.Path(p).write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('m',D/'certification-common-relocated.py');m.O=O;guard=load('guard',D/'planning-certification-guard.py')
R=D/'independent-books9-initial-21-30';rp=R/'receipt.json';r=rd(rp);peers=rd(R/'peers.json');sources=rd(R/'sources.json');ver=rd(R/'verification.json');a=rd(D/'apply-books9-initial-21-30.json');qa=rd(D/'qa-books27-initial-completion.json');A=C/'docs/content-audits/question-quality-wave-8/process-v2-books26-28-cycle1-and-locator3-01a13f31/author';metaP=A/'source9-locator-repair.json';meta=rd(metaP)
assert len(r['entries'])==9 and qa['numPassedTests']==19 and qa['numFailedTests']==qa['numPendingTests']==0
topic=C/'src/content/topics/books-publishing.json';assert raw(topic)==ver['wholeCurrentTopic']['rawSHA256'];assert topic.read_bytes()==subprocess.check_output(['git','-C',str(C),'show','9352f63b4fd3deb2716e0facbaaae1828b62b78d:src/content/topics/books-publishing.json'])
catalog={}
for t in {p['topicId'] for p in peers['actualCurrentPeers']}:catalog.update({q['id']:q for q in rd(C/f'src/content/topics/{t}.json')['questions']})
for p in peers['actualCurrentPeers']:assert p['card']==catalog[p['id']] and sha(p['card'])==p['sha256']
for s in sources['rawSources']:assert raw(C/s['path'])==s['sha256'] and s['independentUse']
assert {e['sourceOrder'] for e in meta['entries']}=={22,23,30}
for e in meta['entries']:
 q=catalog[e['id']];k=e['slot'];assert e['status']=='SUPPORTED' and not e['cardTextChanged'] and sha(q)==e['currentCardCanonicalSHA256'];assert e['fieldGroup']=='note'+str(k) and e['literal']==q['answers'][k]['note']==e['note'] and sha(e['literal'])==e['literalCanonicalSHA256'];tr={'prompt':q['prompt'],'answer':q['answers'][k]['text'],'note':q['answers'][k]['note']};assert e['fullPrompt']==tr['prompt'] and e['answer']==tr['answer'] and sha(tr)==e['tripleCanonicalSHA256'];assert all(e[k] for k in ['exactLocator','concreteClaimGround','personalReadEvidence','conditions'])
 for p,dig in zip(e['newSourcePaths'],e['newRawSHA256']):assert raw(C/p)==dig
# Same original SOURCE author personally completed all changed4 and new27 MAIN dependencies.
S=C/'docs/content-audits/question-quality-wave-8/process-v2-books21-30-01a13f31/author/source27-completion'
for fn in ['same-original-source9-peer-refresh-after-fix4.json','newtwo-peer15-18-completion.json']:
 for e in rd(S/fn)['actualCurrentCards']:assert e['card']==catalog[e['id']] and sha(e['card'])==e['sha256']
ag={(e['id'],e['group']):e for e in a['finalGroupBindings']};av={(e['id'],e['slot']):e for e in a['finalVariantBindings']};accepted=[]
for e in r['entries']:
 i=e['id'];q=catalog[i];assert e['currentCard']==q and sha(q)==e['currentCardCanonicalSHA256'];assert len(e['sixLiteralCanonicalGroups'])==6 and len(e['fourFullPromptAnswerNoteVariants'])==4
 gs={'prompt_ordered_answers_key':{'prompt':q['prompt'],'answers':[v['text'] for v in q['answers']],'correctIndex':q['correctIndex']},'explanation':q['explanation'],**{'note'+str(k):v['note'] for k,v in enumerate(q['answers'])}}
 for g in e['sixLiteralCanonicalGroups']:assert g['literal']==gs[g['group']]==ag[i,g['group']]['literal'] and sha(g['literal'])==g['canonicalSHA256']==ag[i,g['group']]['literalSHA256'] and g['individualGround'] and g['sourcesLocators']
 for v in e['fourFullPromptAnswerNoteVariants']:
  k=v['slot'];tr={'prompt':q['prompt'],'answer':q['answers'][k]['text'],'note':q['answers'][k]['note']};assert {x:v[x] for x in tr}==tr and sha(tr)==v['tripleCanonicalSHA256']==av[i,k]['bindingCanonicalSHA256'];assert all(v[x] for x in ['grammar','plausibility','truthUniqueKey','noteTruthUsefulness','sourcesLocators'])
 if e['status']=='PASS':
  assert e['sourceOrder'] in [21,22,23,24,25,29,30] and not e['defects'];accepted.append({'questionId':i,'cardCanonicalSha256':sha(q),'authorNativeId':a['author'],'authorReceipt':a['authorPacket']+'/sourceproof.json','authorFreeze':'29b50354779ce860cc5274c913c30427c08d07b7','SOURCEPeerCompletionFreeze':'5b639276914b141555f70b11f3bd0ff0bb141c3e','sourceLocatorCompletionAuthor':'01a13fc7-e37f-7822-9f37-2f69122dc2fe' if e['sourceOrder'] in [22,23,30] else None,'sourceLocatorCompletion':str(metaP.relative_to(C)) if e['sourceOrder'] in [22,23,30] else None,'readerNativeId':r['reviewerThread'],'independentReceipt':str(rp.relative_to(C)),'readerReceiptRawSHA256':raw(rp),'coordinatorDecision':'Accept exactINITIAL PASS; SOURCEcurrent6/4, personalPRIMARYandlocator3completion plus freshSOURCE/OTHERMAIN4+27delta allbound. TARGET9literalsunchangedafterpeerupdates, latestwholebookQA19read/verified. INITIALFIX26/28excluded. No countfromhashes/metadataalone.'})
assert len(accepted)==7
report={'scope':'books CURRENTINITIAL9 sourceOrders21–26/28–30 PASS7FIX2','acceptedOrders':[21,22,23,24,25,29,30],'directedCycle1Orders':[26,28],'qualityBasis':'SOURCE+independent full relevant primary meanings and conditions; sixliteral/fourwholevariant bindings +current135peers. Sourcecoauthor personallycorrectedexactlocatorroutes22/23/30 withouttextchange; no inheritedOTHERonlySOURCEclaim. Canonicalwrongnotepoolallowed.','verified':{'currentCards':9,'literalGroups':54,'wholeVariants':36,'currentPeers':len(peers['actualCurrentPeers']),'SOURCElocatorRepairs':3,'target9ExactAfterOnlyNeighbor4And27Changes':True,'latestWholeBookRawSHA256':raw(topic)},'QA':{'path':str((D/'qa-books27-initial-completion.json').relative_to(C)),'pass':19,'fail':0,'pending':0,'testedCatalogCommit':'9352f63b4fd3deb2716e0facbaaae1828b62b78d'},'preleaseGuard':'planning-certification-guard.py actualRealFlow4caseverificationPASS; acquiresBEFORECODEregistrywrite, neverstealsforeignlease','actualCompactionAudit':{'root':1,'SOURCEoriginal':1,'SOURCEcoauthor':'auditafterboundedcompletion','OTHER':1,'method':'Actualnativejournals active+archived uniquelyfound; missingnotzero. OTHERpreservedsliceandthenboundedoriginalFINAL4, nowarchived.'}}
files=[p for p in R.rglob('*') if p.is_file()]+[metaP,pathlib.Path(__file__)];cc=guard.certify_preleased(m,accepted,report,742,8,D/'certification-books9-pass7-locator3.json',files,'9352f63b4fd3deb2716e0facbaaae1828b62b78d')
with m.flow.locked():m.flow.lease('acquire','planning',O)
try:
 sp=P/'evidence/question-revision-process-v2/coordinator-state.json';st=rd(sp);st['coordinatorProgress'].update(CURRENT=749,newlyCertified=42,remaining=1251);st['waveCURRENT']=[500,198,51,0];wr(sp,st)
 gp=P/'evidence/question-revision-process-v2/active-full2000-goal-01a13f31.json';g=rd(gp);g.update(CURRENT=749,remaining=1251,waveCURRENT=[500,198,51,0],latestCodeCommit=cc,latestCertification=str((D/'certification-books9-pass7-locator3.json').relative_to(C)));wr(gp,g)
 print('goalplanning',m.h.save(P,'refs/heads/codex/question-revision-resume-20261014',[str(p.relative_to(P)) for p in [sp,gp]],'Update fullgoal CURRENT749 remaining1251 rootdelta42; sourceMETA3completed',raw(P/m.h.git(P,'rev-parse','--git-path','index'))))
finally:
 with m.flow.locked():m.flow.lease('release','planning',O)
