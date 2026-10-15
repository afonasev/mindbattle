import json,hashlib,pathlib,itertools,datetime
R=pathlib.Path.cwd(); O=R/'docs/content-audits/question-quality-wave-8/coordinator-01a13f31/independent-books8-initial'
P=R/'docs/content-audits/question-quality-wave-8/process-v2-books1-20-01a13f31/author1-10/partial-ready'
C=R/'docs/content-audits/question-quality-wave-8/coordinator-01a13f31'
def read(p):return json.loads(p.read_text())
def digest(x):return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def save(n,x):(O/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
qs=read(R/'src/content/topics/books-publishing.json')['questions']; applied=read(C/'apply-books8-initial.json'); sourceindex=read(P/'source-index.json')['sourceEntries']; candidates=read(P/'candidate.json')['entries']
orders=[1,2,3,6,7,8,9,10]
for a in applied['applied']:
 q=qs[a['sourceOrder']-1];assert q==a['proposedCard'] and digest(q)==a['proposedSHA256']
# These grounds are independently written from personally read retained primary passages.
S={}
limits={
'ingram-cover':'Returned windows omit unrelated page portions, including some book-format discussion. Binding options L44-72 and complete front/back/spine design sections L222-254 are present. They establish Ingram configurations, not every binding in existence. Protection is grounded separately in Bodleian L79.',
'bodleian-binding':'Complete endpaper/marbled-paper passage L85-100; leaf location and decorative examples are explicit. It is not a universal taxonomy of preliminary pages.',
'loc-ebooks':'Relevant main explanatory body L10-14 is complete; L21-27 adds catalog/search caveats. Device/file compatibility is qualified, not a claim that every format has every feature.',
'bodleian-bindings-overview':'L79 contains the complete functional sentence about thread, glue, outer covers and stable/protected textblock; L101-104 supplies binding choice context. Earlier introduction and most pictures are absent, but no condition in this functional claim is cut.',
'ingram-pocket-guide':'Complete three-item Cover Styles discussion L2435-2468 with its limiting introduction (three styles used by many publishers). These examples cannot establish that ALL paperbacks are perfect-bound. Cover-wrap context L2398-2424 is also retained.',
'ciep-workflow':'Full concept-to-publication sequence L32-63 is retained. Development L44-46 precedes copy-editing L51-53; layout includes role overlap at L57. Not a claim of exclusive job boundaries.',
'ciep-glossary':'Complete relevant definitions retained: copy L84, copyediting L85-86, endpapers L117, preliminary pages L231, proof/proofreading/against-copy L234-239. This proves listed inclusion of title pages, not exclusion of every other front leaf.',
'ciep-proofreader':'Full limitation paragraph L60 and sequencing paragraphs L64-67 are retained, including unless-briefed exception and non-book work. They support usually/normally rather than absolute prohibitions.',
'loc-audiobooks':'Entire 42-line viewer output, including complete informational body L9-23. Human/synthetic narration explicit; LoC How-to-read L12 separately supports MP3 prevalence.'}
for key,e in sourceindex.items():
 path=R/e['path'];h=hashlib.sha256(path.read_bytes()).hexdigest();assert h==e['sha256']
 S[key]={'key':key,'path':str(path),'rawReadSHA256':h,'url':e['url'],'locator':e['ref']+' '+e['locator'],'personalReadEvidence':limits[key],'limitations':'Shared returned public web.open output, not an independent HTTP body per URL. '+limits[key]}
def loc(key,l):return {'sourceKey':key,'path':S[key]['path'],'url':S[key]['url'],'locator':l}
cover=[loc('ingram-cover','turn4view2 L222-242'),loc('bodleian-bindings-overview','turn4view3 L79')]
spine=[loc('ingram-cover','turn4view2 L252-254')]
title=[loc('ciep-glossary','turn6view0 L231')]
end=[loc('ciep-glossary','turn6view0 L117'),loc('bodleian-binding','turn4view0 L85-100')]
hard=[loc('ingram-cover','turn4view2 L51-72')]
soft=[loc('ingram-pocket-guide','turn6view3 P108 L2435-2450'),loc('ingram-cover','turn4view2 L51,L68')]
ebook=[loc('loc-ebooks','turn4view1 L10-13')]
audio=[loc('loc-audiobooks','turn7view0 L9-23')]
workflow=[loc('ciep-workflow','turn6view1 L44-60')]
proof=[loc('ciep-glossary','turn6view0 L234-239'),loc('ciep-proofreader','turn6view2 L58-67')]
typeground=[loc('ciep-glossary','turn6view0 L84,L237')]
# Per-card grounds: main, explanation, then each individual option's status/reason and own-note claim.
D={
1:{'status':'FIX','main':'Обложка — внешняя оболочка из передней/задней сторон и корешка; Bodleian прямо связывает outer covers с защитой блока. Корешок — её часть, а титул и форзац — внутренние элементы, поэтому по всему блоку ключ 0 единственный. Но основной факт воспроизводит generic cover identification в anime-manga-manga-cover: manga не меняет конструкцию или связь; нужен независимый MAIN-факт.', 'mainLoc':cover+spine+title+end,'ex':'Два предложения: защитная функция подтверждена Bodleian L79; состав внешнего комплекта прямо дан Ingram L242. Прямо назван ключ. В source.url стоит дизайн-страница, а прямое основание именно защиты находится в companion Bodleian; при замене MAIN выбрать точный поддерживающий URL.', 'exLoc':cover,
'opts':[
('Единственный целый внешний защитный комплект; конкурирующий корешок лишь его часть.','Состав из передней/задней сторон и корешка прямо дан Ingram L222,L242; это дополнительное собственное устройство обложки сверх функции защиты.',cover),
('Правдоподобный внешний элемент, но закрывает корешковую сторону, а не весь блок.','Видимость на полке и порядок названия/автора прямо даны Ingram L252-253.',spine),
('Внутренняя страница книги, не внешняя защитная оболочка.','CIEP L231 явно относит title pages к preliminary pages перед основным текстом.',title),
('Близкий конструктивный элемент соединения, но внутренний лист не защищает блок целиком.','CIEP L117 прямо говорит о соединении обложки и страниц; Oxford L90-91 описывает мраморные форзацы.',end)],
'level':'easy обоснован для широкой взрослой читающей аудитории: защитная обложка — повседневный предмет; термины соседей тематически уместны. Дефект здесь — повтор MAIN, не уровень.',
'extra':'Собственный дополнительный факт: состав обложки из трёх частей; Ingram L222,L242.',
'defects':[{'code':'MAIN_DUPLICATE','field':'prompt_ordered_answers_key','detail':'В anime-manga-manga-cover основной вопрос тоже идентифицирует внешнюю обложку книги; слово «манга» лишь ограничивает вид издания. Текущая карточка меняет признак идентификации на защиту, уже содержащуюся в том же определении/объяснении соседа; отдельного конструктивного или культурного факта нет.','action':'Один адресный авторский цикл: независимый MAIN-факт с frozen ID/topic/difficulty/key, затем проверка затронутой пары.'}]},
2:{'status':'PASS','main':'На тесно заполненной полке корешок первым виден читателю и несёт название/автора (Ingram L252-253). Титул и форзац скрыты внутри; целая обложка шире искомой узкой части. Обычно сохраняет исключения для витринной выкладки.','mainLoc':spine+title+end+cover,'ex':'Два предложения прямо называют корешок и перечисляют название/автора/знак издательства ровно по Ingram L252-253.','exLoc':spine,
'opts':[
('Ключ 0: именно spine показывается при обычной полочной расстановке.','Зависимость ширины от количества страниц прямо сформулирована Ingram L253-254, дополнительно подтверждена Pocket Guide L2421-2424.',spine+[loc('ingram-pocket-guide','turn6view3 P107 L2421-2424')]),
('Титул несёт название внутри книги, поэтому тематически близок, но обычно не виден у стоящей закрытой книги.','Принадлежность title pages к предварительным страницам до текста прямо дана CIEP L231.',title),
('Форзац — видимый при открытии лист, а не наружная сторона полочной книги.','Oxford L90-91 прямо приводит marbled endpapers; CIEP L117 разрешает декоративные papers.',end),
('Обложка может нести те же сведения, но вопрос о части, обычно обращённой наружу, уточняет корешок.','Ingram L242 даёт три части, L234 — название на front cover; дополнительный факт собственной обложки.',cover+[loc('ingram-cover','turn4view2 L234')])],
'level':'easy: большинство взрослых, пользующихся обычными книгами/библиотекой, узнаёт корешок по видимой на полке стороне; ни типографская технология, ни регулярное погружение не нужны.',
'extra':'Зависимость ширины корешка от числа страниц, отсутствующая в prompt/key; Ingram L253-254.', 'defects':[]},
3:{'status':'FIX','main':'CIEP L231 явно включает title pages в prelims. Однако формулировка лишь повторяет категорию страниц до текста и не задаёт различительного признака титула; «Форзац» тоже физически находится перед текстом, а обложка/корешок вообще не страницы. Сохранённая дефиниция front matter не даёт исчерпывающего исключения форзаца.','mainLoc':title+end+cover,'ex':'Включение титула в front matter и перечень иных материалов соответствуют CIEP L231. Два предложения прямо называют ключ, но не устраняют недостающий признак и слабые альтернативы.','exLoc':title,
'opts':[
('Титульный лист подтверждён как член prelims, но тестирует редакторскую классификацию без определения самого листа.','Перечислены содержание/предисловие/список иллюстраций — верные факты о других предварительных частях; нового собственного факта о титульном листе сверх его принадлежности к этой группе нет.',title),
('Форзац — бумажный лист перед текстом; источник описывает его конструкцию, но не даёт полного категориального исключения из подразумеваемых «страниц до текста».','Соединение cover/inside pages и иногда декоративное исполнение прямо даны CIEP L117.',end),
('Обложка — весь внешний комплект, не страница prelims; ответ исключается категорией ещё до знания титульного листа.','Состав cover package прямо дан Ingram L242.',cover),
('Корешок не страница; категориальное исключение делает этот дистрактор слабым.','Название/автор и зависимость ширины от page count прямо даны Ingram L252-254.',spine)],
'level':'Точная принадлежность к издательской front matter — скорее medium; текущая лёгкость получена от заведомо нестраничных альтернатив, что не подтверждает easy. Для frozen easy нужен общеизвестный отличительный признак титула и правдоподобные альтернативы.',
'extra':'FAIL: note0 добавляет только факты о других членах той же группы; собственного свойства титула beyond prompt/key нет.',
'defects':[{'code':'WEAK_CATEGORY_AND_KEY_DISCRIMINATOR','field':'prompt_ordered_answers_key','detail':'Вопрос спрашивает страницу, но обложка и корешок не страницы; форзац также предшествует тексту. CIEP L231 даёт включение title pages, а не исчерпывающую границу, на которой строится исключение форзаца.','action':'Сформулировать собственный узнаваемый признак титула, дать однокатегорийные альтернативы и первичное основание единственного ключа.'},{'code':'CORRECT_NOTE_NOT_OWN_EXTRA_FACT','field':'note0','detail':'Содержание/предисловие/список иллюстраций описывают другие prelims; сама принадлежность титула к prelims уже спросилась.','action':'Добавить подтверждённый собственный факт титула beyond revised prompt/key.'}]},
6:{'status':'FIX','main':'Pocket Guide P108-109 различает бумажную мягкую обложку и hardback case в ткани/ламинации/суперобложке; ключ 1 верен. Но у всех трёх неверных ответов буквально написано «твёрдый переплёт», а вопрос противопоставляет гибкое жёсткому: ответ получается по словам без знания конструкции.','mainLoc':soft+hard+[loc('ingram-pocket-guide','turn6view3 P108-109 L2451-2468')],'ex':'Два предложения называют мягкую обложку и правильно отличают бумажный cover wrap от hardened cover material ткани/ламинации в Pocket Guide.','exLoc':soft+[loc('ingram-pocket-guide','turn6view3 P108-109 L2451-2468')],
'opts':[
('Суперобложка сама бумажная, поэтому форма близка, но ярлык «твёрдый переплёт» уже отвечает на отрицание в prompt.','Ingram L53 даёт hardcover with/without dust jacket, Pocket Guide L2451-2460 описывает отдельную оборачивающую бумажную оболочку.',hard+[loc('ingram-pocket-guide','turn6view3 P108 L2451-2460')]),
('Ключ 1 подтверждён бумажным cover-weight stock, огибающим страницы; но мягкий/твёрдый в самих ярлыках делает выбор тривиальной антонимией.','Плотная бумага и покрытие от царапин/отпечатков прямо даны Pocket Guide L2440-2444.',soft),
('Реальная разновидность переплёта, но слово «твёрдый» исключает её по условию без предметного знания.','Case laminate: cover wrap glued to hardback, gloss/matte coating; Pocket Guide L2461-2468.',[loc('ingram-pocket-guide','turn6view3 P109 L2461-2468')]),
('Ткань могла бы запутать по гибкости внешнего материала, но маркировка «твёрдый» снимает даже это рассуждение.','Cloth skin glued to hardback cover прямо дан Pocket Guide L2451-2453.',[loc('ingram-pocket-guide','turn6view3 P108 L2451-2460')])],
'level':'Основное различие мягкого/твёрдого известно широкой взрослой читающей аудитории и подходит easy. Текущие варианты не проходят требование разумно правдоподобных альтернатив: все неверные уже называют отвергнутое свойство.',
'extra':'Покрытие плотной бумаги защищает от царапин — собственный дополнительный факт мягкой обложки, Pocket Guide L2440-2444.',
'defects':[{'code':'LABEL_SHORTCUT_DISTRACTORS','field':'prompt_ordered_answers_key','detail':'Три неверных варианта прямо названы твёрдыми, prompt требует не жёсткие крышки; key единственный со словом «мягкой». Незнающему не нужно различать способы переплёта.','action':'Один адресный цикл: сохранить key/level, переработать prompt/названия альтернатив, чтобы выбор не решался антонимами в ярлыках; перепроверить MAIN с actual5 и технологическими соседями.'}]},
7:{'status':'FIX','main':'LoC L10-13 описывает чтение e-books на компьютере/планшете/смартфоне/ридере и совместимость файлов. Печатные soft/hardback — материальные исполнения, аудиокнига воспринимается слухом; электронная книга единственный ключ текстового чтения файла на экране.','mainLoc':ebook+hard+soft+audio,'ex':'Два предложения прямо называют электронную книгу, устройство/ПО и примеры PDF/TXT; LoC L10-13 подтверждает все эти утверждения с условием совместимости.','exLoc':ebook,
'opts':[
('Твёрдый переплёт — физический вариант издания, не цифровой файл; близкий формат книги.','Возможность с суперобложкой и без неё буквально дана Ingram L53.',hard),
('Мягкая обложка — физический вариант, не читаемый экранный файл.','NOTE OVERGENERALIZATION: Ingram L51,L68 описывает perfect-bound продукцию, Pocket Guide L2435-2450 — три выбранных стиля. Эти контексты не доказывают склеивание для любой мягкой обложки. Нужно «при клеевом бесшвейном скреплении» либо «часто».',soft),
('Ключ 2: собственно e-book как экранное чтение цифрового текста; даже если audiobook — файл, его не читают как текст на экране.','LoC L10-13 прямо требует совместимого устройства/формата и при необходимости приложения; это собственный дополнительный факт сверх цифровой формы.',ebook),
('Аудиокнига тоже бывает цифровой, поэтому разумный дистрактор, но «читают ... на экране» отличает визуальное чтение от прослушивания.','LoC Audio Books L9,L22 прямо перечисляет human/voice synthesizers и human/computer-read.',audio)],
'level':'easy: электронные книги широко знакомы взрослым пользователям смартфонов и читателям; цифровое визуальное чтение отличается от бумажной формы и прослушивания без регулярного погружения.',
'extra':'Совместимость устройства/программы с форматом файла (LoC L10-13) — дополнительное условие чтения, не простое повторение экрана.',
'defects':[{'code':'UNQUALIFIED_BINDING_GENERALIZATION','field':'note1','detail':'«В мягкой обложке бумажная крышка склеивается ...» переносит perfect-bound конфигурацию на весь формат. Сохранённый контекст ограничен примерами/продуктовой линейкой.','action':'Квалифицировать клеевой способ, используя уже сохранённый источник; не менять основной e-book факт.'}]},
8:{'status':'PASS','main':'LoC Audio Books L9-23 прямо рассматривает чтение вслух людьми/синтезатором. Audio rendition соответствует аудиокниге; остальные варианты — печатные или экранные текстовые исполнения. Electronic file сам по себе не делает произведение аудиокнигой.','mainLoc':audio+ebook+soft+hard,'ex':'Два предложения прямо называют аудиокнигу. Люди/синтезатор поддержаны Audio Books L9,L22; популярность MP3 отдельно дана How-to-read L12.','exLoc':audio+[loc('loc-ebooks','turn4view1 L12')],
'opts':[
('Мягкая обложка — печатное исполнение; не задаёт звуковую запись текста.','Соединение страниц и бумажной крышки у корешка дано Ingram L68/Pocket Guide L2445-2450; note не утверждает здесь обязательность именно клея для всех мягких книг.',soft),
('Электронная книга близка как цифровое исполнение; формулировка звуковое отличает audiobook от визуального чтения.','LoC L12 перечисляет PDF, TXT, web browser formats — note корректно сообщает возможные формы, не все форматы сразу.',ebook),
('Ключ 2: произведение передано голосом, а не печатным/экранным текстом.','Авторы, актёры, волонтёры, синтезаторы прямо перечислены LoC Audio Books L9; конкретные исполнители — новое собственное свойство beyond звучащей формы.',audio),
('Hardback обозначает печатную конструкцию, а не звуковое исполнение.','Hardcover with/without jacket прямо дан Ingram L53.',hard)],
'level':'easy: аудиокниги и понятие голосового исполнения широко распространены среди взрослых. Все ответы — реальные формы книги; цифровое текстовое исполнение даёт содержательную близкую альтернативу.',
'extra':'Авторы/актёры/волонтёры/синтезированный голос — конкретные виды исполнителей, не только повтор «звуковое исполнение»; LoC Audio Books L9.', 'defects':[]},
9:{'status':'FIX','main':'CIEP Development L44-46 прямо описывает hands-on editorial input, cut/moved text before copy-editing L51-53. Ключ редактор; верстальщик/дизайнер работают с формой страницы, корректор с готовыми proofs. Речь о роли, а не эксклюзивном запрете специалисту совмещать задачи.','mainLoc':workflow+typeground+proof,'ex':'Первое предложение верно по Development L44-46. Второе ошибочно переводит copy-editing/line-editing как «копирайтинг»: источник L51-53 говорит о редактировании рукописи, а не создании рекламных текстов. Нужно «языковое/литературное редактирование».','exLoc':[loc('ciep-workflow','turn6view1 L44-53')],
'opts':[
('Верстальщик тематически близок, но его функция — размещение уже подготовленного текста и proofs, не раннее содержание.','CIEP copy L84 отправляет edited content typesetter/designer для finalised version/proofs; L237 подтверждает supplying a proof.',typeground),
('Корректор работает с текстом поздно, а prompt явно задаёт ранний этап.','CIEP proofreading L238 и workflow L58-60 подтверждают проверку свёрстанного финального текста перед publication.',proof+workflow),
('Книжный дизайнер меняет визуальную форму, не авторское содержание; роль может пересекаться с layout, но это не задача ранней редакторской переработки.','Layout design CIEP L55-57 описывает laying out/cutting/fitting text в InDesign; glossary L84 связывает designer с finalised proofs.',workflow+typeground),
('Ключ 3: раннее участие editorial input с перестановкой/сокращением частей прямо дано Development.','Adapted for clearer expression прямо дано L46 — собственное добавление языковой ясности сверх содержания/порядка частей в prompt.',[loc('ciep-workflow','turn6view1 L44-46')])],
'level':'easy допустим по широкой взрослой грамотной аудитории: редактор помогает автору с содержанием; остальные книжные профессии связаны с визуальной/финальной стадией. Последовательность уточняет знакомую роль, не спрашивает специальное имя developmental editing.',
'extra':'Редактор на development также адаптирует формулировки для ясности, CIEP L46; это не уже названные перестановка/содержание.',
'defects':[{'code':'COPYEDITING_MISTRANSLATED','field':'explanation','detail':'Второе предложение называет copy-editing «копирайтингом», хотя CIEP L51-53 описывает редактуру языка/точности/стиля. Это другая деятельность.','action':'Заменить термин на корректное русское название языкового редактирования в одном адресном цикле.'}]},
10:{'status':'PASS','main':'CIEP L239 определяет proofreading against copy как проверку внесения всех corrections copyeditor; L238 включает typesetting errors. Ключ корректор; editor готовит copy, typesetter выдаёт proof, designer макет. Формулировка задаёт именно контроль, не внесение исправлений верстальщиком.','mainLoc':proof+typeground+workflow,'ex':'Два предложения прямо называют корректора, контроль ошибок/отмеченных исправлений и финальную стадию. CIEP L238-239 и What is proofreading L65-66 подтверждают порядок после editing/design.','exLoc':proof,
'opts':[
('Редактор тематически близок и сам может корректировать, но в указанной роли готовит исходную copy; специальная заключительная сверка — proofreading.','Workflow L51-53 прямо даёт consistency/readability при подготовке manuscript.',[loc('ciep-workflow','turn6view1 L51-53')]),
('Дизайнер работает с макетом, поэтому ошибки визуальной страницы близки, но заключительная вычитка — отдельная функция.','Workflow L55-60 и What is proofreading L65 дают design before proofreading; не утверждается невозможность совмещения одним человеком.',workflow+proof),
('Верстальщик принимает copy и создаёт proof, что делает его близким, но контролирующая сверка против copy — роль proofreader.','Glossary copy L84 и proofing L237 прямо описывают создание finalised version/proofs typesetter/designer.',typeground),
('Ключ 3: отмечает ошибки в proof и сверяет внесение исправлений copyeditor; это точное определение L238-239.','What is proofreading L60 говорит unless briefed not altering writing style/moving paragraphs; «обычно» сохраняет исключение и даёт собственный новый предел роли.',proof)],
'level':'easy допустим: поиск опечаток в готовой книге — знакомая взрослой грамотной аудитории роль корректора. Уточнение сверки исправлений не требует знания названия отдельного процесса against-copy; альтернативы — реальные смежные профессии.',
'extra':'Обычно не переписывает стиль/не переставляет абзацы — собственный предел компетенции сверх проверки proofs; CIEP L60 с сохранённым unless-briefed исключением.', 'defects':[]}
}
entries=[]
for order in orders:
 q=qs[order-1];d=D[order];gr=[]
 literal={'prompt_ordered_answers_key':{'prompt':q['prompt'],'answers':[a['text'] for a in q['answers']],'correctIndex':q['correctIndex']},'explanation':q['explanation'],**{'note'+str(i):a['note'] for i,a in enumerate(q['answers'])}}
 for group,value in literal.items():
  if group=='prompt_ordered_answers_key':ground,locations=d['main'],d['mainLoc']
  elif group=='explanation':ground,locations=d['ex'],d['exLoc']
  else:_,ground,locations=d['opts'][int(group[-1])]
  gr.append({'group':group,'literal':value,'canonicalSHA256':digest(value),'individualGround':ground,'sourcesLocators':locations})
 variants=[]
 for i,a in enumerate(q['answers']):
  reason,note,locations=d['opts'][i];tr={'prompt':q['prompt'],'answer':a['text'],'note':a['note']}
  variants.append({'slot':i,**tr,'tripleCanonicalSHA256':digest(tr),'grammar':'Прочитан весь prompt с этим ответом: вопросительное '+('«кто» допускает самостоятельное название профессии в именительном падеже.' if order in [9,10] else 'управление и самостоятельная именная подпись согласованы; падежной подсказки нет.'),'plausibility':reason,'truthUniqueKey':reason,'noteTruthUsefulness':note,'sourcesLocators':locations})
 entries.append({'id':q['id'],'sourceOrder':order,'stage':'INITIAL','currentCard':q,'currentCardCanonicalSHA256':digest(q),'status':d['status'],'sixLiteralCanonicalGroups':gr,'fourFullPromptAnswerNoteVariants':variants,'absoluteLevel':{'frozen':'easy','assessment':d['level']},'correctNoteExtraFact':{'assessment':d['extra'],'sourcesLocators':d['opts'][q['correctIndex']][2]},'defects':d['defects'],'frozen':{'questionId':q['id'],'topicId':'books-publishing','sourceOrder':order,'difficulty':q['difficulty'],'correctIndex':q['correctIndex'],'matchesAuthorBefore':next(e for e in candidates if e['id']==q['id'])['beforeCard']['correctIndex']==q['correctIndex']}})
save('receipt.json',{'reader':'01a13f7e-d71d-7351-8403-696e2273eaca','at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'stage':'INITIAL','assignedApplyCommit':'cdd92f09da579a7445584869954310333f3495e7','sourceCatalogPath':str(R/'src/content/topics/books-publishing.json'),'sourceCatalogRawSHA256':hashlib.sha256((R/'src/content/topics/books-publishing.json').read_bytes()).hexdigest(),'scopeSourceOrders':orders,'qualityCredit':0,'entries':entries,'process':'Pinned 12e5581b question-revision + packet-contract + guide 2026-09-02 + planning GAME_SPEC Content + question-catalog spec21-33. No inherited author PASS. No runtime/tests/build/Git mutations.'})
save('sources.json',{'entries':list(S.values()),'distinctRetainedBodyFiles':3,'urlEntryCount':9,'limitation':'These nine URL/view mappings point into three combined returned tool outputs, not nine distinct HTTP bodies. Complete relevant claim-bearing definitions/conditions personally read; no search snippets used. No failed curl repeated. Universal paperback glue claim not established.'})
# Full actual peers are freshly read from the catalog, never substituted with HOLD proposals.
peerorders=[4,5,*range(11,21),26,27,54,58,65,66,67,68,71,72,84]
peers=[{'id':qs[i-1]['id'],'topicId':'books-publishing','sourceOrder':i,'card':qs[i-1],'canonicalSHA256':digest(qs[i-1]),'readScope':'Full card personally read; MAIN assessed as neighbor, not certified for quality credit.'} for i in peerorders]
for topic,ids in {'crafts':['crafts-perfect-glue','crafts-case-binding-cover'],'anime-manga':['anime-manga-manga-cover','anime-manga-tobira-term']}.items():
 topicqs=read(R/('src/content/topics/'+topic+'.json'))['questions']
 for i,q in enumerate(topicqs,1):
  if q['id'] in ids:peers.append({'id':q['id'],'topicId':topic,'sourceOrder':i,'card':q,'canonicalSHA256':digest(q),'readScope':'Full card personally read; MAIN assessed, no independent quality certification of neighbor.'})
oldpeer=read(P/'peer-snapshot.json')
for e in oldpeer['actualCurrentPeers']+oldpeer['actualCrossTopicCurrentPeers']:
 live=next(p for p in peers if p['id']==e['id']);assert live['card']==e['card'] and live['canonicalSHA256']==e['sha256']
addon=read(P/'final/source-binding-and-current-4-5-addendum.json')
for e in addon['actualCurrent4And5FullCardsAndHashes']:
 live=next(p for p in peers if p['id']==e['id']);assert live['card']==e['card'] and live['canonicalSHA256']==e['sha256']
# Independent tuples state the requested relation rather than copying author duplicate verdicts.
relations={
'books-publishing-cover-part':'книжный блок → внешняя защитная оболочка → обложка; общий физический объект книги',
'books-publishing-spine-part':'обычная полочная расстановка книги → наружу с названием/автором → корешок',
'books-publishing-titlepage-part':'титульный лист → член предварительных страниц до текста → front matter; редакторская классификация',
'books-publishing-endpaper-part':'лист между жёсткой крышкой и блоком → конструктивное соединение → форзац',
'books-publishing-hardcover-form':'формат книги → жёсткие картонные крышки вокруг блока → твёрдый переплёт',
'books-publishing-paperback-form':'бумажная гибкая собственная крышка вместо жёсткого case → мягкая обложка',
'books-publishing-ebook-form':'произведение как читаемый экранный цифровой файл → электронная книга',
'books-publishing-audiobook-form':'произведение в звуковом исполнении → аудиокнига',
'books-publishing-editor-role':'ранняя помощь автору с содержанием/порядком до языковой правки → редактор',
'books-publishing-proofreader-role':'заключительный контроль proof против редакторских отметок/ошибок набора → корректор',
'books-publishing-manuscript-stage':'авторский текст до оформления/печати → рукопись',
'books-publishing-copyedit-stage':'подготовленный текст → языковая ясность/стиль/согласованность → литературное редактирование',
'books-publishing-proof-stage':'почти готовые полосы → объект последней проверки → корректурный оттиск',
'books-publishing-printready-stage':'свёрстанный файл → окончательно готов к производству → оригинал-макет',
'books-publishing-case-binding':'сшитый/клеёный блок → вставка в отдельную жёсткую крышку → твёрдый переплёт как технология',
'books-publishing-perfect-binding':'обработанные корешковые края → приклеивание к мягкой обложке → клеевое бесшвейное скрепление',
'books-publishing-saddle-binding':'сложенные листы → скобы через общий сгиб → внакидку',
'books-publishing-spiral-binding':'пробитые листы → непрерывная спираль через отверстия → спиральный переплёт',
'books-publishing-signature-layout':'сложенный большой лист → последовательность страниц → печатная тетрадь',
'books-publishing-imposition-layout':'страницы на печатном листе → размещение с учётом фальцовки → спуск полос',
'books-publishing-designer-role':'визуальная структура страниц/шрифты → автор оформления → книжный дизайнер',
'books-publishing-typesetter-role':'подготовленные текст/изображения → размещение на страницах → верстальщик',
'books-publishing-contents-structure':'список разделов с номерами → оглавление',
'books-publishing-binding-basic':'скрепление страниц в единый защищённый блок → переплёт как весь процесс',
'books-publishing-epub-format':'открытый формат → подстройка текста под экран → EPUB',
'books-publishing-pdf-format':'формат файла → сохранение фиксированного макета → PDF',
'books-publishing-daisy-format':'доступный формат → синхронизация структурированного текста и звука → DAISY',
'books-publishing-azw-format':'Amazon/Mobipocket → ранний фирменный Kindle формат → AZW',
'books-publishing-foreedge-part':'край блока напротив корешка → передний обрез',
'books-publishing-joint-part':'канавка между корешком крышки и сторонкой → расстав',
'books-publishing-runninghead-nav':'повторяющаяся строка страницы → колонтитул',
'crafts-perfect-glue':'срезанные листы → слой клея на корешке → клеевое бесшвейное скрепление',
'crafts-case-binding-cover':'отдельно изготовленная жёсткая крышка → соединение с блоком → твёрдый переплёт как технология',
'anime-manga-manga-cover':'книга манги → внешняя страница с названием/изображением → обложка; та же внешняя оболочка книги',
'anime-manga-tobira-term':'титульная страница японской книги → японское название → тобира'}
special={
frozenset(['books-publishing-cover-part','anime-manga-manga-cover']):('FIX_DUPLICATE','Оба вопроса идентифицируют одну внешнюю обложку обычной книги. Замена признака «название/изображение» на защиту не вводит отдельной конструкции: в MAIN соседа это та же внешняя страница, в explanation прямо дана её защита. Контекст манги не требует дополнительного факта; нужна независимая MAIN-связь.'),
frozenset(['books-publishing-titlepage-part','anime-manga-tobira-term']):('DISTINCT','Титул как член front matter не проверяет японское слово «тобира». В обратную сторону знание японского термина не устанавливает издательскую классификацию preliminary pages. Совпадает объект, различны relation/value; дефекты №3 остаются собственными.'),
frozenset(['books-publishing-editor-role','books-publishing-copyedit-stage']):('DISTINCT','№9 требует роль раннего развития содержания/порядка, №12 название стадии языкового улучшения подготовленного текста. Early development и copyediting разделены CIEP L44-53; смена роли на этап здесь сопровождается реально другим действием/стадией, не просто прямым обратным вопросом той же связи.'),
frozenset(['books-publishing-proofreader-role','books-publishing-proof-stage']):('DISTINCT','№10 — специалист и операция сверки proof с copy; №13 — название проверяемого почти готового документа. Они не меняют местами субъект/значение одной связи: proof является объектом разных профессиональных операций. Знание имени документа не даёт профессию или against-copy функцию.'),
frozenset(['books-publishing-paperback-form','books-publishing-hardcover-form']):('DISTINCT','Актуальный №5 идентифицирует hardback по жёстким картонным крышкам, №6 paperback по собственной гибкой бумажной крышке. Это контрастные значения классификации двух конструкций, не обмен местами объекта и ответа одной entity-relation-value пары. Разрешённая разница свойств не устраняет отдельный дефект: все неверные ярлыки №6 прямо называют «твёрдый».'),
frozenset(['books-publishing-paperback-form','books-publishing-case-binding']):('DISTINCT','№6 — материал/гибкость собственной крышки; №15 — технологическая вставка уже сшитого/клеёного блока в отдельно изготовленный case. Бумажный материал сам по себе не спрашивает эту сборочную операцию.'),
frozenset(['books-publishing-paperback-form','books-publishing-perfect-binding']):('DISTINCT','№6 — гибкая бумажная крышка, а №16 — обработка краёв и клеевая операция. Мягкий формат не тождественен одной клеевой технологии: именно поэтому безусловная note1 №7 не подтверждена.'),
frozenset(['books-publishing-paperback-form','crafts-case-binding-cover']):('DISTINCT','№6 — гибкая бумажная оболочка, crafts87 — отдельное изготовление жёсткого case и его присоединение. Это материал/класс против конкретной последовательности сборки; не один MAIN с обратным направлением.'),
frozenset(['books-publishing-paperback-form','crafts-perfect-glue']):('DISTINCT','№6 не спрашивает удержание срезанных листов клеем; crafts86 спрашивает именно эту операцию. Общий бумажный формат не заменяет знания метода скрепления.'),
frozenset(['books-publishing-cover-part','books-publishing-binding-basic']):('DISTINCT','№1 — внешняя защитная часть, №58 — весь процесс/конструкция скрепления страниц. Защитная часть не равна сборке блока; общая защитная цель не превращает их в обратную пару.'),
frozenset(['books-publishing-ebook-form','books-publishing-audiobook-form']):('DISTINCT','Визуальное чтение цифрового текста и звуковое исполнение — два самостоятельных вида представления. Цифровой носитель не определяет звук, а звучание не определяет экранный текст; не обратная связь одного факта.')}
comp=[]
for e in entries:
 for p in peers:
  a,b=e['id'],p['id'];status,reason=special.get(frozenset([a,b]),('DISTINCT','A проверяет '+relations[a]+'. B проверяет '+relations[b]+'. Совпадающие термины/канонические facts в notes не являются MAIN. Ни A→B, ни B→A не меняет только направление одной и той же entity-relation-value-context связи.'))
  comp.append({'leftId':a,'leftCurrentSHA256':e['currentCardCanonicalSHA256'],'rightId':b,'rightActualCurrentSHA256':p['canonicalSHA256'],'leftMAIN':relations[a],'rightMAIN':relations[b],'leftToRight':reason,'rightToLeft':'Повторно рассмотрено от B к A: '+reason,'verdict':status})
proposals=[]
for e in candidates:
 proposals.append({'id':e['id'],'sourceOrder':e['sourceOrder'],'card':e['proposedCard'],'canonicalSHA256':digest(e['proposedCard']),'status':'UNAPPLIED_HOLD' if e['sourceOrder'] in [4,5] else 'EXACT_CURRENT_APPLIED'})
proprel=relations.copy();proprel['books-publishing-hardcover-form']='формат книги → возможность отдельной суперобложки или её отсутствия → hardcover; UNAPPLIED HOLD5, не actual CURRENT5'
propcomp=[]
for a,b in itertools.combinations(proposals,2):
 aa,bb=a['id'],b['id'];pair=frozenset([aa,bb]);status,reason=special.get(pair,('DISTINCT','Предложение A: '+proprel[aa]+'. Предложение B: '+proprel[bb]+'. Это разные MAIN relations/values; notes с чужими каноническими facts допустимы и не засчитываются как MAIN-дубликат.'))
 if 'books-publishing-hardcover-form' in pair:
  reason='HOLD5 спрашивает наличие отдельной суперобложки, '+('а №6 — гибкость собственной бумажной крышки. В обоих направлениях это разные конструктивные свойства; HOLD5 не подставлен вместо актуального №5.' if 'books-publishing-paperback-form' in pair else 'другой MAIN в паре: '+proprel[bb if aa=='books-publishing-hardcover-form' else aa]+'. Суперобложка не является этой relation/value; actual5 рассмотрен отдельно по реальной жёсткой крышке.')
 propcomp.append({'leftId':aa,'leftProposedSHA256':a['canonicalSHA256'],'rightId':bb,'rightProposedSHA256':b['canonicalSHA256'],'leftMAIN':proprel[aa],'rightMAIN':proprel[bb],'leftToRight':reason,'rightToLeft':'Проверено обратно: '+reason,'verdict':status})
save('peers.json',{'actualCurrentPeers':peers,'actualCurrentVsReviewedComparisons':comp,'proposedFullCards':proposals,'proposedBilateralComparisons':propcomp,'topicMAINScan': [{'id':q['id'],'sourceOrder':i,'prompt':q['prompt'],'key':q['answers'][q['correctIndex']]['text'],'canonicalSHA256':digest(q)} for i,q in enumerate(qs,1)],'scopeBoundary':'Actual4/5 remain preexisting CURRENT and are neighbors only; proposed4/5 remain unapplied HOLD. Full personal reads for actual4/5,11-20, listed extra relevant peers and four cross-topic peers; MAIN scan all100 books. No inherited author verdicts. Peer cards are not quality-certified here.'})
# Structural and literal validation of only these evidence files; no project test runner.
receipt=read(O/'receipt.json')
for e in receipt['entries']:
 q=e['currentCard'];assert digest(q)==e['currentCardCanonicalSHA256'] and q==qs[e['sourceOrder']-1]
 assert len(e['sixLiteralCanonicalGroups'])==6 and len(e['fourFullPromptAnswerNoteVariants'])==4
 for g in e['sixLiteralCanonicalGroups']:assert digest(g['literal'])==g['canonicalSHA256'] and g['individualGround'] and g['sourcesLocators']
 for v in e['fourFullPromptAnswerNoteVariants']:assert digest({k:v[k] for k in ['prompt','answer','note']})==v['tripleCanonicalSHA256'] and v['noteTruthUsefulness'] and v['sourcesLocators']
 for a in q['answers']:assert len(a['text'].encode('utf-16-le'))//2<=140 and len(a['note'].split())<=35
 assert len(q['explanation'].split())<=70
 assert q['source']['url'].startswith('https://') and q['source']['verifiedAt']=='2026-10-15'
for f in ['receipt.json','sources.json','peers.json']:
 raw=(O/f).read_bytes();assert not any(line.rstrip()!=line for line in raw.decode().splitlines())
save('verification.json',{'stage':'INITIAL','currentExactMatchAppliedCards':8,'sixGroups':48,'fullPromptAnswerNoteTriples':32,'canonicalHashChecks':'PASS','freshActualPeerSnapshotMatches':True,'sourceURLMappings':9,'distinctRawBodyFiles':3,'rawSourceHashChecks':'PASS','structuralOwnArtifactWhitespaceCheck':'PASS','readExistingAffected19QA':{'path':str(C/'qa-books8-initial.json'),'passedTests':read(C/'qa-books8-initial.json')['numPassedTests'],'newTestsRunByReader':False},'statuses':{e['id']:e['status'] for e in entries},'qualityCredit':0,'noOwnRuntimeTestBuildProcessesStarted':True,'noGitIndexRefsCatalogPlanningClaimsMutations':True,'remaining':'Coordinator directed author cycle1 for FIX IDs, exact affected checks and independent FINAL only for changed dependencies, then root binding. Root owns Git preservation; do not archive before that binding/preservation.'})
summary='''INITIAL exact CURRENT books sourceOrders 1/2/3/6/7/8/9/10; assigned apply cdd92f09da579a7445584869954310333f3495e7.\nPASS: 2 spine-part; 8 audiobook-form; 10 proofreader-role.\nFIX: 1 cover-part (MAIN overlap manga-cover); 3 titlepage-part (category/one-key discriminator, own-extra-note); 6 paperback-form (three explicit «твёрдый» distractors); 7 ebook-form (unqualified glued-paperback note); 9 editor-role («копирайтинг» mistranslation).\nNo HOLD from missing relevant source bodies: nine URL/view mappings in three saved files have sufficient relevant passages; universal glue claim is precisely unsupported, not waived.\nAll eight whole cards read; actual4/5 and 11–20 plus listed relevant actual peers, all100 MAIN scan, both proposed sides and four cross-topic peers assessed. 48 literal canonical groups / 32 exact triples; current matches applied proposals. Existing QA19 PASS read, no new tests/runtime/build.\nqualityCredit=0 until coordinator root binding. Next: coordinator sends one directed author cycle1, applies and binds affected FINAL. Root owns Git save; no reader Git/index/refs mutation.\nArtifacts: receipt.json, sources.json, peers.json, verification.json; build-receipt.py records deterministic literal/hash generation and independently written grounds.\nNo own persistent process or disposable build/temp resource created. Durable artifacts remain in assigned folder pending root Git preservation; session archival requires root to preserve them first.\n'''
(O/'INITIAL.md').write_text(summary)
print(json.dumps({'output':str(O),'statuses':{str(e['sourceOrder']):e['status'] for e in entries},'groups':48,'triples':32,'actualPeerCount':len(peers),'actualComparisons':len(comp),'proposedPairs':len(propcomp)},ensure_ascii=False))
