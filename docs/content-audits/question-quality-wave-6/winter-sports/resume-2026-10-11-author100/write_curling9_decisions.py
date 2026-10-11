"""Explicit individual editorial decisions after reading the 2026 original rules pages."""
import json
from pathlib import Path
R=Path(__file__).parent
D=[]
def f(t,a,p):
 return {'literal':t,'verdict':'PASS','substantiveRead':True,'claimAnalysis':a,'proofRefs':[['curling-2026',x-1,x-1] for x in p]}
def add(n,p,opts,ed,fs):
 assert len(fs)==6
 D.append({'questionId':f'winter-sports-{n:03}','prompt':p,'answers':opts,'verdict':'PASS','sourceTitle':'World Curling — Rules of Curling, September 2026','editorialAnalysis':ed,'fields':fs})
add(27,'В конце энда в кёрлинге два красных камня в доме ближе к центру, чем любой жёлтый. Сколько очков получают красные?', ['Ноль','Одно','Два','Три'], 'Medium: нужно применить принцип подсчёта, а не узнать название дома. Все четыре количества правдоподобны при путанице между победой в энде и числом зачётных камней. Прочитаны четыре notes; правильная добавляет, что касание дома тоже достаточно. Нет дубля с hard061 о равенстве замера.',[
f('','R12b: each own stone in/touching house closer than any opposition gives1; ровно2 по условию.',[18]),
f('Нулевой энд бывает, например, когда невозможно определить, камень какой команды ближе к центру.','R12fI blank if equal measure deciding scoring team; конкретный случай нуля.',[19]),
f('Одно очко соответствует одному зачётному камню, а не просто победе в энде.','R12b per stone not per end; уточнение единицы подсчёта.',[18]),
f('Зачётный камень может лишь касаться внешнего края дома.','R12b in or touching; glossary biter outer edge; полезное дополнительное условие.',[18,58]),
f('Три очка требуют трёх своих зачётных камней, расположенных ближе любого камня соперника.','Применение per stone R12b к3; не приписывает условию третий камень.',[18]),
f('Красные получают два очка — по одному за каждый из двух камней. В кёрлинге считают все свои камни в доме или касающиеся его, которые ближе к центру, чем любой камень соперника.','Два предложения; оба включают house и comparison, не считает все камни просто в доме.',[18])])
add(61,'По правилам World Curling 2026 года даже замер не различил расстояния до ближайших камней двух команд. Как засчитывают энд?', ['Без очков обеим командам','По одному очку каждой команде','Очко команде с последним броском','Энд переигрывают'], 'Hard: точное исключение R12fI, а не старое элементарное определение дома. Четыре разные правдоподобные процедуры разрешения равенства. Условие касается выбора команды-победителя энда, не дополнительных очков. Все notes прочитаны; правильная раскрывает отличие от равенства при подсчёте дополнительных очков.',[
f('','R12fI if deciding which team scored and no decision visually/device, blank; nearest stones specified.',[19]),
f('При равенстве, влияющем лишь на дополнительные очки, уже лежащие ближе камни всё же засчитывают.','R12fII closer stones count; отдельное правило, не повтор blank.',[19]),
f('Очки за один энд получает только команда с камнями ближе всех камней соперника.','R12b excludes both teams each one; neither has closer in tie.',[18]),
f('Последний камень энда называют «хаммером», но сам по себе он очка не даёт.','Glossary Hammer + R12b scoring location, not delivery order.',[60,18]),
f('Переигровку назначают, если внешняя сила сдвинула камни, определявшие, какая команда набрала очки.','R12gI concrete replay case; do not confuse equal measure.',[19]),
f('Энд засчитывают без очков обеим командам. Равный замер не даёт преимущества команде, бросавшей последней.','R12fI explicit blank, hammer unrelated; два предложения.',[19])])
add(62,'В кёрлинге энд начала не та команда; ошибку заметили после второго камня. Что предписывают правила World Curling 2026 года?', ['Переиграть энд с начала','Продолжить энд без исправления','Убрать только второй камень','Сменить право первого броска в следующем энде'], 'Hard: нужно различить момент обнаружения по R5mI/II. Варианты все процедурные, без шуток. Прочитаны четыре notes; правильная добавляет контраст первого камня. Primary fact не повторяет подсчёт очков или no-tick.',[
f('','R5mII after2nd play continues as if error had not occurred.',[12]),
f('Энд переигрывают, если неверную очередь первой команды обнаружили после единственного сыгранного камня.','R5mI exact earlier detection case.',[12]),
f('Если сыгран только первый камень, та же ошибка требует переигровки.','R5mI extra boundary condition to key2nd; не повтор correct action.',[12]),
f('Удаление второго камня предусмотрено, когда одна команда ошибочно выполнила два броска подряд.','R5lI with other restoration; note states removal provided not entire sanction.',[12]),
f('В смешанных парах после обычного нулевого энда решение о расстановке получает команда, бросавшая первой.','R17gIII explicitly обычный zero contrasting equal-measure exception; actual related nextend right.',[27]),
f('После второго сыгранного камня энд продолжают как обычно. Правило специально различает обнаружение ошибки после первого и после второго камня.','R5mI/II exactly,2sentences.',[12])])
add(63,'Камень в кёрлинге остановился до полного пересечения дальней хог-линии, но перед этим задел другой камень. Как поступают по правилам World Curling 2026 года?', ['Удаляют в любом случае','Возвращают на исходную позицию','Оставляют в игре','Повторяют бросок'], 'Hard: исключение к норме о коротком камне R2f; ограничено причиной, прочих нарушений в условии нет. Четыре последовательные глагольные подписи. Notes не служат отрицательными заглушками: называют иные конкретные случаи.',[
f('','R2f except when strikes another stone then remains; exactly exception.',[7]),
f('Камень, остановившийся до полного пересечения дальней хог-линии без такого столкновения, удаляют.','R2f ordinary short stone removal.',[7]),
f('Прежние позиции восстанавливают, например, после раннего выбивания чужого камня из зоны свободных защитников.','R6b before6th restored stones nonoffender; distinct explicit restoration.',[12]),
f('Если камень полностью пересечёт заднюю линию дома, его удаляют независимо от этого исключения.','R2g separate boundary removal; adds specific fact to key.',[7]),
f('Повторный бросок можно выбрать, если во время выполнения от камня полностью отделилась ручка.','R2e player option redeliver after restoration.',[7]),
f('Камень оставляют в игре: столкновение с другим камнем образует исключение из правила дальней хог-линии. Без такого столкновения слишком короткий камень пришлось бы удалить.','R2f no overgeneralization to back/side line;2sentences.',[7])])
add(64,'В смешанных парах энд обнулили из-за равного замера ближайших камней. Кто выбирает начальную расстановку следующего энда по правилам World Curling 2026 года?', ['Та же команда, что выбирала её ранее','Команда, бросавшая первой','Команда, бросавшая последней','Победитель нового предварительного замера'], 'Hard: R17gIII exception from ordinary blank-end procedure; prompt tells blank outcome so not duplicate061. All four plausible rights holders, long options balanced. Notes distinguish LSD, first/last delivery and placement decision.',[
f('','R17gIII equal measure decision placement shall not change nextend.',[27]),
f('В первом энде право выбора расстановки определяют предварительными бросками Last Stone Draw.','R17gI lesserLSDdistance obtains choice; additional fact not answer repetition.',[27]),
f('После нулевого энда без равного замера выбор обычно получает команда, бросавшая первой.','R17gIII ordinaryblank exceptqualifier explicit.',[27]),
f('Предустановленный камень этой команды расположен в доме, в позиции B.','R17i Bsecond and alternatingdeliveredstones MD5each -> lastteamsecond; source26 B belongs laststone explicit.',[26,27]),
f('Last Stone Draw определяет выбор перед первым эндом, а не заново после каждого нулевого.','R17gI vsIII scope firstend precise.',[27]),
f('Право выбора остаётся у прежней команды. Для нулевого энда из-за равного замера действует исключение из обычного порядка смешанных пар.','R17gIII exact2sentences.',[27])])
add(85,'До шестого камня энда в обычном командном кёрлинге выбили чужой камень из зоны свободных защитников за пределы игры. Что требуют правила World Curling 2026 года?', ['Удалить брошенный камень и восстановить сдвинутые','Оставить новую расстановку без изменений','Переиграть весь энд с начала','Засчитать сопернику одно очко'], 'Hard: boundary before6th and opposition FGZ removal matter. All options sanction procedures. Notes read individually; rule position not vague guard definition. Отличается от086: здесь out-of-play обязательное восстановление, там off-centre inplay право выбора.',[
f('','R6b before6th outofplay opposition FGZ removed delivered and restoreall.',[12]),
f('Зона свободных защитников лежит между ти-линией и хог-линией и не включает дом.','R6a exact area; adds to sanction.',[12]),
f('При нарушении no-tick соперник может сохранить расстановку, если защитный камень остался в игре.','R7a optionII;R7b outofplayR6. Excludesoutofplay explicitly.',[12,13]),
f('Энд переигрывают, если нарушение двух бросков одной команды подряд заметили уже после следующего камня.','R5lII concrete replaycase.',[12]),
f('Обычные очки считают после энда по камням в доме, расположенным ближе камней соперника.','R12b describes actual point mechanism, no fictitious penaltypoint.',[18]),
f('Брошенный камень удаляют, а все сдвинутые возвращают на прежние места. По правилу зоны свободных защитников восстановлением занимается команда, не нарушившая правило.','R6b delivered removal + nonoffendingrestores;2sentences.',[12])])
add(86,'В обычном кёрлинге до шестого камня чужой защитник сдвинут с центральной линии, но остался в игре и в зоне защитников. Какой выбор даёт сопернику правило no-tick World Curling 2026 года?', ['Только переигровку всего энда','Восстановить позиции с удалением брошенного камня либо оставить их','Только повтор того же броска','Одно штрафное очко либо право последнего броска'], 'Hard: specific nonmandatory restoration underR7a; explicit sameFGZ inplay avoidsR6b. Answer1 longer due two legally precise choices but distractor3 also two choices; correctness comes from rule detail. Four notes separate actual alternatives/cases. Could simplify wording later but no ambiguity found.',[
f('','R7aI/II options remove+restore ORleave;R7b nottriggered sinceinplay.',[12,13]),
f('Переигровка энда применяется при некоторых ошибках очереди, например при неверном первом броске, замеченном сразу.','R5mI afteronly1 firststone replay concrete.',[12]),
f('Правило no-tick не применяется в смешанных парах и кёрлинге на колясках.','R7c exact extra fact.',[13]),
f('Право повторить бросок возникает, например, при полном отделении ручки во время выполнения.','R2e optionalredelivery concrete differentcase.',[7]),
f('Правило no-tick предлагает выбор положения камней; штрафного очка или передачи последнего броска в нём нет.','R7a exhaustive twochoices; identifies specificconfusedright notempty negative.',[12]),
f('Соперник выбирает между восстановлением прежних позиций с удалением брошенного камня и сохранением новой расстановки. Если бы защитник вышел из игры, применялось бы другое правило — обязательное восстановление по зоне свободных защитников.','R7aandb +R6b;2sentences.',[12,13])])
add(87,'В смешанных парах команда сохранила неиспользованный пауэр-плей до дополнительного энда. Можно ли применить его там по правилам World Curling 2026 года?', ['Можно, если команда бросает первой','Можно, если соперник согласен','Нельзя даже при неиспользованном праве','Можно только в первом дополнительном энде'], 'Hard: exception specific to MDpowerplay versus oneuse/game. All answers are plausible conditional eligibility statements, no random entities. Correctnote describes actual positional effect, not merely repeats forbidden.',[
f('','R17fIII cannotusedextraends categorical despiteoncepergame.',[26]),
f('В обычном энде пауэр-плей выбирает команда, имеющая право решения о начальной расстановке.','R17fIII placementdecision not firstthrow alone.',[26]),
f('В правилах право пауэр-плея связано с выбором расстановки, а не с согласием другой команды.','R17fIII exhaustivewho + no consentcondition; named confusedright.',[26]),
f('При пауэр-плее два предустановленных камня располагают с одной стороны площадки.','R17fIII B either side A same side; adds effect.',[26]),
f('Дополнительные энды играют при равном счёте до первых набранных очков.','R12a tied extrasteamfirstscoreswins; explains extraendnotuse.',[18]),
f('В дополнительном энде пауэр-плей запрещён. Это ограничение действует даже тогда, когда команда ещё не использовала свою единственную возможность за игру.','R17fIII oncepergameandcannotextras;2sentences.',[26])])
add(88,'В смешанных парах третьим камнем энда случайно выбили свой предустановленный камень. Как поступают по правилам World Curling 2026 года?', ['Засчитывают сопернику одно очко','Оставляют всё: выбит свой камень','Повторяют энд с начальной расстановки','Удаляют брошенный камень и восстанавливают сдвинутые'], 'Hard: MD before4th protects any previousdelivered ORplaced includingown, unlike ordinaryFGZ. Timing third and ownership/preset each essential. All options plausible resolutions; no duplicate085 because distinctMDownstone exception and threshold.',[
f('','R17e before4th anypreviousdelivered/placed removed =deliveredremovedrestore. Thirdqualifies;ownnotexcepted.',[25]),
f('В смешанных парах предустановленные камни могут приносить обычные очки при подсчёте после энда.','R17b eligibleplacedstones, notpenaltyaward; concrete relatedscoring.',[25]),
f('Ранняя защита смешанных пар распространяется на любые ранее сыгранные или предустановленные камни.','R17e any meansownincluded; identifies misconception.',[25]),
f('Переигровка предусмотрена при ошибочной начальной расстановке, замеченной после первого броска.','R17hI specific replaycase.',[27]),
f('Восстанавливать позиции после этого нарушения должна команда соперника.','R17e nonoffendingteam restoration additionalactor.',[25]),
f('Брошенный камень удаляют, а сдвинутые возвращают на прежние места. До выполнения четвёртого камня в смешанных парах нельзя таким образом выбивать даже собственный предустановленный камень.','R17e before4th anyown explicitinference,2sentences.',[25])])
(R/'curling9-decisions.json').write_text(json.dumps({'role':'author','cards':D},ensure_ascii=False,indent=2)+'\n')
