import json,hashlib,copy
from pathlib import Path
root=Path('/tmp/mindbattle-source-01a137d4-70e3-74f0-bbe4-0d13e5dca25f/weather30-49')
old_path=root/'weather30-49-source-editorial-packet.json'
old=json.loads(old_path.read_bytes()); cards=json.loads((root/'weather-climate-current-after-good7.json').read_bytes())['questions']
cores={
30:'Дистракторы молния, гром и радуга относятся к разным процессам: электрическому разряду, его звуковому следствию и оптике капель. Для уникальности проверь, что механизм заряженных частиц не подменён широкой ассоциацией «атмосферное явление».',
31:'Вопрос уже говорит о слабом местном ветре между морем и сушей, а ключ и объяснение повторяют морской бриз и дневное направление. Раздели береговой дневной и ночной бризы либо не дублируй подсказку в пояснении.',
32:'Региональный термин «ураган» требует согласованного географического охвата и порога устойчивого ветра. Вопрос говорит об Атлантике, тогда как ответ также включает восточную часть Тихого океана.',
33:'«Вихрь, опускающийся из грозы к земле» может ошибочно сделать видимую воронку обязательной частью определения. Проверь разграничение вращающегося столба воздуха, облака-источника и контакта с поверхностью.',
34:'Муссон нельзя сводить только к азиатским летним дождям: определение в варианте опирается на сезонную смену направления. Условие вопроса может проверять климатический эффект вместо режима ветров.',
35:'Текущий NWS glossary описывает ложбину как вытянутую область низкого давления, обычно не связанную с замкнутой циркуляцией, что отличает её от замкнутого минимума. Вопросу полезно явно обозначить это отличие от циклона.',
36:'NWS определяет гребень как вытянутую область относительно высокого давления и противоположность ложбины. Текущая метафора «выступ области» менее точна, фраза об ослаблении облачности источником не подтверждена. Ключевой слот совпадает с #35, что может подсказать парный ответ.',
37:'ENSO не раскрыт при первом появлении; точная область потепления и телесвязи должны совпадать с источником. NOAA capture обрезан после 8192 из 144357 байт и не содержит пригодного тела статьи.',
38:'Ла-Нинья названа противоположной фазой Эль-Ниньо, а пояснение добавляет усиление пассатов. Сохранённая NOAA страница вернула 404, поэтому температурную область и направление изменения ветров нельзя считать проверенными.',
39:'«Режим особенно влияет» не задаёт наблюдаемый признак САК. Ответная заметка определяет разность давления Азорского максимума и Исландского минимума, а объяснение добавляет изменения западных ветров; сформулируй проверяемый аспект.',
40:'Сравнение у Африки и Индонезии следует привязать к западной/восточной части тропического Индийского океана. Не смешивай определение диполя с любым контрастом температуры между побережьями.',
41:'«Направляет циклоны» звучит как прямое управление траекториями. Различай узкую сильную струю верхней тропосферы и приземный пояс западных ветров, а причинность формулируй соразмерно источнику.',
42:'Фраза о постоянных маршрутах парусных торговых судов лексически подсказывает «торговые ветры». Заменить историческую подсказку на определяющие широту и направление ветров после получения пригодного первичного источника.',
43:'Формулировка «несут многие циклоны через Европу» слишком широко связывает циклоны с зональным ветром. Раздели среднеширотный пояс ветров и верхнетропосферную струю из #41.',
44:'Поясни направление полярных восточных ветров отдельно от их происхождения в высоком давлении; эти свойства сейчас соединены одним утверждением, но требуют независимой опоры.',
45:'«Конвективное торможение»/«крышка» смешивает официальный параметр и разговорный образ. SPC подтверждает CINH как интеграл отрицательной площади до LFC и энергию, требуемую для достижения LFC, но не алиас «крышка».',
46:'SPC даёт точную формулу LI на 500 mb: температура поднятой частицы минус температура среды; отрицательные значения означают более тёплую/плавучую частицу. Сохрани уровень и знак в одном ясном определении.',
47:'Уточни термин до storm-relative helicity (SRH): SPC связывает его с streamwise vorticity во входящем в шторм слое и площадью между hodograph и движением шторма. Просто «спиральность» двусмысленна.',
48:'NWS PDF отделяет collision-coalescence в тёплых облаках от Bergeron в холодных. Текущая карточка проверяет базовый терминологический recall, хотя класс Hard заморожен; объяснение лучше сказать, что именно происходит со столкнувшимися каплями.',
49:'NWS PDF поддерживает рост ледяных кристаллов за счёт облачных капель в присутствии переохлаждённой воды и более низкое давление пара над льдом. Он не доказывает безусловный порог «ниже 0 °C» для всякого смешанного облака. Wikipedia не используется.'}
# Primary evidence read summaries and field-level coverage.
reads={
35:'NWS glossary exact entry: trough = elongated relatively low-pressure area, usually without a closed circulation, distinguishing from closed low; opposite of ridge. Does not support the added cloud/precipitation claim.',
36:'NWS glossary exact entry: ridge = elongated area of relatively high atmospheric pressure; opposite of trough. Does not support the added reduced-cloudiness claim; Wikipedia capture is not used as factual authority.',
37:'Exact NOAA capture is incomplete: HTTP 200 but response body 8192 bytes versus Content-Length 144357. The page head identifies ENSO broadly; it does not include the relevant text defining the warm phase/region.',
38:'Exact NOAA URL returned HTTP 404 and a not-found body; that response cannot support the La Niña definition.',
45:'Full SPC linked child parcelvals.html: CINH is integrated negative area from original parcel level to LFC; that area is energy needed to reach LFC. The child does not use colloquial alias “cap”.',
46:'Full SPC linked child parcelvals.html: LI = lifted parcel temperature at 500 mb minus sounding temperature at 500 mb; negative values mean warmer than background and thus buoyant/unstable.',
47:'Full SPC linked child shear.html: SRH represents streamwise vorticity within the storm inflow layer, is proportional to area swept between hodograph and storm motion, and has diagnostic utility for tornadic vs non-tornadic supercells.',
48:'Full 5-page NWS PDF, visually checked: page 3 says collision-coalescence forms precipitation in warm clouds; larger drops collide with smaller droplets, some coalesce; page 2 contrasts Bergeron as cold-cloud mechanism.',
49:'Same full NWS PDF, page 2: Bergeron is a cold-cloud mechanism; ice crystals grow in presence of supercooled liquid water at expense of cloud droplets; saturation vapor pressure over ice is lower than over liquid water.'}
# Raw file list is intentionally limited to evidence actually read.
base=Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle/docs/content-audits/question-quality-wave-7')
source_files=[
('coordinator-continuation-01a13619/capture-only/weather-next10-gaps/trough.body','https://forecast.weather.gov/glossary.php?word=Trough'),
('coordinator-continuation-01a13619/capture-only/weather-next10-gaps/ridge.body','https://forecast.weather.gov/glossary.php?word=Ridge'),
('coordinator-continuation-01a136e6/capture-only/weather20-29-primary/spc-parcel-values.body','https://www.spc.noaa.gov/exper/soundings/help/parcelvals.html'),
('coordinator-continuation-01a136e6/capture-only/weather20-29-primary/spc-help-left.body','https://www.spc.noaa.gov/exper/soundings/help/leftside.html'),
('coordinator-continuation-01a136e6/capture-only/weather20-29-primary/spc-help-right.body','https://www.spc.noaa.gov/exper/soundings/help/rightside.html'),
('coordinator-continuation-01a13772/terminal-second-compaction/capture-helper3a/owned-tmp/spc-children/shear/response.body','https://www.spc.noaa.gov/exper/soundings/help/shear.html'),
('coordinator-continuation-01a13772/terminal-second-compaction/capture-helper3a/owned-tmp/spc-children/shear/response.headers','https://www.spc.noaa.gov/exper/soundings/help/shear.html'),
('coordinator-continuation-01a13772/terminal-second-compaction/capture-helper3a/owned-tmp/spc-children/shear/manifest.json','https://www.spc.noaa.gov/exper/soundings/help/shear.html'),
('coordinator-continuation-01a13772/terminal-second-compaction/capture-helper3a/owned-tmp/17/response.body','https://www.weather.gov/media/zhu/ZHU_Training_Page/clouds/cloud_precipitation/cloud_precipitation.pdf'),
('coordinator-continuation-01a13772/terminal-second-compaction/capture-helper3a/owned-tmp/17/response.headers','https://www.weather.gov/media/zhu/ZHU_Training_Page/clouds/cloud_precipitation/cloud_precipitation.pdf'),
]
receipts=[]
for rel,url in source_files:
 p=base/rel;b=p.read_bytes();receipts.append({'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'url':url})
# capture-index is provenance for raw attempts, not evidence. Include all weather capture records only.
capbase=base/'coordinator-continuation-01a13772/terminal-second-compaction/capture-helper3a/owned-tmp'
idx=json.loads((capbase/'capture-index.json').read_bytes())
cap_recs=[]
for j,e in enumerate(idx[:18],1):cap_recs.append({'captureId':j,'requestedURL':e['requestedURL'],'status':e['httpStatus'],'bodyBytes':e['bodyBytes'],'bodySHA256':e['bodySHA256'],'headerBytes':e['headerBytes'],'headersSHA256':e['headersSHA256']})

def text_sha(v,sort=False):return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=sort,separators=(',',':')).encode()).hexdigest()
new=[]
for i in range(30,50):
 c=copy.deepcopy(cards[i]);proposal=copy.deepcopy(c)
 if i==35:
  proposal['explanation']='Ложбина — вытянутая область относительно низкого атмосферного давления, обычно без замкнутой циркуляции; этим она отличается от замкнутого минимума.'
  proposal['source']={'title':'National Weather Service Glossary: Trough','url':'https://forecast.weather.gov/glossary.php?word=Trough','verifiedAt':'2026-10-14'}
 if i==36:
  proposal['prompt']='Как называется вытянутая область относительно высокого атмосферного давления, противоположная ложбине?'
  proposal['explanation']='Гребень — вытянутая область относительно высокого атмосферного давления, противоположная ложбине.'
  proposal['source']={'title':'National Weather Service Glossary: Ridge','url':'https://forecast.weather.gov/glossary.php?word=Ridge','verifiedAt':'2026-10-14'}
 if i==45:
  proposal['prompt']='Какой параметр выражает энергию, необходимую воздушной частице, чтобы достичь уровня свободной конвекции?'
  proposal['explanation']='CIN — интегральная отрицательная область от начального уровня частицы до LFC; её величина соответствует энергии, необходимой для достижения LFC.'
  proposal['source']={'title':'Storm Prediction Center: Sounding Analysis Help — Parcel Values','url':'https://www.spc.noaa.gov/exper/soundings/help/parcelvals.html','verifiedAt':'2026-10-14'}
 if i==46:
  proposal['prompt']='Какой индекс становится более отрицательным, когда поднятая частица на 500 mb теплее окружающей среды?'
  proposal['explanation']='LI — температура поднятой частицы минус температура среды на 500 mb. Отрицательный LI означает, что частица теплее среды и плавуча/неустойчива.'
  proposal['source']={'title':'Storm Prediction Center: Sounding Analysis Help — Parcel Values','url':'https://www.spc.noaa.gov/exper/soundings/help/parcelvals.html','verifiedAt':'2026-10-14'}
 if i==47:
  proposal['answers'][1]['text']='Штормовая относительная спиральность (SRH)'
  proposal['answers'][1]['note']='SRH характеризует streamwise vorticity во входящем в шторм слое и зависит от площади между hodograph и движением шторма.'
  proposal['explanation']='SRH характеризует streamwise vorticity во входящем в шторм слое. SPC связывает показатель с площадью между hodograph и движением шторма и отмечает его диагностическую пользу для различения торнадических и неторнадических суперячеек.'
  proposal['source']={'title':'Storm Prediction Center: Wind Shear — Storm Relative Helicity','url':'https://www.spc.noaa.gov/exper/soundings/help/shear.html','verifiedAt':'2026-10-14'}
 if i==48:
  proposal['answers'][2]['note']='В тёплых облаках крупные капли сталкиваются с более мелкими; часть мелких капель слипается с крупными.'
  proposal['explanation']='В тёплых облаках более крупные капли падают и сталкиваются с мелкими; часть мелких капель слипается с ними, поэтому капли растут.'
 if i==49:
  proposal['answers'][3]['note']='В холодном облаке ледяные кристаллы растут при наличии переохлаждённой жидкой воды; давление насыщенного пара над льдом ниже, чем над водой.'
  proposal['explanation']='В холодном облаке ледяные кристаллы растут за счёт облачных капель при наличии переохлаждённой жидкой воды. Давление насыщенного пара над льдом ниже, чем над водой.'
  proposal['source']={'title':'NOAA/NWS: Clouds and Precipitation, Lesson 10','url':'https://www.weather.gov/media/zhu/ZHU_Training_Page/clouds/cloud_precipitation/cloud_precipitation.pdf','verifiedAt':'2026-10-14'}
 combined={'prompt':c['prompt'],'answers':[a['text'] for a in c['answers']],'correctIndex':c['correctIndex']}
 vals=[('prompt_ordered_answers_key',combined),('explanation',c['explanation'])]+[(f'note{j}',c['answers'][j]['note']) for j in range(4)]+[('difficulty',c['difficulty']),('source_metadata',c['source'])]
 groups=[]
 for g,val in vals:
  supported=False; ev=reads.get(i)
  if i in (35,36) and g in ('prompt_ordered_answers_key','explanation','note0','note3','source_metadata'):supported=True
  if i in (45,46) and g in ('prompt_ordered_answers_key','explanation','note0','note1','note2','note3','source_metadata'):supported=True
  if i==47 and g in ('prompt_ordered_answers_key','explanation','note0','note1','note2','note3','source_metadata'):supported=True
  if i==48 and g in ('prompt_ordered_answers_key','explanation','note0','note2','source_metadata'):supported=True
  if i==49 and g in ('prompt_ordered_answers_key','explanation','note0','note3','source_metadata'):supported=True
  if g=='difficulty': status='EDITORIAL_ONLY_FROZEN_CLASS'
  elif supported: status='PRIMARY_PASSAGE_READ_WITH_BOUNDS'
  elif i in (35,36,45,46,47,48,49): status='UNSUPPORTED_DETAIL_NEEDS_SOURCE_OR_REMOVAL'
  elif i==37: status='PARTIAL_CAPTURE_NO_ARTICLE_PASSAGE'
  elif i==38: status='CAPTURE_404_NO_FACT_EVIDENCE'
  else: status='CAPTURE_403_NO_FACT_EVIDENCE'
  if g=='difficulty': sreason='Difficulty is a pedagogical classification, not a factual proposition that these meteorological sources can certify; preserve the frozen class and route any taxonomy change separately.'
  else:
   claim=(val if isinstance(val,str) else json.dumps(val,ensure_ascii=False,sort_keys=True,separators=(',',':')))
   if supported:
    sreason=ev
    if i in (35,36): sreason += ' Coverage is limited to the definition; any unrelated distractor claims and cloudiness/precipitation effects are not established by that entry.'
    if i in (45,46): sreason += ' The captured root URL is a frameset; the direct linked `parcelvals.html` child is the full evidence page.'
    if i==47:sreason += ' Restrict the evidence to SRH; it does not define helicity generally.'
    if i in (48,49): sreason += ' NWS PDF page 2/3 was read in full and visually inspected; other distractor definitions remain outside its scope.'
   else:
    why=reads.get(i,'No complete readable primary source passage supports this specific literal in the captured set.')
    sreason=f'This exact literal is {claim!r}. {why} Keep the claim unqualified or remove/replace it only after the listed fact is supported by a complete official passage.'
  # Unique substantive editorial interpretation for each grouped literal.
  if g=='prompt_ordered_answers_key': er=f'{cores[i]} Apply it to the whole stem/options/key as a single item: ensure one defensible answer and retain frozen key index {c["correctIndex"]}.'
  elif g=='explanation': er=f'{cores[i]} For this explanation, separate a definition from added causation/geography; add a meaningful distinction rather than echoing the keyed term.'
  elif g.startswith('note'):
   j=int(g[-1]);er=f'{cores[i]} For answer-note {j}, literal {val!r}: explain the misconception that makes this option wrong or the diagnostic feature that makes it right; avoid circular restatement.'
  elif g=='difficulty':er=f'{cores[i]} Keep {c["difficulty"]} unchanged; note any mismatch between the concept-recall operation and the frozen band for a later taxonomy review.'
  else:er=f'{cores[i]} For source metadata, identify the exact complete supporting page rather than the original publisher label alone; do not treat retrieval date as content verification.'
  refs=[]
  if i==35 and supported:refs=['NWS-Trough-entry']
  if i==36 and supported:refs=['NWS-Ridge-entry']
  if i in (45,46) and supported:refs=['SPC-parcelvals-html']
  if i==47 and supported:refs=['SPC-shear-html']
  if i in (48,49) and supported:refs=['NWS-PDF-pages-2-3']
  if i==37:refs=['capture#08-partial-8192/144357']
  if i==38:refs=['capture#09-HTTP404']
  if 30<=i<=44 and i not in (36,37,38):refs=[f'capture#{i-29:02}-HTTP403']
  groups.append({'group':g,'literal':val,'literalSHA256':text_sha(val,sort=g=='source_metadata'),'source':{'status':status,'reason':sreason,'evidenceRefs':refs},'editorial':{'status':'ITEM_SPECIFIC_REVIEW','reason':er}})
 assert proposal['difficulty']==c['difficulty'] and proposal['correctIndex']==c['correctIndex']
 new.append({'index':i,'id':c['id'],'frozenClass':c['difficulty'],'frozenCorrectIndex':c['correctIndex'],'currentPreimageSHA256':text_sha(c,True),'currentCard':c,'proposedCard':proposal,'groups':groups,'qualityCredit':0,'sourceResolution':{'35':'PARTIAL_PRIMARY','36':'PARTIAL_PRIMARY_SOURCE_METADATA_REPLACEMENT','37':'TRUNCATED_CAPTURE','38':'404','45':'PRIMARY_CHILD_PAGE','46':'PRIMARY_CHILD_PAGE','47':'PRIMARY_CHILD_PAGE','48':'PRIMARY_EXACT_PDF','49':'PRIMARY_PDF_REPLACES_WIKIPEDIA'}.get(str(i),'BLOCKED_CAPTURE_NEEDS_OFFICIAL_ALTERNATE')})
