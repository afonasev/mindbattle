import pathlib,json,hashlib,re
OUT=pathlib.Path(__file__).resolve().parent
ROOT=OUT.parents[4]
B=ROOT/'docs/content-audits/question-quality-wave-8'
C=B/'coordinator-01a14018'
Q=C/'qualified-book4-newsolution'
def read(p):return json.loads(p.read_text())
def sha(v):return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def raw(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p):return str(p.relative_to(ROOT))
def save(n,d):(OUT/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
books_path=ROOT/'src/content/topics/books-publishing.json'
books=read(books_path)['questions'];card=books[3]
candidate=read(Q/'candidate.json')['entries'][0]
assert card==candidate['proposedCard'] and sha(card)=='1418c770e216538cbfdde0b17fea62451fd193674929d4dc9deef36c4c3b714a'
sp=read(Q/'sourceproof.json');se=sp['entries'][0]
for s in sp['rawSources']:assert raw(ROOT/s['path'])==s['sha256']
p_ciep=ROOT/sp['rawSources'][0]['path'];p_ox=ROOT/sp['rawSources'][1]['path'];p_pc=ROOT/sp['rawSources'][2]['path']
u_ciep='https://www.ciep.uk/resource/editorial-glossary.html'
u_ox='https://libguides.bodleian.ox.ac.uk/lmh/bookbindings'
u_pc='https://files.peacecorps.gov/documents/ED204_Setting-Up-and-Running-a-School-Library.pdf'
def loc(p,u,l):return {'path':rel(p),'url':u,'locator':l}
FUNCTION=loc(p_ciep,u_ciep,'CIEP turn6view0 L115–119, complete endpapers definition L117')
OX=loc(p_ox,u_ox,'Bodleian Bookbindings turn4view0 L85–100, especially endpaper location/marbling L90–91')
CONT=loc(p_pc,u_pc,'Peace Corps PDF P35–36 (printed30–31), L1116–1124: full contents-page paragraph; adjacent index distinction L1125–1137')
TITLE=loc(p_pc,u_pc,'Peace Corps PDF P34 (printed29), complete title-page paragraph L1056–1057; cover/spine context L1026–1055')
COPY=loc(p_pc,u_pc,'Peace Corps PDF P34 (printed29), complete title-verso paragraph L1058–1063; position/usage context L1078–1085')
groups=[('prompt_ordered_answers_key',{'prompt':card['prompt'],'answers':[a['text'] for a in card['answers']],'correctIndex':card['correctIndex']}),('explanation',card['explanation'])]+[('note'+str(i),a['note']) for i,a in enumerate(card['answers'])]
grounds=[
 ('Prompt описывает дополнительные листы с двух концов блока рядом с внутренними сторонами крышек, а не называет редкий термин и не сообщает соединительную функцию. Bodleian L90 помещает endpapers между covers и text block; CIEP L117 определяет joining. Остальные три функции принадлежат реальным информационным страницам, подтверждённым Peace Corps. Структурная функция таких концевых листов — единственный ключ1. Здесь описана книга с этими листами, а не утверждается наличие форзацев в любой брошюре/цифровом издании.',[FUNCTION,OX,CONT,TITLE,COPY]),
 ('Первое предложение прямо называет форзацы и их соединительную функцию по CIEP L117; второе добавляет иногда декоративную бумагу и документированный marbled пример Bodleian L90–91. Два предложения объясняют ключ, не утверждают, что все форзацы мраморные или что текстовый блок удерживается исключительно ими.',[FUNCTION,OX]),
 ('Справка0 верно относится к содержанию, а не к форзацам. Peace Corps L1116–1124 описывает outline/summary глав и номер для перехода к главе. Номера страниц старта глав — самостоятельная полезная функция навигационного списка; она не приписана концевым листам.',[CONT]),
 ('Справка1 правильно относит соединение крышек с внутренними страницами к форзацам: CIEP L117. «Иногда» сохраняет условность декоративного исполнения. Bodleian L90–91 показывает мраморную бумагу на форзацах и различает её использование также на обложках/обрезах; наличие другого применения не отменяет факт именно о форзацах.',[FUNCTION,OX]),
 ('Справка2 сообщает о титульной странице. Peace Corps L1056–1057 перечисляет book title, author, publisher и обычное расположение справа в начале. Русское «обычно» не превращает это в безусловный стандарт для любой книги.',[TITLE]),
 ('Справка3 описывает страницу с выходной/издательской информацией. Peace Corps L1058–1063 помещает title verso после title page и перечисляет year published и copyright наряду с другими сведениями. «Могут» аккуратно передаёт возможное размещение; справка не заявляет обязательного порядка/юридического требования для всех стран.',[COPY])]
variant_assessments=[
 ('Список глав и страниц — настоящая функция дополнительных информационных страниц; читатель может спутать неназванные начальные/концевые листы с содержанием. Это не невозможная сущность и не шутка.','DISTRACTOR: contents навигирует по главам, не определяет структурную роль описанной пары концевых листов. Размещение оглавления в конце некоторых книг не делает его парой соединительных листов у обеих крышек.'),
 ('Соединительная функция правдоподобна по расположению листов между крышками и блоком. Она отсутствует в prompt, поэтому нужна пространственная интерпретация, а не повтор слов «соединяют».','KEY: CIEP L117 прямо подтверждает joining cover to inside pages; Bodleian подтверждает положение этих листов. Конструкция на обоих концах отличает их от информационных страниц.'),
 ('Титульная информация — знакомая функция начального листа, расположенного недалеко от крышки; естественный выбор при поверхностном чтении описания.','DISTRACTOR: функция title page не описывает назначение двух концевых соединительных листов. Возможная печать названия на декоративном форзаце является вторичным оформлением, не данной общей структурной функцией.'),
 ('Год и copyright действительно помещают на дополнительной странице перед основным текстом; их можно спутать с неназванными служебными листами.','DISTRACTOR: title verso сообщает выходные сведения, но не определяет функцию концевых листов с двух сторон блока. Дополнительная печать данных на отдельном форзаце не делает copyright его обязательным назначением.')]
variants=[]
for i,a in enumerate(card['answers']):
 variants.append({'slot':i,'prompt':card['prompt'],'answer':a['text'],'note':a['note'],'tripleCanonicalSHA256':sha({'prompt':card['prompt'],'answer':a['text'],'note':a['note']}),'grammar':'PASS: вопрос «Что они делают?» о листах и четыре глагольных ответа во множественном числе. Все подписи — законченные предложения с точкой; справки грамматически самостоятельны.','plausibility':variant_assessments[i][0],'truthUniqueKey':variant_assessments[i][1],'noteTruthUsefulness':grounds[i+2][0],'sourcesLocators':grounds[i+2][1]})
entry={'id':card['id'],'topicId':'books-publishing','sourceOrder':4,'stage':'INITIAL','currentCard':card,'currentCardCanonicalSHA256':sha(card),'status':'PASS','sixLiteralCanonicalGroups':[{'group':g,'literal':v,'canonicalSHA256':sha(v),'individualGround':grounds[i][0],'sourcesLocators':grounds[i][1]} for i,(g,v) in enumerate(groups)],'fourFullPromptAnswerNoteVariants':variants,'absoluteLevel':{'level':'easy','status':'PASS','ground':'Широкая взрослая группа читателей бумажных книг сталкивается с листами у внутренней стороны крышек. Вопрос предлагает узнаваемое расположение и просит простую функцию, не название форзаца и не профессиональную технологию крепления. Можно осмысленно связать физический переход от крышки к блоку с соединением и отличить его от знакомых информационных страниц. Это повседневный опыт чтения, не регулярное занятие переплётом. Prompt не говорит, что листы уже приклеены/соединяют, и не повторяет ключ. Все четыре ответа — реальные функции частей книги; совпадение точного расположения с ключом представляет необходимый предметный признак, а не постороннюю словесную подсказку.'},'correctNoteExtraFact':{'status':'PASS','fact':'Для форзацев иногда используют декоративную мраморную бумагу. Prompt/key говорят о расположении/соединении, но не о материале оформления; дополнение относится именно к форзацам, даже если также встречается в explanation.','sourcesLocators':[FUNCTION,OX]},'defects':[],'frozen':{'id':card['id'],'topicId':'books-publishing','sourceOrder':4,'difficulty':card['difficulty'],'correctIndex':card['correctIndex'],'beforeMatches':all(card[k]==candidate['beforeCard'][k] for k in ['id','difficulty','correctIndex'])}}
save('receipt.json',{'scope':'Only books-publishing-endpaper-part sourceOrder4 genuine new function solution, independent INITIAL','reviewDate':'2026-10-15','appliedCommitAssigned':'039bb7f76b7d1fff02d8b61baec03a77cdcb3ee1','qaSourceCompletionCommitAssigned':'36cf1f6bfac11ad4a66da958ff5b7eb2bac444d7','entries':[entry],'qualityCredit':0,'historicalRoute':'Prior terminal term-route HOLD preserved; this review does not erase that verdict and does not grade it again.','rootBinding':'Pending coordinator SOURCE/current/QA binding and Git preservation; PASS alone not credit.'})

source_reads=[(p_ciep,u_ciep,'Personally read full retained CIEP glossary/workflow context earlier this session and reread complete neighboring end-matter/endnotes/endpapers/epigraph entries L115–119 now; L117 states sometimes decorative and joining.'),(p_ox,u_ox,'Personally read full relevant Bodleian bookbinding passages L81–100: edge decoration; marbling history; cheaper coverings; distinct endpaper location and actual marbled endpaper example; pigment/marbling process context. L90 is location/use of marbling, not independently a joining definition.'),(p_pc,u_pc,'Personally read full relevant More about books context PDF P33–36, L992–1142: cover/spine/title/title-verso/labels/contents/index, with all complete paragraphs and scope words; no old ten-digit ISBN datum used for this card.')]
save('sources.json',{'reviewDate':'2026-10-15','sources':[{'path':rel(p),'rawReadSHA256':raw(p),'url':u,'locator':e,'personalReadEvidence':e,'limitations':'Retained official public-source body reused. No new network request or fresh HTTP claim; no snippet/hash/author verdict substituted for reading.'} for p,u,e in source_reads],'qualificationReview':{'sourceManifest':rel(B/'process-v2-books4-function-newsolution-01a13f31/author/qualification-completion/manifest.json'),'read':True,'finding':'Corrected literal note0 is contents and note1 is keyed endpaper function; corrected variants0/1 bind to the same actual strings. Independently checked all6/4 mappings against actual CURRENT and primary bodies. Source swapped evidence grounds do not persist in qualified entry.','scope':'SOURCE qualification and existing QA19 were not inherited as semantic PASS.'},'policyReads':'Pinned12e5581b process, packet-contract coordinator01a13f31, guide2026-09-02 and actual planning Content/question-catalog21–33 read earlier in this session and unchanged. No new editorial contract.'})

sourcepeers=read(Q/'peer-snapshot.json')['actualCurrentPeers'];peers=[]
for old in sourcepeers:
 t=old['topicId'];qs=read(ROOT/('src/content/topics/'+t+'.json'))['questions'];q=next(q for q in qs if q['id']==old['id'])
 peers.append({'id':q['id'],'topicId':t,'sourceOrder':qs.index(q)+1,'card':q,'sha256':sha(q)})
for t,n in [('anime-manga',36),('crafts',69),('crafts',70),('crafts',86)]:
 qs=read(ROOT/('src/content/topics/'+t+'.json'))['questions'];q=qs[n-1]
 if not any(x['id']==q['id'] for x in peers):peers.append({'id':q['id'],'topicId':t,'sourceOrder':n,'card':q,'sha256':sha(q)})
lookup={p['id']:p for p in peers};left=lookup[card['id']]
reasons={
 'books-publishing-cover-part':'4: положение концевых листов → соединительная функция.1: сторона обложки со штрихкодом → задняя. Note1 о форзаце вправе сообщать канонический факт; MAIN не совпадает.',
 'books-publishing-spine-part':'4 спрашивает внутренние листы/соединение,2 — видимую на полке часть с названием/автором. Декоративный форзац в note2 не является MAIN-дубликатом.',
 'books-publishing-titlepage-part':'4 выбирает структурную роль форзацев,3 — узнаёт титульный лист по названию/автору/издателю. Факт из неверного ответа и note2 карточки4 может быть ключом3; MAIN4 не является обратным MAIN3.',
 'books-publishing-hardcover-form':'4 — функция конкретных листов,5 — формат IngramSpark с/без суперобложки. Объект и отношение различны.',
 'books-publishing-case-binding':'4 — соединение концевыми листами,15 — название ламинированного покрытия жёсткой крышки без суперобложки. Конструкция covers общая, но entity/relation/value различны.',
 'books-publishing-colophon-term':'4 спрашивает функцию соединительных листов,22 — название записи с библиографическими сведениями. Copyright в дистракторе4 не становится MAIN4.',
 'books-publishing-exlibris-term':'4 — концевые листы соединяют крышку и блок,24 — владельческий знак внутри передней крышки. Совпадает область расположения, но лист и знак с другой функцией не один объект.',
 'books-publishing-headband-part':'4 — бумажные концевые листы и соединение,49 — тесьма у верхнего/нижнего края корешка и её имя. Разные физические детали; note о марле не меняет MAIN.',
 'books-publishing-mull-part':'4 — дополнительные бумажные листы у обеих внутренних крышек/их функция.50 — ткань поперёк корешка/название переплётная марля. Обе детали участвуют в соединении блока и крышки, но различаются материал, положение и спрашиваемое отношение. Это не разворот одной связи форзац↔соединение; MAIN50 идентифицирует другую сущность.',
 'books-publishing-contents-structure':'4 — функция форзацев,54 — имя списка разделов/страниц. Справка0 карточки4 вправе объяснять содержание; это не MAIN-дубликат.',
 'books-publishing-foreedge-part':'4 — функция внутренних листов,71 — имя свободного края напротив корешка. Ни одна MAIN-связь не является обратной другой.',
 'books-publishing-joint-part':'4 — бумажные листы между крышками и блоком/соединение,72 — гибкая канавка между корешком и сторонкой/название расстав. Общая конструкция книги, разные детали и отношения.',
 'crafts-case-binding-cover':'4 — какую функцию выполняют конкретные листы,crafts87 — какой метод отдельно делает жёсткую крышку и соединяет её с блоком. Метод твёрдого переплёта не равен одному его компоненту. Explanation87 учит роль форзацев, но MAIN метода не является прямым/обратным MAIN4.',
 'crafts-saddle-stitch-fold':'4 — концевые соединительные листы,crafts69 — способ скрепления листов через общий сгиб. Разные компоненты/процессы.',
 'crafts-coptic-exposed':'4 — функция концевых листов,crafts70 — метод с видимым шитьём и плоским раскрытием. Название метода не выводится из MAIN4.',
 'crafts-perfect-glue':'4 — дополнительные листы между крышкой и блоком,crafts86 — клеевое удержание срезанных листов на корешке. Клей/метод и бумажная деталь — не одна MAIN-связь.',
 'anime-manga-manga-cover':'4 — внутренние листы соединяют крышки с блоком,anime36 — внешняя страница манги с названием/картинкой называется обложкой. Note о форзаце совпадает с каноническим фактом, что допустимо; MAINы различны.',
 'middle-ages-codex':'4 — концевые листы переплёта/функция соединения,средневековый98 — сложенный пергамент с четырьмя страницами/бифолий. Материал, часть конструкции и проверяемая связь различны.',
 'books-publishing-designer-role':'4 — функция детали книги,26 — профессия визуального оформления. Не общий MAIN.',
 'books-publishing-borrow-action':'4 — физическая конструкция,28 — библиотечная выдача. Не общий MAIN.'}
comparisons=[{'left':left,'right':lookup[id],'leftToRight':why,'rightToLeft':'MAIN соседа не спрашивает, какую соединительную функцию выполняют описанные концевые бумажные листы у внутренних сторон крышек.','status':'DISTINCT_MAIN','scope':'Semantic comparison only; no quality rereview of neighbor'} for id,why in reasons.items()]
patterns=[r'форзац',r'endpaper',r'внутренн.{0,20}(крыш|облож)',r'соедин.{0,35}(крыш|облож)',r'мраморн.{0,15}бумаг',r'содержан.{0,20}глав',r'титульн']
rx=re.compile('|'.join(patterns),re.I);hits=[]
for p in sorted((ROOT/'src/content/topics').glob('*.json')):
 for n,q in enumerate(read(p)['questions'],1):
  if rx.search(json.dumps(q,ensure_ascii=False)):hits.append({'topicId':p.stem,'id':q['id'],'sourceOrder':n,'sha256':sha(q),'main':{'prompt':q['prompt'],'key':q['answers'][q['correctIndex']]['text']}})
parallel=[]
for p in B.glob('process-v2-books31-50*/author/candidate.json'):
 d=read(p);es=d.get('entries',[])
 parallel.append({'path':rel(p),'rawSHA256':raw(p),'readySourceOrders':[e.get('sourceOrder') for e in es if e.get('status')=='READY_FOR_INDEPENDENT_REVIEW'],'heldSourceOrders':[e.get('sourceOrder') for e in es if e.get('status')=='HOLD'],'finding':'At review time every entry31–50 HOLD; no ready parallel postimage treated as CURRENT or accepted proposed pair. Current49/50 personally read as peers.'})
save('peers.json',{'actualCurrentPeers':peers,'bilateralMainComparisons':comparisons,'globalRetrieval':{'paths':'src/content/topics/*.json','patterns':patterns,'hits':hits,'method':'Fresh MAIN retrieval beyond SOURCE139; existing same-topic100/full cross-topic snapshot refreshed from actual disk. Relevant complete cards personally read; new anime/crafts candidates retained above. Body keyword matches in cars/architecture unrelated to book construction are discarded by MAIN context.'},'parallelProposalInspection':parallel,'proposedRelevantPairs':[],'freshness':'CURRENT4 replaced old term-route preimage in this new snapshot; all other peers reloaded from current topic files, not inherited hashes.'})
qa=C/'qa-book4-newsolution.json';qd=read(qa);assert qd['success'] and qd['numPassedTests']==19 and qd['numFailedTests']==0
sg={g['group']:g for g in se['literalGroups']};sv={v['slot']:v for v in se['fourFullPromptAnswerNoteAssessments']}
for g,v in groups:
 assert sg[g]['literal']==v and sg[g]['literalSHA256']==sha(v)
for v in variants:
 s=sv[v['slot']];assert (s['fullPrompt'],s['answer'],s['note'],s['tripleSHA256'])==(v['prompt'],v['answer'],v['note'],v['tripleCanonicalSHA256'])
save('verification.json',{'currentCardCanonicalSHA256':sha(card),'catalogRawSHA256':raw(books_path),'sourceQualifiedCandidateRawSHA256':raw(Q/'candidate.json'),'sourceQualifiedProofRawSHA256':raw(Q/'sourceproof.json'),'sourceQualifiedPeersRawSHA256':raw(Q/'peer-snapshot.json'),'sixLiteralGroups':6,'fourTriples':4,'sourceCurrent6Plus4ExactBindingsVerified':True,'sourceQualificationSwapRepair':'Verified actual contents note0/variant0 and endpapers note1/variant1 with correct primary grounds; not merely trusted manifest.','answerUTF16Lengths':[len(a['text'].encode('utf-16-le'))//2 for a in card['answers']],'noteWordCounts':[len(a['note'].split()) for a in card['answers']],'explanationSentenceCount':len(re.findall(r'[.!?](?:\s|$)',card['explanation'])),'explanationWordCount':len(card['explanation'].split()),'frozen':entry['frozen'],'existingQA19':{'path':rel(qa),'rawSHA256':raw(qa),'passed':19,'failed':0,'readNotRerun':True},'qualityCredit':0,'projectTestsRuntimeBuildRun':False,'ownBackgroundProcesses':0,'gitOperations':'None for this assignment. No status/index/refs/catalog/planning/claims changes.','preservation':'All outputs within assigned durable folder; no temp artifacts or own background resources. Task-cleanup reference read earlier in this session; coordinator owns Git preservation and must verify actual branch/commit before archival.'})
save('packet-manifest.json',{'stage':'INITIAL','id':card['id'],'status':'PASS','currentSHA256':sha(card),'files':[{'path':rel(OUT/n),'rawSHA256':raw(OUT/n)} for n in ['receipt.json','sources.json','peers.json','verification.json']],'next':'Root adjudication SOURCE/current/QA binding and Git preservation; no automatic certification credit or old HOLD deletion.'})
print(json.dumps({'verdict':'INITIAL PASS','id':card['id'],'hash':sha(card),'groups':6,'triples':4,'peers':len(peers),'bilateralPairs':len(comparisons),'parallelReady':sum(len(x['readySourceOrders']) for x in parallel),'QA19':'existing PASS read, not rerun'},ensure_ascii=False))
