"""Bind independent parks INITIAL2; credit exact PASS003 only."""
import pathlib,json,hashlib,importlib.util,subprocess
C=pathlib.Path(__file__).resolve().parents[4];D=pathlib.Path(__file__).parent;P=pathlib.Path('/Users/eaafonasev/Projects/mindbattle/planning');O='01a13f31-9224-7dd1-90e0-e5b0ea2e94a9'
def rd(p):return json.loads(pathlib.Path(p).read_text())
def sha(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def raw(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def wr(p,v):pathlib.Path(p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
s=importlib.util.spec_from_file_location('cert',D/'certification-common-relocated.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.O=O
R=D/'independent-parks2-initial';rp=R/'receipt.json';r=rd(rp);sources=rd(R/'sources.json');peers=rd(R/'peers.json');a=rd(D/'apply-parks2-initial.json');qa=rd(D/'qa-parks2-initial.json')
assert len(r['entries'])==2 and qa['numPassedTests']==19 and qa['numFailedTests']==qa['numPendingTests']==0
assert (C/'src/content/topics/national-parks-nature.json').read_bytes()==subprocess.check_output(['git','-C',str(C),'show','5b41b79e9a6490cbb2584c7ffa276edc66560612:src/content/topics/national-parks-nature.json'])
pp=peers['actualCurrentPeers']+peers['additionalActualCrossCatalogPeers'];catalog={}
for t in {p['topicId'] for p in pp}:catalog.update({q['id']:q for q in rd(C/f'src/content/topics/{t}.json')['questions']})
for p in pp:assert p['card']==catalog[p['id']] and sha(p['card'])==p['canonicalSHA256']
for s in sources['entries']:assert raw(s['path'])==s['rawReadSHA256'] and s['personalReadEvidence'] and s['locator']
ag={(e['id'],e['group']):e for e in a['finalGroupBindings']};av={(e['id'],e['slot']):e for e in a['finalVariantBindings']};accepted=[]
for e in r['entries']:
 i=e['id'];q=catalog[i];assert e['currentCard']==q and sha(q)==e['currentCardCanonicalSHA256'];assert len(e['sixLiteralCanonicalGroups'])==6 and len(e['fourFullPromptAnswerNoteVariants'])==4
 gs={'prompt_ordered_answers_key':{'prompt':q['prompt'],'answers':[v['text'] for v in q['answers']],'correctIndex':q['correctIndex']},'explanation':q['explanation'],**{'note'+str(k):v['note'] for k,v in enumerate(q['answers'])}}
 for g in e['sixLiteralCanonicalGroups']:assert g['literal']==gs[g['group']]==ag[i,g['group']]['literal'] and sha(g['literal'])==g['canonicalSHA256']==ag[i,g['group']]['literalSHA256'] and g['individualGround'] and g['sourcesLocators']
 for v in e['fourFullPromptAnswerNoteVariants']:
  k=v['slot'];tr={'prompt':q['prompt'],'answer':q['answers'][k]['text'],'note':q['answers'][k]['note']};assert {x:v[x] for x in tr}==tr and sha(tr)==v['tripleCanonicalSHA256']==av[i,k]['bindingCanonicalSHA256'];assert all(v[x] for x in ['grammar','plausibility','truthUniqueKey','noteTruthUsefulness','sourcesLocators'])
 if e['status']=='PASS':
  assert i=='national-parks-nature-003' and not e['defects'];accepted.append({'questionId':i,'cardCanonicalSha256':sha(q),'authorNativeId':a['author'],'authorReceipt':a['authorPacket']+'/sourceproof.json','authorFreeze':'8f623e96d719108624b7b7c6032d9f8ca8efde5e','readerNativeId':r['reader'],'independentReceipt':str(rp.relative_to(C)),'readerReceiptRawSHA256':raw(rp),'coordinatorDecision':'Accept exactINITIAL003 PASS with SOURCE sixgroups/fourvariants, personalNPS contexts/current119peerbindings. INITIAL001 FIXfrozenEASY excluded pendingsolecycle1; no countfromQA/sourceholds.'})
assert len(accepted)==1
report={'scope':'national-parks-nature INITIAL2 PASS003 FIX001','acceptedOrders':[3],'directedCycle1Orders':[1],'qualityBasis':'Substantive SOURCE+independent exactCURRENT PASS bound byroot; canonical factpool allowed; source/current/all6and4 match. NotQAorstructurecredit.','verified':{'currentCards':2,'literalGroups':12,'wholeVariants':8,'sourcePages':6,'currentPeers':len(pp),'mainComparisons':len(peers['bilateralMAINComparisons'])},'QA':{'path':str((D/'qa-parks2-initial.json').relative_to(C)),'pass':19,'fail':0,'pending':0,'testedCatalogCommit':'5b41b79e9a6490cbb2584c7ffa276edc66560612','preapplyInvalidQAExcluded':True},'actualCompactionAudit':{'root':1,'SOURCE':1,'OTHER':0,'method':'Actual native compacted events active+archived uniquejournals; missing notzero'}}
files=[p for p in R.rglob('*') if p.is_file()]+[pathlib.Path(__file__)];cc=m.certify(accepted,report,730,8,D/'certification-parks2-initial-pass1-fix1.json',files,'5b41b79e9a6490cbb2584c7ffa276edc66560612')
with m.flow.locked():m.flow.lease('acquire','planning',O)
try:
 sp=P/'evidence/question-revision-process-v2/coordinator-state.json';st=rd(sp);st['coordinatorProgress'].update(CURRENT=731,newlyCertified=24,remaining=1269);st['waveCURRENT']=[500,198,33,0];wr(sp,st)
 gp=P/'evidence/question-revision-process-v2/active-full2000-goal-01a13f31.json';g=rd(gp);g.update(CURRENT=731,remaining=1269,waveCURRENT=[500,198,33,0],latestCodeCommit=cc,latestCertification=str((D/'certification-parks2-initial-pass1-fix1.json').relative_to(C)));wr(gp,g)
 print('goalplanning',m.h.save(P,'refs/heads/codex/question-revision-resume-20261014',[str(p.relative_to(P)) for p in [sp,gp]],'Update fullgoal CURRENT731 remaining1269 rootdelta24',raw(P/m.h.git(P,'rev-parse','--git-path','index'))))
finally:
 with m.flow.locked():m.flow.lease('release','planning',O)
