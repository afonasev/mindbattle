"""Case-driven exact SOURCE/CURRENT/reader binding. The planning guard is mandatory."""
import pathlib,json,hashlib,importlib.util,subprocess,sys,datetime
C=pathlib.Path(__file__).resolve().parents[4];D=pathlib.Path(__file__).parent;P=pathlib.Path('/Users/eaafonasev/Projects/mindbattle/planning');O='01a14321-0d63-7232-9aa1-9d71146e491a'
def rd(p):return json.loads(pathlib.Path(p).read_text())
def sha(v):return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def raw(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def wr(p,v):pathlib.Path(p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def digest(p):return p.get('sha256',p.get('canonicalSHA256'))
def compacted(uid):
 fs=list(pathlib.Path('/Users/eaafonasev/.codex/sessions').rglob('*'+uid+'.jsonl'))+list(pathlib.Path('/Users/eaafonasev/.codex/archived_sessions').rglob('*'+uid+'.jsonl'));assert len(fs)==1,(uid,'missing or ambiguous journal')
 return sum(json.loads(line).get('type')=='compacted' for line in fs[0].open())
def verify_source_freeze(applications,freeze):
 frozenSecond=int(subprocess.check_output(['git','-C',str(C),'show','-s','--format=%ct',freeze],text=True));result={}
 for a in applications:
  uid=a['author'];packet=C/a['authorPacket'];critical=[packet/f for f in ['candidate.json','sourceproof.json','peer-snapshot.json']]
  if a.get('actualPeerDelta'):critical.append(C/a['actualPeerDelta'])
  for p in critical:assert subprocess.check_output(['git','-C',str(C),'show',freeze+':'+str(p.relative_to(C))])==p.read_bytes(),('SOURCE_FREEZE_BYTES_DRIFT',uid,str(p))
  for source in rd(packet/'sourceproof.json')['rawSources']:assert raw(C/source['path'])==source['sha256']
  fs=list(pathlib.Path('/Users/eaafonasev/.codex/sessions').rglob('*'+uid+'.jsonl'))+list(pathlib.Path('/Users/eaafonasev/.codex/archived_sessions').rglob('*'+uid+'.jsonl'));assert len(fs)==1,(uid,'missing or ambiguous source journal');events=[json.loads(line) for line in fs[0].open()];boundaries=[e['timestamp'] for e in events if e.get('type')=='compacted'];result[uid]={'actualCompactions':len(boundaries),'freeze':freeze,'criticalFilesByteExact':len(critical)}
  if len(boundaries)>=2:
   second=datetime.datetime.fromisoformat(boundaries[1].replace('Z','+00:00')).timestamp()
   assert frozenSecond+1<=second,('SOURCE_PROOF_FREEZE_AFTER_SECOND_COMPACTION_NEEDS_FRESH_ADOPTION',uid,freeze,boundaries[1]);result[uid]['freezeProvenBeforeSecondCompaction']=True
 return result
casePath=pathlib.Path(sys.argv[1]).resolve();case=rd(casePath);applications=[rd(C/p) for p in case['applyPaths']];sourceLineage=verify_source_freeze(applications,case['sourceFreeze'])
if '--audit-source-only' in sys.argv:
 print(json.dumps({'sourceLineage':sourceLineage,'mutations':False}));raise SystemExit(0)
R=C/case['readerPath'];rp=R/'receipt.json';r=rd(rp);src=rd(R/'sources.json');peers=rd(R/'peers.json');ver=rd(R/'verification.json');qaPath=C/case['qaPath'];qa=rd(qaPath)
assert qa['success'] and qa['numPassedTests']==19 and qa['numFailedTests']==qa['numPendingTests']==qa.get('numTodoTests',0)==0
assert raw(qaPath)==ver['existingQA19']['rawSHA256']
topicId=case.get('topicId','books-publishing')
assert topicId in {p.stem for p in (C/'src/content/topics').glob('*.json')}
tp=C/f'src/content/topics/{topicId}.json'
assert raw(tp)==ver['catalogRawSHA256'] and tp.read_bytes()==subprocess.check_output(['git','-C',str(C),'show',case['testedCatalogCommit']+':'+str(tp.relative_to(C))])
topicIds={q['id'] for q in rd(tp)['questions']}
assert all(e['id'] in topicIds for e in r['entries'])
cat={}
for t in {p['topicId'] for p in peers['actualCurrentPeers']}:cat.update({q['id']:q for q in rd(C/f'src/content/topics/{t}.json')['questions']})
for p in peers['actualCurrentPeers']:assert p['card']==cat[p['id']] and sha(p['card'])==digest(p)
proposals={}
for snapshot in peers.get('latestProposalSnapshots',[]):
 p=snapshot['proposal'];sourcePath=C/snapshot['sourcePath'];assert raw(sourcePath)==snapshot['sourceRawSHA256']
 sourceData=rd(sourcePath)
 if 'entries' in sourceData:
  entry=next(e for e in sourceData['entries'] if e['id']==p['id'])
 elif 'relevantSimultaneousProposals' in sourceData:
  # SOURCE78 retained full own proposals in its immutable MAIN packet.
  # Bind the actual body/hash and the original author's candidate at the same
  # source freeze; a reader pointer alone cannot promote another version.
  local=next(e for e in sourceData['relevantSimultaneousProposals'] if e['id']==p['id'])
  assert local['card']==p['card'] and sha(local['card'])==digest(local)==digest(p)
  original=C/sourceData['originalAuthor'];originalCandidate=original.parent/'candidate.json'
  assert originalCandidate.read_bytes()==subprocess.check_output(['git','-C',str(C),'show',case['sourceFreeze']+':'+str(originalCandidate.relative_to(C))])
  entry=next(e for e in rd(originalCandidate)['entries'] if e['id']==p['id'])
  assert entry['proposedCard']==local['card'] and entry['afterHash']==digest(local)
 else:
  # The reader retained the author's full MAIN-delta proposal. Bind both that
  # exact snapshot and its original candidate, without modifying reader evidence.
  local=next(e for e in sourceData['relevantLocalCards'] if e['id']==p['id'])
  entry=next(e for e in rd(sourcePath.parent/'candidate.json')['entries'] if e['id']==p['id'])
  assert local['frozenLocalProposalCard']==entry['proposedCard'] and local['frozenLocalProposalSHA256']==entry['afterHash']
 assert entry['proposedCard']==p['card'] and sha(p['card'])==digest(p)==entry['afterHash'];assert p['id'] not in proposals;proposals[p['id']]=p
pairEvidence=peers.get('bilateralMainComparisons',peers.get('bilateralMAINComparisons'))
assert isinstance(pairEvidence,list) and pairEvidence
pairEvidence=pairEvidence+peers.get('proposedBilateralMAINComparisons',[])
actualPeerBindings={p['id']:p for p in peers['actualCurrentPeers']}
for pair in pairEvidence:
 if 'leftToRight' in pair:
  assert pair['leftToRight'] and pair['rightToLeft']
 elif 'bilateralGround' in pair:
  # Reader supplied one joint, explicit two-direction assessment and a verbal
  # reverse check. Whole cards remain bound by id/hash below.
  assert pair['bilateralGround'] and pair['directReverseCheck'] and pair['result']=='DISTINCT_MAIN'
 else:
  # Joint bilateral prose names both actual relations; full cards are linked by
  # ID/hash into the personally-read snapshot, rather than duplicated per row.
  assert pair['bilateralEntityRelationValueContextAssessment'] and isinstance(pair['directReverse'],bool)
 for side in ['left','right']:
  p=pair[side]
  known=proposals.get(p['id']) if p.get('state','').startswith('UNAPPLIED_') else actualPeerBindings.get(p['id'])
  assert known and digest(p)==digest(known)
  card=p.get('card',known['card'])
  assert card==known['card'] and sha(card)==digest(p)
  if 'MAIN' in p:
   if isinstance(p['MAIN'],dict):
    # A structured semantic model is not a duplicate verbatim prompt. Require
    # all four dimensions; coordinator reviews alignment against the exact
    # whole card, whose canonical hash and live bytes are still mandatory.
    assert set(p['MAIN'])=={'entity','relation','value','context'} and all(p['MAIN'].values())
    if 'key' in p:assert p['key']==card['answers'][card['correctIndex']]['text']
   else:assert p['MAIN']==card['prompt'] and p['key']==card['answers'][card['correctIndex']]['text']
  if not p.get('state','').startswith('UNAPPLIED_'):assert card==cat[p['id']]
for s in src['sources']:
 assert raw(C/s['path'])==s['rawReadSHA256'] and s['personalReadEvidence'] and (s.get('locator') or s.get('locators'))
 if s.get('readPath'):assert raw(C/s['readPath'])==s['readTextSHA256']
ag={};av={};authors={}
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
report={**case['reportBase'],'scope':case['scope'],'acceptedOrders':case['acceptedOrders'],'verified':{'currentCards':len(r['entries']),'literalGroups':6*len(r['entries']),'wholeVariants':4*len(r['entries']),'acceptedCards':len(accepted),'actualPeers':len(peers['actualCurrentPeers']),'bilateralMainPairs':len(pairEvidence)},'QA':{'path':case['qaPath'],'pass':19,'fail':0,'pending':0,'testedCatalogCommit':case['testedCatalogCommit'],'reportCommit':case['qaReportCommit']},'preleaseGuard':True,'sourceFreezeLineage':sourceLineage,'actualCompactionAudit':audit,'ownIntakeCURRENT':840}
if '--verify-only' in sys.argv:
 print(json.dumps({'verified':report['verified'],'acceptedOrders':case['acceptedOrders'],'audit':audit,'mutations':False}));raise SystemExit(0)
m=load('certificate',D/'certification-common.py');m.O=O;m.P=P;guard=load('guard',D.parent/'coordinator-01a13f31/planning-certification-guard.py')
cc=guard.certify_preleased(m,accepted,report,case['expectedCURRENT'],case['wave'],C/case['reportPath'],[p for p in R.rglob('*') if p.is_file()]+[pathlib.Path(__file__),casePath],case['testedCatalogCommit'])
with m.flow.locked():m.flow.lease('acquire','planning',O)
try:
 cp=rd(P/'openspec/changes/question-quality-future-waves/current-checkpoint.json');n=len(cp['currentEligibleCompletedIds']);waves=[w['currentSourceEditorialCards'] for w in cp['waves']]
 sp=P/'evidence/question-revision-process-v2/coordinator-state.json';st=rd(sp);st['waveCURRENT']=waves;wr(sp,st)
 gp=P/'evidence/question-revision-process-v2/active-full2000-goal-01a14321-0d63-7232-9aa1-9d71146e491a.json';g=rd(gp);g.update(CURRENT=n,remaining=2000-n,newlyCertified=n-840,waveCURRENT=waves,latestCodeCommit=cc,latestCertification=case['reportPath']);wr(gp,g)
 print('projection',m.h.save(P,'refs/heads/codex/question-revision-resume-20261014',[str(p.relative_to(P)) for p in [sp,gp]],f'Record fullgoal CURRENT{n} delta{n-840} exact accepted subset',raw(P/m.h.git(P,'rev-parse','--git-path','index'))))
finally:
 with m.flow.locked():m.flow.lease('release','planning',O)
