import json,hashlib,subprocess,pathlib
root=pathlib.Path('docs/content-audits/question-quality-wave-7/process-v2-weather10/reviewer')
def h(v):return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
manifest=json.load(open(root.parent/'exact-apply.json'))
topic=json.load(open('src/content/topics/weather-climate.json'));questions=topic['questions'] if isinstance(topic,dict) else topic
qs={q['id']:q for q in questions}
base=json.loads(subprocess.check_output(['git','show','31aa848b:src/content/topics/weather-climate.json']))
bqs={q['id']:q for q in (base['questions'] if isinstance(base,dict) else base)}
index=json.loads(subprocess.check_output(['git','show','codex/question-review-process:docs/content-audits/process-review-2026-10-14/preserved/mindbattle-source-01a13956-2a8a-7cf1-8313-aa3392952779/weather-climate-whole-topic.json']))['primaryContextIndex']
# Independent readings of source bodies, with integrity checks, not inherited editorial decisions.
readkeys=['nws-environmental-lapse','nws-stability','nws-cape','spc-parcel-values','nws-lightning','nws-inversion','nws-adiabatic','nws-trough','nws-ridge','spc-shear','nws-enso','noaa-nao','noaa-jetstream','nws-flight-environment','nws-key-glossary']
for k in readkeys:
 b=subprocess.check_output(['git','cat-file','blob',index[k]['body']['gitBlob']]);assert hashlib.sha256(b).hexdigest()==index[k]['body']['sha256']
records={}
def rec(suffix,verdict,keys,options,explanation,notes,editorial,neighbors,neighborReason,defects=(),action='Координатор может принять точный CURRENT после adjudication.'):
 records['weather-climate-'+suffix]=dict(verdict=verdict,keys=keys,options=options,explanation=explanation,notes=notes,editorial=editorial,neighbors=neighbors,neighborReason=neighborReason,defects=list(defects),action=action)
