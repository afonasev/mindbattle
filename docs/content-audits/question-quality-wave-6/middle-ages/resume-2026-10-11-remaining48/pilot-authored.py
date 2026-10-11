"""Hand-authored five-card pilot; no generated editorial decisions.
The explicit texts and judgments below were written after reading original passages.
The emitter only attaches hashes and exact selected source text.
"""
import json, hashlib, os, re
from pathlib import Path
from html.parser import HTMLParser
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[4]
TOPIC=REPO/'src/content/topics/middle-ages.json'
def digest(b): return hashlib.sha256(b).hexdigest()
def canon(x): return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
class Text(HTMLParser):
 def __init__(self): super().__init__(); self.parts=[];self.hidden=0
 def handle_starttag(self,t,a):
  if t in ('script','style'):self.hidden+=1
 def handle_endtag(self,t):
  if t in ('script','style'):self.hidden=max(0,self.hidden-1)
 def handle_data(self,d):
  if not self.hidden:self.parts.append(d)
PDF=PdfReader(ROOT/'sources/kernow-original.pdf')
KURL='https://kresenkernow.org/wp-content/uploads/2024/10/Kresen-Kernow-glossary-of-manorial-terms.pdf'
def kp(page,start,end):
 t=PDF.pages[page-1].extract_text();a=t.index(start);b=t.index(end,a);q=t[a:b].rstrip()
 return {'sourceClass':'Institutional archive glossary, Kresen Kernow (Cornwall archive)','title':'Kresen Kernow glossary of manorial terms','url':KURL,'rawCapture':'sources/kernow-original.pdf','captureFormat':'pdf original bytes with pdfPage locator','captureMethod':'HTTP 206 contiguous byte ranges with the same ETag and complete length; see kernow-ranges.json. No PDF rewrite.','locator':{'pdfPage':page,'entry':start.strip()},'passage':q}
def hp(name,title,url,section,quote):
 f=ROOT/'sources'/(name+'-compressed.html');p=Text();p.feed(f.read_text());t=' '.join(' '.join(p.parts).split());assert quote in t,quote
 return {'sourceClass':'English Heritage, institution responsible for the historical site','title':title,'url':url,'rawCapture':'sources/'+f.name,'captureFormat':'html original bytes','captureMethod':'curl --compressed --http1.1 full successful HTTP response, decompressed entity bytes; corresponding headers and curl receipt saved.','locator':section,'passage':quote}
