"""Serialize manual reader decisions, verify bindings only; never infer editorial truth."""
import json, hashlib, subprocess, os, re
from pathlib import Path
from html.parser import HTMLParser
from collections import Counter
ROOT=Path.cwd(); OUT=Path(__file__).parent
AUTHOR=Path('docs/content-audits/question-quality-wave-6/architecture/resume-2026-10-12-rework21')
FREEZE='dc8e286'; CONTENT='912b2b8'; ID='01a12cdd-6cde-7430-9f66-547d443efd24'
def git(*a): return subprocess.check_output(['git',*a])
def sha(b):return hashlib.sha256(b).hexdigest()
def dump(name,obj): (OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def canonical(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
class Text(HTMLParser):
 def __init__(self):super().__init__();self.skip=0;self.parts=[]
 def handle_starttag(self,t,a):self.skip+=t in ('script','style')
 def handle_endtag(self,t):self.skip-=t in ('script','style')
 def handle_data(self,d):
  if not self.skip:self.parts.append(d)
def norm(b):
 t=Text();t.feed(b.decode());return re.sub(r'\s+',' ',' '.join(t.parts)).strip()
assert os.environ.get('CODEX_THREAD_ID')==ID
revision=git('rev-parse',FREEZE).decode().strip(); contentRevision=git('rev-parse',CONTENT).decode().strip()
raw=git('show',f'{revision}:{AUTHOR}/author-receipt.json');receipt=json.loads(raw)
(OUT/'author-receipt-frozen.json').write_bytes(raw)
oldrev=git('rev-parse','212fb9f').decode().strip();oldraw=git('show',f'{oldrev}:{AUTHOR}/author-receipt.json')
(OUT/'author-receipt-212fb9f-frozen.json').write_bytes(oldraw)
(OUT/'.gitattributes').write_text('*-frozen.json -text\n')
rulesPath=Path('/Users/eaafonasev/Projects/mindbattle-planning/docs/GAME_SPEC.md'); rules=rulesPath.read_bytes(); ruleLines=rules.decode().splitlines()
(OUT/'approved-rules-frozen.txt').write_text('\n'.join(f'{n}: {ruleLines[n-1]}' for n in range(137,155))+'\n')
(OUT/'.gitattributes').write_text('*-frozen.json -text\napproved-rules-frozen.txt -text\n')
rule=lambda n:{'path':str(rulesPath),'line':n,'quote':ruleLines[n-1], 'documentSha256':sha(rules)}
# These analyses and verdicts were manually authored after reading complete originals.
manual={
'architecture-tower-bridge-city':[
('PASS','LPC Display Window задаёт большую застеклённую часть магазина, extending from pier to pier. Русское между простенками передаёт эту геометрию; ключ витрина, index1, точен. Вопрос easy о знакомой магазинной архитектуре. Все четыре ответа — реальное остекление фасада; эркер может быть большим, фрамуга и боковая секция реально встречаются в торговом фасаде. Условие больше не противопоставляет верх фрамуги и витринную функцию; отличие требует узнавания витрины, не абсурдного сноса или категории иного предмета.'),
('PASS','Bay Window — выступающая оконная форма, опирающаяся на землю либо иную опору. Справка эркерного окна сообщает именно выступ и опору, без фактов о витрине; русский смысл соответствует термину.'),
('PASS','Display Window имеет display of goods и daylight. Это два полезных назначения сверх спрашиваемого названия крупного остеклённого проёма. Повтор части определения допустим: справка не ограничивается prompt/key; совпадение с explanation не дефект.'),
('PASS','Transom имеет отдельное значение window above the transom bar of a door. Вариант с уточнением над дверью и его справка относятся к одному значению; горизонтальная перекладина — корректный перевод bar.'),
('PASS','Sidelight — fixed glass flanking a door. Справка даёт неподвижность и положение рядом с дверью, а не назначение витрины. Грамматика образует ... секция верна: подлежащее секция.'),
('PASS','Display Window подтверждает положение below the transom, показ товаров, daylight и visibility into commercial space. Два коротких предложения объясняют название и назначения; чтение укладывается в 30 секунд.')],
'architecture-sydney-opera-house-country':[
('HOLD','UNESCO прямо указывает three groups of interlocking vaulted shells, значит число3 и index1 фактически правильны. Четыре соседних числа — параллельные варианты без грамматического ключа. Но задан easy: точное количество групп инженерных оболочек — второстепенная деталь известного здания. В условии нет картинки, схемы либо исходных величин для содержательного вывода; известность театра не делает количество его групп широко известным взрослой культурной группе. Это редакторский HOLD факта для фиксированного easy, не предложение перенести слот или упростить hard.'),
('FIX','Число две исключается непосредственно UNESCO three groups. Фактология PASS, но вся справка говорит о правильных трёх группах, а не даёт полезный факт о варианте две: только повторяет числовой ключ в отрицательной форме.'),
('FIX','UNESCO подтверждает три группы. Правильная справка только повторяет число и формулировку групп из prompt/key. Она не добавляет факта об их назначении, размещении или устройстве; наличие назначения в explanation не исправляет эту отдельную note.'),
('FIX','UNESCO подтверждает, что четыре — неверный ответ. Справка целиком повторяет правильные три и отрицание четырёх; самостоятельного полезного факта о данном варианте не содержит.'),
('FIX','UNESCO подтверждает, что пять — неверный ответ. Справка целиком повторяет ключ три и отрицание пяти, без самостоятельного объяснения варианта.'),
('FIX','UNESCO прямо связывает три группы с two main performance halls and a restaurant; оба добавочных факта и смысл перекрытия верны. Одно предложение с точкой с запятой остаётся одним предложением. Это нарушает действующее правило от двух до четырёх предложений; содержательная фактология и краткость PASS.')],
'architecture-kremlin-meaning':[
('PASS','Pitt определяет true pilaster как rectangular vertical masonry, projects only slightly from wall. Условие описывает именно пилястру, index0. Это medium: нужно тематическое различение опор. Колонна, контрфорс и консоль являются архитектурными опорами; они не абсурдны, а признаки сечения, выступа и направления отличают их по знанию темы. Термин пирс удалён.'),
('PASS','Pitt подтверждает rectangular element of vertical masonry which projects only slightly. Вопрос уже сообщает прямоугольность, вертикальность и малый выступ, но не конструкцию кладки. Справка добавляет проверенное конструктивное уточнение элемент кладки к данному описанию опоры. Это небольшой, но полезный факт об архитектурном элементе; не требую полностью новой темы, базы и капители именно в note или отсутствия overlap с главным фактом. Утверждённое правило разрешает частичное повторение при полезном добавлении.'),
('PASS','LPC Column — vertical cylindrical support. Это полезное собственное определение колонны и отличие от прямоугольной пристенной пилястры; краткая типологическая формулировка верна в контексте глоссария.'),
('PASS','Illinois Buttress — exterior masonry opposing lateral thrust of arch or vault. Наружная массивная опора стены, воспринимающая боковой распор свода, передаёт этот конструктивный смысл; справка раскрывает назначение контрфорса.'),
('PASS','LPC Corbel — projecting upward and outward from wall, supporting horizontal member. Консоль названа в русском широком смысле выступающего опорного элемента, а не ложным переводом пирса. Текст описывает именно опорный выступ и что он поддерживает; источник LPC Console также подтверждает projecting bracket supporting horizontal member.'),
('PASS','Pitt сообщает both capital and base. Два предложения: идентификация пилястры и дополнительное устройство классической формы. Справка правильной note не подменяется этим explanation; здесь отдельно source/editorial PASS.')],
'architecture-bagan':[
('PASS','Maryland Addition увеличивает размер здания либо добавляет к нему объём. Ключ Строительство пристройки/index3 соответствует. Easy проверяет знакомое различие строительных работ; все четыре — операции с существующим зданием. Ремонт, реставрация, перепланировка могут в бытовом понимании входить в расширение и реконструкцию, но названное добавление нового объёма выделяет пристройку. Удалён очевидно противоположный снос. Это определительный easy, а не запрещённая терминологическая ловушка или буквальный повтор названия варианта в prompt.'),
('PASS','Maryland Repair возвращает sound/acceptable operation, serviceability or appearance. Все три русских свойства проверены; справка характеризует именно ремонт.'),
('PASS','LPC Restoration — returning building or parts as nearly as possible to original form and condition. Справка точно сообщает возвращение исходного вида; относится к реставрации, не к пристройке.'),
('PASS','Maryland Alteration может change floor plan without increasing size. Справка ограничена изменением внутренних помещений и использует может; не объявляет всякую реконструкцию безразмерной. Это факт о выбранном виде изменения планировки.'),
('PASS','Maryland Addition называет porch и attached garage. Примыкающий гараж и крыльцо — два проверенных примера сверх спрашиваемого названия работ. Их повтор в explanation разрешён, не требует нового независимого факта.'),
('PASS','Addition подтверждает увеличение дома и два примера. Два предложения дают причину выбора и познавательные примеры, без неподтверждённых инженерных обобщений.')],
'architecture-summer-palace':[
('PASS','UNESCO прямо называет Summer Palace masterpiece of Chinese landscape garden design; index3 единственный верный. Easy — знакомая культурная традиция китайского императорского ансамбля. Французский регулярный, персидский, японский и китайский ландшафтный — четыре реально существующие традиции садового проектирования, одинаковой категории. Пекин помогает вспомнить происхождение ансамбля, но не повторяет слово Китайский и не логически запрещает импортные стили: сама география не определяет садовую типологию. Утверждённые правила допускают узнавание культурно известного факта в easy; не ввожу запрет национальных вариантов или географического контекста. Все четыре русские подстановки понимаются как названия традиций, гендерных подсказок нет.'),
('PASS','UNESCO Versailles justification описывает French-style garden как систему axial pathways, low hedges, flower beds, streams, lakes, fountains. Осевые дорожки и партеры передают регулярную композицию; справка даёт характерные элементы именно французского регулярного сада.'),
('PASS','UNESCO Persian Garden прямо говорит four sectors и water for irrigation and ornamentation; в justification often divided into four sections. Русское традиционно удачно не превращает эту особенность в безусловное правило для каждого сада. Даны две полезные характеристики своего варианта.'),
('PASS','UNESCO Kyoto описывает art of Japanese gardens, influenced landscape gardening the world over; justification называет Kyoto main centre. Справка о развитии и влиянии искусства японских садов относится к японскому варианту, не к китайскому дворцу.'),
('PASS','UNESCO Summer Palace подтверждает Chinese landscape garden и сочетание natural hills/open water с pavilions/halls/palaces/temples/bridges. Перечень композиционных элементов добавляет полезное знание сверх названия традиции в prompt/key. Перекрытие с explanation разрешено.'),
('FIX','UNESCO подтверждает классификацию и все перечисленные естественные/искусственные элементы; русский текст ясен и краток. Но двоеточие соединяет части одного предложения. Действующее правило требует от двух до четырёх предложений. Это локальный редакторский FIX explanation, не factual HOLD и не запрет overlap с correct note.')]
}
cardRules={'architecture-sydney-opera-house-country':{0:[138],1:[143,145],2:[143],3:[143,145],4:[143,145],5:[152]},'architecture-kremlin-meaning':{},'architecture-summer-palace':{5:[152]}}
current=json.loads(git('show',f'{contentRevision}:src/content/topics/architecture.json'))
actual=json.loads(Path('src/content/topics/architecture.json').read_bytes())
proofCheck=[]; sources={}; cards=[]
for c in receipt['cards']:
 q=next(x for x in current['questions'] if x['id']==c['questionId']); live=next(x for x in actual['questions'] if x['id']==q['id'])
 assert q==live==c['currentCard'];assert sha(canonical(q))==c['cardCanonicalSha256']
 fields=[]
 for i,(old,(verdict,analysis)) in enumerate(zip(c['fields'],manual[q['id']])):
  f=old['field']; literal=json.dumps([q['prompt'],q['correctIndex'],q['answers'][q['correctIndex']]['text']],ensure_ascii=False,separators=(',',':')) if f=='prompt-key' else q['explanation'] if f=='explanation' else q['answers'][int(f[-1])]['note']
  assert literal==old['literal'];assert sha(literal.encode())==old['literalSha256']
  proofs=[]
  for a in old['proofs']:
   path=(AUTHOR/a['rawCapture']).resolve().relative_to(ROOT); rawSource=git('show',f'{revision}:{path}'); liveSource=path.read_bytes()
   assert rawSource==liveSource and sha(rawSource)==a['rawCaptureSha256']
   if path.suffix=='.json':
    data=json.loads(rawSource);assert data['total_count']==1 and len(data['results'])==1
    readable=data['results'][0][a['locator']];match=a['passage'] in readable;mode='complete JSON record field text; verbatim Unicode quote'
   else:readable=norm(rawSource);match=re.sub(r'\s+',' ',a['passage']).strip() in readable;mode='complete original HTML parsed without script/style; whitespace-only rendering'
   assert match and sha(a['passage'].encode())==a['passageSha256']
   blob=git('rev-parse',f'{revision}:{path}').decode().strip()
   proof={k:a[k] for k in ('sourceClass','title','url','rawCaptureSha256','captureFormat','locator','passage','passageSha256')}
   proof.update(rawCapture=str(path),sourceFreezeRevision=revision,frozenGitBlob=blob,readerIdentity=ID,captureMethod='Original retained author HTTP/API capture, independently reopened from frozen Git and working raw bytes; complete English prose inspected before verdict.',quoteMatchMode=mode,quotedPassageSha256=a['passageSha256'])
   proofs.append(proof)
   sources[str(path)]={'path':str(path),'byteCount':len(rawSource),'rawSha256':sha(rawSource),'frozenGitBlob':blob,'frozenRevision':revision,'workingEqualsFrozenGit':True,'readerIdentity':ID,'substantiveReading':'All visible substantive text of complete original HTML, or all English prose fields of complete original UNESCO record; no search result, error response, or script used as factual proof.'}
   proofCheck.append({'questionId':q['id'],'field':f,'source':str(path),'passageMatch':match,'rawBytesMatch':True})
  fields.append({'field':f,'literal':literal,'actualLiteral':literal,'literalSha256':sha(literal.encode()),'sourceVerdict':'PASS','editorialVerdict':verdict,'verdict':verdict,'claimAnalysis':analysis,'substantiveRead':True,'substantiveReadBy':ID,'rules':[rule(n) for n in cardRules.get(q['id'],{}).get(i,[])],'proofs':proofs})
 cv='HOLD' if any(f['verdict']=='HOLD' for f in fields) else 'FIX' if any(f['verdict']=='FIX' for f in fields) else 'PASS'
 cards.append({'questionId':q['id'],'currentCard':q,'cardCanonicalSha256':sha(canonical(q)),'sourceVerdict':'PASS','editorialVerdict':cv,'verdict':cv,'fields':fields,'fieldCounts':dict(Counter(f['verdict'] for f in fields))})
assert len(cards)==5 and sum(len(c['fields']) for c in cards)==30
out={'role':'independent-source-editorial-reader','agentIdentity':ID,'authorAgentIdentity':receipt['agentIdentity'],'readDate':'2026-10-12','branch':git('branch','--show-current').decode().strip(),'sourceFreezeRevision':revision,'contentFreezeRevision':contentRevision,'authorReceipt':{'originalPath':str(AUTHOR/'author-receipt.json'),'frozenCopy':'author-receipt-frozen.json','rawSha256':sha(raw),'gitBlob':git('rev-parse',f'{revision}:{AUTHOR}/author-receipt.json').decode().strip()},'originalAuthorRevision':oldrev,'decisionMethod':'Manual native reader analysis in this chat after complete original source reads. Serializer checks hashes and quote bindings only. Author PASS not inherited. No child agent, source editing, content editing or planning claim.','cards':cards,'summary':{'cards':dict(Counter(c['verdict'] for c in cards)),'fields':dict(Counter(f['verdict'] for c in cards for f in c['fields'])),'sourceCards':{'PASS':5},'sourceFields':{'PASS':30}},'limits':'No root certification, human/runtime/visual/device/audio acceptance, full suite, build, push, merge, deploy or archive. Sixteen unprepared and other79 architecture cards protected; no content edits.'}
dump('independent-receipt.json',out);dump('source-readback.json',{'sources':list(sources.values()),'sourceCount':len(sources),'proofChecks':proofCheck,'fieldCount':30,'verdictCreationByScript':0})
# Mechanical preservation checks, not editorial review of protected cards.
base=json.loads(git('show','2135370f4c76e3dcddff087e04a0bacd2389adb4:src/content/topics/architecture.json'))
a=actual['questions'];b=base['questions'];assert [(x['id'],x['difficulty'],x['correctIndex']) for x in a]==[(x['id'],x['difficulty'],x['correctIndex']) for x in b]
quotas=Counter(q['difficulty'] for q in a);slots={d:dict(Counter(str(q['correctIndex']) for q in a if q['difficulty']==d)) for d in quotas}
assert quotas=={'easy':40,'medium':40,'hard':20};assert all(set(v.values())==({5} if d=='hard' else {10}) for d,v in slots.items())
dump('scope-preservation.json',{'contentFile':'src/content/topics/architecture.json','currentRawSha256':sha(Path('src/content/topics/architecture.json').read_bytes()),'contentFrozenGitBlob':git('rev-parse',f'{contentRevision}:src/content/topics/architecture.json').decode().strip(),'workingEqualsFrozenContent':actual==current,'immutableBaseline':'2135370f4c76e3dcddff087e04a0bacd2389adb4','idOrderDifficultyCorrectIndexUnchanged':True,'quotas':dict(quotas),'correctIndexSlots':slots,'contentEditsByReader':0,'remaining16EditorialReads':0,'protected79EditorialReads':0,'outside2000Edits':0})
dump('qa-scope.json',{'impact':'Evidence-only independent review. No runtime/content/tooling route changed.','checks':['python3 <owned>/bind_review.py: source bytes, literal/card hashes, all30 quote matches, native identity, quota/invariant checks','git diff --cached --check: exact staged owned evidence','git show committed evidence/source blobs: byte roundtrip'], 'reason':'Minimum sufficient checks for serialized manual evidence and immutable source preservation; no test runner or build necessary.','fullSuite':'NotRun; not authorized','build':'NotRun; not needed','deploy':'NotRun; not authorized'})
print(json.dumps(out['summary'],ensure_ascii=False));print('sources',len(sources),'fields',len(proofCheck))
