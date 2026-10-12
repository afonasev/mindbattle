from pathlib import Path
from html.parser import HTMLParser
from pypdf import PdfReader
import json,hashlib,subprocess,os,collections
ROOT=Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle')
assert subprocess.check_output(['git','rev-parse','--show-toplevel'],cwd=ROOT,text=True).strip()==str(ROOT)
OUT=ROOT/'docs/content-audits/question-quality-wave-6/independent-pilot/resume-2026-10-12-winter4-safe-current'
AUTHOR='docs/content-audits/question-quality-wave-6/winter-sports/resume-2026-10-12-safe-author4/author-current-repair-receipt.json'
FROZEN='f96b17ccd33c628d3d32107f8a5b6c5ca4c4f7a0'
def blob(path):return subprocess.check_output(['git','show',FROZEN+':'+path],cwd=ROOT)
def sha(b):return hashlib.sha256(b if isinstance(b,bytes) else b.encode()).hexdigest()
def canonical(x,sort=False):return json.dumps(x,ensure_ascii=False,separators=(',',':'),sort_keys=sort)
def norm(s):return ' '.join(s.split())
class Parser(HTMLParser):
 def __init__(self,tag):super().__init__();self.tag=tag;self.rows=[];self.buf=None;self.skip=0
 def handle_starttag(self,t,a):
  if t in ('script','style','noscript'):self.skip+=1
  if t==self.tag:self.buf=[]
 def handle_endtag(self,t):
  if t==self.tag and self.buf is not None:self.rows.append(norm(' '.join(self.buf)));self.buf=None
  if t in ('script','style','noscript'):self.skip=max(0,self.skip-1)
 def handle_data(self,d):
  if self.buf is not None and not self.skip:self.buf.append(d)
def rows(b,name):
 p=Parser('tr' if name.startswith('iihf') else 'p');p.feed(b.decode());return p.rows
