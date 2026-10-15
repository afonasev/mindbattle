"""Case-driven exact SOURCE/CURRENT/reader binding. The planning guard is mandatory."""
import pathlib,json,hashlib,importlib.util,subprocess,sys
C=pathlib.Path(__file__).resolve().parents[4];D=pathlib.Path(__file__).parent;P=pathlib.Path('/Users/eaafonasev/Projects/mindbattle/planning');O='01a14018-7b8d-7301-ad28-95ee8d812e97'
def rd(p):return json.loads(pathlib.Path(p).read_text())
def sha(v):return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def raw(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def wr(p,v):pathlib.Path(p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def digest(p):return p.get('sha256',p.get('canonicalSHA256'))
def compacted(uid):
 fs=list(pathlib.Path('/Users/eaafonasev/.codex/sessions/2026/10/15').glob('*'+uid+'.jsonl'))+list(pathlib.Path('/Users/eaafonasev/.codex/archived_sessions').glob('*'+uid+'.jsonl'));assert len(fs)==1,(uid,'missing or ambiguous journal')
 return sum(json.loads(line).get('type')=='compacted' for line in fs[0].open())
casePath=pathlib.Path(sys.argv[1]).resolve();case=rd(casePath);R=C/case['readerPath'];rp=R/'receipt.json';r=rd(rp);src=rd(R/'sources.json');peers=rd(R/'peers.json');ver=rd(R/'verification.json');qaPath=C/case['qaPath'];qa=rd(qaPath)
assert qa['success'] and qa['numPassedTests']==19 and qa['numFailedTests']==qa['numPendingTests']==qa.get('numTodoTests',0)==0
assert raw(qaPath)==ver['existingQA19']['rawSHA256'];tp=C/'src/content/topics/books-publishing.json';assert raw(tp)==ver['catalogRawSHA256'] and tp.read_bytes()==subprocess.check_output(['git','-C',str(C),'show',case['testedCatalogCommit']+':src/content/topics/books-publishing.json'])
cat={}
for t in {p['topicId'] for p in peers['actualCurrentPeers']}:cat.update({q['id']:q for q in rd(C/f'src/content/topics/{t}.json')['questions']})
for p in peers['actualCurrentPeers']:assert p['card']==cat[p['id']] and sha(p['card'])==digest(p)
proposals={}
for snapshot in peers.get('latestProposalSnapshots',[]):
 p=snapshot['proposal'];sourcePath=C/snapshot['sourcePath'];assert raw(sourcePath)==snapshot['sourceRawSHA256']
 entry=next(e for e in rd(sourcePath)['entries'] if e['id']==p['id']);assert entry['proposedCard']==p['card'] and sha(p['card'])==digest(p)==entry['afterHash'];assert p['id'] not in proposals;proposals[p['id']]=p
for pair in peers['bilateralMainComparisons']:
 assert pair['leftToRight'] and pair['rightToLeft']
 for side in ['left','right']:
  p=pair[side]
  if p.get('state','').startswith('UNAPPLIED_'):
   assert p['id'] in proposals and p['card']==proposals[p['id']]['card'] and sha(p['card'])==digest(p)==digest(proposals[p['id']])
  else:assert p['card']==cat[p['id']] and sha(p['card'])==digest(p)
for s in src['sources']:
 assert raw(C/s['path'])==s['rawReadSHA256'] and s['personalReadEvidence'] and (s.get('locator') or s.get('locators'))
 if s.get('readPath'):assert raw(C/s['readPath'])==s['readTextSHA256']
applications=[rd(C/p) for p in case['applyPaths']];ag={};av={};authors={}
for a in applications:
 for e in a['applied']:assert e['id'] not in authors;authors[e['id']]={'id':a['author'],'packet':a['authorPacket']}
 ag.update({(g['id'],g['group']):g for g in a['finalGroupBindings']});av.update({(v['id'],v['slot']):v for v in a['finalVariantBindings']})
accepted=[];acceptedOrders=set(case['acceptedOrders']);assert len(acceptedOrders)==len(case['acceptedOrders'])
for e in r['entries']:
 i=e['id'];q=cat[i];assert e['stage']==case['stage'] and e['currentCard']==q and sha(q)==e['currentCardCanonicalSHA256']
 gs={'prompt_ordered_answers_key':{'prompt':q['prompt'],'answers':[v['text'] for v in q['answers']],'correctIndex':q['correctIndex']},'explanation':q['explanation'],**{'note'+str(k):v['note'] for k,v in enumerate(q['answers'])}}
 assert len(e['sixLiteralCanonicalGroups'])==6 and {g['group'] for g in e['sixLiteralCanonicalGroups']}==set(gs)
 for g in e['sixLiteralCanonicalGroups']:assert g['literal']==gs[g['group']]==ag[i,g['group']]['literal'] and sha(g['literal'])==g['canonicalSHA256']==ag[i,g['group']]['literalSHA256'] and g['individualGround'] and g['sourcesLocators']
 assert len(e['fourFullPromptAnswerNoteVariants'])==4 and {v['slot'] for v in e['fourFullPromptAnswerNoteVariants']}==set(range(4))
 for v in e['fourFullPromptAnswerNoteVariants']:
  k=v['slot'];tr={'prompt':q['prompt'],'answer':q['answers'][k]['text'],'note':q['answers'][k]['note']};assert {x:v[x] for x in tr}==tr and sha(tr)==v['tripleCanonicalSHA256']==av[i,k]['bindingCanonicalSHA256'];assert all(v[x] for x in ['grammar','plausibility','truthUniqueKey','noteTruthUsefulness','sourcesLocators'])
 if e['sourceOrder'] in acceptedOrders:
  assert e['status']=='PASS' and not e['defects'];author=authors[i];accepted.append({'questionId':i,'cardCanonicalSha256':sha(q),'authorNativeId':author['id'],'authorReceipt':author['packet']+'/sourceproof.json','authorFreeze':case['sourceFreeze'],'readerNativeId':case['readerNativeId'],'independentReceipt':str(rp.relative_to(C)),'readerReceiptRawSHA256':raw(rp),'coordinatorDecision':case['coordinatorDecision']})
assert len(accepted)==len(acceptedOrders)>0
audit={'root':compacted(O),'SOURCE':{a['id']:compacted(a['id']) for a in authors.values()},'OTHER':compacted(case['readerNativeId'])};assert audit['root']<2
report={**case['reportBase'],'scope':case['scope'],'acceptedOrders':case['acceptedOrders'],'verified':{'currentCards':len(r['entries']),'literalGroups':6*len(r['entries']),'wholeVariants':4*len(r['entries']),'acceptedCards':len(accepted),'actualPeers':len(peers['actualCurrentPeers']),'bilateralMainPairs':len(peers['bilateralMainComparisons'])},'QA':{'path':case['qaPath'],'pass':19,'fail':0,'pending':0,'testedCatalogCommit':case['testedCatalogCommit'],'reportCommit':case['qaReportCommit']},'preleaseGuard':True,'actualCompactionAudit':audit,'ownIntakeCURRENT':754}
if '--verify-only' in sys.argv:
 print(json.dumps({'verified':report['verified'],'acceptedOrders':case['acceptedOrders'],'audit':audit,'mutations':False}));raise SystemExit(0)
m=load('certificate',D/'certification-common.py');m.O=O;m.P=P;guard=load('guard',D.parent/'coordinator-01a13f31/planning-certification-guard.py')
cc=guard.certify_preleased(m,accepted,report,case['expectedCURRENT'],case['wave'],C/case['reportPath'],[p for p in R.rglob('*') if p.is_file()]+[pathlib.Path(__file__),casePath],case['testedCatalogCommit'])
with m.flow.locked():m.flow.lease('acquire','planning',O)
try:
 cp=rd(P/'openspec/changes/question-quality-future-waves/current-checkpoint.json');n=len(cp['currentEligibleCompletedIds']);waves=[w['currentSourceEditorialCards'] for w in cp['waves']]
 sp=P/'evidence/question-revision-process-v2/coordinator-state.json';st=rd(sp);st['waveCURRENT']=waves;wr(sp,st)
 gp=P/'evidence/question-revision-process-v2/active-full2000-goal-01a14018.json';g=rd(gp);g.update(CURRENT=n,remaining=2000-n,newlyCertified=n-754,waveCURRENT=waves,latestCodeCommit=cc,latestCertification=case['reportPath']);wr(gp,g)
 print('projection',m.h.save(P,'refs/heads/codex/question-revision-resume-20261014',[str(p.relative_to(P)) for p in [sp,gp]],f'Record fullgoal CURRENT{n} delta{n-754} exact accepted subset',raw(P/m.h.git(P,'rev-parse','--git-path','index'))))
finally:
 with m.flow.locked():m.flow.lease('release','planning',O)
