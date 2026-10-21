import json,hashlib,copy
from pathlib import Path
ROOT=Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle')
OUT=ROOT/'docs/content-audits/question-quality-wave-8/coordinator-01a15bcc/source-polar86'
UID='01a15bb6-f7ab-7b41-a966-d26e37a5094c'; OWNER='01a15bcc-bb59-7060-a1d6-48c9b65f7d18'
sha=lambda x:hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
load=lambda p:json.loads(Path(p).read_text())
inv=load(OUT/'fresh-inventory.json'); assert len(inv['globalMAIN']['rows'])==11000 and len(inv['sameTopicMAIN']['questions'])==100
before=next(q for q in inv['sameTopicMAIN']['questions'] if q['id']=='polar-regions-satellite-altimetry-height')
assert sha(before)=='7fe2a6ba6aa3dda288b5dfa38943eba082c757a978de6597949af83b14c07af3'
proposed=copy.deepcopy(before)

def groups(card):return {'prompt_ordered_answers_key':{'prompt':card['prompt'],'answers':[a['text'] for a in card['answers']],'correctIndex':card['correctIndex']},'explanation':card['explanation'],**{'note'+str(i):a['note'] for i,a in enumerate(card['answers'])}}
bg=groups(before);ag=groups(proposed)
field={k:{'beforeCanonicalSHA256':sha(bg[k]),'afterCanonicalSHA256':sha(ag[k])} for k in bg}
entry={'id':before['id'],'topicId':'polar-regions','sourceOrder':86,'status':'HOLD','beforeCard':before,'beforeHash':sha(before),'proposedCard':proposed,'afterHash':sha(proposed),'fieldGroups':field,'proposedCardCanonicalSHA256':sha(proposed),
 'holdReason':'No retained complete primary body for the assigned ICESat-2 source or official alternative; historical URL-check reachability records are not statement-level evidence and their referenced temporary body artifact is absent. No re-fetch was made because both URL paths already have recorded attempts. The correct note repeats the prompt rather than adding an own useful fact, and the direct answer cues may undercut frozen MEDIUM; no source-backed repair is possible in this bounded packet.'}
candidate={'owner':OWNER,'sourceNativeId':UID,'stage':'FRESH_PERSONAL_SOURCE86_HOLD','cycle':0,'qualityCredit':0,
 'scope':{'id':before['id'],'topicId':'polar-regions','sourceOrder':86,'frozen':{'id':before['id'],'topicId':'polar-regions','sourceOrder':86,'difficulty':'medium','correctIndex':0}},
 'history':{'preimage':'Fresh current inventory; exact full-card hash matches assigned SOURCE86 beforeHash. No previous author verdict inherited.','sourceBoundary':'The task sourceIndex and targeted raw/path/URL search yielded no complete retained body for either historical NASA URL. The historical source-url-check file points to /private/tmp/mindbattle-source-global-2026-09-04.json, which is absent. Prior primary and official-alternative attempts were not repeated; no edits are proposed without source evidence.'},'entries':[entry]}

url_check=ROOT/'docs/content-audits/source-url-check-2026-09-02.json'
url_data=load(url_check)
want=['https://icesat-2.gsfc.nasa.gov/science','https://science.nasa.gov/mission/icesat-2/']
records={}
def walk(x):
 if isinstance(x,dict):
  u=x.get('url')
  if u in want: records[u]=x
  for v in x.values():walk(v)
 elif isinstance(x,list):
  for v in x:walk(v)
walk(url_data)
assert all(u in records for u in want)
source_attempts=[]
for seq,(kind,u) in enumerate([('historical_primary',want[0]),('historical_official_alternative',want[1])],1):
 r=records[u]
 source_attempts.append({'sequence':seq,'kind':kind,'url':u,'historicalStatus':r.get('status'),'reachable':r.get('reachable'),'contentInspectable':r.get('contentInspectable'),'finalUrl':r.get('finalUrl'),'recordedIn':str(url_check),'evidenceArtifact':r.get('evidenceArtifact'),'evidenceArtifactExists':Path(r.get('evidenceArtifact','')).exists(),'outcome':'Historical URL check indicates reachability only; full primary body is not retained at the listed artifact. No retry or new fetch made.'})

