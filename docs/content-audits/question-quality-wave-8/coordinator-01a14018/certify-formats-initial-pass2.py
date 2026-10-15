"""Bind only INITIAL PASS65/67, preserving INITIAL FIX66/68 for sole cycle1."""
import pathlib,json,hashlib,importlib.util,subprocess
C=pathlib.Path(__file__).resolve().parents[4];D=pathlib.Path(__file__).parent;P=pathlib.Path('/Users/eaafonasev/Projects/mindbattle/planning');O='01a14018-7b8d-7301-ad28-95ee8d812e97'
def rd(p):return json.loads(pathlib.Path(p).read_text())
def sha(v):return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def raw(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def wr(p,v):pathlib.Path(p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def compacted(uid):
 fs=list(pathlib.Path('/Users/eaafonasev/.codex/sessions/2026/10/15').glob('*'+uid+'.jsonl'))+list(pathlib.Path('/Users/eaafonasev/.codex/archived_sessions').glob('*'+uid+'.jsonl'));assert len(fs)==1,(uid,'missing or ambiguous journal')
 return sum(json.loads(line).get('type')=='compacted' for line in fs[0].open())
audit={'root':compacted(O),'SOURCE':compacted('01a1402b-4c6a-7453-8992-25b45d34795e'),'OTHER':compacted('01a14007-6729-7142-a4c8-4b0d3c8627c5')};assert audit['root']<2
m=load('cert',D/'certification-common.py');m.O=O;m.P=P;guard=load('guard',D.parent/'coordinator-01a13f31/planning-certification-guard.py')
R=D/'independent-formats4-initial';rp=R/'receipt.json';r=rd(rp);src=rd(R/'sources.json');peers=rd(R/'peers.json');ver=rd(R/'verification.json');a=rd(D/'apply-formats4.json');qaPath=D/'qa-formats4.json';qa=rd(qaPath);qaCommit='b3a4d853644d480f9422d542e86f39c603b3b20a'
assert qa['success'] and qa['numPassedTests']==19 and qa['numFailedTests']==qa['numPendingTests']==0
assert raw(qaPath)==ver['existingQA19']['rawSHA256'];tp=C/'src/content/topics/books-publishing.json';assert raw(tp)==ver['catalogRawSHA256'] and tp.read_bytes()==subprocess.check_output(['git','-C',str(C),'show',qaCommit+':src/content/topics/books-publishing.json'])
cat={}
for t in {p['topicId'] for p in peers['actualCurrentPeers']}:cat.update({q['id']:q for q in rd(C/f'src/content/topics/{t}.json')['questions']})
for p in peers['actualCurrentPeers']:assert p['card']==cat[p['id']] and sha(p['card'])==p['sha256']
for pair in peers['bilateralMainComparisons']:
 for side in ['left','right']:
  p=pair[side];assert p['card']==cat[p['id']] and sha(p['card'])==p['sha256']
for s in src['sources']:
 assert raw(C/s['path'])==s['rawReadSHA256'] and s['personalReadEvidence'] and s['locators'] and all(p['locator'] for p in s['locators'])
 if s.get('readPath'):assert raw(pathlib.Path(s['readPath']))==s['readTextSHA256']
ag={(g['id'],g['group']):g for g in a['finalGroupBindings']};av={(v['id'],v['slot']):v for v in a['finalVariantBindings']};accepted=[];fix=[]
for e in r['entries']:
 i=e['id'];q=cat[i];assert e['stage']=='INITIAL' and q==e['currentCard'] and sha(q)==e['currentCardCanonicalSHA256'];assert len(e['sixLiteralCanonicalGroups'])==6 and len(e['fourFullPromptAnswerNoteVariants'])==4
 gs={'prompt_ordered_answers_key':{'prompt':q['prompt'],'answers':[v['text'] for v in q['answers']],'correctIndex':q['correctIndex']},'explanation':q['explanation'],**{'note'+str(k):v['note'] for k,v in enumerate(q['answers'])}}
 for g in e['sixLiteralCanonicalGroups']:assert g['literal']==gs[g['group']]==ag[i,g['group']]['literal'] and sha(g['literal'])==g['canonicalSHA256']==ag[i,g['group']]['literalSHA256'] and g['individualGround'] and g['sourcesLocators']
 for v in e['fourFullPromptAnswerNoteVariants']:
  k=v['slot'];tr={'prompt':q['prompt'],'answer':q['answers'][k]['text'],'note':q['answers'][k]['note']};assert {x:v[x] for x in tr}==tr and sha(tr)==v['tripleCanonicalSHA256']==av[i,k]['bindingCanonicalSHA256'];assert all(v[x] for x in ['grammar','plausibility','truthUniqueKey','noteTruthUsefulness','sourcesLocators'])
 if e['sourceOrder'] in [65,67]:
  assert e['status']=='PASS' and not e['defects'];accepted.append({'questionId':i,'cardCanonicalSha256':sha(q),'authorNativeId':a['author'],'authorReceipt':a['authorPacket']+'/sourceproof.json','authorFreeze':'084aaea7e8bedc43b75f64f1860beb5808e28217','readerNativeId':'01a14007-6729-7142-a4c8-4b0d3c8627c5','independentReceipt':str(rp.relative_to(C)),'readerReceiptRawSHA256':raw(rp),'coordinatorDecision':'Accept exact INITIAL PASS, individually grounded SOURCE/reader6/4/fullprimary, audienceMEDIUM and ownextra plus fresh109CURRENT/14MAIN pairs. Source path/container normalization only; retain reader exact locator corrections. First5 newer qualified proposals differ from format-layout/accessibility relations and remain unapplied, not CURRENT.'})
 else:
  assert e['sourceOrder'] in [66,68] and e['status']=='FIX' and e['defects'];fix.append({'id':i,'sourceOrder':e['sourceOrder'],'currentCardCanonicalSHA256':sha(q),'defects':e['defects'],'next':'One directed substantive author cycle1, then exactCURRENT FINAL; unresolved FINAL HOLD0.'})
assert len(accepted)==2 and len(fix)==2
first5=rd(C/'docs/content-audits/question-quality-wave-8/process-v2-books31-50-01a14018/author/source-completion/qualified-first5/candidate.json')
adjudication={'owner':O,'scope':'INITIAL65/67 PASS;66/68 FIX for solecycle1','acceptedOrders':[65,67],'fix':fix,'sourceEvidenceCorrections':src['sourceEvidenceCorrections'],'parallelProposalCaveat':'Reader inspected older original31-50 HOLD packet. Newer first5 SOURCE-qualified proposals are not applied/current; root reconciliation below replaces the stale readiness label, without inventing an independent semantic target PASS.','latestFirst5Proposals':[{'id':e['id'],'card':e['proposedCard'],'sha256':sha(e['proposedCard'])} for e in first5['entries']],'mainAxes':{'format65':'EPUB default reflow plus permitted fixed rendition','format67':'DAISY print-disabled talking-book audience/standard','first5':{'33':'Name of bars/spaces optical symbol','35':'Patron credential/account and checkout association','38':'UK/Ireland publisher legal deposit','39':'Serial-title identifier ISSN','40':'Registration-agency identifier DOI'}},'parallelDecision':'No first5 MAIN shares entity-relation-value-context or direct reverse with accepted65/67; original SOURCEformats qualification independently considered those identifier/legal proposal relations. Fresh5 differ by precise symbol wording/Russian translations, not EPUB layout or DAISY audience. Own-note fact reuse remains allowed.','qualityCredit':0}
wr(D/'adjudication-formats4-initial.json',adjudication)
report={'scope':'formats4 INITIAL PASS65/67 FIX66/68','acceptedOrders':[65,67],'fixOrders':[66,68],'qualityBasis':'Only exact SOURCE+independent INITIAL PASS65/67 receives credit; solecycle1 needed66level/68wording; no automatic completion of FIX/HOLD.','verified':{'currentCards':4,'literalGroups':24,'wholeVariants':16,'acceptedCards':2,'actualPeers':109,'bilateralMainPairs':14},'QA':{'path':str(qaPath.relative_to(C)),'pass':19,'fail':0,'pending':0,'testedCatalogCommit':qaCommit,'reportCommit':'084aaea7e8bedc43b75f64f1860beb5808e28217'},'preleaseGuard':True,'actualCompactionAudit':audit,'ownIntakeCURRENT':754,'adjudication':str((D/'adjudication-formats4-initial.json').relative_to(C))}
cc=guard.certify_preleased(m,accepted,report,757,8,D/'certification-formats-initial-pass2.json',[p for p in R.iterdir() if p.is_file()]+[pathlib.Path(__file__),D/'adjudication-formats4-initial.json'],qaCommit)
with m.flow.locked():m.flow.lease('acquire','planning',O)
try:
 sp=P/'evidence/question-revision-process-v2/coordinator-state.json';st=rd(sp);st['waveCURRENT']=[500,198,61,0];st['sourceFormats4Qualification'].update(status='INITIAL_PASS2_CERTIFIED_FIX2_CYCLE1_PENDING',qualityCredit=2,certificationCodeCommit=cc);st['currentNativeActors']['OTHER'].update(status='IDLE retained INITIALformats4 complete; FINAL66/68 next afterSOURCEcycle1/QA',cursor='589f93ab-4337-4d86-a1a0-de433fa8df3b:19');st['formats66_68Cycle1']={'status':'NEEDS_SOURCE_SOLE_CYCLE1','defects':fix,'qualityCredit':0,'adjudication':str((D/'adjudication-formats4-initial.json').relative_to(C))};st['currentWork'].update(independentActive=0,next='SOURCE solecycle1 formats66/68 priority; exactFINAL afterQA. Keep first5 qualified queue; no unrelated catalog mutation during formatcycle.');wr(sp,st)
 gp=P/'evidence/question-revision-process-v2/active-full2000-goal-01a14018.json';g=rd(gp);g.update(CURRENT=759,remaining=1241,newlyCertified=5,waveCURRENT=[500,198,61,0],latestCodeCommit=cc,latestCertification=str((D/'certification-formats-initial-pass2.json').relative_to(C)));wr(gp,g)
 print('projection',m.h.save(P,'refs/heads/codex/question-revision-resume-20261014',[str(p.relative_to(P)) for p in [sp,gp]],'Record CURRENT759 delta5 and sole sourcecycle1 formats66/68',raw(P/m.h.git(P,'rev-parse','--git-path','index'))))
finally:
 with m.flow.locked():m.flow.lease('release','planning',O)
