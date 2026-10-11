"""Mechanical binding of explicit reader decisions; never decides editorial verdicts."""
import json, hashlib, subprocess, os, re
from pathlib import Path
from html import unescape
OUT=Path(__file__).parent
BASE=Path('docs/content-audits/question-quality-wave-6/middle-ages/resume-2026-10-12-rework28')
AUTHOR_COMMIT='d375f6c82537b38db587a4d3d086754e30eb9e0d'
READER='01a12cb1-4487-7d91-9bd9-8b07a103edb8'
assert os.environ['CODEX_THREAD_ID']==READER

def sha(b):return hashlib.sha256(b).hexdigest()
def canonical(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def gitbytes(p,commit=AUTHOR_COMMIT):return subprocess.check_output(['git','show',f'{commit}:{p}'])
def save(name,v):(OUT/name).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
# These 30 decisions were made after reading preserved originals, not inferred from author verdicts.
DECISIONS={
'middle-ages-precaria':[
('FIX','Ключ подтверждён TLFi: precaria — acte de requête. Но вопрос просит название прошения: аллод есть владение, бенефиций — пожалование, эмфитевзис — вещное право. Они относятся к земельному праву, но не к запрошенной категории прошений. Для hard это оставляет ключ единственным грамматически/семантически точным типом; нужны правдоподобные акты обращения либо другой проверенный hard-факт без категориального исключения.'),
('PASS','ALLEU в разделе DR. FÉOD. прямо определён как унаследованная собственность без обязательств/платежей. Справка сообщает собственный факт об аллоде; не приписывает ему обмен на службу.'),
('PASS','Полная строка fief (fee) в UC Davis называет benefice пожалованием земли или должности за поддержку и службу. Это собственный содержательный факт о варианте. CNRTL II A 1 отдельно описывает франкское военное пожалование; широкий глоссарный смысл справки не противоречит ему.'),
('PASS','EMPHYTÉOSE прямо перечисляет cessible, bien foncier и redevance annuelle. Все три свойства текущей русской справки подтверждены; она не называет это собственностью на чужую землю.'),
('PASS','Полный HIST. DU DR. в PRÉCAIRE говорит о charges modiques ou nulles и отсутствии военных обязательств в отличие от bénéfice. Справка имеет собственный факт; допустимое пересечение с основным вопросом не является дефектом.'),
('PASS','TLFi прямо различает просьбу precaria и плодоносящее имущество precarium. Два русских предложения сохраняют различие, не заявляют наследственную собственность или обязательную военную службу.')],
'middle-ages-dower':[
('FIX','DOUAIRE DR. ANC. подтверждает ключ и условие о пережившей мужа жене. Буквальная вдовья подсказка в ключе удалена. Но примогенитура — старшинство рождения детей, апанаж — компенсация принцу за наследование короны; это не альтернативные брачные имущественные установления. Дистракторы по-прежнему из разных запрошенных категорий. Douaire также единственный латинский ответ среди русских: заметная неоднородность. Нужны четыре сопоставимых брачных/супружеских права, без буквального вдовьего cue, при сохранении medium.'),
('PASS','Определение DR. ANC. даёт именно usufruit, назначение мужем при браке и пользование при пережитии мужа. Повтор главного объяснения разрешён: note сообщает факт о собственном варианте.'),
('FIX','Источник верен: priorité de naissance entraînant des droits, в частности наследственные. Русское «давала старшинство рождения» меняет причинность: институт не создавал возрастное старшинство. Следует сказать, что право примогенитуры давало старшему ребёнку преимущества при наследовании. Сохранить фактическое отличие от брачных имущественных прав.'),
('PASS','Первое определение APANAGE и следующий исторический пример прямо подтверждают фьеф принцу крови в компенсацию за наследование короны старшим. Факт собственный, конкретный, без неподтверждённой независимости владения.'),
('PASS','DOT A и En partic. подтверждают имущество, отложенное для брака. Формулировка краткая, но содержательная, не пустой ярлык. В основном значении речь об имуществе, которое женщина приносит в брак.'),
('PASS','Два предложения воспроизводят условия douaire и противопоставляют их приданому при браке. Оба определения реально прочитаны; утверждения о Magna Carta здесь больше нет. Источник для такой отменённой исторической справки не требуется.')],
'middle-ages-palimpsest':[
('PASS','Полный Palimpsest в Leiden описывает снятие старого текста, новый слой, слабое закрепление новых чернил и проступание старого. Все четыре ответа — последовательные именные подписи рукописей или отношений между ними: апограф, автограф, exemplar можно спутать при незнании способа изготовления. Нет падежного/родового cue. Сохраняемый hard защищаем точной кодикологической особенностью поверхностного слоя и исключением копии, авторского свидетельства и образца через контекст, а не случайными именами.'),
('PASS','Helsinki Apograph полный основной текст определяет новую рукопись переписчика по более раннему exemplar. Русская справка верно передаёт отношение копии и образца; не добавляет свойств автографа.'),
('PASS','Leiden Palimpsest подтверждает оба физических свойства повторно использованного листа. Это собственный проверяемый факт о палимпсесте; пересечение с prompt/explanation допустимо.'),
('PASS','Helsinki Autograph определяет witness written by the author himself. В текстологическом контексте русское «свидетель текста» корректно. Не смешано с бытовой подписью.'),
('PASS','Факт о книге/рукописи-образце подтверждён Leiden: He did so while comparing his work to the exemplar, the book he had copied his text from. Реальный раздел — Insertion, а не Exemplar: locator в reader исправлен без изменения оригинала.'),
('PASS','Полный Palimpsest включает scrape the text off its pages и reapply text of your own. Оба русских предложения подтверждены; не утверждают, что любое проступание текста обязательно вызвано слабым закреплением чернил.')],
'middle-ages-dowry':[
('FIX','Полный publisher abstract UGR описывает уход от brideprice к dowry и различает два типа dowry. Он не формулирует переход именно к родительскому типу с исключением groom donation как отдельный доказанный факт. Вариант «Выкуп за невесту» — буквальный перевод системы brideprice из условия и не может быть её заменой; исключается самим вопросом. «Вдовья доля мужа для содержания жены» также не вклад при заключении брака, плюс неясно «доля мужа». Нужны сопоставимые правдоподобные вклады и точный источник для исключительности ключа; medium и индекс сохранить.'),
('PASS','UGR English/Spanish abstract прямо различает вклад родителей невесты и дар жениха в обмен за невесту. Note сообщает собственный существенный факт о семейном приданом и не добавляет неподтверждённый порядок наследования.'),
('PASS','Abstract действительно описывает brideprice через purchase/exchange price и переход к dowry. Это конкретный факт о системе выкупа, хотя повторяет направление главного объяснения. Совпадение не запрещено; это не пустое «не подходит».'),
('FIX','Текущая справка лишь говорит, что брачный дар — вид имущественного вклада при браке: это уже содержится в названии варианта и условии. Нужен собственный проверяемый факт: abstract даёт in exchange for the bride / donación propter nupcias. Указание получателя «невесте» в самом варианте также не доказано этой формулировкой abstract; нужен точный источник, прежде чем его оставлять.'),
('PASS','DOUAIRE DR. ANC. напрямую подтверждает право пользования имуществом мужа при его пережитии женой. Справка не превращает usufruit в независимую собственность.'),
('PASS','Общий переход brideprice→dowry подтверждён полным abstract, различение двух вкладов — также; CNRTL поддерживает douaire. Это фактический PASS общего объяснения, не доказательство исключительного ключа «со стороны семьи невесты». Прочитан именно abstract, не полная статья.')],
'middle-ages-serf':[
('FIX','SERF HIST. DU MOY. ÂGE. подтверждает прикрепление и личную зависимость; ключ устойчив, easy соответствует школьному понятию. Но «Арендатор манориальной земли» не ограничен свободным статусом: полный Lancaster Court baron прямо говорит tenants both free and villein, Copyhold descended from unfree villein tenures. Арендатор и зависимый крестьянин могут пересекаться. Нужно сделать этот дистрактор заведомо отличным по личному статусу, сохранив правдоподобие, easy и индекс. Все четыре именные подписи грамматически допустимы.'),
('PASS','Yorkshire Historical Dictionary прямо defines labourer hired at a certain rate of wages for the day. Собственный факт о подённом работнике верен. Пример 1600 не выдаётся за средневековый документ.'),
('PASS','Lancaster Rental перечисляет tenants и rent due from each. Справка даёт конкретный факт о регистрации арендаторов, а не пустое описание; не утверждает, что все арендаторы свободны. Факт не устраняет пересечение вариантов в prompt-key.'),
('PASS','CNRTL HIST. DU MOY. ÂGE. прямо описывает прикреплённого человека, труд/имущество и владельца. Справка осторожно атрибутирует словарю обобщённое определение. Прежнее неподтверждённое chevage удалено.'),
('FIX','UC Davis строка sake and soke подтверждает противопоставление lowest freeholder серфу. Но текущая note сообщает факт главным образом о серфе, повторяя его прикрепление, и не объясняет собственное владение фригольдера. Это фактически верное, но недостаточно содержательное отрицательное противопоставление. Полный Lancaster Freehold даёт собственный факт: fee simple «for ever», с homage and service to lord. Можно использовать его; нельзя приписывать освобождение от всех манориальных обязанностей.'),
('PASS','CNRTL основной раздел и пример client/serf подтверждают землю и связь труда/имущества с владельцем. Два русских предложения без неподтверждённых платежей и обобщений о freehold. Serf корректно дан как французский термин.')]
}
a=json.loads((BASE/'author-pilot5-receipt.json').read_text());m=json.loads((BASE/'source-manifest.json').read_text());topicpath=Path('src/content/topics/middle-ages.json');qs=json.loads(topicpath.read_text())['questions'];old=json.loads(gitbytes(topicpath,'f9e2830'))['questions']
sourceidx=[]
for p in [BASE/'author-pilot5-receipt.json',BASE/'source-manifest.json',topicpath]+[BASE/s['rawCapture'] for s in m['sources']]:
 w=p.read_bytes();g=gitbytes(p);assert w==g,(str(p),'changed from author freeze')
 sourceidx.append({'path':str(p),'workingSha256':sha(w),'gitSha256':sha(g),'bytes':len(w),'commit':AUTHOR_COMMIT,'gitBlob':subprocess.check_output(['git','rev-parse',f'{AUTHOR_COMMIT}:{p}']).decode().strip(),'byteIdentical':True})
assert len(sourceidx)==19
cards=[]
for ac in a['cards']:
 q=next(x for x in qs if x['id']==ac['questionId']);assert sha(canonical(q))==ac['cardCanonicalSha256'];oq=next(x for x in old if x['id']==q['id']);assert q['difficulty']==oq['difficulty'] and q['correctIndex']==oq['correctIndex']
 fields=[]
 for af,(verdict,analysis) in zip(ac['fields'],DECISIONS[q['id']]):
  name=af['field'];lit=[q['prompt'],q['correctIndex'],q['answers'][q['correctIndex']]['text']] if name=='prompt-key' else q['explanation'] if name=='explanation' else q['answers'][int(name[-1])]['note']
  lb=json.dumps(lit,ensure_ascii=False,separators=(',',':')).encode() if isinstance(lit,list) else lit.encode();assert sha(lb)==af['literalSha256'] and lit==af['literal']
  proofs=[]
  for ap in af['proofs']:
   p={k:v for k,v in ap.items() if k!='readerIdentity'};path=BASE/ap['rawCapture'];p['rawCapture']=str(path);assert sha(path.read_bytes())==ap['rawCaptureSha256'];assert sha(ap['passage'].encode())==ap['passageSha256']
   p['captureMethod']='Independent local rereading of preserved complete original, with working bytes independently compared to committed author freeze. Original acquisition: '+ap['captureMethod'];p['readerIdentity']=READER
   if q['id']=='middle-ages-palimpsest' and name=='note3':p['locator']={'section':'Insertion','sentence':'He did so while comparing his work to the exemplar'}
   proofs.append(p)
  if q['id']=='middle-ages-serf' and name=='prompt-key':
   s=next(s for s in m['sources'] if 'lancaster' in s['rawCapture']);passage='Court baron: (Latin curia baronis). The basic manorial court, held by a manorial lord for his tenants, both free and villein.'
   proofs.append({**s,'rawCapture':str(BASE/s['rawCapture']),'locator':{'entry':'Court baron'},'passage':passage,'passageSha256':sha(passage.encode()),'readerIdentity':READER})
  if q['id']=='middle-ages-serf' and name=='note3':
   s=next(s for s in m['sources'] if 'lancaster' in s['rawCapture']);passage="Freehold: land held in fee simple, that is 'for ever', by rendering homage and service to the lord of the manor."
   proofs.append({**s,'rawCapture':str(BASE/s['rawCapture']),'locator':{'entry':'Freehold'},'passage':passage,'passageSha256':sha(passage.encode()),'readerIdentity':READER,'captureMethod':'Independent reading of complete preserved Lancaster glossary and working/Git byte comparison. Original acquisition: '+s['captureMethod']})
  fields.append({'field':name,'literal':lit,'literalFormat':'compact UTF-8 JSON array [prompt,correctIndex,keytext]' if isinstance(lit,list) else 'UTF-8 string, no newline','literalSha256':sha(lb),'verdict':verdict,'substantiveRead':True,'claimAnalysis':analysis,'proofs':proofs})
 verdict='FIX' if any(f['verdict']=='FIX' for f in fields) else 'PASS'
 cards.append({'questionId':q['id'],'cardCanonicalSha256':sha(canonical(q)),'difficulty':q['difficulty'],'verdict':verdict,'editorialAnalysis':fields[0]['claimAnalysis']+' Все четыре буквальных варианта прочитаны вместе с условием; notes и explanation оценены отдельно. Связь со средневековым правом/рукописной культурой темы подтверждена. Из пяти карточек dower/dowry связаны, но проверяют разные факты: право пережившей супруги и исторический переход брачных вкладов. Точного дубля prompt или повторного главного факта между ними нет. Узкий механический поиск по ключевым терминам в каталоге не вернул других candidate ID; он не доказывает отсутствие любых смысловых дублей за пределами пилота.','answersRead':[x['text'] for x in q['answers']],'fields':fields})
receipt={'agentIdentity':READER,'role':'independent','actualAuthorIdentity':a['agentIdentity'],'authorReceiptPath':str(BASE/'author-pilot5-receipt.json'),'authorReceiptSha256':sha((BASE/'author-pilot5-receipt.json').read_bytes()),'authorReceiptCommit':AUTHOR_COMMIT,'sourceFreezeCommit':AUTHOR_COMMIT,'roundtripMetadataCommit':'e88b2e7','baselineFreeze':'f9e2830','cardCanonicalRecipe':'UTF-8 JSON of complete card, sorted object keys recursively, ensure_ascii=False, compact separators comma/colon, no newline','literalRecipe':'prompt-key: UTF-8 compact JSON array [prompt,correctIndex,keytext], ensure_ascii=False, no newline; note0..3 and explanation: literal UTF-8 string without newline','decisionMethod':'All 30 field decisions and all five card judgments explicitly decided by this independent reader after substantive reading. Serializer performs binding only; no author PASS inherited.','sourceReadBoundary':'Complete relevant dictionary/glossary sections and full HTML abstract read from preserved raw originals. UGR is publisher abstract, not full article. Persee review p119 is not used as full article. No Magna Carta or chevage claim remains in current five; no such claim certified. CNRTL JSON is complete API response; relevant TLFi entry sections read, unrelated synonyms/examples not claimed as full scholarly works.','scope':list(DECISIONS),'unreadInPilot':0,'unreadFieldsInPilot':0,'other95NotEdited':True,'remaining23NotSubstantivelyRead':True,'rootLedgerNotEdited':True,'counts':{'cards':5,'fields':30,'PASS':sum(c['verdict']=='PASS' for c in cards),'FIX':sum(c['verdict']=='FIX' for c in cards),'HOLD':0,'fieldPASS':sum(f['verdict']=='PASS' for c in cards for f in c['fields']),'fieldFIX':sum(f['verdict']=='FIX' for c in cards for f in c['fields'])},'cards':cards}
save('reader-receipt.json',receipt);save('source-index.json',{'agentIdentity':READER,'role':'independent-byte-readback','contentCommit':AUTHOR_COMMIT,'verifiedFiles':sourceidx,'all19ByteIdentical':True,'editorialVerdictsDerivedFromBytes':False})
print(receipt['counts'])
