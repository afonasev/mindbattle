"""Bind independent exact FINAL001 aftersolecycle1; canonicalwrongnotefactreuse allowed."""
import pathlib,json,hashlib,importlib.util,subprocess
C=pathlib.Path(__file__).resolve().parents[4];D=pathlib.Path(__file__).parent;P=pathlib.Path('/Users/eaafonasev/Projects/mindbattle/planning');O='01a13f31-9224-7dd1-90e0-e5b0ea2e94a9'
def rd(p):return json.loads(pathlib.Path(p).read_text())
def sha(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def raw(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def wr(p,j):pathlib.Path(p).write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
s=importlib.util.spec_from_file_location('m',D/'certification-common-relocated.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.O=O
R=D/'independent-parks2-initial/final-cycle1-001';rp=R/'receipt.json';r=rd(rp);sources=rd(R/'sources.json');peers=rd(R/'peers.json');a=rd(D/'apply-parks001-cycle1.json');qa=rd(D/'qa-parks001-cycle1.json');assert len(r['entries'])==1 and qa['numPassedTests']==19 and qa['numFailedTests']==qa['numPendingTests']==0
assert (C/'src/content/topics/national-parks-nature.json').read_bytes()==subprocess.check_output(['git','-C',str(C),'show','979d4c0ec45ab67d9d3a8480735911e36ee0e15b:src/content/topics/national-parks-nature.json'])
catalog={}
for t in {p['topicId'] for p in peers['actualCurrentPeers']}:catalog.update({q['id']:q for q in rd(C/f'src/content/topics/{t}.json')['questions']})
for p in peers['actualCurrentPeers']:assert p['card']==catalog[p['id']] and sha(p['card'])==p['canonicalSHA256']
for s in sources['entries']:assert raw(s['path'])==s['rawReadSHA256'] and s['personalReadEvidence'] and s['locator']
e=r['entries'][0];i=e['id'];q=catalog[i];assert i=='national-parks-nature-001' and e['stage']=='FINAL' and e['status']=='PASS' and not e['defects'] and e['currentCard']==q and sha(q)==e['currentCardCanonicalSHA256'] and e['INITIALDefectResolution'];ag={g['group']:g for g in a['finalGroupBindings']};av={v['slot']:v for v in a['finalVariantBindings']};assert len(e['sixLiteralCanonicalGroups'])==6 and len(e['fourFullPromptAnswerNoteVariants'])==4
gs={'prompt_ordered_answers_key':{'prompt':q['prompt'],'answers':[v['text'] for v in q['answers']],'correctIndex':q['correctIndex']},'explanation':q['explanation'],**{'note'+str(k):v['note'] for k,v in enumerate(q['answers'])}}
for g in e['sixLiteralCanonicalGroups']:assert g['literal']==gs[g['group']]==ag[g['group']]['literal'] and sha(g['literal'])==g['canonicalSHA256']==ag[g['group']]['literalSHA256'] and g['individualGround'] and g['sourcesLocators']
for v in e['fourFullPromptAnswerNoteVariants']:
 k=v['slot'];tr={'prompt':q['prompt'],'answer':q['answers'][k]['text'],'note':q['answers'][k]['note']};assert {x:v[x] for x in tr}==tr and sha(tr)==v['tripleCanonicalSHA256']==av[k]['bindingCanonicalSHA256'];assert all(v[x] for x in ['grammar','plausibility','truthUniqueKey','noteTruthUsefulness','sourcesLocators'])
accepted=[{'questionId':i,'cardCanonicalSha256':sha(q),'authorNativeId':a['author'],'authorReceipt':a['authorPacket']+'/sourceproof.json','authorFreeze':'1c534e1dcb965b15e018ec0b9f926d98f73165f4','readerNativeId':r['reader'],'independentReceipt':str(rp.relative_to(C)),'readerReceiptRawSHA256':raw(rp),'coordinatorDecision':'Accept exactFINAL PASS aftersolecycle1 andsourceproofcorrectedforforbiddencross-noteban. OldFaithfullookuprewrittenbroadfirstparknationalMAIN; SOURCE6/4/current/independentallbound. HistoryUSAwrongnoteYellowstonefirstparkallowedcanonicalfactpool, actualMAINIndianRemovalnotduplicate. Noautomaticsecondcycle/noQAcredit.'}]
report={'scope':'national-parks-nature001 FINALsolecycle1','acceptedOrders':[1],'qualityBasis':'PersonalSOURCE+independentFINALfullcontexts/onekey/fourplausibleparkoptions/ownextra/absoluteEASY andactualMAINpeers, root6/4exactbindings+required19. Correctedsource-onlynote-overlapmistakewithinsolecycle1, noothercardchanged.','verified':{'currentCards':1,'literalGroups':6,'wholeVariants':4,'primaryPages':6,'actualPeers':len(peers['actualCurrentPeers']),'bilateralMAINComparisons':len(peers['actualBilateralMAINComparisons'])},'QA':{'path':str((D/'qa-parks001-cycle1.json').relative_to(C)),'pass':19,'fail':0,'pending':0,'testedCatalogCommit':'979d4c0ec45ab67d9d3a8480735911e36ee0e15b'},'actualCompactionAudit':{'root':1,'SOURCE':1,'OTHER':0,'method':'Actualnativeuniquelyfoundjournals active+archived. SOURCEparkstage0→firsteventafterfinish; noordinaryreuseafter1.'}}
files=[p for p in R.rglob('*') if p.is_file()]+[pathlib.Path(__file__)];cc=m.certify(accepted,report,741,8,D/'certification-parks001-final-pass1.json',files,'979d4c0ec45ab67d9d3a8480735911e36ee0e15b')
with m.flow.locked():m.flow.lease('acquire','planning',O)
try:
 sp=P/'evidence/question-revision-process-v2/coordinator-state.json';st=rd(sp);st['coordinatorProgress'].update(CURRENT=742,newlyCertified=35,remaining=1258);st['waveCURRENT']=[500,198,44,0];wr(sp,st)
 gp=P/'evidence/question-revision-process-v2/active-full2000-goal-01a13f31.json';g=rd(gp);g.update(CURRENT=742,remaining=1258,waveCURRENT=[500,198,44,0],latestCodeCommit=cc,latestCertification=str((D/'certification-parks001-final-pass1.json').relative_to(C)));wr(gp,g)
 print('goalplanning',m.h.save(P,'refs/heads/codex/question-revision-resume-20261014',[str(p.relative_to(P)) for p in [sp,gp]],'Update fullgoal CURRENT742 remaining1258 rootdelta35; park001FINALclosed',raw(P/m.h.git(P,'rev-parse','--git-path','index'))))
finally:
 with m.flow.locked():m.flow.lease('release','planning',O)
