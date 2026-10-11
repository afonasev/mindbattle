"""Four further individually authored judgments. No generated verdicts."""
import importlib.util,json,os,hashlib
from pathlib import Path
R=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('pilot',R/'pilot-authored.py');p=importlib.util.module_from_spec(sp);sp.loader.exec_module(p)
K=p.KURL
proofs={
 'hide':p.kp(4,'Hide The','Homage '),
 'acre':p.kp(1,'Acreage A','Account '),
 'hundred':p.kp(4,'Hundred Pre','Incidents '),
 'tithing':p.kp(7,'Tithing A','Tithingman '),
 'steward':p.kp(6,'Steward Official','Information Classification:' ) if False else None,
 'bailiff':p.kp(1,'Bailiffs Manorial','Barton '),
 'reeve':p.kp(6,'Reeve A','Relief '),
 'pinder':p.kp(5,'Pinder Official','Pinfold '),
}
# Last entry on page 6 has no following heading on that page.
q=p.PDF.pages[5].extract_text();q=q[q.index('Steward Official'):].rstrip()
proofs['steward']={**proofs['reeve'],'locator':{'pdfPage':6,'entry':'Steward'},'passage':q}
def htmlproof(name,title,url,locator,quote,sourceclass):
 f=R/'sources'/(name+'.html');parser=p.Text();parser.feed(f.read_text());t=' '.join(' '.join(parser.parts).split());assert quote in t,quote
 return {'sourceClass':sourceclass,'title':title,'url':url,'rawCapture':'sources/'+f.name,'captureFormat':'html original bytes','captureMethod':'Complete curl HTTP response with transfer compression decoded. Successful response and bytes saved; no stitched excerpts.','locator':locator,'passage':quote}
