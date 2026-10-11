"""Four authored land-law cards. Verdicts and claim analyses are explicit human-readable decisions."""
import importlib.util,json,os
from pathlib import Path
R=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('p',R/'pilot-authored.py');p=importlib.util.module_from_spec(s);s.loader.exec_module(p)
urls={'alleu':'https://www.cnrtl.fr/definition/alleu','benefice':'https://www.cnrtl.fr/definition/b%C3%A9n%C3%A9fice','precaire':'https://www.cnrtl.fr/definition/pr%C3%A9caire','emphyteose':'https://www.cnrtl.fr/definition/emphyt%C3%A9ose'}
proofs={}
def pr(key,term,locator,quote):
 raw=R/f'sources/cnrtl-api-{term}.html';j=json.loads(raw.read_text());parser=p.Text();parser.feed(' '.join(next(x['content'] for x in j['content'] if x['id']=='tlfi')));t=' '.join(' '.join(parser.parts).split());assert quote in t,quote
 proofs[key]={'sourceClass':'CNRTL / ATILF scholarly dictionary TLFi: original historical lexicographic entry, not search snippet','title':'TLFi — '+j['header']['form'],'url':urls[term],'rawCapture':'sources/'+raw.name,'captureFormat':'Unmodified HTTP JSON response containing original TLFi HTML entry; .html filename retained from capture helper','captureMethod':'Complete HTTP200 curl --compressed response from the public /api/word endpoint used by the CNRTL page. Original JSON bytes retained; HTML passage read inside content[id=tlfi].content. No generated excerpt is substituted for original.','locator':{'jsonEntry':'content[id=tlfi].content','section':locator},'passage':quote}
pr('allod-definition','alleu','Definition, DR. FEOD.','Propriété acquise par héritage et libre de toute obligation ou redevance')
pr('allod-etymology','alleu','Etymologie et histoire','De l\'a. bas frq. * alôd « pleine propriété », composé de al « plein, entier » et * ōd, corresp. frq. du germ. * auda- « bien, propriété »')
pr('allod-salic','alleu','Etymologie et histoire','Cet a. bas frq. est transcrit alodis dans la Loi Salique, rédigée entre 507 et 596')
pr('benefice-land','benefice','II.A.1, medieval and modern history','Terre concédée par les chefs francs, puis par les rois à leurs fidèles, en échange d\'un service militaire, et qui prit par la suite le nom de fief.')
pr('benefice-church','benefice','II.A.2','Titre, revenu accordé à une personne, généralement un ecclésiastique, en échange d\'un service spirituel.')
pr('precaire-history','precaire','A, Emploi substantif, HIST. DU DR.','Procédé juridique, hérité du droit romain, utilisé à l\'époque franque, permettant à un propriétaire de concéder des tenures grevées de charges modiques (ou même nulles), mais n\'impliquant pas d\'obligations militaires à la différence du bénéfice')
pr('precaire-revocable','precaire','A, legal definition','Qui n\'est octroyé, qui ne s\'exerce que grâce à une concession, à une permission toujours révocable par celui qui l\'a accordée.')
pr('precaire-request','precaire','A, Encyclopedie universalis citation','la précaire (precaria), qui est l\'acte de requête par lequel un vassal demandait à son seigneur de lui faire un don suffisant pour assurer sa subsistance, ou par lequel un homme libre demandait un bienfait en offrant en échange sa fidélité et ses services')
pr('emphyteose-rent','emphyteose','Definition','Droit réel, cessible, saisissable, susceptible d\'hypothèque, consenti par une personne ayant la capacité d\'aliéner, sur un bien foncier, par un contrat spécial appelé bail emphytéotique, en échange d\'une redevance annuelle')
pr('emphyteose-plant','emphyteose','Etymologie et histoire','gr. de basse époque ἐμφύτευσις de même sens, dér. de ἐμφυτεύειν « planter », un bail de longue durée permettant de jouir de ses plantations.')
# Each answer note is an authored fact, not an automatic category label.
notes={
 'Аллод':('Аллод был наследственным владением, свободным от феодальных повинностей и платежей.','allod-definition'),
 'Бенефиций':('В церковном употреблении бенефиций означал доход или титул, предоставленный за духовное служение.','benefice-church'),
 'Прекария':('Во франкскую эпоху прекария могла нести небольшие платежи, но, в отличие от военного бенефиция, не предполагала военной обязанности.','precaire-history'),
 'Эмфитевзис':('Эмфитевзис предусматривал ежегодный платёж за пользование земельным имуществом.','emphyteose-rent')}