r=json.loads(blob(AUTHOR));topicBytes=blob('src/content/topics/winter-sports.json');topic=json.loads(topicBytes)
assert r['agentIdentity']=='01a12d03-dca8-7300-bb0f-e5feaef03cc0'
assert len(r['cards'])==4
cardsById={c['id']:c for c in topic['questions']}
analyses={
'winter-sports-007':[
'Канты непосредственно взаимодействуют со снегом и передают боковые усилия; ботинок и крепление передают управление, палки дают опору. Поэтому при прямом чтении вопроса ключ единственный. Все варианты реальные знакомые части снаряжения; нет прежнего редкого интерфейса или подсказки названием. Факт приемлем для Easy внутри большой группы горнолыжников.',
'Справка относится к ботинку: плотный охват стопы и передача движения проверены в определении FIS, это самостоятельные функции обуви.',
'Справка даёт собственную функцию крепления — освобождение при заданных нагрузках; определение на физической/печатной странице 24 действительно поддерживает текст.',
'Справка правильного ответа добавляет материал и износостойкость к основному факту о сцеплении. Пересечение с объяснением допустимо; это не голый повтор ключа.',
'Запрет металлических корзин — конкретный полезный факт о палках, прямо в разделе Ski poles на странице 12. Он не обязан доказывать неверность альтернативы.',
'Передача боковых усилий на странице 16 объясняет удержание поворота. Русский текст понятен, короток; это умеренная механическая интерпретация определения FIS, а не неверная цитата о стоппере.'
],
'winter-sports-008':[
'Сочетание короткой и произвольной программ отличает фигурное катание среди этих четырёх видов. Альтернативы действительно имеют судейскую оценку исполнения; программа для них могла бы казаться правдоподобной незнакомому зрителю. Ключ не выдаётся абсурдом. Уточнение про ритм-танец есть в объяснении; вопрос не утверждает, что все дисциплины используют название короткая программа. Easy — широко узнаваемая структура трансляций.',
'Дальность и стиль — собственные компоненты оценки прыжка с трамплина; полный абзац 10 подтверждает их сложение.',
'Разнообразие, сложность, стиль и исполнение — собственные критерии хафпайпа; в свежей версии страницы абзац 11 сохраняет все эти признаки.',
'Справка точно различает могул и дуал-могул: абзац 9 даёт 60% за повороты и 20% за скорость; соседний абзац 10 имеет другие доли и не используется.',
'Одиночное катание действительно имеет номинальную длительность короткой программы 2:40 и семь элементов. Источник допускает плюс/минус 10 секунд; текст карточки читается как номинальная длительность, не как требование точного времени без допуска. Это добавляет факт сверх prompt/key.',
'Полный абзац 7 и дальнейшие абзацы 8–13 подтверждают две программы и различие названий в танцах. Объяснение короткое и корректно уточняет обобщённый вопрос.'
],
'winter-sports-017':[
'В классической индивидуальной гонке ключ — минута за промах — подтверждён абзацем 9. Штрафной круг 150 м правдоподобен как реальный штраф в соседнем формате; 30 секунд — правдоподобная временная величина; километр — завышенная, но понятная дистанционная альтернатива, не грамматическая подсказка. Easy допустим для многочисленной аудитории биатлонных трансляций. Новый основной факт отличается от определения биатлониста в 014.',
'Двадцать мишеней и чередование позиций прямо подтверждены полным абзацем индивидуальной гонки. Это полезное расширение условий той гонки, где применяется правильный временной штраф, сверх bare key.',
'Справка связана с собственной альтернативой — кругом 150 м — и называет формат, где этот штраф реально применяется. Содержательно полезна и прямо подтверждена абзацем 10.',
'Факт стартового интервала 30 секунд подтверждён абзацем 9 в олимпийском контексте. Но вариант говорит о добавлении 30 секунд к результату: справка описывает стартовую процедуру, а не временной штраф или его применение. Совпадение числа не обеспечивает содержательную связь с собственным вариантом. FAIL editorial binding, не source-load failure.',
'Пять кругов по 4 км у мужчин подтверждены абзацем 9. Но вариант — дополнительный штрафной круг 1 км; справка про основные круги 4 км не даёт проверенный факт о таком круге и не поясняет его. Это другой объект/дистанция в общей гонке; FAIL own-option connection.',
'Оба предложения подтверждены разными полными абзацами 9 и 10. Объяснение различает индивидуальную гонку и спринт, не переносит штрафной круг на индивидуальную и остаётся коротким.'
],
'winter-sports-019':[
'Понятие гола широко известно и соответствует Easy; все четыре варианта — реальные хоккейные термины, ключ один. Но по-русски линию пересекает шайба, не бросок. Дополнительный условный оборот не создаёт отдельного знания: основной факт совпадает с 025 «взятие ворот называется голом». Поэтому FAIL Russian precision и confirmed semantic duplicate, несмотря на поддержку общего понятия глоссарием.',
'Справка относится к офсайду и передаёт первую часть определения строки 72. Синяя линия в атакующем контексте понятна; полезный собственный факт, не подсказка правильного ответа.',
'Полная строка 62 поддерживает исключение при первом касании атакующей команды, но в карточке нет определения броска для проброса. «После такого броска» ссылается на prompt о попадании в ворота; туда исключение проброса не относится. Получилась неполная и неоднозначная самостоятельная справка. FAIL Russian/context binding, хотя исключение в оригинале реально.',
'Центральное вбрасывание после гола прямо подтверждено строкой 18; добавляет процедурный факт сверх названия гола. Совпадение этого факта с объяснением или другой карточкой не делает саму справку bare key.',
'Строка 41 прямо подтверждает начало периода и возобновление после свистка. Справка о собственной альтернативе, полезна и кратка.',
'Источник по-английски употребляет shot attempt, но механическое «бросок ... пересёкший линию» по-русски неверно обозначает физический объект. Нужна шайба, полностью пересёкшая линию между стойками; слово «очко» также менее точно для засчитанного гола. FAIL Russian precision. Это не прежняя проблема Easy Mark IV.'
]}
failed={('winter-sports-017','note2'),('winter-sports-017','note3'),('winter-sports-019','prompt-key'),('winter-sports-019','note1'),('winter-sports-019','explanation')}
fetch=json.loads((OUT/'fetch-manifest.json').read_text());fm={Path(x['path']).name:x for x in fetch}
result=[];sourceChecks=[]
for ac in r['cards']:
 c=cardsById[ac['questionId']];assert sha(canonical(c))==ac['cardCanonicalSha256']
 fields=[]
 for index,af in enumerate(ac['fields']):
  name=af['field'];lit=canonical([c['prompt'],c['correctIndex'],c['answers'][c['correctIndex']]['text']]) if name=='prompt-key' else c['explanation'] if name=='explanation' else c['answers'][int(name[-1])]['note']
  assert lit==af['currentLiteral'] and sha(lit)==af['literalSha256']
  proofs=[]
  for ap in af['proofs']:
   fname=Path(ap['rawCapture']).name;b=(ROOT/ap['rawCapture']).read_bytes();assert b==blob(ap['rawCapture']);assert sha(b)==ap['rawSha256']
   fresh=(OUT/'sources'/fname).read_bytes();fr=fm[fname];assert fr['exitCode']==0 and fr['captureUrl'].startswith('200|');assert sha(fresh)==fr['sha256']
   loc=ap['locator'];n=loc.get('visibleParagraphIndex',loc.get('zeroBasedTrIndex'))
   if fname.endswith('.pdf'):
    assert b.startswith(b'%PDF-') and fresh.startswith(b'%PDF-')
    n=loc['physicalPdfPage'];quoted=norm(PdfReader(OUT/'sources'/fname).pages[n-1].extract_text());frozenPassage=norm(PdfReader(ROOT/ap['rawCapture']).pages[n-1].extract_text());readerloc=dict(physicalPdfPage=n,printedPdfPage=str(n),section={'12':'1.3 Ski poles','16':'3.1.2.1 Definition','24':'3.1.4.1 Definition','25':'3.2.1 Definition'}[str(n)])
   else:
    assert b.lstrip().lower().startswith((b'<!doctype',b'<html'));quoted=rows(fresh,fname)[n];frozenPassage=rows(b,fname)[n];readerloc=dict(loc)
   # Compare quote content after removing whitespace and HTML table separator only; no semantic paraphrase check hidden here.
   flat=lambda s:''.join(s.replace('|','').split())
   assert flat(ap['quotedPassage']) in flat(quoted),(c['id'],name,'fresh passage missing')
   assert flat(ap['quotedPassage']) in flat(frozenPassage),(c['id'],name,'frozen passage missing')
   assert sha(ap['quotedPassage'])==ap['quotedPassageSha256']
   assert sha(canonical(loc,True))==ap['locatorSha256']
   proofs.append(dict(sourceUrl=ap['actualUrl'],captureUrl=fr['captureUrl'].split('|',2)[2],rawType=fr['captureUrl'].split('|',2)[1],captureFormat='complete original HTTP response body bytes; independent curl -L --fail download, no normalization',independentRawCapture=fr['path'],independentRawSha256=sha(fresh),independentRawBytes=len(fresh),frozenAuthorRawCapture=ap['rawCapture'],frozenAuthorRawSha256=sha(b),frozenGitBlob=subprocess.check_output(['git','rev-parse',FROZEN+':'+ap['rawCapture']],cwd=ROOT,text=True).strip(),locator=readerloc,locatorSha256=sha(canonical(readerloc,True)),quotedPassage=quoted,quotedPassageSha256=sha(quoted),frozenPassageAtSameLocator=frozenPassage,frozenPassageAtSameLocatorSha256=sha(frozenPassage),authorDeclaredQuote=ap['quotedPassage'],authorDeclaredQuoteSha256=sha(ap['quotedPassage']),quoteSupportedInBothVersions=True,factualSourceVerdict='PASS'))
  fields.append(dict(field=name,currentLiteral=lit,literalSha256=sha(lit),verdict='FAIL' if (c['id'],name) in failed else 'PASS',sourceVerdict='PASS',substantiveRead=True,manualIndividualAnalysis=analyses[c['id']][index],proofs=proofs))
 result.append(dict(questionId=c['id'],difficulty=c['difficulty'],correctIndex=c['correctIndex'],frozenCard=c,cardCanonicalSha256=sha(canonical(c)),sortedCardSha256=sha(canonical(c,True)),verdict='FAIL' if any(f['verdict']=='FAIL' for f in fields) else 'PASS',easyVerdict='PASS',easyManualAnalysis=analyses[c['id']][0],fields=fields))
