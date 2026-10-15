"""Bind already-saved SOURCE/FINAL2; no project test or content mutation."""
import pathlib,json,hashlib,importlib.util,subprocess
C=pathlib.Path(__file__).resolve().parents[4];D=pathlib.Path(__file__).parent
OLD=D.parent/'coordinator-01a13f31';P=pathlib.Path('/Users/eaafonasev/Projects/mindbattle/planning')
O='01a14018-7b8d-7301-ad28-95ee8d812e97'
def rd(p):return json.loads(pathlib.Path(p).read_text())
def sha(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def raw(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def wr(p,v):pathlib.Path(p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('certificate',D/'certification-common.py');m.O=O;m.P=P
guard=load('guard',OLD/'planning-certification-guard.py')
R=OLD/'independent-books9-initial-21-30/final-cycle1-ready2';rp=R/'receipt.json'
r=rd(rp);src=rd(R/'sources.json');peers=rd(R/'peers.json');ver=rd(R/'verification.json')
a=rd(OLD/'apply-books26-28-cycle1.json');qaPath=OLD/'qa-books26-28-cycle1.json';qa=rd(qaPath)
assert qa['success'] and qa['numPassedTests']==19 and qa['numFailedTests']==qa['numPendingTests']==0
assert raw(qaPath)==ver['existingQA19']['rawSHA256']
qaCommit='9b2cbce5547d11dc8790bd7fc9658f2035aca7d8'
tp=C/'src/content/topics/books-publishing.json'
assert raw(tp)==ver['catalogRawSHA256']
assert tp.read_bytes()==subprocess.check_output(['git','-C',str(C),'show',qaCommit+':src/content/topics/books-publishing.json'])
cat={}
for t in {p['topicId'] for p in peers['actualCurrentPeers']}:
 cat.update({q['id']:q for q in rd(C/f'src/content/topics/{t}.json')['questions']})
for p in peers['actualCurrentPeers']:assert p['card']==cat[p['id']] and sha(p['card'])==p['sha256']
for pair in peers['bilateralMainComparisons']:
 for side in ['left','right']:
  p=pair[side];assert p['card']==cat[p['id']] and sha(p['card'])==p['sha256']
for s in src['sources']:assert raw(C/s['path'])==s['rawReadSHA256'] and s['personalReadEvidence'] and s['locator']
ag={(g['id'],g['group']):g for g in a['finalGroupBindings']}
av={(v['id'],v['slot']):v for v in a['finalVariantBindings']}
candidate=rd(C/a['authorPacket']/'candidate.json');authorProof=rd(C/a['authorPacket']/'sourceproof.json')
assert len(r['entries'])==2 and {e['sourceOrder'] for e in r['entries']}=={26,28}
corrections=[];accepted=[]
for e in r['entries']:
 i=e['id'];q=cat[i];assert e['stage']=='FINAL' and e['authorCycle']==1 and e['status']=='PASS' and not e['defects']
 assert e['currentCard']==q and sha(q)==e['currentCardCanonicalSHA256']
 ce=next(x for x in candidate['entries'] if x['id']==i)
 assert ce['proposedCard']==q and ce['afterHash']==sha(q)
 assert len(e['sixLiteralCanonicalGroups'])==6 and len(e['fourFullPromptAnswerNoteVariants'])==4
 gs={'prompt_ordered_answers_key':{'prompt':q['prompt'],'answers':[v['text'] for v in q['answers']],'correctIndex':q['correctIndex']},'explanation':q['explanation'],**{'note'+str(k):v['note'] for k,v in enumerate(q['answers'])}}
 for g in e['sixLiteralCanonicalGroups']:
  assert g['literal']==gs[g['group']]==ag[i,g['group']]['literal'] and sha(g['literal'])==g['canonicalSHA256']==ag[i,g['group']]['literalSHA256']
  assert g['individualGround'] and g['sourcesLocators']
  if e['sourceOrder']==26 and g['group'] in ['note1','note2','note3']:
   corrections.append({'id':i,'group':g['group'],'literal':g['literal'],'canonicalSHA256':sha(g['literal']),'originalAuthorGround':ag[i,g['group']]['primaryGround'],'correctIndependentGround':g['individualGround'],'sourcesLocators':g['sourcesLocators'],'decision':'Accept explicit independent corrected exact binding; original shifted author label retained, not used as support for this slot. SOURCE has already personally read the relevant primary contexts and supplied role grounds; reader independently confirms full context. No card text change or second author cycle.'})
 for v in e['fourFullPromptAnswerNoteVariants']:
  k=v['slot'];tr={'prompt':q['prompt'],'answer':q['answers'][k]['text'],'note':q['answers'][k]['note']}
  assert {x:v[x] for x in tr}==tr and sha(tr)==v['tripleCanonicalSHA256']==av[i,k]['bindingCanonicalSHA256']
  assert all(v[x] for x in ['grammar','plausibility','truthUniqueKey','noteTruthUsefulness','sourcesLocators'])
 accepted.append({'questionId':i,'cardCanonicalSha256':sha(q),'authorNativeId':a['author'],'authorReceipt':a['authorPacket']+'/sourceproof.json','authorFreeze':'b55eed8d262854c00f06389d0f097fdab82f14f8','readerNativeId':'01a14007-6729-7142-a4c8-4b0d3c8627c5','independentReceipt':str(rp.relative_to(C)),'readerReceiptRawSHA256':raw(rp),'coordinatorDecision':'Accept exact CURRENT FINAL PASS after solecycle1. SOURCE/independent/apply12groups8variants and fresh138peers/24bilateralMAIN match actual catalog; full retained primary contexts read by independent. Explicit shifted SOURCE26 note1/2/3 binding correction retained in adjudication; no semantic claim from generic metadata. QA19 exact catalog unchanged.','sourceEvidenceAdjudication':str((D/'source26-binding-adjudication.json').relative_to(C))})
assert len(corrections)==3
wr(D/'source26-binding-adjudication.json',{'owner':O,'scope':'SOURCE26 three shifted note-ground labels','corrections':corrections,'originalSourcePreserved':True,'sourceReaderCorrection':str((R/'sources.json').relative_to(C)),'qualityCredit':0})
report={'scope':'books26/28 FINAL solecycle1 PASS2','acceptedOrders':[26,28],'qualityBasis':'SOURCE+independent FINAL exact CURRENT substantive PASS; root checks all literal/triple/currentpeer/source hashes and adjudicates three shifted evidence labels. HOLD elsewhere stays0.','verified':{'currentCards':2,'literalGroups':12,'wholeVariants':8,'actualPeers':len(peers['actualCurrentPeers']),'bilateralMainPairs':len(peers['bilateralMainComparisons'])},'QA':{'path':str(qaPath.relative_to(C)),'pass':19,'fail':0,'pending':0,'testedCatalogCommit':qaCommit,'reportCommit':'b55eed8d262854c00f06389d0f097fdab82f14f8','rerun':False,'reason':'Catalog byte-identical to tested snapshot; ownership/evidence metadata only'},'preleaseGuard':True,'ownIntakeCURRENT':754,'actualCompactionAudit':{'root':0,'SOURCE':1,'OTHER':0,'missingNotZero':True}}
files=[pathlib.Path(__file__),D/'source26-binding-adjudication.json']
cc=guard.certify_preleased(m,accepted,report,754,8,D/'certification-books26-28-final-pass2.json',files,qaCommit)
with m.flow.locked():m.flow.lease('acquire','planning',O)
try:
 sp=P/'evidence/question-revision-process-v2/coordinator-state.json';st=rd(sp);st['waveCURRENT']=[500,198,58,0];st['currentNativeActors']=rd(P/'evidence/question-revision-process-v2/owned-intake-01a14018.json')['actors'];st['readyQueue']=[{'scope':'book4 genuine new function solution','status':'SOURCE_READY_UNQUALIFIED_UNAPPLIED','qualityCredit':0}];st['currentWork'].update(authorActive=0,independentActive=0,readyCurrentQueue=1,next='Qualify book4 concrete new function proposal; fullgoal2000 continues.');wr(sp,st)
 gp=P/'evidence/question-revision-process-v2/active-full2000-goal-01a14018.json';g=rd(gp);g.update(CURRENT=756,remaining=1244,newlyCertified=2,waveCURRENT=[500,198,58,0],latestCodeCommit=cc,latestCertification=str((D/'certification-books26-28-final-pass2.json').relative_to(C)));wr(gp,g)
 print('projection',m.h.save(P,'refs/heads/codex/question-revision-resume-20261014',[str(p.relative_to(P)) for p in [sp,gp]],'Record successor CURRENT756 delta2 and book4 next',raw(P/m.h.git(P,'rev-parse','--git-path','index'))))
finally:
 with m.flow.locked():m.flow.lease('release','planning',O)
