import json,pathlib,hashlib,subprocess,datetime
from html.parser import HTMLParser
P=pathlib.Path('docs/content-audits/question-quality-wave-7/process-v2-weather20');R=P/'reviewer'
def read(p):return json.load(open(p))
def canonical(o):return json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def sha(o):return hashlib.sha256(canonical(o)).hexdigest()
def git(x):return subprocess.check_output(['git','show',x])
def save(n,o):(R/n).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
a=read(P/'exact-fix-apply.json');scope=a['scope'];expected={e['id']:e['afterHash'] for e in a['applied']};topic=read('src/content/topics/weather-climate.json');qs={q['id']:q for q in topic['questions']};prev=read(R/'review.json');pre={e['id']:e['card'] for e in read(P/'preimage.json')['entries']};snapshot=read(R/'current20-snapshot.json');old={q['id']:q for q in snapshot['cards']}
# Source locators only; previous judgments/source reasons not used for rereview.
sources={s['locator']:s for s in read(R/'source-integrity.json')}
for s in read(R/'sources/manifest.json'):sources[s['locator']]=s
required=['nws-flight-environment','spc-parcel-values','spc-shear','nws-basic-fronts','nws-occluded','noaa-climate-zones','metoffice-climate-zones','noaa-weather-satellites','nws-stratus','nws-key-glossary','nws-radar','nws-radiosonde','nws-ceilometer','nws-cumulus','nws-cirrus']
class Text(HTMLParser):
 def __init__(self):super().__init__();self.d=[];self.skip=0
 def handle_starttag(self,t,a):
  if t in ['style','script']:self.skip+=1
 def handle_endtag(self,t):
  if t in ['style','script']:self.skip=max(0,self.skip-1)
 def handle_data(self,d):
  if d.strip() and not self.skip:self.d.append(d.strip())
texts={};integrity=[]
for k in required:
 s=sources[k]
 def get(f):
  item=s[f]
  if item.get('gitBlob'):return git(item['gitBlob'])
  if s.get('gitCommit'):return git(s['gitCommit']+':'+item['path'])
  return pathlib.Path(item['path']).read_bytes()
 b=get('body');h=get('headers')
 for f,v in [('body',b),('headers',h)]:assert len(v)==s[f]['bytes'] and hashlib.sha256(v).hexdigest()==s[f]['sha256'],(k,f)
 p=Text();p.feed(b.decode());texts[k]='\n'.join(p.d)
 integrity.append({'locator':k,'bodyBytes':len(b),'bodySHA256':hashlib.sha256(b).hexdigest(),'headersBytes':len(h),'headersSHA256':hashlib.sha256(h).hexdigest(),'actualBodyAndHeadersReadVerified':True})
# Compare current extraction to earlier durable transcript after actual-byte re-open.
prior_texts=read(R/'context-texts.json')
for k in required:
 if k in prior_texts:assert texts[k]==prior_texts[k],k
save('rereview-source-integrity.json',integrity)
W={
 'Струйное течение':'nws-flight-environment THE JET STREAM: narrow high-speed bands at 20–40 thousand feet, associated with tropopause; upper-atmospheric jet, not surface belt.',
 'Пассаты':'nws-flight-environment HEMISPHERIC PREVAILING WINDS: tropical cell produces northeast trades; Hadley cell surface flow is equatorward from subtropical sinking air.',
 'Западные ветры':'nws-flight-environment Ferrel cell: near-surface midlatitude air flows poleward and eastward, while circulation at 30–60° produces prevailing westerlies.',
 'Полярные восточные ветры':'nws-flight-environment Polar cell: sinking air makes polar highs and diverges outward at surface; surface polar winds are easterly.'}
S={
 'CIN':'spc-parcel-values CINH: integrated negative area in J/kg from original parcel level to LFC; energy needed to reach LFC.',
 'CAPE':'spc-parcel-values CAPE: integrated positive area in J/kg from LFC to EL; buoyancy/updraft energy, not a single-level temperature difference.',
 'Индекс поднятия':'spc-parcel-values LI: lifted parcel and sounding temperatures at 500 mb are compared; negative values mean parcel WARMER than environment. Therefore a literal Tparcel−Tenvironment formula cannot have the claimed negative sign for the warmer parcel.',
 'Спиральность шторма':'spc-shear SRH: storm-relative helicity represents streamwise vorticity WITHIN storm inflow layer, swept area between hodograph and STORM MOTION; reference is storm motion, not inflow-relative motion.'}
