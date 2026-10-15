"""Exact standard packet application. Does not grant editorial quality credit."""
import pathlib,json,hashlib,importlib.util,subprocess
C=pathlib.Path(__file__).resolve().parents[4];P=pathlib.Path('/Users/eaafonasev/Projects/mindbattle-planning')
def read(p):return json.loads(pathlib.Path(p).read_text())
def sha(v):return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def raw(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def write(p,v):pathlib.Path(p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def fg_after(v):return v if isinstance(v,str) else v['afterCanonicalSHA256']
def read_issues(topic):
 p=pathlib.Path(__file__).parent/'validate-proposed-topic.cjs';return json.loads(subprocess.check_output(['node',str(p)],input=json.dumps(topic,ensure_ascii=False).encode()))
def apply(B,author,orders,out,qa,runner,peerAddendum=None,concerns=None,qualifyOnly=False,peerSnapshot=None):
 a=read(B/'candidate.json');sp=read(B/'sourceproof.json');ps={e['id']:e for e in sp['entries']};peers=peerSnapshot if peerSnapshot is not None else read(B/'peer-snapshot.json');topicId=a['entries'][0]['topicId'];tp=C/f'src/content/topics/{topicId}.json';topic=read(tp);current={q['id']:q for q in topic['questions']};cp=read(P/'openspec/changes/question-quality-future-waves/current-checkpoint.json');selected={e['questionId']:e for e in cp['selectedCards']};sources={s['path']:s for s in sp['rawSources']}
 for s in sources.values():assert raw(C/s['path'])==s['sha256']
 delta={p['id']:p for p in read(peerAddendum)['actualCurrentPeers']} if peerAddendum else {}
 for p in peers['actualCurrentPeers']:
  assert sha(p['card'])==p['sha256'];p=delta.get(p['id'],p);assert p['card']==current[p['id']] and sha(p['card'])==p['sha256']
 for p in delta.values():assert p['card']==current[p['id']] and sha(p['card'])==p['sha256']
 applied=[];groupbindings=[];variants=[]
 for e in a['entries']:
  if e['sourceOrder'] not in orders:continue
  i=e['id'];c=e['proposedCard'];p=dict(ps[i]);p['literalGroups']=p['literalGroups'] if 'literalGroups' in p else p['sixLiteralGroups'];assert e['status']=='READY_FOR_INDEPENDENT_REVIEW' and e['topicId']==topicId;assert current[i]==e['beforeCard'] and sha(current[i])==e['beforeHash'];assert sha(c)==e['afterHash'];assert c['id']==i and c['difficulty']==selected[i]['difficulty'] and c['correctIndex']==selected[i]['correctIndex'];assert topic['questions'][e['sourceOrder']-1]['id']==i and i not in cp['currentEligibleCompletedIds'];gs={'prompt_ordered_answers_key':{'prompt':c['prompt'],'answers':[v['text'] for v in c['answers']],'correctIndex':c['correctIndex']},'explanation':c['explanation'],**{'note'+str(k):v['note'] for k,v in enumerate(c['answers'])}};assert len(p['literalGroups'])==6 and {g['group'] for g in p['literalGroups']}==set(gs)
  for g in p['literalGroups']:assert g['literal']==gs[g['group']] and sha(g['literal'])==g['literalSHA256'] and (not isinstance(e['fieldGroups'],dict) or fg_after(e['fieldGroups'][g['group']])==g['literalSHA256']) and g['primaryGround'] and g['locator'];groupbindings.append({'id':i,**g})
  if isinstance(e['fieldGroups'],list) and all(isinstance(v,str) for v in e['fieldGroups']):
   b=e['beforeCard'];bg={'prompt_ordered_answers_key':{'prompt':b['prompt'],'answers':[v['text'] for v in b['answers']],'correctIndex':b['correctIndex']},'explanation':b['explanation'],**{'note'+str(k):v['note'] for k,v in enumerate(b['answers'])}};assert set(e['fieldGroups'])=={k for k in gs if gs[k]!=bg[k]}
  if isinstance(e['fieldGroups'],list) and any(isinstance(v,dict) for v in e['fieldGroups']):
   fg=e['fieldGroups'];assert len(fg)==6 and {g['group'] for g in fg}==set(gs)
   for g in fg:assert g['literal']==gs[g['group']] and sha(g['literal'])==g['literalSHA256']
  if isinstance(e['fieldGroups'],dict):
   assert set(e['fieldGroups'])==set(gs);b=e['beforeCard'];bg={'prompt_ordered_answers_key':{'prompt':b['prompt'],'answers':[v['text'] for v in b['answers']],'correctIndex':b['correctIndex']},'explanation':b['explanation'],**{'note'+str(k):v['note'] for k,v in enumerate(b['answers'])}}
   for k,v in e['fieldGroups'].items():
    if isinstance(v,dict):assert v['beforeCanonicalSHA256']==sha(bg[k]) and v['afterCanonicalSHA256']==sha(gs[k])
  vs=p['fourFullPromptAnswerNoteAssessments'];assert len(vs)==4 and {v['slot'] for v in vs}==set(range(4))
  # Repeated prose is a review signal, never a new lexical quality criterion.
  # Concrete claim-to-source and per-slot judgments remain a human/agent review gate.
  normalizedVariants=[]
  for original in vs:
   v=dict(original)
   if 'grammar' not in v and 'grammarAndPlausibility' in v:
    v['grammar']=v['grammarAndPlausibility'];v['plausibilityUniqueKeyAndNoteTruthUsefulness']={k:v[k] for k in ['judgement','whyKeyOrDistractor','grammarAndPlausibility','noteClaimAndTruthJudgement']};v['technicalFieldNormalization']='Exact existing grounded authorjudgementfields combined understandard assessment container; no semanticclaimchanged.'
   normalizedVariants.append(v)
  for v in normalizedVariants:
   k=v['slot'];tr={'prompt':c['prompt'],'answer':c['answers'][k]['text'],'note':c['answers'][k]['note']};assert v['fullPrompt']==tr['prompt'] and v['answer']==tr['answer'] and v['note']==tr['note'] and v['grammar'] and v['plausibilityUniqueKeyAndNoteTruthUsefulness'] and v['locator'];assert v['sourcePaths'] and all(x in sources for x in v['sourcePaths']);
   if 'tripleSHA256' in v:assert sha(tr)==v['tripleSHA256']
   variants.append({'id':i,'slot':k,**tr,'bindingCanonicalSHA256':sha(tr),'authorAssessment':v})
  assert len(c['prompt'].encode('utf-16-le'))//2<=320
  for v in c['answers']:assert len(v['text'].encode('utf-16-le'))//2<=140 and len(v['note'].split())<=35
  applied.append({'id':i,'sourceOrder':e['sourceOrder'],'beforeCard':current[i],'beforeSHA256':sha(current[i]),'proposedCard':c,'proposedSHA256':sha(c)})
 assert len(applied)==len(orders)
 for e in cp['completedCardHashes']:
  if e['questionId'] in current:assert sha(current[e['questionId']])==e['cardCanonicalSha256']
 replace={e['id']:e['proposedCard'] for e in applied};proposedTopic={**topic,'questions':[replace.get(q['id'],q) for q in topic['questions']]};issues=read_issues(proposedTopic);assert issues==[],issues
 if qualifyOnly:return {'author':author,'authorPacket':str(B.relative_to(C)),'topicId':topicId,'applied':applied,'finalGroupBindings':groupbindings,'finalVariantBindings':variants,'primarySources':sp['rawSources'],'actualPeerDelta':str(peerAddendum.relative_to(C)) if peerAddendum else None,'editorialConcernsForOTHER':concerns or [],'qualityCredit':0}
 topic=proposedTopic;write(tp,topic);write(out,{'stage':'AppliedexactauthorCURRENT pendingaffected19/OTHER','author':author,'authorPacket':str(B.relative_to(C)),'applied':applied,'finalGroupBindings':groupbindings,'finalVariantBindings':variants,'primarySources':sp['rawSources'],'actualPeerDelta':str(peerAddendum.relative_to(C)) if peerAddendum else None,'editorialConcernsForOTHER':concerns or [],'qualityCredit':0,'qaSelection':{'command':'node node_modules/vitest/vitest.mjs run tests/unit/catalog-topics.test.ts tests/unit/content.test.ts tests/unit/content-answer-notes.test.ts --reporter=json --outputFile='+str(qa.relative_to(C)),'reason':'Only affectedcontentcard changes; catalog schema, uniqueIDs, frozenkey/difficulty and notes. No runtime/build/fullsuite'}})
 s=importlib.util.spec_from_file_location('h',P/'evidence/question-revision-process-v2/private-save-helper-01a13cb1.py');h=importlib.util.module_from_spec(s);s.loader.exec_module(h);files=[str(p.relative_to(C)) for p in B.rglob('*') if p.is_file()]+[str(p.relative_to(C)) for p in [tp,out,pathlib.Path(__file__).resolve(),pathlib.Path(__file__).parent/'validate-proposed-topic.cjs',runner]];print(h.save(C,'refs/heads/codex/question-quality-wave-6',files,f'Apply exact standard author CURRENT{len(applied)} {topicId}',raw(C/h.git(C,'rev-parse','--git-path','index'))))
