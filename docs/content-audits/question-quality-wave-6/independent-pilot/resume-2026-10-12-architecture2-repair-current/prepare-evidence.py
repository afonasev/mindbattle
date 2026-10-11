import json, hashlib, subprocess, os
from pathlib import Path
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parents[5]
OUT=Path(__file__).resolve().parent
FROZEN='d8b64c1'
IDENTITY=os.environ['CODEX_THREAD_ID']
AUTHOR=ROOT/'docs/content-audits/question-quality-wave-6/architecture/resume-2026-10-12-rework21/author-receipt.json'
def sha(b):return hashlib.sha256(b).hexdigest()
def canonical(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def blob(p):return subprocess.check_output(['git','show',FROZEN+':'+str(p.relative_to(ROOT))],cwd=ROOT)
def write(n,d): (OUT/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
class Text(HTMLParser):
 def __init__(self):super().__init__();self.skip=0;self.out=[]
 def handle_starttag(self,t,a):
  if t in ['script','style','svg']:self.skip+=1
 def handle_endtag(self,t):
  if t in ['script','style','svg']:self.skip-=1
 def handle_data(self,d):
  if not self.skip and d.strip():self.out.append(d.strip())
a=json.loads(blob(AUTHOR));ids=['architecture-sydney-opera-house-country','architecture-summer-palace']
orig=json.loads(blob(ROOT/'src/content/topics/architecture.json'))['questions']
current=json.loads((ROOT/'src/content/topics/architecture.json').read_text())['questions']
analyses={
ids[0]:[
'Полная Description связывает датского архитектора Jørn Utzon с проектом Sydney Opera House и международным жюри 1957 года; Justification отдельно относит исходную концепцию к Утзону. Ключ 1 верен, остальные три архитектора не названы авторами этого проекта.',
'Полное описание серийного объекта Райта прямо перечисляет Fallingwater (Mill Run, Pennsylvania) и Guggenheim Museum (New York) среди восьми зданий в США. Каждое утверждение справки поддержано; это самостоятельные примеры работ выбранного автора.',
'Полная Description говорит о Danish architect Jørn Utzon и присуждении ему проекта международным жюри в 1957 году. Дата и процедура добавляют полезный факт к простому вопросу об авторстве; совпадение с explanation допустимо.',
'Полная Description называет градостроителя Lucio Costa и архитектора Oscar Niemeyer, согласование всех элементов с общим замыслом; Justification различает Plano Piloto Косты и architectural creations Нимейера. Справка точно описывает сотрудничество без приписывания Нимейеру всего градостроительного плана.',
'Полный первый раздел институциональной хронологии говорит об объединении Гропиусом Weimar School of Fine Arts и School of Arts and Crafts для основания Staatliches Bauhaus в 1919 году. Справка точно передаёт обе школы, место, автора и год.',
'Полная Description поддерживает датское происхождение, авторство, жюри и 1957 год; её начало и конец вместе поддерживают новизну формы и construction. Два предложения дают ответ и полезный контекст без превращения даты в условие вопроса.'
],
ids[1]:[
'Полные Description и Justification однозначно определяют Summer Palace in Beijing как Chinese landscape garden design. Ключ 3 точен; вопрос спрашивает культурную традицию ансамбля, не одну из встречающихся во многих странах деталей.',
'Полная Justification Версаля называет французскую садовую типологию Le Nôtre, axial pathways, low hedges, flower beds, streams, lakes and fountains. Все компоненты справки подтверждены; «партеры» здесь соответствует оформленным цветочным участкам французского сада, без ложного обобщения о любом французском саде.',
'Полная Description персидского сада говорит four sectors и важности воды для irrigation and ornamentation. Справка осторожно говорит «традиционно»; оба её утверждения прямо поддержаны и имеют самостоятельную ценность.',
'Полная Description Киото связывает культурный центр Японии с развитием Japanese gardens и влиянием на landscape gardening the world over; Justification Criterion (ii) уточняет роль центра развития. Справка относится к японскому садовому искусству без приписывания всем японским садам единственной формы.',
'Полная Description называет китайское landscape garden design и естественные hills/open water, объединённые с pavilions, halls, palaces, temples, bridges. Справка добавляет конкретный принцип композиции и её элементы сверх названия правильной традиции; повтор в explanation сам по себе не дефект.',
'Все три предложения поддержаны полной Description: Chinese landscape garden design; сочетание природного ландшафта с перечисленными постройками; harmonious ensemble. Объяснение соблюдает 2–4 предложения, содержит причину ответа и раскрывает композиционный принцип.'
]}
editorial={ids[0]: 'PASS. Основной факт — авторство всемирно известного памятника современной архитектуры — относится к общекультурному знанию большой культурной группы, интересующейся искусством, путешествиями и мировой архитектурой; профессиональная инженерная деталь не требуется. Это редакторская калибровка, не измерение доли знающих имя. Все четыре варианта — реальные известные архитекторы XX века, без грамматической или абсурдной подсказки. Нельзя получить ключ по повтору имени в условии. Справка Утзона сообщает датское происхождение, процедуру выбора и год сверх prompt/key; она вправе пересекаться с объяснением. Редкая дата 1957 находится после раскрытия, а не является проверяемым easy-фактом. Оснований HOLD по действующей рубрике не найдено.',ids[1]: 'PASS. Определение китайской садовой традиции известного пекинского императорского ансамбля доступно взрослой культурной аудитории; географический контекст помогает содержательной культурной логике и не является терминологической ловушкой. Четыре варианта — реальные садовые традиции, которые нельзя отвергнуть как абсурдные или грамматически несогласованные. Местонахождение сада не исключает само по себе влияние других традиций. Notes сообщают особенности/примеры каждой традиции, правильная note раскрывает природно-архитектурную композицию сверх prompt/key. Полезный факт не обязан отсутствовать в explanation. Три предложения объяснения исправляют прежний дефект длины.'}
sources={};cards=[]
for id in ids:
 ac=next(c for c in a['cards'] if c['questionId']==id);card=next(c for c in orig if c['id']==id)
 assert card==ac['currentCard']==next(c for c in current if c['id']==id)
 fields=[]
 for i,af in enumerate(ac['fields']):
  name=af['field'];literal=json.dumps([card['prompt'],card['correctIndex'],card['answers'][card['correctIndex']]['text']],ensure_ascii=False,separators=(',',':')) if name=='prompt-key' else card['explanation'] if name=='explanation' else card['answers'][int(name[-1])]['note']
  assert literal==af['literal']; proofs=[]
  for ap in af['proofs']:
   path=(AUTHOR.parent/ap['rawCapture']).resolve();raw=blob(path);assert raw==path.read_bytes();assert sha(raw)==ap['rawCaptureSha256']
   name2=path.name;dest=OUT/'sources'/name2;dest.write_bytes(raw)
   http=path.with_name(path.name+'.http.json')
   provenance=json.loads(blob(http)) if http.exists() else {}
   if path.suffix=='.json':
    record=json.loads(raw)['results'][0];key='justification_en' if id==ids[1] and name=='note0' else 'description_en';passage=record[key]
    if key=='justification_en':
     start=passage.index('The gardens that complete the Palace');end=passage.index(' Criterion (i):',start);passage=passage[start:end]
    rawlit=json.dumps(passage,ensure_ascii=True)[1:-1];assert rawlit.encode() in raw
    locator='results[0].'+key;quoteformat='Decoded complete description, or complete gardens paragraph; raw JSON string literal also bound without changing bytes'
   else:
    t=Text();t.feed(raw.decode());visible=' '.join(t.out);start=visible.index('Walter Gropius united');end=visible.index(' 1925–1932:',start);passage=visible[start:end];rawlit=None
    locator='1919–1925: State Bauhaus Weimar; complete founding/closure text';quoteformat='HTML visible text; scripts/styles/SVG omitted, whitespace joined; complete section read in original'
   rel=str(path.relative_to(ROOT));sources[rel]={'originalPath':rel,'frozenRevision':FROZEN,'originalGitBlob':subprocess.check_output(['git','rev-parse',FROZEN+':'+rel],cwd=ROOT,text=True).strip(),'rawCapture':'sources/'+name2,'rawCaptureSha256':sha(raw),'bytes':len(raw),'originalAndWorktreeEqual':True,'captureUrl':provenance.get('url',ap['url']),'captureFormat':ap['captureFormat'],'sourceClass':ap['sourceClass'],'sourceUrl':ap['url'],'readScope':'Full English original description and justification in UNESCO record; full visible original chronology for Bauhaus. All relevant complete passages read by this reader, not author verdict adoption.'}
   proofs.append({**sources[rel],'locator':locator,'passage':passage,'passageSha256':sha(passage.encode()),'rawQuotedLiteral':rawlit,'rawQuotedLiteralSha256':sha(rawlit.encode()) if rawlit else None,'quoteFormat':quoteformat,'readerIdentity':IDENTITY,'manualIndividualRead':True})
  fields.append({'field':name,'literal':literal,'literalSha256':sha(literal.encode()),'sourceVerdict':'PASS','editorialVerdict':'PASS','manualIndividualAnalysis':analyses[id][i],'readerIdentity':IDENTITY,'proofs':proofs})
 cards.append({'questionId':id,'cardCanonicalSha256':sha(canonical(card).encode()),'currentCard':card,'sourceVerdict':'PASS','editorialVerdict':'PASS','difficultyAnalysis':editorial[id],'fields':fields})
rule=next(l[2:] for l in Path('/Users/eaafonasev/Projects/mindbattle-planning/docs/GAME_SPEC.md').read_text().splitlines() if l.startswith('- Easy-вопрос проверяет'))
write('independent-receipt.json',{'role':'distinct independent source/editorial reader','agentIdentity':IDENTITY,'authorIdentity':a['agentIdentity'],'readDate':'2026-10-12','frozenContentRevision':'3cc178a','frozenAuthorAndSourceRevision':FROZEN,'authorReceiptSha256':sha(blob(AUTHOR)),'priorReviewCommits':['fcb61a7','3bf99b0'],'approvedDifficultyRule':rule,'rulePath':'/Users/eaafonasev/Projects/mindbattle-planning/docs/GAME_SPEC.md','counts':{'cards':2,'fields':12,'sourcePASS':12,'sourceFIX':0,'sourceHOLD':0,'editorialPASSCards':2,'editorialFIXCards':0,'editorialHOLDCards':0,'editorialPASSFields':12},'cards':cards,'limits':'Only these two current cards reviewed. Other98 including three already certified pilot cards not reread; remaining16 not prepared here. No human acceptance, root certification, fullsuite, build, deploy, merge, push, archive, content/planning/claim edits.'})
write('source-readback.json',{'readerIdentity':IDENTITY,'sources':list(sources.values()),'sourceCount':len(sources),'manualReadIsNotProvedByScript':'Script binds original bytes and quotes after the reader substantive read; this file does not substitute for manual individual analysis.'})
write('current-cards.json',[c['currentCard'] for c in cards])
write('scope-preservation.json',{'reviewedIds':ids,'currentEqualsFrozen':True,'contentEdited':False,'idOrderDifficultyKeyUnchanged':True,'other98Edited':False,'remaining16Edited':False,'historicalHoldsAndSourceAttemptsPreserved':True,'sourceFrozenRevision':FROZEN,'baselineQuotas':'40/40/20, key slots10/10/5 preserved because no content edits','readerIdentity':IDENTITY})
(OUT/'.gitattributes').write_text('sources/* -text\n')
write('qa-scope.json',{'scope':'evidence only; two current cards and 12 field bindings','selectedChecks':['python3 prepare-evidence.py: freeze equality, canonical/literal SHA, full raw SHA and raw JSON quote membership','python3 verify-evidence.py: Git committed raw/source roundtrip and scope','git diff --cached --check -- selected evidence'], 'reason':'No runtime/content edits; evidence bindings and preservation are affected contracts. No fullsuite or build required/authorized.'})
print(json.dumps({'identity':IDENTITY,'cards':len(cards),'fields':sum(len(c['fields']) for c in cards),'sources':len(sources)}))