F={
 'Холодный фронт':'nws-basic-fronts Cold Front: denser cold air advances and displaces warm air; sufficient moisture gives rain and instability can give thunderstorms.',
 'Тёплый фронт':'nws-basic-fronts Warm Front: cold air must retreat before warm air advances; warm air ascends slantwise over cooler air and can give precipitation ahead with moisture.',
 'Стационарный фронт':'nws-basic-fronts Stationary Front: denser cool air does not retreat; balance means neither mass advances, so boundary barely moves.',
 'Фронт окклюзии':'nws-occluded Occluded Front: composite when cold front overtakes warm or quasi-stationary front; coldest-air placement distinguishes warm/cold occlusion.'}
C={
 'Экваториальный климат':'metoffice-climate-zones Tropical rainforest climate: equatorial regions have high temperatures and year-round rainfall, usually 20–30 °C with minor annual variation; NOAA A covers moist tropics.',
 'Полярный климат':'noaa-climate-zones E: year-round cold and warmest month below 10 °C; geography includes Antarctica. Met Office ice cap climates occur in Antarctic regions and have no month averaging above 0 °C.',
 'Пустынный климат':'metoffice-climate-zones Desert climate: subtropical descending air yields almost permanent high pressure and virtually year-round cloud-free skies. Gobi is a cold desert where annual average temperatures CAN BE below 0 °C; universal assertion without can is not established.',
 'Средиземноморский климат':'metoffice-climate-zones Mediterranean climate: dry summers and mild wet winters; occurrence on western coasts and California/Western Australia/Chile/South Africa.'}
O={
 'Кучевые облака':'nws-cumulus Cumulus: detached domes/mounds/towers, rounded tops and more horizontal bases; this supports the flat-base note.',
 'Перистые облака':'nws-cirrus Cirrus: high clouds composed of ice crystals, white delicate filaments and typical fibrous/hairlike appearance.',
 'Кучево-дождевые облака':'nws-key-glossary CUMULONIMBUS: cumulus with great vertical development, frequent thunderstorms/heavy rain and often anvil.',
 'Слоистые облака':'nws-stratus Stratus: low generally gray layer with fairly uniform base, may be ragged patches; fog usually a surface-based form.'}
I={
 'Метеорадар':'nws-radar RADAR/Radar Beam/Mosaic: reflected radio waves from targets, precipitation targets with limited coverage; surface radar gives detailed regional mosaics, not an optical image of all cloud cover.',
 'Геостационарный метеоспутник':'noaa-weather-satellites Geostationary Satellites: located over equator, orbit in 24 hours, fixed Earth-relative perspective permits measurement of cloud motion; polar views limited by Earth curvature.',
 'Радиозонд':'nws-radiosonde Radiosonde: balloon carries transmitter for temperature, pressure, humidity; tracking by radar/radio direction/navigation gives WIND. Note that wind is obtained by tracking, not a direct humidity/temperature payload measurement.',
 'Цеилометр':'nws-ceilometer Ceilometer: light/laser measures cloud-base height, optical triangulation or laser pulse travel time; local base measurement rather than regional cloud imagery.'}
