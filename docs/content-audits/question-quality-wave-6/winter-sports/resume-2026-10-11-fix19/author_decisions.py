"""Explicit author decisions. Serializer computes identities only, never creates verdicts."""
import json,hashlib,os,copy,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
OUT=Path(__file__).resolve().parent
TOPIC=ROOT/'src/content/topics/winter-sports.json'
OLD=ROOT/'docs/content-audits/question-quality-wave-6/independent-pilot/resume-2026-10-11-winter-first25'
AUTHOR=OUT.parent/'resume-2026-10-11-author100'
ID='01a12c0c-9bf3-77d1-9328-374ef53d32e4'
assert os.environ['CODEX_THREAD_ID']==ID
base=json.loads((OUT/'baseline.json').read_text());topic=json.loads(TOPIC.read_text());cards={int(c['id'][-3:]):c for c in topic['questions']}
old={int(c['questionId'][-3:]):c for c in json.loads((OLD/'receipt.json').read_text())['cards']}
idx=json.loads((AUTHOR/'source-index.json').read_text())
def sha(x):return hashlib.sha256(x).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def preserve(p,origin):
 p=copy.deepcopy(p);src=(origin/p['rawCapture']).resolve();body=src.read_bytes();assert sha(body)==p['rawCaptureSha256'],src
 dst=OUT/'originals'/src.name;dst.parent.mkdir(exist_ok=True);assert not dst.exists() or dst.read_bytes()==body;dst.write_bytes(body)
 p['rawCapture']='originals/'+src.name;p.pop('independentReader',None);p['reader']=ID;
 if isinstance(p.get('locator'),dict):
  p['locator']={k:v for k,v in p['locator'].items() if k not in ('index','authorSourceIndex')}
 p['captureMethod']+='; this author preserved exact original bytes from '+str(src.relative_to(ROOT))+' and read indexed passage anew'
 return p
def B(n,f):return [preserve(p,OLD) for p in next(x for x in old[n]['fields'] if x['field']==f)['proofs']]
def P(k,a,b=None):
 s=idx[k];pdf=s['rawCapture'].endswith('.pdf');passage=s['nodes'][a-1] if pdf else ' '.join(s['nodes'][a:(b if b is not None else a)+1])
 return [preserve(dict(sourceClass='primary sports governing institution',title=k+' official original',url=s['http']['url'],rawCapture=s['rawCapture'],rawCaptureSha256=s['rawCaptureSha256'],captureFormat='pdf original bytes with pdfPage locator' if pdf else 'html original bytes',captureMethod=s['http']['method']+'; '+s['extraction'],locator={'pdfPage':a} if pdf else {'textNodeStart':a,'textNodeEnd':b if b is not None else a},passage=passage,passageSha256=sha(passage.encode())),AUTHOR)]
rows=[]
def F(name,verdict,analysis,proofs):return dict(field=name,verdict=verdict,substantiveRead=True,claimAnalysis=analysis,proofs=proofs)
def R(n,verdict,editorial,fields):
 c=cards[n];expected={'prompt-key':canon([c['prompt'],c['correctIndex'],c['answers'][c['correctIndex']]['text']]),'explanation':c['explanation'].encode(),**{f'note{i}':a['note'].encode() for i,a in enumerate(c['answers'])}}
 for f in fields:f['literalSha256']=sha(expected[f['field']]);f['literal']=json.loads(expected[f['field']]) if f['field']=='prompt-key' else expected[f['field']].decode()
 rows.append(dict(questionId=c['id'],cardCanonicalSha256=sha(canon(c)),verdict=verdict,editorialAnalysis=editorial,fields=fields))
def setcard(n,prompt=None,answers=None,explanation=None):
 c=cards[n]
 if prompt is not None:c['prompt']=prompt
 if answers is not None:c['answers']=[dict(text=t,note=v) for t,v in answers]
 if explanation is not None:c['explanation']=explanation
 c['source']['verifiedAt']='2026-10-11'
