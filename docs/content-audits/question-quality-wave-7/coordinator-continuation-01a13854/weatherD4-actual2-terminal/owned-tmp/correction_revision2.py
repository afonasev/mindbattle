import json,hashlib
from pathlib import Path
TMP=Path('/tmp/mindbattle-source-01a137d4-70e3-74f0-bbe4-0d13e5dca25f');base=TMP/'author-correction.json';out=TMP/'author-correction-2.json';d=json.loads(base.read_bytes())
d['previousCorrection']={'path':str(base),'bytes':base.stat().st_size,'sha256':hashlib.sha256(base.read_bytes()).hexdigest(),'preserveImmutable':True}
# Prompt and content corrections based on coordinator review.
for c in d['cards']:
 i=c['index'];x=c['proposedCard']
 if i==21:
  x['prompt']='Порция начинает подъём на 2 °C теплее среды. До уровня конденсации при подъёме (LCL) на высоте 1 км среда охлаждается на 6 °C/км, ненасыщенная порция — на 9,8 °C/км; выше LCL значения равны 7 и 5 °C/км соответственно. На каких высотах температуры порции и среды сравняются?'
 if i==22:
  x['prompt']='Порции начинают на 0,5 °C теплее среды и проходят три слоя по 0,5 км. Среда охлаждается на 4, 7 и 10,5 °C/км; ненасыщенная порция — на 9,8 °C/км, насыщенная — на 5 °C/км весь путь. Каковы их температуры относительно среды на вершине?'
  texts=['Ненасыщенная холоднее на 3,45 °C, насыщенная тоже холоднее на 3,75 °C','Ненасыщенная холоднее на 3,45 °C, насыщенная теплее на 3,75 °C','Ненасыщенная теплее на 3,45 °C, насыщенная теплее на 3,75 °C','Ненасыщенная теплее на 3,75 °C, насыщенная холоднее на 3,45 °C']
  for a,t in zip(x['answers'],texts):a['text']=t
  x['explanation']='В трёх слоях среда охлаждается суммарно на 10,75 °C; сухая порция — на 14,7 °C, насыщенная — на 7,5 °C. С учётом начального избытка +0,5 °C на вершине сухая порция холоднее среды на 3,45 °C, а насыщенная теплее на 3,75 °C. По слоям сравнение проходит от среды медленнее обоих градиентов к промежуточному режиму и затем к среде быстрее обоих.'
  notes=[
   'В среднем и верхнем слоях насыщенная порция охлаждается медленнее среды, поэтому к вершине она теплее, а не холоднее неё.',
   'В среднем слое скорость охлаждения среды 7 °C/км находится между влажным и сухим градиентами: насыщенная порция выигрывает, ненасыщенная теряет тепло относительно среды.',
   'За весь путь сухая порция остывает на 14,7 °C, что на 3,95 °C больше охлаждения среды; исходные +0,5 °C оставляют дефицит 3,45 °C.',
   'На вершине сухая порция холоднее на 3,45 °C, а насыщенная теплее на 3,75 °C; предложенные здесь знаки и величины не совпадают с итогом.'
  ]
  for a,n in zip(x['answers'],notes):a['note']=n
 if i==23:
  x['prompt']='Профили A/B: барьер подъёма — 180/260 Дж/кг, положительная энергия выше него — 2 200/4 000 Дж/кг. Порция подходит с 40 Дж/кг кинетической энергии и получает 210 Дж/кг работы. Без потерь остаток после барьера и верхняя энергия переходят в кинетическую. Кто достигает уровня равновесия и с какой энергией?'
  texts=['Достигают оба: A — 2 270, B — 3 990 Дж/кг; положительная энергия доступна в каждом профиле.','Достигает только B: 3 990 Дж/кг; больший запас энергии позволяет пройти его барьер.','Достигает только A: 2 270 Дж/кг; для B не хватает 10 Дж/кг до барьера.','Не достигает ни один: 250 Дж/кг начальной энергии и работы меньше обоих барьеров.']
  for a,t in zip(x['answers'],texts):a['text']=t
  x['explanation']='Порция располагает 40+210=250 Дж/кг до прохождения барьера. В A барьер 180 оставляет 70 Дж/кг, затем 2 200 Дж/кг положительной энергии дают 2 270 Дж/кг у уровня равновесия. В B порции не хватает 10 Дж/кг до барьера, поэтому верхняя энергия 4 000 Дж/кг ей недоступна.'
  notes=[
   'В профиле B до барьера имеется 250 Дж/кг, а требуется 260; положительная энергия над барьером не помогает, пока он не пройден.',
   'Размер положительной энергии не определяет, удастся ли начать подъём: сначала суммарные 250 Дж/кг надо сравнить с барьером профиля B.',
   'Инверсионный колпак представляет сравнительно тёплый слой выше приземного воздуха, который подавляет или задерживает развитие грозы.',
   'В профиле A начальная энергия вместе с работой равна 250 Дж/кг и превосходит барьер 180; поэтому вариант «ни один» неверен.'
  ]
  for a,n in zip(x['answers'],notes):a['note']=n
 if i==24:
  x['prompt']='Зондирование: ускорение вверх 0,8 м/с² на 0–500 м и 0,45 м/с² на 500–1500 м; выше уровня равновесия (EL) ускорение отрицательно. Доступную потенциальную энергию конвекции (CAPE) считайте суммой a×h, скорость — √(2×CAPE). Каковы скорость и максимальный уровень подъёма (MPL)?'
  texts=['35,4 м/с; максимум на MPL, который может быть выше EL из-за набранного импульса.','30,0 м/с; максимум на EL, поскольку выше него ускорение становится отрицательным.','49,0 м/с; максимум на EL, поскольку он завершает слой положительной плавучести.','41,2 м/с; максимум на MPL, который может быть выше EL после накопления импульса.']
  for a,t in zip(x['answers'],texts):a['text']=t
  x['explanation']='Положительная работа на нижнем участке равна 0,8×500=400 Дж/кг, на верхнем — 0,45×1 000=450 Дж/кг; CAPE составляет 850 Дж/кг. Тогда √(2×850)≈41,2 м/с. EL завершает область положительной плавучести, но максимум подъёма по теории воздушной частицы может оказаться выше из-за набранного импульса.'
  notes=[
   'Во втором слое задана высота 1 000 м, поэтому его вклад равен 450, а не 225 Дж/кг; оба участка дают CAPE 850.',
   'Первый участок также вносит 400 Дж/кг в CAPE; отрицательное ускорение выше EL не означает, что максимум обязан совпасть с EL.',
   'Нельзя продолжать ускорение 0,8 м/с² на всём пути: на верхнем участке оно равно только 0,45 м/с², а порция может продолжить подъём по инерции выше EL.',
   'Зондирование даёт идеализированную оценку: вовлечение окружающего воздуха и водная нагрузка могут уменьшать фактическую скорость восходящего потока.'
  ]
  for a,n in zip(x['answers'],notes):a['note']=n
 if i==27:
  # Keep frozen correctIndex=1; rewrite distractor notes to match their actual variant text.
  notes=[
   'Разряд внутри облака ограничен облачной областью; термин «облако—земля» описывает канал, достигающий поверхности.',
   'Положительные разряды в целом встречаются реже, хотя в некоторых сильных грозах их доля выше.',
   'Типичный разряд облако—земля может включать несколько последовательных ударов; каждый включает лидер и обратный стример.',
   'Национальная метеорологическая служба США противопоставляет положительный разряд более частому отрицательному, поэтому частоты не одинаковы.'
  ]
  for a,n in zip(x['answers'],notes):a['note']=n