# Fresh judgments of CURRENT11 only. No second fix cycle requested.
J={
 'cin-cap':('HOLD',[('note3','SRH назван «Спиральность шторма относительно притока». SPC задаёт относительность к движению шторма, а приток — слой вычисления. Фраза смешивает систему отсчёта с местом вычисления.')],'note0 добавляет измерение энергии в Дж/кг, поэтому прежний дефект повторения закрыт; новая note3 не соответствует primary определению.'),
 'cold-front-symbol':('PASS',[],'note2 добавляет большую плотность холодной массы, которой не было в prompt; механизм и условные дождь/гроза подтверждены NWS.'),
 'desert-dry':('HOLD',[('source.url','Карточка показывает NOAA Climate Zones, где нет нового главного факта о почти постоянном субтропическом высоком давлении и почти безоблачном небе. Этот факт найден в Met Office Desert climate; точный игровой URL остался от прежней карточки.')],'Правильная note даёт самостоятельный условный факт о холодной Гоби; вопрос о механизме субтропических пустынь отличен от буквенного критерия B Кёппена. Точный source.url не соответствует новому спрашиваемому факту.'),
 'lifted-index':('HOLD',[('note1','Tчастицы−Tсреды отрицательно при ХОЛОДНОЙ частице, а note говорит, что отрицательно при тёплой. Фактическое противоречие: LI с указанной интерпретацией знака требует Tсреды−Tчастицы.','explanation'),('note1','«индекс равен температуре ... минус температуру» не согласовано: исходная конструкция с равен требует согласованной формы для разности.'),('note3','«относительно притока» подменяет storm-relative, как в CIN; SPC говорит о завихренности в слое притока относительно движения шторма.')],'Английский sounding убран и 500 мб вынесено в note как допфакт, но формула знака стала неверной. Описание SPC «difference between» без порядка нельзя трактовать вопреки следующему предложению о warmer parcel.'),
 'occluded-front':('PASS',[],'note1 теперь говорит о границе холодного воздуха без погони за «ним». Note3 сверх prompt добавляет возможность обгона квазистационарного фронта; источник определяет два типа окклюзии.'),
 'polar-cold':('HOLD',[('note2','Met Office: annual average temperatures CAN BE below 0 °C. CURRENT утверждает безусловно, что вся Гоби «имеет среднюю годовую температуру ниже 0 °C», утратив оговорку и распространив локально возможное свойство на пустыню целиком.')],'note1 теперь добавляет температурный порог, отсутствующий в Antarctic prompt; прежняя неподтверждённая холодная пустыня Антарктиды удалена. Новое утверждение о Гоби выходит за прочитанный primary.'),
 'polar-easterlies':('HOLD',[('prompt','«в полярной ячейке» почти дословно указывает единственный вариант «Полярные восточные ветры». Удаление слов «с востока» не устранило подсказку: medium не требует знания модели, достаточно сопоставления слова полярный.')],'note3 добавляет опускание плотного холодного воздуха и полярный максимум, подтверждённые NWS. Факт ключа устойчив, но абсолютный medium нарушен очевидной словесной подсказкой.'),
 'satellite-clouds':('HOLD',[('prompt','Главный признак «почти неизменная точка обзора» → геостационарный спутник повторяет spaceflight-geo-fixed («орбита позволяет казаться неподвижным»). Обзор облаков задаёт применение той же связи, но нового различения наблюдательных свойств не требует.')],'Уточнение геостационарного типа корректно; note1 добавляет экватор и 24 часа. Однако семантический repeat основного признака фиксированной перспективы с spaceflight-geo-fixed не закрыт; GOES/ABI сосед спрашивает серию и сам по себе не дубль.'),
 'stationary-front':('HOLD',[('note2','Note2 вновь повторяет весь prompt: фронт почти не движется, когда массы не вытесняют друг друга. Отсутствие отступления холодного воздуха из prompt просто пересказано как отсутствие вытеснения; нового самостоятельного факта нет.')],'Неподтверждённая обязательная облачность/осадки убраны. Правильная note практически не изменилась и не выполняет требование дополняющего факта.'),
 'stratus-layer':('PASS',[],'note3 теперь даёт новый факт: туман обычно является приземной формой stratus. Четыре рода облаков, key, explanation и все notes подтверждены прочитанными NWS entries.'),
 'westerlies-midlat':('HOLD',[('note3','Новая справка говорит о любом движущемся воздухе в Северном полушарии и не связывает факт с Западными ветрами. Тот же текст подходит пассатам/полярным восточным/струйным течениям. Нужен самостоятельный факт о конкретном варианте, а не общий принцип атмосферы без связи с ним.')],'Кориолисовское отклонение вправо подтверждено NWS, но literal правильной справки не сообщает свойства конкретно западного пояса. Сам вопрос остаётся отличным от полярной/тропической циркуляции и высотной струи.')}
family_ids={
 'wind':['westerlies-midlat','polar-easterlies','jet-stream-fast'],
 'diag':['cin-cap','lifted-index','cape-buoyancy','inversion-positive'],
 'climate':['desert-dry','polar-cold','koppen-dry-b','koppen-polar-e','koppen-tropical-a','equator-hot','mediterranean-dry-summer'],
 'front':['cold-front-symbol','stationary-front','occluded-front','frontal-rain'],
 'cloud':['stratus-layer','cirrus-feathery','cumulonimbus-storm'],
 'instrument':['satellite-clouds']}
