"""Bind independent FINAL4 with author's exact-primary-locator completion14."""
import pathlib,json,hashlib,importlib.util,subprocess
C=pathlib.Path(__file__).resolve().parents[4];D=pathlib.Path(__file__).parent;P=pathlib.Path('/Users/eaafonasev/Projects/mindbattle/planning');O='01a13f31-9224-7dd1-90e0-e5b0ea2e94a9'
def rd(p):return json.loads(pathlib.Path(p).read_text())
def sha(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def raw(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def wr(p,j):pathlib.Path(p).write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('m',D/'certification-common-relocated.py');m.O=O;guard=load('guard',D/'planning-certification-guard.py')
R=D/'independent-books11-combined/final-cycle1-ready4';rp=R/'receipt.json';r=rd(rp);sources=rd(R/'sources.json');peers=rd(R/'peers.json');a=rd(D/'apply-books-fix4-cycle1.json');qa=rd(D/'qa-books27-initial-completion.json');A=C/'docs/content-audits/question-quality-wave-8/process-v2-books12-15-17-18-cycle1-01a13f31/author';originalMP=A/'source4-exact-locator-completion.json';meta=rd(originalMP);mp=D/'source4-exact-locator-completion-normalized.json'
assert len(r['entries'])==4 and qa['numPassedTests']==19 and qa['numFailedTests']==qa['numPendingTests']==0
assert (C/'src/content/topics/books-publishing.json').read_bytes()==subprocess.check_output(['git','-C',str(C),'show','9352f63b4fd3deb2716e0facbaaae1828b62b78d:src/content/topics/books-publishing.json'])
catalog={}
for t in {p['topicId'] for p in peers['actualCurrentPeers']}:catalog.update({q['id']:q for q in rd(C/f'src/content/topics/{t}.json')['questions']})
for p in peers['actualCurrentPeers']:assert p['card']==catalog[p['id']] and sha(p['card'])==p['canonicalSHA256']
for s in sources['rawSources']:assert raw(C/s['path'])==s['rawSHA256'] and s['completeness']
for s in sources['authorShortenedExcerptsSupplementaryOnly']:assert raw(C/s['path'])==s['rawSHA256']
assert {e['sourceOrder'] for e in meta['entries']}=={12,15,17,18};nb=0
for e in meta['entries']:
 q=catalog[e['id']];assert sha(q)==e['currentCardCanonicalSHA256'] and not e['cardTextChanged'] and q['prompt']==e['fullPrompt']
 for b in e['bindings']:
  assert b['status']=='SUPPORTED' and b['primaryGround'] and b['locator'] and b['conditions'];g=b['fieldGroup'];v=({'prompt':q['prompt'],'answers':[x['text'] for x in q['answers']],'correctIndex':q['correctIndex']} if g=='prompt_ordered_answers_key' else q['explanation'] if g=='explanation' else q['answers'][int(g[4:])]['note']);assert v==b['literal'];
  if sha(v)!=b['literalSHA256']:
   assert e['sourceOrder']==17 and g=='prompt_ordered_answers_key';b['originalAuthorLiteralSHA256']=b['literalSHA256'];b['literalSHA256']=sha(v);b['technicalNormalization']='Only incorrectcanonicalobjectdigest recomputed; literalexactlyCURRENT/SOURCE/OTHER, allclaimgrounds andlocators unchanged'
  assert sha(v)==b['literalSHA256']
  for s in b['sources']:assert raw(C/s['path'])==s['sha256'] and s['url']
  nb+=1
assert nb==14;meta['originalAuthorCompletionPath']=str(originalMP.relative_to(C));meta['rootTechnicalNormalization']='Exactlyone KEYobjectdigest17 correctedafterliteralidentity; originalauthorfile preserved';wr(mp,meta)
ag={(e['id'],e['group']):e for e in a['finalGroupBindings']};av={(e['id'],e['slot']):e for e in a['finalVariantBindings']};accepted=[]
for e in r['entries']:
 i=e['id'];q=catalog[i];assert e['stage']=='FINAL' and e['status']=='PASS' and not e['unresolvedDefects'];assert e['currentCard']==q and sha(q)==e['currentCardCanonicalSHA256'];assert len(e['sixLiteralCanonicalGroups'])==6 and len(e['fourFullPromptAnswerNoteVariants'])==4
 gs={'prompt_ordered_answers_key':{'prompt':q['prompt'],'answers':[v['text'] for v in q['answers']],'correctIndex':q['correctIndex']},'explanation':q['explanation'],**{'note'+str(k):v['note'] for k,v in enumerate(q['answers'])}}
 for g in e['sixLiteralCanonicalGroups']:assert g['literal']==gs[g['group']]==ag[i,g['group']]['literal'] and sha(g['literal'])==g['canonicalSHA256']==ag[i,g['group']]['literalSHA256'] and g['individualGround'] and g['sourcesLocators']
 for v in e['fourFullPromptAnswerNoteVariants']:
  k=v['slot'];tr={'prompt':q['prompt'],'answer':q['answers'][k]['text'],'note':q['answers'][k]['note']};assert {x:v[x] for x in tr}==tr and sha(tr)==v['tripleCanonicalSHA256']==av[i,k]['bindingCanonicalSHA256'];assert all(v[x] for x in ['grammar','plausibility','truthUniqueKey','noteTruthUsefulness','sourcesLocators'])
 accepted.append({'questionId':i,'cardCanonicalSha256':sha(q),'authorNativeId':a['author'],'authorReceipt':a['authorPacket']+'/sourceproof.json','authorFreeze':'18d1192f49b3593a8f2e9703c872f990b44742d0','sourceExactLocatorCompletion':str(mp.relative_to(C)),'readerNativeId':r['reviewerThread'],'independentReceipt':str(rp.relative_to(C)),'readerReceiptRawSHA256':raw(rp),'coordinatorDecision':'Accept exactFINAL PASS aftersolecycle1. Current24groups16variants matchSOURCE+apply, independentlypersonallyreadwholeprimary/source/conditions/levels/currentMAIN; AUTHORsupplement14exactlocatorclaims personallyreadincludingnewfullCIEPtypesetterL312–313, noquestiontextchanges. Noautomaticsecondcycle.'})
report={'scope':'books sourceOrders12/15/17/18 FINALsolecycle1 PASS4','acceptedOrders':[12,15,17,18],'qualityBasis':'Substantive exactCURRENT SOURCE+independentFINALPASS andROOTbindings/required19; source14claimlocatorcompletion preservesSOURCEpersonalprimaryground withcorrectexactlimits. Canonicalwrongnotefactpoolallowed.','verified':{'currentCards':4,'literalGroups':24,'wholeVariants':16,'currentPeers':len(peers['actualCurrentPeers']),'SOURCEExactLocatorBindings':nb,'freshCurrent21to30Pairs':len(peers['currentBooks21to30BilateralPairs'])},'QA':{'path':str((D/'qa-books27-initial-completion.json').relative_to(C)),'pass':19,'fail':0,'pending':0,'testedCatalogCommit':'9352f63b4fd3deb2716e0facbaaae1828b62b78d'},'preleaseGuard':True,'actualCompactionAudit':{'root':1,'SOURCE':'lastaudit0beforeboundedproofcompletion; inspectcurrentjournalforreuse','OTHER':1,'method':'Actualnativejournals active+archived, OTHERcompletedoriginalFINALsliceandarchivedall65filesbyteverified. Nootherstageafter1.'}}
files=[p for p in R.rglob('*') if p.is_file()]+[mp,originalMP,pathlib.Path(__file__)];cc=guard.certify_preleased(m,accepted,report,749,8,D/'certification-books-fix4-final-pass4.json',files,'9352f63b4fd3deb2716e0facbaaae1828b62b78d')
with m.flow.locked():m.flow.lease('acquire','planning',O)
try:
 sp=P/'evidence/question-revision-process-v2/coordinator-state.json';st=rd(sp);st['coordinatorProgress'].update(CURRENT=753,newlyCertified=46,remaining=1247);st['waveCURRENT']=[500,198,55,0];wr(sp,st)
 gp=P/'evidence/question-revision-process-v2/active-full2000-goal-01a13f31.json';g=rd(gp);g.update(CURRENT=753,remaining=1247,waveCURRENT=[500,198,55,0],latestCodeCommit=cc,latestCertification=str((D/'certification-books-fix4-final-pass4.json').relative_to(C)));wr(gp,g)
 print('goalplanning',m.h.save(P,'refs/heads/codex/question-revision-resume-20261014',[str(p.relative_to(P)) for p in [sp,gp]],'Update fullgoal CURRENT753 remaining1247 rootdelta46; FINAL4closedwithSOURCEexactlocators',raw(P/m.h.git(P,'rev-parse','--git-path','index'))))
finally:
 with m.flow.locked():m.flow.lease('release','planning',O)
