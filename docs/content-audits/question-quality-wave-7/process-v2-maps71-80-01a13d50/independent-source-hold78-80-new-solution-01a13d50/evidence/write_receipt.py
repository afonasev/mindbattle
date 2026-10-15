import json, hashlib, io
from pathlib import Path
from pypdf import PdfReader
# Resolve by catalog rather than assume the depth of a future relocated audit.
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'src/content/topics/maps-cartography.json').exists())
B=ROOT/'docs/content-audits/question-quality-wave-7/process-v2-maps71-80-01a13d50'
OUT=Path(__file__).resolve().parents[1]
def canon(x): return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode('utf-8')
def h(x): return hashlib.sha256(canon(x)).hexdigest()
def bh(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p): return json.loads(p.read_bytes())
def save(p,x): p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
q=load(ROOT/'src/content/topics/maps-cartography.json')['questions']; byid={c['id']:c for c in q}
proof=load(B/'source-hold78-80-new-solution-author-01a13d50/sourceproof.json')
sources=[]
locators=[
 'PDF p.1, Large Is Small: representative fraction means same units; larger second number means smaller scale; larger scale permits more detail. p.2 opening paragraphs distinguish detail at 1:24,000, 1:50,000–1:100,000 and 1:250,000. Both pages including table and footnote read.',
 'Full context, opening definition; paragraph Lines of latitude, also called parallels; Infographic Transcript: Latitude, right image labels northern/southern sides of equator.',
 'Full context, opening definition and first image description; paragraph The prime meridian; paragraph Like latitude; Infographic Transcript: Longitude right image labels Western/Eastern Hemisphere.'
]
for i,s in enumerate(proof['sources']):
 p=ROOT/s['path']; assert bh(p)==s['byteSHA256']
 sources.append({'id':['usgs-scale','noaa-latitude','noaa-longitude'][i],'path':s['path'],'byteSHA256':bh(p),'bytes':len(p.read_bytes()),'url':s['url'],'title':['Map Scales — USGS Fact Sheet 015-02','What is latitude? — NOAA National Ocean Service','What is longitude? — NOAA National Ocean Service'][i],'personallyReadFullContext':True,'locator':locators[i]})
 if i==0:
  pages=PdfReader(io.BytesIO(p.read_bytes())).pages; assert len(pages)==2
  (OUT/'evidence/usgs-full-two-pages.txt').write_text('\n\n'.join('PAGE '+str(j+1)+'\n'+page.extract_text() for j,page in enumerate(pages)))

grounds=[
 [
 'Данные покрытия и названия явно условны и полностью даны в prompt. Среди полных Юг/Запад/Север знаменатели 100000/50000/25000; минимальный знаменатель 25000 даёт самый крупный масштаб. Восток 10000 исключается частичным покрытием. Единственный ключ — Север, индекс 3.',
 'Полное покрытие Севера дано условием; USGS p.1 связывает меньший знаменатель с более крупным масштабом и большей детализацией. Упоминание вымышленных значений отделяет их от реальных примеров USGS.',
 'Юг полностью покрывает область по условию; 100000 > 25000, поэтому масштаб мельче и деталей меньше по правилу USGS p.1.',
 'Восток имеет наименьший знаменатель 10000 и крупнейший масштаб, но явное частичное покрытие нарушает требование всей области.',
 'Запад полностью покрывает ту же область; 50000 > 25000, значит мельче Севера. Слово участок относится к названной области и не вводит новых габаритов.',
 'Север покрывает область по условию. USGS p.1 прямо определяет representative fraction через одинаковые единицы. Дополнительный факт — смысл 1:25000 — не содержится в actual prompt или key.'
 ],
 [
 'Четыре условные пары заданы полностью: Альфа N/W, Бета S/W, Гамма N/E, Дельта S/E. Только Альфа удовлетворяет одновременно обоим полушариям; ключ 3. Пограничных 0°/180°/полюсов нет.',
 'NOAA latitude определяет N/S относительно экватора; NOAA longitude E/W относительно нулевого меридиана. Fictional coordinates не приписаны источникам.',
 'Бета 20° ю. ш.,30° з. д.: W верно, N неверно. Заметка корректно объясняет ровно эту ошибку.',
 'Гамма 15° с. ш.,10° в. д.: N верно, W неверно. Заметка соответствует данным этой точки.',
 'Дельта 5° ю. ш.,80° в. д.: S/E не соответствуют N/W; ни одно требование не выполнено.',
 'Альфа 40° с. ш.,70° з. д. соответствует N/W. Дополнительный факт о градусах, минутах и секундах долготы буквально подтверждён полным NOAA longitude, отсутствует в actual prompt/key и относится к чтению координат.'
 ],
 [
 'Увеличение линейных размеров ровно x2 превращает исходный сантиметр в 2 см при тех же 2 км местности. Поэтому 2/2=1 км на новый сантиметр; единственный ключ 3. Увеличение по ширине не означает x4 для длины.',
 'USGS p.1 определяет отношение расстояний на карте и местности. Из заданного линейного увеличения следует 1 км/см; 1 км=100000 см, RF 1:100000. Это вывод из условных данных, а не пример USGS.',
 '4 км/см — обратное изменение масштаба: при увеличении карты местности на сантиметр становится меньше. Заметка верно исправляет направление 2→1.',
 '2 км/см верно до увеличения; исходный отрезок занимает 2 см после него. Заметка не путает длину и площадь.',
 'Чтобы 2 км приходились на 4 см, линейное увеличение должно быть x4. Тогда 0,5 км/см. Для заданного x2 вариант неверен.',
 '1 км=100000 см, поэтому новый RF 1:100000. Это полезное преобразование единиц в дополнительную форму масштаба, которой нет в actual prompt/key. USGS p.1 требует одинаковых единиц.'
 ]]
