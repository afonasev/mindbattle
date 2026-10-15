import pathlib,json,hashlib,importlib.util
C=pathlib.Path(__file__).resolve().parents[4];P=pathlib.Path('/Users/eaafonasev/Projects/mindbattle-planning');D=pathlib.Path(__file__).parent;B=D/'author-cycle1-01a13e5e';read=lambda p:json.loads(p.read_text())
def sha(v):return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def raw(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
a=read(B/'candidate.json');sp=read(B/'sourceproof.json');ad=read(B/'proof-variants-addendum.json');proof={e['id']:e for e in ad['entries']};topicp=C/'src/content/topics/engineering-machines.json';topic=read(topicp);current={q['id']:q for q in topic['questions']};cp=read(P/'openspec/changes/question-quality-future-waves/current-checkpoint.json');selected={e['questionId']:e for e in cp['selectedCards']}
for s in sp['primarySources']+ad['sourceFiles']:assert raw(C/s['path'])==s['rawBytesSHA256']
for e in read(B/'peer-snapshot.json')['relevantCurrentEngineeringNeighbors']:assert current[e['id']]==e['fullCard'] and sha(e['fullCard'])==e['canonicalSHA256']
applied=[]
for e in a['entries']:
 i=e['id'];c=e['proposedCard'];assert e['status']=='READY_FOR_INDEPENDENT_REVIEW' and current[i]==e['beforeCard'] and sha(current[i])==e['beforeCanonicalSHA256'];assert sha(c)==e['proposedCanonicalSHA256']==proof[i]['proposedFullCardCanonicalSHA256'];assert c['difficulty']==selected[i]['difficulty'] and c['correctIndex']==selected[i]['correctIndex'] and c['id']==i;assert topic['questions'][e['sourceOrder']-1]['id']==i and i not in cp['currentEligibleCompletedIds'];gs={'prompt_ordered_answers_key':{'prompt':c['prompt'],'answers':[v['text'] for v in c['answers']],'correctIndex':c['correctIndex']},'explanation':c['explanation'],**{'note'+str(k):v['note'] for k,v in enumerate(c['answers'])}};assert len(e['sixLiteralGroups'])==6 and {g['group'] for g in e['sixLiteralGroups']}==set(gs)
 for g in e['sixLiteralGroups']:assert gs[g['group']]==g['after'] and sha(g['after'])==g['afterCanonicalSHA256']
 assert len(proof[i]['slots'])==4 and {v['slot'] for v in proof[i]['slots']}==set(range(4))
 for v in proof[i]['slots']:
  k=v['slot'];tr={'prompt':c['prompt'],'answer':c['answers'][k]['text'],'note':c['answers'][k]['note']};assert v['fullPrompt']==tr['prompt'] and v['fullAnswer']==tr['answer'] and v['fullNote']==tr['note'] and sha(tr)==v['tripleCanonicalSHA256']
 assert len(c['prompt'].encode('utf-16-le'))//2<=320
 for v in c['answers']:assert len(v['text'].encode('utf-16-le'))//2<=140 and len(v['note'].split())<=35
 applied.append({'id':i,'sourceOrder':e['sourceOrder'],'beforeCard':current[i],'beforeSHA256':sha(current[i]),'proposedCard':c,'proposedSHA256':sha(c),'sixLiteralGroups':e['sixLiteralGroups'],'finalFourVariants':proof[i]['slots']})
assert len(applied)==2
for e in cp['completedCardHashes']:
 if e['questionId'] in current:assert sha(current[e['questionId']])==e['cardCanonicalSha256']
replace={e['id']:e['proposedCard'] for e in applied};topic['questions']=[replace.get(q['id'],q) for q in topic['questions']];write(topicp,topic);out=D/'apply-cycle1two.json';write(out,{'stage':'solecycle1CURRENT2 pending affected19andFINALOTHER','author':'01a13ec5-dca5-7db3-b6b7-b1303219898c','authorPath':str(B.relative_to(C)),'applied':applied,'qualityCredit':0,'primarySources':sp['primarySources'],'proofAmendment':'Originalgeneric per-slot grounds preserved; individual8 addendum bound, no content changes. Pulley ideal-equal-tension inference explicitly labeled and remains independently adjudicated.','qaSelection':{'command':'node node_modules/vitest/vitest.mjs run tests/unit/catalog-topics.test.ts tests/unit/content.test.ts tests/unit/content-answer-notes.test.ts --reporter=json --outputFile=docs/content-audits/question-quality-wave-8/process-v2-engineering1-10-01a13e5e/qa-cycle1two.json','reason':'Only2simplemachinecontentcards; schema catalog key/difficulty/note constraints; no runtime/full/build'}})
s=importlib.util.spec_from_file_location('h',P/'evidence/question-revision-process-v2/private-save-helper-01a13cb1.py');h=importlib.util.module_from_spec(s);s.loader.exec_module(h);files=[str(p.relative_to(C)) for p in B.rglob('*') if p.is_file()]+[str(p.relative_to(C)) for p in [topicp,out,pathlib.Path(__file__).resolve()]];print(h.save(C,'refs/heads/codex/question-quality-wave-6',files,'Apply solecycle1 pulley and wheel axle CURRENT2 with individual8 source proofs',raw(C/h.git(C,'rev-parse','--git-path','index'))))
