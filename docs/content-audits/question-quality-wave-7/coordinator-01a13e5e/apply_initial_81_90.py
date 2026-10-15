import pathlib,json,hashlib,importlib.util
C=pathlib.Path(__file__).resolve().parents[4];P=pathlib.Path('/Users/eaafonasev/Projects/mindbattle-planning');B=C/'docs/content-audits/question-quality-wave-7/process-v2-maps81-90-01a13d50/author-qualification-01a13e5e';F=B/'remaining4-final'
def read(p):return json.loads(p.read_text())
def sha(v):return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def raw(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
a=read(B/'candidate.json');final=read(F/'candidate.json');source6=read(F/'evidence-addendum-ready6.json');source4=read(F/'sourceproof.json');assess4={x['id']:x for x in read(F/'assessments.json')['assessments']};six={x['id']:x for x in source6['cards']};four={x['id']:x for x in source4['entries']};entries=[x for x in a['entries'] if x['sourceOrder'] in [81,82,83,84,85,87]]+final['entries'];entries.sort(key=lambda x:x['sourceOrder']);assert len(entries)==10 and len(six)==6 and len(four)==4
p=C/'src/content/topics/maps-cartography.json';topic=read(p);current={x['id']:x for x in topic['questions']};beforeTopicSHA=raw(p);cp=read(P/'openspec/changes/question-quality-future-waves/current-checkpoint.json');selected={x['questionId']:x for x in cp['selectedCards']};sources=[]
for src in source6['rawSources']+source4['rawSources']:
 path=C/src['path'];assert path.is_file() and raw(path)==src['sha256'];sources.append({'path':src['path'],'rawSHA256':raw(path)})
for pp in [B/'peer-snapshot.json',F/'peer-snapshot.json']:
 for e in read(pp)['peers']:
  assert sha(e['card'])==e['sha256']
  if e['version']=='CURRENT':assert e['card']==current[e['card']['id']],e['card']['id']
bindings=[];applied=[]
for e in entries:
 i=e['id'];c=e['proposedCard'];before=current[i];assert e['status']=='FIX';assert before==e['beforeCard'] and sha(before)==e['beforeHash'];assert sha(c)==e['afterHash'];assert c['id']==i and c['difficulty']==selected[i]['difficulty'] and c['correctIndex']==selected[i]['correctIndex'];assert topic['questions'][e['sourceOrder']-1]['id']==i
 groups={'prompt_ordered_answers_key':{'prompt':c['prompt'],'answers':[v['text'] for v in c['answers']],'correctIndex':c['correctIndex']},'explanation':c['explanation'],**{'note'+str(k):v['note'] for k,v in enumerate(c['answers'])}}
 proof=six.get(i,four.get(i));gs=proof.get('sixLiteralGroups',proof.get('literalGroups'));assert len(gs)==6 and {g['group'] for g in gs}==set(groups)
 for g in gs:assert g['literal']==groups[g['group']] and g.get('canonicalSHA256',g.get('literalSHA256'))==sha(g['literal'])
 assessment=proof if i in six else assess4[i];assert assessment['fullPromptLiteral']==c['prompt'] and assessment['fullExplanationLiteral']==c['explanation'];variants=assessment['fullAnswersAndNotes'];assert len(variants)==4 and {v['slot'] for v in variants}==set(range(4))
 for v in variants:
  k=v['slot'];assert v['answerLiteral']==c['answers'][k]['text'] and v['noteLiteral']==c['answers'][k]['note'];assert v.get('answerJudgment',v.get('answerAssessment')) and v.get('noteJudgment',v.get('noteAssessment'));triple={'prompt':c['prompt'],'answer':v['answerLiteral'],'note':v['noteLiteral']};bindings.append({'id':i,'answerIndex':k,**triple,'canonicalSHA256':sha(triple),'authorAssessment':v})
 for ans in c['answers']:assert len(ans['text'].encode('utf-16-le'))//2<=140 and len(ans['note'].split())<=35
 applied.append({'id':i,'topicId':'maps-cartography','sourceOrder':e['sourceOrder'],'beforeCard':before,'beforeSHA256':sha(before),'proposedCard':c,'proposedSHA256':sha(c)})
for e in cp['completedCardHashes']:
 if e['questionId'] in current:assert sha(current[e['questionId']])==e['cardCanonicalSha256']
replacement={x['id']:x['proposedCard'] for x in applied};topic['questions']=[replacement.get(q['id'],q) for q in topic['questions']];write(p,topic)
for q in topic['questions']:
 if q['id'] not in replacement:assert q==current[q['id']]
out=C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-initial-81-90.json';write(out,{'stage':'INITIAL10 CURRENT pending affected19 and OTHER independent','authorNativeId':'01a13e66-1c13-71d3-8c00-86ff1c5251b1','baseline':a['baselineCommit'],'authorReady6':str((F/'evidence-addendum-ready6.json').relative_to(C)),'authorFinal4':str(F.relative_to(C)),'applied':applied,'variantBindings40':bindings,'rawSources':sources,'qualityCredit':0,'beforeTopicRawSHA256':beforeTopicSHA,'afterTopicRawSHA256':raw(p),'qaSelection':{'command':'node node_modules/vitest/vitest.mjs run tests/unit/catalog-topics.test.ts tests/unit/content.test.ts tests/unit/content-answer-notes.test.ts --reporter=json --outputFile=docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/qa-initial-81-90.json','reason':'Only10contentcards; schema/uniqueIDs/constraints/answer-note contracts; no runtime/build/fullsuite'},'verified':'60canonicalgroups40variants/frozenIDtopicorderdifficultykey/fullrawsources/actualpeerpreimages; oldfailedauthorhistorypreserved; existing682cardhashes unchanged'})
s=importlib.util.spec_from_file_location('h',P/'evidence/question-revision-process-v2/private-save-helper-01a13cb1.py');h=importlib.util.module_from_spec(s);s.loader.exec_module(h);idx=C/h.git(C,'rev-parse','--git-path','index');files=[str(f.relative_to(C)) for f in B.rglob('*') if f.is_file()]+[str(p.relative_to(C)),str(out.relative_to(C)),str(pathlib.Path(__file__).resolve().relative_to(C))];print('APPLIED10',h.save(C,'refs/heads/codex/question-quality-wave-6',files,'Apply qualified initial ten map-use cards pending independent',raw(idx)),'qualityCredit0')