assess=[
 ['Полное покрытие верно, но это наименее подробная из полных страниц. Правдоподобна при игнорировании сравнения масштабов.','Соблазнительный крупнейший масштаб; не выполняет независимое условие полного покрытия.','Полное покрытие и промежуточная подробность; уступает Северу.','Единственная полная страница с крупнейшим среди полных масштабом.'],
 ['Совпадает только западное полушарие.','Совпадает только северное полушарие.','Не совпадает ни одно из требуемых полушарий; типичная полная инверсия меток.','Совпадают обе метки координат.'],
 ['Ошибка направления: умножение вместо деления.','Ошибка сохранения исходного масштаба после перепечатки.','Ошибка подмены линейного коэффициента коэффициентом площади 4.','Правильное деление 2 км на коэффициент длины 2.']]
peer_findings=[
 {'demand':'Отфильтровать неполное покрытие, затем сравнить масштабы полных страниц. Без вычисления расстояния.', 'inbound':'ratio-scale и large-scale обучают отношению знаменателя и подробности; они не называют вымышленные страницы или их покрытие. index-place требует максимального northing, не охвата и масштаба. Даже зная правило, нужно отсеять Восток и связать Север с 1:25000.', 'outbound':'Заметки повторяют общее правило масштабов и могут помочь ratio/large-scale; они не выдают их числовую пару 63360/316800 или требуемый термин как ответ к конкретному чужому prompt. Это общий prerequisite, не whole-key копия задания.','decision':'PASS: два явно заданных простых критерия; не дубль сравнения равного отрезка.'},
 {'demand':'Классифицировать названную точку по конъюнкции N и W; арифметики нет.', 'inbound':'equator/prime/parallel notes объясняют N/S/E/W, но не содержат вымышленных точек. latitude-ns вычисляет изменение широты, longitude-ew вычисляет долготу по времени; UTM добавляет зону. Их ключи не отвечают на выбор Альфы.', 'outbound':'Новые заметки помогают читать обозначения и содержат общий DMS факт; они не дают 33° ю.ш./36° з.д. или номер UTM-зоны и не копируют полный ключ чужой задачи.','decision':'PASS: простая операция сопоставления двух признаков; отличается от севернейшего OS квадрата.'},
 {'demand':'Изменить расстояние на сантиметр после линейного увеличения изображения.', 'inbound':'verbal-scale делит 750/3, bar-scale применяет 200×1,5/4, ratio-scale сравнивает две неизменные карты. Они обучают пропорции, но не решают направление изменения при перепечатке. Pending measure-distance даёт 1 см=1 км при уже заданном RF, без увеличения.', 'outbound':'Correct note RF1:100000 совпадает с общей конверсией в pending measure-distance, но не выбирает его действие и не выводит 3 км. Соседние задачи не содержат исходные 2 км/см и увеличение x2. Общая конверсия не подменяет требуемую новую операцию.','decision':'PASS: одна операция деления на 2; не три одинаковых вычисления в группе78–80.'}
]
peerpaths=[B/'author/candidate.json',ROOT/'docs/content-audits/question-quality-wave-7/process-v2-maps51-60-01a13d50/exact-language-recovery2-author-01a13d50/candidate.json',ROOT/'docs/content-audits/question-quality-wave-7/process-v2-maps51-60-01a13d50/source-hold3-new-solution-author-01a13d50/candidate.json',ROOT/'docs/content-audits/question-quality-wave-7/process-v2-maps81-90-01a13d50/author/candidate.json',B/'source-hold78-80-new-solution-author-01a13d50/peer-snapshot.json']
# Preserve actual whole cards and both before/proposed versions without treating snapshots as CURRENT.
peers={'actualCurrent':[{'sourceOrder':i+1,'card':c,'cardSHA256':h(c)} for i,c in enumerate(q) if i in [1,27,28,29,35,41,42] or 50<=i<=57 or 70<=i<=89], 'proposalAndHistoricalSnapshots':[{'path':str(p.relative_to(ROOT)),'byteSHA256':bh(p),'snapshot':load(p)} for p in peerpaths], 'scope':'Read relevant full CURRENT scale/index/coordinate/71–77/81–90 cards and relevant proposed scale2, scalegrid3,71–77,81–90 versions, including notes. Older embedded snapshot cards remain historical. No exhaustive 679-card quality claim.'}
save(OUT/'evidence/peer-comparison.json',peers)
entries=[]
ids=['maps-cartography-atlas-collection','maps-cartography-globe-sphere','maps-cartography-wall-map']
exact=load(B/'exact-apply-source-hold78-80-new-solution-01a13d50.json')
for j,id in enumerate(ids):
 c=byid[id]; applied=next(x for x in exact['applied'] if x['id']==id)
 assert h(c)==applied['afterHash']; assert c==applied['proposedCard']; assert c['difficulty']=='easy' and c['correctIndex']==3 and q.index(c)+1==78+j
 refs=[sources[0]] if j!=1 else sources[1:]
 literals=[('prompt_ordered_answers_key',{'prompt':c['prompt'],'answers':[a['text'] for a in c['answers']],'correctIndex':c['correctIndex']}),('explanation',c['explanation'])]+[('note'+str(i),a['note']) for i,a in enumerate(c['answers'])]
 groups=[{'group':name,'literal':literal,'literalSHA256':h(literal),'status':'PASS','grounds':grounds[j][i],'sourceClaims':refs,'conditionalInputs':'Fictional page coverage/scales, marker coordinates or print enlargement are explicit prompt assumptions; the external primary supports operations only.'} for i,(name,literal) in enumerate(literals)]
 assessments=[]
 for i,a in enumerate(c['answers']):
  triple={'prompt':c['prompt'],'answer':a['text'],'note':a['note']}
  assessments.append({'answerIndex':i,'fullPrompt':c['prompt'],'answer':a['text'],'note':a['note'],'isKey':i==3,'tripleSHA256':h(triple),'status':'PASS','answerAssessment':assess[j][i],'noteGrounds':grounds[j][i+2],'grammar':'Ответ естественно согласован с вопросом; имя/число совпадает с предоставленными данными. Русский текст понятен, нет требуемой смысловой правки.','sourceClaims':refs})
 entries.append({'id':id,'topicId':'maps-cartography','sourceOrder':78+j,'actualCurrentCard':c,'actualCurrentCardSHA256':h(c),'status':'PASS','fieldGroups':groups,'assessments':assessments,'easyAssessment':['Четыре короткие записи; простое исключение частичного покрытия и сравнение знаменателей без пространственных вычислений.','Четыре точки представляют четыре комбинации N/S и E/W; достаточно прочитать два базовых обозначения.','Одно деление 2 на 2; все единицы согласованы, точные данные без округления.'][j],'correctNoteAddsUsefulNewFact':grounds[j][5],'peerComparison':peer_findings[j],'sourceMetadata':'Название и URL соответствуют прочитанному первичному материалу; у globe основной link latitude, supplemental longitude проверен отдельно.','precisionUnits':'PASS: целые точные входы; нет округления, недостающего местоположения, измерения или масштаба.','unresolvedDefects':[]})