AQ='https://www.newadvent.org/summa/'
primary='Medieval primary work, Thomas Aquinas Summa Theologiae; English Dominican translation published by New Advent'
proofs['heresy-definition']=htmlproof('aquinas-heresy','Summa Theologiae II-II, question 11',AQ+'3011.htm','Article 1, I answer that, last sentence','Therefore heresy is a species of unbelief, belonging to those who profess the Christian faith , but corrupt its dogmas.',primary)
proofs['heresy-correction']=htmlproof('aquinas-heresy','Summa Theologiae II-II, question 11',AQ+'3011.htm','Article 2, Reply to Objection 3','By no means should we accuse of heresy those who, however false and perverse their opinion may be, defend it without obstinate fervor, and seek the truth with careful anxiety, ready to mend their opinion, when they have found the truth',primary)
proofs['schism']=htmlproof('aquinas-schism','Summa Theologiae II-II, question 39',AQ+'3039.htm','Article 1, I answer that','Accordingly schismatics properly so called are those who, wilfully and intentionally separate themselves from the unity of the Church',primary)
proofs['apostasy']=htmlproof('aquinas-apostasy','Summa Theologiae II-II, question 12',AQ+'3012.htm','Article 1, I answer that','But if he give up the faith , then he seems to turn away from God altogether: and consequently, apostasy simply and absolutely is that whereby a man withdraws from the faith , and is called "apostasy of perfidy."',primary)
proofs['simony']=htmlproof('aquinas-simony','Summa Theologiae II-II, question 100',AQ+'3100.htm','Article 1, I answer that','Therefore by buying or selling a spiritual thing, a man treats God and divine things with irreverence, and consequently commits a sin of irreligion.',primary)
proofs['dom-name']=htmlproof('dominicans-english-retry','About the Dominicans — English Province of the Order of Preachers','https://english.op.org/about-us/','Main article, first paragraph','We are the Friars – brothers and priests – of the Order of Preachers , a religious Order of the Catholic Church that is commonly known as the ‘Dominicans’ after the name of our founder, St Dominic.','Official religious order, own institutional history')
proofs['dom-date']=htmlproof('dominicans-english-retry','About the Dominicans — English Province of the Order of Preachers','https://english.op.org/about-us/','Main article, paragraph beginning Since our origins','Since our origins in 1216 members of the Order have, following the example of St Dominic, devoted their lives to the quest for truth , and to sharing the Christian Faith in a reasoned and loving way, with a great concern for individuals and their particular needs and circumstances.','Official religious order, own institutional history')
proofs['dom-life']=htmlproof('dominicans-english-retry','About the Dominicans — English Province of the Order of Preachers','https://english.op.org/about-us/','Main article, paragraph on community','As religious bound to a Rule and the evangelical counsels of obedience , chastity and poverty , we live together in communities, but we are not tied to particular monasteries. Unlike monks, we are itinerant preachers , who are thus called to make the world our cloister.','Official religious order, own institutional history')
proofs['benedictines']=htmlproof('benedictines-roots','A Brief History of the Benedictine Order','https://osb.org/our-roots/a-brief-history-of-the-benedictine-order/','The Spreading of the Rule','In the early 8th century, monks from England proudly proclaim that they follow only the Rule of Benedict – the first genuine „Benedictines“.','Official Benedictine Confederation institutional history')
proofs['cistercians']=htmlproof('citeaux-history','Abbaye Notre-Dame de Cîteaux — Originally','https://citeaux-abbaye.org/en/the-cistercians-yesterday-today-tomorrow/history/originally','History, opening paragraph','Founded in 1098 by Robert of Molesme, the Abbey of Cîteaux, birthplace of the Cistercian Order, is located in the valley of the Saône, in the heart of Burgundy.','Founding abbey official institutional history')
proofs['franciscans']=htmlproof('franciscans-history','History — Order of Friars Minor','https://ofm.org/en/history.html','Main history, paragraph beginning In 1209','In 1209, the first group of friars walked from Assisi to Rome and, in an extraordinary example of how the Holy Spirit acts, this group of dishevelled friars dressed in ragged clothes was received by Pope Innocent III, who approved their rule of life.','Official Order of Friars Minor institutional history')
edits={
 'middle-ages-heresy':{
 'prompt':'Как средневековые католические богословы называли отклонение от церковных догматов, при котором человек продолжал исповедовать христианство?',
 'answers':[{'text':'Схизма','note':'Схизма означала сознательный разрыв церковного единства.'},{'text':'Апостасия','note':'Апостасией в собственном смысле Фома Аквинский называл полный отказ от веры.'},{'text':'Ересь','note':'Фома Аквинский не предлагал обвинять в ереси всякого ошибающегося: он выделял готовность искать истину и исправлять своё мнение.'},{'text':'Симония','note':'Симония связана с покупкой или продажей духовных благ, которые, по учению церкви, не должны быть товаром.'}],
 'explanation':'Такое отклонение называли ересью: человек исповедовал христианство, но искажал его догматы с точки зрения церкви. Полный отказ от веры отличали от ереси и называли апостасией.',
 'source':{'title':'Фома Аквинский — Summa Theologiae, II-II, question 11','url':AQ+'3011.htm','verifiedAt':'2026-10-11'}},
 'middle-ages-hide':{
 'prompt':'Какую земельную единицу средневековой Англии связывали с участком, достаточным для содержания одного хозяйства в течение года?',
 'answers':[{'text':'Гайда','note':'В традиционном счёте десять гайд составляли тайтинг, а сто — сотню.'},{'text':'Акр','note':'Местный корнуолльский акр мог включать от 40 до 60 стандартных акров.'},{'text':'Сотня','note':'Сотня была административным подразделением Англии ещё до нормандского завоевания.'},{'text':'Тайтинг','note':'Тайтингом называли также группу из десяти мужчин и их хозяйств в системе круговой поруки.'}],
 'explanation':'Так определяли гайду: землю, необходимую для годового содержания хозяйства. Из гайд складывались более крупные расчётные единицы — тайтинг и сотня.',
 'source':{'title':'Kresen Kernow — glossary of manorial terms, Hide','url':K,'verifiedAt':'2026-10-11'}},
 'middle-ages-manor':{
 'prompt':'Кто из служащих английского манора председательствовал в манориальном суде в отсутствие лорда?',
 'answers':[{'text':'Бейлиф','note':'Бейлиф представлял лорда и часто ведал одним или несколькими манорами.'},{'text':'Стюард','note':'Стюард управлял манором от имени его владельца.'},{'text':'Рив','note':'Рив был держателем земли, которому поручали управление хозяйством манора.'},{'text':'Пиндер','note':'Пиндер отвечал за помещение задержанного скота в специальный загон.'}],
 'explanation':'В отсутствие лорда в манориальном суде председательствовал стюард. Он был должностным лицом, которое управляло манором от имени лорда.',
 'source':{'title':'Kresen Kernow — glossary of manorial terms, Steward','url':K,'verifiedAt':'2026-10-11'}},
 'middle-ages-inquisition':{
 'prompt':'Какой католический орден, возникший в XIII веке, официально называется Орденом проповедников?',
 'answers':[{'text':'Бенедиктинцы','note':'В начале VIII века английские монахи, следовавшие только уставу Бенедикта, стали распространять его в континентальной Европе.'},{'text':'Цистерцианцы','note':'Цистерцианская традиция берёт начало в аббатстве Сито, основанном Робертом Молемским в 1098 году.'},{'text':'Францисканцы','note':'В 1209 году первые братья пришли из Ассизи в Рим, где Иннокентий III одобрил их образ жизни.'},{'text':'Доминиканцы','note':'Название «доминиканцы» связано с основателем ордена, святым Домиником; его последователи не были прикреплены к одному монастырю.'}],
 'explanation':'Орден проповедников — это доминиканцы, чья история начинается в 1216 году. Проповедь они сочетали с учёбой и молитвой.',
 'source':{'title':'About the Dominicans — English Province of the Order of Preachers','url':'https://english.op.org/about-us/','verifiedAt':'2026-10-11'}}}
