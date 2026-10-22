import json,hashlib,re
from pathlib import Path
C=Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle');D=C/'docs/content-audits/question-quality-wave-8/coordinator-01a16329';N='01a164f5-4b8d-7761-a3f7-0ec75266cb95'
def rd(p):return json.loads(Path(p).read_text())
def raw(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def sha(v):return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
T=rd(D/'reader-history-russia91-cycle1-final-task.json');O=Path(T['outputDirectory']);I=Path(T['previousIndependentInitial']).parent
r=rd(I/'receipt.json');s=rd(I/'sources.json');p=rd(I/'peers.json');v=rd(I/'verification.json');e=r['entries'][0];old=e['currentCard'];cat=rd(C/'src/content/topics/history-russia.json')['questions'];q=next(x for x in cat if x['id']==T['id']);assert sha(q)==T['cardHash'];copy=dict(q);copy['prompt']=old['prompt'];assert copy==old and q['prompt']!=old['prompt']
def ptr(file,pointer):return {'path':str((I/file).relative_to(C)),'rawSHA256':raw(I/file),'jsonPointer':pointer,'readerNativeId':N,'basis':'Same-reader personal INITIAL judgment retained only for exact unchanged material; no author or QA truth inheritance.'}
refs=e['sixLiteralCanonicalGroups'][0]['sourcesLocators']
gs={'prompt_ordered_answers_key':{'prompt':q['prompt'],'answers':[a['text'] for a in q['answers']],'correctIndex':q['correctIndex']},'explanation':q['explanation'],**{'note'+str(i):a['note'] for i,a in enumerate(q['answers'])}}
for i,g in enumerate(e['sixLiteralCanonicalGroups']):
 g['literal']=gs[g['group']];g['canonicalSHA256']=sha(g['literal'])
 if g['group']=='prompt_ordered_answers_key':
  g['individualGround']='PASS directed FINAL: prompt теперь спрашивает событие марта1921 без политической категории. Полный ряд лично прочитан заново. Все варианты — российские общественно-политические события; невозможно исключить все три одним словом «антибольшевистское». Для выбора требуется знание хронологии: L63 Кронштадтского контекста прямо даёт март1921, Кровавое воскресенье1905/декабристы1825/Февраль1917 подтверждены ранее лично прочитанными неизменными контекстами. Один ключ slot3. Грамматическая конструкция «Какое из этих событий произошло...» согласуется с каждым именным названием, не требует, чтобы род названия совпадал со словом «событие».'
  g['directedResolutionOf']=ptr('receipt.json','/entries/0/defects/0')
 else:
  assert g['literal']==rd(I/'receipt.json')['entries'][0]['sixLiteralCanonicalGroups'][i]['literal'];g['retainedOwnInitialJudgment']=ptr('receipt.json',f'/entries/0/sixLiteralCanonicalGroups/{i}')
plaus=[
'Допустимый дистрактор общего ряда российских политических потрясений: Кровавое воскресенье могло быть спутано с подавленным выступлением началаXXвека. Новый prompt не содержит указания на большевиков; исключение требует знания самого события1905 или его царского контекста. Для знакомого с историей это лёгкий отсев, который разумно сужает ряд, но не выдаёт остальные одним квалификатором.',
'Допустимый более лёгкий хронологический отсев: восстание декабристов реально и относится к той же общей категории выступлений, его дореволюционная эпоха узнаётся из знания истории. Оно не маскируется как антибольшевистское; prompt лишь предлагает выбрать событие из ряда. Знание1825 сужает выбор, но не решает весь вопрос одним словом.',
'Правдоподобный ближайший по эпохе дистрактор: Февральская революция относится к1917, но события по новому стилю шли в марте (самостоятельно прочитанный turn1view0 L51–59). Поэтому название «Февральская» не даёт простого исключения месяца; нужно различить годы1917/1921 и последующие события.',
'Кронштадтское восстание — то же категориальное название исторического события, без добавленной в label даты/числа/политической подсказки. Его связь с мартом1921 — тематическое знание, а не единственный подходящий политический ярлык.']
for i,t in enumerate(e['fourFullPromptAnswerNoteVariants']):
 tr={'prompt':q['prompt'],'answer':q['answers'][i]['text'],'note':q['answers'][i]['note']};t.update(tr);t['tripleCanonicalSHA256']=sha(tr);t['grammar']='«'+q['prompt']+'» — «'+q['answers'][i]['text']+'»: корректный именной ответ на выбор события; управление и форма prompt не дают ключ. Note неизменна и грамматически корректна.';t['plausibility']=plaus[i];t['truthUniqueKey']=[
'Неверно по датировке: Кровавое воскресенье9(22)января1905 (turn2view0 L45–52), тогда как спрашивается март1921.',
'Неверно по датировке: восстание декабристов14(26)декабря1825 (turn3view0 L44), не март1921.',
'Неверно по году: Февральская революция1917 (turn1view0 L50–60); март нового стиля не делает её событием1921.',
'Единственный правильный ключ: turn4view0 L63 прямо называет Кронштадтское восстание и март1921. Остальные три сохранённых контекста дают другие годы.'][i]
 t['retainedOwnUnchangedNoteJudgment']=ptr('receipt.json',f'/entries/0/fourFullPromptAnswerNoteVariants/{i}/noteTruthUsefulness')
e.update(stage='FINAL',cycle=1,currentCard=q,currentCardCanonicalSHA256=sha(q),status='PASS',defects=[])
e['absoluteLevel']={'frozen':'medium','assessment':'PASS. Требуется тематическое историческое знание связи Кронштадтского восстания с мартом1921 либо несколько осмысленных хронологических исключений. Человек вне темы может отсеять декабристов, но остаются события началаXXвека; отличить1905,1917,1921 нужно по знаниям, а не по формальному политическому слову. Февраль1917 в марте нового стиля оставляет объяснимую путаницу месяца. Это школьная тематическая хронология, не экспертная деталь и не широко гарантированное взрослой аудитории узнавание, поэтому абсолютный MEDIUM допустим.','directedResolutionOf':ptr('receipt.json','/entries/0/absoluteLevel')}
e['correctNoteExtraFact']['retainedOwnInitialJudgment']=ptr('receipt.json','/entries/0/correctNoteExtraFact');e['directedResolution']={'initialDefect':ptr('receipt.json','/entries/0/defects/0'),'result':'RESOLVED','onlyChangedLiteral':'prompt','noNewInitialOrCycle2':True};r.update(stage='FINAL',catalogCommit=T['catalogCommit'],date='2026-10-23',qualityCredit=0)
for i,x in enumerate(s['sources']):
 assert raw(C/x['path'])==x['rawReadSHA256'];body=rd(C/x['path'])
 for k in x['completeOutputPointer'].strip('/').split('/'):body=body[int(k)] if isinstance(body,list) else body[k]
 assert hashlib.sha256(body.encode()).hexdigest()==x['completeOutputSHA256'];x['initialPersonalReadEvidence']=ptr('sources.json',f'/sources/{i}');x['reuseMeaning']='Same-reader complete original context personally read in INITIAL, exact raw/body hashes unchanged. Directed FINAL uses own reading, no refetch.'
 if i==0:x['personalReadEvidence']+=' FINAL91 directed: лично повторно прочитан контекст L61–65, в том числе полный L63 и L64; дата/участники/подавление подтверждены. Полное original body прочитано мною в INITIAL, как указано по exact pointer.'
s['directedScope']='FINAL91 solecycle1: prompt and four whole variants reassessed; unchanged substantive source/note/explanation judgments retained from own INITIAL. Original91 mechanicalFAIL/technicalENOSPC preserved, semantic verdict and QA do not cure procedure.'
for x in p['actualCurrentPeers']:
 current=next(z for z in rd(C/f"src/content/topics/{x['topicId']}.json")['questions'] if z['id']==x['id'])
 if current!=x['card']:assert x['id'] in [q['id'],'history-russia-port-arthur-war']
 x.update(card=current,canonicalSHA256=sha(current),fileSHA256=raw(C/f"src/content/topics/{x['topicId']}.json"))
by={x['id']:x for x in p['actualCurrentPeers']}
for i,pair in enumerate(p['bilateralMainComparisons']):
 for side in ['left','right']:
  x=pair[side];x['canonicalSHA256']=by[x['id']]['canonicalSHA256']
  if x['id']==q['id']:x['MAIN']={'entity':'март1921','relation':'датирует событие из предложенного ряда','value':'Кронштадтское восстание','context':'история России'}
 pair['retainedOwnInitialPair']=ptr('peers.json',f'/bilateralMainComparisons/{i}');pair['directedApplicability']='Удалён политический квалификатор, но запрашиваемое событие/дата не изменены. В обоих направлениях конкретные entity/relation/value/context peer по прежнему отличаются от Кронштадт→март1921. FULL actual peer body сверены; предыдущая конкретная bilateralGround сохраняет силу как историческое сопоставление, а не повторное требование антибольшевистского prompt.'
 if pair['right']['id']=='history-russia-port-arthur-war':
  pair['bilateralGround']='Актуальная90 имеет исправленную note3 о падении Порт-Артура; собственный MAIN90 остаётся оборона1904–1905→Русско-японская война. MAIN91 теперь без политического квалификатора: событие марта1921→Кронштадтское восстание. Разные event/date/relation/value; ни один ключ не отвечает другому в обе стороны, direct reverse нет.90 не переоценивается, актуальная карточка только привязана.'
p['catalog90Guard']='Актуальная cycle1 CURRENT90 hash/body обновлены. Никакого повторного вердикта90.'
rows=[];bindings=[];hits=[];pattern=p['globalMAINRetrieval']['query']
for f in sorted((C/'src/content/topics').glob('*.json')):
 qs=rd(f)['questions'];bindings.append({'path':str(f.relative_to(C)),'rawSHA256':raw(f),'questionCount':len(qs)})
 for card in qs:
  row={'topicId':f.stem,'id':card['id'],'prompt':card['prompt'],'answers':[a['text'] for a in card['answers']],'correctIndex':card['correctIndex']};rows.append(row)
  if re.search(pattern,row['prompt']+' '+' '.join(row['answers']),re.I):hits.append(row)
p['globalMAINRetrieval'].update(rowsCanonicalSHA256=sha(rows),fileBindings=bindings,hits=hits);p['directedMAINBoundary']='Prompt is broader event wording, but same exact date/value and no new entity relation introduced. No new relevant MAIN duplicate appears from deleting qualifier; historical/current self version not counted distinct.'
qa=rd(T['qa']);assert raw(T['qa'])==T['qaSHA256'] and qa['success'] and qa['numPassedTests']==19 and qa['numFailedTests']==qa['numPendingTests']==0
fs=list(Path('/Users/eaafonasev/.codex/sessions/2026/10/22').glob('*-'+N+'.jsonl'));assert len(fs)==1;jr=[json.loads(l) for l in fs[0].open()];assert [x['payload']['id'] for x in jr if x.get('type')=='session_meta']==[N];comp=sum(x.get('type')=='compacted' for x in jr);assert comp<2
v.update(catalogCommit=T['catalogCommit'],catalogRawSHA256=raw(C/'src/content/topics/history-russia.json'),currentCardCanonicalSHA256=sha(q),existingQA19={'path':str(Path(T['qa']).relative_to(C)),'rawSHA256':raw(T['qa']),'pass':19,'fail':0,'pending':0,'meaning':'Existing exact sharedcycle1 report hash-bound; no reviewer tests and no inherited content verdict.'},actualCompactions=comp,stage='FINAL',status='PASS')
v['source91OriginalMechanicalFAILsPreserved']=True;v['source91Cycle1ENOSPC']='Preserved by coordinator; not changed, not claimed cured.';v['directedDiff']={'only91PromptChanged':True,'allFourVariantHashesRegenerated':True,'current90RefreshedWithoutReReview':True,'initialReceipt':ptr('receipt.json','/entries/0')}
a=rd(T['applyReport'])
for g in e['sixLiteralCanonicalGroups']:
 ag=next(x for x in a['finalGroupBindings'] if x['id']==q['id'] and x['group']==g['group']);assert g['literal']==ag['literal'] and g['canonicalSHA256']==ag['literalSHA256']
for t in e['fourFullPromptAnswerNoteVariants']:
 av=next(x for x in a['finalVariantBindings'] if x['id']==q['id'] and x['slot']==t['slot']);assert t['tripleCanonicalSHA256']==av['bindingCanonicalSHA256'] and all(t[k] for k in ['grammar','plausibility','truthUniqueKey','noteTruthUsefulness','sourcesLocators'])
for name,value in [('receipt.json',r),('sources.json',s),('peers.json',p),('verification.json',v)]:
 dest=O/name;assert dest.parent==O and not dest.exists();dest.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
# Exact saved readback; no binder, tests or Git.
for name in ['receipt.json','sources.json','peers.json','verification.json']:assert rd(O/name)
assert next(x for x in rd(C/'src/content/topics/history-russia.json')['questions'] if x['id']==q['id'])==q and raw(C/'src/content/topics/history-russia.json')==v['catalogRawSHA256']
for peer in p['actualCurrentPeers']:
 actual=next(x for x in rd(C/f"src/content/topics/{peer['topicId']}.json")['questions'] if x['id']==peer['id']);assert actual==peer['card'] and sha(actual)==peer['canonicalSHA256']
print(json.dumps({'status':'PASS','stage':'FINAL','sourceOrder':91,'cycle':1,'cardHash':sha(q),'sixGroups':6,'fourVariants':4,'sourceEntries':len(s['sources']),'actualPeers':len(by),'bilateralPairs':len(p['bilateralMainComparisons']),'actualCompactions':comp,'qualityCredit':'0 until coordinator binding','outputDirectory':str(O),'filesSHA256':{name:raw(O/name) for name in ['receipt.json','sources.json','peers.json','verification.json']}},ensure_ascii=False))
