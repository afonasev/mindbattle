import pathlib,json,hashlib,importlib.util,re
C=pathlib.Path(__file__).resolve().parents[4];P=pathlib.Path('/Users/eaafonasev/Projects/mindbattle-planning');B=pathlib.Path(__file__).parent/'author/source-recovered/qualified-notes';S=B.parent
read=lambda p:json.loads(p.read_text())
def sha(v):return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def raw(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
a=read(B/'candidate.json');proof={e['id']:e for e in read(B/'sourceproof.json')['cards']};peers=read(B/'peer-snapshot.json');topicp=C/'src/content/topics/engineering-machines.json';topic=read(topicp);current={q['id']:q for q in topic['questions']};selected={e['questionId']:e for e in read(P/'openspec/changes/question-quality-future-waves/current-checkpoint.json')['selectedCards']};assert len(a['entries'])==4
sources=[]
for line in (B/'sourceRegister.jsonl').read_text().splitlines():
 src=json.loads(line);p=pathlib.Path(src['publicToolOutputPath']);assert p.is_file() and raw(p)==src['rawFileSHA256'];full=pathlib.Path(src['fullPublicToolOutputPath']);assert raw(full)==src['fullPublicToolOutputSHA256'];anchors={int(n) for n in re.findall(r'\bL(\d+):',p.read_text())};end=int(src['locatorSpan'].split('-L')[-1]);assert anchors==set(range(end+1)),(p,len(anchors),end);sources.append({'path':str(p.relative_to(C)),'rawSHA256':raw(p),'fullPublicOutput':str(full.relative_to(C)),'fullPublicSHA256':raw(full)})
for e in peers['currentCards']:assert current[e['id']]==e['card'] and sha(e['card'])==e['canonicalSHA256']
applied=[];bindings=[]
for e in a['entries']:
 i=e['id'];c=e['proposedCard'];p=proof[i];assert e['status']=='READY';assert e['beforeCard']==current[i] and sha(current[i])==e['beforeSHA256'];assert sha(c)==e['proposedSHA256']==p['proposedCardSHA256'];assert c['id']==i and c['difficulty']==selected[i]['difficulty'] and c['correctIndex']==selected[i]['correctIndex'];assert topic['questions'][e['sourceOrder']-1]['id']==i
 gs={'prompt_ordered_answers_key':{'prompt':c['prompt'],'answers':[v['text'] for v in c['answers']],'correctIndex':c['correctIndex']},'explanation':c['explanation'],**{'note'+str(k):v['note'] for k,v in enumerate(c['answers'])}};assert len(p['sixLiteralGroups'])==6 and {g['group'] for g in p['sixLiteralGroups']}==set(gs)
 for g in p['sixLiteralGroups']:
  assert g['literal']==gs[g['group']] and sha(g['literal'])==g['canonicalSHA256'];assert raw(S/g['sourceOutput'])==g['sourceFileSHA256'] and raw(S/g['sourcePageOutput'])==g['sourcePageOutputSHA256']
 assert len(p['fourSubstitutions'])==4 and {v['slot'] for v in p['fourSubstitutions']}==set(range(4))
 for v in p['fourSubstitutions']:
  k=v['slot'];assert v['fullPrompt']==c['prompt'] and v['answer']==c['answers'][k]['text'] and v['note']==c['answers'][k]['note'];assert v['grounds'] and v['primaryLocators'] and v['uniqueKey'] and v['usefulness'];tr={'prompt':c['prompt'],'answer':v['answer'],'note':v['note']};bindings.append({'id':i,'slot':k,**tr,'canonicalSHA256':sha(tr),'authorJudgment':v})
 assert len(c['prompt'].encode('utf-16-le'))//2<=320
 for ans in c['answers']:assert len(ans['text'].encode('utf-16-le'))//2<=140 and len(ans['note'].split())<=35
 applied.append({'id':i,'sourceOrder':e['sourceOrder'],'beforeCard':current[i],'beforeSHA256':sha(current[i]),'proposedCard':c,'proposedSHA256':sha(c)})
replace={e['id']:e['proposedCard'] for e in applied};topic['questions']=[replace.get(q['id'],q) for q in topic['questions']];write(topicp,topic)
for q in topic['questions']:
 if q['id'] not in replace:assert q==current[q['id']]
out=pathlib.Path(__file__).parent/'apply-initial4.json';write(out,{'stage':'INITIALCURRENT4pendingaffected19andOTHER','authorNativeId':'01a13e80-549f-78c1-9129-44030f2f9072','baseline':a['baselineCommit'],'authorPath':str(B.relative_to(C)),'applied':applied,'variantBindings16':bindings,'sources':sources,'qualityCredit':0,'verified':'24canonicalJSONgroups16actualvariants/fullYaleUMasssourcebyteSHA/all100actualpeerpreimages/6pairs12directions/frozenIDtopicorderdifficultykey/unchangedother96','qaSelection':{'command':'node node_modules/vitest/vitest.mjs run tests/unit/catalog-topics.test.ts tests/unit/content.test.ts tests/unit/content-answer-notes.test.ts --reporter=json --outputFile=docs/content-audits/question-quality-wave-8/process-v2-engineering1-10-01a13e5e/qa-initial4.json','reason':'Only4contentcards schema/uniqueIDs/notes constraints; no runtime/build/fullsuite'}})
spec=importlib.util.spec_from_file_location('h',P/'evidence/question-revision-process-v2/private-save-helper-01a13cb1.py');h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h);idx=C/h.git(C,'rev-parse','--git-path','index');files=[str(p.relative_to(C)) for p in (pathlib.Path(__file__).parent/'author').rglob('*') if p.is_file()]+[str(topicp.relative_to(C)),str(out.relative_to(C)),str(pathlib.Path(__file__).resolve().relative_to(C))];print('APPLIED4',h.save(C,'refs/heads/codex/question-quality-wave-6',files,'Apply initial engineering four after source and note qualification',raw(idx)),'qualityCredit0')