proofs={
 'demesne':kp(3,'Demesne Land','Deodand '),
 'tin':kp(7,'Toll Tin ','Turbary '),
 'copyhold':kp(2,'Copyhold A','Conventionary Rent '),
 'freehold':kp(4,'Free Hold ','Free Warren '),
 'common':kp(2,'Common Land ','Copyhold '),
 'rental':kp(6,'Rental A','Right of Wreck '),
 'extent':kp(3,'Extent A','Extinguishment '),
 'custumal':kp(2,'Custumal A','Court Baron '),
 'customs':kp(2,'Customs Laws','Customary tenant '),
 'terrier':kp(7,'Terrier Description','Tithing A'),
 'survey':kp(7,'Survey Description','Tallage '),
 'account':kp(1,'Account Contains','Admission '),
 'court':kp(2,'Court Roll / Book','Cucking stool '),
}
EH='https://www.english-heritage.org.uk/visit/places/'
proofs['raid']=hp('lindisfarne','History of Lindisfarne Priory',EH+'lindisfarne-priory/history/','The Vikings, first paragraph','On 8 June 793 Lindisfarne suffered a devastating raid by Viking pirates – their first significant attack in western Europe. The raid caused horror across the continent.')
proofs['shock']=hp('lindisfarne','History of Lindisfarne Priory',EH+'lindisfarne-priory/history/','The Vikings, paragraph after Alcuin quotation','The raid was physically and psychologically devastating: one of England’s holiest shrines had been attacked by pagans, and St Cuthbert had not intervened to stop them.')
proofs['cuthbert']=hp('lindisfarne','History of Lindisfarne Priory',EH+'lindisfarne-priory/history/','Refoundation after the Norman Conquest, church paragraph','The church, which was built by about 1150, contained a cenotaph (an empty tomb) marking the spot where, according to tradition, Cuthbert’s body had been buried. Although his relics were by then in Durham, the place of his primary shrine on Lindisfarne was still a sacred spot which attracted pilgrims.')
proofs['cluny']=hp('castle-acre','History of Castle Acre Priory',EH+'castle-acre-castle-acre-priory/history/','Introduction, first paragraph','It was also part of a vast monastic network centred on the great abbey of Cluny in France.')
proofs['finchale']=hp('finchale','History of Finchale Priory',EH+'finchale-priory/history/','A new priory, first paragraph','After Godric’s death the Durham community sent two monks, Reginald and Henry, to occupy his hermitage. In effect, Finchale became a small, subordinate monastery of Durham. In 1196 it became a priory in its own right when the monks of Durham persuaded Henry du Puiset, son of Bishop Hugh du Puiset of Durham, to endow it with possessions he had previously bestowed on another monastery.')
proofs['parent']=hp('finchale','History of Finchale Priory',EH+'finchale-priory/history/','Introduction, first paragraph','By the mid 14th century this was serving as a holiday home for monks from Finchale’s parent monastery, Durham.')
proofs['oswine']=hp('tynemouth','History of Tynemouth Priory and Castle',EH+'tynemouth-priory-and-castle/history/','A new monastery, building programme paragraph','Around 1090, a programme of new building at Tynemouth began, initially with a church dedicated to St Oswine and the Virgin Mary. Twenty years later, St Oswine’s remains were brought from Jarrow to a permanent tomb in the new church at Tynemouth, a sign that the east end of the church was finished and that the priory was to be a place of pilgrimage.')
# Explicit author text. Each field decision is separate and supplied below.
edits={
'middle-ages-priory':{
 'prompt':'Какой английский монастырь викинги разграбили в 793 году во время одного из самых известных ранних набегов?',
 'answers':[
 {'text':'Монастырь Касл-Акр','note':'Приорат Касл-Акр входил в сеть монастырей, связанную с аббатством Клюни во Франции.'},
 {'text':'Монастырь Линдисфарн','note':'Линдисфарн оставался центром почитания святого Кутберта, хотя его мощи уже хранились в Дареме.'},
 {'text':'Монастырь Финчейл','note':'В 1196 году Финчейл получил статус приората, сохранив связь с материнским монастырём в Дареме.'},
 {'text':'Монастырь Тайнмут','note':'После переноса останков святого Освайна в церковь Тайнмута место стало центром паломничества.'}],
 'explanation':'В 793 году викинги разграбили монастырь Линдисфарн. Нападение потрясло христианскую Европу: пострадало одно из самых почитаемых святых мест Англии.',
 'source':{'title':'History of Lindisfarne Priory | English Heritage','url':EH+'lindisfarne-priory/history/','verifiedAt':'2026-10-11'}},
'middle-ages-demesne':{
 'prompt':'Как в средневековом английском маноре называли землю, оставленную для собственного хозяйства лорда, а не переданную держателям?',
 'answers':[
 {'text':'Домен','note':'Домен мог приносить доход и от добычи олова: владельцу земли причитался особый платёж toll tin.'},
 {'text':'Копигольд','note':'Копигольдер получал копию записи манориального суда о передаче держания; от этой копии произошло название формы владения.'},
 {'text':'Фригольд','note':'Фригольд означал свободное владение землёй, не подчинённое обычаям манора.'},
 {'text':'Общинные угодья','note':'На общинных угодьях определённые жители имели права выпаса, сбора топлива или рыбной ловли; земля могла принадлежать лорду.'}],
 'explanation':'Домен — земля, которую лорд оставлял для собственного использования. Её отличали от участков, переданных держателям.',
 'source':{'title':'Kresen Kernow — glossary of manorial terms, Demesne','url':KURL,'verifiedAt':'2026-10-11'}},
'middle-ages-common-land':{
 'prompt':'Как назывались угодья английского манора, где определённые жители имели общие права выпаса скота и сбора древесины, хотя владельцем земли оставался лорд?',
 'answers':[
 {'text':'Домен','note':'Домен составляли земли, оставленные лордом для собственного использования, в отличие от земель держателей.'},
 {'text':'Общинные угодья','note':'Права на общинных угодьях могли включать рыбную ловлю в водоёмах и добычу торфа для топлива.'},
 {'text':'Копигольд','note':'Передачу копигольда записывали в протокол манориального суда, а держателю выдавали копию записи.'},
 {'text':'Фригольд','note':'Фригольд означал свободное владение землёй, не подчинённое обычаям манора.'}],
 'explanation':'Это общинные угодья: право пользоваться ими не означало, что сама земля принадлежала всем жителям. Набор прав мог включать выпас, сбор древесины, торфа и рыбную ловлю.',
 'source':{'title':'Kresen Kernow — glossary of manorial terms, Common Land','url':KURL,'verifiedAt':'2026-10-11'}},
'middle-ages-terrier':{
 'prompt':'Как называлось описание английского манора, в котором сведения о земле располагались по её местоположению — в топографическом порядке?',
 'answers':[
 {'text':'Террьер','note':'Террьеры входили в число манориальных описаний наряду с ренталями, перечислявшими ренту, и экстентами, оценивавшими доходные элементы владения.'},
 {'text':'Ренталь','note':'Ренталь перечислял держателей и суммы причитавшейся с них ренты.'},
 {'text':'Экстент','note':'Экстент оценивал элементы владения и службы, от которых лорд получал доход.'},
 {'text':'Кустумал','note':'Кустумал описывал обычаи держания земли, а также ренты и службы, которыми держатели были обязаны лорду.'}],
 'explanation':'Террьер описывал манор в топографическом порядке. Ренталь прежде всего перечислял держателей и ренту, а экстент давал финансовую оценку владения.',
 'source':{'title':'Kresen Kernow — glossary of manorial terms, Terrier','url':KURL,'verifiedAt':'2026-10-11'}},
'middle-ages-custumal':{
 'prompt':'В каком документе английского манора записывали местные обычаи держания земли вместе с рентами и службами, причитавшимися лорду?',
 'answers':[
 {'text':'Ренталь','note':'Ренталь представлял собой список держателей с суммами причитавшейся ренты.'},
 {'text':'Кустумал','note':'Описанные в кустумалах обычаи не были единообразны: они могли различаться от манора к манору.'},
 {'text':'Счёт управляющего','note':'Манориальные счета отражали доходы и расходы; их обычно вёл управляющий или бейлиф.'},
 {'text':'Судебный свиток','note':'Судебные свитки фиксировали дела манориального суда, в том числе смерти держателей и передачу земли.'}],
 'explanation':'Кустумал связывал держания с местными обычаями, рентами и обязательными службами. Именно сведения об обычаях отличают его от простого списка рент.',
 'source':{'title':'Kresen Kernow — glossary of manorial terms, Custumal','url':KURL,'verifiedAt':'2026-10-11'}}}