source_keys={'wind':['nws-flight-environment'],'diag':['spc-parcel-values','spc-shear'],'climate':['noaa-climate-zones','metoffice-climate-zones'],'front':['nws-basic-fronts','nws-occluded'],'cloud':['nws-stratus','nws-cumulus','nws-cirrus','nws-key-glossary'],'instrument':['noaa-weather-satellites','nws-radar','nws-radiosonde','nws-ceilometer']}
maps={'wind':W,'diag':S,'climate':C,'front':F,'cloud':O,'instrument':I}
neighbor_reasons={
 'wind':'CURRENT jet-stream-fast — верхняя узкая скоростная струя; западный пояс — Ferrel, полярный — Polar. Разные циркуляционные структуры. Нынешний полярный prompt всё ещё даёт словесную подсказку.',
 'diag':'CURRENT CAPE — положительный интеграл между LFC/EL, CIN — отрицательная энергия до LFC, LI — температурная разность на 500 мб. CURRENT inversion-positive задаёт численный профиль/барьер, не индекс. SRH — другой физический диагностический параметр.',
 'climate':'CURRENT koppen-dry-b — буквенная группа по испарению/осадкам; desert спрашивает субтропическое формирование. CURRENT koppen-polar-e — буквенная группа по порогу; polar-cold — температурный тип Антарктиды. CURRENT Mediterranean H10 спрашивает сезонность осадков, equator-hot — годовую вариацию. Эти факты различаются; новые neighbour conclusions не кредитуются.',
 'front':'Наступление холодной массы, почти неподвижная граница и составная окклюзия — разные сценарии; frontal-rain классифицирует осадки. Исправление note не создало дубля.',
 'cloud':'CURRENT cirrus спрашивает высокие перья, cumulonimbus — грозовую связь; stratus — низкий слой и теперь fog в correct note. Разные cloud genera/признаки.',
 'instrument':'CURRENT spaceflight-geo-fixed использует ту же связь геостационарности с неподвижной перспективой; добавление облачного покрова не требует иного знания. GOES/ABI спрашивает конкретную серию и не дублирует тип спутника.'}
