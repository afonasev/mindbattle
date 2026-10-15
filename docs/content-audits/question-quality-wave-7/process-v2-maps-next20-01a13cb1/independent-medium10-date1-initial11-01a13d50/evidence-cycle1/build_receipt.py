import json,pathlib,hashlib,subprocess
R=pathlib.Path.cwd();B=R/'docs/content-audits/question-quality-wave-7/process-v2-maps-next20-01a13cb1';O=B/'independent-medium10-date1-initial11-01a13d50';E=O/'evidence-cycle1'
def rd(p):return json.loads(p.read_text())
def sha(x):return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
REQ=rd(B/'fix-request-medium-initial9-cycle1.json');PRE={x['id']:x for x in REQ['entries']};C={q['id']:q for q in rd(E/'current-topic.json')['questions']};NOW={q['id']:q for q in rd(R/'src/content/topics/maps-cartography.json')['questions']};ACT=rd(E/'actual-peers.json');IP=rd(O/'evidence/primary-read-index.json');AP={};AUTHOR={}
for part,label in [('first3-completion','first3'),('remaining6-completion','remaining6')]:
 for x in rd(B/f'exact-apply-medium-{label}-cycle1-01a13d50.json')['applied']:AP[x['id']]=x
 for x in rd(B/'fix-medium9-cycle1-author-01a13d50'/part/'sourceproof.json')['entries']:AUTHOR[x['id']]=x