partners=[]
for id in ['winter-sports-014','winter-sports-025']:
 p=cardsById[id];partners.append(dict(questionId=id,prompt=p['prompt'],key=p['answers'][p['correctIndex']]['text'],canonicalCardSha256=sha(canonical(p)),purpose='Targeted fact comparison only; no re-certification or editing of protected partner.'))
report=dict(agentIdentity=os.environ['CODEX_THREAD_ID'],nativeIdentityEvidence='CODEX_THREAD_ID and CODEX_SESSION_ID from reader process environment',nativeSessionId=os.environ['CODEX_SESSION_ID'],role='independent reader',readAt='2026-10-12',frozenContentCommit='d898e6c',frozenReceiptCommit=FROZEN,authorAgentIdentity=r['agentIdentity'],authorReceiptPath=AUTHOR,authorReceiptSha256=sha(blob(AUTHOR)),authorProvenance='Actual new author receipt frozen in Git; historical daeb3ba draft and prior failed reader receipt are not adopted as current reading/verdict.',topicPath='src/content/topics/winter-sports.json',topicSha256=sha(topicBytes),topicGitBlob=subprocess.check_output(['git','rev-parse',FROZEN+':src/content/topics/winter-sports.json'],cwd=ROOT,text=True).strip(),canonicalRecipes=r['canonicalRecipes'],readerQuoteRecipe='SHA256 UTF-8 whitespace-collapsed complete paragraph/table row or full physical PDF-page extracted text; no trailing newline. HTML data nodes joined with one space; no script/style/noscript.',scopeExactIds=[c['questionId'] for c in result],scopeCount=4,fieldCount=24,cardCounts=dict(collections.Counter(c['verdict'] for c in result)),fieldCounts=dict(collections.Counter(f['verdict'] for c in result for f in c['fields'])),sourceCounts={'PASS':24,'FAIL':0},easyRule=r['cards'][0]['difficultyRuleResolution'],notesRule=r['cards'][0]['notesRule'],cards=result,duplicateComparisons=[dict(pair=['winter-sports-017','winter-sports-014'],verdict='DISTINCT',testedFact='minute-per-miss penalty in individual vs athlete combining skiing and shooting',resolved=True),dict(pair=['winter-sports-019','winter-sports-025'],verdict='CONFIRMED_DUPLICATE',testedFact='hockey puck entering goal / counted taking of goal is called goal',resolved=False,reason='Same primary fact and same keyed term; crossing-line wording does not supply a distinct tested fact. Matching correct-note centre face-off reinforces overlap. Recording alone does not resolve duplication.')],targetedPartners=partners,duplicateBoundary='Targeted prompt scan of Winter/Sports only and direct comparison of named 014/025; no other2000 cards and no global duplicate certification.',sourceRead='Complete original downloads preserved. All relevant full HTML paragraphs/table rows read with surrounding sport context; PDF physical pages 12/16/24/25 independently read, page labels equal physical indices, cover/TOC checked. No HTML landing page treated as PDF. Full PDF of 35 pages captured; no claim that unrelated geometry/helmet sections were substantively audited.',preservation='Only independent evidence and scoped .gitattributes. No content/reviews/planning/claim/protected96 changes; foreign Middle/Architecture and primary incident preserved.',checksScope='Evidence-only: exact four canonical/literal hashes, 24 independently analysed fields, both frozen/fresh passage and locator binding, raw type/HTTP validation, Git byte round trip and diff checks. No tests/runtime/build/deploy/full-suite.',pilotGate='Not passed: 2 PASS, 2 FAIL. Remaining28 stay protected; coordinator adjudication/author repair needed.')
(OUT/'reader-receipt.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['cardCounts','fieldCounts','sourceCounts']},indent=2))
