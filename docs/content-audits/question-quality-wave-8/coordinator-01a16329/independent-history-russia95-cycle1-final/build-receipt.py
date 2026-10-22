import json,hashlib,re
from pathlib import Path
C=Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle');D=C/'docs/content-audits/question-quality-wave-8/coordinator-01a16329';N='01a164f5-4b8d-7761-a3f7-0ec75266cb95'
def rd(p):return json.loads(Path(p).read_text())
def raw(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def sha(v):return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
T=rd(D/'reader-history-russia95-cycle1-final-task.json');O=Path(T['outputDirectory']);I=Path(T['previousIndependentInitial']).parent;q=rd(C/'src/content/topics/history-russia.json')['questions'][94];assert sha(q)==T['cardHash'] and q['difficulty']=='hard' and q['correctIndex']==2
S=rd(Path(T['authorPacket'])/'sourceproof.json')['rawSources'];exact=['turn2view0 L44-L51; main L51 / note0 L48 / note2 L51 / note3 L45','turn3view0 L44-L46'];loc=[{'path':z['path'],'url':z['url'],'completeOutputPointer':z['completeOutputPointer'],'locator':exact[i]} for i,z in enumerate(S)]
def refs(*ns):return [loc[i] for i in ns]
def ptr(file,pointer):return {'path':str((I/file).relative_to(C)),'rawSHA256':raw(I/file),'jsonPointer':pointer,'readerNativeId':N}
defect={'code':'CORRECT_NOTE_OTHER_ORGAN_NO_OWN_EXTRA_FACT','field':'answers[2].note / correctNoteExtraFact','severity':'substantive own-option usefulness','literal':q['answers'][2]['note'],'ground':'Правильныйответ — шестьгласныхвпостояннодействующейобщейградскойдуме. Noteрассказывает о другоморгане:собрании«градскогообщества»,еготрёхлетнейпериодичностииимущественномсоставе. L51источникаподтверждаетэтососеднеесведение,норазделяетсобраниеи постояннуюдуму;самаexplanationтожеявноназываетсобраниеотдельныморганом. Noteненазываетни6,нигласных,ниихдуму,неназываетихполномочия/представительство/назначениеит.п. Поэтомуистинныйобщийфактизтойжеграмоты незаменяетконкретныйдополнительныйфактобответе6гласных/ихоргане. Это не требование непременно повторитьцифру, а требованиесодержательнойсвязи с объектомправильногоответа.','sourcesLocators':refs(0),'terminal':True,'nextAction':'TerminalHOLD0послеединственногообычногоcycle1. Не исправлять,не создаватьcycle2/новыйINITIAL/reset; дальнейшеепереоткрытиетолькопоотдельнойавторизацииисохраняющимсяfences.'}
gs={'prompt_ordered_answers_key':{'prompt':q['prompt'],'answers':[a['text'] for a in q['answers']],'correctIndex':q['correctIndex']},'explanation':q['explanation'],**{'note'+str(i):a['note'] for i,a in enumerate(q['answers'])}}
grounds={
'prompt_ordered_answers_key':('Directedrepairдостаточендлясамоговопроса:личнопрочитанныйL51называетпостоянныйорган«общаяградскаядума»исоставгородскойголова+6гласных;promptисключаетголову,потому7невторойключ.14естьчислоразделовгородскойграмотыL48,92статейдворянскойL45,7первыйсоставдругогоСоветаL46. Всеlabelтеперьчислаоднойкатегории;исчезлаподсказка«города→городам». HARDтребуетзнанияконкретногосоставаоргана,анеобеспечиваетсяпростоцифрами.',refs(0,1)),
'explanation':('L51точноуказываетголовуишестьгласныхвсоставепостояннойдумыиотдельнособраниеградскогообществаразвтригода. Первое предложение«руководили»читаетихкакгородскойоргануправления,соответствуяописаниюучреждения/L50–51;непредъявляетновуюиндивидуальнуюдолжностькаждого. Второепредложениекорректноразличаеторганы. Двапредложения,ключшестьпрямоназван.',refs(0)),
'note0':('L48городскаяграмотасостоялаиз14разделов. Noteсодержитпроверенныйсобственныйисторическийфактозначениичисла14вструктуретого жеакта;неназывает14гласных.',refs(0)),
'note1':('Советturn3view0L46прямодаётпервыйсоставиз7человекиперечисляетих. NoteясноуказываетдругойСовет,неприписываясемьместгласным. Этофактчисла7висторическомуправленческомконтексте.',refs(1)),
'note2':(defect['ground'],refs(0)),
'note3':('Грамотыturn2view0L45прямодаётдворянскуюграмоту,4раздела/92статьи. Noteточносоотноситчисло92сдругимпараллельнымактом,нечисломгородскихгласных. Самостоятельныйподтверждённыйфактдистрактора.',refs(0))}
groups=[{'group':g,'literal':z,'canonicalSHA256':sha(z),'individualGround':grounds[g][0],'sourcesLocators':grounds[g][1]} for g,z in gs.items()]
plaus=[
'14можнопринятьзачисленностьболееширокогопредставительногоорганаилиспутатьсчисломразделовтойжеграмоты. Это не заведомоневозможнаячисленность, хотяспециалистразличиттипколичества.',
'7—особенноправдоподобныйсоседнийответ:6гласных+головадают7членоввсего. Prompt«помимоголовы»требуетнеподменитьчислогласныхобщимсоставом;этонеарифметическаязадачаизданныхprompt,посколькусамосновноечислоне дано.',
'6невыделеноединицамиилилексикой;длявыборанадознатьузкуюинституциональнуюдетальлибоосмысленноразличитьеёссоседнимичислами,известнымиизисторическогоконтекста.',
'92—болеелегкоисключаемыйкрупныйчисловойдистрактор,взятыйиздругойграмоты. ОдинболееслабыйотсевсампосебенеотменяетHARDоставшегосяразличения6/7/14;нооднопроисхождениечислаизисточникаещёнеделаетегоключом.']
truth=[
'Неверно:городскаяграмотаL48имеет14разделов,носоставорганаL51прямошестьгласныхпомимоголовы.',
'Неверно:7можетбытьобщейсуммойголовы+6,нопомимоголовыгласных6. Вдругомпрочитанномконтексте7действительночислопервогоСоветаL46.',
'ЕдинственныйистинныйключподословномупрочитанномуL51:городскойголоваишестьгласных;promptисключаетголову. Всеостальныеличиныразличнысшестью.',
'Неверно:92—статьидворянскойграмотыL45,невосемь/девяностодвагородскихгласных;L51даёт6.']
variants=[]
for i,a in enumerate(q['answers']):
 tr={'prompt':q['prompt'],'answer':a['text'],'note':a['note']};variants.append({'slot':i,**tr,'tripleCanonicalSHA256':sha(tr),'grammar':'«'+q['prompt']+'» — «'+a['text']+'»: число подходит как самостоятельный ответ на «сколько»; все labels оформлены одинаково. Русский текст note синтаксически корректен.','plausibility':plaus[i],'truthUniqueKey':truth[i],'noteTruthUsefulness':grounds['note'+str(i)][0],'sourcesLocators':refs(0,1) if i==1 else refs(0)})
e={'id':q['id'],'topicId':T['topicId'],'sourceOrder':95,'stage':'FINAL','cycle':1,'currentCard':q,'currentCardCanonicalSHA256':sha(q),'status':'HOLD','sixLiteralCanonicalGroups':groups,'fourFullPromptAnswerNoteVariants':variants,'absoluteLevel':{'frozen':'hard','result':'INITIALHARDdefectresolvedfortherevisedprompt/row','assessment':'Составконкретногопостоянногогородскогоорганапограмоте1785,сразличениемгласныхиголовы,—специфическоеинституциональноезнание,нешироковзрослоеузнавание. ЧисласамипосебенеHARD;здесьсущественнопомнитьсоставирольголовы.7—осмысленнаяподменаобщегосостава,14—числоструктурныхчастейакта;92легчеотсекается. Старойлексическойподсказкинет,поэтомупрежнийдефектсложностиснят. ИтогкарточкиHOLDиз-заcorrectnote,неиз-зачисловогоформата.'},'correctNoteExtraFact':{'status':'FAIL_OWN_OPTION_LINK','fact':'Периодичность/имущественныйсоставсобранияградскогообществаистинны,нонедаютновогофактошестигласных/ихпостояннойдуме.','sourcesLocators':refs(0)},'defects':[defect],'frozen':T['frozen'],'directedResolution':{'initialDefect':ptr('receipt.json','/entries/0/defects/0'),'result':'RESOLVED_FOR_MAIN_ROW','remainingIntroducedDependency':'answers[2].note other organ; terminalHOLD0, no secondcycle'},'previousIndependentInitial':ptr('receipt.json','/entries/0')}
r={'readerNativeId':N,'date':'2026-10-23','role':'independent','stage':'FINAL','catalogCommit':T['catalogCommit'],'qualityCredit':0,'entries':[e],'terminal':'HOLD0 sole ordinary cycle1 exhausted'}
sources=[]
for i,z in enumerate(S):
 assert raw(C/z['path'])==z['sha256'];body=rd(C/z['path'])
 for k in z['completeOutputPointer'].strip('/').split('/'):body=body[int(k)] if isinstance(body,list) else body[k]
 bs=hashlib.sha256(body.encode()).hexdigest();assert bs==z['completeOutputSHA256'];sources.append({'path':z['path'],'url':z['url'],'rawReadSHA256':raw(C/z['path']),'completeOutputPointer':z['completeOutputPointer'],'completeOutputSHA256':bs,'actualReturnedCharacters':len(body),'locator':exact[i],'personalReadEvidence':[
'Лично повторно прочитан весь original body7942символа,turn2view0L0–126. L45дворянскаяграмота4раздела/92статьи,L48городская14разделов,L50шестьгородскихразрядов,L51отдельнособрание3года/богатыегорожанеипостояннаядумаголова+6гласных. Sourceбуквальноподтверждаетключ;note2соседнийфактодругоморгане,дополнительнаясвязьсправильнымответомнеобнаружена.',
'Лично повторно прочитан весь original body8325символов,turn3view0L0–132. L44–46СоветЕкатериныI1726,первыйсоставиз7имён. Этооснованиеnote1,несодержательноеподтверждениекаких-либоheldстарыхкарт.'][i],'previousOwnFullRead':ptr('sources.json',f'/sources/{i}'),'limitations':'Толькоactualsavedreturnedbody;никакихnewfetch/retry/alternative. Авторскиеоценки/QAневзятыкакистина.'})
s={'readerNativeId':N,'sources':sources,'proceduralEvidence':rd(I/'sources.json')['proceduralEvidence'],'ownReadDeviation':ptr('reviewer-procedural-deviation.json',''),'fences':'Authorbootstrap/additionalreadscopeandrootwrongSTARTremainuncured;content/QAнеисправляетпроцедуру. Old43/44HOLDunchanged. НетnewINITIAL/cycle2/reset.','qualityCredit':0}
p=rd(I/'peers.json');by={}
for z in p['actualCurrentPeers']:
 actual=next(t for t in rd(C/f"src/content/topics/{z['topicId']}.json")['questions'] if t['id']==z['id'])
 if actual!=z['card']:assert z['id']==q['id']
 z.update(card=actual,canonicalSHA256=sha(actual),fileSHA256=raw(C/f"src/content/topics/{z['topicId']}.json"));by[z['id']]=z
extra=rd(C/'src/content/topics/history-russia.json')['questions'][73];assert extra['id']=='history-russia-supreme-privy-council';ex={'id':extra['id'],'topicId':'history-russia','sourceOrder':74,'card':extra,'canonicalSHA256':sha(extra),'sourcePath':'src/content/topics/history-russia.json','fileSHA256':raw(C/'src/content/topics/history-russia.json')};p['actualCurrentPeers'].append(ex);by[ex['id']]=ex
newmain={'entity':'гласные постоянной общей градской думы1785 помимо головы','relation':'имеют численность','value':'6','context':'городской орган/Жалованная грамота'}
prose={
'history-russia-sudebnik-1497':'95теперьспрашиваетчислогородскихгласных1785,31правителякодекса1497. ИзменившийсяMAINнеприближаеткИвануIII;разныеentity/relation/value/contextвобеихсторонах,обращениенет.',
'history-russia-charter-to-nobility':'Heldactual43неизменён:условиелишениядворянинаправсудомравныхвдворянскойграмоте. Новый95численностьпостояннойгородскойдумывгородскойграмоте. Общийгод/автор/rawнеобщаяосновнаясвязь. Ни6,нисудебноеусловие невзаимныеответы;HOLD43непереревьюен.',
'history-russia-military-settlements':'Heldactual44неизменён:военныепоселенияXIX→Аракчеев,95городскаядумаXVIII→6гласных. Нетсовпадающегоинститута/отношения/эпохи/ключавобеихсторонах;HOLD44непереоткрыт.',
'history-russia-zemstvo-reform':'45реформа1864→земства,95составпостояннойдумы1785→6. Однаобщаясфераместногосамоуправления,нодругиеорганы/год/отношение/значение;недирект/реверспара.',
'history-russia-church-council-1551':'Стоглавдистракторудалён.71названиецерковногосборника1551,95численностьгородскойдумы1785. Никакоевзаимноеперефразированиеилиобращениеобщейсвязиневозникает.',
'history-russia-anna-conditions':'Кондициидистракторудалён.75документограниченияАнны1730,95составгородскогооргана1785. Note75огородскойграмоте неосновнойвопрос75. КаждыйключнеответдругогоMAIN,прямогообращениянет.',
'history-russia-universal-conscription':'97актповинности1874,95числовойсоставдумы1785. Названиегородскойграмотытеперьдановprompt95,нонеспрашивается;новыйMAINещёявнееотличаетсяотактадругойреформы.',
'history-russia-supreme-privy-council':'Новыйрелевантныйpeer74личнопрочитанполностью:органЕкатериныI1726→Верховныйтайныйсовет.95числогласныхдумы1785→6;note95slot1содержит7первогосоставаСовета,ноэтонеMAIN95или74. Орган/год/отношение/значениевобеихсторонахразличны;обращениянет.'}
for i,pair in enumerate(p['bilateralMainComparisons']):
 for side in ['left','right']:
  z=pair[side];z['canonicalSHA256']=by[z['id']]['canonicalSHA256']
  if z['id']==q['id']:z['MAIN']=newmain;z['key']='6'
 pair['bilateralGround']=prose[pair['right']['id']];pair['previousOwnFullPeerRead']=ptr('peers.json',f'/bilateralMainComparisons/{i}');pair['directedApplicability']='Fullunchangedactualpeerbody/hashсверены,новаячисловаяосновнаясвязь95оцененавобоихнаправлениях. СтарыеHOLDнепринимаются.'
left={'id':q['id'],'canonicalSHA256':sha(q),'MAIN':newmain,'key':'6'};right={'id':extra['id'],'canonicalSHA256':sha(extra),'MAIN':{'entity':'высший совещательный орган1726','relation':'учреждён при ЕкатеринеI','value':'Верховныйтайныйсовет','context':'центральное управление'},'key':extra['answers'][extra['correctIndex']]['text']};p['bilateralMainComparisons'].append({'left':left,'right':right,'bilateralGround':prose[extra['id']],'directReverseCheck':'ПолныеCURRENTобеихсторонпрочитаны;численностьгородскихгласныхнеобращениеидентификациидругогоцентральногооргана.','result':'DISTINCT_MAIN'})
rows=[];bindings=[];hits=[];pattern=r'\bгласных\b|\bгласные\b|\bградск\w*|Жалованн|городск.{0,8}дум|городск.{0,10}самоуправ'
for f in sorted((C/'src/content/topics').glob('*.json')):
 qs=rd(f)['questions'];bindings.append({'path':str(f.relative_to(C)),'rawSHA256':raw(f),'questionCount':len(qs)})
 for z in qs:
  row={'topicId':f.stem,'id':z['id'],'prompt':z['prompt'],'answers':[a['text'] for a in z['answers']],'correctIndex':z['correctIndex']};rows.append(row)
  if re.search(pattern,row['prompt']+' '+' '.join(row['answers']),re.I):hits.append(row)
p['globalMAINRetrieval'].update(rowsCanonicalSHA256=sha(rows),fileBindings=bindings,query=pattern,hits=hits);p['directedRetrieval']='Первыйширокийsubstringretrievalдаллексическиеложныеhits/обрезался;затемсуженграницамислов,результатполностьюпрочитан. Лингвистическиегласныедругойсмысл,неинституциональныйповтор95. НовыйчисловойMAINнеимеетрелевантнойдублирующейсвязиввыявленныхpeers.'
qa=rd(T['qa']);assert raw(T['qa'])==T['qaSHA256'] and qa['success'] and qa['numPassedTests']==19 and qa['numFailedTests']==qa['numPendingTests']==0
fs=list(Path('/Users/eaafonasev/.codex/sessions/2026/10/22').glob('*-'+N+'.jsonl'));assert len(fs)==1;jr=[json.loads(l) for l in fs[0].open()];assert [z['payload']['id'] for z in jr if z.get('type')=='session_meta']==[N];comp=sum(z.get('type')=='compacted' for z in jr);assert comp<2
v={'readerNativeId':N,'stage':'FINAL','status':'HOLD','terminal':True,'catalogCommit':T['catalogCommit'],'catalogRawSHA256':raw(C/'src/content/topics/history-russia.json'),'currentCardCanonicalSHA256':sha(q),'existingQA19':{'path':str(Path(T['qa']).relative_to(C)),'rawSHA256':raw(T['qa']),'pass':19,'fail':0,'pending':0,'meaning':'Existingexactreporthash-bound,notreviewerQAorcontentproof.'},'nativeJournal':str(fs[0]),'session_meta':N,'actualCompactions':comp,'mechanicalChecks':{'sixGroups':6,'fourVariants':4,'sourceEntries':2,'actualPeers':len(by),'bilateralPairs':len(p['bilateralMainComparisons']),'frozenMatch':q['id']==T['frozen']['id'] and q['difficulty']==T['frozen']['difficulty']=='hard' and q['correctIndex']==T['frozen']['correctIndex']==2,'answerUTF16Lengths':[len(a['text'].encode('utf-16-le'))//2 for a in q['answers']],'noteWordCounts':[len(a['note'].split()) for a in q['answers']],'explanationWords':len(q['explanation'].split()),'explanationSentences':2},'proceduralComplianceClaimed':False,'sourceProceduralDeviation':rd(I/'verification.json')['originalSourceDeviation'],'ownReadDeviation':rd(I/'verification.json')['ownReadDeviation'],'notRun':['Git/binder','tests/runtime/browser/build/fullsuite','network/refetch/retry','human/deviceacceptance'],'integration':'Notassessed:Gitforbidden;catalogCommittaskbindingnotverifiedbranch/integration.','stop':'Solecycle1FINALterminalHOLD0;nocycle2/reset/newINITIAL;endrolework.'}
a=rd(T['applyReport'])
for g in groups:
 ag=next(z for z in a['finalGroupBindings'] if z['id']==q['id'] and z['group']==g['group']);assert g['literal']==ag['literal'] and g['canonicalSHA256']==ag['literalSHA256']
for t in variants:
 av=next(z for z in a['finalVariantBindings'] if z['id']==q['id'] and z['slot']==t['slot']);assert t['tripleCanonicalSHA256']==av['bindingCanonicalSHA256'] and all(t[k] for k in ['grammar','plausibility','truthUniqueKey','noteTruthUsefulness','sourcesLocators'])
for name,value in [('receipt.json',r),('sources.json',s),('peers.json',p),('verification.json',v)]:
 dest=O/name;assert dest.parent==O and not dest.exists();dest.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
for name in ['receipt.json','sources.json','peers.json','verification.json']:assert rd(O/name)
assert rd(C/'src/content/topics/history-russia.json')['questions'][94]==q and raw(C/'src/content/topics/history-russia.json')==v['catalogRawSHA256']
for z in p['actualCurrentPeers']:
 actual=next(t for t in rd(C/f"src/content/topics/{z['topicId']}.json")['questions'] if t['id']==z['id']);assert actual==z['card'] and sha(actual)==z['canonicalSHA256']
print(json.dumps({'status':'HOLD','terminal':True,'stage':'FINAL','cycle':1,'sourceOrder':95,'cardHash':sha(q),'initialHARDDefect':'resolved','remainingDefects':[defect['code']],'sixGroups':6,'fourVariants':4,'sourceEntries':2,'actualPeers':len(by),'bilateralPairs':len(p['bilateralMainComparisons']),'actualCompactions':comp,'qualityCredit':0,'outputDirectory':str(O),'filesSHA256':{name:raw(O/name) for name in ['receipt.json','sources.json','peers.json','verification.json']}},ensure_ascii=False))
