"""Explicit manual readings; serialization below only binds these decisions to literals.
No scripted substantive judgments. Prior proof catalogue supplies raw passage locators only.
"""
from pathlib import Path
import importlib.util,json,hashlib,copy,sys
R=Path(__file__).resolve().parent; repo=R.parents[4]
spec=importlib.util.spec_from_file_location('prior_proofs',R.parent/'resume-2026-10-11-remaining23/proof_catalog.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
P=copy.deepcopy(m.PROOFS)
for p in P.values(): p['rawCapture']='../resume-2026-10-11-remaining23/'+p['rawCapture']
P['red-conditional']=copy.deepcopy(P['canasta-red']);P['red-conditional']['passage']+=' The value of the red threes is credited to a side that has made a meld, or debited against a side that has made no meld, when the hand ends.'
REVISIONS={
'card-games-durak-attack':{1:'Козырные туз и десятка занимают третье и четвёртое места по старшинству, уступая валету и девятке.'},
'card-games-belote-contract':{3:'В некозырной масти валет и девятка уступают даме, королю, десятке и тузу.'},
'card-games-canasta-natural':{3:'800 очков дают за все четыре красные тройки стороне, сделавшей хотя бы одну выкладку; без выкладки это штраф.'},
'card-games-canasta-mixed':{3:'Четыре красные тройки дают стороне премию 800 очков, если она сделала хотя бы одну выкладку; иначе это штраф.'},
'card-games-skat-three':{0:'Эти трое делятся на разыгрывающего и двух защитников, выступающих против него.'},
}
# Each tuple: field label, explicit author verdict, exact proof IDs, substantive analysis.
D={}
D['card-games-durak-attack']=('PASS','Medium: узнавание специальной пары классического белота, не общеизвестный easy. Четыре козырные пары согласованы с вопросом «какая пара»; единственна K/Q, индекс3. Отдельный факт от старшинства козырей в соседней карточке. Все четыре варианта и шесть полей прочитаны.',[
('prompt-key','PASS',['belote-pair'],'Классические правила стр14 прямо называют Roi et Dame d’atout dans la main. Вариант3 точно король/дама козырей; остальные пары не подходят.'),
('note0','PASS',['belote-order'],'Козырные J/9 буквально первые два в порядке atout; справка именно о паре варианта0.'),
('note1','PASS',['belote-order'],'Исправлено: выбранные козырные A/10 стоят третьим и четвёртым после J/9. Позиции непосредственно отсчитаны в напечатанном порядке, не перенесены с некозырных.'),
('note2','PASS',['belote-order'],'Обе последовательности заканчиваются 8,7. Справка относится к выбранным козырным низшим картам и добавляет сравнение с некозырными.'),
('note3','PASS',['belote-pair'],'20 очков команде — полезное дополнение к распознаванию пары. Допустимо также в explanation; запрет overlap не применяется.'),
('explanation','PASS',['belote-pair'],'Два предложения: правильная пара в одной руке и премия20. Французское dans la main, équipe и bonus20 полностью поддерживают перевод.')])
D['card-games-belote-contract']=('PASS','Medium: тематическое правило рангов. Все именные пары грамматически одинаковы; ключ3 J/9, A/10 правдоподобны из некозырного порядка. Основной факт отличается от белот-ребелот, дубликата между ними нет.',[
('prompt-key','PASS',['belote-order'],'Порядок козырей начинается Valet,9; точно выбран индекс3.'),
('note0','PASS',['belote-order'],'Вариант без слова козырные; сравнение с некозырной мастью верно: As,10 начинают normal порядок.'),
('note1','PASS',['belote-pair'],'Король и дама именно козырные, вместе в руке: belote/rebelote20. Полезный факт выбранной пары.'),
('note2','PASS',['belote-order'],'8/7 замыкают обе последовательности. Младшие — старшинство, не стоимость.'),
('note3','PASS',['belote-order'],'Новое дополнение о самих J/9: в обычной масти As,10,Roi,Dame предшествуют им обоим. Не повторяет только вопрос о двух старших козырях.'),
('explanation','PASS',['belote-order'],'Два предложения перечисляют правильные два и остальных по порядку. Все8 рангов совпадают с atout.')])
D['card-games-canasta-natural']=('PASS','Hard: точная премия выбранной нормативной версии Bicycle, не общая узнаваемость игры. Четыре числа100/300/500/800 реальны в счёте. Ключ2; одиночное сколько очков согласуется с каждым числом. Факт о премии не дублирует максимум wild в смешанной.',[
('prompt-key','PASS',['canasta-bonus'],'Natural/pure no wild earns bonus500, не сумма стоимостей. Источник явно Bicycle в вопросе; индекс2.'),
('note0','PASS',['canasta-score'],'For going out100; concealed extra100 отдельно, поэтому «обычная» точно ограничивает справку.'),
('note1','PASS',['canasta-bonus'],'Mixed bonus300, факт именно о числовом варианте300.'),
('note2','PASS',['canasta-marker'],'Красная верхняя карта означает natural canasta. Полезное дополнительное свойство чистой канасты, а не повтор500.'),
('note3','PASS',['red-conditional'],'Добавлено обязательное условие хотя бы одной выкладки; made a meld даёт плюс800, made no meld — дебет800. Все четыре красные тройки и знак начисления проверены вместе.'),
('explanation','PASS',['canasta-bonus','canasta-meld'],'500 сверх стоимости явно in addition. Minimum7, отсутствие wild и same rank из определения meld вместе дают семь натуральных одного ранга. Два предложения.')])
D['card-games-canasta-mixed']=('PASS','Hard: точный лимит wild, числа1–4 правдоподобны, правило не выводится из длины ответов. Ключ2 три. Основной факт отличен от чистой премии500. Все шесть полей прочитаны.',[
('prompt-key','PASS',['canasta-bonus'],'Mixed содержит one to three wild, значит максимум3; индекс2.'),
('note0','PASS',['canasta-bonus'],'Одна wild входит в диапазон1–3 mixed, в отличие от pure no wild. Это положительный факт об одной.'),
('note1','PASS',['canasta-valid'],'Обычная valid meld требует at least two natural same rank. Справка не утверждает, что2 достаточно для семикарточной канасты.'),
('note2','PASS',['canasta-bonus'],'At least four natural — дополнительная нижняя граница при выбранном максимуме3. Напрямую прочитан base, не только арифметика7−3.'),
('note3','PASS',['red-conditional'],'Уточнён знак800: премия за4 red threes только стороне с выкладкой; без неё штраф. Прочитаны оба предложения Red Threes.'),
('explanation','PASS',['canasta-bonus'],'Два предложения: максимум3 wild, минимум7 всего и4 natural. Все три ограничения одновременно в Canastas.')])
D['card-games-skat-three']=('PASS','Medium: знание состава сдачи ската. Числа2–5 правдоподобны из состава стола и команд; формулировка непосредственно разыгрывают исключает зрителей. Ключ0 три; отдельно от размера skat/колоды.',[
('prompt-key','PASS',['skat-three','skat-roles'],'Каждая игра declarer against two defenders; определение Player явно three involved. Число3 не перепутано с3–5 за столом.'),
('note0','PASS',['skat-three'],'Новое дополнение к числу3 — асимметричное разделение ролей 1+2. Относится именно к этим трём; повтор полезного факта в explanation разрешён.'),
('note1','PASS',['skat-three'],'Two defenders — ровно двое против declarer. Числовой дистрактор получает точный факт.'),
('note2','PASS',['skat-deck'],'32cards in four suits, обе цифры непосредственно1.2.1.'),
('note3','PASS',['skat-table','skat-roles'],'Playing partner three to five за столом; Player onlythree. Пять допустимо, но не все одновременно играют.'),
('explanation','PASS',['skat-three','skat-table'],'Два предложения корректно различают конкретную сдачу и общий состав стола. Не выдают три за верхнюю границу участников.')])
exec((R/'remaining-decisions.py').read_text())
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def sha(x):return hashlib.sha256(x).hexdigest()
def main():
 path=repo/'src/content/topics/card-games.json';topic=json.loads(path.read_text());allowed=json.loads((R/'manifest.json').read_text())['ids']
 for c in topic['questions']:
  for i,n in REVISIONS.get(c['id'],{}).items():c['answers'][i]['note']=n
  if c['id'] in SOURCE_UPDATES:c['source']=SOURCE_UPDATES[c['id']]
 path.write_text(json.dumps(topic,ensure_ascii=False,indent=2)+'\n')
 rows=[]
 for c in topic['questions']:
  if c['id'] not in D:continue
  verdict,analysis,fs=D[c['id']];h=sha(canon(c));row=dict(questionId=c['id'],cardCanonicalSha256=h,verdict=verdict,editorialAnalysis=analysis,fields=[])
  lit={'prompt-key':canon([c['prompt'],c['correctIndex'],c['answers'][c['correctIndex']]['text']]),**{f'note{i}':a['note'].encode() for i,a in enumerate(c['answers'])},'explanation':c['explanation'].encode()}
  for f,v,ps,a in fs:
   fh=sha(lit[f]);proofs=[]
   for pid in ps:
    pr=copy.deepcopy(P[pid]);raw=R/pr['rawCapture'];assert raw.is_file();pr.update(rawCaptureSha256=sha(raw.read_bytes()),passageSha256=sha(pr['passage'].encode()),role='author',agentIdentity='01a12ba6-cb18-7ad0-849f-b1a5baed8a00',currentCardSha256=h,fieldLiteralSha256=fh);proofs.append(pr)
   row['fields'].append(dict(field=f,literalSha256=fh,verdict=v,substantiveRead=True,claimAnalysis=a,proofs=proofs))
  rows.append(row)
 out=R/sys.argv[1];out.write_text(json.dumps(dict(role='author',agentIdentity='01a12ba6-cb18-7ad0-849f-b1a5baed8a00',date='2026-10-11',cards=rows,limits=['Manual substantive author readings only; independent current reader pending.','Earlier HOLD/FIX receipts retained unchanged. Formatter computes hashes and never originates PASS.']),ensure_ascii=False,indent=2)+'\n');print(out,len(rows))
if __name__=='__main__':main()