# These are individually authored substantive decisions, not a rule or generated PASS.
reads={
'middle-ages-priory':('PASS','Новый основной факт — известный набег 793 года на Линдисфарн, а не редкая военная функция Тайнмута. Medium оправдан узнаваемостью ранней истории викингов для знакомого с эпохой; в тексте нет Тайн/Тайнмут или буквального имени ключа. Четыре варианта — монастыри Англии; неверные обители исторически существовали позднее, но узнавание их дат основания не требуется, и по самим названиям дата не выводится. Notes описывают именно свои обители. Линдисфарн получил новую позицию 1 при сохранении correctIndex. Поиск по всем main prompts: Линдисфарн/793 не встречаются вне этой карточки.',[
 ('prompt-key','PASS','793 и набег прямо указаны в The Vikings; русское разграбили передаёт devastating raid, но не утверждает первый в истории набег. Факт широко представлен в истории эпохи, а не местная загадка.', ['raid']),
 ('note0','PASS','Castle Acre назван частью сети с центром Cluny in France. Именно эта связь переведена как сеть монастырей, связанная с Клюни.', ['cluny']),
 ('note1','PASS','Абзац о церкви XII века прямо связывает святыню Кутберта на Линдисфарне с паломниками при мощах в Дареме. Это дополнительный факт о ключе, независимый от набега 793 года.', ['cuthbert']),
 ('note2','PASS','In its own right передано как получил статус приората, без самостоятельности. Сохранившаяся связь проверена вторым пассажем parent monastery Durham в XIV веке; независимость от Дарема не заявлена.', ['finchale','parent']),
 ('note3','PASS','Останки именно Oswine перенесены из Jarrow в Tynemouth; источник связывает новый храм с place of pilgrimage. Не перепутан Cuthbert из соседнего варианта.', ['oswine']),
 ('explanation','PASS','Два предложения: набег и его религиозный резонанс. Первое подтверждает 793/Lindisfarne; второе основано на horror across the continent и one of England’s holiest shrines. Нет неподтверждённого утверждения об уничтожении всех монахов.', ['raid','shock'])]),
'middle-ages-demesne':('PASS','Medium: узнавание домена по его функции в маноре, знакомое изучающему феодальное хозяйство. Четыре именные подписи обозначают режимы земельного владения/пользования; копигольд и фригольд правдоподобны как держания, common отличается коллективными правами. Один ключ задан исключением передачи держателям. Добавочный факт о доходе от олова не повторяет условие. Соседний manor спрашивает целое владение, common — права совместного пользования; это разные main facts.',[
 ('prompt-key','PASS','Demesne прямо противопоставлен land leased/granted to tenants и retained for own use. Русское собственное хозяйство лорда соответствует смыслу; не утверждается, что любой домен во все века обрабатывали только лично.', ['demesne']),
 ('note0','PASS','Toll Tin определён как royalty paid to owner if tin mining occurred in manorial demesne. Мог приносить доход сохраняет условность if; это дополнительная доходная функция именно домена.', ['tin']),
 ('note1','PASS','Статья Copyhold связывает название с копией court rolls, выдаваемой держателю при передаче. Все части русской справки находятся в том же абзаце.', ['copyhold']),
 ('note2','PASS','Free Hold — land held outright and not subject to customs of manor. Свободное владение — перевод правового статуса, а не утверждение об отсутствии любых налогов.', ['freehold']),
 ('note3','PASS','Common Land прямо называет лорда владельцем, commoners носителями прав, а дальше перечисляет pasture, estovers и piscary. Не утверждается доступ всех жителей без ограничения.', ['common']),
 ('explanation','PASS','Два предложения передают определение Demesne и его отличие от granted to tenants. Дополнительный горный доход оставлен в note; объяснение не делает обязательным труд сервов.', ['demesne'])]),
'middle-ages-common-land':('PASS','Medium проверяет различие собственности и общих прав пользования в маноре. Все варианты обозначают земельные режимы; ключ нельзя получить только по слову община, которого в условии нет. Общие права выпаса/дров отделяют common от личного домена и индивидуальных держаний. Extra note добавляет piscary/turbary, которых нет в prompt. Это самостоятельная правовая связь, не инверсия домена.',[
 ('prompt-key','PASS','В Common Land одновременно названы владелец lord, ограниченный круг commoners и rights of pasture/estovers. Это основание единственного ответа; в русском не говорится об общенародной собственности.', ['common']),
 ('note0','PASS','Прямое определение Demesne: own use vs tenants. Справка относится к дистрактору, не переносит на него коллективные права.', ['demesne']),
 ('note1','PASS','Piscary — fish from ponds and streams; turbary — turf or peat for fuel. Русская справка выбирает торф, а не неверно обобщает на полезные ископаемые вообще. Это два дополнительных вида прав на ключевые угодья.', ['common']),
 ('note2','PASS','Copyhold paragraph описывает court rolls и выдачу копии tenant. Справка даёт конкретный юридический механизм, а не отрицательную заглушку.', ['copyhold']),
 ('note3','PASS','Free Hold exact definition задаёт held outright/not subject to customs. Справка не обещает отсутствие обязательств перед государством или церковью.', ['freehold']),
 ('explanation','PASS','Два предложения объясняют раздельность собственности и прав пользования и дают перечисление четырёх подтверждённых прав. Все claims в Common Land; общедоступность всем исключена.', ['common'])]),
'middle-ages-terrier':('PASS','Hard: различие близких типов манориальных документов по организации сведений. Четыре самостоятельные именные подписи — реальные документы о земле/доходах/повинностях; можно логически исключить ренталь по финансовому корню, но точный термин требует знания. Террьер отделён от неоднозначного прежнего вопроса про платежи. Дополнительная note раскрывает его место среди surveys и функции двух соседних видов; не пустой ярлык. Поиск main prompts должен подтвердить отсутствие топографического описания манора вне этой карточки.',[
 ('prompt-key','PASS','Terrier прямо определяется как description following a topographical arrangement. Местоположение поясняет слово топографический по смыслу, без новых исторических claims.', ['terrier']),
 ('note0','PASS','Survey перечисляет extents/rentals/terriers как три вида; Rental и Extent подтверждают функции остальных двух. Справка добавляет документальную классификацию терьера, а не повтор топографического порядка.', ['survey','rental','extent']),
 ('note1','PASS','Rental — document listing tenants and amount of rent due. Перевод сохраняет оба элемента: держатели и суммы ренты.', ['rental']),
 ('note2','PASS','Extent — financial survey with valuation of every element of land and services generating income. Оценка, элементы владения, службы и доход лорда подтверждены.', ['extent']),
 ('note3','PASS','Custumal перечисляет tenants, manor customs, rents and services owed lord. Русская note сохраняет обычаи держания и обязательства, не приписывает топографическую организацию.', ['custumal']),
 ('explanation','PASS','Два предложения с явным ключом и содержательным различением близких документов. Топографический принцип и финансовые функции двух дистракторов подтверждены разными словарными статьями.', ['terrier','rental','extent'])]),
'middle-ages-custumal':('PASS','Hard: специальные типы английских манориальных документов. Кустумал, ренталь, счёт и судебный свиток реально могли содержать платежи; признак customs вместе с rents/services оставляет один ключ. Все ответы — документы, не лица или участки. Полезная note объясняет местную вариативность записанных обычаев; эта вариативность не повторяется в prompt. Террьер теперь спрашивает способ топографической организации, то есть отдельный main fact.',[
 ('prompt-key','PASS','Определение Custumal содержит полный набор customs they held land by, rents and services owed lord. Простые платежные записи в остальных документах не равны своду обычных условий держания.', ['custumal','rental','account','court']),
 ('note0','PASS','Rental называет список tenants и amount of rent due. Русская note точна и относится к ренталю.', ['rental']),
 ('note1','PASS','Статья Customs указывает could differ from manor to manor. Связь с кустумалом обоснована соседней статьёй Custumal, где эти customs описаны как содержание документа. Это явное сопоставление двух определений, не фальшивая единая цитата.', ['customs','custumal']),
 ('note2','PASS','Account contains manorial income and expenditure, usually kept by steward or bailiff. Перевод управляющий/бейлиф соответствует steward/bailiff; обычно сохраняет qualifier.', ['account']),
 ('note3','PASS','Court Roll / Book — minutes of court с death of tenants и surrenders of land. Русское передача земли обобщает юридическую surrender; не приписывает судебным свиткам функцию ренталя.', ['court']),
 ('explanation','PASS','Два предложения: содержание кустумала и отличие от rental. Контраст основан на явном customs в Custumal и только tenants/rent в Rental; не утверждается, что ренталь никогда не мог содержать дополнительных заметок.', ['custumal','rental'])])}

