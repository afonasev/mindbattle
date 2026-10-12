import json,hashlib,subprocess,re
from pathlib import Path
ROOT=Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle')
assert Path(subprocess.check_output(['git','rev-parse','--show-toplevel'],cwd=ROOT).decode().strip())==ROOT
OUT=ROOT/'docs/content-audits/question-quality-wave-6/independent-pilot/resume-2026-10-12-winter30-current'
pre=json.loads((OUT/'preflight.json').read_text());manifest={m['id']:m for m in json.loads((OUT/'sources-manifest.json').read_text())}
sha=lambda b:hashlib.sha256(b).hexdigest()
canon=lambda o:json.dumps(o,ensure_ascii=False,separators=(',',':')).encode()
proof={}
def node(k,file,*indices):
 d=json.loads((OUT/'readings'/(file+'.json')).read_text())['textNodes'];proof[k]=[{**manifest[file],'locator':{'htmlTextNodeIndex0Based':i,'recipe':'HTMLParser handle_data stripped nonempty outside script/style'},'exactQuote':d[i],'exactQuoteSha256':sha(d[i].encode())} for i in indices]
def pdf(k,file,page,start,end,section,printed=None):
 text=json.loads((OUT/'readings'/(file+'.json')).read_text())['physicalPages1Based'][str(page)];a=text.index(start);b=text.index(end,a) if end else len(text);quote=text[a:b];proof[k]=[{**manifest[file],'locator':{'pdfPhysicalPage1Based':page,'printedPage':printed,'section':section,'extraction':'pypdf page.extract_text(); exact substring, whitespace retained'},'exactQuote':quote,'exactQuoteSha256':sha(quote.encode())}]
E='fis-equipment-2026-10-08.pdf';I='fis-icr-2026.pdf';S='isu-sys-rules-2026.pdf';H='iihf-olympic-2026-terminology.html';C='coc-figure-skating.html'
pdf('edge',E,16,'3.1.2.1 Definition','3.1.2.2 Geometric','3.1.2.1',16)
pdf('weight',E,16,'3.1.1.2.2 Ski Weight','3.1.2 Component','3.1.1.2.2',16)
pdf('interface',E,24,'3.1.3 Component','3.1.3.2 Geometric','3.1.3.1',24)
pdf('binding',E,24,'3.1.4 Component',None,'3.1.4.1',24)
pdf('brake',E,25,'3.1.5 Component','3.2 Ski boots','3.1.5.1',25)
pdf('boot',E,25,'3.2 Ski boots','3.2.2 Geometric','3.2.1',25)
pdf('sole',E,25,'3.2.2 Geometric',None,'3.2.2.1',25)
pdf('poles',E,27,'3.3 Ski poles','3.4 Competition suits','3.3',27)
pdf('goggles',E,35,'3.7 Ski goggles','3.8 Ski gloves','3.7',35)
pdf('bearing',E,15,'3.1.1.2.1 Bearing',None,'3.1.1.2.1',15)
pdf('helmet','hockeycanada-player-equipment-guide.pdf',13,'HELMET','At Hockey Canada','HELMET')
pdf('shin','hockeycanada-player-equipment-guide.pdf',5,'SHIN PADS',None,'SHIN PADS')
pdf('facial','hockeycanada-facial-protectors.pdf',80,'FACIAL PROTECTORS',None,'FACIAL PROTECTORS',80)
pdf('block',S,43,'7.  DEFINITION',None,'Definition of elements/shapes section 7',43)
pdf('shapes',S,44,'Circle (Artistic',None,'Circle / Line / Wheel',44)
pdf('homology',I,79,'650.3 Documents',None,'650.3.1',73)
pdf('width',I,104,'902 The Courses','903 Course Setting','902.1',98)
pdf('gs',I,104,'903.1.3 A Giant Slalom','903.1.4','903.1.3',98)
pdf('combined',I,109,'1101 Alpine Combined','1102 Classical Combined','1101.1',103)
pdf('sum',I,108,'1100.7 The Combined',None,'1100.7',102)
pdf('superg',I,108,'1006 Execution','1007 Crash Helmet','1006',102)
pdf('gate',I,86,'661.4 Correct Passage','662 Importance','661.4.1-661.4.2',80)
pdf('jumpbase','fis-ski-jumping-current.pdf',71,'433.3 The Collective','433.4 The Total','433.3',69)
pdf('jumpcomp','fis-wc-jumping-men-2026-27.pdf',13,'4.5  For all WCJ','4.6','4.5',13)
pdf('expiry',I,83,'650.5.5 Expiration','650.5.7 Compulsory','650.5.5-650.5.6.3',77)
for k,ids in {'mask':[94,95],'boards':[37,38],'endboards':[92,93],'cage':[121,122],'goalposts':[130,131],'glass':[37,38],'stick':[230,231],'overtime':[167,168,173],'regulation':[206,207],'intermission':[142,143],'shootout':[218,219],'powerplay':[220,221],'shorthanded':[186,187,220,221],'delayed':[79,80,81],'hat':[134,135],'emptygoal':[90,91],'blocker':[33,34],'catcher':[45,46]}.items():node(k,H,*ids)
for k,ids in {'overview':[66,67,69,71,73,74],'singles':[80,81],'pairs':[84,85],'dance':[88,89],'programorder':[80,81,84,85,88,89]}.items():node(k,C,*ids)
node('throw','skate-throw-complete.html',17,18)
node('synchro','isu-synchronized-skating-2026.html',44)
node('alpine','alpine-skiing.html',71,72,73,74,75,76,77,80,81,83,84,85)
node('long','long-track.html',75,76)
node('mass','long-track.html',89,90,91)
node('pursuit','long-track.html',95,96,97)
node('short','short-track.html',67,68,69,70,71,72,73,74,75)
node('jump','coc-ski-jumping.html',69,70,71)
node('halfpipe','coc-snowboard.html',81,83)
node('mogul','coc-freestyle-skiing.html',77,79,80)
node('visor','uvex-wanted-visor-pro-v.html',55,56,57,59)
node('uvex','uvex-victorious-pro-v-goggles.html',54,55,56,58,62,76)
node('sprint','ibu-competition-formats.html',176)
node('biapursuit','ibu-competition-formats.html',190)
node('biamass','ibu-competition-formats.html',234)
node('bobequip','bcs-bobsleigh-facts.html',96)
node('bobstart','bcs-bobsleigh-facts.html',82,84)
node('bobshoe','bcs-bobsleigh-facts.html',103)
# Manually authored independent source/editorial readings; no author verdicts or analyses used.
reviews={}
def F(refs,s,e,code='PP'):
 return {'sourceRefs':refs.split(),'sourceVerdict':{'P':'PASS','F':'FIX','H':'HOLD'}[code[0]],'editorialVerdict':{'P':'PASS','F':'FIX','H':'HOLD'}[code[1]],'sourceAnalysis':s,'editorialAnalysis':e}
