import json,hashlib,pathlib,subprocess
from decimal import Decimal
root=pathlib.Path('docs/content-audits/question-quality-wave-7/process-v2-weather10/reviewer')
h=lambda v:hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
manifest=json.load(open(root.parent/'exact-fix-apply.json'));topic=json.load(open('src/content/topics/weather-climate.json'));arr=topic['questions'] if isinstance(topic,dict) else topic;qs={q['id']:q for q in arr}
rawbase=json.loads(subprocess.check_output(['git','show','31aa848b:src/content/topics/weather-climate.json']));basearr=rawbase['questions'] if isinstance(rawbase,dict) else rawbase;base={q['id']:q for q in basearr}
idx=json.loads(subprocess.check_output(['git','show','12e5581b:docs/content-audits/process-review-2026-10-14/preserved/mindbattle-source-01a13956-2a8a-7cf1-8313-aa3392952779/weather-climate-whole-topic.json']))['primaryContextIndex']
# Arithmetic applies to the exact hypothetical prompt; these are not claimed observed source data.
fall=Decimal('16.0')-Decimal('2.5');depth=Decimal('2.9')-Decimal('0.4');rate=fall/depth
assert (fall,depth,rate)==(Decimal('13.5'),Decimal('2.5'),Decimal('5.4'))
assert Decimal('4.0')*depth==Decimal('10.0')
assert Decimal('10.4')-Decimal('2.5')==Decimal('7.9')
records={}
def add(suffix,verdict,keys,options,explanation,notes,editorial,noteEditorial,neighbors,neighborReason,defects=(),action='Координатор: принять точный CURRENT по hash после adjudication и сохранить commit.'):
 records['weather-climate-'+suffix]=dict(verdict=verdict,keys=keys,options=options,explanation=explanation,notes=notes,editorial=editorial,noteEditorial=noteEditorial,neighbors=neighbors,neighborReason=neighborReason,defects=list(defects),action=action)