# Every tuple is a separate authored decision after reading the exact source, not computed from terms.
reads={
'middle-ages-heresy':('PASS','Medium: различение известных церковно-исторических понятий. Четыре названия осуждавшихся религиозных отступлений, без прежней смеси учения/следствия/наказания. Сохранение исповедания веры отличает ересь от апостасии; схизма относится к единству, симония — к сделке. Текст явно передаёт взгляд средневековых католических богословов, а не объявляет чью-то веру объективно ложной. Главный факт не повторяет вопрос о наказании за светскую инвеституру. Все четыре подписи прочитаны в именительном падеже.',[
 ('prompt-key','PASS',True,'II-II q11 a1 прямо относит heresy к тем, кто profess Christian faith but corrupt its dogmas. Перевод отклонение от догматов при сохранении христианского исповедания точен и явно атрибутирован традиции.', ['heresy-definition']),
 ('note0','PASS',True,'Q39 a1: willingly and intentionally separate from unity of Church. Сознательный разрыв церковного единства передаёт оба признака схизмы.', ['schism']),
 ('note1','PASS',True,'Q12 a1 distinguishes apostasy simply and absolutely as withdrawal from faith; в собственном смысле исключает другие упомянутые Аквинским виды ухода из монашества.', ['apostasy']),
 ('note2','PASS',True,'Q11 a2 ad3 приводит с одобрением Августинов критерий: не обвинять тех, кто ищет истину без упорства и готов исправиться. Русская note сообщает дополнительный критерий, а не повторяет определение ереси.', ['heresy-correction']),
 ('note3','PASS',True,'Q100 a1 прямо осуждает buying or selling a spiritual thing как irreligion. Русская note говорит о симонии как сделке, не о всякой церковной плате.', ['simony']),
 ('explanation','PASS',True,'Два предложения сопоставляют Q11 и Q12. Слова с точки зрения церкви сохраняют атрибуцию доктринального суждения; отказ от веры не выдан за обычное догматическое расхождение.', ['heresy-definition','apostasy'])]),
'middle-ages-hide':('PASS','Medium: общеисторический земельный термин англосаксонской Англии, а не редкий локальный памятник или точная случайная дата. Все варианты — реальные земельные/административные единицы; единица одного хозяйства отделяет гайду от групп и площади акра. Сложность редакторская: знакомый с английским феодальным хозяйством может знать определение, вне темы остаётся угадывание. Справка ключа добавляет масштаб десять/сто. Четыре самостоятельные именные подписи грамматически одинаковы. Исторический вариант акра не приравнен к современной стандартной мере.',[
 ('prompt-key','PASS',True,'Hide определена amount of land need for a household in a year. Русская формулировка связывали с сохраняет характер расчётной единицы, а не обещает постоянную площадь.', ['hide']),
 ('note0','PASS',True,'В том же определении прямо написано 10 hides made a tithing, 100 hides made a hundred. В традиционном счёте не утверждает, что каждая реальная административная сотня всегда содержала ровно100.', ['hide']),
 ('note1','PASS',True,'Acreage прямо distinguishes Cornish acres usually containing40to60statute acres. Мог включать передаёт местный вариант и не утверждает, что стандартный acre равен40acre.', ['acre']),
 ('note2','PASS',True,'Hundred определяется Pre Norman Conquest administrative division. Русская справка точно передаёт время существования и функцию сотни.', ['hundred']),
 ('note3','PASS',True,'Tithing entry говорит group of ten men and their households in frankpledge. Система круговой поруки — смысловой перевод frankpledge; также отделяет социальное значение от единицы земли.', ['tithing']),
 ('explanation','PASS',True,'Два предложения: значение household/year и соотношение гайд с более крупными единицами. Обе части прямо присутствуют в Hide; не повторяется неподтверждённая универсальная площадь.', ['hide'])]),
'middle-ages-manor':('PASS','Medium: функции манориального управления, четыре реальные должности. Новый основной факт — председательство стюарда в суде, а не определение манора, смешанное с мерами земли. Бейлиф и рив действительно связаны с хозяйственным управлением и потому правдоподобны; пиндер — другой низовой служащий. Correct-note добавляет общую административную обязанность стюарда к судебной, допустимо повторяя её в explanation. Каждая подпись — должность в именительном падеже; длина и форма одинаковы.',[
 ('prompt-key','PASS',True,'Steward entry explicitly presided at manor courts if lord absent. Условие отсутствие лорда сохранено; бейлиф не объявлен человеком, который никогда не мог исполнять поручений суда.', ['steward']),
 ('note0','PASS',True,'Bailiffs: lord representative often in charge one or more manors. Часто, представительство и один/несколько маноров совпадают с точным текстом.', ['bailiff']),
 ('note1','PASS',True,'Steward official running manor on behalf lord: справка об общей функции управления дополняет конкретный вопрос о суде.', ['steward']),
 ('note2','PASS',True,'Reeve is a tenant responsible for management of manor. Держатель и управление хозяйством передают определение; не добавлены неподтверждённые выборность или ежегодный срок.', ['reeve']),
 ('note3','PASS',True,'Pinder official impounded livestock in pound. Задержанный скот и специальный загон — перевод этого технического действия, не свойство соседнего рива.', ['pinder']),
 ('explanation','PASS',True,'Два предложения основаны на двух частях Steward: presiding in court and general running manor. Объяснение и correct-note могут иметь общий дополнительный факт.', ['steward'])]),
'middle-ages-inquisition':('PASS','Medium: общеизвестное в истории средневекового монашества название Доминиканского ордена. Четыре реальные католические монашеские традиции/ордена; слово проповедников не повторяет имя ключа. XIII век отсеивает часть вариантов только знающему историю орденов, а не по грамматике. Прежний main fact об инквизиционном расследовании близок к history-spain-easy-01-07 и заменён независимым. ID/index/level сохранены. Все четыре ответа прочитаны как самостоятельные названия множественного числа.',[
 ('prompt-key','PASS',True,'Официальная английская провинция прямо equates Order of Preachers and Dominicans. Origins1216 подтверждает XIII век в условии; это не дата какого-либо позднего провинциального отделения.', ['dom-name','dom-date']),
 ('note0','PASS',True,'OSB сообщает early8th-century English monks follow only Rule Benedict, далее popularize through mission continental Europe. Для второй части добавлен следующий пассаж при сохранении полного оригинала.', ['benedictines']),
 ('note1','PASS',True,'Официальное аббатство Сито указывает founding1098byRobertofMolesme и birthplaceofCistercianOrder. Русский текст связывает традицию с этим основанием, не с поздней реформой траппистов.', ['cistercians']),
 ('note2','PASS',True,'История OFM:1209 group walked AssisitoRome, InnocentIIIapproved ruleoflife. Образ жизни переводит ruleoflife и не смешивается с окончательным письменным уставом1223.', ['franciscans']),
 ('note3','PASS',True,'Два отдельных факта того же ордена: имя founderStDominic и общины nottiedtoparticularmonasteries. Это дополнение к официальному названию, не повтор проповеди.', ['dom-name','dom-life']),
 ('explanation','PASS',True,'Два предложения: тождество названий,1216, сочетание проповеди с учёбой и молитвой. Последний clause проверен в следующем абзаце официальной страницы.', ['dom-name','dom-date'])])}