def emit():
 topic=json.loads(TOPIC.read_text());byid={c['id']:c for c in topic['questions']};receipt={'role':'author','agentIdentity':os.environ['CODEX_THREAD_ID'],'cards':[],'status':'AUTHOR_CANDIDATE_ONLY; requires independent reader and coordinator decision'}
 for qid,edit in edits.items():
  c=byid[qid];c.update(edit);verdict,analysis,fields=reads[qid];rec={'questionId':qid,'cardCanonicalSha256':digest(canon(c)),'verdict':verdict,'editorialAnalysis':analysis,'literalSnapshot':c,'grammarSubstitutions':[],'fields':[]}
  # Complete readings are captured for manual readback, never auto-certified.
  for a in c['answers']:rec['grammarSubstitutions'].append(c['prompt']+' — '+a['text']+'.')
  for name,v,a,refs in fields:
   lit=[c['prompt'],c['correctIndex'],c['answers'][c['correctIndex']]['text']] if name=='prompt-key' else c['explanation'] if name=='explanation' else c['answers'][int(name[-1])]['note']
   f={'field':name,'verdict':v,'substantiveRead':True,'claimAnalysis':a,'literal':lit,'literalSha256':digest(canon(lit) if isinstance(lit,list) else lit.encode()),'proofs':[]}
   for ref in refs:
    p=dict(proofs[ref]);p['proofId']=ref;p['rawCaptureSha256']=digest((ROOT/p['rawCapture']).read_bytes());p['passageSha256']=digest(p['passage'].encode());f['proofs'].append(p)
   rec['fields'].append(f)
  receipt['cards'].append(rec)
 TOPIC.write_text(json.dumps(topic,ensure_ascii=False,indent=2)+'\n');(ROOT/'author-pilot5.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
 (ROOT/'pilot5-candidate.json').write_text(json.dumps([byid[q] for q in edits],ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':emit()
