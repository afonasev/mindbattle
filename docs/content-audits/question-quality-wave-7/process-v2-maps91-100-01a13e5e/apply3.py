import pathlib,json,hashlib,importlib.util
C=pathlib.Path(__file__).resolve().parents[4];P=pathlib.Path('/Users/eaafonasev/Projects/mindbattle-planning');B=pathlib.Path(__file__).parent/'author/qualified/final'
read=lambda p:json.loads(p.read_text())
def sha(v):return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def raw(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
a=read(B/'candidate.json');sp=read(B/'sourceproof.json');proof={x['id']:x for x in sp['cards']};peers=read(B/'peer-snapshot.json');topicp=C/'src/content/topics/maps-cartography.json';topic=read(topicp);current={q['id']:q for q in topic['questions']};cp=read(P/'openspec/changes/question-quality-future-waves/current-checkpoint.json');selected={e['questionId']:e for e in cp['selectedCards']};ready=[e for e in a['entries'] if e['status']=='READY_FOR_INDEPENDENT_REVIEW'];assert len(ready)==3
for src in sp['sourceRegister']:assert raw(C/src['path'])==src['rawReadBytesSHA256']
for e in peers['actualCurrentPeers']:assert current[e['id']]==e['card'] and sha(e['card'])==e['sha256']
applied=[];bindings=[];groupbindings=[];technicalRebindings=[]
for e in ready:
 i=e['id'];c=e['proposedCard'];p=proof[i];assert current[i]==e['beforeCard'] and sha(current[i])==e['beforeSHA256'];assert sha(c)==e['proposedSHA256']==p['proposedCardSHA256'];assert c['id']==i and c['difficulty']==selected[i]['difficulty'] and c['correctIndex']==selected[i]['correctIndex'];assert topic['questions'][e['sourceOrder']-1]['id']==i;assert i not in cp['currentEligibleCompletedIds']
 gs={'prompt_ordered_answers_key':{'prompt':c['prompt'],'answers':[v['text'] for v in c['answers']],'correctIndex':c['correctIndex']},'explanation':c['explanation'],**{'note'+str(k):v['note'] for k,v in enumerate(c['answers'])}};assert len(p['sixLiteralGroups'])==6 and {g['group'] for g in p['sixLiteralGroups']}==set(gs)
 for g in p['sixLiteralGroups']:assert g['literal']==gs[g['group']] and sha(g['literal'])==g['canonicalSHA256']
 vs=[dict(v) for v in p['fourSubstitutions']]
 for v in vs:
  k=v['answerSlot']-1
  if v['note']!=c['answers'][k]['note']:
   assert k==3 and p['correctNoteNewFact'] and v['locators']
   prior=next(x for x in read(B.parent/'sourceproof.json')['cards'] if x['id']==i)
   assert v['note']==prior['fourSubstitutions'][k]['note']
   finalNote=next(g for g in p['sixLiteralGroups'] if g['group']=='note3');assert finalNote['literal']==c['answers'][k]['note'] and sha(finalNote['literal'])==finalNote['canonicalSHA256']
   technicalRebindings.append({'id':i,'slot':k,'oldStaleAuthorLiteral':v['note'],'finalAuthorLiteral':finalNote['literal'],'authorCorrectNoteNewFact':p['correctNoteNewFact'],'authorSourceLocators':v['locators'],'basis':'Only stale substitution-note literal normalized to final author candidate AND final six-group literal and explicit author new-fact statement. Original evidence remains unchanged; no semantic assertion invented.'})
   v['note']=finalNote['literal'];v['authorCorrectNoteNewFact']=p['correctNoteNewFact']
 assert len(vs)==4 and {v['answerSlot'] for v in vs}=={1,2,3,4}
 for v in vs:
  k=v['answerSlot']-1;assert v['fullPrompt']==c['prompt'] and v['answer']==c['answers'][k]['text'] and v['note']==c['answers'][k]['note'];assert all(v['grounds'][x] for x in ['grammarGround','plausibilityGround','truthAndUniqueKeyGround','noteUsefulnessGround']) and v['sourcePaths'] and v['locators'];tr={'prompt':c['prompt'],'answer':v['answer'],'note':v['note']};bindings.append({'id':i,'answerIndex':k,**tr,'canonicalSHA256':sha(tr),'authorAssessment':v})
 for group,literal in gs.items():
  vv=vs if group in ['prompt_ordered_answers_key','explanation'] else [vs[int(group[-1])]];groupbindings.append({'id':i,'group':group,'literal':literal,'canonicalSHA256':sha(literal),'bindingMethod':'Mechanical binding of existing author per-slot semantic grounds and exact source locators, no additional quality inference','authorGrounds':[v['grounds'] for v in vv],'sourcePaths':sorted({x for v in vv for x in v['sourcePaths']}),'sourceLocators':sorted({x for v in vv for x in v['locators']})})
 assert len(c['prompt'].encode('utf-16-le'))//2<=320
 for ans in c['answers']:assert len(ans['text'].encode('utf-16-le'))//2<=140 and len(ans['note'].split())<=35
 applied.append({'id':i,'sourceOrder':e['sourceOrder'],'beforeCard':current[i],'beforeSHA256':sha(current[i]),'proposedCard':c,'proposedSHA256':sha(c)})
for e in cp['completedCardHashes']:
 if e['questionId'] in current:assert sha(current[e['questionId']])==e['cardCanonicalSha256']
replace={e['id']:e['proposedCard'] for e in applied};topic['questions']=[replace.get(q['id'],q) for q in topic['questions']];write(topicp,topic)
for q in topic['questions']:
 if q['id'] not in replace:assert q==current[q['id']]
out=pathlib.Path(__file__).parent/'apply-initial3-92-93-95.json';write(out,{'stage':'INITIALCURRENT3 pending affected19andOTHER','authorNativeId':'01a13e77-59ef-7673-a3dc-32a4f701f292','authorFinalPath':str(B.relative_to(C)),'baseline':a['baselineCommit'],'applied':applied,'finalVariantBindings12':bindings,'finalGroupBindings18':groupbindings,'qualityCredit':0,'technicalFinalNoteRebindings':technicalRebindings,'sourceRegister':sp['sourceRegister'],'otherSeven':'AuthorHOLD0credit, exact frozen oldcatalog versions retained; not independently reviewed or applied','qaSelection':{'command':'node node_modules/vitest/vitest.mjs run tests/unit/catalog-topics.test.ts tests/unit/content.test.ts tests/unit/content-answer-notes.test.ts --reporter=json --outputFile=docs/content-audits/question-quality-wave-7/process-v2-maps91-100-01a13e5e/qa-initial3-92-93-95.json','reason':'Only3contentcards schema/uniqueIDs/constraints/notes; no runtime/build/fullsuite'}})
s=importlib.util.spec_from_file_location('h',P/'evidence/question-revision-process-v2/private-save-helper-01a13cb1.py');h=importlib.util.module_from_spec(s);s.loader.exec_module(h);idx=C/h.git(C,'rev-parse','--git-path','index');files=[str(p.relative_to(C)) for p in (pathlib.Path(__file__).parent/'author').rglob('*') if p.is_file()]+[str(topicp.relative_to(C)),str(out.relative_to(C)),str(pathlib.Path(__file__).resolve().relative_to(C))];print('APPLIED3',h.save(C,'refs/heads/codex/question-quality-wave-6',files,'Apply initial map generalization classification label CURRENT3 after qualification',raw(idx)),'qualityCredit0')