# Additional exact passages read in the original adjoining sentences, needed for the full claim.
proofs['benedictines-mission']=htmlproof('benedictines-roots','A Brief History of the Benedictine Order','https://osb.org/our-roots/a-brief-history-of-the-benedictine-order/','The Spreading of the Rule, following sentence','They popularize this rule further through their mission in continental Europe and eventually in 816/17 an important synod declares Benedict’s Rule binding for all monks.','Official Benedictine Confederation institutional history')
proofs['dom-study']=htmlproof('dominicans-english-retry','About the Dominicans — English Province of the Order of Preachers','https://english.op.org/about-us/','Main article, final sentence','In practical terms, this means we have always devoted ourselves to study and prayer on the one hand, and meaningful and faithful preaching on the other.','Official religious order, own institutional history')
reads['middle-ages-inquisition'][2][1][4].append('benedictines-mission')
reads['middle-ages-inquisition'][2][5][4].append('dom-study')
def emit():
 topic=json.loads(p.TOPIC.read_text());by={c['id']:c for c in topic['questions']};receipt={'role':'author','agentIdentity':os.environ['CODEX_THREAD_ID'],'cards':[],'status':'AUTHOR_CANDIDATE_ONLY; not independent certification'}
 for qid,edit in edits.items():
  c=by[qid];c.update(edit);v,a,rows=reads[qid];rec={'questionId':qid,'cardCanonicalSha256':p.digest(p.canon(c)),'verdict':v,'editorialAnalysis':a,'literalSnapshot':c,'grammarSubstitutions':[c['prompt']+' — '+x['text']+'.' for x in c['answers']],'fields':[]}
  for name,verdict,read,analysis,refs in rows:
   lit=[c['prompt'],c['correctIndex'],c['answers'][c['correctIndex']]['text']] if name=='prompt-key' else c['explanation'] if name=='explanation' else c['answers'][int(name[-1])]['note'];f={'field':name,'verdict':verdict,'substantiveRead':read,'claimAnalysis':analysis,'literal':lit,'literalSha256':p.digest(p.canon(lit) if isinstance(lit,list) else lit.encode()),'proofs':[]}
   for ref in refs:
    pr=dict(proofs[ref]);pr.update(proofId=ref,rawCaptureSha256=p.digest((R/pr['rawCapture']).read_bytes()),passageSha256=p.digest(pr['passage'].encode()));f['proofs'].append(pr)
   rec['fields'].append(f)
  receipt['cards'].append(rec)
 p.TOPIC.write_text(json.dumps(topic,ensure_ascii=False,indent=2)+'\n');(R/'author-next4.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n');(R/'next4-candidate.json').write_text(json.dumps([by[x] for x in edits],ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':emit()