BASE=json.loads(subprocess.check_output(['git','show','0ae8e14e535c74000ebc8e4cbc7dbdc479aca91b:src/content/topics/maps-cartography.json']))
ORD={q['id']:i+1 for i,q in enumerate(rd(E/'current-topic.json')['questions'])};BASEORD={q['id']:i+1 for i,q in enumerate(BASE['questions'])}
AM=rd(B/'qa-format-amendment-utm-cycle1-01a13d50.json');PEERS=rd(E/'author-peer-snapshots.json')
# Grounds correspond to prompt+ordered answers+key, explanation, note0, note1, note2, note3.
J={
'spot-elevation':{'status':'PASS','sources':[0]*6,'level':'MEDIUM: две независимые разности 720−700=20 и712−700=12, с различением контура и точечной отметки. Числа теперь участвуют в решении, устраняя прежнюю easy-подмену.', 'grounds':[
'USGS p1 Reading Topographic Maps: interval — разность соседних линий. Prompt явно называет линии соседними, поэтому20; point712 выше700 на12. Только индекс1 даёт обе требуемые величины без переноса точки на линию.',
'720−700=20;712−700=12. Отдельный × с числом не задаёт высоту протяжённого контура и сам не доказывает класс контрольной марки (USGS p3).',
'Для12м note выбирает правильные входы: два соседних контура, а не point minus contour. Это точечная коррекция реальной ошибки.',
'Расширение индекса широкой линией и повторные подписи — отдельный факт изUSGS p1 lines74–75 сверх prompt/key. Полезен при чтении этой же карты; не attribution.',
'Для назначения контуру712 note возвращает свойство equal elevation и запрещает перенос точечной метки на линию (p1,p3).',
'Для необоснованного репера note указывает раздельные легендные записиUSGS p3; маленький× spot elevation и контрольные marks различимы в PNG. Она не объявляет любой знак× универсально не-репером.'], 'choices':[
'Неверно:12 — превышение точки, а не сечение; грамматика корректна, ошибка неверной пары вычитания правдоподобна.',
'Верно:20 и12; единый ключ. Note добавляет факт об индексных горизонталях.',
'Неверно: сечение20 верно, но ближайшая линия700/720 не приобретает высоту712 от отдельной точки; правдоподобное смешение точки и линии.',
'Не следует: сечение20 верно, контрольный статус× не доказан без легенды/марки. Как ответ на две величины неполон, но недоказанная подмена статуса точки в relief-контексте правдоподобна.'], 'peers':'contour-interval/line дают базовые определения, index-contour считает другие переходы. Новый benchmark CURRENT содержит recoverable/no-tablet/grade и иной предмет контроля; его note не поставляет20/12. Старый и новый proposed benchmark прочитаны; нет прямого дубля расчёта.', 'defects':[]},
'choropleth-shading':{'status':'PASS','sources':[1]*6,'level':'MEDIUM: вычислить два отношения18/300 и36/400, перевести в проценты, отнести оба к5–10%, отличить общий класс от точного равенства; answer не дан в prompt.', 'grounds':[
'Graduated colors opening + normalization:18/300=.06=6%;36/400=.09=9%. Оба внутри5–10%, не на границах. Только1 объединяет правильные расчёты и общий класс.',
'Цвет класса одинаков, значения6/9 разные; физическая площадь полигонов не входит в знаменатель доли домов. Источник различает class color и numeric magnitude.',
'Для ошибки по сырым количествам note правильно требует знаменатель — общее число домов своего района. Не переносит знаменатель между районами.',
'Источник opening line16 прямо говорит size of symbols stays same. Новый факт — значение кодируется цветом без изменения symbol size; это про канал символизации, не утверждение, что площади всех реальных районов равны. Он отсутствует в prompt/key.',
'Для9→10–15 note верна: интервал включает9 в5–10, округление не является правилом перескакивать через границы; ни boundary equality, ни round ambiguity в данных нет.',
'Дляequal exact note показывает class range, внутри которого много значений. Это специфическая поправка кsame color→same exact.'], 'choices':[
'Неверно:6% не0–5, хотя в этом набореY действительно имеет большую долю; причинный вывод по абсолютному числу недостаточен. Частично верный итог не создаёт второй ключ.',
'Верно:6%,9%,оба5–10%,общийцвет без точногоравенства. Note — новый символизационный факт.',
'Неверно:9% не попадает10–15; plausible rounding-to-break ошибка, к которой адресованаnote.',
'Неверно: обакласса верны, но6≠9; plausible confusion class/exact value.'], 'peers':'natural-breaks/standard-deviation говорят о способах классификации, dot-density о весе точек, isoline о поле. Их CURRENT и сохранённые proposed не дают18/300 или36/400 и не дублируют новую нормализацию; стандартные определения классов — общая база, не раскрытый числовой ключ.', 'defects':[]},
'dot-density':{'status':'PASS','sources':[4]*6,'level':'MEDIUM: рассчитать1800/2800, разность1000 и общий4600, отделить перерисовку seed от перемещения жителей. Это составная количественная интерпретация.', 'grounds':[
'Esri Dot density opening constant weight200. 9×200=1800;14×200=2800;разность1000,сумма4600. Maintain placement допускает regenerate seed без изменения населения. Только1 отвечает всем трём частям.',
'Арифметика и отсутствие адресной интерпретации корректны: случайные dots лежат внутри полигонов, отдельные точки не query individual records.',
'Для5/23 note использует вес200, а не считает точки людьми. Это именно unit-weight ошибка данного варианта.',
'Esri Caution lines120–123 требует equal-area CRS для валидных визуальных сравнений density. Новый факт о проекции отсутствует в prompt/key; связан с корректным использованием той же dot-density карты.',
'Дляобщего2800 note требует сложения двух участков; не повторяет false total как верный.',
'Дляложного переезда note привязывает reshuffle к алгоритмическому размещению внутри полигона, не адресам; прямой Esri regenerate-placement context.'], 'choices':[
'Неверно:5 и23 — количества точек, не жителей; грамматика корректная, plausible забытый вес.',
'Верно:1000,4600,no evidence move; key единственный, note добавляетequal-area.',
'Неверно:разность1000 верна,2800 толькоB и неtotal; plausible omission A.',
'Неверно:оба числа верны, но seed reshuffle не наблюдение физических переездов; plausible diagram/data confusion.'], 'peers':'choropleth рассчитываетдоли/классы, flow-map объёмы поездок, raster/vector peers другой data-model. CURRENT и уже существующие proposals maps61–70 не раскрывают1000/4600 и не дублируют aggregate-versus-seed задачу.', 'defects':[]},
'isoline-value':{'status':'PASS','sources':[5]*6,'level':'MEDIUM: найти долю(15−12)/(24−12)=1/4, умножить8км и отличить модель от station measurement. Линейнаяинтерполяция задана явно; специальных формул на память не требуется.', 'grounds':[
'Esri contouring example использует linear interpolation для target contour между точками. При12→24 на8км,15 находитсяна3/12=1/4пути:2км. Это поверхностьмодели, не отдельнаястанция. Только1.',
'Перепад12°C,целевойприрост3°C,путь2км; source contourquality отделяет raster interpretation отactualsurfaceaccuracy.',
'Для6км note объясняет ошибочное обращениеfraction:3из12четверть,не3/4. Корректно ксвоейошибке.',
'Esri opening paragraph послеопределения:closer contours показываютбыстрыеизменения. Новыйфактоградиенте/spacing,неповтор2кмиstation distinction; полезенвчтенииполя.',
'Для4км note вычисляетmidpoint18°C,не15. Корректнаяspecificпроверкасередины.',
'Дляневозможностиизотермы note вернопоказываетderivedcontourмеждуobservations; source example прямоинтерполируетмеждупиксельнымицентрами.'], 'choices':[
'Неверно:6кмсоответствует21°C,а не15; stationclaimтоженеверен; plausible reversedfraction.',
'Верно:2км,значениемодели; единыйключ. Noteдобавляетspacing/gradient.',
'Неверно:середина8кмдаёт18°C; plausible automaticmidpoint.',
'Неверно:точноеизмерение15настанциинетребуетсядляinterpolatedcontour; plausible measurement/modelconfusion.'], 'peers':'close-steep/wide-gentle CURRENT/partial-HOLD тожеучатрасстоянияммеждулиниями,нонеfractioninterpolation; ихnotesневыдают2км. contour-line/intervalдаюттопографическиетермины. Raster-current/proposedобъясняютячейки,нечисленныйпрофиль12→24.', 'defects':[]},
'flow-map':{'status':'PASS','sources':[6]*6,'level':'MEDIUM: отношение120/40=3 и суммавходящего/исходящегоC120+30=150, два независимых показателя и канала карты. Ошибки теперь арифметически/семантически правдоподобны.', 'grounds':[
'ICA полный abstract:width relativequantity,node diameter totalin/out,arrowsdirection. Prompt задаёт именно этиусловия. Только1даётratio3иtotal150.',
'120/40=3,120+30=150. Суммируютсяобъёмыпоездок,анеподразумевается150уникальныхлюдей. Curvingforlegibility источникразрешает.',
'Дляобратногоratio note верно40=120/3 и arrowdirectionнепереопределяетcount.',
'ICA opening:curving flows reduceintersections/overlap. Новыйпрактическийфактотрисовкисверхзаданныхwidth/direction/node-total,неattribution.',
'Для80× note различаетразность80иratio3; отвечаетглавнойошибкеэтоговарианта,хотянеповторяетещёошибкуnode120.',
'Дляonlyincoming120 note явнодобавляетoutgoing30; source node-totalin/out точноотноситсякэтомуварианту.'], 'choices':[
'Неверно:ratioобращён,хотяsum150верна; plausible inversecomparison.',
'Верно:ratio3,total150; noteновыйcurvingfact.',
'Неверно:разность80не80-кратнаяширина;totalCне120. Двойнаяошибка,нообестандартныеreadoutпутаницы,не«перемещающиесякилометры».',
'Неверно:ratio3верен,сумма120пропускаетoutgoing30; plausible incompleteflowaggregation.'], 'peers':'dot-densityумножаетsymbolweightнасчёт,choroplethдоли,а flow-mapсравниваетedgesиnode-total. Староеflow-definitionнеснабжало150;actual/proposedpeersнеповторяютэтупаруопераций.', 'defects':[]},
'latitude-ns':{'status':'HOLD','sources':[7,7,7,7,7,8],'level':'MEDIUM по сути:444/111=4,37S−4°north=33S,безпересеченияэкватора. Ошибкидистракторовохватываютзнак,полушарие,ось.', 'grounds':[
'NOAA Latitude north/south отequator плюс111км/градус. −37+4=−33. Только1. Висходномматематическомфрагменте37S−4понимаетсямодульюжнойшироты,аполушариесохранено.',
'444/111=4;33S;экватордалеко. Финальнаяпунктуационнаяправкаexplanationсохраненаиучтенаточнымhash.',
'Содержаниенote0верно:северныйходвЮжномполушарииуменьшаетмодуль. Но «На южном полушарии» —неправильнаярусскаялокативнаяформа;здесьнужно«В Южном полушарии».CURRENTцеломнепроходитgrammar.',
'NOAA заключительныйcontextотличаетellipsoidотperfectsphereиговоритосложностиhighaccuracy. Новыйфактоприроде111кмприближениясверхprompt/key,безанглийскогоостатка.',
'Для33N note вернопроверяет,что4<37;знакменяетсятолькопослеэкватора.',
'Для37S note верно:meridianпостояннойlongitude,ходnorth/southменяетlatitude. NOAA Longitudeopeningэтообосновывает.'], 'choices':[
'41Sневерно:модульувеличенвневерномнаправлении;plausible signerror. Noteфактическикорректна,но«На...полушарии»грамматическинеисправлено.',
'33Sверно:4°севернее;noteоприближениидаётдобавочныйфакт.',
'33Nневерно:переход4°непересекает37°доequator;plausible hemispheremarkererror.',
'37Sневерно:перепутаныlatitude/longitudeвдольmeridian;plausible axisswap.'], 'peers':'equator/parallel CURRENTдают0/111км,ноне33S. Longitudeпроверяетtime→west,nogridsourcechangesвgrid-squareнеподсказываютlatitude. Обевстреченныесохранённыеproposedверсииисследованы;новыедатчики40N/40SнеCURRENT.','defects':[{'field':'answers[0].note','kind':'language','defect':'«На южном полушарии» — некорректный предлог для нахождения отряда; нормативная форма «В Южном полушарии». Это оставшийся языковой дефект точного CURRENT после использованного substantive cycle.','needed':'Нового primary не нужно: фактическая часть подтверждена. Координатор фиксирует terminal HOLD этой версии и решает disposition конкретной механической редакторской поправки в уже разрешённом scope; reader не запускает второй substantive cycle и не меняет каталог.'}]},
'longitude-ew':{'status':'PASS','sources':[8]*6,'level':'MEDIUM: перевести24минв0,4часа,добавить2часа,умножитьна15иопределитьзападныйзнак;дистракторыправдоподобнопутаютзнак,неполныечасыиangularminutes.', 'grounds':[
'NOAA localnoon/GMTexample:Greenwich14:00приlocalnoon→west. 14:24−12:00=2,4h;×15=36W. Единственный1.',
'Расчёт2,4×15=36ипозднийпоGreenwichclocklocalnoonзначитwest. Explanationраскрываетзападнуюдолготусловами,technicalformatнеизменилmeaning.',
'Прежняяошибкаисправлена:для36Eполденьпри09:36Greenwich,раньше12;для36Wпри14:24,позже. Noteправильноотвергаетeast.',
'NOAA Longitudeparagraphпроspacing:111кмнаequator,56кмна60°,схождениеуполюсов. Этоотдельныйгеометрическийфактсверхtimeconversion,неповторкоэффициента15.',
'Для30W note вернотребуетучестьfractionhour. 24minдаёт6°,не0.',
'Для2°24′ note объясняетразныеединицыtimeиangleсмасштабом15;24timemin≠24arcmin.'], 'choices':[
'36Eневерно:времяуказанопослеполудняGreenwich;причинноепредложениеопозднемполудневерно,новыводeastложен. Noteтеперьисправляетименноошибкузнака.',
'36Wверно:2h24min=2,4h;одинключ. Noteдаётновыйspacingfact.',
'30Wневерно:24minнельзяопустить,добавка6°;plausible roundingdown.',
'2°24′неверно:цифрыпоказанийперенесеныбезмасштаба15;plausibletime/angularconfusion.'], 'peers':'prime-zero-long/date-lineдают0/180,не36W;latitudeтакжетребуетчисленногоперехода,ноинойоси. Сохранённыйстарыйproposedlongitude14:00/30WнеCURRENTинеотменяетличнуюпроверкуисправленногоnote0.', 'defects':[]},
'utm-zones':{'status':'PASS','sources':[9,9,9,9,9,10],'level':'MEDIUM: от180Wдойтидо75W(105°),разделитьна6,взять17полныхзон+1=18;по40NвыбратьN,отличитьзнакlongitudeотhemisphere. Нумерация/ширина даны, а result не дан.', 'grounds':[
'Esri SDKRemarkszone1starts180W,6°wide;zone18covers78–72W. −75внутри,40Nсевер. Только18Nиндекс1,неboundarycase.',
'180−17×6=78;180−18×6=72. 75Wвнутри. Полушариезадаётlatitude. UPSвнеобычногоUTMcoverage,40Nнеpolar. Финальныйabbreviationamendmentнеизменилzone/hemisphere.',
'Для17N note верноназываетzone17западнеезаданного78–72W;онапокрывает84–78W. Этоoff-by-oneвсчёте,неошибкаединицы.',
'Esri documentedCreateWgs84UtmFromLocationacceptsdecimaldegree longitude/latitudeandreturnsWGS84UTMreference. NoteдаётпроверяемыйдополнительныйспособполученияCRSизкоординат,не«согласноEsri»и неповтор18N. Названиесредстваобобщено,ноcapabilityисточникомподтверждена.',
'Для18S note правильноотделяетnegativewestlongitudeотsouthlatitude. SDKотдельныеlatitude/longitudeargumentsи51N/51Sпримеры;NOAALat/Longтожеобосновываютнаправления.',
'Esri StereographicUPSsectionnorth84/south80;noteточноприменяетпределык40N. ЭтообоснованиепротивUPS,непротивлюбыхградусныхкоординат.'], 'choices':[
'17Nневерно:75Wне84–78W;правдоподобныйoff-by-one.',
'18Nверно;noteобAPIcapability—самостоятельныйдополнительныйфакт,беззачётатребованияобиспользованииArcGISигроком.',
'18Sневерно:перепутанзападныйзнакдолготысюжнымполушарием;plausibleaxis/signconfusion.',
'UPSневерно:40Nнеполярнаяобласть;единицаградуснеопределяетвыборUPS.'], 'peers':'stereographic-conformalCURRENTупоминаетточнуюполярнуюпараллель81°06′52,3″ипараметры,нонеzone18. grid-squareOSдругаясетка/адрес1945. Latitude/longitudepeersнерассчитываютUTMzone. ИхHOLDстатуснепревращаетCURRENTвнепрочитанныйтекст.', 'defects':[]},
'elevation-vertical':{'status':'HOLD','sources':[11]*6,'level':'HARD по абсолютной необходимой подготовке: prompt не даёт связь h=H+N, но требует вспомнить её знак/значение N и одновременно знать специфическое отношение американского NAVD88 к idealglobalgeoid. Простота вычитания не делает эти две непредоставленные геодезические предпосылки MEDIUM общего тематического каталога.', 'grounds':[
'NOAA diagramheights.gifличноосмотрен:h=H+N,поэтомуH=34,7−(−18,2)=52,9. VDatumGEOIDtextсвязываетмоделиN,NAD83иNAVD88. NAVD88sectionотличаетреализациюотidealglobalgeoid. Индекс1фактическиодин,ноfrozenMEDIUMневыдержан.',
'52,9мверно;promptоговариваетсовместимуюNAD83реализациюиприменимуюмодель,устранивнеопределённыйWGS84/geoidconversioninitial. NAVD88действительнонетождественidealglobalgeoid.',
'Для16,5иidentitynoteверноуказываетзнаковыйNифактнетождества;16,5=34,7+(−18,2),а неH=h−N.',
'NOAA NAVD88paragraph:adoptedelevationPointRimouski;Helmertorthometricapproximation. Note1—дваполезныхновыхфакта,неповторkey/attribution,русскийязыкпоправлен.',
'Для−52,9noteверноалгебраическивыводитH=h−NиэффектвычитанияnegativeN.',
'ДляH=hnoteверно:горизонтальнаякорректностьнеустраняетgeoidheightN. SourceVerticalDatum/GEOIDотделяетellipsoidalиorthometric.'], 'choices':[
'16,5неверно:неверныйзнакоперациииплюсfalseNAVD=idealgeoid;правдоподобнаягеодезическаямисконцепция.',
'52,9верноиdatumpropertyверна;одинключ. Noteсодержательноновая,нонеоблегчаетпредварительнонеизвестныеh/H/Nдляmedium.',
'−52,9неверно:взятоN−h;plausibleorderreversal.',
'34,7неверно:приN=−18,2ellipsoidalиorthometricнеравны;plausiblehorizontalaccuracy/verticaldatumconfusion.'], 'peers':'Критическийactualpeer,не включённыйавторомвчастьсписков:ellipsoidCURRENTsource46такжепроситH=h−NдляNAVD88ипрямопечатаетформулувcorrectanswer. Qвнёмдаёт52,9(случайнотожеtargetanswer). Это существенныйcross-cardдубльсемействаоперации,а некакбудтотерминнаястараякарта. НовыйdatumCURRENTотделяетгеоидальнуювертикальнуюосновуотгоризонтальногоприведения;benchmarkCURRENT—другаязадачаповторногонивелирования. Старые/новыеproposedтекстырассмотрены,terminalHOLD5неотменяетреальныеподсказкивCURRENT.', 'defects':[{'field':'difficulty/prompt','kind':'absoluteDifficulty','defect':'Связьh,H,NиразличиеNAVD88/idealglobalgeoidнепереданывусловии;нужныспециализированныегеодезическиезнания. Этоhardпоабсолютнойподготовке,аfrozenlevelmedium.','needed':'Новый источник не нужен: факты и арифметика подтверждены. Координатор сохраняет terminal HOLD этой точной версии и фиксирует отдельное scoped disposition medium-содержания без смены frozen difficulty; использованный цикл не повторять автоматически.'},{'field':'crossCard/actual maps-cartography-ellipsoid','kind':'semanticDuplicationAndCue','defect':'Обе CURRENT задачи используютNAVD88,H=h−N,арифметикуh/Nиодинcorrectindex1;actualellipsoidпрямораскрываетформулусоседнейзадачи. ДополнительныйNAVD/idealpropertyразличаетчастьсодержания,нонеустраняетдубльчисленногоскилла. АвторскийpeerнаборнеучёлновуюсложнуюCURRENTellipsoidполностью.','needed':'Координатор adjudicates точный semantic overlap по двум сохранённым CURRENT, а не по старому определению эллипсоида; не считатьterminalHOLDpeerотсутствующим.'}]}
}
entries=[]
for id in REQ['scopeIds']:
 q=C[id];j=J[id.removeprefix('maps-cartography-')];expected=AM['currentCardSHA256'] if id==AM['id'] else AP[id]['afterHash'];assert sha(q)==expected,(id,sha(q),expected);assert q==NOW[id]
 gs=[('prompt_ordered_answers_key',{'prompt':q['prompt'],'answers':[a['text'] for a in q['answers']],'correctIndex':q['correctIndex']}),('explanation',q['explanation'])]+[(f'note{i}',a['note']) for i,a in enumerate(q['answers'])]
 gproof=[]
 for n,(name,literal) in enumerate(gs):
  source=IP[j['sources'][n]];gproof.append({'group':name,'literal':literal,'canonicalSHA256':sha(literal),'independentPrimaryGround':j['grounds'][n],'primaryURL':source['url'],'fullContextPath':str((R/source['independentReadContext']).resolve()),'fullContextSHA256':source['contextSHA256'],'rawPrimaryFiles':source['rawFiles'],'exactReadLocators':source['exactLocators'],'authorLiteralMatchesFinal':literal==AUTHOR[id]['groups'][n]['literal'],'authorSpecificLocator':AUTHOR[id]['groups'][n]['source']['exactlocator']})
 extra={'maps-cartography-elevation-vertical':['maps-cartography-ellipsoid','maps-cartography-gnss-positioning'],'maps-cartography-isoline-value':['maps-cartography-raster-cells'],'maps-cartography-utm-zones':['maps-cartography-stereographic-conformal']}.get(id,[])
 peerids=sorted(set([x['id'] for x in PEERS if x['forTarget']==id]+extra))
 entries.append({'id':id,'cycle':1,'terminal':j['status']=='HOLD','status':j['status'],'currentCard':q,'currentCardSHA256':sha(q),'frozen':{'topicId':'maps-cartography','sourceOrder':ORD[id],'baselineSourceOrder':BASEORD[id],'orderPreserved':ORD[id]==BASEORD[id],'difficulty':q['difficulty'],'correctIndex':q['correctIndex'],'idDifficultyKeyPreserved':all(q[k]==PRE[id]['beforeCard'][k] for k in ['id','difficulty','correctIndex']),'beforeSHA256':PRE[id].get('beforeHash',sha(PRE[id]['beforeCard']))},'absoluteLevelAssessment':j['level'],'sixLiteralGroups':gproof,'fourVariants':[{'index':n,'fullPrompt':q['prompt'],'answerText':a['text'],'noteText':a['note'],'correctIndex':q['correctIndex'],'isKey':n==q['correctIndex'],'independentGrammarTruthOneKeyPlausibility':j['choices'][n],'ownNoteGroundUsefulness':j['grounds'][n+2],'answerPrimaryURL':IP[j['sources'][0]]['url'],'notePrimaryURL':IP[j['sources'][n+2]]['url']} for n,a in enumerate(q['answers'])],'actualRelevantPeers':[{'id':i,'currentCardSHA256':sha(C[i]),'snapshot':'evidence-cycle1/actual-peers.json#'+i} for i in peerids],'bothAuthorPeerVersions':'evidence-cycle1/author-peer-snapshots.json','additionalAlreadyExistingProposedNeighbors':'evidence-cycle1/neighbor61-70-proposed-relevant.json','independentCrossCardAssessment':j['peers'],'defects':j['defects'],'qualityCredit':0})
