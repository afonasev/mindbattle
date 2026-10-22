import json,hashlib,re
from pathlib import Path
C=Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle');D=C/'docs/content-audits/question-quality-wave-8/coordinator-01a16329';N='01a164f5-4b8d-7761-a3f7-0ec75266cb95'
def rd(p):return json.loads(Path(p).read_text())
def raw(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def sha(v):return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
T=rd(D/'reader-history-russia90-cycle1-final-task.json');O=Path(T['outputDirectory']);I=Path(T['previousIndependentInitial']).parent
r=rd(I/'receipt.json');s=rd(I/'sources.json');p=rd(I/'peers.json');v=rd(I/'verification.json');e=r['entries'][0];old=e['currentCard'];cat=rd(C/'src/content/topics/history-russia.json')['questions'];q=next(x for x in cat if x['id']==T['id']);assert sha(q)==T['cardHash']
copy=json.loads(json.dumps(q));copy['answers'][3]['note']=old['answers'][3]['note'];assert copy==old and q['answers'][3]['note']!=old['answers'][3]['note']
def ptr(file,pointer):return {'path':str((I/file).relative_to(C)),'rawSHA256':raw(I/file),'jsonPointer':pointer,'readerNativeId':N,'basis':'Same-reader personally assessed INITIAL; exact unchanged literal and applicable grounds retained, not inherited author judgment.'}
primary=s['sources'][0];body=rd(C/primary['path'])
for k in primary['completeOutputPointer'].strip('/').split('/'):body=body[int(k)] if isinstance(body,list) else body[k]
assert hashlib.sha256(body.encode()).hexdigest()==primary['completeOutputSHA256'];line55=next(line for line in body.splitlines() if line.startswith('L55: '));assert line55[5:].startswith(q['answers'][3]['note'][:-1]+', потерявшей флот и военно-морскую базу на Тихом океане.')
refs=e['sixLiteralCanonicalGroups'][-1]['sourcesLocators']
gs={'prompt_ordered_answers_key':{'prompt':q['prompt'],'answers':[a['text'] for a in q['answers']],'correctIndex':q['correctIndex']},'explanation':q['explanation'],**{'note'+str(i):a['note'] for i,a in enumerate(q['answers'])}}
for i,g in enumerate(e['sixLiteralCanonicalGroups']):
 g['literal']=gs[g['group']];g['canonicalSHA256']=sha(g['literal'])
 if g['group']=='note3':
  g['individualGround']='PASS directed FINAL: субъект исправлен с обороны на падение крепости. Лично повторно прочитан полный retained body L0–139, особенно L54–55: L54 описывает сопротивление/сковывание японских сил; L55 связывает именно падение с ходом войны и поражением России. Текущий literal точно передаёт этот отдельный дополнительный факт о Русско-японской войне и не приписывает поражение самой обороне. Справка грамматически корректна и полезна своему ключу.'
  g['directedResolutionOf']=ptr('receipt.json','/entries/0/defects/0')
 else:
  assert g['literal']==rd(I/'receipt.json')['entries'][0]['sixLiteralCanonicalGroups'][i]['literal'];g['retainedOwnInitialJudgment']=ptr('receipt.json',f'/entries/0/sixLiteralCanonicalGroups/{i}')
for i,t in enumerate(e['fourFullPromptAnswerNoteVariants']):
 tr={'prompt':q['prompt'],'answer':q['answers'][i]['text'],'note':q['answers'][i]['note']};t.update(tr);t['tripleCanonicalSHA256']=sha(tr)
 if i==3:
  t['noteTruthUsefulness']=next(g['individualGround'] for g in e['sixLiteralCanonicalGroups'] if g['group']=='note3');t['sourcesLocators']=refs;t['directedResolutionOf']=ptr('receipt.json','/entries/0/fourFullPromptAnswerNoteVariants/3');t['grammar']='«Во время Русско-японской войны происходила оборона Порт-Артура?» — согласованный родительный падеж. «Падение ... предопределило» — согласование среднего рода; причинный субъект теперь соответствует L55.'
 else:t['retainedOwnInitialJudgment']=ptr('receipt.json',f'/entries/0/fourFullPromptAnswerNoteVariants/{i}')
e.update(stage='FINAL',cycle=1,currentCard=q,currentCardCanonicalSHA256=sha(q),status='PASS',defects=[])
e['absoluteLevel']['retainedOwnInitialJudgment']=ptr('receipt.json','/entries/0/absoluteLevel');e['correctNoteExtraFact']={'status':'SUPPORTED','fact':'Падение Порт-Артура определило дальнейший ход Русско-японской войны и поражение России. Это дополнительная связь результата обороны с исходом войны сверх спрашиваемой принадлежности обороны к войне; совпадение с explanation не запрещено.','sourcesLocators':refs}
e['directedResolution']={'initialDefect':ptr('receipt.json','/entries/0/defects/0'),'result':'RESOLVED','onlyChangedLiteral':'note3','noNewInitialOrCycle2':True};r.update(stage='FINAL',catalogCommit=T['catalogCommit'],date='2026-10-23',qualityCredit=0)
for i,x in enumerate(s['sources']):
 assert raw(C/x['path'])==x['rawReadSHA256'];x['initialPersonalReadEvidence']=ptr('sources.json',f'/sources/{i}');x['reuseMeaning']='Same-reader full original contexts personally read in INITIAL; immutable raw/body hashes checked unchanged. No new fetch.'
 if i==0:x['personalReadEvidence']+=' FINAL90: лично повторно прочитан весь тот же retained body L0–139; L54/L55 разделяют оборону и падение. Исправленная note3 соответствует причинному субъекту L55.';x['locator']='turn1view0 L44, L54-L55'
s['directedScope']='FINAL90 solecycle1 note3 only. All previous source limitations persist; original SOURCE91 mechanicalFAIL/ENOSPC diagnostics neither altered nor cured by this verdict.'
for x in p['actualCurrentPeers']:
 current=next(z for z in rd(C/f"src/content/topics/{x['topicId']}.json")['questions'] if z['id']==x['id'])
 if current!=x['card']:assert x['id'] in [q['id'],'history-russia-kronstadt-year']
 x.update(card=current,canonicalSHA256=sha(current),fileSHA256=raw(C/f"src/content/topics/{x['topicId']}.json"))
by={x['id']:x for x in p['actualCurrentPeers']}
for i,pair in enumerate(p['bilateralMainComparisons']):
 for side in ['left','right']:
  x=pair[side];x['canonicalSHA256']=by[x['id']]['canonicalSHA256']
  if x['id']=='history-russia-kronstadt-year':x['MAIN']={'entity':'март 1921 года','relation':'датирует событие из предложенного ряда','value':'Кронштадтское восстание','context':'история России'}
 if pair['right']['id']=='history-russia-kronstadt-year':pair['bilateralGround']='Лично прочитан обновлённый полный actual CURRENT91: теперь «Какое из этих событий произошло в марте1921?» — Кронштадтское восстание. CURRENT90 по-прежнему спрашивает принадлежность обороны Порт-Артура к Русско-японской войне1904–1905. Изменён только квалификатор вопроса91, не его историческая сущность. Ни entity, ни relation/value/context с90 не совпадают; обратный MAIN90 не даёт вопрос о событии1921. Это проверка зависимости, не FINAL91.'
 else:pair['retainedOwnInitialJudgment']=ptr('peers.json',f'/bilateralMainComparisons/{i}');pair['continuedApplicability']='MAIN90 не изменён: поправлена только причинная справка, которая не превращает запрос принадлежности обороны к войне в MAIN о договоре/месяце начала/территориальном возврате/базе1955. Полные peer cards и hashes сверены unchanged.'
rows=[];bindings=[];hits=[]
for f in sorted((C/'src/content/topics').glob('*.json')):
 qs=rd(f)['questions'];bindings.append({'path':str(f.relative_to(C)),'rawSHA256':raw(f),'questionCount':len(qs)})
 for card in qs:
  row={'topicId':f.stem,'id':card['id'],'prompt':card['prompt'],'answers':[a['text'] for a in card['answers']],'correctIndex':card['correctIndex']};rows.append(row)
  if re.search(r'Порт.?Артур|Люйшун|Ляодун|Цусим|русско-япон',row['prompt']+' '+' '.join(row['answers']),re.I):hits.append(row)
p['globalMAINRetrieval'].update(rowsCanonicalSHA256=sha(rows),fileBindings=bindings,hits=hits);p['current91']='Actual cycle1 CURRENT91 personally read/refreshed solely as dependency; its own FINAL remains unassigned here.'
qa=rd(T['qa']);assert raw(T['qa'])==T['qaSHA256'] and qa['success'] and qa['numPassedTests']==19 and qa['numFailedTests']==qa['numPendingTests']==0
fs=list(Path('/Users/eaafonasev/.codex/sessions/2026/10/22').glob('*-'+N+'.jsonl'));assert len(fs)==1;jr=[json.loads(l) for l in fs[0].open()];assert [x['payload']['id'] for x in jr if x.get('type')=='session_meta']==[N];comp=sum(x.get('type')=='compacted' for x in jr);assert comp<2
v.update(catalogCommit=T['catalogCommit'],catalogRawSHA256=raw(C/'src/content/topics/history-russia.json'),currentCardCanonicalSHA256=sha(q),existingQA19={'path':str(Path(T['qa']).relative_to(C)),'rawSHA256':raw(T['qa']),'pass':19,'fail':0,'pending':0,'meaning':'Existing sharedcycle1 exact report hash-bound; no reviewer tests run and no inherited semantic PASS.'},actualCompactions=comp)
v['mechanicalChecks']['noteWordCounts']=[len(a['note'].split()) for a in q['answers']];v['directedDiff']={'only90Note3Changed':True,'actual91PromptRefreshed':True,'retainedOwnInitialReceipt':ptr('receipt.json','/entries/0'),'source91ProcedureDiagnostics':'Preserved; content/QA does not cure procedure.'};v['stage']='FINAL';v['status']='PASS';v['localMechanicalFailures']={'path':str((O/'original-mechanical-diagnostic.json').relative_to(C)),'rawSHA256':raw(O/'original-mechanical-diagnostic.json'),'exitCodes':[1,1],'meaning':'Two invalid exact-substring assertions preserved. Exact printed L55 established comma continuation versus note sentence period; corrected assertion binds exact source clause and its continuation, without raw/literal/hash changes.'}
apply=rd(T['applyReport'])
for g in e['sixLiteralCanonicalGroups']:
 ag=next(z for z in apply['finalGroupBindings'] if z['id']==q['id'] and z['group']==g['group']);assert g['literal']==ag['literal'] and g['canonicalSHA256']==ag['literalSHA256']
for t in e['fourFullPromptAnswerNoteVariants']:
 av=next(z for z in apply['finalVariantBindings'] if z['id']==q['id'] and z['slot']==t['slot']);assert t['tripleCanonicalSHA256']==av['bindingCanonicalSHA256']
for name,value in [('receipt.json',r),('sources.json',s),('peers.json',p),('verification.json',v)]:
 dest=O/name;assert dest.parent==O and not dest.exists();dest.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
# Saved readback and fresh exact current/source checks, no Git or binder.
for name in ['receipt.json','sources.json','peers.json','verification.json']:assert rd(O/name)
assert next(z for z in rd(C/'src/content/topics/history-russia.json')['questions'] if z['id']==q['id'])==q
assert raw(C/'src/content/topics/history-russia.json')==v['catalogRawSHA256']
print(json.dumps({'status':'PASS','stage':'FINAL','sourceOrder':90,'cycle':1,'cardHash':sha(q),'sixGroups':6,'fourVariants':4,'actualPeers':len(by),'bilateralPairs':len(p['bilateralMainComparisons']),'sourceEntries':len(s['sources']),'actualCompactions':comp,'qualityCredit':'0 until coordinator binding','outputDirectory':str(O),'filesSHA256':{name:raw(O/name) for name in ['receipt.json','sources.json','peers.json','verification.json']}},ensure_ascii=False))
