import json,hashlib,os
from pathlib import Path
root=Path('/tmp/mindbattle-source-01a137d4-70e3-74f0-bbe4-0d13e5dca25f/weather30-49')
scope=json.load(open('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle/docs/content-audits/question-quality-wave-7/coordinator-continuation-01a13772/weather-climate-next30-49-source-scope.json'))
source=json.load(open(root/'weather-climate-current-after-good7.json'))['questions']
byid={q['id']:q for q in source}
# Full six-field current card and class/metadata partitions are independently bound by hashes.
def canon(x,sort=False): return json.dumps(x,ensure_ascii=False,separators=(',',':'),sort_keys=sort).encode()
def sha(b): return hashlib.sha256(b).hexdigest()
# source-gaps reflect the independent exact-URL manifest audit and read receipts.
exact_missing=set(range(30,45))|{48,49}
thin={45,46,47}
# IDs plus concrete similarity anchors from the full current neighbor snapshot.
clusters={30:[27,28,29],31:[34,41,42,43,44],32:[64,65,66,96,97,98,99],33:[18,32,47,76],34:[31,41,42,43,44],35:[18,36],36:[19,35],37:[38],38:[37],39:[37,38],40:[37,38],41:[42,43,44,72,73,74,95],42:[31,34,41,43,44],43:[41,42,44,72,73,74],44:[41,42,43],45:[14,15,16,17,20,21,22,23,24],46:[14,15,20,21,22,23,24],47:[20,21,22,23,24,72,73,74],48:[2,70,71,76,85],49:[2,70,71,76]}
editorial={
30:'Короткий вопрос проверяет распознавание явления; варианты молния, гром и радуга близки только общей атмосферной тематикой. Объяснение содержит механизм, требующий отдельного источника.',
31:'Вопрос задаёт местный ветер между морем и сушей, а пояснение уже ограничивает ответ морским бризом и дневным направлением; это может упростить выбор через формулировку.',
32:'Вопрос и вариант ответа ограничивают термин Атлантикой, тогда как пояснение расширяет его также на восточную часть Тихого океана; проверьте согласованность географического охвата.',
33:'Формулировка «опускающийся из грозы» может ошибочно внушать, что вихрь обязан выглядеть как нисходящий столб; соседние вихревые явления требуют чёткого разграничения.',
34:'Вопрос сводит муссон к сезонному ветру и азиатским летним ливням; ответное пояснение добавляет сезонную смену направления. Это полезное уточнение, но требует строгого источника и не должно превращать термин в синоним дождей.',
35:'Варианты противопоставляют вытянутую область замкнутым циклону/антициклону и гребню; формулировка NWS «обычно без замкнутой циркуляции» была бы более различительной, но текущая формулировка не уточняет этот критерий.',
36:'Парная карточка о гребне использует тот же ключевой слот 0, что и ложбина #35, создавая возможный позиционный сигнал в паре. Не менять замороженный ключ в этом пакете.',
37:'ENSO вводится аббревиатурой без расшифровки; причина Эль-Ниньо названа «ослаблением пассатов», что требует проверки точной причинной связи. Соседняя Ла-Нинья образует тематическую пару.',
38:'Ла-Нинья описана через охлаждение поверхности и усиление пассатов; проверьте, что география и временной масштаб указаны достаточно точно. Соседняя Эль-Ниньо образует пару.',
39:'Формулировка «особенно влияет» не задаёт измеряемого последствия САК; вопрос может проверять только расширение аббревиатуры. Уточнить наблюдаемый индекс/режим при редактуре.',
40:'IOD связан с температурным контрастом западной и восточной частей Индийского океана; термин «положительная фаза» требует точного определения и знака градиента.',
41:'«Переносят многие циклоны» — широкое следствие о струйных течениях; карточку легко спутать с поясом западных ветров (#43). Уточнить различие между узким высотным потоком и приземным поясом.',
42:'Русское «торговые ветры» почти напрямую подсказывает англоязычный термин trade winds, а «между тропиками и экватором» географически подозрительно: нужна проверка по первоисточнику.',
43:'Западные ветры представлены как поток средних широт, связанный с переносом циклонов; сравнение с высотным струйным течением (#41) и пассатами (#42) должно явно разделять масштаб и слой.',
44:'Вопрос спрашивает о направлении у полюсов; пояснение добавляет циркуляцию от полюсов к субтропикам. Проверьте, что оба направления описывают один и тот же пояс ветров без чрезмерного упрощения.',
45:'Карточка о CIN спрашивает определение, но ключевой ответ — краткая аббревиатурная формула. Текущий класс Hard выглядит несоразмерным терминологическому recall; класс заморожен и не меняется здесь.',
46:'Lifted Index проверяется как знак/смысл значения, однако Hard-класс может быть завышен для простого определения. Условие с уровнем 500 mb не задано в вопросе; класс и literal сохраняются.',
47:'Helicity вводится термином и одним словесным объяснением вращения; без контекста слоя/штормового относительного потока сложность может быть ниже Hard. Не добавлять неподтверждённые детали.',
48:'Столкновение капель описывает рост капель в тёплом облаке, но «сливаются» требует точности и отличия от ледяного процесса #49. Вопрос представляет простой recall при Hard-классе.',
49:'Процесс Бергерона описан через кристаллы и переохлаждённые капли; нужна точная проверка условия насыщения и переноса водяного пара. Hard-класс выглядит терминологическим recall и сохраняется.'}
entries=[]
for i in range(30,50):
 t=next(x for x in scope['targets'] if x['index']==i); card=byid[t['currentCard']['id']]
 assert card==t['currentCard']
 fields=[('prompt',card['prompt']),('answer0',card['answers'][0]['text']),('answer1',card['answers'][1]['text']),('answer2',card['answers'][2]['text']),('answer3',card['answers'][3]['text']),('explanation',card['explanation']),('difficulty_key',[card['difficulty'],card['correctIndex']]),('metadata',card['source'])]
 groups=[]
 for name,val in fields:
  literal=canon(val,sort=(name in ('metadata','difficulty_key')))
  src_status='HOLD_MISSING_EXACT_CAPTURE' if i in exact_missing else ('HOLD_EXACT_CAPTURE_THIN_FRAMES_ONLY' if i in thin else 'HOLD_SOURCE_REVIEW_REQUIRED')
  source_reason=(f'Не утверждаю факт по этому literal: точный URL {card["source"]["url"]} не имеет пригодного сохранённого первичного body в текущем пакете; требуется полный источник с разделом и цитируемым фрагментом. Сохранённое окружение/соседи не заменяют прямое доказательство.')
  if i in (35,36) and name in ('prompt','answer0','answer1','answer2','answer3','explanation'):
   source_reason='Текущий embedded URL не совпадает с лично прочитанным эквивалентом NWS glossary. NWS определяет trough как вытянутую область относительно низкого давления, обычно без замкнутой циркуляции; ridge — вытянутую область относительно высокого давления. Это ограниченная поддержка определения, но не подтверждает все дистракторы/следствия карточки; полный exact-source gate остаётся открытым.'
   src_status='PARTIAL_EQUIVALENT_PRIMARY_SUPPORT_EXACT_URL_MISMATCH'
  if i in (45,46) and name in ('prompt','answer0','answer1','answer2','answer3','explanation'):
   source_reason='SPC parcelvals.html лично прочитан: подтверждает CIN как интеграл отрицательной плавучести от исходного уровня до LFC и Lifted Index как разность температуры порции и среды на 500 mb; отрицательное значение означает более тёплую/плавучую порцию. Это другой URL, чем embedded frameset; не подтверждает все варианты и exact URL capture остаётся тонким.'
   src_status='PARTIAL_EQUIVALENT_PRIMARY_SUPPORT_EXACT_URL_MISMATCH'
  edit_reason=editorial[i] if name in ('prompt','explanation','difficulty_key','metadata') else f'Literal «{val}» участвует в различении терминов: проверьте, что он сохраняет единый предмет карточки и не подсказывает ключ формулировкой; связанный редакционный риск: {editorial[i]}'
  groups.append({'group':name,'literal':val,'literalSHA256':sha(literal),'source':{'status':src_status,'reason':source_reason,'evidenceRefs':[]},'editorial':{'status':'REVIEWED_OBSERVATION_NO_TEXT_CHANGE','reason':edit_reason}})
 neighbor_ids=clusters[i]
 targetNeighborObjects=[q for q in source if q['id'] in {next((x['currentCard']['id'] for x in scope['targets'] if x['index']==n),None) for n in neighbor_ids}]
 # neighbors are provided from the full-current neighbor set below, preserving all 80; refs identify indices for coordinator rebinding.
 entries.append({'index':i,'id':card['id'],'frozenClass':card['difficulty'],'frozenCorrectIndex':card['correctIndex'],'currentPreimageSHA256':sha(canon(card,sort=True)),'card':card,'groups':groups,'relatedCurrentNeighborIndices':neighbor_ids,'sourceAudit':{'embeddedURL':card['source']['url'],'status':'EXACT_URL_CAPTURE_MISSING' if i in exact_missing else 'EXACT_URL_CAPTURE_THIN' if i in thin else 'EXACT_URL_REVIEW_REQUIRED','personalReadReceipts':['NWS trough/ridge glossary; full saved bodies, exact URL mismatch' if i in (35,36) else 'SPC parcelvals; full saved body, exact URL mismatch' if i in (45,46) else 'SPC help frameset body; 676 bytes, no term-level definitions' if i==47 else 'No suitable personally read source body bound to this exact URL']},'qualityCredit':0})