def add(n,d,rows):
 assert len(rows)==6;reviews[f'winter-sports-{n:03}']={'difficultyAnalysis':d,'readings':rows}
add(7,'Easy сохранён: узнавание функции канта по повороту, без знания номера правила. С 023 связан той же деталью, но 023 спрашивает нормативный материал и боковую передачу усилий.',[
F('edge','FIS связывает края скользящей поверхности с передачей боковых сил; связь с удержанием в повороте является физическим толкованием этой функции, а не цитатой о снеге.','Все четыре варианта прочитаны: ботинок и крепление передают управление косвенно; именно контактный край объясняет «цепляться». Формулировка допускает косвенное участие других деталей; желательно уточнить непосредственный контакт.', 'PF'),
F('edge','Два утверждения — положение краёв и твёрдый износостойкий материал — находятся в одной полной дефиниции 3.1.2.1.','Два предложения, нормативная функция и материал; объяснение не подменяет геометрию ботинка.'),
F('boot','3.2.1 прямо говорит robust footwear, firm enclosure и transfer of every steering movement.','О ботинке дан свой факт — охват стопы и передача движений, без называния канта.'),
F('binding','3.1.4.1 говорит освобождение ботинка при pre-set loads.','Полезное свойство крепления, отличное от контакта канта со снегом.'),
F('edge','3.1.2.1 подтверждает материал и lateral forces.','Правильная справка добавляет материал и положение края сверх бытового вопроса о сцеплении.'),
F('poles','3.3 запрещает metal baskets из-за риска травмы.','Конкретный нормативный факт именно о палках; ключ не раскрывает.')])
add(8,'Easy сохранён: знакомая пара названий программ. Главный факт совпадает с 026, который спрашивает первый сегмент этой же последовательности. HOLD до решения координатора о замене одного вопроса.',[
F('programorder','В singles и pairs short отбирает участников free; overview относит обе программы к figure skating.','Ключ единственный среди четырёх разных видов; вопрос и 026 проверяют один порядок short→free, поэтому смысловой дубль остаётся.', 'PH'),
F('programorder','Singles/pairs подтверждены раздельными абзацами 80–85; rhythm→free dance — 88–89, а не одним обзорным списком.','Два предложения; оговорка про танцы устраняет подмену rhythm dance короткой программой.'),
F('jump jumpbase jumpcomp','COC71 и ICR433.3 подтверждают базовый collective score style+distance. Но полный WC2026/27 пункт4.5 требует wind/gate system для всех WCJ; справка не оговаривает базовый балл и формат без компенсаций.','Факт полезен, однако «итоговый» без оговорки вводит в заблуждение о полном современном расчёте. Добавить точную область базовой суммы и дополнительные компенсации.', 'FF'),
F('halfpipe','Абзац 83 перечисляет variety, difficulty, style, execution.','Четыре конкретных критерия именно хафпайпа, без утечки названия фигурного катания.'),
F('mogul','Абзац 80 даёт turns 60%, speed20%; это могул, не dual moguls50/25/25.','Два числа названы с дисциплиной; факт полезен и не называет ключ.'),
F('singles','80 подтверждает номинальные 2:40 и семь элементов, но также прямо задаёт ±10 секунд.','Полезный новый факт, однако длительность написана как точная; добавить допуск и взрослую/олимпийскую область применения.', 'PF')])
add(23,'Medium сохранён: специальная нормативная функция/материал отличает кант от четырёх компонентов. 007 связан с кантами, но бытовое сцепление и нормативное определение не полностью тождественны.',[
F('edge','Дефиниция 3.1.2.1 одновременно называет hard material, wear и lateral forces.','Интерфейс, крепление и тормоз не соответствуют совокупности свойств; подсказки названием ключа нет.'),
F('edge','Edges of running surface подтверждает положение; hard resistant материал и силы подтверждены тем же абзацем.','Два предложения; ясно связывает положение и назначение, без неподтверждённого числового требования.'),
F('interface','3.1.3.1 устанавливает положение между skis и release bindings.','Свой факт об интерфейсе, не инструкция выбрать канты.'),
F('binding','3.1.4.1 задаёт pre-set нагрузку освобождения.','Полезная защитная функция крепления, без ключа.'),
F('edge','Справка точно передаёт определение материала и сил.','Сверх вопроса добавлено расположение по краю скользящей поверхности; это содержательная геометрия, не одна замена «канты» синонимом.'),
F('brake','3.1.5.1 описывает slowdown detached ski; авторская страница 27 была про палки, исправленная привязка —25.','Собственное назначение тормоза, ответ не назван.')])
add(26,'Easy сохранён. HOLD по смысловому дублю с 008: знание, что short precedes free, решает оба вопроса, различие обратного запроса не создаёт нового факта.',[
F('programorder','80–85 раздельно описывают short→free у singles и pairs, олимпийские проходные места явно названы.','Все варианты сегментов прочитаны; короткая единственна для singles/pairs. В каталоге 008 тот же порядок программ.', 'PH'),
F('programorder','80–85 подтверждают первый тезис;88–89 отдельно dance/rhythm/free.','Два предложения с полезной границей дисциплин.'),
F('dance','89 указывает top20 couples from rhythm dance advance free dance.','Самостоятельный олимпийский факт о произвольном танце; не сообщает short для одиночников.'),
F('programorder','Порядок short→free подтверждён в singles и pairs.','Повторяет ровно основной вопрос и ключ; нового факта о короткой программе нет.', 'PF'),
F('dance','88–89 подтверждают rhythm и free dance.','Факт именно о ритмическом танце, другой дисциплине; не раскрывает требуемую короткую программу.'),
F('singles','80 перечисляет три jumping passes,81 семь; сравнение напрямую следует из двух абзацев Olympic overview.','Полезное сравнение нагрузки сегментов; формулировка «одиночники» шире Olympic seniors, нужна оговорка уровня/редакции, актуальные ISU после июня не проверены.', 'HF')])
add(29,'Easy сохранён: повседневное узнавание детали застёжки; чашка и ремень близки, но глагол «застёгивают» разделяет их.',[
F('helmet','HELMET говорит chinstrap snug enough prevent wobbling; положение под chin следует из названия и чашки, не из картинки.','Все варианты разных деталей прочитаны; ремешок — единственная застёжка.'),
F('helmet','Prevent wobbling, chin cup touches chin и1–2 fingers eyebrows — три независимых пункта одной страницы13.','Два предложения, все три части подтверждены; не смешивает чашку и корпус.'),
F('helmet','Пункт про chinstrap подтверждает плотную посадку.','Повтор основной цели «не болтался», ссылка на Hockey Canada не добавляет факта о ремешке.', 'PF'),
F('helmet','Страница требует cup touching chin; удержание именно чашки ремешком на этой странице не утверждается.','Первая часть полезна, вторую нужно независимо подтвердить; не закрывать пробел общим рассказом о шлеме.', 'HP'),
F('helmet','Пункт1–2 fingers above eyebrows подтверждает число и ориентир.','Полезный факт о посадке корпуса; ключа нет.'),
F('helmet','Always check CSA certification sticker прямо указан.','Отдельный конкретный факт о наклейке и проверке, применим к своему варианту.')])
add(30,'Easy сохранён: термин маска знакомый; решётка/экран описывают исполнение протектора, не отдельное имя вратарской защиты.',[
F('mask facial','IIHF Face Mask определяет goalkeeper protection; Hockey Canada различает full protectors и visors.','Ключ терминологически единственный, хотя реальные маски могут содержать решётку; вопрос о названии, не материале.'),
F('mask facial','Mask подтверждена IIHF; три типа fullface и visor eyes-only — полная страница80.','Два предложения; не говорит, что решётка не может быть частью маски.'),
F('facial','Full-face styles включают wire cage.','Факт о категории решётки конкретен, ключ не назван.'),
F('mask','IIHF действительно относит mask к goalkeeper (также women players).','Справка повторяет вопрос/ключ без дополнительного свойства маски.', 'PF'),
F('facial','Fullface styles включают high-impact polycarbonate shield.','Материал/категория экрана даёт собственную справку.'),
F('facial','Таблица categoryC describes partial shields only eyes, age18+.','Частичная защита глаз — полезный факт; отсутствие возраста здесь не меняет название категории.')])
add(31,'Easy сохранён, но вопрос почти переводит goggles в ключ. Требуется новый содержательный критерий в том же классе, а не переименование difficulty.',[
F('goggles','FIS heading3.7 буквально Ski goggles.','Prompt «лыжными очками» и ответ «горнолыжные очки» делают задачу словесным сопоставлением, а не знанием экипировки.', 'PF'),
F('goggles visor uvex','FIS подтверждает goggles; uvex visor integrated подтверждён, но victorious proV также goggles, не доказательство отдельной категории спортивных очков.','Два предложения; классификация спортивных очков нуждается в правильной модели источника.', 'FF'),
F('visor','Wanted visor proV — visor helmet с self-tinting variomatic; integrated часть следует из whole product visor helmet.','Модель и реакция освещения — конкретный факт о визоре.'),
F('uvex','Victorious proV назван goggles со strap/foam/OTG; Ski touring лишь listed application. Это не отдельная спортивная модель очков.','UVA/UVB/UVC подтверждены, но вариант обозначает другую категорию; заменить источник/факт.', 'FF'),
F('goggles','3.7 прямо describes weather/rays optically correct lenses.','Добавляет назначение и оптику сверх простой идентификации goggles.'),
F('uvex','OTG design в highlights62 и полном описании56 подтверждает over prescription glasses.','Справка даёт конкретную связь корригирующих очков с конструкцией OTG, ключ не раскрывает.')])
add(32,'Easy сохранён: посадка щитка по анатомическим ориентирам; оба ориентиры близкие, источник явно задаёт верх конька.',[
F('shin','Physical5 прямо from knee down to top of skate.','Среди четырёх точек источник однозначно даёт верх конька.'),
F('shin','Границы knee→top skate и knee centre donut находятся рядом в полном разделе.','Два предложения; второй факт о выемке помогает примерке.'),
F('shin','Диапазон knee→top skate включает середину голени.','Неверная справка прямо называет верх конька — ключ, исправить утечку.', 'PF'),
F('shin','Two finger widths между topfoot и bottompad буквально указан.','Число и ориентиры конкретны и относятся к нижней посадке щитка.'),
F('shin','Knee sits comfortably in centre donut подтверждает место колена.','Факт о колене полезен и не раскрывает нижний край.'),
F('shin','Границы покрытия прямо подтверждены.','Правильная справка повторяет заданный ответ без нового факта.', 'PF')])
add(35,'Easy сохранён: пары распознаются по двум характерным элементам, танцы/синхронное — близкие реальные дисциплины.',[
F('pairs','84 перечисляет twist lift иthrow в pairs short.','Два элемента дают единственный pairs среди четырёх дисциплин.'),
F('pairs throw','Первый тезис —84–85; помощь takeoff и самостоятельное landing —полная отдельная Throw Jump статья18. Старый T-slice не использован.','Два предложения; второй раскрывает механику выброса, а не только называет пары.'),
F('dance','88–89 перечисляют dance segments, lifts, twizzles иstep sequences.','Два сегмента и тип элементов — факт о танцах; не называет pairs.'),
F('singles','80–81 перечисляют jumps spins step sequence.','Справка о составе singles программы конкретна.'),
F('pairs','84 содержит twist,throw иsolo jump performed side-by-side.','Добавляет третью разновидность прыжка рядом друг с другом сверх двух элементов prompt.'),
F('block shapes','Current ISU44 перечисляет circle,line,wheel;block на43. Привязка исправлена на полный rulebook, не статью о будущем Synchro9.','Свои геометрические построения синхронного катания полезны.')])
add(36,'Easy сохранён: термин дополнительного периода; shootout — близкий, но не период.',[
F('overtime','168 устанавливает overtime после tie regulation.','Овертайм единственен среди периода, перерыва и shootout.'),
F('overtime shootout','168 подтверждает дополнительное время;219 shootout after overtime. Конкретная Olympic страница не заменяет все возможные турнирные правила.','Два предложения; «в некоторых форматах» сохраняет нужную оговорку.'),
F('shootout','219 прямо ties after overtime→shootout, но 2026 Olympic page не универсальный IIHF rulebook для всех форматов.','Для этого глоссария факт полезен; нужен форматный предел вместо универсального «IIHF предусматривает».', 'PF'),
F('regulation','207 определяет three20min periods excludes overtime/shootout.','Отдельный факт о структуре основного времени.'),
F('intermission','143 определяет recess between three periods.','Факт о назначении перерыва свой, не сообщает overtime.'),
F('overtime','168tie и173first goal stop подтверждены.','Добавляет sudden-death условие сверх вопроса о названии.')])
add(38,'Easy сохранён: окружение площадки противопоставлено стеклу и воротам; концевые борта лишь часть, не вся конструкция.',[
F('boards','38 говорит encloses playing surface иglass rises above.','Единственны общие борта, концевые ограничивают только торцы.'),
F('boards cage goalposts','Окружение и стекло —38; cage —122, goalposts —131 прямо rest on centre of goal line. Положение каркаса следует из расположения его стоек.','Два предложения; все части привязаны к отдельным полным статьям глоссария, включая линию ворот.'),
F('endboards','93 прямо Boards at each end rink.','Местоположение концевых бортов — факт об этом подтипе.'),
F('boards','38 прямо encloses playing surface;glass rises above boards.','Оба утверждения уже в вопросе; правильная справка не добавляет нового факта.', 'PF'),
F('glass','38 описывает стекло над бортами для additional protection.','Свой факт об установке стекла; называет борта и тем самым раскрывает ключ вопроса об основании.', 'PF'),
F('cage','122 crossbar,two goalposts,net attached.','Состав ворот — собственный конкретный факт, ключа нет.')])
add(39,'Easy сохранён: функция лопасти бытовая, heel/toe — части лопасти, но не целое изогнутое рабочее звено.',[
F('stick','231 буквально curved blade carrying passing shooting.','Среди shaft/heel/blade/toe blade соответствует полной функции; ключ не встроен в prompt.'),
F('stick','231 даёт straightshaft,curvedblade иheel/toe relationship.','Два предложения; всё многосоставное описание подтверждено одним полным абзацем.'),
F('stick','231 straightshaft held by players.','Форма/хват шафта — конкретный факт о нём.'),
F('stick','231heel closest shaft.','Справка локализует пятку относительно шафта, не называет ключ.'),
F('stick','231curvedblade итри действия точны.','Повторяет все признаки вопроса и ключ; нового факта нет.', 'PF'),
F('stick','231toe furthestshaft.','Положение носка — отдельный конкретный факт о варианте.')])
add(43,'Medium сохранён: составной сравнительный признак speed+drop+gates отделяет супергигант от GS и DH.',[
F('alpine','76lowerdrop/moregates и77bothspeedevents;сопоставлены также73DH и81GS.','Все четыре дисциплины прочитаны; SG единственный удовлетворяет speed при меньшемdrop.'),
F('alpine','76 подтверждает обе сравнительные характеристики;77speed.','Два предложения, каждая часть поддержана соседними абзацами, не одним усечённым node76.'),
F('alpine','84mostgates и85bothtechnical дают Slalomtechnical.','Технический класс и ворота — предметный факт о слаломе.'),
F('alpine gs','81COC и903.1.3FIS перечисляют long medium shortturns.','Полезная характеристика GS, не раскрывает SG.'),
F('alpine','76lowerdrop и77speed подтверждены.','Повторяет сравнение и класс уже в prompt; нового факта нет.', 'PF'),
F('alpine','73DH highest speeds,greatestverticaldrop.','Конкретный факт о DH как исходной сравнительной дисциплине.')])
add(57,'Easy сохранён: парный старт и смена дорожек — узнаваемый формат, group events отделены. Связь с 058/059 — общая длинная дорожка, но формат/размер/направление разные проверяемые факты.',[
F('long','76 прямо pairs against clock иonceperlap switching.','Massstart иpursuit не pairs againstclock; shorttrack групповая борьба, ключ единственный.'),
F('long','76 содержит pairs againstclock иequalizedistance reason.','Два предложения, добавлена причина смены дорожек; обе части подтверждены.'),
F('long','76 подтверждает pairs иonceperlap.','Правильная справка полностью повторяет признаки prompt, без нового факта.', 'PF'),
F('short','67 smalleroval и72/75 group4/6 подтверждают simultaneous race.','Свой факт о меньшем овале и совместной борьбе, исправленная привязка к shorttrack.'),
F('mass long','91allcompetitors onice и75alllongtrack400m подтверждают massstart group.','Групповой формат именно massstart, не называет правильный индивидуальный.'),
F('pursuit','97Two teams ofthree simultaneous oppositesides.','Три участника и противоположные стороны — полезный факт о преследовании.')])
add(58,'Easy сохранён: групповой старт плюс малый овал внутри катка отделяют shorttrack от групповых longtrack. Нет полного дубля с 057, который проверяет пары/смену дорожек.',[
F('short long mass','67short111.12m internationalrink и72/75groups;75long400m,91massgroup на этом овале.','Совокупность размер+место+группа даёт только шорт-трек.'),
F('short long mass','67 подтверждает первый тезис;75/91longtrack подтверждают второй с massstart.','Два предложения, сравнение включает оба источника, не один shortnode.'),
F('long','76pairs againstclock для individualdistances.','Свой формат longtrackindividual; ключа нет.'),
F('short','67короткий овал international-sizedice rink.','Сверх вопроса о катке уточняется международный размер; полезно, но сильнее добавить111.12m, это предложение ещё не голое повторение.'),
F('long mass','75alllongtrack400m и91massallcompetitors.','Точная длина400m игруппа — конкретный факт именноmassstart.'),
F('pursuit','97simultaneous oppositesides для teams.','Начальные позиции команд — самостоятельный факт.')])
add(59,'Easy сохранён: одно общеизвестное направление. Варианты «стартовая дорожка»/«каждое пересечение» объясняют другую операцию и заметно слабее реального clockwise distractor.',[
F('long','76Skating counterclockwise directly.','Ключ однозначен; два неверных варианта искусственны, стоит улучшить набор без измененияEasy.', 'PF'),
F('long','76counterclockwise, change lanes, equalizedistance — три связанные части.','Два предложения, причина смены дорожек подтверждена.'),
F('long','76rightofway outside crossover подтверждает вторую часть; «противоположное» —логическое отношение направлений.','Справка о приоритете пересечения не объясняет свой вариант clockwise; первая часть отбрасывает ответ вместо полезного факта.', 'PF'),
F('long','76pairs/lanechange говорит о дорожках, но не формулирует роль стартовой дорожки. Начальная позиция следует из самого термина.','Это тавтологическая коррекция неверной гипотезы, не конкретная предметная справка.', 'PF'),
F('long','76direction+lanechange поддерживает обе части.','Правильная справка добавляет смену дорожек сверх направления, поэтому новый факт есть.'),
F('long','76counterclockwise сохраняется вместе сonceperlaplanechange; смена направления не предписана.','Факт о смене именно дорожек конкретен; не называет против часовой стрелки, прямой утечки ключа нет.')])
add(60,'Medium сохранён: специальная геометрия синхронного катания с числовыми минимальными требованиями. Wheel допускает two/three-line parallelwheel: вопрос о базовом построении minimumthree даёт Block, не о числе линий любого сложного колеса.',[
F('block shapes','43minimumthree block;44line max2,circle min3skaters,wheelspoke min2.','Четыре формы прочитаны; квалификация базового построения желательно явнее, чтобы не спутать three-lineparallelWheel.', 'PF'),
F('block shapes','43oneblockconfiguration минимумthree;44раздельные minima/maxima.','Два предложения; все три альтернативные требования привязаны к44, а не только43.'),
F('shapes','44A Circle has minimumthreeSkaters.','Конкретный минимум участников круга, без ключа.'),
F('shapes','44A Line maximumtwo lines.','Числовой максимум именноформыLine, без называнияBlock.'),
F('shapes','44A spoke minimumtwoSkaters.','Точный минимум наспицу, полезен оWheel.'),
F('block','43allSkaters formingoneblockconfiguration minimumthree.','Сверх числа линий добавлены все участники в одной конфигурации, предметный факт о единстве построения.')])
add(67,'Medium сохранён, но задача заметно легче соседних правил offside/icing: узнаётся распространённое большинство. Difficulty HOLD для координатора отдельно от истинности термина.',[
F('powerplay','221opposingteam superioradvantage afterpenalties explicitlypowerplay.','Ключ единственный, но задача только на знакомое название ситуации; Medium нуждается в отдельном согласовании/усилении, класс не изменён.', 'PH'),
F('powerplay overtime delayed','221подтверждает большинство;168overtime tie и81delayedpossession —различные ситуации.','Два предложения, отрицательное сравнение обосновано отдельными статьями.'),
F('overtime','168tie→overtime.','Конкретное условие наступления овертайма, правильный ключ не назван.'),
F('shorthanded','187short one/two duepenalties и221 противопоставление teams.','Своя ситуация меньшинства; слово большинство не названо, ответ напрямую не сообщён.'),
F('powerplay','221прямо inferior/opposing advantage powerplay.','Повтор вопроса и ключа, авторитетIIHF не добавляет содержательного факта.', 'PF'),
F('delayed','81referee notblow покаnonoffendingpossession.','Полезное условие отложенного свистка; текущая author221 привязка этого не доказывала.')])
add(68,'Easy сохранён: спортивный термин с точным числом; числа1/2/4 правдоподобны как варианты определения.',[
F('hat','135Threegoals playeronegame прямо.','Число3 иодин игрок/матч однозначны; вопрос не сообщает число заранее.'),
F('hat','135задаёт критерий числа, не обстоятельства гола; отсутствие условий —вывод из полного определения.','Два предложения; второе поясняет независимость от типа гола.'),
F('hat','2<3 логическое следствие определения, не отдельная фактическая статья о двух голах.','Справка лишь говорит «ещё не соответствует» вместо конкретного факта о своём варианте.', 'PF'),
F('emptygoal overtime powerplay hat','91emptygoal,173firstgoalOT и221powerplay подтверждают возможные ситуации;135hat считает число.','Три обстоятельства одного гола —конкретные, но заключение про хет-трик повторяет критерий вопроса, желательно оставить только собственный факт.'),
F('hat','4>3 прямо следует из определения.','Называет превышение требуемого числа, не даёт факта о четырёхголовом результате; после исключения2/4 ответ вычисляется. Нужна самостоятельная справка.', 'PF'),
F('hat','1353oneplayeronegame точно.','Все признаки уже в prompt+key; правильная справка не добавляет нового факта.', 'PF')])
add(73,'Easy сохранён: узнавание устройства освобождения ботинка по нагрузке. С 029 нет тематического дубля; 023про материал канта. Исторический вопрос о073Easy не переносится в PASS автоматически: вся текущая карточка перечитана.',[
F('binding','3.1.4.1Ski binding releasesboot prespecifiedloads прямо.','Все четыре компонента прочитаны; binding единственен по release, простой уровеньEasy оправдан.'),
F('binding interface','Release нагрузки —24binding, betweenplacement —24interface.','Два предложения; второй добавляет платформу как отдельный компонент.'),
F('binding','24release presetload подтверждает справку, но авторское note0quote было проinterfaces.','Повторяет основной вопрос и ключ; нет новой детали о креплении.', 'PF'),
F('interface','24mountedbetween skis/releasebindings прямо. Авторское note1quote проedges не соответствует полю.','Конкретное расположение платформы, правильный ответ не назван.'),
F('edge','16skisdefinition иedgeslateralforces; «основной» базовый компонент следует изcomponentA, не нормативное превосходство.','Даёт конструктивный факт именно о лыже, без названия крепления.'),
F('brake','25slowski afterbindingrelease. Авторская страница24 не содержит brake definition.','Свой факт тормоза, но явно сообщает «срабатывание крепления», раскрывая правильный механизм текущего вопроса; нужна другая деталь.', 'PF')])
add(76,'Hard не менялся. HOLD: нормативное systemweight специальное, но distractors boots/poles очевидно внешние; единственная разница ski+binding vs ski+platform+binding —простой список, нет исключения/применения правила. Нужна сверка утверждённогоHard координатором.',[
F('weight','16systemweight fullyassembled including ski,interface,binding.','Все четыре списки прочитаны; ключ нормативно единственен. Сложность списка неубедительна дляHard, вопрос нельзя сертифицировать только наличиемFIS2026.', 'PH'),
F('weight','16закрытый перечень подтверждает отсутствиеboot/poles именно вsystemweight.15assembledunit также включаетretentiondevice, но это другая дефиниция: не смешаны.','Два предложения; отрицательное членство обосновано специальнымsystemweight перечнем, не общимassembledunit.'),
F('sole boot','25boots отдельно иsolethickness definition.','Полезный факт о геометрии ботинка; не раскрывает mass list.'),
F('binding','24releasesatpresetloads.','Свой механизм крепления, безplatform иполного списка ключа.'),
F('poles','27отдельный3.3Ski poles.','Только упоминание наличия разделаFIS вместо спортивного свойства палок —метаданные источника, недостаточная полезность.', 'PF'),
F('bearing','15bearingheight bottomrunningsurface→skibootsole; авторский16quote говорил standingheight/thickness, не полный измерительныйdefinition.','Новый геометрический факт о системе лыжи; соответствует вопросу о собранной системе.')])
add(82,'Medium сохранён: зависимость стартовых отставаний от полного результата, а непромахов/временистарта. Годовую Olympic2026 область нельзя закрыть generic IBUoverview; это sourceHOLD отдельно отdifficulty.',[
F('biapursuit','190sprint top60/secondsbehindwinner подтверждает общее правилоIBU. Полный rawOlympic2026N02A получить не удалось (DNS); specific2026 не сертифицирован.','Все четыре причины прочитаны; sprintresults единственный общий ответ, словесной подсказки нет.', 'HP'),
F('biapursuit sprint','190intervalsbehindwinner и176continuousclock penaltyloop подтверждают разную роль результатов ипромахов.','Два предложения, причинная цепочка полная; Olympic2026 оговорка всё ещё зависит от полного документа.', 'HP'),
F('sprint','176individualstart30seconds.','Конкретный интервал спринта30s полезен для варианта старта.'),
F('biapursuit','190top60/timebehindwinner прямо, но genericIBU не фиксирует Olympic2026.','Сверх вопроса добавлен допускtop60, предметный новый факт.', 'HP'),
F('sprint biapursuit','176miss150mpenaltycontinuousclock,190intervalfromsprinttimes.','В неверной справке прямое указание расчёта по результату гонки раскрывает правильный ответ, убрать утечку.', 'PF'),
F('biamass','234WorldCup25+currentweek иexplicitOlympicmodifications. Авторскийnode231 —только словоPenalties ифакт не подтверждает.','Свой факт о критерияхmassstart полезен при WorldCupscope; Olympic отбор отдельно оговорён в оригинале, справка не должна читаться как Олимпийский.', 'PF')])
add(89,'Medium сохранён. HOLDdifficulty: prompt дословно определяет длину по поверхности ивариант повторяет её; фактический developedlength правильный, но словесное узнавание не Medium. Исторический089Medium сохранён какfinding, не унаследованPASS.',[
F('homology','650.3.1 прямоsurfacelength inmeters(realdevelopedlength), отдельноverticaldrop иgradient%.','Ключ «длина трассы по поверхности» повторяет prompt «протяжённость трассы по поверхности»; слабая проверкаMedium, требует нового критерия в сохранённом классе.', 'PH'),
F('homology','650.3.1раздельно surfaceinmeters,verticalinmeters,gradientpercentages.','Два предложения, все три измеряемые величины сопоставлены с собственными пунктами.'),
F('homology','Surface length expressedinmeters(real developedlength) прямо.','Повторяет определение иединицу из вопроса; новогофакта о длине нет.', 'PF'),
F('homology','650.3.1 содержитstart/finish above sea level иverticaldropinmeters; разность высот —геометрическое значениетермина.','Отличие вертикального расстояния от поверхности полезно ио своём варианте.'),
F('homology','650.3.1average/max/min gradients inpercentages. Авторскаяпривязка99width40m не соответствует крутизне.','Конкретная единица иразновидности крутизны, безутечки названиядлины.'),
F('width','902.1GS normallyapproximately40m; completeparagraph permits narrower withterrain/safety. «Обычно около» сохраняет непредельный статус.','Часть «вопрос о длине» раскрываетключ в невернойсправке ислужитметакомментарием. Оставить собственныйфакт ширины сдисциплиной.', 'PF')])
add(90,'Medium сохранён: специальный индивидуальныйcombined отличается от Olympicteam2026 (044). Question явно FISindividual, поэтому заменаOlympic event не делает его ложным.',[
F('combined sum','1101.1speedDH/SG+singleSLtwo runs;1100.4single/teampossible.','Ключ уникальный средиGS,DH,SG; individualscope явно исключает смешение044Olympicteam.'),
F('combined alpine','1101.1DH/SG+SL поддерживает состав;COC разделяет speed/technical. Фраза о проверке навыков —объяснительныйвывод издвухклассов.','Два предложения, второе добавляет смысл комбинации; вывод помечен кактолкование, не отдельнаянорма.'),
F('gs','903.1.3long/medium/shortturns прямо. Авторская109страницабылаcombined, неGS.','Предметныйфакт именноGS, безподсказкиcombined.'),
F('sum','1100.7addingracetimes, specialforms exception.','«В обычной» отражает исключениеspecialforms; способзачёта добавляет факт сверх состава.'),
F('combined','1101.1DHorsGspeedrun plusSL.','Собственныйфакт оDH допустим, но отрицательнаячасть прямо сообщает отсутствующийSL ипомогаетотброситьвариант; ключcombined не назван.'),
F('superg','1006one run physical108printed102, а неauthor109.','Количествозаездов именноSG —конкретныйфакт.')])
add(91,'Medium сохранён: точныеусловия gatepass относительнодвухtips/feet, исключениеlostski явно исключеноprompt. НеHard: требуетсяодноцентральноеусловие, а неразборисключения.',[
F('gate','661.4.1bothski tips andbothfeet;lostskiexceptionпрочитан иисключён «обе сохранены».','Совокупность4пересечений делает ключуникальным средиsubsetвариантов, нетутечки вprompt.'),
F('gate poles','661.4.1задаётtips/feet;head неупомянута ине замещаетrequiredtips.3.3polebalanceне частьgatequalification.','Два предложения; отрицательнаячасть —выводизнеобходимогоусловия, нецитатао голове.'),
F('gate','661.4.1requiresbothfeet aswellastips.','Невернаясправка «не только лыжи, но и стопы» практически собирает ключ; это коррекцияошибки вместо собственногофакта оtips.', 'PF'),
F('gate','661.4.1обаfeet вместоone поддержано.','Прямаяутечкаполногоусловияобеfeet в неверномварианте, исправить.', 'PF'),
F('gate','661.4.1.3originalgate lineafterpole removed, includingmissingturningpole.','Самостоятельноеусловие сбитойвешки добавляетфакт сверх основных4пересечений.'),
F('poles gate','27polefunctionbalance и661.4.1tips/feet; полныйнаборсвязан издвухпассажей.','Конкретныйфакт обалансе палок не относится к варианту «обе стопы, но не концы лыж»; заменяетобъяснение своего варианта другимпредметом.', 'PF')])
add(92,'Hard сохранён: специальный срокhomologation требуетзнания разныхсемейств иотличия application expiry отcertificate; prompt10years задаётсравнение, не5. Утечкаправильного числа вnote0 сохраняется.',[
F('expiry','650.5.6.1five later1July/1Nov и.2tenyearslalom;общаяvaliditycondition.3прочитана.','Обычныйсрокуточнён, всеfourчислапрочитаны; promptне сообщаетfive.'),
F('expiry','650.5.6.1fiveyearlater/1July;footnote Southern1November прямо.','Два предложения, точнаясезоннаяоговоркасохранена; обычныйсрокнеобещаетнеизменнуюvalidityприизменениитрассы.'),
F('expiry','5DH/SG и10SL/GS истинны.','Невернаясправка «два года» прямо раскрывает «пятилетний», не даётфактаодвухлетнемварианте; FIX.', 'PF'),
F('expiry','650.5.5four years afterinspection incompletework deletes pendingapplication.','Справка опускает точкуотсчёта «после инспекции» иусловиезапрошенныеработы незавершены. Добавитьих, чтобыневыглядетьчетырьмя годамиот подачи.', 'PF'),
F('expiry','650.5.6.2ten yearsSL/GS.','Конкретныйфакт именнодесятилетнегосертификата; fiveключне назван.'),
F('expiry','650.5.6.1re-homologationbefore newcertificate.','Дополнительныйфакт продлениясверхчислаfive, справка полезна.')])
add(95,'Medium сохранён, но «ловящая»→«ловить» словеснаяподсказка; требуетсяфункциональный вопрос без корняключа, а неклассEasy.',[
F('catcher','46catchorstopshotsnonstickhand.','Prompt «ловящей» дословноподсказывает «ловить»; три альтернативныезадачи явно другихпредметов, Mediumослаблен.', 'PF'),
F('catcher blocker','46nonstickcatchorstop;34stickhandblockshots.','Два предложения; каждаяперчатка имеетсвойпассаж, неавторский46 дляобеих.'),
F('blocker','34blockerwornhandholdingstick.','Конкретныйфакт оположенииблина именнона руке с клюшкой;связан с вариантомзакрыватьэтуруку.'),
F('mask','95protective maskgoalkeeper. Авторский46 был проcatcher, переадресован95.','Факт олицевоймаске соответствует варианту защитылица;правильный catcherключ нераскрывает.'),
F('catcher','46nonstick hand/catchstop подтверждаетвсё.','Добавляетположение свободнойотклюшкируки, это факт сверхpromptфункции.'),
F('stick blocker','231goalie stickprimarilydefendinggoal;34blockersideblockshots.','Собственныефакты окомплекте клюшка/блин, без catcher ключа.')])
add(97,'Medium сохранён: механикабоба иsteeringropes;словогибкая делаетпальцы/полозья/рукоятки заведомонегибкими исловесно исключаетвесьнабор. Нужнапредметнаяпереработкавтомжеклассе.',[
F('bobequip','96controlledbyropeshelddriver,frontonsteeringpin. «Тянет» —механическийвыводизropescontrol, буквальноготянетнет.','Гибкостьодногоответапротивтрёхжёсткихдеталей даётключбеззнаниябобслея;исправитьнабор/критерий.', 'PF'),
F('bobequip bobstart','96ropes/pin/front;handlesbrakeman. Буквальное «тянет» ииспользованиеhandle дляторможения подразумеваютсяфункцией, неописаниемдвижениярук.','Два предложения;источникпрямоподтверждаетсвязьрулевогоуправления, brakefunctionобычноефункциональноетолкование.'),
F('bobequip','96ropescontrolledfrontrunnersandpin.','Сверхpromptдобавленмонтажнаsteeringpin, новаяконструктивнаядеталь.'),
F('bobequip','96frontmountedpinapprox3incheslateral.','Предметныйфакт опальцах/боковомходе, нерассказываетпро правильныетросы.'),
F('bobequip bobstart','96frontcontrolleddriver;84steerthroughturns.','Факт именнопереднихполозьев иих движенияна пальце;ключropesне назван.'),
F('bobequip','96расположениеhandlesaroundbrakeman. Использованиеbraking —выводизназваниядетали.','Конкретныйчленэкипажа уhandles, полезныйфактнеошибочного«руля».')])
add(98,'Medium сохранён: расположениеуправляемойпары требуетзнанияустройства, четыреальтернативысохраняютправдоподобное количество. Пересечение с097частично: тотспрашиваеттросы, этотпереднююпару, ноихсправкивзаимноподсказывают.',[
F('bobequip','96four runners,twofrontmountedsteeringpin lateral.','Средиrear/front/all/none толькоfront соответствуетmountedpin;истинностьключаподтверждена.'),
F('bobequip','96поддерживаетfrontpins/ropes. Неутверждаетявно, чтоrearнеповорачиваютсянаэтихпальцах: описаниеfrontнеполнаякинематическаясхема.','Два предложения;убратьилиотдельнодоказатьусиленныйотрицательныйтезисозадних.', 'HP'),
F('bobequip','96four иfrontmountedpin;rearnotmounted —неполучаетпрямойдоказательности отодногоописанияfront.','Справка предметноозадних, ноотрицательноемонтажноезаявление требуетполнойсхемы/правила.', 'HP'),
F('bobequip','96twofrontmountedsteeringpinlateral прямо.','Повторяетвсёвprompt+key, новаямонтажнаядетальне добавлена.', 'PF'),
F('bobequip','96sledruns onfour highlypolishedsteelrunners.','Первыйтезисфактичен, нозаключение «фактнеопределяет» —метакомментарийотбросаварианта. Датьматериал/полировкувместологическогоотказа.', 'PF'),
F('bobstart bobequip','84steerthroughhighspeedturns,96frontlateral подтверждаютпотребностьсменынаправления.','Рассуждениепротив«ниодин» не даётсобственногофакта/условия неподвижныхполозьев;этоотрицаниеневерногоответа.', 'PF')])
add(100,'Medium сохранён, нообычнаяфункцияшиповочевидна,разницаheel/sole ещёпредметна. HOLDdifficulty дооценкикоординатором:нормативноеприменениешипов/пределпараметровлучше соответствуетMedium, классне изменён.',[
F('bobshoe bobstart','103racingshoes smallspikes solestraction,82pushstandingstart.','Ключединственныйизtractionoptions;nominalMediumспоренкак бытоваяфункцияобуви, требуетсяотдельноерешение.', 'PH'),
F('bobstart bobshoe','82первыйpushandload,103spikestraction.','Два предложения,обетехническиечастиимеютсвойpassage;BCSуказаниенеединственноедоказательствопервоготезиса.'),
F('bobshoe','103пишетsmallspikes, неsolidrubber;заявление «неописывает» —провереннаяграницапрочитанногополногоEquipmentраздела.','Вместофактаорельефнойрезинесообщаетотсутствиеупоминаниявисточнике,метаданные/выбраковка,недостаточно.', 'PF'),
F('bobshoe','103неуточняетremovable/heel: честноеописаниеграницыисточника, неотрицаниеихсуществования.','НевернаясправкаоботсутствииданныхBCSне даётполезногофактаосъёмныхпяточныхшипах.', 'PF'),
F('bobshoe','103spikesfortraction; «гладкаяне соответствует» —механическийвывод, исходникневысказываетпределыработыгладкойподошвы.','Отбрасываетвариантбезконкретнойхарактеристики/условияприменениягладкойобуви.', 'PF'),
F('bobshoe','103smallspikesonthe solestraction прямо.','Полностьюповторяетосновнойвопроси ключ, новогофактаошипахнет.', 'PF')])
# Attach exact frozen literals and independent proof bindings, field by field.
assert set(reviews)==set(pre['scopeIds'])
fields=['prompt-key','explanation','note0','note1','note2','note3'];cards=[]
for snap in pre['cards']:
 q=snap['actualCard']; rev=reviews[q['id']]; entries=[]
 literals=[{'prompt':q['prompt'],'options':[a['text'] for a in q['answers']],'correctIndex':q['correctIndex'],'key':q['answers'][q['correctIndex']]['text']},q['explanation']]+[a['note'] for a in q['answers']]
 for name,literal,reading in zip(fields,literals,rev['readings']):
  raw=canon(literal) if isinstance(literal,dict) else literal.encode()
  bindings=[b for ref in reading.pop('sourceRefs') for b in proof[ref]]
  entries.append({'field':name,'literal':literal,'literalSha256':sha(raw),'substantiveRead':True,**reading,'proofBindings':bindings,'individualAnalysis':reading['sourceAnalysis']+' '+reading['editorialAnalysis']})
 def aggregate(values):return 'HOLD' if 'HOLD' in values else 'FIX' if 'FIX' in values else 'PASS'
 source=aggregate([f['sourceVerdict'] for f in entries]);editorial=aggregate([f['editorialVerdict'] for f in entries]);overall=aggregate([source,editorial])
 cards.append({'questionId':q['id'],'wholeCardSha256':snap['wholeCardSha256'],'difficulty':q['difficulty'],'correctIndex':q['correctIndex'],'difficultyAnalysis':rev['difficultyAnalysis'],'sourceVerdict':source,'editorialVerdict':editorial,'independentVerdict':overall,'fields':entries})
