"""Root binding of existing independent INITIAL10, credit only exact SOURCE+PASS3."""
import pathlib,json,hashlib,importlib.util,subprocess,datetime
C=pathlib.Path(__file__).resolve().parents[4];D=pathlib.Path(__file__).parent
P=pathlib.Path('/Users/eaafonasev/Projects/mindbattle/planning');O='01a13f31-9224-7dd1-90e0-e5b0ea2e94a9'
def rd(p):return json.loads(pathlib.Path(p).read_text())
def sha(v):return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def raw(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def wr(p,v):pathlib.Path(p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def mod(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=mod('cert_rel',D/'certification-common-relocated.py');m.O=O
R=D/'independent-books8-initial';rp=R/'initial10-current-completion-receipt.json';r=rd(rp);old=rd(R/'receipt.json');sources=rd(R/'sources.json');peers=rd(R/'initial10-current-completion-peers.json');qa=rd(D/'qa-books10-combined-initial.json');idx=rd(D/'books10-current-initial-source-index.json');applies=[rd(D/'apply-books8-initial.json'),rd(D/'apply-books2-initial-completion.json')]
assert len(r['entries'])==10 and qa['numPassedTests']==19 and qa['numFailedTests']==qa['numPendingTests']==0
assert (C/'src/content/topics/books-publishing.json').read_bytes()==subprocess.check_output(['git','-C',str(C),'show',idx['QA']['testedCatalogCommit']+':src/content/topics/books-publishing.json'])
catalog={};topics={};cp=rd(P/'openspec/changes/question-quality-future-waves/current-checkpoint.json')
for t in {e['topicId'] for e in cp['selectedCards']}|{p['topicId'] for p in peers['actualCurrentPeers']}:
 q=rd(C/f'src/content/topics/{t}.json')['questions'];topics[t]=q;catalog.update({x['id']:x for x in q})
baselineTopics={t:json.loads(subprocess.check_output(['git','-C',str(C),'show',cp['baselineSHA']+f':src/content/topics/{t}.json']))['questions'] for t in {e['topicId'] for e in cp['selectedCards']}}
for e in cp['selectedCards']:
 t=e['topicId']; pos=next(k for k,q in enumerate(baselineTopics[t]) if q['id']==e['questionId']);q=topics[t][pos];assert q['id']==e['questionId'] and q['difficulty']==e['difficulty'] and q['correctIndex']==e['correctIndex']
for s in sources['entries']:assert raw(s['path'])==s['rawReadSHA256'] and s['personalReadEvidence'] and s['locator']
for p in peers['actualCurrentPeers']:assert p['card']==catalog[p['id']] and sha(p['card'])==p['canonicalSHA256']
for p in peers['all10ProposedFullCards']:assert p['card']==catalog[p['id']] and sha(p['card'])==p['canonicalSHA256']
for name,digest in rd(R/'initial10-current-completion-verification.json')['initial8HistoryHashesUnchanged'].items():assert raw(R/name)==digest
ag={ (e['id'],e['group']):e for a in applies for e in a['finalGroupBindings']};av={(e['id'],e['slot']):e for a in applies for e in a['finalVariantBindings']}
accepted=[]
for e in r['entries']:
 i=e['id'];q=catalog[i];assert e['currentCard']==q and sha(q)==e['currentCardCanonicalSHA256'];assert len(e['sixLiteralCanonicalGroups'])==6 and len(e['fourFullPromptAnswerNoteVariants'])==4
 gs={'prompt_ordered_answers_key':{'prompt':q['prompt'],'answers':[a['text'] for a in q['answers']],'correctIndex':q['correctIndex']},'explanation':q['explanation'],**{'note'+str(k):a['note'] for k,a in enumerate(q['answers'])}}
 for g in e['sixLiteralCanonicalGroups']:
  assert g['literal']==gs[g['group']]==ag[i,g['group']]['literal'] and sha(g['literal'])==g['canonicalSHA256']==ag[i,g['group']]['literalSHA256'];assert g['individualGround'] and g['sourcesLocators']
 for v in e['fourFullPromptAnswerNoteVariants']:
  k=v['slot'];tr={'prompt':q['prompt'],'answer':q['answers'][k]['text'],'note':q['answers'][k]['note']};assert {key:v[key] for key in tr}==tr and sha(tr)==v['tripleCanonicalSHA256']==av[i,k]['bindingCanonicalSHA256'];assert all(v[key] for key in ['grammar','plausibility','truthUniqueKey','noteTruthUsefulness','sourcesLocators'])
 assert e['absoluteLevel'] and e['correctNoteExtraFact']
 if e['status']=='PASS':
  assert e['sourceOrder'] in [2,8,10] and not e['defects'];accepted.append({'questionId':i,'cardCanonicalSha256':sha(q),'authorNativeId':'01a13f55-ee13-7aa2-8a9a-cbb4535f2628','authorReceipt':str((C/'docs/content-audits/question-quality-wave-8/process-v2-books1-20-01a13f31/author1-10/partial-ready/sourceproof.json').relative_to(C)),'authorFreeze':'cdd92f09da579a7445584869954310333f3495e7','readerNativeId':'01a13f7e-d71d-7351-8403-696e2273eaca','independentReceipt':str(rp.relative_to(C)),'readerReceiptRawSHA256':raw(rp),'coordinatorDecision':'Accept exactINITIAL PASS. Six literal groups and four wholevariants match SOURCE/apply/current; substantive independent personal primary grounds and freshpeer delta preserved; FIX7 excluded.'})
assert len(accepted)==3
report={'scope':'books-publishing INITIAL original10; PASS3 FIX7','acceptedOrders':[2,8,10],'directedCycle1Orders':[1,3,4,5,6,7,9],'qualityBasis':'SOURCE full relevant public primarycontexts + independent exactCURRENT wholecards PASS; root literal/hash/frozen/peer/source bindings. QA and structural metadata alone grant0. Canonical wrongnotes allowed.','verified':{'CURRENTCards':10,'literalGroups':60,'fullPromptAnswerNoteTriples':40,'sourceURLMappings':9,'distinctRawPublicFiles':3,'actualFreshPeers':len(peers['actualCurrentPeers']),'allSelected2000FrozenAndOrder':True,'historyINITIAL8Unchanged':True,'sharedPlanningRelocationFollowed':str(P)},'QA':{'path':str((D/'qa-books10-combined-initial.json').relative_to(C)),'pass':19,'fail':0,'pending':0,'testedCatalogCommit':idx['QA']['testedCatalogCommit']},'actualCompactionAudit':{'root':1,'SOURCE':1,'OTHER':0,'method':'Exactlyone nativejournal each acrossactive+archived; count actual top-level compacted events; missing notzero'},'noFullTestsBuildRuntimeRelease':True}
files=[p for p in R.rglob('*') if p.is_file()]+[pathlib.Path(__file__),D/'certification-common-relocated.py']
cc=m.certify(accepted,report,727,8,D/'certification-books10-initial-pass3-fix7.json',files,'26df419d2901d1c66e126138e88db1147341de28')
with m.flow.locked():m.flow.lease('acquire','planning',O)
try:
 sp=P/'evidence/question-revision-process-v2/coordinator-state.json';st=rd(sp);st['coordinatorProgress'].update(CURRENT=730,newlyCertified=23,remaining=1270);st['waveCURRENT']=[500,198,32,0];st['phase']='ACTIVE_FULL_EXACT2000_WAVE8_32_OF500';wr(sp,st)
 gp=P/'evidence/question-revision-process-v2/active-full2000-goal-01a13f31.json';g=rd(gp);g.update(CURRENT=730,remaining=1270,waveCURRENT=[500,198,32,0],latestCodeCommit=cc,latestCertification=str((D/'certification-books10-initial-pass3-fix7.json').relative_to(C)));wr(gp,g)
 print('goalplanning',m.h.save(P,'refs/heads/codex/question-revision-resume-20261014',[str(p.relative_to(P)) for p in [sp,gp]],'Update fullgoal CURRENT730 remaining1270; rootdelta23',raw(P/m.h.git(P,'rev-parse','--git-path','index'))))
finally:
 with m.flow.locked():m.flow.lease('release','planning',O)