levels={'wind':'medium требует знакомства с циркуляцией; polar prompt имеет прямую подсказку и этого уровня не достигает.', 'diag':'hard: специфическая диагностика зондирования, физически различимые энергия, температура и завихренность.', 'climate':'easy: Антарктида/климатические контрасты широко знакомы; ясное небо даёт допустимый вывод о засушливости, хотя текст о субтропическом давлении сложнее общего критерия сухости.', 'front':'easy для холодного/стационарного поверхностного сценария; medium для составной окклюзии.', 'cloud':'easy: распространённые облачные формы для взрослой аудитории.', 'instrument':'medium для метеорологических систем, однако проверяемая связь фиксированной перспективы совпадает с существующей easy orbit-карточкой.'}
entries=[]
for id in scope:
 q=qs[id];s=id.removeprefix('weather-climate-');f=next(k for k,v in family_ids.items() if s in v);v,issues,why=J[s];idx=q['correctIndex'];assert sha(q)==expected[id]
 for k in ['id','difficulty','correctIndex']:assert q[k]==pre[id][k]
 reasons=[maps[f][b['text']] for b in q['answers']]
 # One explicit reason for each of the four substitutions; note groups separately checked.
 groups=[{'group':'prompt_ordered_answers_key','literal':{'prompt':q['prompt'],'answers':[b['text'] for b in q['answers']],'correctIndex':idx},'sourceReasons':reasons,'editorialReason':'Четыре подстановки прочитаны лично: '+q['prompt']+' / '+' / '.join(b['text'] for b in q['answers'])+'. Последовательные самостоятельные именные ответы; grammar/key/distractor category проверены. '+levels[f]+' '+why}]
 er=reasons[idx]
 if s=='desert-dry':er+=' Второе предложение о «не критерий B» — сравнение двух primary: NOAA B defines evaporation/transpiration>precipitation; Met Office passage defines subtropical mechanism.'
 if s=='stationary-front':er+=' NWS balance does not logically imply mandatory rainfall: отсутствие обязательности — корректный предел вывода из описанного механизма.'
 groups.append({'group':'explanation','literal':q['explanation'],'sourceReasons':[er],'editorialReason':'Два предложения, ключ назван, отличительный механизм объяснён; '+why})
 for n,b in enumerate(q['answers']):
  reason=reasons[n]
  if s=='westerlies-midlat' and n==3:reason='nws-flight-environment: Coriolis deflects air RIGHT in Northern Hemisphere; factual literal is supported, but it states general moving-air law, not a west-wind-specific property.'
  if s=='polar-easterlies' and n==3:reason='nws-flight-environment Polar cell and preceding cold-air paragraph: cold dense polar air sinks, creates high pressure, then diverges at surface. Correct note adds this causal context beyond prompt.'
  if s=='cin-cap' and n==0:reason='spc-parcel-values CINH gives negative-area integral IN J/kg; unit is a new fact beyond prompt.'
  if s=='polar-cold' and n==2:reason='metoffice-climate-zones Desert climate says Gobi annual averages CAN BE below 0°C; does NOT establish categorical temperature below zero for entire Gobi. Literal exceeds primary qualification.'
  if s=='stationary-front' and n==2:reason=F[b['text']]+' Fact true, but note duplicates the queried immobility/no-retreat mechanism.'
  if s=='stratus-layer' and n==3:reason='nws-stratus Stratus final sentence: Fog usually is a surface-based form of stratus. New correct-note fact, not in prompt.'
  gissues=[z[1] for z in issues if z[0]=='note'+str(n)]
  groups.append({'group':'note'+str(n),'literal':b['note'],'sourceReasons':[reason],'editorialReason':('Правильная справка: '+why if n==idx else 'Самостоятельное содержание о названном дистракторе проверено лично; '+(' '.join(gissues) if gissues else 'относится к этому варианту, факты не подменены свойствами ключа.'))})
 for g in groups:g['literalSHA256']=sha(g['literal'])
 neighbors=[]
 for ni in family_ids[f]:
  nid='weather-climate-'+ni
  if nid!=id:neighbors.append({'id':nid,'currentHash':sha(qs[nid]),'prompt':qs[nid]['prompt'],'correctAnswer':qs[nid]['answers'][qs[nid]['correctIndex']]['text'],'readStatus':'ACTUAL_CURRENT_READ_FOR_DEPENDENCY_ONLY; no credit inferred'})
 e={'id':id,'currentHash':sha(q),'verdict':v,'fieldGroups':groups,'sourceLocators':[{'locator':k,**sources[k]} for k in source_keys[f]],'neighborReview':{'currentNeighbors':neighbors,'editorialReason':neighbor_reasons[f]},'defects':[{'fields':[z[0]]+list(z[2:]),'detail':z[1]} for z in issues],'nextAction':('Координатор: принять точный hash после adjudication и сохранить результат.' if v=='PASS' else 'Координатор: оставить CURRENT вне зачёта как HOLD; дефекты сохранены для отдельного решения. Единственный fix-cycle исчерпан, второй в этом пакете не запускать.'),'frozenContract':{'id':True,'topic':True,'position':True,'difficulty':True,'correctIndex':True},'difficultyReview':{'frozen':q['difficulty'],'absoluteAssessment':levels[f]},'scopeReview':{'topicId':'weather-climate','withinScope':True,'reason':'Спрашивается метеонаблюдение, атмосферная циркуляция, фронт, облако или климат; экологическая политика/общая отвлечённая физика не являются предметом вопроса.'},'sourceLinkReview':{'url':q['source']['url'],'verifiedAt':q['source']['verifiedAt'],'mainFactConfirmedByDisplayedSource':s!='desert-dry','reason':'Точная primary страница подтверждает главный факт.' if s!='desert-dry' else 'Main fact found only in captured Met Office Desert climate; displayed NOAA Climate Zones URL lacks this fact.'}}
 if s=='satellite-clouds':
  sp={c['id']:c for c in read('src/content/topics/spaceflight.json')['questions']};e['neighborReview']['crossTopicNeighbors']=[{'id':n,'currentHash':sha(sp[n]),'prompt':sp[n]['prompt'],'correctAnswer':sp[n]['answers'][sp[n]['correctIndex']]['text']} for n in ['spaceflight-geo-fixed','spaceflight-goes-weather']]
 if f=='climate':
  e['neighborReview']['h10CurrentNotCredited']=[{'id':n,'currentHash':sha(qs[n]),'role':'Observed current dependency, not accepted/credited by this review'} for n in ['weather-climate-mediterranean-dry-summer','weather-climate-iod-indian']]
  e['neighborReview']['h10Reason']='Mediterranean actual current seasonality compared above; IOD actual current asks an Indian Ocean SST/rainfall dipole, not climate-type classification or desert formation.'
 entries.append(e)
