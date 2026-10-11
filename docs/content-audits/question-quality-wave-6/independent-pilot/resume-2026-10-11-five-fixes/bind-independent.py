"""Serialize explicit reader decisions; hash/check bytes only, never infer verdicts."""
import copy, hashlib, json, os, subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = next(p for p in HERE.parents if (p / 'src/content/topics').is_dir())
AUTHOR = REPO / 'docs/content-audits/question-quality-wave-6/resume-2026-10-11-five-fixes'
def sha(b): return hashlib.sha256(b).hexdigest()
def canonical(x): return json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()
def write(name, obj): (HERE/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def field(name, verdict, analysis, *proofs):
    return dict(field=name, verdict=verdict, substantiveRead=True, claimAnalysis=analysis, proofIds=list(proofs))

# These are the independent reader's individual substantive judgments after reading
# all current literals and raw source passages. None comes from the author verdict.
decisions = [
 dict(questionId='middle-ages-priory', verdict='FIX_REQUIRED',
 editorialAnalysis='Факт о крепости подтверждён, но смена локальной зависимости на локальную достопримечательность не даёт устойчивого medium для общей темы Средневековья. Тайн в условии и Тайнмут в единственном ответе позволяют выбрать по имени, не зная истории места; без этого совпадения остаётся редкая деталь конкретной английской обители. Дополнительно самостоятельный в note2 внушает административную независимость, которой источник не утверждает. Все четыре названия приоратов — допустимые именные ответы, без падежной подсказки. Объяснение: 2 предложения, фактологически верно. Correct-note сообщает дополнительный факт об Освайне.',
 fields=[
 field('prompt-key','FIX_REQUIRED','L228 точно подтверждает Тайнмут, устье Тайн, роспуск и последующую крепость. Фактический ключ верен; editorial FIX: Тайн → Тайнмут раскрывает ответ формой топонима. Знание узкого местного памятника без этой подсказки не соответствует обычному medium общей исторической темы. Нужен иной содержательный факт при неизменяемом уровне, не косметическая перестановка слов.','tynemouth-fortress'),
 field('note0','PASS','Castle Acre назван частью сети с центром в Cluny во Франции (L224); русская справка передаёт именно этот самостоятельный факт о дистракторе.','castle-acre-cluny'),
 field('note1','PASS','L245 связывает перенос останков Освайна в новую церковь с паломничеством. Справка добавляет культ святого к спрашиваемой военно-географической функции; нет переноса свойств другой обители.','tynemouth-oswine'),
 field('note2','FIX_REQUIRED','1196 и содействие монахов Дарема подтверждены L261. Но priory in its own right обозначает учреждение приората; перевод самостоятельного может означать освобождение от Дарема. L220 прямо называет Дарем parent monastery в XIV веке. Следует написать получил статус приората/стал приоратом без утверждения независимости.','finchale-1196','finchale-parent'),
 field('note3','PASS','L268 говорит о святыне и паломниках на Линдисфарне при мощах Кутберта уже в Дареме; это ровно смысл русской справки.','lindisfarne-cuthbert'),
 field('explanation','PASS','Два предложения: положение приората на мысе у Тайн, роспуск при Генрихе VIII и военное использование до 1956. Все датированные и пространственные утверждения есть в L226/L228; речь о месте, не о непрерывной монастырской жизни до 1956.','tynemouth-headland','tynemouth-fortress')]),
 dict(questionId='middle-ages-cloister', verdict='PASS',
 editorialAnalysis='Medium: узнавание клуатра по функции и плану — базовый термин средневековой монастырской архитектуры для знакомого с темой. Капитулярный зал, клуатр, трапезная, спальня относятся к монастырским пространствам; различаются содержательно, а не грамматически. Все четыре самостоятельных именных ответа согласованы. Explanation теперь 2 предложения. Correct-note добавляет конкретный Лиллесхолл и четыре прохода; совпадение дополнительного факта с explanation разрешено. Это не одно лишь повторение общего определения.',
 fields=[
 field('prompt-key','PASS','L223/L226 описывают типовой центральный cloister, четыре крытых прохода и выходы к другим зданиям. Это клуатр; глава монастыря встречается в chapter house, едят в refectory, спят в dormitory — иные пространства.','lilleshall-layout','lilleshall-four-walkways'),
 field('note0','PASS','Каждое утро, обычно после мессы, каноники встречались в chapter house: точное соответствие L231. Справка о капитулярном зале, не о галереях.','lilleshall-chapter-house'),
 field('note1','PASS','В L226 конкретно четыре крытых прохода Лиллесхолла, ведущие к иным зданиям. Число четыре и названный пример дополняют общее определение prompt; повтор в explanation не дефект.','lilleshall-four-walkways'),
 field('note2','PASS','L235 явно датирует XIV веком деление refectory и warming room в eastern half. Русский текст сохраняет дату и восточную часть; перевод помещение для обогрева точен.','lilleshall-refectory'),
 field('note3','PASS','L250 помещает dormitory above над east range Клива. Это спальня монахов именно этого аббатства, самостоятельная содержательная справка.','cleeve-dormitory'),
 field('explanation','PASS','Два самостоятельных предложения определяют клуатр и дают пример Лиллесхолла. L226 связывает проходы с другими зданиями и прямо описывает вход каноников в церковь; including church обосновано.','lilleshall-layout','lilleshall-four-walkways')]),
 dict(questionId='middle-ages-lord', verdict='PASS',
 editorialAnalysis='Easy: прозвище Ричарда Львиное Сердце широко известно из истории и массовой культуры. Четыре ответа — реальные прозвища средневековых правителей, в одном формате самостоятельных именных подписей; смешение существительного и субстантивированных прилагательных грамматически допустимо. Correct-note добавляет крестовый поход. Explanation — 2 предложения; исправленная хронология не использует ошибочную фразу Westminster о возвращении после смерти отца. Раздельно проверены королевский период Фридриха с 1152 и императорский с 1155.',
 fields=[
 field('prompt-key','PASS','Заголовок Royal Household прямо даёт Richard I / The Lionheart; перевод Львиное Сердце однозначен. Все альтернативы реальные прозвища, но относятся к другим правителям.','richard-lionheart-title'),
 field('note0','PASS','Royal Household подтверждает прозвище и поход 1190 года, возвращение из Святой земли после событий 1192. Westminster буквально называет Third Crusade to the Holy Land; использую только эту подтверждаемую часть, отвергая ошибочное продолжение о смерти отца в 1189. Поход — полезный дополнительный факт.','richard-lionheart-title','richard-crusade','richard-third-explicit','richard-return-captured'),
 field('note1','PASS','John L5 подтверждает Lackland, братство с Ричардом, смерть Ричарда и вступление Иоанна в 1199. В русской справке нет неподтверждённой причинности.','john-succession'),
 field('note2','PASS','Полный контекст Edward L2-L3 подтверждает изгнание, возвращение на престол, обязательство восстановить монастырь св. Петра и строительство церкви в Вестминстере. Авторская короткая цитата об условии папы одна не покрывала завершённое действие; здесь привязан весь нужный контекст.','edward-context'),
 field('note3','PASS','NLA L142 точно разделяет Königszeit 1152–1155 и Kaiserzeit 1155–1190. Met L88 подтверждает перевод прозвища Red-Beard; его отдельное ошибочное elected emperor под 1152 не принимаю. Справка не смешивает два титула.','nla-frederick-periods','frederick-nickname'),
 field('explanation','PASS','Royal L26/L30/L31: плен на обратном пути из Святой земли, выкуп/освобождение в 1194, возвращение и повторная коронация в Англии в 1194. Новая формулировка соответствует этой последовательности; первое предложение о прозвище также привязано.','richard-lionheart-title','richard-return-captured','richard-release','richard-return-england')]),
 dict(questionId='geology-earth-gypsum-plaster', verdict='FIX_REQUIRED',
 editorialAnalysis='Факт растворения и кристаллизации научно подтверждён, но не достаточен для Easy. Знание гипса из бытового опыта обычно касается штукатурки/застывания; бытовая аналогия с солью не позволяет надёжно вывести именно растворимость гипса. Три дистрактора являются породами, ключ минералом: категориальная подсказка вместо честного сопоставления свойств. Все 4 именные ответа грамматически допустимы, но не одной научной категории. Correct-note полностью повторяет prompt/key и не даёт дополнительного факта. Explanation из 2 предложений, фактологически верно. Старые авторские PASS для note1/explanation обсуждают базальт при хешах нынешнего гипса: они не являются фактическим прочтением текущих полей.',
 fields=[
 field('prompt-key','FIX_REQUIRED','Свежий полный NPS HTML независимо прочитан: gypsum dissolves ... recrystallize ... much like salt. Ключ фактически верен. Но слово минерал исключает гранит/мрамор/песчаник уже по категории; без этой подсказки требуется нетипичное для широко образованного взрослого знание растворимости гипса. Это не честный Easy-вывод вроде единица → величина. Требуется новая постановка и правдоподобные сопоставимые альтернативы, сохраняющие уровень.','nps-gypsum-fresh','usgs-mineral','usgs-granite-definition','usgs-marble-full','usgs-sandstone-definition'),
 field('note0','PASS','USGS перечисляет quartz, feldspar, mica как составляющие гранита. Справка указывает основные кварц/полевые шпаты и магматический класс; не объявляет их единственными компонентами. Самостоятельный факт о породе.','usgs-granite-definition'),
 field('note1','FIX_REQUIRED','Нынешний literal о растворении/кристаллизации соответствует NPS, но совпадает с проверяемой связью prompt/key целиком. Ни одного дополнительного факта о гипсе нет. Это нарушение correct-note, а не blanket запрет совпадения с explanation. Авторские basalt proof/analysis к этому literal неприменимы.','nps-gypsum-fresh'),
 field('note2','PASS','USGS прямо называет marble metamorphic и кристаллы calcite; кальцит — основной, не обязательно единственный компонент. Обе части справки проверены по полному тексту.','usgs-marble-full'),
 field('note3','PASS','USGS Sandstone: sedimentary rock composed chiefly of quartz grains. Осадочная природа и основной кварц переведены корректно.','usgs-sandstone-definition'),
 field('explanation','PASS','Два предложения буквально передают растворение гипса, кристаллизацию при испарении и сравнение с солью из NPS. Фактический PASS этого поля не устраняет дефекты Easy/дистракторов/correct-note карточки и не исправляет старую авторскую базальтовую привязку.','nps-gypsum-fresh')]),
 dict(questionId='geology-earth-granite-coarse', verdict='PASS',
 editorialAnalysis='Новая текущая карточка прочитана полностью: вопрос уже о строительном использовании и континентальной коре, а не только о прежнем размере зерна. Easy допустим: общеизвестный строительный гранит и школьное различие гранитной континентальной/базальтовой океанической коры дают честное сужение. Базальт — содержательный магматический конкурент, мрамор и песчаник — правдоподобные строительные камни; все четыре — породы и самостоятельные именные ответы. Correct-note добавляет структуру/состав. Explanation содержит 2 предложения. Полный новый Syracuse HTML и его abstract прочитаны, исторический утраченный SHA не заменён и старый HOLD не переобъявлен PASS.',
 fields=[
 field('prompt-key','PASS','Новый abstract прямо говорит common use as a building material и abundance in continental crust; USGS подтверждает igneous. Особенно распространена читается как характерное широкое присутствие, не как строгий рейтинг самой распространённой породы. Совместные признаки выделяют гранит среди этих вариантов.','thompson-granite-abstract','usgs-granite-definition'),
 field('note0','PASS','USGS: light or speckled, coarse-grained igneous; quartz, feldspar, mica. Русская справка корректно даёт типичный светлый крупнозернистый гранит и основные кварц/полевые шпаты, без исключения слюды. Это дополнительный состав/структура сверх prompt.','usgs-granite-definition'),
 field('note1','PASS','NPS introduction прямо объясняет low silica → low viscosity → лёгкое течение на большие расстояния. Справка говорит обычно и не обещает одной скорости всем базальтовым потокам.','nps-basaltic-flows'),
 field('note2','PASS','Полный USGS текст подтверждает metamorphic и calcite crystals, также допускает non-calcite inclusions. Главным образом в справке сохраняет это ограничение.','usgs-marble-full'),
 field('note3','PASS','USGS определяет sandstone как осадочную породу chiefly of quartz grains. Это и есть обе части русского note.','usgs-sandstone-definition'),
 field('explanation','PASS','Первые два предложения оригинального abstract содержат building material/continental crust и From countertops to library steps. В отличие от одной авторской цитаты здесь привязано и конкретное перечисление примеров. Русский explanation из двух предложений точно передаёт их.','thompson-two-sentences')])]

proofs = json.loads((AUTHOR/'proof-index.json').read_text())['proofs']
def newproof(key, base, passage, locator):
    proofs[key]=dict(copy.deepcopy(proofs[base]), passage=passage, locator=locator)
newproof('finchale-parent','finchale-1196','By the mid 14th century this was serving as a holiday home for monks from Finchale’s parent monastery, Durham.','English Heritage rendered L220, paragraph on origins and parent monastery')
newproof('edward-context','edward-westminster','This led to the building of a new church in the Norman style to replace the Saxon church at Westminster.','Westminster Edward L3; read with L2 exile and L3 papal condition')
newproof('frederick-nickname','nla-frederick-periods','Frederick I, nicknamed Barbarossa (Red-Beard)','Met chronology L88, nickname clause only; erroneous emperor-at-1152 clause rejected')
proofs['frederick-nickname'].update(rawCapture='sources/frederick-met.txt', sourceClass='Metropolitan Museum of Art historical chronology', title='Central Europe (including Germany), 1000–1400 A.D. | The Metropolitan Museum of Art',url='https://www.metmuseum.org/ja/toah/ht/07/euwc',captureMethod='Existing full original web.open rendered response, 213 source lines; independently read L87-L89 including chronology error.')
newproof('richard-third-explicit','richard-crusade','He joined the Third Crusade to the Holy Land','Westminster Richard L3, first clause only; following false 1189 chronology rejected')
proofs['richard-third-explicit'].update(rawCapture='sources/richard-westminster.txt',sourceClass='Westminster Abbey royal biography',title='Richard I | Westminster Abbey',url='https://www.westminster-abbey.org/abbey-commemorations/royals/richard-i',captureMethod='Existing full original web.open rendered response, 86 source lines; independently read L3-L4 with contradictions recorded.')
newproof('usgs-marble-full','usgs-marble-calcite','The main difference between limestone and marble is that limestone is a sedimentary rock, typically composed of calcium carbonate fossils, and marble is a metamorphic rock.','USGS first prose paragraph (metamorphic); calcite clause separately bound below')
newproof('usgs-mineral','usgs-granite-definition','Mineral - a naturally occurring inorganic substance with an ordered structure; rocks are made of one or more minerals','USGS glossary, Mineral entry')
newproof('thompson-two-sentences','thompson-granite-abstract',"Granite is ubiquitously recognized by many people due to its common use as a building material and its abundance in the Earth's continental crust. From countertops to library steps, and as a source of economically important elements, granitic rocks are deeply intertwined with human development.",'Syracuse original abstract, first two sentences')
newproof('nps-gypsum-fresh','nps-gypsum-evaporation','Gypsum is an evaporate mineral--it dissolves in water and will recrystallize during evaporation of liquid, much like salt.','What is Gypsum?, second paragraph, sentence 2; original main prose matches web.open L27')
proofs['nps-gypsum-fresh'].update(rawCapture=str(HERE/'sources/nps-gypsum-original.html'),captureFormat='html original bytes',captureMethod='Independent curl --fail --location HTTPS 200 complete response, 36604 bytes; headers preserved in sources/nps-gypsum-headers.txt. Read main prose directly from raw HTML and corroborated via web.open on 2026-10-11. Python SSL failure retained separately; curl did not disable certificate verification.')

cards={c['id']:c for name in ['middle-ages','geology-earth'] for c in json.loads((REPO/f'src/content/topics/{name}.json').read_text())['questions']}
receipt=dict(role='independent',agentIdentity=os.environ['CODEX_THREAD_ID'], authorIdentity='01a12bd2-207a-7da1-9035-d9c7d5eeaa37', reviewedDate='2026-10-11',baselineCommit='c1ded1d',decisionMethod='Explicit manual six-field current literal and original-source reading; binder only serializes decisions and identities. Source locator metadata reused after actual independent raw passage reading; author verdicts are not imported.',cards=[])
for row in decisions:
    row=copy.deepcopy(row);c=cards[row['questionId']];row['cardCanonicalSha256']=sha(canonical(c))
    row['grammarSubstitutions']=[dict(reading=c['prompt']+' — '+a['text']+'.',verdict='PASS',analysis='Самостоятельная именная подпись, прочитана с полным вопросом; категория и сложность оценены отдельно.') for a in c['answers']]
    row['literalSnapshot']=c
    for f in row['fields']:
        n=f['field'];literal=[c['prompt'],c['correctIndex'],c['answers'][c['correctIndex']]['text']] if n=='prompt-key' else c['explanation'] if n=='explanation' else c['answers'][int(n[-1])]['note']
        f['literal']=literal;f['literalSha256']=sha(canonical(literal) if isinstance(literal,list) else literal.encode());f['proofs']=[]
        ids=f.pop('proofIds')
        if 'usgs-marble-full' in ids:ids.append('usgs-marble-calcite')
        if 'edward-context' in ids:ids.append('edward-westminster')
        for pid in ids:
            p=copy.deepcopy(proofs[pid]);raw=(AUTHOR/p['rawCapture']).resolve();p['proofId']=pid
            p['rawCapture']=os.path.relpath(raw,HERE);p['rawCaptureSha256']=sha(raw.read_bytes());p['passageSha256']=sha(p['passage'].encode())
            f['proofs'].append(p)
    receipt['cards'].append(row)
write('independent-receipt.json',receipt)
write('manual-decisions.json',dict(role='independent',agentIdentity=receipt['agentIdentity'],cards=decisions))
print('Serialized 5 explicit card decisions / 30 field decisions; no scripted substantive verdicts.')