# Short-form/reason requalification for every changed literal and every affected answer note.
reason_updates={
21:{'prompt+orderedAnswers+key':'Короткий стем сохраняет начальную разность, высоту LCL и оба набора градиентов; четыре высоты проверяют два корня и ошибки границы.','explanation':'До LCL возникает первый корень при 0,53 км; значение −1,8 °C на границе даёт второй при 1,90 км.','note0':'SPC сообщает, что при вынужденном подъёме высота уровня конденсации соответствует основанию облака.','class':'Два корня лежат по разные стороны LCL и требуют переносить знаковую разность через смену режима, поэтому frozen Hard остаётся оправдан.','source':'NWS adiabatic glossary и полный SPC parcel-values контекст подтверждают сухой/влажный градиенты, LCL и облачное основание.'},
22:{'prompt+orderedAnswers+key':'Три слоя проводят профиль среды через области, где она охлаждается медленнее обоих parcel rates, между ними и быстрее обоих; варианты параллельно дают две итоговые разности.','explanation':'Нужно сложить охлаждение среды по трём сегментам, отдельно проследить два parcel paths и сохранить исходный запас +0,5 °C.','note0':'Средний/верхний сегменты дают насыщенной порции преимущество над средой, поэтому отрицательный итог для неё невозможен.','note1':'В среднем слое окружающая скорость попадает между сухим и влажным градиентами, отчего знаки отклонения двух порций различаются.','note2':'Суммарное охлаждение сухой порции превосходит средовое на 3,95 °C; начальный избыток уменьшает конечный дефицит до 3,45 °C.','note3':'Фактические конечные знаки противоположны и конкретные остатки равны −3,45 и +3,75 °C.','class':'Hard поддерживается тремя последовательными stability regimes и двумя интегрируемыми parcel trajectories, а не одним средним градиентом или сравнением пары чисел.','source':'NWS environmental-lapse, stability и adiabatic sources задают наблюдаемую среду, нейтральность и parcel rates; сегменты профиля даны в стеме.'},
23:{'prompt+orderedAnswers+key':'Два профиля имеют разные барьеры и положительные области при общей входной кинетике и работе; правильный ответ требует сначала ветвить доступ к уровню свободной конвекции.','explanation':'В A порция проходит барьер и может добавить положительную энергию; в B барьер выше всей входной энергии, поэтому большая верхняя область недоступна.','note0':'Профиль B остаётся ниже порога: 40+210=250, что меньше его барьера 260 Дж/кг.','note1':'CAPE в профиле B не помогает до прохождения нижнего барьера; поэтому общий размер верхней области не выбирает исход.','note2':'NWS определяет инверсионный колпак как сравнительно тёплый слой aloft, задерживающий/подавляющий грозовое развитие.','note3':'Профиль A получает 70 Дж/кг после барьера и затем добавляет CAPE; следовательно, ни один не является верным исходом.','class':'Hard оправдан условным переходом: сначала проверяется доступность LFC отдельно для A/B, затем только достижимая положительная область включается в энергетический итог.','source':'SPC задаёт смысл CINH/CAPE как нижнего барьера и верхней положительной области; NWS capping inversion glossary подтверждает физическую роль барьера.'},
24:{'prompt+orderedAnswers+key':'Вместо готового CAPE заданы два участка ускорения и высоты; требуется проинтегрировать оба, извлечь корень из удвоенной суммы и определить maximum parcel level.','explanation':'Отдельные вклады 400 и 450 Дж/кг сначала дают CAPE 850; только после суммы вычисляется скорость 41,2 м/с.','note0':'При нижнем ускорении 0,8 вклад равен 400; в верхнем сегменте следует использовать всю тысячу метров и получить 450.','note1':'Расчёт требует обоих слоёв; источник также различает конец положительной области EL и максимальный уровень подъёма.','note2':'Экстраполяция 0,8 на верхний слой завышает площадь; после EL parcel theory допускает дальнейшее движение по импульсу.','class':'Hard теперь требует интегрировать профиль, применить нелинейный квадратный корень и отделить EL от предельного уровня MPL.','source':'SPC directly supports integrated CAPE, square-root speed, EL as positive-area top, and momentum-limited MPL; all numeric segments are explicit in the prompt.'},
27:{'note0':'The NWS lightning glossary distinguishes in-cloud channels from cloud-to-ground discharges that reach the surface, contradicting the “no ground” reading.','note2':'A typical cloud-to-ground flash is a composite of sequential strokes, each initiated by a leader and terminated by a return streamer; that describes stroke structure, not equal occurrence of both polarities.','note3':'The source explicitly contrasts the more common negative charge with positive CG, so equal polarity frequency is inaccurate.','class':'Easy remains a direct sign inference from a source-stated frequency contrast; the key sign itself is absent from the stem.','source':'Full NWS lightning glossary supplies the positive/negative frequency contrast, charge-to-ground definition, in-cloud entry and composite-stroke context.'}}
for c in d['cards']:
 u=reason_updates.get(c['index']);
 if not u:continue
 for group,val in u.items():
  if group in c['ownSourceEditorialReasons']:c['ownSourceEditorialReasons'][group]=[val]
  elif group in ('class','source'):c['difficultyAndMetadataSourceEditorialReasons'][group]=[val]