cards=[
('middle-ages-allod','Какой термин землевладения восходит к древнефранкскому сочетанию со значением «полная собственность»?',['Бенефиций','Прекария','Аллод','Эмфитевзис'],'Аллод восходит к сочетанию элементов со значениями «полный» и «имущество». В латинской записи alodis слово встречается в Салической правде.','alleu',[
('prompt-key','PASS',True,'TLFi explicitly derives alod from Old Low Franconian al + od, full + property. Древнефранкское сочетание отражает оба элемента; это вопрос об этимологии, а не дубль определения феода.',['allod-etymology']),
('note0','PASS',True,'Отдельное церковное значение benefice определено как title/revenue for spiritual service. Не смешано с военным пожалованием или абсолютным владением.',['benefice-church']),
('note1','PASS',True,'Статья precaria прямо противопоставляет малые либо нулевые платежи отсутствию military obligations во франкскую эпоху. Слово могла не утверждает обязательность платежа для каждой прекарии.',['precaire-history']),
('note2','PASS',True,'Definition acquis par heritage + free of obligations/redevance under feudal law supports наследственное владение и отсутствие феодальных платежей. Это дополнительный факт к этимологии, не её повтор.',['allod-definition']),
('note3','PASS',True,'Annual redevance on real estate directly supports annual payment, without unsupported perpetual duration or compulsory improvement.',['emphyteose-rent']),
('explanation','PASS',True,'Два предложения передают два разных положения этимологической статьи: компоненты al/od и транскрипцию alodis в Loi Salique. Точная спорная датировка кодекса намеренно не добавлена.',['allod-etymology','allod-salic'])],
'Hard: специальная этимология правового термина. Все четыре варианта — исторические формы земельного владения/держания. Франкский корень отличает аллод от латинских и греческих заимствований; одинаковые именные подписи. Correct-note добавляет режим владения.'),
('middle-ages-benefice','Как называлось земельное пожалование за военную службу у франкских вождей и королей, позднее получившее название «фьеф»?',['Аллод','Прекария','Бенефиций','Эмфитевзис'],'Такое пожалование называли бенефицием. В историческом развитии земельных пожалований за службу его сменило название «фьеф», или феод.','benefice',[
('prompt-key','PASS',True,'II.A.1 contains all three restrictions: Frankish chiefs then kings, military service, later name fief. Вопрос об историческом предшествующем названии, не о самом условии феода из middle-ages-fief.',['benefice-land']),
('note0','PASS',True,'Feudal-domain heading and heritage/free obligations definition support full hereditary landholding without seigneurial dues.',['allod-definition']),
('note1','PASS',True,'TLFi explicitly contrasts precaria with military benefice; малые платежи and no military obligation are stated, not inferred from similar spelling.',['precaire-history']),
('note2','PASS',True,'Ecclesiastical sense in II.A.2 adds income/title for spiritual service, distinct from asked Frankish military land grant. No unsupported absolute ownership claim remains.',['benefice-church']),
('note3','PASS',True,'Emphyteosis definition states annual payment; note does not ascribe benefice military service to this distractor.',['emphyteose-rent']),
('explanation','PASS',True,'Два предложения restate named land tenure and later fief. Русское феод — перевод fief; нет утверждения единой даты или превращения каждого бенефиция в конкретный феод.',['benefice-land'])],
'Hard: различение последовательных юридических названий во франкской истории среди близких типов держания. Служба делает аллод менее вероятным; происхождение и позднее имя отделяют бенефиций от прочих зависимых держаний. Это не повтор вопроса о том, какую службу требовал сеньор. Все ответы — самостоятельные названия в именительном падеже.'),
('middle-ages-precaria','Как называлось предоставляемое по просьбе получателя земельное пользование, основанное на отзывном разрешении собственника?',['Аллод','Бенефиций','Эмфитевзис','Прекария'],'Такое предоставление связывали с прекарией: владелец разрешал пользоваться своим имуществом по просьбе получателя. Разрешение могло быть отозвано.','precaire',[
('prompt-key','PASS',True,'Precaria is explicitly a request instrument; precaire legal definition states concession always revocable by grantor. Исторический раздел подтверждает земельные tenures. Синтез двух частей обозначен, прекария не приравнивается к полному наследственному праву.',['precaire-request','precaire-revocable','precaire-history']),
('note0','PASS',True,'Allod source defines hereditary property free of feudal obligations. Отдельный факт именно об аллоде.',['allod-definition']),
('note1','PASS',True,'Церковное значение benefice подтверждено отдельно от франкского военного. Доход за духовное служение не свойство ключевой прекарии.',['benefice-church']),
('note2','PASS',True,'Definition emphyteose specifies annual redevance. Не переносит отзывность прекарии на эмфитевзис.',['emphyteose-rent']),
('note3','PASS',True,'Историческое применение во франкскую эпоху с малыми/нулевыми платежами и без военной обязанности — дополнительный факт сверх просьбы и отзывности.',['precaire-history']),
('explanation','PASS',True,'Two sentences summarize request plus revocable permission. Предоставление связывали с preserves distinction between instrument precaria and granted property precarium noted by TLFi.',['precaire-request','precaire-revocable'])],
'Hard: редкий институт раннесредневекового землепользования. Все альтернативы в сфере земельных прав, две являются зависимыми держаниями, а аллод можно исключить по полноте собственности. Формулировка явно различает просьбу и условие отзывности; одинаковые подписи.'),
('middle-ages-emphyteusis','Название какого вида долгосрочного земельного пользования связано с греческим глаголом «сажать», поскольку срок позволял получить плоды насаждений?',['Эмфитевзис','Аллод','Бенефиций','Прекария'],'Это эмфитевзис: его название восходит к греческому глаголу со значением «сажать». Длительный срок пользования давал возможность воспользоваться плодами собственных насаждений.','emphyteose',[
('prompt-key','PASS',True,'Etymology explicitly connects Greek emphyteuein planter and long lease allowing enjoyment of plantations. Не повторяется неподтверждённая обязательная мелиорация исходной карточки.',['emphyteose-plant']),
('note0','PASS',True,'Annual redevance is in the definition and adds payment to the question about Greek root and duration.',['emphyteose-rent']),
('note1','PASS',True,'Alleu definition under feudal law supports inherited property free of dues; no military condition incorrectly added.',['allod-definition']),
('note2','PASS',True,'Benefice II.A.2 directly gives income/title for spiritual service, distinct ecclesiastical application.',['benefice-church']),
('note3','PASS',True,'Precaria historical subsection says charges modest or none and no military obligations unlike benefice; exact historical framing retained.',['precaire-history']),
('explanation','PASS',True,'Two sentences correspond to planter etymology and long-term benefit of plantations. This is historical lexical explanation, not current legal advice or a claim of universal modern lease requirements.',['emphyteose-plant'])],
'Hard: специальный греко-римский юридический термин, сохранявшийся в средневековом латинском словаре. Нужно отличить этимологию от других трёх форм владения, а не вспомнить случайную цифру. Все четыре варианта — именные термины земельного права. Correct-note добавляет ежегодную плату.')]
def emit():
 topic=json.loads(p.TOPIC.read_text());by={c['id']:c for c in topic['questions']};receipt={'role':'author','agentIdentity':os.environ['CODEX_THREAD_ID'],'status':'AUTHOR_CANDIDATE_ONLY; not independent certification','cards':[]}
 for qid,prompt,opts,explanation,term,rows,editorial in cards:
  c=by[qid];c.update(prompt=prompt,answers=[{'text':a,'note':notes[a][0]} for a in opts],explanation=explanation,source={'title':'CNRTL / TLFi — '+term,'url':urls[term],'verifiedAt':'2026-10-11'})
  rec={'questionId':qid,'cardCanonicalSha256':p.digest(p.canon(c)),'verdict':'PASS','editorialAnalysis':editorial,'literalSnapshot':c,'grammarSubstitutions':[prompt+' — '+a+'.' for a in opts],'fields':[]}
  for name,verdict,read,analysis,refs in rows:
   literal=[c['prompt'],c['correctIndex'],opts[c['correctIndex']]] if name=='prompt-key' else c['explanation'] if name=='explanation' else c['answers'][int(name[-1])]['note']
   f={'field':name,'verdict':verdict,'substantiveRead':read,'claimAnalysis':analysis,'literal':literal,'literalSha256':p.digest(p.canon(literal) if isinstance(literal,list) else literal.encode()),'proofs':[]}
   for ref in refs:
    pr=dict(proofs[ref]);pr.update(proofId=ref,rawCaptureSha256=p.digest((R/pr['rawCapture']).read_bytes()),passageSha256=p.digest(pr['passage'].encode()));f['proofs'].append(pr)
   rec['fields'].append(f)
  receipt['cards'].append(rec)
 p.TOPIC.write_text(json.dumps(topic,ensure_ascii=False,indent=2)+'\n');(R/'author-land4.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n');(R/'land4-candidate.json').write_text(json.dumps([by[x[0]] for x in cards],ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':emit()
