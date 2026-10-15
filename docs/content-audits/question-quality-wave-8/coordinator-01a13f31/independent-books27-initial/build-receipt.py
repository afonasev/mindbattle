import json, hashlib, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parents[5]
OUT = pathlib.Path(__file__).resolve().parent
BASE = ROOT / 'docs/content-audits/question-quality-wave-8'
AUTHOR = BASE / 'process-v2-books21-30-01a13f31/author/source27-completion'
COORD = BASE / 'coordinator-01a13f31'
def read(p): return json.loads(p.read_text())
def sha(v): return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def raw(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p): return str(p.relative_to(ROOT))
def save(name,data): (OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')

books = read(ROOT/'src/content/topics/books-publishing.json')['questions']
design = read(ROOT/'src/content/topics/design.json')['questions']
q = books[26]
entry = read(AUTHOR/'candidate.json')['entries'][0]
assert q == entry['proposedCard'] and sha(q) == '7e6651c54866fa0a9cdcddd0190c3d5c777b586f20d7d3995cfc3d03aad34326'
ctx = AUTHOR/'contexts/kdp-and-ingram-interior-layout-2026-10-15.json'
assert raw(ctx) == 'cb7295d4ab47e7cd4b346036b6c5dc692a85b4db585da36776aa3dc8303ffe9e'
kdp = q['source']['url']
ingram = 'https://www.ingramspark.com/blog/9-tips-for-interior-book-design'
def loc(lines,url=kdp): return {'path':rel(ctx),'url':url,'locator':lines}
ground = [
 ('prompt_ordered_answers_key', {'prompt':q['prompt'],'answers':[a['text'] for a in q['answers']],'correctIndex':q['correctIndex']},
  'Внутреннее поле находится у переплёта: IngramSpark объясняет, что его ширина оставляет место для скрепления и сгиба страницы и позволяет читать текст. Внешнее поле находится на свободном крае. Trim size задаёт размеры книги, а bleed выводит изображение за линию реза. Эти реальные параметры относятся к одному макету; только увеличение внутреннего поля прямо задаёт нужный отступ.',[loc('KDP L84–93; L197–215; L216–223'),loc('IngramSpark §6 Mind Your Margins L33–35',ingram)]),
 ('explanation',q['explanation'],'Первое предложение прямо называет увеличение внутреннего поля. Второе корректно относит зависимость нужной ширины от числа страниц к KDP: L214 объясняет толщину блока, таблица L218–222 повышает минимум от 0,375 до 0,875 дюйма. Это объяснение причины, а не универсальный норматив для любого издателя.',[loc('KDP Margins L211–223')]),
 ('note0',q['answers'][0]['note'],'KDP L87 и L215 называют inside margin gutter. L214 и таблица L216–222 связывают его минимум с числом страниц/толщиной блока; минимум растёт по диапазонам, а не обязательно при каждой добавленной странице. Справка не утверждает линейную зависимость.',[loc('KDP L87; L214–222')]),
 ('note1',q['answers'][1]['note'],'Для внешнего поля KDP прямо указывает минимум 0,25 дюйма без bleed и 0,375 с bleed; оба числа повторяются во всех строках таблицы. В справке сохранены квалификатор KDP и условие наличия вылетов; это не правило всех типографий.',[loc('KDP L214; L217–223')]),
 ('note2',q['answers'][2]['note'],'KDP определяет trim size как ширину и высоту напечатанной книги (L85) и требует выбрать размер до настройки полей (L87). Справка сообщает именно об обрезном формате, не приписывает ему функцию внутреннего поля.',[loc('KDP L84–94')]),
 ('note3',q['answers'][3]['note'],'KDP L86 объясняет выход печатного объекта за линию реза, L159 — запас 0,125 дюйма, L197–200 — необходимость bleed для изображений/фона до края. Справка правильно описывает сохранение изображения до края после обрезки.',[loc('KDP L85–87; L146–159; L197–206')])
]
variant_grounds = [
 ('Оба элемента «увеличить» и «внутреннее поле» называют действие с нужным параметром. Это не повтор слов prompt: игрок соотносит внутреннюю сторону страницы с переплётом.', 'PASS: непосредственно увеличивает расстояние от текста до внутреннего края.', 'Полезное дополнение — название gutter и зависимость минимума от числа страниц. Факт о конкретном параметре, которого нет в prompt/key.',[loc('KDP L87; L214–222'),loc('IngramSpark L33–35',ingram)]),
 ('Внешнее поле — реальный параметр того же макета; его можно спутать с внутренним, если неверно определить сторону страницы.', 'Неверен: увеличение отступа от свободного края не задаёт дополнительного пространства у переплёта.', 'Числа 0,25/0,375 и условие bleed достоверны именно для KDP. Это самостоятельный факт об указанном внешнем поле.',[loc('KDP L87; L214–223')]),
 ('Обрезной формат — реальная настройка геометрии книги; правдоподобен для игрока, считающего, что большая страница автоматически даёт больше свободного места.', 'Неверен как достаточное изменение: «изменить» не задаёт ни направления, ни увеличения внутреннего отступа. KDP L91 допускает изменение числа страниц при смене формата, а L214 связывает с числом страниц требуемый минимум; это не утверждение об автоматическом изменении фактического поля. Даже переход между диапазонами таблицы требует отдельно установить поле. Для второго ключа пришлось бы добавить не указанное действие или автоматическую перенастройку. Нельзя обосновывать неверность ложным тезисом, будто формат вообще не влияет на пагинацию/требования к gutter.', 'Определение размеров и порядок настройки trim перед margins подтверждены. Справка не скрывает зависимости: она явно указывает порядок расчёта.',[loc('KDP L85–94; L214–223')]),
 ('Вылет — ещё одна реальная печатная настройка; его можно ошибочно принять за запас свободного места на странице. Самая длинная подпись — неверная, длина не выделяет ключ.', 'Неверен: bleed продолжает изображение за наружный рез и не сдвигает текст от переплёта.', 'Самостоятельный факт о цели вылета подтверждён в разделе When to choose bleed. Он может совпадать с ключевым фактом design-bleed-print: запрета на такие справки нет.',[loc('KDP L86; L159; L197–206')])
]
variants=[]
for i,(plaus,truth,note,locs) in enumerate(variant_grounds):
 a=q['answers'][i]
 variants.append({'slot':i,'prompt':q['prompt'],'answer':a['text'],'note':a['note'],'tripleCanonicalSHA256':sha({'prompt':q['prompt'],'answer':a['text'],'note':a['note']}),'grammar':'PASS: законченный вопрос «Какое изменение…?» и самостоятельная инфинитивная подпись; управление и вид действия естественны.','plausibility':plaus,'truthUniqueKey':truth,'noteTruthUsefulness':note,'sourcesLocators':locs})
receipt={'scope':'ONLY books-publishing sourceOrder27; independent INITIAL, not FINAL','reviewDate':'2026-10-15','baselineCommit':'de2e42ccefde89923450e3c0c328f138a0441472','sourceFreeze':'5b639276914b141555f70b11f3bd0ff0bb141c3e','entries':[{'id':q['id'],'topicId':'books-publishing','sourceOrder':27,'stage':'INITIAL','currentCard':q,'currentCardCanonicalSHA256':sha(q),'status':'PASS','sixLiteralCanonicalGroups':[{'group':g,'literal':v,'canonicalSHA256':sha(v),'individualGround':s,'sourcesLocators':ls} for g,v,s,ls in ground],'fourFullPromptAnswerNoteVariants':variants,'absoluteLevel':{'level':'easy','status':'PASS','ground':'Знакомая обычному читателю проблема: текст скрывается у сгиба. Нужно выбрать, с какой стороны увеличить пустой отступ. Термин gutter, числа KDP и профессиональная роль не нужны для ответа. Есть простая пространственная связь внутренней стороны с переплётом, а не редкое профессиональное знание. Альтернативы — реальные параметры страницы; вопрос не повторяет словосочетание «внутреннее поле» и не задаёт невозможных вариантов.'},'correctNoteExtraFact':{'status':'PASS','fact':'В KDP inside margin также называется gutter; его минимум определяется диапазоном числа страниц из-за толщины блока. Prompt/key говорят только об увеличении отступа для читаемости.','sourcesLocators':[loc('KDP L87; L214–222')]},'frozen':{'id':q['id'],'topicId':'books-publishing','sourceOrder':27,'difficulty':'easy','correctIndex':0,'matchesAuthorBefore':all(q[k]==entry['beforeCard'][k] for k in ['id','difficulty','correctIndex'])},'defects':[]}],'qualityCredit':0,'creditNote':'Independent PASS only. Root must bind SOURCE/current/QA and preserve Git. Does not complete goal2000.'}
save('receipt.json',receipt)

actual=[]
for t,qs in [('books-publishing',books),('design',design)]:
 for n,c in enumerate(qs,1):actual.append({'id':c['id'],'topicId':t,'sourceOrder':n,'card':c,'sha256':sha(c)})
external=[]
patterns=[r'gutter',r'внутренн\w*\s+пол',r'обрезн\w*\s+формат',r'пол[яе]\s+страниц',r'поле\s+у\s+корешка',r'кореш[коа]',r'вылет',r'перепл[её]т',r'типограф',r'макет']
rx=re.compile('|'.join(patterns),re.I)
hits=[]
for p in sorted((ROOT/'src/content/topics').glob('*.json')):
 for n,c in enumerate(read(p)['questions'],1):
  if rx.search(json.dumps(c,ensure_ascii=False)):
   hits.append({'topicId':p.stem,'sourceOrder':n,'id':c['id'],'sha256':sha(c),'main':{'prompt':c['prompt'],'key':c['answers'][c['correctIndex']]['text']}})
  if c['id']=='middle-ages-gloss':external.append({'id':c['id'],'topicId':p.stem,'sourceOrder':n,'card':c,'sha256':sha(c)})
actual.extend(external)
left=next(x for x in actual if x['id']==q['id'])
comparisons=[]
reasons={
 'books-publishing-spine-part':'27: отступ текста у сгиба → увеличить внутреннее поле. Сосед: видимая часть стоящей книги с названием/автором → корешок. Общая часть книги не делает связи тождественными; заметка соседа о числе страниц не MAIN27.',
 'books-publishing-copyedit-stage':'27 проверяет пространственный параметр готовой страницы; 12 — место copyediting в производственном цикле. Упоминание верстки в справке 12 не повторяет MAIN27.',
 'books-publishing-case-binding':'27 — отступ при читаемости у сгиба; 15 — наименование конструкции ламинированной твёрдой крышки без суперобложки. Не прямой/обратный факт.',
 'books-publishing-saddle-binding':'27 — внутристраничный отступ; 17 — кратность числа страниц четырём при конкретном скреплении. Число страниц в note27 не задаёт арифметический ключ17.',
 'books-publishing-spiral-binding':'27 — увеличение внутреннего поля; 18 — распознать coil по петле через отверстия. Раскрытие плоско в справке18 связано с читаемостью, но не является MAIN27.',
 'books-publishing-signature-layout':'27 выбирает отступ текста; 19 распознаёт секцию из сложенного листа как signature. Сгиб и переплёт — общая предметная область, связь различна.',
 'books-publishing-imposition-layout':'27 выбирает внутристраничный отступ; 20 называет размещение полос на печатном листе для порядка после фальцовки. Не обратные вопросы.',
 'books-publishing-designer-role':'27 — какая настройка решает проблему у корешка; 26 — кто отвечает за оформление обложки/интерьера. Роль и параметр — разные отношения. Ни один MAIN не сообщает ключ другого.',
 'books-publishing-borrow-action':'27 относится к физическому макету; 28 — библиотечная выдача на срок. Смыслового совпадения нет.',
 'books-publishing-trim-layout':'27 требует отступа у переплёта; 37 называет выравнивание трёх свободных краёв готового блока. Обрезной формат среди неверных27 не делает MAIN равным обрезке37.',
 'books-publishing-binding-basic':'27: параметр отступа; 58: название процесса соединения страниц с оболочкой. Упоминание переплёта в prompt27 не является прямым или обратным определением процесса58.',
 'books-publishing-pdf-format':'27 проверяет внутреннее поле; 66 — формат файла с фиксированным расположением. Общий макет не означает общий ключевой факт.',
 'books-publishing-foreedge-part':'27 — увеличиваем отступ у корешка; 71 — называем край напротив корешка. Общая пространственная ось, но ни отношение, ни значение не совпадают.',
 'design-grid-swiss':'27 выбирает конкретный отступ; 38 — инструмент организации колонок/полей в швейцарской типографике. Часть регулируемой геометрии не равна инструменту организации.',
 'design-font-size':'27 — скрытый сгибом текст/внутреннее поле; 59 — мелкий текст/размер шрифта. Практическая форма схожа, причины и изменяемые параметры независимы.',
 'design-line-spacing':'27 — горизонтальный отступ от переплёта; 60 — вертикальное расстояние между строками. Не прямой/обратный факт.',
 'design-bleed-print':'27 спрашивает отступ у переплёта, 61 — название продолжения изображения за рез. Note3 карточки27 вправе объяснять bleed; это не MAIN-дубликат.',
 'design-crop-marks':'27 — поле внутри книжного блока; 62 — линии положения реза. Обе относятся к подготовке печати, ключевые связи различны.',
 'design-line-length':'27 решает скрытие текста у сгиба; 76 — трудность найти начало следующей строки/длина строки. Общая читаемость, разные причины и параметры.',
 'design-portrait-format':'27 — отступ у переплёта; 78 — высота больше ширины/портретная ориентация. Разные отношения.',
 'design-landscape-format':'27 — отступ у переплёта; 79 — ширина больше высоты/альбомная ориентация. Разные отношения.',
 'design-square-format':'27 — внутреннее поле; 80 — равенство ширины и высоты/квадрат. Обрезной формат — неверная альтернатива27, не MAIN.',
 'design-panorama-format':'27 — внутреннее поле; 81 — очень широкий формат/панорама. Не прямой/обратный вопрос.',
 'middle-ages-gloss':'27 — расстояние от текста до переплёта для читаемости; средневековая карточка — расширение полей для разросшейся глоссы по Leiden. Общий приём «больше поля» не делает одинаковыми параметр, причину и контекст: место для комментария против отступа у скрепления.'}
for id,why in reasons.items():
 right=next(x for x in actual if x['id']==id)
 comparisons.append({'left':left,'right':right,'status':'DISTINCT_MAIN','bilateralMainAssessment':why,'scope':'semantic neighbor only; no quality rereview of counterpart'})
proposal_path=BASE/'process-v2-books26-28-cycle1-and-locator3-01a13f31/author/candidate.json'
proposed=[]
for e in read(proposal_path)['entries']:
 c=e['proposedCard']; assert sha(c)==e['afterHash']
 proposed.append({'left':left,'right':{'id':c['id'],'topicId':e['topicId'],'sourceOrder':e['sourceOrder'],'card':c,'sha256':sha(c),'state':'PROPOSAL_NOT_CURRENT'},'status':'DISTINCT_MAIN','bilateralMainAssessment':reasons[c['id']]+' Изменены справки, MAIN сохраняется.','sourcePath':rel(proposal_path)})
save('peers.json',{'actualCurrentPeers':actual,'bilateralMainComparisons':comparisons,'proposedRelevantPairs':proposed,'catalogRetrieval':{'paths':'src/content/topics/*.json','queryPatterns':patterns,'matchingCards':hits,'method':'Fresh MAIN retrieval across all topic files; 200 books/design MAIN screen, personally full-read relevant neighbors retained above. Cross-topic broader matches screened by entity/relation/context; middle-ages-gloss retained as closest external neighbor. Source200 not treated as exhaustive current search.'},'freshness':'CURRENT read directly from disk; SOURCE200 and four-peer delta are context, not inherited verdicts.'})
save('sources.json',{'reviewDate':'2026-10-15','sources':[{'path':rel(ctx),'rawReadSHA256':raw(ctx),'urls':[kdp,ingram],'personalReadEvidence':'Personally read decoded retained context: KDP terms L84–94; both paperback/hardcover trim/page-count context L95–142; bleed L146–206 including 0.125 inch setup; Margins L211–223 including five page-count bands and software inside/gutter caveat L215. Read full IngramSpark article L11–45, especially book size L18–20 and bound-side readability L33–35.','locator':['KDP L84–94, L95–142, L146–223','IngramSpark L11–45'],'limitations':'Retained official public page captures dated 2026-10-15 reused, no new download. Review establishes sourced contents, not an independently refreshed network response. Source URL including query retained exactly. No software behavior inferred beyond what text says.'}],'policyReads':['12e5581b:.agents/references/question-revision.md',rel(COORD/'packet-contract.json'),'docs/content-audits/question-authoring-guide-2026-09-02.md','/Users/eaafonasev/Projects/mindbattle/planning/docs/GAME_SPEC.md:135-149','/Users/eaafonasev/Projects/mindbattle/planning/openspec/specs/question-catalog/spec.md:21-33'],'sourceAuthorReceiptRead':'SOURCE claims compared against primary context; not accepted on author PASS/HTTP/hash.'})
qa=COORD/'qa-books27-initial-completion.json';qa_data=read(qa)
assert qa_data['success'] and qa_data['numPassedTests']==19
catalog_bytes=(ROOT/'src/content/topics/books-publishing.json').read_bytes()
save('verification.json',{'currentCardCanonicalSHA256':sha(q),'catalogRawSHA256':raw(ROOT/'src/content/topics/books-publishing.json'),'catalogGitBlobSHA1ComputedWithoutGit':hashlib.sha1(b'blob '+str(len(catalog_bytes)).encode()+b'\0'+catalog_bytes).hexdigest(),'assignedWholebookIdentity':'9352f63b4fd3deb2716e0facbaaae1828b62b78d','wholebookBinding':'UNCONFIRMED: supplied wholebook identity is 40 hex and does not equal computed Git blob SHA1. It is not labeled or treated as SHA256. Target card exactly matches assigned canonical SHA256; current12/15/17/18 match supplied delta, 26/28 remain before proposal. Root must resolve supplied wholebook identity before quality credit. No Git inspection authorized here.','sourceRawSHA256':raw(ctx),'sixGroups':len(ground),'fourTriples':len(variants),'answerUTF16Lengths':[len(a['text'].encode('utf-16-le'))//2 for a in q['answers']],'noteWordCounts':[len(a['note'].split()) for a in q['answers']],'explanationWordCount':len(q['explanation'].split()),'explanationSentenceCount':len(re.findall(r'[.!?](?:\s|$)',q['explanation'])),'frozenMatches':receipt['entries'][0]['frozen']['matchesAuthorBefore'],'qaEvidenceOnly':{'path':rel(qa),'rawSHA256':raw(qa),'passed':qa_data['numPassedTests'],'failed':qa_data['numFailedTests'],'scope':'Existing coordinator QA19 read; independent reviewer ran no project tests/runtime/build. QA result JSON has no source fingerprint; exact wholebook binding remains root responsibility.'},'ownProjectProcessesStarted':0,'gitOperations':'Only assigned pinned git-show policy read; no status/index/refs/commits. Root owns Git preservation.','qualityCredit':0,'preservation':'All outputs and generator in assigned durable folder. Coordinator must commit exact reviewed packet; uncommitted ownership delegated to coordinator. No temporary files, own background jobs or cleanup targets.'})
save('packet-manifest.json',{'stage':'INITIAL','id':q['id'],'status':'PASS','files':[{'path':rel(OUT/n),'rawSHA256':raw(OUT/n)} for n in ['receipt.json','sources.json','peers.json','verification.json']],'next':'Root binds to SOURCE/current and QA19, preserves exact packet in branch codex/question-quality-wave-6. No automatic FINAL or credit.'})
print(json.dumps({'verdict':'INITIAL PASS','card':sha(q),'groups':6,'triples':4,'peers':len(actual),'comparisons':len(comparisons),'proposalPairs':len(proposed),'catalogRawSHA256':raw(ROOT/'src/content/topics/books-publishing.json')},ensure_ascii=False))