literals=[]
for key in bg:
 value=ag[key]
 literals.append({'group':key,'literal':value,'literalSHA256':sha(value),
   'primaryGround':'HOLD — no personally readable complete primary context is retained for the assigned claim. Historical URL-check status and the card source metadata cannot ground this literal.',
   'sourcePaths':[],'locator':'Historical primary https://icesat-2.gsfc.nasa.gov/science and official alternative https://science.nasa.gov/mission/icesat-2/ were checked previously; no complete body artifact is available.'})

assess=[]
assess_text=[
 ('Промпт грамматически корректен, а ключевая пара «высота ледяной поверхности»/«спутниковая альтиметрия» понятна. Но терминологическая связь сама по себе не подтверждает физический смысл правильного метода, а буквальное совпадение с «из космоса» может сделать ответ угадываемым; полный первичный контекст отсутствует. Текущая заметка повторяет определение из вопроса, не добавляя отдельного факта. HOLD: уникальность ключа по замороженному MEDIUM и истинность заметки не сертифицированы.'),
 ('Формулировка ответа и заметки грамматически корректна. Ледяной керн выглядит тематически правдоподобным дистрактором, но это образец/операция отбора, а не непосредственно космическое измерение поверхности; источник для точной заметки в этом пакете не сохранился. HOLD: truth/usefulness по первичному контексту не подтверждены.'),
 ('Формулировка грамматически корректна, радиолокационное зондирование — тематически правдоподобный метод. В текущем тексте оно связано с толщиной льда и скрытым ложем, тогда как вопрос спрашивает изменение высоты поверхности; это различает предполагаемые значения, но источник для обоих конкретных утверждений не сохранён. HOLD: note truth и ключ по источнику не подтверждены.'),
 ('Формулировка грамматически корректна; спутниковая геодезия GPS — правдоподобная альтернатива для движения ледника. Заметка связывает GPS с изменением координат, но сохранённого полного первичного контекста нет. HOLD: источник не позволяет подтвердить точность заметки и абсолютную уникальность метода для данного промпта.')]
for i,a in enumerate(before['answers']):
 assess.append({'slot':i,'fullPrompt':before['prompt'],'answer':a['text'],'note':a['note'],'tripleSHA256':sha({'prompt':before['prompt'],'answer':a['text'],'note':a['note']}),'grammar':'Грамматика проверена непосредственно по полной русской формулировке промпта, варианта и заметки.',
  'plausibilityUniqueKeyAndNoteTruthUsefulness':assess_text[i],'sourcePaths':[],'locator':'No complete relevant primary source body retained; see sourceproof.sourceAttempts and sourceproof.limitations.'})
proof={'owner':OWNER,'sourceNativeId':UID,'stage':'FRESH_PERSONAL_SOURCE86_HOLD','cycle':0,'qualityCredit':0,'rawSources':[],
 'sourceIndex':'Task-designated retained source index and targeted raw/sourceproof/URL search were read. No complete full body for https://icesat-2.gsfc.nasa.gov/science or the historical official NASA alternative was found. The source-url-check record is only reachability metadata, and its referenced /private/tmp/mindbattle-source-global-2026-09-04.json artifact no longer exists. No source refetch was made.',
 'sourceAttempts':source_attempts,
 'entries':[{'id':before['id'],'status':'HOLD','beforeHash':sha(before),'literalGroups':literals,'fourFullPromptAnswerNoteAssessments':assess,
  'correctNoteNewFact':'HOLD: current correct note restates the prompt/key relation (“tracks change in ice-sheet surface height”) and supplies no separate useful own fact. A factual extension requires a retained complete primary context.',
  'absoluteDifficulty':'HOLD for frozen MEDIUM. As written, “height” plus “from space” points directly toward “satellite altimetry,” while the alternatives describe different activity classes (a physical core, radar sounding, GPS geodesy). This may reduce adult difficulty below MEDIUM; no answer-rate or test evidence is available and no source-backed rewrite is proposed.'}],
 'limitations':['No current candidate card changes are proposed; all six field groups have identical before/after hashes.','The assigned NASA primary URL and the official NASA alternative both have historical status-200 content-inspectable records, but no complete primary text survives; status/hash/URL metadata are not factual proof.','Source85 and other neighboring/fenced claims are not being reopened. No source fetch, retry, raw-copy, catalog apply, independent review, or quality credit is claimed.']}