from collections import Counter
counts={'cards':len(cards),'fields':sum(len(c['fields']) for c in cards),'cardVerdicts':dict(Counter(c['independentVerdict'] for c in cards)),'fieldSourceVerdicts':dict(Counter(f['sourceVerdict'] for c in cards for f in c['fields'])),'fieldEditorialVerdicts':dict(Counter(f['editorialVerdict'] for c in cards for f in c['fields']))}
receipt={'schema':'mindbattle.independent.winter30.current.v1','readerThreadId':pre['readerThreadId'],'authorThreadId':pre['authorThreadId'],'frozenCommit':'b31dc20','topicSha256':pre['topicSha256'],'hashRecipes':{k:pre[k] for k in ['canonicalRecipe','promptLiteralRecipe','otherLiteralRecipe']},'scopeIds':pre['scopeIds'],'counts':counts,'independentCertification':False,'certificationOwner':'coordinator01a12cda','cards':cards,'limitations':['PASS is field-level finding, not independent certificate for entire topic. HOLD remains unresolved; author QA is not reader certification.','Original PDF/HTML bytes preserved. pypdf extracts complete relevant physical pages; text is a derivative, not a normalized raw source.','Raw Olympic2026 biathlon description unavailable via local DNS; web-rendered text not accepted as original-byte evidence.','No card edits, full tests, build, Player, deploy, merge, OpenSpec archive or human acceptance.']}
(OUT/'independent-receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(counts))