neighbors=json.load(open(root/'full-current-neighbor-objects.json'))
packet={'schema':'mindbattle-weather30-49-source-editorial-packet-v1','authorNativeThreadId':'01a137d4-70e3-74f0-bbe4-0d13e5dca25f','scopeTupleSHA256':scope['reservedRootTupleSHA256'],'topicRAW':scope['currentRuntimeRAW'],'qualityCredit':0,'sourceLimitation':'No new capture/network. Statements lacking complete primary evidence are explicit HOLD. Packet is a review draft; no source qualification or production changes.','entries':entries,'currentNeighborSnapshot':neighbors,'rawSourceReceipts':[{'name':'NWS Trough glossary','url':'https://forecast.weather.gov/glossary.php?word=Trough','path':'/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle/docs/content-audits/question-quality-wave-7/coordinator-continuation-01a13619/capture-only/weather-next10-gaps/trough.body','bytes':3492,'sha256':'96a5e4e6d9e9242f6dcd8860ff36d71dd0753a4c8b0cd8bad2b0dce94a703aa'}, {'name':'NWS Ridge glossary','url':'https://forecast.weather.gov/glossary.php?word=Ridge','path':'/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle/docs/content-audits/question-quality-wave-7/coordinator-continuation-01a13619/capture-only/weather-next10-gaps/ridge.body','bytes':3673,'sha256':'182403e247425986f965279b82a5d19831d4a4c2992a05685514f2760115ad82'}, {'name':'SPC sounding help frameset','url':'https://www.spc.noaa.gov/exper/soundings/help/','path':'/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle/docs/content-audits/question-quality-wave-7/coordinator-continuation-01a13772/weather20-29-primary/cape-cin-sounding.body','bytes':676,'sha256':'aaa597f5a034b49ce1a9aab3cf79da695942430edc2cb6dd0bf5e1d050d62669','status':'THIN_FRAMESET_NO_TERM_CONTENT'}, {'name':'SPC parcel values','url':'https://www.spc.noaa.gov/exper/soundings/help/parcelvals.html','path':'/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle/docs/content-audits/question-quality-wave-7/coordinator-continuation-01a13772/weather20-29-primary/spc-parcel-values.body','bytes':2386,'sha256':'fc6ee69c1ea46c620c867bb2c35294597803563d64b9a57f6ed7b572c0226917','status':'READ_EQUIVALENT_URL_NOT_EMBEDDED'}, {'name':'NOAA Origin of Wind','url':'https://www.noaa.gov/jetstream/synoptic/origin-of-wind','path':'/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle/docs/content-audits/question-quality-wave-7/coordinator-continuation-01a13294/capture-only/weather-origin-wind-full-range-assembled.body','bytes':120647,'sha256':'f2b563bc770505e59b8726990598c38335c094dc4a4a3f03e8674351f54565e1','status':'READ_CONTEXT_ONLY_NO_BELT_DEFINITIONS'}]}
out=canon(packet,sort=False)
(root/'weather30-49-source-editorial-packet.json').write_bytes(out)
print(json.dumps({'path':str(root/'weather30-49-source-editorial-packet.json'),'bytes':len(out),'sha256':sha(out),'entries':len(entries),'groups':sum(len(x['groups']) for x in entries),'pairReasons':sum(2*len(x['groups']) for x in entries),'neighbors':len(neighbors),'qualityCredit':0},indent=2))
