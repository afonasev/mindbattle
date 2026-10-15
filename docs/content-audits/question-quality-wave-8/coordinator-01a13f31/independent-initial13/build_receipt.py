#!/usr/bin/env python3
"""Serialize personally authored INITIAL judgments; never adopts author/QA verdicts."""
import hashlib
import itertools
import json
from pathlib import Path
import re
import subprocess
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).resolve().parent
AUTHOR = ROOT / 'docs/content-audits/question-quality-wave-8/process-v2-engineering13-01a13f31/author/final13'
COORD = OUT.parent
def read(p):
    return json.loads(p.read_text())
def dump(p, x):
    p.write_text(json.dumps(x, ensure_ascii=False, indent=2) + '\n')
def canon(x):
    return json.dumps(x, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')
def sha(x):
    return hashlib.sha256(canon(x)).hexdigest()
def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()

judgments = read(OUT/'judgments.json')
applied = read(COORD/'apply-initial13.json')
sourceproof = read(AUTHOR/'sourceproof.json')
author_candidate = read(AUTHOR/'candidate.json')
author_peers = read(AUTHOR/'peer-snapshot.json')
qa = read(COORD/'qa-initial13.json')
topic_path = ROOT/'src/content/topics/engineering-machines.json'
topic = read(topic_path)
allq = {q['id']: q for q in topic['questions']}
before = json.loads(git('show', '532b283ea672c8b4e6ae39d02f2bbf3a6ec3e5aa:src/content/topics/engineering-machines.json'))
baseline = {q['id']: q for q in before['questions']}
sources = {x['path']: x for x in sourceproof['rawSources']}
orders = [x['sourceOrder'] for x in applied['applied']]
assert orders == list(range(26,36)) + [38,39,40]
assert len(author_candidate['entries']) == 13

# Each locator below was checked against the saved PRIMARY body, including the
# unrelated captures before the target in the two composite capture files.
locators = {
 '00f376fde503-skf_lubrication.pdf.txt': ('PDF P2 L10–24; P7 L141–159; P8–10 L165–237', 'Read complete relevant page contexts: costs, friction/wear benefits, contamination and lubricant-film mechanism. L208–214, not the author P3 locator, directly supports separated surfaces.', 'Saved text ends before all 36 PDF pages. Relevant P2/P7–10 contexts are continuous; no claim to have read absent later brochure pages.'),
 '0394a83905a1-public-web-1312-1.txt': ('Indium Semiconductor Fluxes section Product Overview L278–280, Features L282–297', 'Read the Indium full Product Overview with surrounding features within this composite capture; remove oxides/impurities and enable wetting are stated together.', 'File also contains a separate Mitutoyo capture with colliding L numbers. Only the Indium URL section is evidence for flux.'),
 '32ccce15059c-johnson_bubble_level.txt': ('Spirit Levels Vials L120–159, especially L126–139 and L148–154', 'Read complete substantive article from liquid/vial construction through bubble position, markings, sensitivity, temperature, pitch vials and certification; distinguished ordinary centre reading from special pitch vials.', 'Numerical accuracy examples contain suspect units but are not asserted in the card. Article does not say a tilted level always centres its bubble.'),
 '33b4de20e900-osu_machine_shop.txt': ('Full page L0–36; tool list L17–29', 'Read full saved page including lathe/mill definitions and abrasive wheel/belt tools; corroborates process/tool categories.', 'Short equipment listing; not a substitute for the GWU/MIT cutting-mechanism descriptions.'),
 '37a3e3858e3c-doe_belt_drive.pdf.txt': ('Both PDF pages P0–1 L0–120; especially L4–12,L24–36,L78–88', 'Read full two-page DOE tip sheet, including synchronous/notched belt distinction, diameter/speed relation, tension, example calculation and design requirements.', '2012 efficiency figures are contextual only; cards do not assert a current universal numerical efficiency.'),
 '433900a05721-khk_gears.pdf.txt': ('PDF P5–6 L123–173; P9–10 L249–304, with document context L0–529', 'Read saved introductory gear text, including wrapping connector classification, relative speeds, pitch/teeth geometry, involute mating, shaft layouts and tool/material sections. Separates direct gear contact from chain/belt connectors.', 'Capture ends L529 although metadata reports 568 lines; later application examples are absent. All relied-on P5–6/P9–10 contexts are continuous and present.'),
 '4f54b86afd8a-gwu_machine_tools.txt': ('Full saved L0–112; lathe L65–89; milling L90–112', 'Read full saved safety/lathe/milling page: rotating workpiece, turning along axis, facing across face, centre drilling, boring; table X–Y/head Z; cutter/flute and roughing/form operations.', 'English turning narrowly distinguishes facing, whereas Russian точение includes longitudinal/transverse feed. Source is shop instruction, not a universal machine geometry standard.'),
 '71d6803e8df8-tsubaki_drive_chain.txt': ('Full page L0–119; Chain Products L58–62', 'Read complete saved page: chain categories and transmission/conveying contrast, in the context of drive/attachment/conveyor/plastic chain and sprocket navigation.', 'The displayed source.url for card30 establishes transmission vs conveying but does not itself explicitly describe the chain/sprocket pairing. That pairing is supported by saved KHK P5.'),
 '7818a2029254-uni_rotation_alternate.pdf.txt': ('Full lecture capture L0–266; P1–2 L4–14; P9 L94–101', 'Read saved lecture, particularly complete classification/rigid-body slides: translation without rotation, pure rotation about fixed axis, equal angular displacement; later angular velocity/acceleration and torque contexts agree.', 'No assertion that all rotational motion is non-oscillatory; oscillation can be a rotational regime.'),
 '7991dce76a8d-case_drive_shaft_alternate.txt': ('Full page L0–188; Design and Construction L99–133', 'Read full saved SeaDog design page, including biological inspiration, seals, compliant legs, exact outer/inner shaft torque-and-bending passage and testing. The outer shaft resists bending of the inner shaft.', 'Specific robot example supports shaft function and extra fact; it is not an explicit general classification or Russian terminology authority.'),
 'a465b1529adf-mitutoyo_caliper_quick_guide.pdf': ('PDF pages20–23 / printed PG18–21, Calipers; matching extracted text lines1654–1945', 'Verified raw binary SHA and read the corresponding complete extracted Calipers page contexts in fdb9acf122bb. Outside/inside/depth measurement examples and measuring faces are present.', 'Binary hash is integrity evidence only. Semantic reading used saved full PDF text extraction; no claim of independent visual/render inspection.'),
 'bad10344ef6c-illinois_motion.txt': ('Full page L0–76; full question and answer L16–32', 'Read entire saved Q&A, including opening mostly-a-matter-of-words caveat, sinusoidal and non-sinusoidal oscillation, changing size, pump/steam pistons, saw, and context-dependent distinction in postscript.', 'Does not establish mutually exclusive oscillation and reciprocation. Engineer/physicist word choice is a tendency, not a rule excluding oscillatory piston motion.'),
 'bb35e04ee0c4-mit_machining.txt': ('Full article L0–143; chips L21–47, blade L50–80, settings L83–106', 'Read complete saved machining article. Grinding edges/abrasive grains, drill direction/feed, large-diameter lower spindle speed, deep-hole chip heating, cutting fluid and rigidity are all read in their full sections.', 'Illustrated tool diagrams are not separately visually inspected; claims used are explicit in continuous text.'),
 'be02b79df6fe-starrett_precision_rules.txt': ('Whole retained Precision Rules body, steel-rule definition and English/Metric graduation paragraph', 'Read entire saved short page-body record, including the two substantive paragraphs and stated page remainder. Confirms steel rule, length and inch/metric graduations.', 'Saved record is a substantive page-body transcription, not full original HTML or numbered reader output. No claimed line24–29 binding is used; retained full substantive paragraph is the locator.'),
 'cf6b64bcc79e-psu_translation_alternate.txt': ('Full page L0–62; Rigid Body Translation L2–12 and braking car L4', 'Read complete text, including translation/rotation/general planar distinction, braking-car example, zero angular acceleration and worked-problem contexts.', 'A body can translate while reciprocating or oscillating. This article does not create mutually exclusive taxonomy against those regimes.'),
 'dd033eb4f1cb-permatex_right_stuff.html': ('Instructions DIRECTIONS, Product Description, Features, Suggested Applications', 'Read substantive HTML body after excluding script/style: continuous bead and assembly instructions explicitly say material fills surface imperfections; Description addresses leaks/seepage; Features list oil/coolant/transmission-fluid resistance.', 'No claim that this particular RTV is suitable for fuel contact; instructions explicitly exclude gasoline/head-gasket use, neither asserted by the card.'),
 'f74840e9e4c0-mitutoyo_micrometer.txt': ('QuantuMike MD-E URL section L0–134; High-speed movement L31–33', 'Read complete saved QuantuMike page section after unrelated error/blog capture. The target section compares 0.5mm typical screw lead with 2mm spindle travel per thimble turn and adds ratchet/measurement contexts.', 'Composite file begins with a failed Henkel request and Indium blog. Those are diagnostics/non-evidence; only QuantuMike URL section supports micrometer.'),
 'fdb9acf122bb-mitutoyo_caliper_quick_guide.txt': ('Extracted lines1654–1945; PDF pages20–23 / printed PG18–21, Calipers', 'Read complete Calipers definition/nomenclature page, measurement examples page, vernier principles and general-use/inside/depth contexts. Measured dimensions are not inferred from search snippets.', 'Author pp2–4 locator is incorrect; PG18–21 / PDF20–23 is the independently read location. Other manual chapters are not relevant to this card.')
}
evidence = []
for path, x in sources.items():
    b=(ROOT/path).read_bytes()
    h=hashlib.sha256(b).hexdigest()
    assert h==x['sha256'], path
    locator, read_evidence, limitations = locators[Path(path).name]
    evidence.append(dict(path=path,url=x['url'],rawReadSHA256=h,bytes=len(b),locator=locator,readEvidence=read_evidence,limitations=limitations))
assert len(evidence)==18
source_by_path={x['path']:x for x in evidence}
def refs(paths):
    return [{k:source_by_path[p][k] for k in ['path','url','rawReadSHA256','locator']} for p in dict.fromkeys(paths)]

entries=[]
for a in applied['applied']:
    order=a['sourceOrder']; q=allq[a['id']]; j=judgments[str(order)]
    assert q==a['proposedCard'], f'CURRENT drift {order}'
    sp=next(x for x in sourceproof['entries'] if x['id']==q['id'])
    gs={x['group']:x for x in sp['literalGroups']}
    k=dict(prompt=q['prompt'], answers=[x['text'] for x in q['answers']],correctIndex=q['correctIndex'])
    literals=[('prompt_ordered_answers_key',k,j['key']),('explanation',q['explanation'],j['explanation'])]+[(f'note{i}',x['note'],j['notes'][i]) for i,x in enumerate(q['answers'])]
    groups=[]
    for name,literal,ground in literals:
        paths=list(gs[name]['sourcePaths'])
        # Correct three inherited author locator/source-binding mistakes.
        if order==26 and name=='prompt_ordered_answers_key':
            paths=list(gs['explanation']['sourcePaths'])
        if order==38 and name=='explanation':
            paths=list(gs['note1']['sourcePaths'])
        if order==40 and name=='explanation':
            paths=list(dict.fromkeys(gs['note1']['sourcePaths']+gs['note0']['sourcePaths']))
        if order==30 and name=='prompt_ordered_answers_key':
            assert any('khk' in p for p in paths)
        affected=(name=='explanation' and order==30) or (name=='prompt_ordered_answers_key' and order in [30,33,34])
        groups.append(dict(group=name,literal=literal,canonicalSHA256=sha(literal),status='FIX' if affected else 'PASS',individualGround=ground,sourcesLocators=refs(paths)))
    variants=[]
    for i,x in enumerate(q['answers']):
        bad=(order==33 and i in [0,1,2]) or (order==34 and i in [0,2,3])
        triple=dict(prompt=q['prompt'],answer=x['text'],note=x['note'])
        grammar='Полностью прочитано «'+q['prompt']+' — '+x['text']+'». '
        if order==27:
            grammar+='Название «'+x['text']+'» в мужском роде/единственном числе отвечает сочетанию «какой инструмент»; note грамматически относится к этому инструменту.'
        elif order in [28,29,30,31]:
            grammar+='Подпись «'+x['text']+'» в женском роде/единственном числе согласована с «какая передача»; род и форма не выделяют ключ.'
        elif order in [32,33,34,35]:
            grammar+='Именная подпись «'+x['text']+'» с согласованным определением среднего рода называет движение; формат одинаков для всех четырёх терминов.'
        else:
            grammar+='Отглагольное существительное «'+x['text']+'» в именительном падеже корректно называет процесс в ответ на полный вопрос; предметного/родового конфликта с note нет.'
        if order==26:
            grammar='Полная подстановка «Что наносят …? — '+x['text']+'» корректна в винительном падеже; note относится к названному материалу, управление согласовано.'
        variants.append(dict(slot=i,**triple,tripleCanonicalSHA256=sha(triple),grammar=dict(status='PASS',ground=grammar),plausibility=dict(status='PASS',ground=j['variants'][i]),truthUniqueKey=dict(status='FIX' if bad else 'PASS',role='key' if i==q['correctIndex'] else 'distractor',ground=j['variants'][i]),noteTruthUsefulness=dict(status='PASS',ground=j['notes'][i]),sourcesLocators=groups[i+2]['sourcesLocators']))
    b=baseline[q['id']]
    frozen=dict(id=q['id'],topicId='engineering-machines',difficulty=q['difficulty'],correctIndex=q['correctIndex'],orderedAnswerTexts=[x['text'] for x in q['answers']],baselineCommit='532b283ea672c8b4e6ae39d02f2bbf3a6ec3e5aa',idPreserved=q['id']==b['id'],difficultyPreserved=q['difficulty']==b['difficulty'],correctIndexPreserved=q['correctIndex']==b['correctIndex'])
    assert all(frozen[k] for k in ['idPreserved','difficultyPreserved','correctIndexPreserved'])
    entries.append(dict(id=q['id'],sourceOrder=order,stage='INITIAL',currentCard=q,currentCardCanonicalSHA256=sha(q),status='FIX' if j['defects'] else 'PASS',sixLiteralCanonicalGroups=groups,fourFullPromptAnswerNoteVariants=variants,absoluteLevel=dict(status='FIX' if any('ABSOLUTE' in d['code'] or 'LEVEL' in d['code'] for d in j['defects']) else 'PASS',assigned=q['difficulty'],ground=j['level']),correctNoteExtraFact=dict(status='PASS',ground=j['extra'],sourcesLocators=groups[q['correctIndex']+2]['sourcesLocators']),defects=j['defects'],frozen=frozen))

# MAIN tuples are editorial mappings personally made after reading the cards;
# notes and explanations are deliberately excluded from fact-identity matching.
tuples={
26:('контакт движущихся поверхностей','наносимый материал для уменьшения трения/износа','смазка','машина'),
27:('установка поверхности','прибор пузырькового контроля положения','уровень','бытовой измерительный инструмент'),
28:('два зубчатых колеса','название передачи непосредственным зацеплением','зубчатая передача','передача вращения'),
29:('гибкий ремень между шкивами','название передачи','ремённая передача','передача вращения'),
30:('металлическая цепь между звёздочками','название передачи','цепная передача','передача вращения'),
31:('вращающийся вал','название передачи момента самим валом','вальная передача','передача момента'),
32:('твёрдое тело вокруг фиксированной оси','общий геометрический вид движения','вращательное движение','кинематика'),
33:('тело перемещается без поворота','общий геометрический вид движения','поступательное движение','кинематика; варианты содержат пересекающиеся частные режимы'),
34:('поршень насоса вперёд/назад по одной линии','специальное название повторного хода','возвратно-поступательное движение','кинематика; более общие истинные виды не исключены'),
35:('маятник и натянутая струна','общий термин повторного движения туда/обратно','колебательное движение','школьные механические примеры'),
38:('вращающаяся заготовка и подаваемый резец','название обработки','точение','токарный станок'),
39:('вращающаяся многозубая фреза','название обработки','фрезерование','обработка резанием'),
40:('вращающееся сверло с осевой подачей','название обработки отверстия','сверление','обработка резанием'),
10:('валы с изменяющимся углом пересечения','вид шарнира передачи вращения','карданный шарнир','соединение валов'),
11:('идеальная зубчатая пара на параллельных валах','отсутствие осевой силы от наклона зубьев','прямозубая передача','силы в зацеплении'),
12:('внешняя косозубая пара на параллельных валах','совместимые угол и направление винтовых линий','одинаковый угол и противоположные направления','геометрия сопряжения'),
13:('делительные поверхности с общей вершиной','семейство для пересекающихся валов','коническая шестерня','геометрия делительных поверхностей'),
14:('взаимно перпендикулярные непересекающиеся оси','подходящий тип из предложенного набора','червячная передача','пространственная компоновка; CURRENT cycle1'),
15:('подшипник качения для высокой скорости','класс при малом контакте вместо линейного','шариковый подшипник','опора вращения'),
16:('компактная опора с приоритетом радиальной грузоподъёмности','класс подшипника качения','роликовый подшипник','нагрузка и вторичная скорость'),
17:('вал во втулке без тел качения','тип опоры скользящей поверхностью','подшипник скольжения','опора вала'),
18:('подшипник качения','классификация по преимущественно осевой нагрузке','упорный подшипник','направление нагрузки'),
19:('перекрывающиеся листы','вид соединения','нахлёсточное соединение','стык деталей'),
20:('торцы деталей в одной плоскости','вид соединения','стыковое соединение','стык деталей'),
21:('материал с заметной необратимой деформацией','пороговое напряжение','предел текучести','свойство материала'),
22:('текущая вместо исходной площади сечения','мера напряжения','истинное напряжение','после начала пластического течения'),
23:('рост трещины','характеристика сопротивления','трещиностойкость','материал'),
24:('медленная горячая деформация при длительной нагрузке','сопротивление процессу','сопротивление ползучести','материал'),
25:('горизонтальный участок S–N у некоторых сталей','характеристика циклической прочности','предел выносливости','много циклов'),
36:('конец детали к поверхности другой','вид соединения','тавровое соединение','примерно прямой угол'),
37:('края двух деталей под углом','вид соединения','угловое соединение','стык деталей'),
41:('множество абразивных зёрен','процесс обработки поверхности','шлифование','съём материала'),
49:('быстрое позиционирование без резания','команда G-кода','G00','ЧПУ'),
50:('линейная интерполяция с рабочей подачей','команда G-кода','G01','ЧПУ'),
55:('вращающийся вал','поддерживающая деталь с уменьшением трения','подшипник','опора'),
57:('колебания скорости вращения','сглаживание запасом кинетической энергии','маховик','вращающаяся деталь'),
58:('два вращающихся вала','временное соединение/разъединение','сцепление','узел трансмиссии'),
65:('гидравлический исполнитель','создание поступательного хода поршня','гидроцилиндр','гидропривод'),
66:('гидравлический исполнитель','создание вращательного движения','гидромотор','гидропривод'),
76:('жидкость','машина сообщения энергии и перемещения','насос','гидромашина'),
80:('получение формы удалением материала','общий класс обработки','механическая обработка','режущий инструмент')
}
actual_orders=[x['sourceOrder'] for x in author_peers['actualCurrentPeers']]
supplemental=[10,41,49,50,55,57,58,65,66,76,80]
peer_orders=list(dict.fromkeys(actual_orders+supplemental))
def main_tuple(t):
    return dict(zip(['entity','relation','value','context'],t))
def wrap(topic_id,q,order=None):
    x=dict(topicId=topic_id,id=q['id'],card=q,canonicalSHA256=sha(q))
    if order is not None: x['sourceOrder']=order
    return x
targets=[dict(**wrap('engineering-machines',e['currentCard'],e['sourceOrder']),MAIN=main_tuple(tuples[e['sourceOrder']])) for e in entries]
peers=[]
for o in peer_orders:
    q=topic['questions'][o-1]
    old=next((x for x in author_peers['actualCurrentPeers'] if x['sourceOrder']==o),None)
    peers.append(dict(**wrap('engineering-machines',q,o),MAIN=main_tuple(tuples[o]),authorSnapshotDrift=old is not None and q!=old['card'],readEvidence='CURRENT full card read: prompt, ordered answers/notes, key, explanation and source; compared MAIN tuple only.'))

cross_spec={
 'physics-friction-effect':('physics',('скользящие поверхности','направление кинетического трения','против относительного скольжения','сухое трение')),
 'physics-ext-quality-factor':('physics',('резонанс колебательной системы','безразмерная характеристика остроты','добротность','резонанс')),
 'tourism-travel-rack-railway':('tourism-travel',('горная железная дорога с центральной рейкой','вид железной дороги','зубчатая железная дорога','преодоление уклона')),
 'railways-rail-grinder':('railways',('дефекты и профиль головки рельса','специализированная путевая машина','рельсошлифовальный поезд','ремонт рельсов')),
 'cars-road-transport-power-stroke-expansion':('cars-road-transport',('цикл поршневого двигателя','такт передачи энергии коленчатому валу','рабочий ход','четырёхтактный двигатель')),
 'materials-fatigue-cyclic':('materials',('вал после миллионов циклов','механизм разрушения','усталость','циклическая нагрузка')),
 'oceans-seas-wave-wind':('oceans-seas',('поверхность воды с ветровыми колебаниями','название явления','волна','океан')),
 'astronomy-space-earth-rotation-day':('astronomy-space',('Земля','движение как причина дня и ночи','вращение вокруг оси','освещённость планеты')),
 'astronomy-space-venus-retrograde-rotation':('astronomy-space',('Венера','отличие направления вращения','ретроградность','планеты')),
 'board-games-spinner-spin':('board-games',('компонент настольной игры','выбор сектора вращением стрелки','вертушка','случайный выбор')),
 'crafts-sandpaper-abrasive':('crafts',('абразивные зёрна на основе','название материала сглаживания','наждачная бумага','ручная обработка')),
 'laboratories-measurement-caliper-diameter':('laboratories-measurement',('диаметр монеты','инструмент более точного измерения','штангенциркуль','размерный контроль')),
 'laboratories-measurement-micrometer-thickness':('laboratories-measurement',('толщина тонкой проволоки','инструмент высокой точности','микрометр','размерный контроль')),
 'ships-navigation-roll-motion':('ships-navigation',('судно с борта на борт','название угловой качки','бортовая качка','продольная ось судна')),
 'ships-navigation-pitch-motion':('ships-navigation',('судно носом/кормой вверх-вниз','название угловой качки','килевая качка','поперечная ось судна'))
}
for id,(tid,t) in cross_spec.items():
    d=read(ROOT/f'src/content/topics/{tid}.json')
    o,q=next((i,q) for i,q in enumerate(d['questions'],1) if q['id']==id)
    peers.append(dict(**wrap(tid,q,o),MAIN=main_tuple(t),readEvidence='Full CURRENT card personally read; counterpart MAIN differs in entity/relation/value/context. Notes may repeat canonical facts without creating a MAIN duplicate.'))

def description(x):
    m=x['MAIN'];return f"{m['entity']} / {m['relation']} → {m['value']} ({m['context']})"
def compare(a,b):
    ao=a.get('sourceOrder') if a['topicId']=='engineering-machines' else None
    bo=b.get('sourceOrder') if b['topicId']=='engineering-machines' else None
    special=''
    if ao in [28,29,30,31] and bo in [28,29,30,31]:
        special='Один пул альтернативных передач, но разные основные передающие звенья; определения разных элементов пула не являются прямым/обратным повтором одного факта. '
    elif ao in [32,33,34,35] and bo in [32,33,34,35]:
        special='Различные определения общего геометрического вида и повторного режима: тождества MAIN нет, однако пересечение классификаций создаёт отдельные defects 33/34, оно не замаскировано как дубль. '
    elif ao in [38,39,40] and bo in [38,39,40,41,80]:
        special='Операции различаются режущим звеном/подачей; общий класс механической обработки и отдельный процесс не спрашивают один и тот же факт. Каноническая note про другой процесс разрешена. '
    elif ao==28 and bo in [11,12,13,14]:
        special='Общая зубчатая передача определяется способом передачи движения; сосед проверяет силу/геометрию конкретной пары, а не это общее определение. '
    elif ao==26 and bo in [17,55]:
        special='Смазка — наносимый материал; подшипник — опорная деталь. Совпадение уменьшения трения не делает функции объектов идентичными. '
    elif ao==27 and b['topicId']=='laboratories-measurement':
        special='MAIN уровня — пузырьковая установка поверхности; MAIN соседа — размер монеты/проволоки. Совпадают только distractor notes о размерных инструментах. '
    elif ao in [32,33,34,35] and b['topicId'] in ['astronomy-space','ships-navigation','oceans-seas','physics','board-games']:
        special='Сосед спрашивает причину, прибор, характеристику либо название конкретного явления, а target — тип движения; использование движения как условия не превращает это в обратную формулировку его общего определения. '
    else:
        special='Сравнены спрашиваемые связи и значения с контекстом, а не совпадения слов в заметках; MAIN кортежи описывают разные отношения/объекты. '
    return dict(leftId=a['id'],leftTopicId=a['topicId'],leftCanonicalSHA256=a['canonicalSHA256'],rightId=b['id'],rightTopicId=b['topicId'],rightCanonicalSHA256=b['canonicalSHA256'],leftMAIN=a['MAIN'],rightMAIN=b['MAIN'],directDuplicate=False,reverseDuplicate=False,leftToRight=dict(status='DISTINCT_MAIN',ground=special+'Левая связь: '+description(a)+'. Правая: '+description(b)+'.'),rightToLeft=dict(status='DISTINCT_MAIN',ground='В обратном направлении ответ «'+b['MAIN']['value']+'» относится к «'+b['MAIN']['relation']+'», а не к связи «'+a['MAIN']['relation']+'» для «'+a['MAIN']['entity']+'». Перестановка условия/ключа не воспроизводит левый MAIN.'))

mutual=[compare(a,b) for a,b in itertools.combinations(targets,2)]
external=[compare(a,b) for a in targets for b in peers]
assert len(mutual)==78
peer_receipt=dict(stage='INITIAL',freshPeerDelta='CURRENT11/12/14 reread after apply-gear-newsolution3-cycle1.json; target13 unchanged. No restart of sources or target review.',targets=targets,actualRelevantCURRENTNeighbors=peers,mutual13ProposedPairsBidirectional=mutual,eachTargetAgainstActualCURRENTNeighborsBidirectional=external,MAINOnlyPolicy='Duplicate identity concerns prompt+key relation, including direct/reverse restatements. Wrong notes may and preferably do reuse another key canonical fact. Their reuse is not a defect.',counts=dict(targets=len(targets),currentNeighbors=len(peers),mutualPairs=len(mutual),targetToNeighborPairs=len(external)),limitations='Candidate retrieval is a tool-assisted union of narrow entity/mechanism searches over every CURRENT topic MAIN. It is not a semantic proof over arbitrary undiscovered paraphrases. All saved relevant peers and both target sides were personally read.')
dump(OUT/'peer-review.json',peer_receipt)
dump(OUT/'source-evidence.json',dict(stage='INITIAL',rawSources=evidence,reuse='All18 saved raw sources reused; no HTTP200/snippet accepted as content proof; source/read limitations explicit.'))
counts={s:[e['sourceOrder'] for e in entries if e['status']==s] for s in ['PASS','FIX','HOLD']}
receipt=dict(stage='INITIAL',independent=True,createdAt=datetime.now(timezone.utc).isoformat(),worktree=str(ROOT),branch=git('branch','--show-current'),actualRef=git('rev-parse','HEAD'),baselineCommit='532b283ea672c8b4e6ae39d02f2bbf3a6ec3e5aa',applyCommit='d6b4a20e6cd4899e8240319c991baff783279e8e',qaCommit='fb5b7acf18beb40975cc4f36c758c7424b27a9f7',pinnedProcessRef='12e5581b:.agents/references/question-revision.md',policyRead=['pinned process','docs/content-audits/question-authoring-guide-2026-09-02.md','mindbattle-planning/docs/GAME_SPEC.md Контент вопросов','mindbattle-planning/openspec/specs/question-catalog/spec.md21–33'],hashMethod='UTF-8 JSON dumps sort_keys=True separators=(comma,colon) ensure_ascii=False; entire card and each literal/triple separately.',entries=entries,counts=counts,qualityCredit=0,rootBinding='Pending coordinator adjudication and binding. INITIAL PASS is an independent content judgment, not catalog/root credit.',evidence=dict(sources='source-evidence.json',peers='peer-review.json',judgments='judgments.json'),priorQAReadOnly=dict(path=str((COORD/'qa-initial13.json').relative_to(ROOT)),numTotalTests=qa['numTotalTests'],success=qa['success'],adoptedAsEditorialPass=False),notRun=['No tests/runtime/browser/audio/build/deploy; documentation receipt only. No claim of human acceptance.'],cleanup=dict(ownProcesses=[],temporaryResourcesCreated=[],gitMutation='Forbidden by task; coordinator must preserve own output directory in Git.',sourceCopiesCreated=0,foreignWork='Not modified; repository contains concurrent unrelated changes and staged evidence lifecycle work.'),nextAction='Coordinator adjudicates INITIAL FIX30/31/33/34/39/40, requests one directed cycle1 for chosen fixes; reader checks only changed cards and affected peer relations. Unresolved after cycle1 => FINAL HOLD.',finalIntegrity=dict(current13EqualsAppliedProposal=True,groups=78,fullVariants=52,rawSources=18,mutualPairs=78,currentNeighbors=len(peers),targetNeighborPairs=len(external),frozenIdDifficultyKey=True))
dump(OUT/'receipt.json',receipt)
print(json.dumps(dict(counts=counts,groups=78,variants=52,sources=18,neighbors=len(peers),comparisons=78+len(external),output=str(OUT)),ensure_ascii=False))