rec('environmental-lapse','FIX',['nws-environmental-lapse','nws-stability','nws-adiabatic','nws-inversion'],[
'NWS Adiabatic Lapse Rate определяет охлаждение поднимающейся частицы без теплообмена; это модель частицы, а не измеренный профиль среды.',
'NWS Environmental Lapse Rate определяет изменение температуры окружающего воздуха с высотой и измерение радиозондом: ключ 1 соответствует объекту измерений.',
'NWS Moist Adiabatic Lapse Rate относится к насыщенной поднимающейся частице, а не окружающей атмосфере.',
'NWS Temperature Inversion обозначает частный профиль с ростом температуры; условие не задаёт знак, поэтому инверсия не следует из него.'
], 'NWS Environmental Lapse Rate подтверждает определение и радиозонд; Neutral Stability в NWS Stability связывает градиент среды с сухим/влажным адиабатическим градиентом.',[
'NWS Adiabatic Lapse Rate даёт 9,8 °C/км для ненасыщенной поднимающейся частицы.',
'NWS Environmental Lapse Rate прямо называет радиозонд; NWS Neutral Stability сравнивает градиент среды с адиабатическим при соответствующем насыщении.',
'NWS Moist Adiabatic Lapse Rate прямо указывает зависимость от температуры и давления.',
'NWS Temperature Inversion прямо определяет рост температуры с высотой.'
], 'Русский вопрос и четыре именные подписи согласованы; различение среды и частицы требует тематического знакомства, но в CURRENT нет специфической детали или содержательной логики для hard. Абсолютная оценка medium; difficulty менять нельзя.', ['weather-climate-dry-adiabatic-rate','weather-climate-inversion-positive','weather-climate-inversion-warmer-above'], 'Сосед dry-adiabatic-rate требует двухслойного расчёта равенства температур; инверсионные карточки проверяют тип профиля. Самостоятельный факт измеряемого градиента не дублирует этот расчёт.', ['prompt: простое узнавание определения не соответствует frozen hard.'], 'Автор: за один цикл усложнить содержательную задачу о наблюдаемом градиенте среды при неизменных ID/topic/difficulty/key, без повторения расчёта dry-adiabatic-rate; затем повторно проверить только эту карточку и соседей.')
rec('inversion-positive','FIX',['nws-inversion','nws-adiabatic','nws-environmental-lapse'],[
'NWS Dry Adiabatic Lapse Rate описывает охлаждение ненасыщенной частицы при подъёме, не рост температуры окружающей среды.',
'NWS Moist Adiabatic Lapse Rate описывает насыщенную частицу, не измеренный тёплый верхний слой.',
'NWS Temperature Inversion определяет повышение температуры с высотой; Capping Inversion описывает потерю плавучести поднятой частицы.',
'Environmental Lapse Rate является общим измеренным градиентом; инверсия точнее классифицирует заданный знак, но варианты имеют отношение общего и частного.'
], 'NWS Temperature Inversion подтверждает рост температуры; Capping Inversion отдельно подтверждает, что поднятая частица становится холоднее окружения и её подъём подавляется.',[
'NWS Adiabatic и Dry Adiabatic Lapse Rate подтверждают отсутствие теплообмена и ненасыщенность частицы.',
'NWS Moist Adiabatic Lapse Rate подтверждает охлаждение насыщенной частицы и зависимость от температуры/давления.',
'NWS Capping Inversion прямо описывает подавление гроз при extreme instability и explosive development при ослаблении крышки; note дополняет основной профиль.',
'NWS Environmental Lapse Rate прямо подтверждает реальный профиль окружающей атмосферы и радиозонд.'
], 'Грамматика согласована. Вторая часть условия о частице не требуется для выбора инверсии: ответ уже даёт простое описание роста температуры. Абсолютно medium, а не frozen hard; желательно спросить наиболее конкретный тип, чтобы снять общее/частное.', ['weather-climate-inversion-warmer-above','weather-climate-convection-buoyancy','weather-climate-environmental-lapse'], 'CURRENT inversion-warmer-above проверяет приземное основание против приподнятого; это отдельный факт, прямого дубля нет. Тематическое соседство с градиентом и сухой конвекцией допустимо.', ['prompt: базовое определение инверсии не соответствует frozen hard; описательная добавка не добавляет необходимой логики.'], 'Автор: один адресный цикл — создать содержательную hard-задачу о инверсионном профиле/барьере, сохраняя ключ и избегая вопроса о приземном основании; снять неоднозначность общего градиента среды.')
rec('cape-buoyancy','PASS',['nws-cape','spc-parcel-values','spc-shear'],[
'SPC CINH интегрирует отрицательную площадь от исходного уровня до LFC; условие задаёт положительную энергию между LFC и EL.',
'SPC Lifted Index — разность температур на 500 mb, не интеграл по слою.',
'SPC Storm Relative Helicity представляет streamwise vorticity во входящем слое шторма, а не термодинамическую энергию.',
'SPC CAPE прямо определяет интегрированную положительную площадь в J/kg от LFC до EL; NWS CAPE описывает тёплую относительно среды частицу.'
], 'SPC CAPE задаёт интеграл от LFC до EL и J/kg; NWS связывает CAPE с потенциальной скоростью восходящего потока и предупреждает об отсутствии гарантированного порога наступления severe weather. Это не гарантия запуска грозы.',[
'SPC CINH определяет отрицательную площадь и энергию достижения LFC.',
'SPC Lifted Index сравнивает поднятую частицу и sounding на 500 mb (500 гПа).',
'SPC Storm Relative Helicity прямо определяет streamwise vorticity внутри storm inflow layer; «потоковая завихрённость» передаёт этот смысл.',
'SPC CAPE задаёт J/kg и связь с updraft strength, NWS CAPE отрицает автоматическое наступление опасной погоды; note даёт единицы и практический предел использования.'
], 'Специальное чтение зондирования и различение интегрального, локального и кинематического индексов соответствует hard. Четыре индекса правдоподобны; все именные подстановки согласованы, ровно ключ 3.', ['weather-climate-cin-cap','weather-climate-lifted-index','weather-climate-helicity-rotation'], 'Соседи проверяют соответственно барьер до LFC, знак локального температурного индекса и вращение суперячейки. CURRENT проверяет интегральную положительную энергию ограниченного слоя; это отдельный термодинамический факт.')
rec('lightning-electric','FIX',['nws-lightning'],[
'NWS In-Cloud Lightning действительно протекает внутри облака, но не удовлетворяет явно заданному cloud-to-ground разряду.',
'NWS Positive Cloud to Ground Lightning противопоставляет доставляемый положительный заряд более распространённому отрицательному; ключ 1 фактологически верен.',
'NWS описывает положительный CG как менее частый относительно отрицательного; это уже сказано в prompt.',
'NWS утверждает более частый отрицательный заряд, поэтому равная частота противоречит первичному определению.'
], 'NWS Positive CG подтверждает более распространённый отрицательный заряд; Lightning Channel/Stroke подтверждают несколько последовательных ударов с лидером и return streamer.',[
'NWS In-Cloud Lightning определяет молнию внутри облака; note полезна, но сам вариант противоречит условию облако—земля.',
'NWS Lightning Channel и Lightning Stroke подтверждают последовательные удары, leader и return streamer; это дополнительный факт к полярности.',
'NWS Positive CG противопоставляет эту полярность более распространённой отрицательной; note фактически правильна.',
'NWS Lightning перечисляет разряды внутри/между облаками, облако—воздух и облако—земля; Positive CG даёт неравную частоту, а не вывод о частоте из направления.'
], 'Полярность распространённых CG-разрядов — специальный факт, не общеизвестный easy. CURRENT превращает его в логическую подсказку: более редкие положительные уже названы в условии. «Заряд не достигает земли» не подстановка к вопросу «какой заряд»; варианты неоднородны.', ['weather-climate-thunder-sound','weather-climate-rainbow-refraction','weather-climate-aurora-particles'], 'Сосед thunder-sound проверяет форму звука и расстояние; rainbow — оптику, aurora — возбуждение частицами. Сам факт полярности независим, но качество easy и вариантов неудовлетворительно.', ['prompt: раскрывает неравную частоту положительных разрядов и делает ключ выводимым из авторской подсказки.','difficulty: факт о знаке заряда не соответствует frozen easy без такой подсказки.','answers[0], answers[3]: не четыре сопоставимые подписи зарядов; первый противоречит cloud-to-ground в условии.'], 'Автор: один цикл — вернуть широко известный независимый факт о молнии для frozen easy, сохранив смысл ключа/его позицию по контракту; если с frozen ключом это невозможно, HOLD с запросом конкретного продуктового решения, не смена difficulty.')
rec('trough-elongated-low','PASS',['nws-trough','nws-ridge','nws-key-glossary','live-nws-cyclone'],[
'NWS Trough определяет elongated relatively low pressure, usually without closed circulation: ключ 0.',
'NWS Cyclone определяет циркуляцию вокруг central low pressure; это замкнутый центр в отличие от обычно незамкнутой ложбины.',
'NWS Anticyclone определяет циркуляцию вокруг central high pressure; знак и морфология не отвечают условию.',
'NWS Ridge определяет elongated relatively high pressure — противоположный знак.'
], 'NWS Trough прямо даёт вытянутую область низкого давления, обычное отсутствие closed circulation и противопоставление ridge.',[
'NWS Shortwave Trough прямо описывает подъём перед возмущением и возможный вклад в грозы при благоприятных условиях; note содержит проверенный дополнительный факт.',
'Прочитанный NWS Cyclone описывает large-scale circulation around central low pressure; контекст Trough отдельно противопоставляет closed low.',
'Прочитанный NWS Anticyclone определяет circulation around central high pressure; Key West ANTICYCLONE подтверждает high pressure system.',
'NWS Ridge прямо определяет вытянутую область относительно высокого давления и opposite of trough.'
], 'Русский и четыре барических термина согласованы. Medium соответствует тематическому знанию морфологии; cyclone — сильный правдоподобный дистрактор того же знака. Ключ уникален.', ['weather-climate-ridge-elongated-high','weather-climate-cyclone-low','weather-climate-anticyclone-high'], 'Проверены три разные морфологические задачи: закрытый low у cyclone-low, вращение вокруг high у anticyclone-high, вытянутый high у ridge. Ridge/trough тематически зеркальны по знаку, но проверяют две отдельные формы поля давления, а не прямую/обратную привязку одной пары объекта и места. Пересечение отмечено; автоматического дубля не объявляю.')
rec('ridge-elongated-high','PASS',['nws-ridge','nws-trough','live-nws-cyclone','live-nws-theta-e'],[
'NWS Ridge определяет elongated relatively high pressure, opposite of trough: ключ 0.',
'NWS Cyclone — циркуляция вокруг центрального низкого давления, а не вытянутый high.',
'NWS Anticyclone — циркуляция вокруг central high; дистрактор того же знака, но иной морфологии.',
'NWS Trough — вытянутый low, противоположный знак.'
], 'NWS Ridge имеет два значения: вытянутый atmospheric high и hydrological line/wall of broken ice. Оба предложения фактически верны, хотя второе повторяет определение и затем вводит малополезный для барики гидрологический смысл.',[
'NWS Theta-e Ridge определяет ось высоких theta-e; дополнительно реально прочитанный NWS Theta-e раскрывает Equivalent Potential Temperature, подтверждая русское название. Note добавляет другой вид гребня.',
'NWS Cyclone задаёт циркуляцию вокруг central low pressure; Trough противопоставляет closed low.',
'NWS Anticyclone задаёт circulation around central high pressure; distinction от вытянутого Ridge вытекает из двух определений.',
'NWS Trough определяет вытянутый относительно низкий pressure, opposite of ridge.'
], 'Medium и барические дистракторы оправданы: антициклон совпадает по знаку, ложбина по вытянутой форме. Имённые подписи грамматически последовательны; θe-note специальная, но понятие раскрыто русским названием. Редакторская избыточность explanation не блокирует достоверность.', ['weather-climate-trough-elongated-low','weather-climate-cyclone-low','weather-climate-anticyclone-high'], 'Полностью прочитаны CURRENT этих соседей. Есть тесная тематическая зеркальность с Trough, но закрытая циркуляция и знак/морфология различают объекты; независимость оцениваю как достаточную для барического набора, с явно отмеченным пересечением.')
rec('el-nino-warm','FIX',['nws-enso','noaa-nao'],[
'NWS ENSO задаёт La Niña как cooling, а не warm phase.',
'NWS ENSO задаёт El Niño как warming/above-average SST в central and eastern tropical Pacific: ключ 1.',
'CPC NAO описывает североатлантический dipole pressure/height anomalies; это климатический режим, но не фаза ENSO и исключается самой формой вопроса.',
'NWS Neutral определено Neither El Niño nor La Niña; обычно SST near average, но источник допускает ocean/atmosphere mismatch.'
], 'NWS ENSO напрямую подтверждает повышение SST, уменьшение осадков над Индонезией и увеличение в central/eastern tropical Pacific.',[
'NWS La Niña подтверждает cold SST phase и обычное увеличение осадков над Индонезией.',
'NWS El Niño прямо говорит об ослаблении обычных east-to-west surface winds вдоль экватора и иногда обращении к west-to-east; дополнительный факт note подтверждён.',
'CPC NAO определяет североатлантическую изменчивость pressure/height, не тропический Pacific.',
'NWS ENSO описывает третью neutral phase между крайними, neither El Niño nor La Niña. Note не требует обязательной средней SST и потому не противоречит оговорке о рассогласовании океана/атмосферы.'
], 'Medium соответствует знанию климатических фаз; именные подписи согласованы. Но «Какая фаза ENSO» заранее делает NAO чужой категорией. Для четырёх правдоподобных вариантов нужно изменить рамку вопроса, не key.', ['weather-climate-la-nina-cool','weather-climate-nao-pressure','weather-climate-iod-indian'], 'La Niña CURRENT полностью повторяет структуру и SST-связь со сменой warm/cool; это одна сравнительная связь ENSO, а не достаточное разнообразие двух задач. Предлагаю сохранить El Niño как якорь, изменить проверяемый факт только у La Niña. NAO и IOD проверяют другие бассейны/величины.', ['prompt/answers[2]: NAO не фаза ENSO, что видно из формулировки; нарушена однородность дистракторов.'], 'Автор: один цикл — спросить климатический режим/явление вместо фазы ENSO, сохранив факт и ключ; зеркальный факт La Niña исправлять в её карточке. Повторно проверить изменённую формулировку и пару.')
rec('la-nina-cool','FIX',['nws-enso','noaa-nao'],[
'NWS El Niño задаёт warming, а не cooling.',
'NWS La Niña задаёт cooling/below-average SST в central and eastern tropical Pacific: ключ 1.',
'CPC NAO задаёт североатлантический dipole pressure/height, не фазу ENSO; условие автоматически исключает вариант.',
'NWS Neutral — neither El Niño nor La Niña; это третья, не cold phase.'
], 'NWS La Niña прямо подтверждает cold SST и усиление normal easterly winds along equator.',[
'NWS El Niño говорит о повышении SST и rainfall increases over central/eastern tropical Pacific; русское «осадки смещаются» корректно передаёт эту региональную перераспределённость вместе с ослаблением над Индонезией.',
'NWS La Niña прямо подтверждает усиление обычных восточных экваториальных ветров — дополнительный факт правильной note.',
'CPC NAO подтверждает североатлантическое pressure/height изменение; это действительно не ENSO.',
'NWS neutral phase — neither El Niño nor La Niña; промежуточность между крайними состояниями есть в вводном абзаце.'
], 'Русский согласован, уровень medium адекватен факту. NAO не относится к фазам ENSO. Кроме этого, зеркальное определение с El Niño не обеспечивает самостоятельного разнообразия.', ['weather-climate-el-nino-warm','weather-climate-nao-pressure','weather-climate-iod-indian'], 'El Niño/La Niña CURRENT заданы одинаковой конструкцией с противоположной температурной аномалией и почти одинаковым набором. Проверен именно текущий сосед, не прежний авторский пакет.', ['prompt: зеркальный повтор связи фазы ENSO и знака SST-аномалии из el-nino-warm.','prompt/answers[2]: NAO не фаза ENSO, автоматически исключается по категории.'], 'Автор: один адресный цикл — для сохранённого ключа La Niña проверить другой независимый medium-факт из реально прочитанного ENSO-контекста, избегая определения через охлаждение и автоматического исключения NAO по слову «фаза».')
rec('nao-pressure','HOLD',['noaa-nao','nws-enso','live-bom-iod'],[
'NWS El Niño описывает Pacific SST warming, не North Atlantic pressure.',
'CPC NAO задаёт north-south pressure/height dipole Greenland/central North Atlantic и воздействие на jet/storm track. Он не называет Icelandic Low/Azores High; этот точный маркер CURRENT не подтверждён прочитанным источником.',
'NWS La Niña описывает Pacific SST cooling, не North Atlantic pressure.',
'Прочитанный официальный BOM IOD задаёт разность температур поверхности tropical western/eastern Indian Ocean, не Atlantic pressure.'
], 'CPC NAO подтверждает противоположные pressure/height anomalies и jet/storm-track, зимние precipitation и European temperature различия. Исландский минимум/Азорский максимум в этой странице отсутствуют: частичный, не полный source PASS.',[
'NWS ENSO прямо определяет El Niño как warming central/eastern tropical Pacific.',
'CPC NAO прямо связывает обе фазы со storm-track changes и winter precipitation/temperature patterns в Европе; correct note добавляет эффекты к определению pressure dipole.',
'NWS ENSO прямо определяет La Niña как cooling central/eastern tropical Pacific.',
'BOM IOD напрямую определяет sustained changes в разности SST tropical west/east Indian Ocean; note проверена отдельно, не по старому HOLD и не по URL.'
], 'Русские именные подписи согласованы. Название правильного варианта повторяет географическое определение «Северная Атлантика» в prompt, а остальные варианты названы иными океаническими явлениями. Это сильная лексико-географическая подсказка для medium; source HOLD имеет приоритет над FIX.', ['weather-climate-el-nino-warm','weather-climate-la-nina-cool','weather-climate-iod-indian'], 'IOD сосед сравнивает Indian Ocean SST запад/восток; ENSO соседи проверяют Pacific SST; NAO — pressure/height в Atlantic. Разные величины/режимы, самостоятельный факт, но географическая подсказка делает выбор проще.', ['source prompt/explanation: CPC не содержит Icelandic Low/Azores High; climate.gov альтернативное чтение вернуло robot challenge, Met Office официальный альтернативный URL — 404.','prompt: Северная Атлантика прямо подсказывает одноимённый вариант, снижая абсолютную сложность.'], 'HOLD владельцу источников/автору: предоставить сохранённый полный официальный контекст с точным Icelandic Low–Azores High и westerly link либо в одном fix-cycle убрать неподтверждённую конкретизацию в пользу прямо проверенного pressure dipole, одновременно устранить географическую подсказку medium. Повторный поиск по тем же недоступным URL не выполнять.')
rec('jet-stream-fast','PASS',['nws-flight-environment','noaa-jetstream'],[
'Flight Environment связывает northeast trades с tropical circulation cell и направлением к экватору; это приземный пояс, не upper jet.',
'Flight Environment и NOAA Ferrel cell задают prevailing westerlies в midlatitudes; west-to-east само по себе не узкая скоростная струя.',
'Flight Environment THE JET STREAM прямо описывает narrow bands exceedingly high speed в higher atmosphere и west-to-east flow: ключ 2.',
'Flight Environment Polar cell задаёт surface easterlies высоких широт, не upper jet.'
], 'Flight Environment THE JET STREAM подтверждает узкие сильные верхние ветры, запад-восток, близость tropopause и связь polar front; отдельно отличает subtropical jet без фронта.',[
'Flight Environment Hadley/tropic cell и NOAA Hadley cell подтверждают движение к equatorial low; название trade и eastward origin описаны в hemispheric prevailing winds.',
'NOAA Ferrel cell задаёт westerlies между средними широтами, Flight Environment — prevailing westerlies 30–60°; narrow exceedingly high speed band отдельно определяется как jet.',
'Flight Environment THE JET STREAM прямо связывает jet с tropopause/polar front и отличает subtropical jet без фронтов; correct note добавляет положение/фронт к prompt.',
'Flight Environment Polar cell прямо описывает поверхностные easterly winds; NOAA Polar cell задаёт движение от polar high. Note относится к конкретному поясу.'
], 'Средний тематический факт; западные ветры правдоподобно совпадают по направлению, а высота и узкая морфология отличают струю. Четыре именные подписи согласованы, key 2 уникален.', ['weather-climate-trade-winds-tropics','weather-climate-westerlies-midlat','weather-climate-polar-easterlies'], 'Соседи проверяют торговые маршруты, перенос циклонов через Европу и приземный полярный пояс. CURRENT проверяет узкую высокоскоростную верхнюю струю, отдельную по вертикальному положению и структуре.')
entries=[]
for id in manifest['scope']:
 q=qs[id];r=records[id];expected=next(a['afterHash'] for a in manifest['applied'] if a['id']==id)
 assert h(q)==expected
 assert all(q[f]==bqs[id][f] for f in ['id','difficulty','correctIndex'])
 literals=[dict(prompt=q['prompt'],answers=[a['text'] for a in q['answers']],correctIndex=q['correctIndex']),q['explanation']]+[a['note'] for a in q['answers']]
 names=['prompt_ordered_answers_key','explanation','note0','note1','note2','note3']
 reasons=[r['options'],[r['explanation']]]+[[s] for s in r['notes']]
 groups=[]
 for i,(n,l,s) in enumerate(zip(names,literals,reasons)):
  er=r['editorial'] if i==0 else ('Объяснение проверено отдельно: 2 предложения, русский связен, правильный ответ назван.' if i==1 else ('Справка относится к своему варианту, до 35 слов; ' + ('добавляет проверенный факт к prompt/key.' if i-2==q['correctIndex'] else 'фактологически проверена как самостоятельная справка дистрактора.')))
  if r['verdict']=='HOLD' and i==1:er+=' Точное именование двух центров остаётся неподтверждённым.'
  groups.append(dict(group=n,literal=l,literalSHA256=h(l),sourceReasons=s,editorialReason=er))
 locs=[]
 for k in r['keys']:
  if k in index:locs.append(dict(sourceId=k,sourceUrl=index[k]['sourceUrl'],typedLocator=index[k]['typedLocator'],gitCommit=index[k]['gitCommit'],body=index[k]['body'],independentRead=True))
  else:locs.append(dict(sourceId=k,sourceUrl={'live-nws-cyclone':'https://forecast.weather.gov/glossary.php?word=Cyclone','live-nws-theta-e':'https://forecast.weather.gov/glossary.php?word=Theta-e','live-bom-iod':'https://www.bom.gov.au/climate/iod/'}[k],preservedRead=str(root/'sources/supplemental-web-read.json'),independentRead=True,typedLocator={'live-nws-cyclone':'Anticyclone and Cyclone entries','live-nws-theta-e':'Theta-e and Theta-e Ridge entries','live-bom-iod':'Indian Ocean Dipole definition, phases and Monitoring the IOD'}[k]))
 entries.append(dict(id=id,currentHash=h(q),verdict=r['verdict'],frozenContract=dict(idTopicDifficultyKeyPreserved=True,baseline='31aa848b',difficulty=q['difficulty'],correctIndex=q['correctIndex'],correctText=q['answers'][q['correctIndex']]['text'],baselineCorrectText=bqs[id]['answers'][bqs[id]['correctIndex']]['text'],correctLiteralUnchanged=q['answers'][q['correctIndex']]['text']==bqs[id]['answers'][bqs[id]['correctIndex']]['text'],keyMeaningReview='Инверсионный градиент → инверсия температуры: терминологическое переименование того же положительного профиля; отрицательный заряд сокращён без смены факта. Остальные правильные подписи неизменны.' if id in ['weather-climate-inversion-positive','weather-climate-lightning-electric'] else 'Правильная подпись совпадает с baseline.'),fieldGroups=groups,sourceLocators=locs,neighborReview=dict(ids=r['neighbors'],currentHashes={n:h(qs[n]) for n in r['neighbors']},editorialReason=r['neighborReason']),defects=r['defects'],nextAction=r['action']))