add('environmental-lapse','HOLD',['nws-environmental-lapse','nws-adiabatic','nws-stability'],[
'По exact условию 4,0×(2,9−0,4)=10,0 °C; это меньше actual заданного перепада 16,0−2,5=13,5 °C. Число правдоподобно как ошибочный расчёт, но не ключ.',
'По exact условию (16,0−2,5)/(2,9−0,4)=13,5/2,5=5,4 °C/км. NWS Environmental Lapse Rate определяет decrease temperature with height; key correctIndex 1 единственен.',
'7,9 °C — разность 10,4−2,5 между промежуточным и верхним уровнем; это не скорость полного слоя. Вариант моделирует ошибку единиц/выбора интервала.',
'NWS Adiabatic Lapse Rate даёт 9,8 °C/км для ненасыщенной частицы. Это не наблюдаемый средний градиент из заданных крайних уровней.'
], 'Точные крайние значения дают 13,5 °C на 2,5 км, то есть 5,4 °C/км. NWS Environmental Lapse Rate подтверждает предмет измерений радиозондом; NWS Neutral Stability сопоставляет градиент среды с сухим или влажным адиабатическим в зависимости от насыщения.',[
'Вычислено непосредственно из prompt: 4,0×2,5=10,0 °C против 13,5 °C заданного перепада. Note конкретно разбирает числовой дистрактор.',
'NWS Environmental Lapse Rate прямо определяет decrease temperature with height, usually measured with radiosonde. Note раскрывает смысл измеряемой величины, добавляя определение к числовому ключу.',
'Exact prompt: 10,4−2,5=7,9 °C для высот 1,1 и 2,9 км; единицы °C отличаются от °C/км, и этот интервал не равен полному 0,4–2,9 км.',
'NWS Adiabatic Lapse Rate прямо устанавливает 9,8 °C/км для unsaturated lifted parcel без теплообмена; NWS Environmental Lapse Rate отдельно относится к окружающей атмосфере.'
], 'Грамматика числовых подстановок, единицы и уникальность ключа исправны. Однако CURRENT прямо спрашивает среднюю скорость падения на заданном слое: два вычитания и деление не требуют специальной метеорологии, промежуточное показание игнорируется. Абсолютная оценка medium (обычная школьная скорость изменения), не frozen hard. Новые числа сами по себе сложности hard не создают.',[
'Полезная адресная арифметическая справка, не пустая заглушка.',
'Правильная note добавляет определение градиента среды и способ измерения к спрашиваемому числу.',
'Справка связывает ошибочное число с конкретным неполным интервалом; не приписывает ему правильную скорость.',
'Справка привязана к известному сухоадиабатическому числу и различает частицу/среду.'
], ['weather-climate-dry-adiabatic-rate','weather-climate-inversion-positive','weather-climate-inversion-warmer-above'], 'CURRENT dry-adiabatic-rate требует учёта двух разных средовых градиентов и смены слоя для равенства частицы/среды. Новый environmental-lapse не повторяет этот факт, но значительно проще. Две инверсии проверяют знак профиля/расположение основания, другие факты.', ['difficulty hard / prompt: простой расчёт среднего перепада на высоту не содержит специфического знания или содержательной hard-логики; дефект сложности после одного fix-cycle не закрыт.'], 'Координатор: сохранить HOLD точного hash и вынести решение о дальнейшей судьбе frozen-hard слота/калибровке человеку. В этом пакете второй fix-cycle не выполнять.')
add('inversion-positive','HOLD',['nws-inversion','nws-adiabatic','nws-environmental-lapse'],[
'NWS Dry Adiabatic Lapse Rate описывает охлаждение ненасыщенной частицы. По условию среда при движении вверх нагревается, это иной профиль.',
'NWS Moist Adiabatic Lapse Rate описывает охлаждение насыщенной поднятой частицы и зависит от T/P; это не рост температуры окружающей среды между уровнями.',
'NWS Temperature Inversion определяет рост T с высотой. Из 11 °C на 1,2 км и 17 °C на 1,8 км этот рост виден напрямую; Capping Inversion подтверждает подавление подъёма частицы. Key 2 верен.',
'NWS Environmental Lapse Rate является общим измеренным градиентом среды. Инверсия конкретнее классифицирует его знак; более общий термин не является лучшей классификацией указанного барьера.'
], 'Из exact чисел 17>11 при 1,8>1,2 следует повышение температуры с высотой, соответствующее NWS Temperature Inversion. NWS Capping Inversion описывает тёплый слой, в котором поднятая частица холоднее окружения, и подавление/задержку гроз.',[
'NWS Adiabatic Lapse Rate прямо даёт 9,8 °C/км для lifted unsaturated parcels.',
'NWS Moist Adiabatic Lapse Rate прямо говорит о saturated lifted parcel, непостоянстве и зависимости от температуры/давления.',
'NWS Capping Inversion прямо описывает explosive thunderstorm development при removed/weakened cap. Это самостоятельный полезный эффект снятия барьера, не повтор определения роста T.',
'NWS Environmental Lapse Rate прямо определяет фактический градиент окружающего воздуха и radiosonde.'
], 'Четыре именные подписи согласованы. Но 11→17 °C при 1,2→1,8 км лишь численно повторяет определение инверсии. Упоминание остановки частицы и возврата к убыванию выше не требуется для ключа. Тематическому читателю достаточно базового знания инверсии: medium, не hard. Текущий сценарий не закрывает ранее адресно указанный дефект.',[
'Конкретная справка о числе для сухой ненасыщенной частицы.',
'Конкретная справка о зависимости влажного градиента от T/P.',
'Correct note добавляет последствие ослабления инверсионной крышки.',
'Самостоятельное определение градиента среды и способа его измерения.'
], ['weather-climate-inversion-warmer-above','weather-climate-convection-buoyancy','weather-climate-environmental-lapse'], 'CURRENT inversion-warmer-above различает приземное/приподнятое основание; convection-buoyancy проверяет сухую конвекцию; environmental-lapse — среднюю измеренную скорость изменения T. Прямого дубля нет, но эти medium-распознавания подтверждают недостаточную сложность нового hard-профиля.', ['difficulty hard / prompt: прямое узнавание роста температуры с высотой осталось medium; добавленные числа и описание барьера не являются необходимой hard-логикой.'], 'Координатор: сохранить HOLD по новому hash, передать человеку конкретное решение о frozen-hard слоте/калибровке. Второй fix-cycle этой карточки не запускать.')
add('lightning-electric','PASS',['nws-lightning','nws-thunder','nws-rainbow','nasa-auroras','nws-thunder-jetstream'],[
'NWS Thunder определяет sound caused by expanding gases, не видимый electrical discharge. Сопутствующий эффект грозы — правдоподобная путаница.',
'NWS Lightning прямо определяет visible electrical discharge produced by thunderstorm: key 1. Широко известный взрослой аудитории факт соответствует easy.',
'NWS Rainbow определяет luminous arc от refraction/reflection/dispersion солнечного света через воду; это другой видимый атмосферный эффект, не грозовой разряд.',
'NASA Auroras объясняет свечение возбуждением atmospheric gas energetic particles; это другой световой атмосферный эффект, не lightning discharge.'
], 'NWS Lightning подтверждает электрический видимый разряд при грозе и направления within/between clouds, cloud-air, cloud-ground; explanation не добавляет неподтверждённых ограничений.',[
'NWS Thunder говорит о rapidly expanding gases; дополнительно лично прочитанный сохранённый NWS Sound of Thunder прямо описывает нагрев воздуха у lightning channel и explosive expansion. Это подтверждает и звук, и нагрев.',
'NWS Lightning Channel определяет typical ground-cloud flash как composite из sequential strokes; note добавляет составность к определению разряда.',
'NWS Rainbow прямо даёт refraction, total reflection и dispersion, sunlight через water spray/raindrops. Русская note передаёт все три механизма.',
'NASA What Causes Auroras / More on Physics: energetic particles дают extra energy atoms/molecules atmospheric gases, высотные gas emissions описаны в Why Are Auroras Colorful. Это подтверждает excitation верхней атмосферы.'
], 'Новый разрешённый независимый факт с тем же correctIndex 1: молния как электрический разряд. Полярность и подсказка частоты устранены. Четыре атмосферных явления одной категории, русские именные ответы согласованы; гром можно спутать как вторую часть грозы, радуга/сияние — другие видимые эффекты. Easy соответствует общеизвестному определению без редкой детали.',[
'Самостоятельная справка именно о громе и механизме звука.',
'Correct note содержит дополнительный факт о последовательности ударов.',
'Справка именно о радуге и её оптическом механизме.',
'Справка именно о полярном сиянии и возбуждении атмосферных газов.'
], ['weather-climate-thunder-sound','weather-climate-rainbow-refraction','weather-climate-aurora-particles'], 'Точный CURRENT thunder-sound проверяет короткий звук/расстояние; rainbow-refraction — второй порядок по числу отражений; aurora-particles — солнечные частицы и высокие широты. Новый lightning-electric проверяет электрический разряд при грозе; это отдельный факт, а не обратная карточка об акустике/частицах.')
add('el-nino-warm','PASS',['nws-enso','noaa-nao'],[
'NWS La Niña описывает rain increase over Indonesia и decrease over central/eastern Pacific; это противоположно заданному осадочному распределению.',
'NWS El Niño прямо описывает rainfall reduced over Indonesia и increased over central/eastern tropical Pacific; key 1.',
'CPC NAO описывает dipole pressure/height и North Atlantic jet/storm-track changes. Климатический режим той же категории, но иного механизма, не описанная ENSO схема осадков.',
'NWS Neutral — neither El Niño nor La Niña, often SST near average с оговоркой ocean/atmosphere mismatch. Нейтральность не именует характерную заданную El Niño схему.'
], 'NWS El Niño напрямую подтверждает две области противоположного изменения rainfall и ослабление normal easterly equatorial surface winds.',[
'NWS La Niña прямо подтверждает увеличение rainfall над Индонезией и уменьшение над central/eastern tropical Pacific.',
'NWS El Niño: обычные low-level east-to-west surface winds слабеют и иногда start west-to-east. Note добавляет ветровой отклик к осадочному вопросу.',
'CPC NAO: north-south dipole anomalies, opposite pressure/height signs; обе фазы меняют location/intensity jet stream и storm track.',
'NWS Neutral: Neither El Niño nor La Niña; Often tropical Pacific SSTs generally close to average. Оговорка «часто» сохраняет случаи рассогласования океана/атмосферы.'
], 'Теперь спрашивается климатический режим, а не фаза ENSO: NAO больше не исключён формально чужой категорией. Региональное изменение осадков — содержательное medium-знание, не географическая подсказка совпадающего названия. Четыре именные подписи согласованы и сопоставимы.',[
'Справка о конкретном режиме La Niña, с проверенными регионами осадков.',
'Correct note даёт дополнительный ветровой факт, отсутствующий в prompt.',
'Справка сообщает собственный pressure/height и jet/storm-track механизм NAO.',
'Самостоятельная справка о нейтральности и частой близости температуры к средней.'
], ['weather-climate-la-nina-cool','weather-climate-nao-pressure','weather-climate-iod-indian'], 'Новый La Niña спрашивает усиление восточных ветров, а El Niño — перераспределение осадков. Это разные атмосферные отклики, не прежний зеркальный warm/cool SST-вопрос. NAO спрашивает pressure/height dipole; IOD — сравнение океанических температур у разных берегов. Связь ENSO notes с соседними facts допустима; вопросы различаются.')
add('la-nina-cool','PASS',['nws-enso','noaa-nao'],[
'NWS El Niño: нормальные easterlies weaken or reverse, не усиление.',
'NWS La Niña: normal easterly winds along equator become even stronger; key 1.',
'CPC NAO описывает North Atlantic pressure/height и jet/storm track, не экваториальное усиление easterly surface winds ENSO.',
'NWS Neutral — ни El Niño, ни La Niña, а не именованный режим усиления обычных equatorial easterlies.'
], 'NWS La Niña прямо подтверждает усиление normal equatorial easterlies, увеличение rainfall over Indonesia и уменьшение over central/eastern tropical Pacific.',[
'NWS El Niño напрямую говорит о weakening/reversal normal easterly winds.',
'NWS La Niña напрямую даёт rain increase Indonesia / decrease central/eastern tropical Pacific. Correct note дополняет вопрос о ветрах осадочным откликом.',
'CPC NAO напрямую даёт opposite pressure/height dipole и basin-wide jet/storm-track changes.',
'NWS Neutral напрямую даёт neither El Niño nor La Niña и often near-average tropical Pacific SST. SST соответствует source sea surface temperature; аббревиатура техническая, но факт проверен; предпочтительна русская расшифровка при будущей редактуре, без нового fix-cycle.'
], 'Усиление обычных экваториальных восточных ветров — самостоятельный medium-факт о режиме. Категория «климатический режим» подходит всем четырём подписям; явной подсказки NAO исключением из фаз ENSO больше нет. «Низовые» понятны как low-level; «приземные» и русская расшифровка SST были бы стилистически яснее, но смысл и уникальность ключа не меняют.',[
'Справка о конкретном ветровом отклике El Niño.',
'Correct note добавляет осадочный отклик к вопросу о ветре.',
'Справка о самостоятельном режиме NAO, не пересказ правильного ответа.',
'Справка самостоятельна по нейтральному ENSO; английская аббревиатура SST — малозначимая редакторская оговорка, раскрытый source-term sea surface temperature, не непроверенный факт.'
], ['weather-climate-el-nino-warm','weather-climate-nao-pressure','weather-climate-iod-indian'], 'Новый El Niño проверяет распределение rainfall, а La Niña — intensification equatorial easterlies. Это разные признаки ENSO, а не два вопроса с одной сменой знака SST. NAO — dipole pressure/height; IOD — western/eastern basin SST, иной факт.')
add('nao-pressure','PASS',['noaa-nao','nws-enso'],[
'NWS El Niño: tropical Pacific ocean-atmosphere warming/rainfall/wind pattern, не north-south pressure/height dipole CPC.',
'CPC NAO прямо определяет north-south dipole opposite anomalies и изменения intensity/location North Atlantic jet stream/storm track. Key 1; удалённые Icelandic Low/Azores High больше не требуют неподтверждённого контекста.',
'NWS La Niña: cold SST phase с усилением equatorial easterlies; это не заданная pressure/height телесвязь.',
'NWS Neutral: neither El Niño nor La Niña, обычно near-average tropical Pacific SST; это не NAO dipole.'
], 'CPC NAO прямо даёт два opposite-sign anomaly centers и обе фазы с jet/storm-track changes; European temperature/precipitation including winter effects подтверждены отдельными абзацами. Непроверенные географические имена удалены.',[
'NWS El Niño прямо даёт rain decrease Indonesia, increase central/eastern tropical Pacific.',
'CPC Strong positive phase: above-average temperature northern Europe и above-average winter precipitation northern Europe/Scandinavia. Note добавляет конкретный фазовый климатический эффект к диполю.',
'NWS La Niña прямо даёт normal easterly equatorial winds become stronger.',
'NWS Neutral прямо даёт neither El Niño nor La Niña и often tropical Pacific SST near average. «Часто» не превращено в абсолютное условие.'
], 'Географическое слово «Северная Атлантика», напрямую повторявшее ключ, из prompt удалено. Теперь нужно узнать давление/высотные аномалии и изменение jet/storm track — medium тематическое знание. «Аномалии высоты» передаёт source heights в метеорологическом контексте; возможное уточнение «геопотенциальной высоты» — stylistic clarity, не ложный факт. Четыре климатических режима грамматически согласованы.',[
'Справка конкретно о региональном дождевом отклике El Niño.',
'Correct note даёт дополнительный факт о сильной положительной фазе в Европе.',
'Справка конкретно о ветрах La Niña.',
'Справка конкретно о нейтральной фазе и часто средней температуре.'
], ['weather-climate-el-nino-warm','weather-climate-la-nina-cool','weather-climate-iod-indian'], 'CURRENT El Niño спрашивает rainfall shift, La Niña — equatorial wind strengthening, IOD — ocean temperature west/east. Новый NAO спрашивает pressure/height dipole и jet/storm track без географического раскрытия названия. Отдельные величины и процессы, смыслового дубля нет.')
readkeys=sorted({k for r in records.values() for k in r['keys'] if k in idx})
for k in readkeys:
 v=idx[k];b=subprocess.check_output(['git','show',v['gitCommit']+':'+v['body']['path']]);assert hashlib.sha256(b).hexdigest()==v['body']['sha256']