# Full current peer inventories, exact-term global retrieval, and bilateral checks.
polar=inv['sameTopicMAIN']['questions']; pby={q['id']:(i,q) for i,q in enumerate(polar,1)}
ocean_path=ROOT/'src/content/topics/oceans-seas.json'; ocean=json.loads(ocean_path.read_text()); oceanqs=ocean['questions']
oby={q['id']:(i,q) for i,q in enumerate(oceanqs,1)}
selected=[('polar-regions','polar-regions-gamburtsev-buried'),('polar-regions','polar-regions-ice-core-past-atmosphere'),('polar-regions','polar-regions-gps-glacier-speed'),('oceans-seas','oceans-seas-satellite-altimetry')]
peerfacts={
'polar-regions-gamburtsev-buried':('Gamburtsev Mountains / East Antarctic ice sheet','subglacial-object identification and radar survey','Gamburtsev Mountains hidden near Dome A','polar subglacial geomorphology','Both mention radar-related cryosphere science, but peer identifies a buried mountain range and uses radar to study subsurface relief; candidate asks a method for changing surface height. Different entity/relation/value.','Knowing the buried mountain range does not identify the method that measures surface-height change; altimetry does not identify the hidden range.'),
'polar-regions-ice-core-past-atmosphere':('polar ice core','extraction operation and climate record','drilling extracts a core whose trapped air preserves past atmosphere','ice-core sampling','The shared option is “ice core”, but this peer asks how to extract a physical core and what its trapped air reveals; candidate asks a space-based surface-height method.','Knowing the satellite method does not say which operation extracts a core; drilling/ice-core facts do not identify surface altimetry.'),
'polar-regions-gps-glacier-speed':('point on glacier surface / GPS geodesy','direct surface motion measurement','repeat coordinates yield direction and speed of point displacement','glacier kinematics','The cards use the same four method choices and share their answer-note sentence for altimetry, but ask complementary measurements: height change (candidate) versus point velocity (peer). The relation/value changes and each answer does not solve the other.','Knowing GPS speed does not identify the method for height change, and knowing altimetry does not answer which field method directly measures point speed.'),
'oceans-seas-satellite-altimetry':('ocean surface / satellite altimeter','surface-height measurement from orbital range','sea-surface height from satellite orbit and radar round-trip time','ocean sea-level measurement','This is the closest global overlap: same method and surface-height measurement family, but this peer is ocean sea level and specifies radar range/orbit; candidate concerns change in ice-sheet surface elevation. Mark as high thematic overlap, not a fully duplicate entity/context.','The ocean sea-level relation alone does not answer the ice-surface-change question; the ice-sheet context does not give the peer’s ocean range/orbit relation. Both resolve to the same method, so a cross-topic redundancy risk remains.')}
closest=[];comparisons=[]
for topic,pid in selected:
 if topic=='polar-regions':order,q=pby[pid]; path=ROOT/'src/content/topics/polar-regions.json'; fhash=inv['sameTopicMAIN']['fileSHA256']
 else:order,q=oby[pid]; path=ocean_path; fhash=hashlib.sha256(path.read_bytes()).hexdigest()
 h=sha(q);closest.append({'id':pid,'topicId':topic,'sourceOrder':order,'card':q,'sha256':h})
 ent,rel,val,ctx,ctop,ptoc=peerfacts[pid]
 comparisons.append({'kind':'CURRENT_MAIN','peerId':pid,'peerFullCardSHA256':h,
  'candidateERVC':{'entity':'satellite altimetry','relation':'space-based measurement of surface-height change','value':'change in ice-sheet surface elevation','context':'polar glacier/ice-sheet monitoring'},
  'peerERVC':{'entity':ent,'relation':rel,'value':val,'context':ctx},'candidateToPeer':ctop,'peerToCandidate':ptoc,'isDuplicate':False})