# Verify author cited paths independently; raw sources in initial read index are linked and hashed too.
checks={}
for e in AUTHOR.values():
 for g in e['groups']:
  s=g['source'];fp=R/s['primarypath'];checks[str(fp)]={'path':str(fp),'expected':s['fileSHA256'],'actual':hashlib.sha256(fp.read_bytes()).hexdigest()}
for s in IP:
 for raw in s['rawFiles']:
  fp=pathlib.Path(raw['path']);checks[str(fp)]={'path':str(fp),'expected':raw['sha256'],'actual':hashlib.sha256(fp.read_bytes()).hexdigest()}
img=B/'independent-hard5-initial-01a13d50/evidence-cycle1/noaa-heights.gif';imgsha=hashlib.sha256(img.read_bytes()).hexdigest();checks[str(img)]={'path':str(img),'expected':imgsha,'actual':imgsha,'personallyViewed':True,'url':'https://vdatum.noaa.gov/images/docs/heights.gif','locator':'entirediagram; topformula h=H+N, bottomdefinitions h,N,H'}
for c in checks.values():c['matches']=c['expected']==c['actual']
dump(E/'source-verification.json',{'sources':list(checks.values()),'mismatches':sum(not c['matches'] for c in checks.values()),'formulaDiagram':str(img),'formulaDiagramSHA256':imgsha})
# Make readers aware of accurate current source lines rather than silently trusting old author locator ranges.
dump(E/'primary-read-index.json',{'completeContexts':IP,'formulaDiagram':{'path':str(img),'sha256':imgsha,'personallyViewed':'Full diagram: h=H+N, h/N measured along ellipsoid normal, H along plumb line. Raw parent page references ../images/docs/heights.gif.'},'correctedPreciseLocators':{'USGS':'primary-00 lines71–86; p3 PNG upper-left Control Data/VerticalControl; spot elevation and recoverable/no-tablet signs','GraduatedColors':'primary-01 lines11–21 and normalization80–88; author normalization52–58 is imprecise','DotDensity':'primary-04 lines102–125: placement112–119, equal-area120–123','Contouring':'primary-05 lines12–13,25–30','Flow':'primary-06 complete abstract paragraphs under Abstract.','Latitude':'primary-07 complete defining/111km paragraphs and Degrees of Accuracy','Longitude':'primary-08 lines60–72: angularbasis/spacing/local-noonexample; author spacing40–44 misses actualspacingline68','UTM':'primary-09 complete method Parameters/ReturnValue/Remarks, not merely37–41','VDatum':'primary-11 lines122–132 geoid/N;151–158verticaltypes;191–192NAVD88, plus personallyvieweddiagram; author121–127doesnotitselfshowtheequation'}})
head=subprocess.check_output(['git','rev-parse','HEAD']).decode().strip();branch=subprocess.check_output(['git','branch','--show-current']).decode().strip();counts={s:sum(e['status']==s for e in entries) for s in ['PASS','FIX','HOLD']};receipt={'schemaVersion':1,'stage':'FINAL CURRENT9 independent cycle1 complete; no certification or quality credit','scope':REQ['scopeIds'],'cycle':1,'substantiveCyclesRemaining':0,'qualityCredit':0,'counts':counts,'snapshotBranch':branch,'snapshotHead':head,'requestedBaseline':'16ae42e5028c1110e95f8795079f5ce4b27588b5','fixRequestBaseline':REQ['baselineCommit'],'finalContentCommits':['8fb6df2e7e06283b27ad92a1ba04bfcc1acff61f','ba5af0570b5e130452e449b9a7f2a4a1dc1f16cd','ea4b8d96c8edc94b01c918e002731a988bff3cd2'],'method':'Personally read CURRENT9 in full, six literal groups, each actual fullprompt+answer+note, relevant complete preserved primary contexts and NOAA heights diagram, actual peers including current hard5 after84b89615 and partial-sourceHOLD language2, both author peer versions and already present relevant maps61–70 proposals. Initial verdicts and author PASS were not inherited. Peer HOLD is never treated as absent.','canonicalization':'SHA256 UTF8 JSON ensure_ascii=false sort_keys=true separators=(comma,colon)','entries':entries,'checks':{'currentCards':len(entries),'literalGroups':sum(len(e['sixLiteralGroups']) for e in entries),'fullPromptVariants':sum(len(e['fourVariants']) for e in entries),'allFinalCardHashesBound':all(e['currentCardSHA256']==(AM['currentCardSHA256'] if e['id']==AM['id'] else AP[e['id']]['afterHash']) for e in entries),'allFrozen':all(e['frozen']['orderPreserved'] and e['frozen']['idDifficultyKeyPreserved'] for e in entries),'noCurrentDrift':all(C[i]==NOW[i] for i in REQ['scopeIds']),'allPeerSnapshotNoDrift':all(ACT[i]==NOW[i] for i in ACT),'actualPeerSnapshotCount':len(ACT),'sourceHashPairs':len(checks),'sourceHashMismatches':sum(not c['matches'] for c in checks.values())},'sourceAndPeerLimits':'No unavailable primary claim left; evidence is existing saved material, not new fetch. Maps61–70 proposals were read only where already present and relevant (vector/raster/GNSS), never assumed applied. Some author source line ranges are inaccurate; independent precise locators are in evidence-cycle1/primary-read-index.json. Foreign hard5 dispositions remain terminal HOLD5; reader does not certify or edit them.','oldReceiptsUnchanged':True,'notRun':['runtime','tests','build','fullQA','audio'],'qaBoundary':'Supplied final19/19 QA is not an editorial truth/difficulty certificate and was not rerun. Reader executes no runtime or test commands.','preservation':{'ownOutputs':['receipt-cycle1-current9.json','evidence-cycle1/'],'coordinatorMustCommit':True,'readerCommitForbidden':True,'ownRuntimeProcesses':0,'claimsTouched':False,'oldReceiptTouched':False,'catalogTouched':False},'next':'Coordinator adjudicates PASS7/HOLD2 against exact hashes and saves this new evidence. Keep unresolved exact cards terminal HOLD after cycle1; no automatic further substantive rewrite cycle. Latitude needs only a concrete mechanical grammar disposition; elevation needs scoped medium/overlap disposition, no source hunt or human policy invented.'}
dump(O/'receipt-cycle1-current9.json',receipt);print(json.dumps({'counts':counts,'checks':receipt['checks'],'receiptSHA256':hashlib.sha256((O/'receipt-cycle1-current9.json').read_bytes()).hexdigest()},ensure_ascii=False,indent=2))
