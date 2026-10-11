import json,copy
from pathlib import Path
R=Path(__file__).parent
# Explicit author field decisions following read of bobsleigh65–77, luge68–69, skeleton65.
N=[
{'literal':'В олимпийском бобслее время измеряют до сотых долей секунды.','verdict':'PASS','substantiveRead':True,'claimAnalysis':'Bobsleigh75 explicitly hundredth(0.01), applies Olympic events in source context. Additional fact, not crew size.','proofRefs':[['bobsleigh',75,75]]},
{'literal':'Саночники управляют санями переносом веса и давлением ног на полозья.','verdict':'PASS','substantiveRead':True,'claimAnalysis':'Luge69 shifting body weight and pressing runners with feet. Useful technique distinct from lying feet-first.','proofRefs':[['luge',69,69]]},
{'literal':'На старте спортсмен бежит рядом с санями, удерживая их одной рукой.','verdict':'PASS','substantiveRead':True,'claimAnalysis':'Skeleton65 sprint alongside sled first seconds holding one hand. Additional starting technique, distinct from prone head-first question.','proofRefs':[['skeleton',65,65]]},
{'literal':'В монобобе пилот — единственный член экипажа.','verdict':'PASS','substantiveRead':True,'claimAnalysis':'Bobsleigh73–74 only crew member, specific fact about monobob; no claim standardized machine without original rules.','proofRefs':[['bobsleigh',73,74]]}]
rows=[
(69,'В каком виде спорта экипажи из двух или четырёх человек разгоняют сани и затем едут в них по ледовой трассе?','PASS','Easy: широко узнаваемый экипажный спуск. Монобоб исключён явным числом членов экипажа, устранено прежнее пересечение общего бобслея и его подвида. Четыре справки прочитаны отдельно: точность времени, управление санями, старт скелетона, один пилот; grammar4 самостоятельные названия.',
 'Bobsleigh65–74 directly two/four crews push then jump in on ice track; correct0. Саны открытых индивидуальных видов не соответствуют экипажу2/4 в условии.',[['bobsleigh',65,74]],
 'Это бобслей, где экипаж сначала разгоняет сани бегом, а затем занимает места внутри. В двухместном бобе есть пилот и разгоняющий, который также отвечает за торможение.', 'Bobsleigh65 running start and70 pilot/brakeman. Разгоняющий — русская роль brakeman с учётом общего толкания, оба предложения подтверждены.'),
(70,'В каком виде спорта спортсмен спускается на санях, лёжа на спине ногами вперёд?','PASS','Easy: зримо различимое положение тела саночника, четыре близких санных названия. В санном спорте бывает doubles, но вопрос не утверждает только singles. Прочитаны все notes; note1 добавляет управление. Самостоятельные именные ответы grammar4 согласованы.',
 'Luge68 explicitly lying backs feet stretched front. Bobsleigh and monobob seated, skeleton65 stomach-down headfirst; correct1.',[['luge',68,69],['skeleton',65,65]],
 'Так спускаются в санном спорте: спортсмен лежит на спине, вытянув ноги вперёд. Направление меняют переносом веса и давлением ног на полозья.', 'Luge68 положение,69 управление. Два предложения; overlap с useful correct-note разрешён.'),
(71,'В каком виде спорта спортсмен спускается на санях головой вперёд, лёжа на животе?','PASS','Easy: отличие скелетона от санного спорта и бобслея по положению тела. Это соседнее сравнение70, но две отдельные техники разных видов; риск близости отмечен для independent. Все notes прочитаны, note2 даёт самостоятельный стартовый факт. Grammar4 одинаковые названия.',
 'Skeleton65 explicit head-first stomach-down; luge68 inverse supports distractor exclusion; correct2.',[['skeleton',65,65],['luge',68,68]],
 'Это скелетон: спортсмен лежит на животе и движется головой вперёд. Для управления он использует небольшие движения плеч, головы и тела.', 'Skeleton65 steering shoulders/head/body explicitly; два предложения без ошибочного утверждения о рулевом механизме.')]
D=[]
for n,p,v,ed,ka,refs,ex,ea in rows:
 fields=[{'literal':'','verdict':v,'substantiveRead':True,'claimAnalysis':ka,'proofRefs':refs}]+copy.deepcopy(N)+[{'literal':ex,'verdict':v,'substantiveRead':True,'claimAnalysis':ea,'proofRefs':refs}]
 D.append({'questionId':f'winter-sports-{n:03}','prompt':p,'answers':['Бобслей','Санный спорт','Скелетон','Монобоб'],'verdict':v,'editorialAnalysis':ed,'sourceTitle':'Canadian Olympic Committee — '+refs[0][0],'fields':fields})
(R/'sliding3-decisions.json').write_text(json.dumps({'role':'author','cards':D},ensure_ascii=False,indent=2)+'\n')
