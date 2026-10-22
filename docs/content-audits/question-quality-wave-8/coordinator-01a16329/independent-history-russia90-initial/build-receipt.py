import json,hashlib,re
from pathlib import Path
C=Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle')
D=C/'docs/content-audits/question-quality-wave-8/coordinator-01a16329'
T=json.loads((D/'reader-history-russia90-initial-task.json').read_text());O=Path(T['outputDirectory']);N='01a164f5-4b8d-7761-a3f7-0ec75266cb95'
def rd(p):return json.loads(Path(p).read_text())
def sha(v):return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def raw(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def wr(n,v):
 p=O/n;assert p.parent==O and not p.exists();p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
q=next(x for x in rd(C/'src/content/topics/history-russia.json')['questions'] if x['id']==T['id']);assert sha(q)==T['cardHash']
S=rd(Path(T['authorPacket'])/'sourceproof.json')['rawSources']
loc=[{'path':s['path'],'url':s['url'],'completeOutputPointer':s['completeOutputPointer'],'locator':s['locator']} for s in S]
def refs(*ns):return [loc[i] for i in ns]
defect={'code':'NOTE3_CAUSAL_SUBJECT_CHANGED','field':'answers[3].note','severity':'substantive','literal':q['answers'][3]['note'],'ground':'В L55 источника субъект причинного утверждения — падение Порт-Артура, а не его оборона. Смена субъекта превращает длительное сопротивление в причину поражения России; L54, напротив, описывает сковывание японских сил обороной. Текущая справка не является точной передачей прочитанного контекста.','sourcesLocators':refs(0),'requiredAction':'В единственном разрешённом directed fix-cycle исправить причинный субъект на падение крепости либо дать другой дополнительный факт о Русско-японской войне из уже сохранённого контекста. Не менять хороший prompt/key/прочие notes ради новизны; сеть не требуется.','suggestedMinimalText':'Падение Порт-Артура предопределило дальнейший ход войны и поражение России.','scope':'INITIAL90 only; no change applied'}
gs={'prompt_ordered_answers_key':{'prompt':q['prompt'],'answers':[a['text'] for a in q['answers']],'correctIndex':q['correctIndex']},'explanation':q['explanation'],**{'note'+str(i):a['note'] for i,a in enumerate(q['answers'])}}
grounds={
'prompt_ordered_answers_key':('L44 прямо относит сдачу Порт-Артура после обороны к Русско-японской войне 1904–1905; L45–54 разворачивают тот же эпизод. Крымская война в другом сохранённом контексте датирована 1853–1856, Северная — 1700–1721. Версальский контекст относится к завершению Первой мировой в 1919, Брестский — к миру России в 1918. Все варианты — названия войн в родительном падеже после «во время какой войны»; ключ только slot3.',refs(0,1,2,3,4)),
'explanation':('L44 подтверждает войну 1904–1905 и статус главной базы Тихоокеанского флота России. L55 подтверждает влияние падения крепости на дальнейшую войну. Два предложения прямо называют ключ и не смешивают оборону с падением.',refs(0)),
'note0':('Крымский контекст turn3view3 L40,44,48–51 устанавливает 1853–1856 и коалицию Турции, Великобритании, Франции и Сардинии против России; «Османская империя и европейские державы» корректно обобщает перечисленные стороны. Собственный полезный факт о дистракторе.',refs(1)),
'note1':('Северный контекст L45 датирует объявление войны Швеции 1700 годом; L51 фиксирует мир в Ништадте 1721 года. Справка называет начало/конец и завершивший эту войну договор, а не факт о Порт-Артуре.',refs(2)),
'note2':('Library of Congress turn3view1 L8–11 связывает Версаль с Первой мировой и прямо сообщает два отказа Сената в 1919/1920 и отдельный мир США с Германией в 1921. Справка даёт конкретный послевоенный итог собственного варианта, не приписывает ему оборону Порт-Артура.',refs(3)),
'note3':('FIX: L55 говорит о падении, тогда как literal называет оборону причиной дальнейшего хода войны и поражения. L54 описывает сопротивление и связывание японских сил. Дополнительный факт задуман сверх prompt/key, но при данном причинном субъекте не подтверждён.',refs(0))}
groups=[{'group':g,'literal':v,'canonicalSHA256':sha(v),'individualGround':grounds[g][0],'sourcesLocators':grounds[g][1]} for g,v in gs.items()]
plaus=[
'Крымская война — российская война с известной обороной военно-морской базы (Севастополя); путаница между двумя оборонами объяснима. Название по категории/длине сопоставимо с ключом.',
'Северная война — другой крупный российский военный конфликт с морской составляющей; незнающий хронологии Порт-Артура должен различить эпоху и театр, а не отсеять выдуманную войну.',
'Первая мировая — близкий по эпохе большой конфликт с участием России; может быть выбрана при путанице начала XX века. Нет языковой подсказки или заведомо невозможной сущности.',
'Русско-японская война — та же категория названия войны, без уникальной даты/развёрнутой подсказки в label. Установление связи крепости с этим конфликтом требует исторического знания.']
truth=[
'Неверный вариант: сохранённый Крымский контекст относится к 1853–1856 и Севастополю, тогда как L44 Порт-Артурского контекста прямо называет 1904–1905 и войну с Японией.',
'Неверный вариант: L45,51 Северного контекста задают 1700–1721; Порт-Артурский L44 задаёт Русско-японскую войну 1904–1905.',
'Неверный вариант: Порт-Артурский L44 прямо помещает оборону в 1904–1905 Русско-японской войны. Сохранённые контексты Версаля и Бреста относятся к другой войне; они не создают второго ключа.',
'Единственный правильный вариант: Порт-Артурский L44 прямо связывает оборону/сдачу с Русско-японской войной, а L45–54 дают ход событий этой обороны.']
variants=[]
for i,a in enumerate(q['answers']):
 tr={'prompt':q['prompt'],'answer':a['text'],'note':a['note']}
 variants.append({'slot':i,**tr,'tripleCanonicalSHA256':sha(tr),'grammar':'«Во время '+a['text']+' происходила оборона Порт-Артура?» — согласованный родительный падеж; справка является самостоятельным грамматическим предложением.','plausibility':plaus[i],'truthUniqueKey':truth[i],'noteTruthUsefulness':grounds['note'+str(i)][0],'sourcesLocators':refs(0,[1,2,3,0][i]) if i!=3 else refs(0)})
level={'frozen':'medium','assessment':'Соответствует абсолютному MEDIUM: узнавание принадлежности обороны конкретной дальневосточной крепости к Русско-японской войне — школьное тематическое знание истории; оно вероятно знакомо читающему историю, но не дано широкой взрослой аудитории самим названием места. Вне темы можно спутать с другой обороной базы или близкой по времени мировой войной. Точная экспертная дата/командующий не требуются, случайных имён нет.'}
e={'id':q['id'],'topicId':T['topicId'],'sourceOrder':90,'stage':'INITIAL','cycle':0,'currentCard':q,'currentCardCanonicalSHA256':sha(q),'status':'FIX','sixLiteralCanonicalGroups':groups,'fourFullPromptAnswerNoteVariants':variants,'absoluteLevel':level,'correctNoteExtraFact':{'status':'FIX','intendedFact':'Влияние падения крепости на дальнейший ход Русско-японской войны и поражение России — сверх связи оборона→война из prompt/key.','actualProblem':'Текущий literal подменил падение обороной; дополнительный факт в этой формулировке не принят.','sourcesLocators':refs(0)},'defects':[defect],'frozen':T['frozen']}
receipt={'readerNativeId':N,'role':'independent','stage':'INITIAL','date':'2026-10-23','catalogCommit':T['catalogCommit'],'qualityCredit':0,'entries':[e]}
readEvidence=[
'Лично прочитан весь извлечённый original tool body L0–139 (8837 символов): L44 война и база; L45–54 оборона; L55 именно падение как причина хода войны и поражения. Чужие PASS не использованы.',
'Лично прочитан полный сохранённый batch body (23134 символа), включая turn3view3 L0–120: даты, коалиция и конец Крымской войны L40–51. Другие страницы/error outputs не выдаются за источник этого факта.',
'Лично прочитан весь original body L0–133 (8875 символов): объявление войны 1700 L45 и мир в Ништадте 1721 L51. Контекст сверён лично.',
'Лично прочитан полный original batch body (37335 символов, два последовательных диапазона 0:19000 и 19000:end): LOC turn3view1 L0–40, особенно L8–11; FRUS turn3view0 фактически возвращён только L0–248 из заявленных 773. Невозвращённая часть не прочитана и не используется.',
'Тот же лично прочитанный целиком original batch body: FRUS turn3view0 L14–18,78–82 даёт Брестский договор и 1918. Полученный текст заканчивается L248 из 773; полный документ не заявляется.'
]
sources=[]
for i,s in enumerate(S):
 p=C/s['path'];assert raw(p)==s['sha256'];v=rd(p)
 for k in s['completeOutputPointer'].strip('/').split('/'):v=v[int(k)] if isinstance(v,list) else v[k]
 body=hashlib.sha256(v.encode()).hexdigest();assert body==s['completeOutputSHA256']
 sources.append({'path':s['path'],'url':s['url'],'rawReadSHA256':raw(p),'completeOutputPointer':s['completeOutputPointer'],'completeOutputSHA256':body,'actualReturnedCharacters':len(v),'locator':s['locator'],'personalReadEvidence':readEvidence[i],'readDate':'2026-10-23','limitations':'Только фактически сохранённый original output; сеть, поиск, refetch и альтернативные попытки не выполнялись. SOURCE16 ограничения Britannica/National Archives сохранены; чужой PASS и HTTP status не являются доказательством содержания.'})
sourceDoc={'readerNativeId':N,'sources':sources,'independence':'Основания сформулированы после личного чтения actual CURRENT и original source outputs. Авторские оценки/QA не наследуются.','attemptFences':'SOURCE16 не переоткрыт; SOURCE86/Witte→89, SOURCE83/87/88 и прочие consumed/HOLD fences сохраняются.','bootstrapAuditHistory':'Оригинальный coordinator auditFAIL из-за буквального распознавания путей сохраняется как история; успешные оригинальные full4 reads и exact-ID proof приняты без смены identity assertions.'}
# Semantic models and prose are independent judgments; cards/hashes are read mechanically from actual CURRENT.
selected={
'history-russia':['history-russia-port-arthur-war','history-russia-borodino-war','history-russia-portsmouth-treaty','history-russia-crimean-war-fortress','history-russia-kronstadt-year'],
'history-china':['history-china-hard-02-01','history-china-hard-02-03'],
'history-japan':['history-japan-easy-01b-05','history-japan-easy-02b-04','history-japan-hard-01-04']}
models={
q['id']:('оборона Порт-Артура','принадлежит войне','Русско-японская война','оборона крепости 1904–1905'),
'history-russia-borodino-war':('Бородинская битва','принадлежит войне','Отечественная война 1812 года','вторжение армии Наполеона'),
'history-russia-portsmouth-treaty':('Русско-японская война','завершена договором','Портсмутский','мирное урегулирование 1905'),
'history-russia-crimean-war-fortress':('Крымская война','имеет центральную оборону города','Севастополь','осада базы Черноморского флота'),
'history-russia-kronstadt-year':('март 1921 года','датирует антибольшевистское выступление','Кронштадтское восстание','гарнизон и экипажи Балтийского флота'),
'history-china-hard-02-01':('Тройственная интервенция 1895','привела к возвращению территории','Ляодунский полуостров','Симоносекский договор и Китай'),
'history-china-hard-02-03':('советско-китайские соглашения 1954','предусматривали вывод войск из порта','Порт-Артур','советская база и срок май 1955'),
'history-japan-easy-01b-05':('Русско-японская война','началась в месяце','февраль 1904','начало боевых действий'),
'history-japan-easy-02b-04':('принятие Потсдамской декларации','являлось поражением Японии в войне','Вторая мировая','август 1945'),
'history-japan-hard-01-04':('создание Национального полицейского резерва Японии','непосредственно вызвано началом войны','Корейская война','75 тысяч человек и переброска американских войск 1950')}
pe=[]
for topic,ids in selected.items():
 for n,card in enumerate(rd(C/f'src/content/topics/{topic}.json')['questions'],1):
  if card['id'] in ids:pe.append({'id':card['id'],'topicId':topic,'sourceOrder':n,'card':card,'canonicalSHA256':sha(card),'sourcePath':f'src/content/topics/{topic}.json','fileSHA256':raw(C/f'src/content/topics/{topic}.json')})
by={p['id']:p for p in pe}
def side(i):
 p=by[i];return {'id':i,'canonicalSHA256':p['canonicalSHA256'],'MAIN':dict(zip(['entity','relation','value','context'],models[i])),'key':p['card']['answers'][p['card']['correctIndex']]['text']}
prose={
'history-russia-borodino-war':'Одинаков тип вопроса «сражение/оборона→война», но разные события, войны и эпохи: Бородино→1812 не сообщает Порт-Артур→1904–1905; связь Порт-Артура с Японией не отвечает, в какой войне было Бородино.',
'history-russia-portsmouth-treaty':'CURRENT90 спрашивает принадлежность обороны к войне; peer46 спрашивает договор окончания этой войны. Из ключа Русско-японская война нельзя получить название договора, а знание договора без знания Порт-Артура не устанавливает принадлежность обороны. Это две разные связи, не прямое обращение.',
'history-russia-crimean-war-fortress':'CURRENT90 — Порт-Артур→Русско-японская война, peer57 — Крымская война→Севастополь. И сущность обороны, и война различны; обратный вопрос CURRENT90 был бы «какая оборона была в Русско-японской войне», а не оборона Севастополя. Факт о Порт-Артуре в неверной note peer57 не его MAIN.',
'history-russia-kronstadt-year':'Применённая actual CURRENT91 связывает март1921 с антибольшевистским Кронштадтским восстанием, CURRENT90 — оборону Порт-Артура с войной1904–1905. Ни entity, ни relation, ни value/context не совпадают; оба полных actual body прочитаны, старый preimage91 не используется.',
'history-china-hard-02-01':'Общий регион Ляодун не равен MAIN: peer спрашивает территорию, возвращённую Китаю в1895 после интервенции; CURRENT90 — войну обороны Порт-Артура1904–1905. Возвращение полуострова не отвечает о войне обороны, и название войны не отвечает о территориальном возврате1895.',
'history-china-hard-02-03':'Один топоним, разные relation/context: CURRENT90 классифицирует оборону1904–1905 по войне; peer50 идентифицирует порт вывода советских войск по соглашениям1954/1955. Это не вопрос «в какой войне обороняли порт» наоборот; ни одна ключевая связь не отвечает другой.',
'history-japan-easy-01b-05':'Одна война, но CURRENT90 связывает её с отдельной обороной, peer10 устанавливает месяц начала боевых действий. Знание февраля1904 не само по себе доказывает принадлежность названной обороны; название войны не даёт месяц. Не direct reverse.',
'history-japan-easy-02b-04':'Тип «событие→война» общий, но peer — капитуляция Японии по Потсдамской декларации1945→Вторая мировая, CURRENT90 — оборона1904–1905→Русско-японская. Разные entity/value/context, взаимных ответов и обращения одной связи нет.',
'history-japan-hard-01-04':'Общая категория названий войн не совпадение MAIN: peer резерв75тыс→начало Корейской1950, CURRENT90 оборона Порт-Артура→Русско-японская1904–1905. В каждом направлении знание одного не даёт другого; обратный вопрос про ту же оборону отсутствует.'}
pairs=[{'left':side(q['id']),'right':side(i),'bilateralGround':s,'directReverseCheck':'Проверено в обе стороны по полным актуальным карточкам: перестановка entity/value CURRENT90 не воспроизводит MAIN peer; см. конкретные связи в bilateralGround.','result':'DISTINCT_MAIN'} for i,s in prose.items()]
rows=[];bindings=[];hits=[]
for p in sorted((C/'src/content/topics').glob('*.json')):
 qs=rd(p)['questions'];bindings.append({'path':str(p.relative_to(C)),'rawSHA256':raw(p),'questionCount':len(qs)})
 for card in qs:
  row={'topicId':p.stem,'id':card['id'],'prompt':card['prompt'],'answers':[a['text'] for a in card['answers']],'correctIndex':card['correctIndex']};rows.append(row)
  if re.search(r'Порт.?Артур|Люйшун|Ляодун|Цусим|русско-япон',card['prompt']+' '+' '.join(row['answers']),re.I):hits.append(row)
peerDoc={'readerNativeId':N,'actualCurrentPeers':pe,'bilateralMainComparisons':pairs,'globalMAINRetrieval':{'topicFiles':len(bindings),'rows':len(rows),'rowsCanonicalSHA256':sha(rows),'fileBindings':bindings,'query':'Порт.?Артур|Люйшун|Ляодун|Цусим|русско-япон case insensitive over actual prompt+answers','hits':hits,'limitation':'Retrieval is mechanical, not a semantic verdict for unread 11000 full cards. All100 history-russia MAIN prompts+keys personally read; relevant full actual cards above personally read and compared. Source90 historical preimage excluded as DISTINCT peer.'},'latestProposalSnapshots':[],'current91':'Applied exact actual CURRENT91 retained and compared as a relevant batch-delta guard, no independent quality verdict for91.'}
qa=rd(T['qa']);assert qa['success'] and qa['numPassedTests']==19 and qa['numFailedTests']==qa['numPendingTests']==0;assert raw(T['qa'])==T['qaSHA256']
fs=list(Path('/Users/eaafonasev/.codex/sessions/2026/10/22').glob('*-'+N+'.jsonl'));assert len(fs)==1
jr=[json.loads(l) for l in fs[0].open()];assert [v['payload']['id'] for v in jr if v.get('type')=='session_meta']==[N];comp=sum(v.get('type')=='compacted' for v in jr);assert comp<2
verification={'readerNativeId':N,'catalogCommit':T['catalogCommit'],'catalogRawSHA256':raw(C/'src/content/topics/history-russia.json'),'currentCardCanonicalSHA256':sha(q),'existingQA19':{'path':str(Path(T['qa']).relative_to(C)),'rawSHA256':raw(T['qa']),'pass':19,'fail':0,'pending':0,'meaning':'Existing exact shared90+91 report read and hash-bound; no QA executed by this reviewer and no inherited substantive PASS.'},'nativeJournal':str(fs[0]),'session_meta':N,'actualCompactions':comp,'bootstrapAuditHistoryPreserved':True,'mechanicalChecks':{'sixLiteralGroups':len(groups),'fourWholeVariants':len(variants),'sourceFileHashes':len(sources),'actualPeers':len(pe),'bilateralPairs':len(pairs),'allFrozenFieldsMatch':q['id']==T['frozen']['id'] and q['difficulty']==T['frozen']['difficulty'] and q['correctIndex']==T['frozen']['correctIndex'],'answerUTF16Lengths':[len(a['text'].encode('utf-16-le'))//2 for a in q['answers']],'noteWordCounts':[len(a['note'].split()) for a in q['answers']],'explanationWordCount':len(q['explanation'].split()),'explanationSentences':2},'notRun':['Git/binder (binder invokes Git and coordinator-only planning writes)','tests/runtime/browser/build/full suite','network/refetch','human/device acceptance'],'integration':'Not assessed; Git forbidden. Assigned frozen catalog commit is a task binding, not an independently checked branch/integration claim.'}
assert len(groups)==6 and len(variants)==4
for g in groups:assert sha(g['literal'])==g['canonicalSHA256']
for v in variants:assert sha({k:v[k] for k in ['prompt','answer','note']})==v['tripleCanonicalSHA256']
for p in pe:assert sha(p['card'])==p['canonicalSHA256']
for n,v in [('receipt.json',receipt),('sources.json',sourceDoc),('peers.json',peerDoc),('verification.json',verification)]:wr(n,v)
print(json.dumps({'status':'FIX','id':q['id'],'defects':[defect['code']],'outputDirectory':str(O),'files':{n:raw(O/n) for n in ['receipt.json','sources.json','peers.json','verification.json']},'actualCompactions':comp,'qualityCredit':0},ensure_ascii=False))
