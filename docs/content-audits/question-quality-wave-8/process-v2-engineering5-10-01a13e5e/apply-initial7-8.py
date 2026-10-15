import pathlib,json,hashlib,importlib.util
C=pathlib.Path(__file__).resolve().parents[4];P=pathlib.Path('/Users/eaafonasev/Projects/mindbattle-planning');D=pathlib.Path(__file__).parent;B=D/'author';read=lambda p:json.loads(p.read_text())
def sha(v):return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def raw(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
a=read(B/'candidate.json');sp=read(B/'sourceproof.json');proof={e['id']:e for e in sp['cards']};peer=read(B/'peer-snapshot.json');tp=C/'src/content/topics/engineering-machines.json';topic=read(tp);current={q['id']:q for q in topic['questions']};cp=read(P/'openspec/changes/question-quality-future-waves/current-checkpoint.json');selected={e['questionId']:e for e in cp['selectedCards']}
def resolve(p):
 q=C/p
 return q if q.exists() else B/p
for key,s in sp['sources'].items():assert raw(resolve(s['capturedPath']))==s['rawSHA256'] and raw(resolve(s['fullTextPath']))==s['fullTextSHA256']
for e in peer['currentCards']:assert current[e['id']]==e['card'] and sha(e['card'])==e['canonicalSHA256']
applied=[];variants=[];groupbindings=[];normalizations=[]
for e in a['entries']:
 if e['sourceOrder'] not in [7,8]:continue
 i=e['id'];c=e['proposedCard'];p=proof[i];assert current[i]==e['beforeCard'] and sha(current[i])==e['beforeSHA256']==p['beforeCanonicalSHA256'];assert sha(c)==e['proposedSHA256']==p['proposedCardSHA256'];assert c['id']==i and c['difficulty']==selected[i]['difficulty'] and c['correctIndex']==selected[i]['correctIndex'] and i not in cp['currentEligibleCompletedIds'];assert topic['questions'][e['sourceOrder']-1]['id']==i;gs={'prompt_ordered_answers_key':{'prompt':c['prompt'],'answers':[v['text'] for v in c['answers']],'correctIndex':c['correctIndex']},'explanation':c['explanation'],**{'note'+str(k):v['note'] for k,v in enumerate(c['answers'])}};assert len(p['sixLiteralGroups'])==6
 for g in p['sixLiteralGroups']:
  k=g['group'];literal=g['afterLiteral']
  if k=='prompt_ordered_answers_key':assert sha(literal)==g['afterCanonicalSHA256']
  else:
   assert g['literalEncoding']=='UTF-8 raw string' and hashlib.sha256(literal.encode()).hexdigest()==g['afterSHA256'];normalizations.append({'id':i,'group':k,'authorRawStringSHA256':g['afterSHA256'],'canonicalProcessLiteral':literal,'canonicalProcessSHA256':sha(literal),'reason':'Verify original raw-string checksum then compute required canonical JSON-string checksum. Same exact literal; original evidence preserved.'})
  if k=='prompt_ordered_answers_key':
   normalized={**literal,'answers':[v['text'] for v in literal['answers']]};assert normalized==gs[k];normalizations.append({'id':i,'group':k,'authorLiteral':literal,'authorRepresentationSHA256':sha(literal),'canonicalProcessLiteral':normalized,'canonicalProcessSHA256':sha(normalized),'reason':'Mechanical answer object wrappers removed to standard four text strings; original author evidence intact. Exactsameprompt/orderedtexts/key. No semantic assertion changed.'})
  else:assert literal==gs[k]
  groupbindings.append({'id':i,'group':k,'literal':gs[k],'canonicalSHA256':sha(gs[k]),'primaryClaims':g['specificPrimaryClaims']})
 vs=p['fourSubstitutions'];assert len(vs)==4 and {v['slot'] for v in vs}==set(range(4))
 for v in vs:
  k=v['slot'];tr={'prompt':c['prompt'],'answer':c['answers'][k]['text'],'note':c['answers'][k]['note']};assert v['fullPrompt']==tr['prompt'] and v['answer']==tr['answer'] and v['note']==tr['note'] and v['grounds'] and v['primaryLocators'] and v['grammar'] and v['plausibility'] and v['uniqueKey'] and v['usefulness'];variants.append({'id':i,'slot':k,**tr,'bindingCanonicalSHA256':sha(tr),'authorAssessment':v})
 assert len(c['prompt'].encode('utf-16-le'))//2<=320
 for v in c['answers']:assert len(v['text'].encode('utf-16-le'))//2<=140 and len(v['note'].split())<=35
 applied.append({'id':i,'sourceOrder':e['sourceOrder'],'beforeCard':current[i],'beforeSHA256':sha(current[i]),'proposedCard':c,'proposedSHA256':sha(c)})
assert len(applied)==2
for e in cp['completedCardHashes']:
 if e['questionId'] in current:assert sha(current[e['questionId']])==e['cardCanonicalSha256']
replace={e['id']:e['proposedCard'] for e in applied};topic['questions']=[replace.get(q['id'],q) for q in topic['questions']];write(tp,topic);out=D/'apply-initial7-8.json';write(out,{'stage':'INITIALCURRENT2nutrivet pendingaffected19/OTHER','author':'01a13ecd-517c-7080-8b18-9e9f02ced4f8','authorPacket':str(B.relative_to(C)),'applied':applied,'finalGroups12':groupbindings,'finalVariants8':variants,'technicalCanonicalRepresentationNormalizations':normalizations,'sourceRegister':sp['sources'],'qualityCredit':0,'qualification':'Onlyready7/8 fromcompleteINITIAL6 outcome.5/6returnedforactualuniqueeasyqualification,9/10sourceHOLDretained; no inheritedauthorquality. Bothfullsources/rawSHA and100actualengineeringpeers verified.','qaSelection':{'command':'node node_modules/vitest/vitest.mjs run tests/unit/catalog-topics.test.ts tests/unit/content.test.ts tests/unit/content-answer-notes.test.ts --reporter=json --outputFile=docs/content-audits/question-quality-wave-8/process-v2-engineering5-10-01a13e5e/qa-initial7-8.json','reason':'Only2contentcards; catalog schema IDs key/difficulty andnoteconstraints; no runtime/build/fullsuite'}})
s=importlib.util.spec_from_file_location('h',P/'evidence/question-revision-process-v2/private-save-helper-01a13cb1.py');h=importlib.util.module_from_spec(s);s.loader.exec_module(h);print(h.save(C,'refs/heads/codex/question-quality-wave-6',[str(p.relative_to(C)) for p in [tp,out,pathlib.Path(__file__).resolve()]],'Apply ready initial engineering nut rivet CURRENT2 with canonical group wrapper normalization',raw(C/h.git(C,'rev-parse','--git-path','index'))))