result=dict(reviewerThreadId='01a13b89-56e0-7661-a8d3-88b67254735f',baseline='31aa848b',reviewedBranch='codex/question-quality-wave-6',entries=entries,sourceReadNotes={'archivedWorktree':'question-review-process absent; used surviving Git branch and blobs, no restoration or new worktree','inheritance':'Only primaryContextIndex and group payload schema read from old source packet; no prior PASS/editorial conclusions adopted','failedSources':[{'url':'https://www.climate.gov/news-features/understanding-climate/climate-variability-north-atlantic-oscillation','outcome':'JavaScript robot challenge; not source content'},{'url':'https://www.metoffice.gov.uk/weather/learn-about/weather/atmosphere/north-atlantic-oscillation','outcome':'404 official alternative; no further attempts'},{'route':'Python urllib TLS','outcome':'certificate verification failure; stopped route, no insecure TLS bypass. Successful web reading preserved separately.'}]},checks=dict(exactAfterHashes='10/10 match',frozenIdDifficultyKey='10/10 match baseline',fieldGroups='60 exact literals and programmatic hashes',catalogMutation=False,fullQa=False,build=False,runtime=False))
(root/'review.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
(root/'pass-current.json').write_text(json.dumps(dict(reviewerThreadId=result['reviewerThreadId'],entries=[dict(id=e['id'],currentHash=e['currentHash']) for e in entries if e['verdict']=='PASS']),ensure_ascii=False,indent=2)+'\n')
(root/'fix-requests.json').write_text(json.dumps([dict(id=e['id'],currentHash=e['currentHash'],verdict=e['verdict'],defects=e['defects'],nextAction=e['nextAction']) for e in entries if e['verdict']!='PASS'],ensure_ascii=False,indent=2)+'\n')
print({v:sum(e['verdict']==v for e in entries) for v in ['PASS','FIX','HOLD']})
