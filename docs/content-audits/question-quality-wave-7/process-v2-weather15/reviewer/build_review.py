import json,hashlib,subprocess,pathlib,re
root=pathlib.Path(__file__).resolve().parents[5]
p=root/'docs/content-audits/question-quality-wave-7/process-v2-weather15'
canon=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
hashof=lambda x:hashlib.sha256(canon(x)).hexdigest()
a=json.loads((p/'exact-apply.json').read_text());topic=json.loads((root/'src/content/topics/weather-climate.json').read_text());cards={q['id']:q for q in topic['questions']}
idxpath='docs/content-audits/process-review-2026-10-14/preserved/mindbattle-source-01a13956-2a8a-7cf1-8313-aa3392952779/weather-climate-whole-topic.json'
idx=json.loads(subprocess.check_output(['git','show','12e5581b:'+idxpath],cwd=root))['primaryContextIndex']
keys=['nws-key-glossary','noaa-climate-zones','noaa-windward-leeward','noaa-rain-shadow-pdf','nws-basic-fronts']
sources={}
for k in keys:
 s=idx[k];checked={}
 for kind in ['body','headers']:
  m=s[kind];b=subprocess.check_output(['git','cat-file','blob',m['gitBlob']],cwd=root)
  assert len(b)==m['bytes'] and hashlib.sha256(b).hexdigest()==m['sha256'],(k,kind)
  checked[kind]={'gitBlob':m['gitBlob'],'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'matchesIndex':True}
  if kind=='headers':
   checked[kind]['httpDateLines']=re.findall(r'(?im)^date:[^\r\n]*',b.decode('latin1'))
 sources[k]={'url':s['sourceUrl'],'readAt':'2026-10-14','captureDate':'Retained capture; no new retrieval. Original headers retained at headers.gitBlob.','verified':checked,'personalRead':'Full preserved scientific/article context read; PDF text read pages 1-22 with pypdf. Navigation/scripts not used as scientific support.'}
pre=json.loads((p/'preimage.json').read_text());before={e['id']:e['card'] for e in pre['entries']}
# Editorial findings below are independent decisions on CURRENT, not author conclusions.
D={
'tropical-depression':[('note3','Справка описывает СУБтропический циклон, хотя вариант — ВНЕтропический циклон. Это разные категории; сохранённый NWS SUBTROPICAL CYCLONE не подтверждает эту справку о данном варианте.','Заменить note3 фактом именно о внетропическом циклоне с полным сохранённым официальным основанием. Если такого контекста нет — HOLD данного утверждения, не переносить субтропическое определение.')],
'tropical-storm':[('note3','Справка о внетропическом циклоне подменена справкой о субтропическом шторме. Фраза про отсутствие имён относится к другому объекту и устаревшему утверждению сохранённого глоссария.','Заменить note3 проверенным фактом о внетропическом циклоне; не использовать утверждение SUBTROPICAL STORM о неназначении имён.')],
'hurricane-eye':[('note3','Вариант «Внетропический циклон» сопровождается определением субтропического циклона. NWS SUBTROPICAL CYCLONE определяет non-frontal non-tropical систему; перенос на extratropical неверен.','Заменить note3 проверенным самостоятельным фактом о внетропическом циклоне; все остальные поля перечитать в рамках изменённой карточки.')],
'orographic-rain':[('prompt_ordered_answers_key','«Грозовые осадки» и «Конвективные осадки» пересекаются по смыслу; первые два notes фактически описывают одну грозу. PDF p10 прямо допускает запуск грозового подъёма холмами и горами. Неверные варианты не дают трёх сопоставимых независимых альтернатив механизму из prompt.','Заменить один пересекающийся дистрактор и его note самостоятельным типом осадков/механизмом, сохранив позицию ключа 3. Для всех четырёх подстановок явно отделить преобладающий механизм; не называть грозовые и конвективные осадки взаимоисключающими.')],
'rain-shadow':[('neighborReview','Карточка проверяет подветренную сухость после орографического выпадения осадков; соседняя orographic-rain проверяет наветренный подъём, а её explanation и correct note уже сообщают подветренное высыхание. Это две стороны одной причинной связи, а не достаточное разнообразие независимых фактов по ручной калибровке.','Оставить orographic-rain на механизме подъёма; для rain-shadow выбрать независимый факт о дождевой тени (например, конкретный сохранённый географический пример из PDF p5/p15), сохранив ID/topic/order/difficulty/correctIndex=3. Полностью проверить новую карточку и обе соседние формулировки.')],
'humidity-water-vapor':[('note0','«к тому, сколько воздуха может его удержать» грамматически и семантически неверно: сравнивается количество пара с количеством воздуха, который якобы удерживает пар. NWS сравнивает amount of water vapor actually in air с how much water vapor the air can hold.','Заменить на «...к количеству водяного пара, которое воздух может удержать»; предпочтительно явно сказать о текущей температуре при наличии точного основания.'),('note1','Определение давления как силы на единицу площади общефизически корректно, но сохранённый NWS PRESSURE сообщает гравитацию/вес воздуха, не force per unit area. В предоставленном primary context эта дополнительная формула не установлена.','В этом цикле использовать уже подтверждённый факт NWS PRESSURE о весе воздуха либо дать полный официальный контекст определения силы на площадь.')],
'pressure-air-weight':[('note1','Правильная справка повторяет единственную связь из prompt — гравитация/вес воздуха. Она не добавляет факта к спрашиваемому признаку.','Заменить correct note дополнительным фактом: например, единицы давления inches of mercury и millibars из сохранённого nws-basic-fronts, начало A Basic Discussion. Тогда добавить этот locator. Не менять correctIndex=1.')]
}
prefix='weather-climate-'
G='nws-key-glossary'
common_notes={
'Тропическая депрессия':G+' / TROPICAL DEPRESSION: sustained winds 23–38 mph (20–33 knots).',
'Тропический шторм':G+' / TROPICAL STORM: 39–73 mph (34–63 knots); once a tropical storm forms it is given a name.',
'Ураган':G+' / HURRICANE: forms in tropics, sustained wind at least 74 mph (64 knots). The retained source itself does not delimit Atlantic usage.',
'Внетропический циклон':G+' / SUBTROPICAL CYCLONE and SUBTROPICAL STORM refer to subtropical systems; these passages do NOT validate a note about an extratropical cyclone.',
'Индекс жары':G+' / HEAT INDEX: apparent temperature felt by body due to high air temperature combined with high relative humidity.',
'Точка росы':G+' / DEW POINT: temperature to which air must cool for water vapor to condense.',
'Влажность':G+' / HUMIDITY defines amount of water vapor; RELATIVE HUMIDITY compares actual vapor with holding amount and expresses percent.',
'Атмосферное давление':G+' / PRESSURE attributes atmospheric force to gravity and uses weight of air; force per area is not stated here.'}
climate={'Группа A':'noaa-climate-zones / A: moist tropics, all monthly mean temperatures >18 C; annual precipitation >59 inches in this NOAA educational description; latitude about 15–25 degrees N/S.', 'Группа B':'noaa-climate-zones / B: potential evaporation and transpiration exceed precipitation; belts 20–35 degrees N/S and large midlatitude continental regions.', 'Группа C':'noaa-climate-zones / C: generally warm humid summers, mild winters; winter midlatitude cyclones, summer convective thunderstorms.', 'Группа E':'noaa-climate-zones / E: warmest month <10 C; northern coasts of North America, Europe, Asia, Greenland and Antarctica.'}
entries=[]
for id in a['scope']:
 c=cards[id];short=id[len(prefix):];expected=next(e['afterHash'] for e in a['applied'] if e['id']==id);assert hashof(c)==expected,(id,hashof(c),expected)
 b=before[id];assert c['id']==b['id'] and c['difficulty']==b['difficulty'] and c['correctIndex']==b['correctIndex']
 # Comparing frozen position to retained baseline topic rather than trusting mutable author output.
 baseline=json.loads(subprocess.check_output(['git','show',pre['baselineCommit']+':src/content/topics/weather-climate.json'],cwd=root))
 assert [q['id'] for q in baseline['questions']].index(id)==[q['id'] for q in topic['questions']].index(id)
 defects=[{'field':f,'reason':r,'fix':n} for f,r,n in D.get(short,[])]
 if short.startswith('koppen-'):
  loc=['noaa-climate-zones'];pn=[climate[z['text']] for z in c['answers']];ex=[climate[c['answers'][c['correctIndex']]['text']]];notes=[[climate[z['text']]] for z in c['answers']]
  neighbors=['equator-hot','desert-dry','polar-cold','mediterranean-dry-summer']+[s[len(prefix):] for s in a['scope'] if 'koppen-' in s and s!=id]
  nr='Соседние A/B/C/E проверяют соответствия разных групп разным критериям; это четыре разные классификационные связи. Географические easy-карточки не спрашивают букву классификации. Список вариантов одной системы, ключ единственный; medium требует знакомства с Кёппеном—Гейгером. Формулировка C явно ограничена изложением NOAA; не расширять её до утверждения о каждом подтипе C.'
 elif short in ['tropical-depression','tropical-storm','hurricane-eye']:
  loc=[G];pn=[common_notes[z['text']] for z in c['answers']];ex=[common_notes[z['text']] for z in c['answers'] if z['text']!='Внетропический циклон'];notes=[[common_notes[z['text']]] for z in c['answers']]
  neighbors=['tropical-depression','tropical-storm','hurricane-eye','extratropical-fronts','eyewall-replacement'];neighbors.remove(short)
  nr='Все четыре именные подстановки грамматически согласованы. Депрессия спрашивает нижнюю категорию, шторм — порог следующей категории, hurricane-eye теперь верхний переход к урагану (не глаз). Граница 39 и 74 различна; близкий кластер требует сохранить это различие, не создавать ещё обратный вопрос о том же пороге. medium допустим: названия знакомы, точная граница/классификация требует предметного знания. extratropical-fronts спрашивает фронты; eyewall-replacement — иной процесс.'
 elif short in ['humidity-water-vapor','pressure-air-weight']:
  loc=[G,'nws-basic-fronts'];pn=[common_notes[z['text']] for z in c['answers']];ex=[common_notes['Влажность'],common_notes['Атмосферное давление']];notes=[[common_notes[z['text']]] for z in c['answers']]
  neighbors=['dew-point-saturation','relative-humidity-ratio',('pressure-air-weight' if short=='humidity-water-vapor' else 'humidity-water-vapor')]
  nr='Именные варианты одинакового синтаксического статуса, без подсказки согласованием. Влажность — базовое определение; соседняя dew-point-saturation сравнивает две пробы, relative-humidity-ratio требует расчёта 8/20. Давление — другая величина и гравитационная причина. easy соответствует распространённым понятиям; индекс жары и точка росы — тематически связанные альтернативы, пусть менее знакомые.'
 else:
  loc=['noaa-windward-leeward','noaa-rain-shadow-pdf','nws-basic-fronts',G]
  pn=['noaa-windward-leeward / main article: damp air ascends hills and mountains; condensation/clouds/precipitation; lee-side air warms and dries.', 'noaa-rain-shadow-pdf / p2 and p14: windward rainfall, lee dry air; p10 thunderstorm recipe includes solar heating and lift by hills/mountains.', 'nws-basic-fronts / cold and warm front cross-sections: converging/lifting moist air and slantwise warm air ascent produce precipitation.']
  ex=pn[:1]+['noaa-rain-shadow-pdf / p2 describes rain shadow; p14 explicitly states rising air cools and vapor condenses into rain/snow.']
  notes=[]
  for z in c['answers']:
   if z['text']=='Орографические осадки':notes.append([pn[0],ex[1]])
   elif z['text']=='Дождевая тень':notes.append([ex[1],G+' / RAIN OR SNOW SHADOW: upwind moisture condenses as air rises; dries descending lee side.'])
   elif z['text']=='Фронтальные осадки':notes.append([pn[2]])
   else:notes.append(['noaa-rain-shadow-pdf / p1: warm moist air rises, vapor condenses forming thunderstorm cloud, releases heat and rain falls; p10: local solar warming and continued buoyant rise after terrain lift. Supports factual rising-air content, but not treating convective and thunderstorm precipitation as exclusive categories.'])
  neighbors=['orographic-rain','rain-shadow','convectional-rain','frontal-rain'];neighbors.remove(short)
  nr='Карточки прочитаны целиком. Orographic-rain и rain-shadow дают наветренную/подветренную стороны одной причинной цепочки; обе уже объясняют обе стороны. Требуется независимый факт у rain-shadow. convectional-rain спрашивает летний нагретый подъём; frontal-rain — прохождение фронта. Для rain-shadow одна альтернатива — эффект/область, остальные — типы осадков; это категориальная подсказка, которую следует устранить при замене факта. medium по механизму/термину допустим.'
 groups=[('prompt_ordered_answers_key',{'prompt':c['prompt'],'answers':[z['text'] for z in c['answers']],'correctIndex':c['correctIndex']},pn),('explanation',c['explanation'],ex)]+[(f'note{i}',z['note'],notes[i]) for i,z in enumerate(c['answers'])]
 fgs=[]
 for group,literal,reasons in groups:
  gd=[d for d in defects if d['field']==group]
  ed=(' '.join(d['reason'] for d in gd) if gd else ('Четыре подстановки прочитаны: именные ответы согласованы с вопросительной конструкцией; ключ имеет указанный проверяемый критерий. '+nr if group=='prompt_ordered_answers_key' else 'Два предложения объясняют критерий и связанный факт; краткость и русский синтаксис приемлемы.' if group=='explanation' else 'Справка относится к своему варианту, сообщает проверяемый факт, укладывается в 35 слов.'))
  if group=='note'+str(c['correctIndex']) and not gd:ed+=' Дополнение к prompt: '+({'orographic-rain':'подветренное высыхание','rain-shadow':'выпадение влаги на наветренном склоне','tropical-depression':'численный диапазон ветра','tropical-storm':'присвоение имени','hurricane-eye':'численный порог 74 mph/64 knots','koppen-tropical-a':'годовой объём осадков в изложении NOAA','koppen-dry-b':'широтные пояса и материковые области','koppen-temperate-c':'сезонные грозы/циклоны','koppen-polar-e':'географическое распространение'}.get(short,'см. конкретное основание'))+'.'
  fgs.append({'group':group,'literal':literal,'literalSHA256':hashof(literal),'sourceReasons':reasons,'editorialReason':ed,'verdict':'FIX' if gd else 'PASS'})
 entries.append({'id':id,'currentHash':hashof(c),'verdict':'FIX' if defects else 'PASS','fieldGroups':fgs,'sourceLocators':loc,'neighborReview':{'neighborIds':[prefix+s for s in neighbors],'editorialReason':nr,'verdict':'FIX' if short=='rain-shadow' else 'PASS'},'defects':defects,'nextAction':'Автор: один адресный цикл; '+ ' '.join(d['fix'] for d in defects) if defects else 'Координатор: eligible for adjudication как ready PASS точного currentHash; не считать автоматически merged/accepted.'})
result={'reviewerThreadId':'01a13baa-2597-74a3-9a01-93cea5b90c83','scope':a['scope'],'baselineCommit':pre['baselineCommit'],'sourceIndexGitLocator':'12e5581b:'+idxpath,'hashRecipe':'SHA256 UTF-8 JSON recursively sorted keys, compact separators, unescaped unicode, array order preserved','sources':sources,'checks':{'currentAfterHash':'11/11 match exact-apply afterHash','frozen':'11/11 ID/difficulty/correctIndex and topic position match retained baseline; topic file remains weather-climate','groups':'11*6 literals/hashes generated directly from CURRENT','noCatalogEdits':True,'excludedHolds':[h['id'] for h in a['hold']],'runtimeTests':'NotRun: independent editorial artifacts only; no game/runtime/build/full test needed'},'entries':entries,'readyPASS':[{'id':e['id'],'currentHash':e['currentHash']} for e in entries if e['verdict']=='PASS'],'fix':[e['id'] for e in entries if e['verdict']=='FIX'],'hold':[],'preservation':{'branch':'codex/question-quality-wave-6','commit':'Coordinator owns saving/commit; reviewer did not commit','integration':'Reviewer makes no main integration claim.'}}
(p/'reviewer/review.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
(p/'reviewer/ready-pass.json').write_text(json.dumps({'reviewerThreadId':result['reviewerThreadId'],'entries':result['readyPASS']},ensure_ascii=False,indent=2)+'\n')
print('PASS',len(result['readyPASS']),'FIX',len(result['fix']),'HOLD',len(result['hold']))