receipt={'schemaVersion':1,'readerRole':'OTHER independent reader, distinct from author 01a13e32-1076-7d13-b329-a1aab08cd3fd','baselineCommit':'3f1ebd1ce5f16cb7d37dd0a25476863fa0c6f130','branch':'codex/question-quality-wave-6','scope':'CURRENT78–80 new source-gap solution only','canonicalization':'json.dumps(sort_keys=True,separators=(comma,colon),ensure_ascii=False).encode(UTF-8); all source/file byteSHA from read_bytes, no CRLF normalization','sources':sources,'entries':entries,'counts':{'PASS':3,'HOLD':0,'fieldGroups':18,'individualAssessments':12},'history':'Original definition/source HOLD and earlier drafts remain retained at their existing paths; this PASS applies only to exact hashed new CURRENT cards. No inherited author/QA PASS.','peerEvidence':str((OUT/'evidence/peer-comparison.json').relative_to(ROOT)),'groupDiversity':'coverage filter plus ordinal comparison; hemisphere conjunction; linear enlargement ratio. Not three identical calculations.','qualityCredit':0,'coordinatorBindingRequired':True,'humanAcceptance':False,'integrationStamp':False,'checksPerformed':'Own receipt canonical hashes, exact CURRENT/application match, frozen ID/order/easy/key3, raw source byte integrity, 18 groups/12 assessments and references verified while producing evidence. No runtime/tests/build/audio, no catalogue/index/planning/claims mutations. Existing QA19/19 not inherited or rerun.','nextAction':'Coordinator binds this independent receipt to unchanged CURRENT hashes, adjudicates alongside author proof and existing affected QA, and preserves artifacts in Git. Reader has no Git mutation authorization.'}
save(OUT/'receipt.json',receipt)
assert len(entries)==3 and sum(len(e['fieldGroups']) for e in entries)==18 and sum(len(e['assessments']) for e in entries)==12
print(json.dumps({'receipt':str((OUT/'receipt.json').relative_to(ROOT)),'byteSHA256':bh(OUT/'receipt.json'),'cards':[(e['id'],e['actualCurrentCardSHA256'],e['status']) for e in entries],'counts':receipt['counts']},ensure_ascii=False,indent=2))