actual=[{'id':q['id'],'topicId':'polar-regions','sourceOrder':i,'card':q,'sha256':sha(q)} for i,q in enumerate(polar,1)]
# Distinct exact-query hits, including sea-surface cards that carry the same method as an answer.
hit_specs=[('polar-regions','polar-regions-gps-glacier-speed')]+[('oceans-seas',x) for x in ['oceans-seas-multibeam-sonar','oceans-seas-side-scan-sonar','oceans-seas-satellite-altimetry','oceans-seas-seismic-reflection']]
hits=[]
for topic,pid in hit_specs:
 if topic=='polar-regions':order,q=pby[pid];path=ROOT/'src/content/topics/polar-regions.json';fhash=inv['sameTopicMAIN']['fileSHA256']
 else:order,q=oby[pid];path=ocean_path;fhash=hashlib.sha256(path.read_bytes()).hexdigest()
 hits.append({'topicId':topic,'sourceOrder':order,'id':pid,'card':q,'cardCanonicalSHA256':sha(q),'sourceFilePath':str(path),'sourceFileSHA256':fhash})
peer={'owner':OWNER,'sourceNativeId':UID,'stage':'FRESH_PERSONAL_SOURCE86_HOLD','cycle':0,'qualityCredit':0,
 'candidate':{'id':before['id'],'topicId':'polar-regions','sourceOrder':86,'beforeCard':before,'beforeCardCanonicalSHA256':sha(before),'proposedCard':proposed,'proposedCardCanonicalSHA256':sha(proposed),'frozen':{'id':before['id'],'topicId':'polar-regions','sourceOrder':86,'difficulty':'medium','correctIndex':0},'semanticEntity':'satellite altimetry','semanticRelation':'measurement of surface-height change from space','semanticValue':'ice-surface elevation change','semanticContext':'Antarctic ice-sheet monitoring'},
 'globalMAIN':{'topicFileCount':inv['globalMAIN']['topicFileCount'],'questionCount':inv['globalMAIN']['questionCount'],'projectionShape':'{topicId,id,prompt,answers:[four text],correctIndex}; sorted topic filenames and original question order','rowsCanonicalSHA256':inv['globalMAIN']['rowsCanonicalSHA256'],'allCurrentFileByteBindings':inv['globalMAIN']['allCurrentFileByteBindings'],'readDate':'2026-10-21'},
 'sameTopicMAIN':inv['sameTopicMAIN'],'fullClosestCurrentPeers':closest,
 'currentGuardRows':{'candidateLiveMainBinding':{'sourceFilePath':str(ROOT/'src/content/topics/polar-regions.json'),'sourceFileSHA256':inv['sameTopicMAIN']['fileSHA256'],'sourceOrder':86,'card':before,'cardCanonicalSHA256':sha(before)}},
 'bilateralCurrentComparisons':comparisons,'globalLiteralRetrievalOnlyHits':hits,'genuineProposalPairs':[],'observedNonmatchingProposals':[],
 'proposalSearchLimitations':'No live proposal inventory was designated. Fresh 11,000-row global MAIN search used exact terms satellite altimetry, ice core, radar sounding, GPS geodesy and surface-height methods. Full closest peers include the complementary polar GPS-method question and the global ocean altimetry question; every listed exact-method result has its full current body in globalLiteralRetrievalOnlyHits.',
 'limitations':['The direct correct source body is unavailable, so no source-backed content change or PASS is proposed.','The 100 current polar-regions card bodies are bound in actualCurrentPeers. Four closest current peers have full bilateral ERVC/direct-reverse comparisons; the global ocean altimetry card is explicitly flagged for high thematic overlap.','No source-driven candidate peer is treated as independent review; no quality credit or catalog application is claimed.'],'actualCurrentPeers':actual}
for n,d in [('candidate.json',candidate),('sourceproof.json',proof),('peer-snapshot.json',peer)]: (OUT/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'beforeHash':sha(before),'afterHash':sha(proposed),'status':'HOLD','sources':0,'groups':len(literals),'triples':len(assess),'actualPeers':len(actual),'closest':len(closest),'globalHits':len(hits)},ensure_ascii=False))
