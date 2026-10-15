import json,pathlib,hashlib,subprocess,importlib.util,re
C=pathlib.Path(__file__).resolve().parents[4];P=pathlib.Path('/Users/eaafonasev/Projects/mindbattle-planning');B=C/'docs/content-audits/question-quality-wave-7/process-v2-maps71-80-01a13d50/author-cycle1-01a13e5e'
def read(p):return json.loads(p.read_text())
def sha(v):return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def raw(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
a=read(B/'candidate.json');s=read(B/'sourceproof.json');peers=read(B/'peer-snapshot.json');topicp=C/'src/content/topics/maps-cartography.json';topic=read(topicp);byid={q['id']:q for q in topic['questions']};cp=read(P/'openspec/changes/question-quality-future-waves/current-checkpoint.json');sel={e['questionId']:e for e in cp['selectedCards']};proof={e['id']:e for e in s['cards']};assert len(a['entries'])==7
sources=[]
for src in s['sourceRegister']:
 p=C/src['path'];assert p.is_file() and raw(p)==src['rawSHA256'];sources.append({'path':src['path'],'rawSHA256':raw(p)})
for src in s['newCaptures']:
 p=C/src['path'];assert src['completeFullPage'] and p.is_file() and raw(p)==src['rawReadBytesSHA256']
 text=p.read_text();anchors=set(int(n) for n in re.findall(r'\bL(\d+):',text));assert anchors==set(range(src['totalLines'])),(src['id'],len(anchors),src['totalLines'])
for e in peers['targets']:
 assert byid[e['id']]==e['currentCard'] and sha(byid[e['id']])==e['currentSHA256']
# Additional hard peer evidence is checked and retained verbatim alongside the full CURRENT/apply receipt.
bindings=[];applied=[]
for e in [v for v in a['entries'] if v['sourceOrder'] in [76,77]]:
 i=e['id'];before=byid[i];c=e['proposedCard'];p=proof[i];assert e['status']=='FIX';assert before==e['beforeCard'] and sha(before)==e['beforeSHA256'];assert sha(c)==e['proposedSHA256']==p['proposedCardSHA256'];assert c['id']==i and c['difficulty']==sel[i]['difficulty'] and c['correctIndex']==sel[i]['correctIndex'];assert topic['questions'][e['sourceOrder']-1]['id']==i
 groups={'prompt_ordered_answers_key':{'prompt':c['prompt'],'answers':[v['text'] for v in c['answers']],'correctIndex':c['correctIndex']},'explanation':c['explanation'],**{'note'+str(k):v['note'] for k,v in enumerate(c['answers'])}}
 assert len(p['sixLiteralGroups'])==6 and {g['group'] for g in p['sixLiteralGroups']}==set(groups)
 for g in p['sixLiteralGroups']:assert g['literal']==groups[g['group']] and g['sha256']==sha(g['literal'])
 assert len(p['fourSubstitutions'])==4 and {v['slot'] for v in p['fourSubstitutions']}==set(range(4))
 for v in p['fourSubstitutions']:
  k=v['slot'];assert v['rationale'];triple={'prompt':c['prompt'],'answer':c['answers'][k]['text'],'note':c['answers'][k]['note']};bindings.append({'id':i,'answerIndex':k,**triple,'tripleSHA256':sha(triple),'authorRationale':v['rationale']})
 for ans in c['answers']:assert len(ans['text'].encode('utf-16-le'))//2<=140 and len(ans['note'].split())<=35
 applied.append({'id':i,'topicId':'maps-cartography','sourceOrder':e['sourceOrder'],'beforeSHA256':sha(before),'proposedSHA256':sha(c),'beforeCard':before,'proposedCard':c})
# Exact current hashes of all previously certified IDs must stay valid before mutation.
for e in cp['completedCardHashes']:
 if e['questionId'] in byid:assert sha(byid[e['questionId']])==e['cardCanonicalSha256']
oldbytes=topicp.read_bytes();newby={e['id']:e['proposedCard'] for e in applied};topic['questions']=[newby.get(q['id'],q) for q in topic['questions']];write(topicp,topic)
for q in topic['questions']:
 if q['id'] not in newby:assert q==byid[q['id']]
out=C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-cycle1-76-77.json';write(out,{'stage':'solecycle1 CURRENT2 easy76–77 pending affected19 and retained independent reader36; hard71–75 not applied, peer qualification pending','authorNativeId':'01a13e63-3568-70d1-bc76-88e6628dcb42','baseline':a['baselineCommit'],'authorPath':str(B.relative_to(C)),'applied':applied,'bindings8':bindings,'sources':sources,'qualityCredit':0,'qaSelection':{'command':'node node_modules/vitest/vitest.mjs run tests/unit/catalog-topics.test.ts tests/unit/content.test.ts tests/unit/content-answer-notes.test.ts --reporter=json --outputFile=docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/qa-cycle1-76-77.json','reason':'Only2contentcards; catalogschema/uniqueIDs/textconstraints/answer-note contracts; no runtime/build/fullsuite'},'unrelatedCardsPreserved':True,'frozenIDtopicorderdifficultykey':True})
spec=importlib.util.spec_from_file_location('h',P/'evidence/question-revision-process-v2/private-save-helper-01a13cb1.py');h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h);idx=C/h.git(C,'rev-parse','--git-path','index');files=[str((B/name).relative_to(C)) for name in ['candidate.json','sourceproof.json','peer-snapshot.json','needed-evidence.json','DRAFT.md','sources/define-projection-reader-full.txt','sources/project-reader-full.txt']]+[str(p.relative_to(C)) for p in (B/'history/preapply-returned').rglob('*') if p.is_file()]+[str(topicp.relative_to(C)),str(out.relative_to(C)),str(pathlib.Path(__file__).resolve().relative_to(C))];commit=h.save(C,'refs/heads/codex/question-quality-wave-6',files,'Apply sole cycle1 easy hill and valley cards pending independent',raw(idx));print('APPLIED2',commit,'qualityCredit0')