packet={'schema':'mindbattle-weather30-49-source-editorial-packet-v2','authorNativeThreadId':'01a137d4-70e3-74f0-bbe4-0d13e5dca25f','supersedes':str(old_path),'supersedesSHA256':hashlib.sha256(old_path.read_bytes()).hexdigest(),'scopeTupleSHA256':'66a9cde4368a052113af4a01e9d2f9b8cf16835c61082014d7b962107e1720b5','currentTopicRAW':'b3b48f84d6334f168c0a8a9f800c683dcab2142c4aa2b356b2f3a532ac26fd39','countAsOf':558,'remainingAsOf':1442,'scopeTotal':2000,'qualityCredit':0,'scopeBoundary':'Only Weather indices 30–49. Current originals preserved; proposal cards are not applied to shared files. Frozen IDs, classes, correct indices remain unchanged.','evidencePolicy':'HTTP errors, truncated responses, frameset landing pages and unsupported neighbor context are capture evidence only, not fact evidence. Claims count only when a complete relevant source passage was personally read.','entries':new,'currentNeighborSnapshot':old['currentNeighborSnapshot'],'readSourceReceipts':receipts,'weatherCaptureAttemptIndex':cap_recs,'captureSourceStatus':'The inspected capture-index has #1–18 Weather attempts; no official alternative batch was present in it at author time. Britannica attempts are HTTP403, NOAA La Niña HTTP404, NOAA El Niño body truncated. Need coordinator-provided alternative capture bindings for #30–34 and #37–44 before qualification.'}
out=json.dumps(packet,ensure_ascii=False,separators=(',',':')).encode();dest=root/'weather30-49-source-editorial-packet-v2.json';dest.write_bytes(out)
print(json.dumps({'path':str(dest),'bytes':len(out),'sha256':hashlib.sha256(out).hexdigest(),'entries':len(new),'groups':sum(len(e['groups']) for e in new),'reasons':sum(2*len(e['groups']) for e in new),'neighbors':len(packet['currentNeighborSnapshot']),'readSources':len(receipts),'captures':len(cap_recs),'qualityCredit':0},indent=2))