# Unchanged previous PASS7 checked only mechanically; their contents not rereviewed.
pass7=[e for e in prev['entries'] if e['verdict']=='PASS']
for e in pass7:assert sha(qs[e['id']])==e['currentHash']
hold2=['weather-climate-bergeron-ice','weather-climate-warm-cloud-collision']
for i in hold2:assert sha(qs[i])==sha(old[i])
base=json.loads(git(prev['baselineCommit']+':src/content/topics/weather-climate.json'))
assert [(i,q['id']) for i,q in enumerate(topic['questions']) if q['id'] in scope]==[(i,q['id']) for i,q in enumerate(base['questions']) if q['id'] in scope]
counts={v:sum(e['verdict']==v for e in entries) for v in ['PASS','HOLD']}
result={'reviewerThreadId':'01a13bb3-f49e-7001-a980-fa3fba1f72b3','reviewedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'baselineCommit':prev['baselineCommit'],'cycle':1,'scope':scope,'counts':counts,'entries':entries,'unchangedPass7':{'mechanicalHashVerificationOnly':True,'ids':[e['id'] for e in pass7],'notRereviewed':True},'unchangedHold2':{'mechanicalHashVerificationOnly':True,'ids':hold2,'notRereviewedNotCredited':True},'process':'Personally read actual CURRENT11 and primary bodies, verified exact bytes+SHA. No author verdict inherited, no subagents/chats/downloads/second fix cycle. Actual changed Weather15 and H10 dependencies read without credit.','checks':{'all11MatchAfterHash':True,'originalTopicPositionsFrozen':True,'frozenIdDifficultyKey':True,'sixLiteralGroupsWithCanonicalSHA256':True,'notesWithin35Words':all(len(b['note'].split())<=35 for id in scope for b in qs[id]['answers']),'explanationsWithin70Words':all(len(qs[id]['explanation'].split())<=70 for id in scope),'runtimeBuildFullQA':'NotRun: outside task scope'},'stopCondition':'Rereview of the single fix cycle complete; unresolved defects are HOLD, no further fixes authorized in this batch.'}
save('rereview.json',result);save('rereview-current11-snapshot.json',{'topicId':'weather-climate','scope':scope,'cards':[qs[i] for i in scope]});save('pass-fix-cycle-current.json',{'reviewerThreadId':result['reviewerThreadId'],'entries':[{'id':e['id'],'currentHash':e['currentHash']} for e in entries if e['verdict']=='PASS']})
lines=['# CURRENT11 — итог единственного fix-cycle','',f"Независимое rereview: **PASS {counts['PASS']}, HOLD {counts['HOLD']}**. Exact CURRENT11 совпадает с afterHash в exact-fix-apply.json; исходные id/topic/position/difficulty/key сохранены.",'','## PASS','']+[f"- `{e['id']}` — {J[e['id'].removeprefix('weather-climate-')][2]}" for e in entries if e['verdict']=='PASS']+['','## HOLD без второго fix-cycle','']+[f"- `{e['id']}`: "+' '.join(d['detail'] for d in e['defects']) for e in entries if e['verdict']=='HOLD']+['','## Проверки и сохранение','','Лично прочитаны actual CURRENT11: prompt/4 substitutions/key, explanation/4 notes, grammar, absolute difficulty, plausible homogeneous distractors, six exact literal groups, topic scope and semantic neighbours. Прочитаны actual Weather15 dependencies и H10Ready2 (Mediterranean/IOD); их статус не засчитывался. Для спутника проверены actual spaceflight-geo-fixed и spaceflight-goes-weather; для климата — current Köppen A/B/E.','', '15 используемых сохранённых primary body/header контекстов снова открыты по Git blobs/55db9891 или reviewer/sources и сверены bytes/SHA; сохранённые транскрипты сверены с повторной extraction из actual body. Источники не скачивались повторно. Все sourceReasons сформулированы независимо по лично прочитанному материалу; авторские PASS/FIX не унаследованы.','', 'Предыдущие 7 PASS и 2 HOLD проверены лишь по hash на unchanged, без повторного содержательного чтения. Добавлено 3 PASS из fix-cycle; пакет теперь имеет 10 доказанных PASS и 10 HOLD (8 новых unresolved + 2 прежних). Это результат reviewer, adjudication/credit остаются за координатором.','', 'Выполнены целевые exact-hash/frozen/group/word-limit/source-integrity и whitespace checks. Full QA/build/runtime NotRun: вне scope. Только reviewer/ записи, каталог/index/claims не менялись. Новых процессов, скачиваний и временных сборок нет.','', 'Новые rereview файлы находятся в ветке `codex/question-quality-wave-6`, без собственного коммита: commit выполняет координатор. В main новые результаты этого rereview не интегрированы.','', 'Следующий шаг: координатор выполняет adjudication, сохраняет reviewer/ в Git и оставляет unresolved в HOLD без второго fix-cycle. До сохранения новых файлов сессию архивировать нельзя.']
(R/'report-final.md').write_text('\n'.join(lines)+'\n');print(counts)
