import pathlib,json,hashlib,importlib.util,datetime
C=pathlib.Path(__file__).resolve().parents[4];P=pathlib.Path('/Users/eaafonasev/Projects/mindbattle-planning');D=pathlib.Path(__file__).parent
read=lambda p:json.loads(p.read_text())
def sha(v):return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def raw(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
A=C/'docs/content-audits/question-quality-wave-7/process-v2-maps81-90-01a13d50/author-cycle1-01a13e5e/final';B=C/'docs/content-audits/question-quality-wave-7/process-v2-terminal-hard3-new-solution-01a13e5e/author/final';topicp=C/'src/content/topics/maps-cartography.json';topic=read(topicp);current={q['id']:q for q in topic['questions']};cp=read(P/'openspec/changes/question-quality-future-waves/current-checkpoint.json');selected={e['questionId']:e for e in cp['selectedCards']};allApplied=[];bundles=[]
for base,kind in [(A,'solecycle1-five'),(B,'concrete-NEW-three')]:
 a=read(base/'candidate.json');proof=read(base/'sourceproof.json');ps={x['id']:x for x in proof['entries' if base==A else 'cards']};peers=read(base/('peer-current-final6-addendum.json' if base==A else 'peer-snapshot.json'));sources=proof['rawSources' if base==A else 'sourceRegister']
 for s in sources:assert raw(C/s['path'])==s['sha256' if base==A else 'rawSHA256'],s['path']
 for p in peers['currentPeers' if base==A else 'currentRelevantCards']:
  assert current[p['id']]==p['card'];assert sha(p['card'])==p['currentCanonicalSHA256' if base==A else 'canonicalSHA256']
 eligible=[e for e in a['entries'] if not (base==A and e['id']=='maps-cartography-area-distortion')];assert len(eligible)==(5 if base==A else 3)
 applied=[];variants=[];groups=[]
 for e in eligible:
  i=e['id'];c=e['proposedCard'];p=ps[i];assert current[i]==e['beforeCard'];assert sha(current[i])==e['beforeHash' if base==A else 'beforeCanonicalSHA256'];assert sha(c)==e['afterHash' if base==A else 'proposedCanonicalSHA256'];assert c['id']==i and c['difficulty']==selected[i]['difficulty'] and c['correctIndex']==selected[i]['correctIndex'];assert topic['questions'][e['sourceOrder']-1]['id']==i;assert i not in cp['currentEligibleCompletedIds']
  gs={'prompt_ordered_answers_key':{'prompt':c['prompt'],'answers':[v['text'] for v in c['answers']],'correctIndex':c['correctIndex']},'explanation':c['explanation'],**{'note'+str(k):v['note'] for k,v in enumerate(c['answers'])}}
  gl=p['literalGroups' if base==A else 'sixLiteralGroups'];assert len(gl)==6 and {g['group'] for g in gl}==set(gs)
  for g in gl:assert g['literal']==gs[g['group']] and sha(g['literal'])==g['literalSHA256' if base==A else 'sha256'];groups.append({'id':i,**g})
  vl=p['fourFullPromptAnswerNoteAssessments' if base==A else 'fourSubstitutions'];assert len(vl)==4 and {v['slot'] for v in vl}==set(range(4))
  for v in vl:
   k=v['slot'];assert v['answer' if base==A else 'finalText']==c['answers'][k]['text'] and v['note' if base==A else 'finalNote']==c['answers'][k]['note']
   if base==A:assert v['fullPrompt']==c['prompt'] and v['grammar'] and v['plausibilityUniqueKeyAndNoteTruthUsefulness'] and v['locator']
   else:assert v['assessment']
   tr={'prompt':c['prompt'],'answer':c['answers'][k]['text'],'note':c['answers'][k]['note']};variants.append({'id':i,'slot':k,**tr,'bindingCanonicalSHA256':sha(tr),'authorAssessment':v,'binding':'Exact final author fullcard+sixgroup+slot binding; NEW3 source assessment implicitly fullprompt via complete proposedCardSHA256, explicitly materialized here'})
  assert len(c['prompt'].encode('utf-16-le'))//2<=320,(i,len(c['prompt']))
  for v in c['answers']:assert len(v['text'].encode('utf-16-le'))//2<=140 and len(v['note'].split())<=35
  applied.append({'id':i,'sourceOrder':e['sourceOrder'],'beforeCard':current[i],'beforeSHA256':sha(current[i]),'proposedCard':c,'proposedSHA256':sha(c),'route':kind})
 bundles.append({'route':kind,'authorNativeId':'01a13e9d-1924-76d2-b2ce-91137ee914f1' if base==A else '01a13eaa-35b2-7083-be8b-17c6531ab714','authorPath':str(base.relative_to(C)),'applied':applied,'finalGroups':groups,'finalVariants':variants,'sourceRegister':sources,'qualityCredit':0});allApplied+=applied
for e in cp['completedCardHashes']:
 if e['questionId'] in current:assert sha(current[e['questionId']])==e['cardCanonicalSha256']
replace={e['id']:e['proposedCard'] for e in allApplied};assert len(replace)==8
for q in topic['questions']:
 if q['id'] in replace:q.update(replace[q['id']])
write(topicp,topic);out=D/'apply-cycle1five-newthree.json';write(out,{'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'bundles':bundles,'authorHOLD88':'Not applied, prior CURRENT retained, terminal solecycle1 authorHOLD0','oldTerminal71_73_74':'Preserved independently; concrete NEW coordinate/numeric-demand solution needs fresh INITIAL reader, no inheritedPASS','preapplyPeerSnapshot':'Both author actualCURRENT peer snapshots validated before joint atomic8 apply. FINAL proposals now coexist; reader must check actual CURRENT and all changed peer dependencies.','qaSelection':{'command':'node node_modules/vitest/vitest.mjs run tests/unit/catalog-topics.test.ts tests/unit/content.test.ts tests/unit/content-answer-notes.test.ts --reporter=json --outputFile=docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/qa-cycle1five-newthree.json','reason':'8contentcard changes; catalog schema IDs frozenkey difficulty and note limits affected; no runtime/build/fullsuite'},'qualityCredit':0})
s=importlib.util.spec_from_file_location('h',P/'evidence/question-revision-process-v2/private-save-helper-01a13cb1.py');h=importlib.util.module_from_spec(s);s.loader.exec_module(h);files=[str(p.relative_to(C)) for base in [A,B] for p in base.rglob('*') if p.is_file()]+[str(topicp.relative_to(C)),str(out.relative_to(C)),str(pathlib.Path(__file__).resolve().relative_to(C))];print(h.save(C,'refs/heads/codex/question-quality-wave-6',files,'Apply solecycle1 maps5 and concrete NEW hard3 with exact source variant bindings',raw(C/h.git(C,'rev-parse','--git-path','index'))))
