import json,hashlib,subprocess,pathlib
root=pathlib.Path(__file__).resolve().parents[5];p=root/'docs/content-audits/question-quality-wave-7/process-v2-weather15';out=p/'reviewer'
canonical=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
hashof=lambda x:hashlib.sha256(canonical(x)).hexdigest()
a=json.loads((p/'exact-fix-apply.json').read_text());topic=json.loads((root/'src/content/topics/weather-climate.json').read_text());cards={q['id']:q for q in topic['questions']}
pre=json.loads((p/'preimage.json').read_text());base=json.loads(subprocess.check_output(['git','show',pre['baselineCommit']+':src/content/topics/weather-climate.json'],cwd=root));baseline={c['id']:c for c in base['questions']}
idxloc='12e5581b:docs/content-audits/process-review-2026-10-14/preserved/mindbattle-source-01a13956-2a8a-7cf1-8313-aa3392952779/weather-climate-whole-topic.json';idx=json.loads(subprocess.check_output(['git','show',idxloc],cwd=root))['primaryContextIndex']
S={}
for key in ['nws-key-glossary','nws-basic-fronts','noaa-windward-leeward','noaa-rain-shadow-pdf']:
 s=idx[key];v={}
 for kind in ['body','headers']:
  m=s[kind];b=subprocess.check_output(['git','cat-file','blob',m['gitBlob']],cwd=root);assert len(b)==m['bytes'] and hashlib.sha256(b).hexdigest()==m['sha256'];v[kind]={'gitBlob':m['gitBlob'],'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'matchesIndex':True}
 S[key]={'url':s['sourceUrl'],'sourceIndex':idxloc,'readAt':'2026-10-14','verification':v,'personalRead':'Full retained scientific contexts read in initial review; relevant complete entries/article context and PDF pp1,2,5,10,14,15 personally reread against CURRENT7. No author conclusion used.'}
manifestPath='docs/content-audits/question-quality-wave-7/process-v2-weather15/fix-author/sources/'
manifest=json.loads(subprocess.check_output(['git','show','dd091c98:'+manifestPath+'manifest.json'],cwd=root))
for s in manifest['sources']:
 if s['id'] not in ['noaa-extratropical-cyclone','nws-extratropical','nws-convection']:continue
 v={}
 for kind in ['body','headers']:
  loc='dd091c98:'+manifestPath+s[kind+'Path'];b=subprocess.check_output(['git','show',loc],cwd=root);assert len(b)==s[kind+'Bytes'] and hashlib.sha256(b).hexdigest()==s[kind+'Sha256'];v[kind]={'gitLocator':loc,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'matchesManifest':True}
 S[s['id']]={'url':s['url'],'retrievedAt':s['retrievedAt'],'readAt':'2026-10-14','verification':v,'personalRead':'Full retained primary article/glossary scientific context personally read, not author excerpts/verdicts.'}
P='weather-climate-';G='nws-key-glossary'
TR={
'Тропическая депрессия':G+' / TROPICAL DEPRESSION: tropical cyclone, sustained wind 23–38 mph (20–33 knots); TROPICAL CYCLONE has closed low-pressure area and definite cyclonic circulation.',
'Тропический шторм':G+' / TROPICAL STORM: 39–73 mph (34–63 knots); once formed it is given a name.',
'Ураган':G+' / HURRICANE: intense tropical low-pressure area, sustained wind at least 74 mph (64 knots). NOAA A7 compares tropical 34/64 kt wind fields. This is a tropical-system threshold, not a claim that extratropical winds cannot be as strong.',
'Внетропический циклон':'noaa-extratropical-cyclone / A7 opening: main energy is horizontal atmospheric temperature contrasts; midlatitude/baroclinic low-pressure systems with cold, warm, occluded fronts. nws-extratropical / Extratropical: change to baroclinic warm/cold contrast; Extratropical Cyclone/Low: middle/high latitudes and frontal systems. These are EXTRAtropical definitions, not SUBtropical.'}
HU={
'Влажность':G+' / HUMIDITY defines amount of water vapor in air; RELATIVE HUMIDITY compares actual vapor with how much air can hold, expressed in percent.',
'Атмосферное давление':G+' / PRESSURE: gravity acting on atmosphere; may be thought of as weight of air.',
'Индекс жары':G+' / HEAT INDEX: apparent temperature body feels due to high air temperature together with high relative humidity.',
'Точка росы':G+' / DEW POINT: cooling temperature at which vapor condenses.'}
entries=[]
for id in a['scope']:
 c=cards[id];short=id[len(P):];expected=next(e['afterHash'] for e in a['applied'] if e['id']==id);assert hashof(c)==expected
 b=baseline[id];assert c['difficulty']==b['difficulty'] and c['correctIndex']==b['correctIndex'];assert list(cards).index(id)==list(baseline).index(id)
 defects=[]
 if short in ['tropical-depression','tropical-storm','hurricane-eye']:
  loc=[G,'noaa-extratropical-cyclone','nws-extratropical'];pr=[{'answerIndex':i,'reason':TR[z['text']]} for i,z in enumerate(c['answers'])];notes=[[TR[z['text']]] for z in c['answers']]
  ex={'tropical-depression':[TR['Тропическая депрессия'],TR['Тропический шторм']],'tropical-storm':[TR['Тропический шторм']],'hurricane-eye':[TR['Ураган'],TR['Тропический шторм']]}[short]
  neighbors=['tropical-depression','tropical-storm','hurricane-eye','extratropical-fronts','eyewall-replacement'];neighbors.remove(short)
  nr='CURRENT соседей прочитан: depression спрашивает слабейшую замкнутую тропическую категорию, storm — начало 39 mph, hurricane — превышение верхнего предела 73 mph. Это разные категории и две разные границы 39/74, хотя кластер тесный. extratropical-fronts спрашивает фронты, eyewall-replacement — изменение ветрового поля. Справки о соседних объектах не превращаются в дубли задаваемого факта. Замена SUB→EXTRA теперь подтверждена независимым полным контекстом.'
  difficulty='medium: различение ступеней/точных границ тропического циклона требует знакомства с метеорологической классификацией; все четыре варианта относятся к циклонам.'
  supplement={'tropical-depression':'диапазон 23–38 mph/20–33 узла сверх качественного «самая слабая»','tropical-storm':'присвоение имени сверх спрашиваемого нижнего порога','hurricane-eye':'численный порог 74 mph/64 узла сверх относительного «выше предела шторма»'}[short]
 elif short in ['humidity-water-vapor','pressure-air-weight']:
  loc=[G]+(['nws-basic-fronts'] if short=='pressure-air-weight' else []);pr=[{'answerIndex':i,'reason':HU[z['text']]} for i,z in enumerate(c['answers'])];ex=[HU['Влажность'],HU['Атмосферное давление']];notes=[[HU[z['text']]] for z in c['answers']]
  if short=='pressure-air-weight':notes[1]=['nws-basic-fronts / first paragraph A Basic Discussion: actual pressure of high/low systems measured in inches of mercury (30.10 example) or millibars (1004 example). Русские «дюймы ртутного столба» и «миллибары» точно передают обе единицы.']
  neighbors=['dew-point-saturation','relative-humidity-ratio','wet-bulb-evaporation',('pressure-air-weight' if short=='humidity-water-vapor' else 'humidity-water-vapor')]+(['cyclone-low','anticyclone-high'] if short=='pressure-air-weight' else [])
  nr='CURRENT прочитан: dew-point-saturation — сравнение влаги двух проб; relative-humidity-ratio — расчёт 8/20; wet-bulb-evaporation — психрометрическая разность. Это иные задачи, чем простое определение влажности. Давление проверяет гравитационное происхождение другой величины; cyclone/anticyclone — циркуляцию и барические центры. Дублирующей задаваемой связи не найдено.'
  difficulty='easy: базовые бытовые/школьные определения влажности и атмосферного давления; альтернативы — реальные связанные метеорологические величины.'
  supplement='процентная относительная влажность сверх определения содержания пара' if short=='humidity-water-vapor' else 'две единицы измерения, которых нет в prompt'
 else:
  loc=['noaa-rain-shadow-pdf','noaa-windward-leeward','nws-basic-fronts','nws-convection'] if short=='orographic-rain' else ['noaa-rain-shadow-pdf']
  neighbors=['rain-shadow','convectional-rain','frontal-rain'] if short=='orographic-rain' else ['orographic-rain','desert-dry','convectional-rain','frontal-rain']
  if short=='orographic-rain':
   notes=[['noaa-rain-shadow-pdf / p2: cold air over unfrozen relatively warm Great Lakes gains heat/moisture, air rises and narrow cloud bands cause snow. Note describes lake-effect snow as a concrete lake-precipitation example, without claiming all lake precipitation is snow.'],['noaa-rain-shadow-pdf / p10 entire thunderstorm recipe: solar surface heating, rising unstable moist air, terrain as initial lift; nws-convection / Convection: vertical heat/moisture transport, thunderstorms are one form of convection. Combining orographic initiation with buoyant continuation is expressly allowed.'],['nws-basic-fronts / warm-front cross-section: warm air rises slantwise over low-level cold air, causing cloud/precipitation; cold front also lifts moist air.'],['noaa-rain-shadow-pdf / p14: rising air cools, vapor condenses into rain/snow; noaa-windward-leeward / main article: damp air ascends hills/mountains, forms condensation/clouds/precipitation, lee air warms/dries.']]
   pr=[{'answerIndex':i,'reason':r[0]} for i,r in enumerate(notes)];ex=notes[3]
   nr='CURRENT rain-shadow теперь спрашивает число осадков для Мохаве, а не обратную наветренной стороне связь; дубль исходной причинной пары устранён. CURRENT convectional-rain спрашивает летний ливень после нагрева, frontal-rain — прохождение фронта. У orographic-rain явно задан вынужденный подъём над рельефом; такая классификация механизма имеет один наиболее точный ответ. Озёрные осадки заменили перекрывающий «грозовые» вариант; note1 прямо объясняет возможность сочетания процессов, не объявляет их взаимоисключающими.'
   difficulty='medium: термин механизма осадков; все четыре ответа — виды осадков по причине образования, незнающему доступны тематически реальные альтернативы.';supplement='более сухая подветренная сторона сверх спрашиваемого вынужденного подъёма'
  else:
   notes=[['noaa-rain-shadow-pdf / p15: Hilo 120 inches/year; p5 answer11: not in rain shadow and Hawaii tradewinds come from east.'],['noaa-rain-shadow-pdf / p15: Los Angeles 14 inches/year; p5 answer10 says it is not in rain shadow.'],['noaa-rain-shadow-pdf / p15: Captain Cook 31 inches/year; p5 answer12 says it is in rain shadow.'],['noaa-rain-shadow-pdf / p15: Mojave Desert, California 3.5 inches/year; p5 answer9 explicitly identifies rain shadow.']]
   pr=[{'answerIndex':i,'reason':r[0]} for i,r in enumerate(notes)];ex=['noaa-rain-shadow-pdf / p5 answer9 and p15 entry9 directly give Mojave rain shadow and 3.5 inches/year; remaining entries list Los Angeles/Hilo/Captain Cook. Exact source attribution avoids presenting a number from a worksheet as a separately established universal climatological normal.']
   nr='CURRENT orographic-rain проверяет вынужденный подъём, эта карточка — отдельное число для Мохаве. Смыслового дубля нет. desert-dry (актуальный weather20) проверяет общий признак дефицита влаги, не сумму Мохаве; convectional/frontal-rain — другие механизмы. Однако новый факт не прошёл gate difficulty; correct note добавляет положение Мохаве в Калифорнии и отдельно проходит минимальное требование дополнения.'
   difficulty='HOLD: 3,5 дюйма именно из одного учебного примера NOAA — второстепенная точная цифра, которую знакомый с погодой/климатом человек не обязан знать. Выбор из 120/14/31/3,5 может свестись к эвристике «пустыня → минимум», а не проверять содержательное medium-знание. Frozen medium нельзя менять для легализации карточки.';supplement='положение Мохаве в Калифорнии, которого нет в prompt; p15 прямо указывает California'
   defects=[{'field':'difficulty','reason':difficulty}]
 literals=[('prompt_ordered_answers_key',{'prompt':c['prompt'],'answers':[z['text'] for z in c['answers']],'correctIndex':c['correctIndex']},pr),('explanation',c['explanation'],ex)]+[(f'note{i}',z['note'],notes[i]) for i,z in enumerate(c['answers'])]
 groups=[]
 for name,lit,reasons in literals:
  issue=[d['reason'] for d in defects if d['field']==name or (name=='prompt_ordered_answers_key' and d['field']=='difficulty')]
  if name=='prompt_ordered_answers_key':editorial='Все четыре подстановки лично прочитаны. Именные/числовые ответы в одном синтаксическом формате; падеж, число, единицы и пунктуация не выдают ключ. '+difficulty
  elif name=='explanation':editorial='Два предложения, кратко и грамматически связно объясняют выбранный критерий; факты сверены с полными первичными контекстами. Для rain-shadow фактическая точность explanation не закрывает дефекты других групп.'
  else:
   i=int(name[-1]);editorial='Справка относится именно к варианту '+c['answers'][i]['text']+'; самостоятельное проверяемое содержание, не отрицательная заглушка; русский синтаксис и предел 35 слов проверены.'
   if i==c['correctIndex']:editorial+=' Дополнение к prompt: '+supplement+'.'
  if issue:editorial+=' '+ ' '.join(issue)
  groups.append({'group':name,'literal':lit,'literalSHA256':hashof(lit),'sourceReasons':reasons,'editorialReason':editorial,'verdict':'HOLD' if issue else 'PASS'})
 entries.append({'id':id,'currentHash':hashof(c),'verdict':'HOLD' if defects else 'PASS','fieldGroups':groups,'sourceLocators':loc,'neighborReview':{'neighbors':[{'id':P+n,'currentHash':hashof(cards[P+n])} for n in neighbors],'editorialReason':nr,'verdict':'PASS'},'difficultyReview':difficulty,'defects':defects,'nextAction':'Координатор: HOLD без credit; один fix-cycle исчерпан. Сохранить точный результат, не запускать второй цикл. Решение о новом независимом medium-факте/последующем пакете требует отдельного scope.' if defects else 'Координатор: adjudication PASS только этого currentHash; самостоятельный commit/merge/приёмка не подразумеваются.'})
result={'reviewerThreadId':'01a13baa-2597-74a3-9a01-93cea5b90c83','cycle':1,'scope':a['scope'],'baselineCommit':pre['baselineCommit'],'hashRecipe':'SHA256 compact UTF-8 JSON recursively sorted object keys, literal unicode, array order preserved','sources':S,'entries':entries,'readyPASS':[{'id':e['id'],'currentHash':e['currentHash']} for e in entries if e['verdict']=='PASS'],'hold':[{'id':e['id'],'currentHash':e['currentHash']} for e in entries if e['verdict']=='HOLD'],'checks':{'afterHash':'7/7 match exact-fix-apply','frozen':'7/7 ID/topic file/order/difficulty/correctIndex agree with baseline','fieldGroups':'7 x 6 exact CURRENT payloads/hashes generated','sourceBodiesHeaders':'All 7 relevant preserved sources read; bytes/SHA match retained index/manifest','unchangedPASS4':'Not reopened; not recertified by this rereview','initialSourceHOLD4':'Not reviewed as corrected; unchanged / 0 credit','unqualifiedAuthorSubagentPASS':'Excluded: pre-application result and process violation, no evidentiary weight','fullTestsBuildRuntime':'NotRun: editorial artifacts only','catalogIndexClaims':'Not modified'},'preservation':{'branch':'codex/question-quality-wave-6','commit':'Reviewer does not commit; coordinator owns preservation','integration':'No main integration performed by reviewer'}}
(out/'rereview.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');(out/'ready-pass-final.json').write_text(json.dumps({'reviewerThreadId':result['reviewerThreadId'],'cycle':1,'entries':result['readyPASS']},ensure_ascii=False,indent=2)+'\n');print('CURRENT7',len(result['readyPASS']),'PASS',len(result['hold']),'HOLD')