# All reasons are unique and directly support this packet's current text.
# Update review counters and content lengths; qualification remains exclusively coordinator-owned.
d['authorPreflight'].update({'allModifiedPromptsWithin320Chars':True,'hard22ThreeRegimeIntegratedTrajectories':True,'hard23ConditionalBarrierBranch':True,'hard24IntegratedProfileThenNonlinearSpeedAndMPL':True,'variantNoteIndexesManuallyRechecked22And27':True,'qualificationAndAcceptance':'NOT_CLAIMED'})
d['additiveCorrectionFromAuthor']=d['additiveCorrectionFromAuthor']+' Additive edition two keeps previous 5eb packet intact; #22 uses three stability regimes, #23 branches on whether each profile clears its own barrier, #24 derives CAPE from two acceleration-height segments before speed/MPL interpretation. #21–24 stems meet the 320-character limit. #22/#27 answer-index note bindings were manually corrected.'
# Recompute all group/full card/class/metadata hashes with prescribed literal recipes.
compact=lambda o,sort=False:json.dumps(o,ensure_ascii=False,sort_keys=sort,separators=(',',':')).encode('utf-8')
for c in d['cards']:
 x=c['proposedCard'];k=c['frozenCorrectIndex'];assert x['correctIndex']==k and x['difficulty']==c['frozenClass'] and x['id']==c['id']
 lit={'prompt':x['prompt'],'orderedAnswerTexts':[a['text'] for a in x['answers']],'correctIndex':k,'correctAnswerText':x['answers'][k]['text']};c['literalGroupRecipes']['promptAnswersKey']['literal']=lit
 c['proposedCardCanonicalSHA256']=hashlib.sha256(compact(x,True)).hexdigest();c['sixGroupSHA256']={'promptAnswersKey':hashlib.sha256(compact(lit)).hexdigest(),'explanation':hashlib.sha256(x['explanation'].encode()).hexdigest(),**{'note'+str(j):hashlib.sha256(a['note'].encode()).hexdigest() for j,a in enumerate(x['answers'])}};c['classSHA256']=hashlib.sha256(compact(x['difficulty'])).hexdigest();c['metadataSHA256']=hashlib.sha256(compact(x['source'],True)).hexdigest()
# Text length receipt for whole altered stem group.
d['promptCharacterCounts']={str(c['index']):len(c['proposedCard']['prompt']) for c in d['cards']}
assert all(len(d['cards'][i-20]['proposedCard']['prompt'])<=320 for i in range(21,25))
assert [c['frozenCorrectIndex'] for c in d['cards']]==[0,0,1,2,3,0,0,1,1,1]
out.write_bytes(compact(d)+b'\n')
print('bytes',len(out.read_bytes()),'sha256',hashlib.sha256(out.read_bytes()).hexdigest())
print('prompt chars',d['promptCharacterCounts'])
for i in (22,23,24,27):
 c=d['cards'][i-20]; print(i,'choices', [len(a['text']) for a in c['proposedCard']['answers']],'key',c['proposedCard']['answers'][c['frozenCorrectIndex']]['text'])