extraPath='docs/content-audits/question-quality-wave-7/coordinator-continuation-01a13772/weather5b-e933b9f/raw-capture/thunder-jetstream.body'
extraCommit='9b2b0b1a225b2970e916c023b35986e0449e4d31';extraBody=subprocess.check_output(['git','show',extraCommit+':'+extraPath]);extraBlob=subprocess.check_output(['git','rev-parse',extraCommit+':'+extraPath]).decode().strip()
entries=[]
for id in manifest['scope']:
 q=qs[id];r=records[id];assert h(q)==next(a['afterHash'] for a in manifest['applied'] if a['id']==id)
 assert all(q[f]==base[id][f] for f in ['id','difficulty','correctIndex']);assert arr.index(q)==basearr.index(base[id]);assert len(q['answers'])==4 and len({a['text'] for a in q['answers']})==4
 literals=[dict(prompt=q['prompt'],answers=[a['text'] for a in q['answers']],correctIndex=q['correctIndex']),q['explanation']]+[a['note'] for a in q['answers']]
 groups=[]
 for i,(name,literal) in enumerate(zip(['prompt_ordered_answers_key','explanation','note0','note1','note2','note3'],literals)):
  reasons=r['options'] if i==0 else [r['explanation']] if i==1 else [r['notes'][i-2]]
  ed=r['editorial'] if i==0 else 'Explanation проверено целиком: 2 предложения, до 70 слов, русский и фактическая причинная связь согласованы.' if i==1 else r['noteEditorial'][i-2]
  groups.append(dict(group=name,literal=literal,literalSHA256=h(literal),sourceReasons=reasons,editorialReason=ed))
 locs=[]
 for k in r['keys']:
  if k in idx:
   v=idx[k];locs.append(dict(sourceId=k,sourceUrl=v['sourceUrl'],typedLocator=v['typedLocator'],gitCommit=v['gitCommit'],body=v['body'],readMethod='git show gitCommit:body.path; personally read scientific context; body SHA verified'))
  else:locs.append(dict(sourceId=k,sourceUrl='https://www.weather.gov/source/zhu/ZHU_Training_Page/lightning_stuff/lightning2/thunder.html',typedLocator='The Sound of Thunder: heat lightning channel and explosive air expansion',gitCommit=extraCommit,body=dict(path=extraPath,gitBlob=extraBlob,sha256=hashlib.sha256(extraBody).hexdigest(),bytes=len(extraBody)),readMethod='personally read complete retained primary page via Git'))
 entries.append(dict(id=id,currentHash=h(q),verdict=r['verdict'],fieldGroups=groups,sourceLocators=locs,neighborReview=dict(ids=r['neighbors'],currentHashes={n:h(qs[n]) for n in r['neighbors']},editorialReason=r['neighborReason']),defects=r['defects'],nextAction=r['action'],frozenContract=dict(idTopicOrderCorrectIndexDifficultyPreserved=True,baseline='31aa848b',topicFile='src/content/topics/weather-climate.json',order=arr.index(q),correctIndex=q['correctIndex'],difficulty=q['difficulty'],independentFactReplacementAllowed=True)))