# Pilot five: literal decisions below are authored after original reading.
cards[10]['answers'][0]['note']='В олимпийском скоростном спуске победителя определяют по времени одного заезда.'
R(10,'PASS','Четыре однородных названия горнолыжных дисциплин; читаны все подстановки. Слалом узнаваем широкой аудиторией по частым поворотам; easy сохранён. Note0 теперь сообщает правило одного заезда, а не ярлык скоростной. Ключ1 неизменен; note1 дополняет основной факт и может пересекаться с другими explanations.',[
F('prompt-key','PASS','COC называет slalom shortest alpine event и most gates; перевод относится именно к слалому среди четырёх данных дисциплин.',B(10,'prompt-key')),
F('note0','PASS','COC For both of those speed events...single run относится к downhill и super-G, перечисленным непосредственно выше; note0 про downhill, один заезд.',P('alpine-skiing',72,77)),
F('note1','PASS','Both technical events после giant slalom/slalom: cumulative time двух заездов. Дополнительный факт о слаломе в index1.',B(10,'note1')),
F('note2','PASS','Long, medium and short turns прямо характеризуют giant slalom; note2 не относится к slalom.',B(10,'note2')),
F('note3','PASS','Longer form super giant slalom раскрывает Super-G. Русское название передано без добавочного этимологического утверждения.',B(10,'note3')),
F('explanation','PASS','Shortest и most gates/technical skill покрывают два предложения; частые технические повороты являются смысловым описанием частых ворот.',B(10,'explanation'))])
setcard(16,'Сколько игроков одной команды одновременно участвуют в традиционном кёрлинге, не считая запасного?',[
('Два','В смешанном парном кёрлинге команда состоит из мужчины и женщины.'),('Пять','В традиционном кёрлинге пятый член состава может быть запасным.'),('Три','Трое конькобежцев составляют команду в командной гонке преследования.'),('Четыре','Капитана кёрлинговой команды называют скипом.')],
'В традиционном кёрлинге играют команды по четыре человека. Пятый участник состава может быть запасным и не увеличивает число одновременно играющих.')
R(16,'PASS','Вопрос о традиционном составе без прямой подсказки парном; одинаковые числительные2/5/3/4. Два путают с mixed doubles, пять с запасным, три с небольшими зимними командами; все числа правдоподобны. Базовый состав популярной олимпийской игры оставлен easy. Ключ3; это не карточка27 о начислении очков.',[
F('prompt-key','PASS','World Curling traditional teams four, fifth Alternate substitute; вопрос явно исключил запасного.',P('curling',42)),
F('note0','PASS','Mixed doubles two, one female one male; самостоятельный факт именно о числе два.',P('curling',42)),
F('note1','PASS','Fifth player known as Alternate — a substitute прямо объясняет путаницу пятого в составе и играющих.',P('curling',42)),
F('note2','PASS','Two teams of three skaters в team pursuit; число три относится к одной команде, не к обеим.',B(16,'note2')),
F('note3','PASS','Each team designates a Skip — team captain; дополнительное знание о правильном составе команды, не повтор four.',P('curling',42)),
F('explanation','PASS','Four и fifth substitute покрывают оба предложения; одновременный состав не увеличен запасным.',P('curling',42))])
setcard(18,'Как на Олимпиаде 2026 года стартовали женщины в смешанном сноуборд-кроссе, если партнёры финишировали и их отставания не превышали установленный предел?',explanation='Женщины стартовали с отставаниями, полученными их партнёрами на мужском этапе. Правила ограничивали максимальную задержку старта; при сходе мужчины с дистанции применяли этот предельный интервал.')
cards[18]['answers'][1]['note']='При разных отставаниях партнёров общий одновременный старт отменил бы преимущество мужского этапа.'
cards[18]['answers'][2]['note']='Обратный порядок дал бы ранний старт команде с более поздним мужским финишем, чего этот формат не предусматривает.'
R(18,'PASS','Все четыре способа старта сопоставимы; medium о знакомстве с форматом. Условие ограничено финишировавшими без превышения cap. Ни одна альтернатива не становится вторым верным общим правилом из-за возможного нулевого разрыва. Notes1/2 объясняют конкретное ошибочное преобразование порядка, явно как логический вывод. Ключ0, дата2026.',[
F('prompt-key','PASS','FIS5801 прямо связывает time delay с первым этапом и устанавливает maximum; вопрос теперь ограничен обычным случаем ниже maximum и всеми финишировавшими.',B(18,'prompt-key')),
F('note0','PASS','COC one man and one woman подтверждает дополнительный факт состава именно mixed event.',B(18,'note0')),
F('note1','PASS','Логический вывод из сохранения разницы времени: обнуление различных разрывов убирает преимущество. Это не выдаётся за буквальную цитату.',B(18,'prompt-key')),
F('note2','PASS','Логический вывод: reversing finish order дал бы преимущество позже финишировавшему; FIS сохраняет time delay. Утверждение именно про ложный ответ2.',B(18,'prompt-key')),
F('note3','PASS','COC individual biathlon start in30 second intervals; это пример фиксированного интервала, не правило mixed snowboard.',B(18,'note3')),
F('explanation','PASS','FIS5801,5801.3.2 и5801.3.5: delay, maximum и DNF penalty time; оба предложения теперь покрывают основной принцип и оговорки.',B(18,'prompt-key'))])
setcard(20,'Как в олимпийском бобслее 2026 года считали итог экипажа, завершившего все четыре зачётных заезда?',explanation='Результатом была сумма времени всех четырёх заездов. В решающий четвёртый заезд допускались только 20 лучших экипажей, а победителя определяли по наименьшей общей сумме.')
cards[20]['answers'][2]['note']='Последний заезд добавляют к предыдущим: в бобслее он не заменяет накопленную сумму времени.'
R(20,'PASS','Четыре способа подсчёта правдоподобны: лучший, сумма двух, последний, сумма четырёх. Условие явно только завершившие все4, не выбывшие и не отменённые заезды. Medium о формате сохранён. Ключ3; note2 теперь адресует именно ошибку последнего заезда.',[
F('prompt-key','PASS','OWG format adds times of all heats; four descents и top20 fourth. Ограничение allfour в вопросе делает ключ точным.',B(20,'prompt-key')),
F('note0','PASS','COC snowboard halfpipe only highest-scoring run counts; это самостоятельный пример метода best, без переноса его в бобслей.',B(20,'note0')),
F('note1','PASS','COC both technical events два заезда с cumulative time; предыдущие строки устанавливают slalom. Привязал полный контекст, не безымянное both.',P('alpine-skiing',80,85)),
F('note2','PASS','Adding times of all competition heats логически исключает замену суммы временем четвёртого; note прямо объясняет ложный метод.',B(20,'prompt-key')),
F('note3','PASS','OWG четыре heats на двух последовательных днях по два; полезное дополнение к методу суммы.',B(20,'prompt-key')),
F('explanation','PASS','OWG top20 decisivefourth и lowestaggregate прямо покрывают оба предложения для завершившего полный зачёт экипажа.',B(20,'prompt-key'))])
setcard(23,answers=[('Лыжный тормоз','Тормоз замедляет лыжу, отстегнувшуюся от ботинка.'),('Кант','Износостойкие канты лыжи передают боковые усилия.'),('Платформу','По требованиям FIS её ширина не должна превышать ширину скользящей поверхности лыжи.'),('Сердечник','Требования FIS не ограничивают материал и размеры сердечника лыжи.')])
R(23,'HOLD','Убраны подсказка «под крепление» в ключе и очевидно чужая палка. Все ответы — реальные детали лыжи/системы, в винительном падеже, источник точен; тормоз может путаться с деталями крепления, кант и сердечник — с конструктивными слоями. Но положение канта большинству лыжников известно, а специалист легко исключит сердечник; не считаю правдоподобие всех трёх дистракторов и уровень medium окончательно решёнными. Требуется независимая редакторская калибровка, не certified.',[
F('prompt-key','PASS','FIS3.1.3 interface mounted between skis and release bindings, examples plates/lifters; Платформу — русский термин для plate без встроенной подсказки.',P('fis-equipment-2026',24)),
F('note0','PASS','FIS3.1.5 ski brake slows ski comeoff after release; note0 относится к тормозу, не платформе.',P('fis-equipment-2026',25)),
F('note1','PASS','FIS3.1.2.1 edges hard material resistant wear for lateral forces; точный перевод про кант.',P('fis-equipment-2026',16)),
F('note2','PASS','FIS3.1.3.2.1 at each point interface width not exceed running surface; note2 относится к платформе.',P('fis-equipment-2026',24)),
F('note3','PASS','FIS3.1.2.5.2 Core no limitations material/dimensions; нормативный факт именно сердечника, без утверждения произвольной геометрии всей лыжи.',P('fis-equipment-2026',23)),
F('explanation','PASS','FIS componentB interface and mountedbetween подтверждают оба предложения, may оставляет возможность, не универсальную обязательность.',P('fis-equipment-2026',24))])
exec(compile((OUT/'remaining_decisions.py').read_text(),str(OUT/'remaining_decisions.py'),'exec'))
if __name__=='__main__':
 TOPIC.write_text(json.dumps(topic,ensure_ascii=False,indent=2)+'\n')
 (OUT/'originals/.gitattributes').write_text('* -text -diff\n')
 (OUT/'receipt.json').write_text(json.dumps(dict(role='author',agentIdentity=ID,scope='exact19 independent non-PASS; current revised cards; no certification',cards=rows),ensure_ascii=False,indent=2)+'\n')
