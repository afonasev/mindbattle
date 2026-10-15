import pathlib,json,hashlib,copy,os
B=pathlib.Path('docs/content-audits/question-quality-wave-8');D=B/'coordinator-01a14103';O=D/'independent-books31-37-46-source37-final';PRE=D/'independent-books10-sourcec2-initial'
def j(p):return json.loads(pathlib.Path(p).read_text())
def h(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def raw(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def save(n,x):
 p=O/n;t=O/(n+'.partial');t.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');t.replace(p)
cp=pathlib.Path('src/content/topics/books-publishing.json');cat=j(cp);actual={q['id']:q for q in cat['questions']};prior=j(PRE/'receipt.json');apply=j(D/'apply-books31-37-46-cycle1-source37.json')['applied'];entries=[]
LOC=str(B/'process-v2-books15-current-source3-01a14018/author/sources/loc-flicc-preservation-binding-glossary-2026-10-15.txt');G=str(B/'process-v2-books51-70-01a14018/author/source-completion/remaining16/sources/dcrmr-glossary.html');H=str(B/'process-v2-books-remaining15-source-completion-01a14018/author/sources/halifax-combined-full-primary-context-2026-10-15.txt')
def ref(p,l):return {'path':p,'rawSHA256':raw(p),'locator':l}
for a in apply:
 n=a['sourceOrder'];c=actual[a['id']];assert c==a['proposedCard'];old=next(e for e in prior['entries'] if e['sourceOrder']==n);e=copy.deepcopy(old)
 assert {'prompt':c['prompt'],'answers':[z['text'] for z in c['answers']],'correctIndex':c['correctIndex']}==e['sixLiteralCanonicalGroups'][0]['literal']
 assert c['difficulty']==old['currentCard']['difficulty']
 e.update({'stage':'FINAL','status':'PASS','currentCard':c,'currentCardCanonicalSHA256':h(c),'defects':[],'cycle':'same solecycle1; no secondordinarycycle','initialReviewBinding':{'path':str(PRE/'receipt.json'),'rawSHA256':raw(PRE/'receipt.json'),'initialCurrentCardSHA256':old['currentCardCanonicalSHA256'],'initialStatus':old['status'],'resolvedInitialDefects':old['defects'],'reuseScope':'My own unchanged substantive initial checks reused with literal equality; full FINAL card/4triples personally reread, new fields independently verified.'}})
 if n==31:
  why='Новое объяснение прямо называет «Резервирование», затем описывает waiting list при занятости/недоступности и7дней хранения после готовности. Halifax L383 задаёт эти условия; уведомление описано для аккаунтов с email/phone. Объяснение — нормальное описание этой процедуры, не универсальная гарантия связи без контактных данных.'
  rs=[ref(H,'Halifax complete Holds and Returns L381–387, specifically L383; notification contacts L375–383')]
  g=e['sixLiteralCanonicalGroups'][1];g.update({'literal':c['explanation'],'canonicalSHA256':h(c['explanation']),'individualGround':why,'sourcesLocators':rs});e['resolutionAssessment']='INITIAL defect explanation fixed: reservation is now directly named; no MAIN/answer/notes/level change.'
 elif n==37:
  why='Полная LOC Guillotine entry L3117–3118 называет машину для резки большого числа листов бумаги и картона и отдельно её применение в library binding для trimming edges of books. «Могут обрезать» сохраняет необязательность конкретной машины; не утверждает, что любая обрезка всегда делается гильотиной.'
  rs=[ref(LOC,'Complete Guillotine L3117–3118; complete Trim/Trimming L3409–3411')];e['correctNoteExtraFact']='Гильотина как конкретное оборудование для обрезки краёв книги и её назначение для большого числа листов бумаги/картона — предметный новый факт, не повтор окончательного размера/момента до casing.'
  g=e['sixLiteralCanonicalGroups'][2];g.update({'literal':c['answers'][0]['note'],'canonicalSHA256':h(c['answers'][0]['note']),'individualGround':why,'sourcesLocators':rs});v=e['fourFullPromptAnswerNoteVariants'][0];v['noteTruthUsefulness']=why+' '+e['correctNoteExtraFact'];v['sourcesLocators']=rs;e['resolutionAssessment']='INITIAL correctnoteextra defect fixed. Guillotine entry directly covers both machine capacity/material and trimming library-book edges.'
 elif n==46:
  why='Полная DCRMR state definition допускает copy/group differences printed textual sheet или publisher casing within the same impression or issue. Новая note утверждает возможность различающихся states внутри одного impression, не переопределяет impression и не утверждает, что всякое различие объявлено отдельным issue.'
  rs=[ref(G,'Complete Glossary #impression and #state; adjacent #edition, #issue, #copy, #variant')];e['correctNoteExtraFact']='Внутри одного impression могут сосуществовать состояния печатного листа/издательской крышки. Это дополнительное свойство состава одного тиражного оттиска сверх его определения как копий одного printing event.'
  g=e['sixLiteralCanonicalGroups'][2];g.update({'literal':c['answers'][0]['note'],'canonicalSHA256':h(c['answers'][0]['note']),'individualGround':why,'sourcesLocators':rs});v=e['fourFullPromptAnswerNoteVariants'][0];v['noteTruthUsefulness']=why+' '+e['correctNoteExtraFact'];v['sourcesLocators']=rs;e['resolutionAssessment']='INITIAL synonym-only correctnoteextra defect fixed with independently sourced within-impression state variation; fact about own impression composition remains allowed even though state is another card KEY.'
 for k,v in enumerate(e['fourFullPromptAnswerNoteVariants']):
  v.update({'prompt':c['prompt'],'answer':c['answers'][k]['text'],'note':c['answers'][k]['note'],'tripleCanonicalSHA256':h({'prompt':c['prompt'],'answer':c['answers'][k]['text'],'note':c['answers'][k]['note']})})
 # No stale INITIAL FIX language retained for corrected key-note triples.
 if n in [37,46]:
  v=e['fourFullPromptAnswerNoteVariants'][0];v['plausibility']=e['sixLiteralCanonicalGroups'][0]['individualGround']+' Все четыре термина сопоставлены с полным prompt; новый ownnote не меняет единственный ключ.'
 entries.append(e)
ps=j(D/'actual-current-books31-37-46-peers.json')['actualCurrentPeers'];by={}
for p in ps:
 path=pathlib.Path('src/content/topics')/(p['topicId']+'.json');q=next(q for q in j(path)['questions'] if q['id']==p['id']);assert q==p['card'],('peer drift',p['id']);p['canonicalSHA256']=p['sha256']=h(q);p['sourceFile']=str(path);p['catalogRawSHA256']=raw(path);by[p['id']]=p
ids={e['id'] for e in entries};pairs=[]
for oldpair in j(PRE/'peers.json')['bilateralMAINComparisons']:
 if not ids.intersection([oldpair['left']['id'],oldpair['right']['id']]):continue
 p=copy.deepcopy(oldpair)
 for side in ['left','right']:
  z=by[p[side]['id']];assert p[side]['MAIN']==z['card']['prompt'];assert p[side]['key']==z['card']['answers'][z['card']['correctIndex']]['text'];p[side]['sha256']=h(z['card'])
 p['personalReuse']='My own substantive INITIAL bilateral judgment; MAIN/key unchanged verified on both exact full current cards; updated canonical bindings. Correctnote facts are not a MAIN duplicate ban.';pairs.append(p)
# Snapshot current unqualified proposals once; full relevant cards preserved, SOURCE status not treated as source qualification.
P20=B/'process-v2-books71-90-source-01a14103/author/candidate.json';P5=B/'process-v2-books31-37-43-46-47-cycle1-01a14103/author/candidate.json';props=[];proppairs=[]
for path,orders in [(P20,[73,74,75,78,80,81]),(P5,[43,47])]:
 data=j(path);rh=raw(path)
 for a in data['entries']:
  if a['sourceOrder'] not in orders:continue
  c=a['proposedCard'];props.append({'sourcePath':str(path),'sourceRawSHA256':rh,'proposal':{'id':c['id'],'card':c,'sha256':h(c),'state':'UNAPPLIED_UNQUALIFIED_'+a['status']},'sourceOrder':a['sourceOrder']})
  # Relevant dependency relations;43 is legal status with no physical/production MAIN overlap.
  nums=([46] if a['sourceOrder'] in [73,74,75,47] else [31] if a['sourceOrder']==78 else [37,46] if a['sourceOrder'] in [80,81] else [31,37,46])
  rightwhy={73:'73 asks abstract intellectual work in FRBR, not grouping physical copies by one print event.',74:'74 asks language/music realization (expression), not copies from one print event.',75:'75 asks the FRBR level manifestation for concrete publishing embodiment/common production traits;46 asks impression bounded by one printing event. Model-level embodiment and analytical-bibliography printing-event scope are different criteria; terminology related, no same relation/direct reverse.',78:'78 names the institution that collects and lends books;31 names placing a waiting-list request, a service action rather than institution.',80:'80 names the organization coordinating publication;37 names physical sizing operation and46 a group by printing event. Actor responsibility differs from operation/group definition.',81:'81 names the enterprise doing printing/binding;37 names edge-sizing and46 names copies from one printing event. Enterprise and process/result grouping are different entities.',43:'43 asks public-domain status of never-protected content;31/37/46 ask waiting-list action, sizing operation, or copy grouping. No common queried relation.',47:'47 defines issue by a deliberately differentiated publishing unit;46 impression by one printing event. New draft-based note does not change either MAIN definition; pending47 qualification is not inherited.'}[a['sourceOrder']]
  for n in nums:
   e=next(e for e in entries if e['sourceOrder']==n);proppairs.append({'left':{'id':e['id'],'sha256':h(e['currentCard'])},'right':{'id':c['id'],'sha256':h(c),'state':'UNAPPLIED_UNQUALIFIED_'+a['status']},'leftToRight':e['sixLiteralCanonicalGroups'][0]['individualGround']+' '+rightwhy,'rightToLeft':rightwhy+' These queries do not ask the same fact in reverse.','verdict':'DISTINCT_MAIN','directReverse':False})
save('peers.json',{'actualCurrentPeers':ps,'snapshotPath':str(D/'actual-current-books31-37-46-peers.json'),'snapshotRawSHA256':raw(D/'actual-current-books31-37-46-peers.json'),'bilateralMAINComparisons':pairs,'latestProposalSnapshots':props,'proposedBilateralMAINComparisons':proppairs,'unchangedMAINProof':'Both sides of reused INITIAL pairs checked literal prompt and correct-answer equality on full CURRENT snapshots; hashes rebound, not inherited from old peer snapshot.','source20Qualification':'READY is raw author status only. FRBR future source completion not assumed PASS; actual/current and proposed cards kept separate.'})
for e in entries:e['MAINComparisons']={'file':'peers.json','pairIndexes':[i for i,p in enumerate(pairs) if e['id'] in [p['left']['id'],p['right']['id']]],'proposalPairIndexes':[i for i,p in enumerate(proppairs) if p['left']['id']==e['id']],'fullCardLookup':'actualCurrentPeers/latestProposalSnapshots exact id+canonical sha','result':'DISTINCT_MAIN; own prior substantive analysis reused only under verified unchanged MAIN.'}
sourceprior=j(PRE/'sources.json')['sources'];used=set()
for e in entries:
 for g in e['sixLiteralCanonicalGroups']:
  for r in g['sourcesLocators']:used.add(r['path'])
sources=[]
for p in sorted(used):
 prev=next((s for s in sourceprior if s['path']==p),None)
 if prev:
  assert raw(p)==prev['rawReadSHA256'];s=copy.deepcopy(prev);s['FINALReadEvidence']='Same retained bytes personally read earlier in this uncompacted reviewer chat; unchanged-field substantive claims reused. FINAL wholecard4variants reread. Changed LOC/DCRMR entry passages specifically reread for corrected extra facts.'
 else:s={'path':p,'rawReadSHA256':raw(p),'url':'https://bsc.rbms.info/DCRMR/glossary/','locator':'Glossary #impression/#state complete definitions','personalReadEvidence':'Read full retained glossary in INITIAL and re-read complete relevant entries in FINAL.','limitations':'Full HTML retained; no new network fetch.'}
 sources.append(s)
save('sources.json',{'sources':sources,'changedFieldGrounds':[{'sourceOrder':e['sourceOrder'],'resolution':e['resolutionAssessment']} for e in entries],'reusedOwnINITIAL':{'path':str(PRE/'receipt.json'),'rawSHA256':raw(PRE/'receipt.json'),'notAuthorInheritance':True},'scopeLimitation':'No claims about unassigned pending43/47 correctness; no new network fetch when full relevant retained context exists.'})
receipt={'stage':'FINAL','scope':[31,37,46],'catalogCommitAssigned':'4f04bfe34793eeae25b6a1276cc65651212203e8','sourceFreezeAssigned':'b39fe7aba21f2f9838fd3bd3d0e8f2d4e1fc55e4','reviewDate':'2026-10-16','cycle':'same solecycle1','qualityCredit':0,'entries':entries,'summary':{'PASS':[31,37,46],'HOLD':[]},'rootBinding':'Required before any CURRENT quality credit'};save('receipt.json',receipt)
qa=D/'qa-books31-37-46-cycle1-source37.json';q=j(qa)
save('verification.json',{'catalogPath':str(cp),'catalogRawSHA256':raw(cp),'existingQA19':{'path':str(qa),'rawSHA256':raw(qa),'numPassedTests':q['numPassedTests'],'success':q['success'],'rerun':False},'cardBindings':[{'id':e['id'],'sourceOrder':e['sourceOrder'],'canonicalSHA256':h(e['currentCard']),'exactAppliedCURRENT':True,'MAINunchangedFromOwnINITIAL':True} for e in entries],'computedTotals':{'cards':3,'literalGroups':18,'wholePromptAnswerNoteTriples':12,'actualCurrentFullPeers':len(ps),'reusedReboundBilateralPairs':len(pairs),'unappliedProposalBilateralPairs':len(proppairs)},'hashMethod':'SHA256 UTF8 json.dumps sort_keys=True,separators=(comma,colon),ensure_ascii=False; triples exactly{prompt,answer,note}','prohibitedActionsNotRun':['catalog/Git/index/ref/status/planning/claim mutations','tests','runtime/browserplaytest','build/deploy','new actors'],'qualityCredit':0})
save('checkpoint.json',{'stage':'FINAL','status':'PASS31_37_46_COMPLETE_AWAITING_ROOT_BINDING','PASSready':[31,37,46],'HOLD':[],'qualityCredit':0,'next':'Coordinator preserve exact owned packet via private Git and bind eligible PASS31/37/46.43/47 remain separate pending SOURCE task; no secondordinarycycle.','preservation':'No own tests/runtime/tmp/build processes or artifacts; retained receipts/source links/scripts are durable evidence. Git commit forbidden for reader; root preservation pending.','sessionBoundaryAudit':'session-boundary-audit.json'})
print(receipt['summary'],'MAINpairs',len(pairs),'proposalpairs',len(proppairs),'sources',len(sources))
