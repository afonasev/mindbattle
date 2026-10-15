"""Bind mixed INITIAL10/FINAL3 existing independent wholeCURRENT11; accept7 only."""
import pathlib,json,hashlib,importlib.util,subprocess
C=pathlib.Path(__file__).resolve().parents[4];D=pathlib.Path(__file__).parent;P=pathlib.Path('/Users/eaafonasev/Projects/mindbattle/planning');O='01a13f31-9224-7dd1-90e0-e5b0ea2e94a9'
def rd(p):return json.loads(pathlib.Path(p).read_text())
def sha(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def raw(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def wr(p,j):pathlib.Path(p).write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
s=importlib.util.spec_from_file_location('m',D/'certification-common-relocated.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.O=O
R=D/'independent-books11-combined';rp=R/'receipt.json';r=rd(rp);sources=rd(R/'sources.json');peers=rd(R/'peers.json');qa=rd(D/'qa-books11-combined.json');idx=rd(D/'books11-combined-current-source-index.json');aa=[rd(D/'apply-books10-initial.json'),rd(D/'apply-books3-newprimary.json')]
assert len(r['entries'])==11 and qa['numPassedTests']==19 and qa['numFailedTests']==qa['numPendingTests']==0 and raw(D/'books11-combined-current-source-index.json')==r['sourceIndexRawSHA256']
assert (C/'src/content/topics/books-publishing.json').read_bytes()==subprocess.check_output(['git','-C',str(C),'show',idx['testedCatalogCommit']+':src/content/topics/books-publishing.json'])
catalog={}
for t in {p['topicId'] for p in peers['actualCurrentPeers']}:catalog.update({q['id']:q for q in rd(C/f'src/content/topics/{t}.json')['questions']})
for p in peers['actualCurrentPeers']:assert p['card']==catalog[p['id']] and sha(p['card'])==p['canonicalSHA256']
for p in peers['all11AppliedProposedFullCards']:assert p['card']==catalog[p['id']] and sha(p['card'])==p['canonicalSHA256']
for s in sources['primaryReadEvidence']:assert raw(s['path'])==s['rawReadSHA256'] and s['personalReadEvidence'] and s['locator']
for s in sources['originalSOURCETransportIntegrity']:assert raw(C/s['path'])==s['sha256']
ag={(e['id'],e['group']):e for a in aa for e in a['finalGroupBindings']};av={(e['id'],e['slot']):e for a in aa for e in a['finalVariantBindings']};am={e['id']:a for a in aa for e in a['applied']};accepted=[]
for e in r['entries']:
 i=e['id'];q=catalog[i];assert e['currentCard']==q and sha(q)==e['currentCardCanonicalSHA256'];assert len(e['sixLiteralCanonicalGroups'])==6 and len(e['fourFullPromptAnswerNoteVariants'])==4
 gs={'prompt_ordered_answers_key':{'prompt':q['prompt'],'answers':[v['text'] for v in q['answers']],'correctIndex':q['correctIndex']},'explanation':q['explanation'],**{'note'+str(k):v['note'] for k,v in enumerate(q['answers'])}}
 for g in e['sixLiteralCanonicalGroups']:assert g['literal']==gs[g['group']]==ag[i,g['group']]['literal'] and sha(g['literal'])==g['canonicalSHA256']==ag[i,g['group']]['literalSHA256'] and g['individualGround'] and g['sourcesLocators']
 for v in e['fourFullPromptAnswerNoteVariants']:
  k=v['slot'];tr={'prompt':q['prompt'],'answer':q['answers'][k]['text'],'note':q['answers'][k]['note']};assert {x:v[x] for x in tr}==tr and sha(tr)==v['tripleCanonicalSHA256']==av[i,k]['bindingCanonicalSHA256'];assert all(v[x] for x in ['grammar','plausibility','truthUniqueKey','noteTruthUsefulness','sourcesLocators'])
 assert e['absoluteLevel'] and e['correctNoteExtraFact']
 if e['status']=='PASS':
  assert e['sourceOrder'] in [3,11,13,14,16,19,20] and not e['defects'];a=am[i];accepted.append({'questionId':i,'cardCanonicalSha256':sha(q),'authorNativeId':a['author'],'authorReceipt':a['authorPacket']+'/sourceproof.json','authorFreeze':'d1bbc362d220a2d0b41ba6c7451e60a5f3015d60' if e['sourceOrder']==3 else '8abd6a3918dd48913d529801981ced9829c20c8b','readerNativeId':r['reader'],'independentReceipt':str(rp.relative_to(C)),'readerReceiptRawSHA256':raw(rp),'coordinatorDecision':'Accept exact'+e['stage']+' PASS. SOURCE6/4/appliedCURRENT/independent66groups44variants andcurrent108peers bound. Personalfullrelevantprimarycontexts independentlyread, mutableSOURCEversions explicit. FINAL3 onconcretenewprimary notunchangedautomaticcycle. INITIALFIX12/15/17/18 excluded.'})
assert len(accepted)==7
report={'scope':'Books CURRENT11 mixedINITIAL10 andFINALgenuinenewprimary3','acceptedOrders':[3,11,13,14,16,19,20],'directedCycle1Orders':[12,15,17,18],'qualityBasis':'Substantive SOURCE+independent exactCURRENT PASS withfullprimarymeaning/conditions, all6/4literalbindings andactual+proposedMAINpairs; affected19 androotbinding. NotQA/metadata/source-downloadcredit. Canonicalwrongnotefactpoolallowed.','verified':{'currentCards':11,'literalGroups':66,'wholeVariants':44,'currentPeers':len(peers['actualCurrentPeers']),'bilateralMAINComparisons':len(peers['actualBilateralMAINComparisons']),'proposedPairs':len(peers['all11ProposedPairComparisons']),'primaryLiveOutputFiles':3,'originalSOURCEHashBindings':len(sources['originalSOURCETransportIntegrity']),'source3AuthorBothSidesCurrentIdentity':all(p['literalEqual'] for p in peers['source3AuthorBothSidesActualIdentityCheck'])},'QA':{'path':str((D/'qa-books11-combined.json').relative_to(C)),'pass':19,'fail':0,'pending':0,'testedCatalogCommit':idx['testedCatalogCommit']},'actualCompactionAudit':{'root':1,'SOURCE10':1,'SOURCE3':1,'OTHER':0,'method':'Actual uniquelyfoundjournals active+archived; SOURCE3 firstevent occurredafterstageatparkcompletion, stageitself0. Missingnotzero.'},'noFullTestsRuntimeBuildMainDeployHumanAcceptance':True}
files=[p for p in R.rglob('*') if p.is_file()]+[pathlib.Path(__file__)];cc=m.certify(accepted,report,734,8,D/'certification-books11-combined-pass7-fix4.json',files,'32064b5f6a55e5bc22d8d9778825b1843d406838')
with m.flow.locked():m.flow.lease('acquire','planning',O)
try:
 sp=P/'evidence/question-revision-process-v2/coordinator-state.json';st=rd(sp);st['coordinatorProgress'].update(CURRENT=741,newlyCertified=34,remaining=1259);st['waveCURRENT']=[500,198,43,0];wr(sp,st)
 gp=P/'evidence/question-revision-process-v2/active-full2000-goal-01a13f31.json';g=rd(gp);g.update(CURRENT=741,remaining=1259,waveCURRENT=[500,198,43,0],latestCodeCommit=cc,latestCertification=str((D/'certification-books11-combined-pass7-fix4.json').relative_to(C)));wr(gp,g)
 print('goalplanning',m.h.save(P,'refs/heads/codex/question-revision-resume-20261014',[str(p.relative_to(P)) for p in [sp,gp]],'Update fullgoal CURRENT741 remaining1259 rootdelta34; directedINITIALfix4 pending',raw(P/m.h.git(P,'rev-parse','--git-path','index'))))
finally:
 with m.flow.locked():m.flow.lease('release','planning',O)