result=dict(reviewerThreadId='01a13b89-56e0-7661-a8d3-88b67254735f',cycle=1,baseline='31aa848b',branch='codex/question-quality-wave-6',sourceIndexRef='12e5581b:docs/content-audits/process-review-2026-10-14/preserved/mindbattle-source-01a13956-2a8a-7cf1-8313-aa3392952779/weather-climate-whole-topic.json',entries=entries,checks=dict(afterHashMatches='6/6',frozenIdTopicOrderCorrectIndexDifficulty='6/6',exactFieldGroups='36 with generated literal/hash',sourceBodiesVerified=len(readkeys)+1,previousPass4Reread=False,fullQa=False,build=False,runtime=False,catalogOrIndexEdited=False),editorialAdjudication='Two difficulty HOLD judgments are independent human-audience calibration, not arithmetic or source failures. No second fix-cycle requested.',frozenContractCorrection='Earlier literal/semantic freezing of the correct answer was overbroad; only ID/topic/order/correctIndex/difficulty quotas frozen. Full independently reviewed fact replacements allowed. Historical review remains immutable; this rereview supersedes only six hashes.')
(root/'rereview.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
(root/'pass-fix-cycle-current.json').write_text(json.dumps(dict(reviewerThreadId=result['reviewerThreadId'],cycle=1,entries=[dict(id=e['id'],currentHash=e['currentHash']) for e in entries if e['verdict']=='PASS']),ensure_ascii=False,indent=2)+'\n')
print('CURRENT6:',{v:sum(e['verdict']==v for e in entries) for v in ['PASS','HOLD']})
