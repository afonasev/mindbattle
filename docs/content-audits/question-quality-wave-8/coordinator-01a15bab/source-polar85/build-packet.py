import json, hashlib, copy
from pathlib import Path
ROOT=Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle')
OUT=ROOT/'docs/content-audits/question-quality-wave-8/coordinator-01a15bab/source-polar85'
UID='01a15bb6-f7ab-7b41-a966-d26e37a5094c'; OWNER='01a15bab-dac7-7741-aafb-9f7eeddc5513'
sha=lambda x:hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
file_sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
load=lambda p:json.loads(Path(p).read_text())
inv=load(OUT/'fresh-inventory.json')
assert inv['globalMAIN']['topicFileCount']==110 and inv['globalMAIN']['questionCount']==11000
assert len(inv['sameTopicMAIN']['questions'])==100
qs=inv['sameTopicMAIN']['questions']; before=next(q for q in qs if q['id']=='polar-regions-concordia-france-italy')
assert sha(before)=='91b8594246a2ee629a0cf7897fa68dc84f70dbe66a1199369577c25920016656'
proposed=copy.deepcopy(before)
proposed['answers'][1]['note']='Станция Восток находится на 79° ю. ш. и 107° в. д., на высоте 3 477 м.'
proposed['answers'][2]['note']='Мак-Мердо — крупнейшая круглогодичная станция США и центральный логистический узел USAP.'
proposed['answers'][3]['note']='Конкордия непрерывно обитаема с 2005 года и служит важной площадкой для сейсмических и геомагнитных наблюдений.'
proposed['explanation']='В источнике IPEV Конкордия описана как французско-итальянская станция на куполе C. Поэтому только этот вариант соответствует обоим признакам вопроса.'
proposed['source']={'title':'IPEV — Concordia station','url':'https://institut-polaire.fr/en/antarctica/concordia-station/','verifiedAt':'2026-10-21'}
assert proposed['difficulty']=='medium' and proposed['correctIndex']==3

def groups(card):
 return {'prompt_ordered_answers_key':{'prompt':card['prompt'],'answers':[a['text'] for a in card['answers']],'correctIndex':card['correctIndex']},'explanation':card['explanation'],**{'note'+str(i):a['note'] for i,a in enumerate(card['answers'])}}
def mk_entry():
 bg,ag=groups(before),groups(proposed)
 return {'id':before['id'],'topicId':'polar-regions','sourceOrder':85,'status':'READY_FOR_INDEPENDENT_REVIEW','beforeCard':before,'beforeHash':sha(before),'proposedCard':proposed,'afterHash':sha(proposed),'fieldGroups':{k:{'beforeCanonicalSHA256':sha(bg[k]),'afterCanonicalSHA256':sha(ag[k])} for k in bg},'proposedCardCanonicalSHA256':sha(proposed)}
entry=mk_entry()
candidate={'owner':OWNER,'sourceNativeId':UID,'stage':'FRESH_PERSONAL_SOURCE85_COMPLETE','cycle':0,'qualityCredit':0,
 'scope':{'id':before['id'],'topicId':'polar-regions','sourceOrder':85,'frozen':{'id':before['id'],'topicId':'polar-regions','sourceOrder':85,'difficulty':'medium','correctIndex':3}},
 'history':{'preimage':'Fresh current inventory; exact complete-card hash matches the SOURCE85 assignment. No previous author verdict inherited.','previousEvidence':'Reuse complete saved IPEV, USAP, BAS, and NSF sources; no new fetch and no raw body duplication. The Vostok option note is narrowed to the saved BAS station-row facts, without the nationality claim held in SOURCE83.'},'entries':[entry]}

source_specs=[
 {'path':ROOT/'docs/content-audits/question-quality-wave-8/coordinator-01a15b80/source-polar82/raw/ipev-concordia-open.json','url':'https://institut-polaire.fr/en/antarctica/concordia-station/','title':'IPEV — Concordia station','locator':'L52 French-Italian operators; L54 continuously inhabited since 2005 and inland station; L55 Dome C; L85 coordinates; L90 altitude 3,233 m.','coverage':'Personally reread the complete retained IPEV capture and the full station identity/location section L50-L56,L83-L90. Used only for Concordia facts; no Vostok nationality claim is used.','reuse':True},
 {'path':ROOT/'docs/content-audits/question-quality-wave-8/coordinator-01a15b80/source-polar82/raw/usap-south-pole-open.json','url':'https://www.usap.gov/videoclipsandmaps/spwebcam.cfm','title':'USAP — South Pole Station Webcams','locator':'L104 station/axis passage; L111 Amundsen-Scott South Pole profile.','coverage':'Personally reread the complete retained USAP page and the identifying context at L91-L111. It places Amundsen-Scott at the Earth axis/geographic South Pole.','reuse':True},
 {'path':ROOT/'docs/content-audits/question-quality-wave-8/coordinator-01a1593a/source-polar42-complete/raw-sources/bas-factsheet-open-turn423.txt','url':'https://www.bas.ac.uk/wp-content/uploads/2026/05/Antarctic-factsheet_A4_Feb26-1.pdf','title':'British Antarctic Survey — Antarctic factsheet','locator':'L50@P1 lists Vostok station at 79ºS,107ºE, elevation 3,477 m.','coverage':'Personally reread the complete retained four-page factsheet and the complete Vostok station row L50@P1. Used only for the coordinate/elevation note; no Russian nationality claim is asserted.','reuse':True},
 {'path':ROOT/'docs/content-audits/question-quality-wave-8/coordinator-01a15bab/source-polar84/raw-nsf-mcmurdo-open.json','url':'https://www.nsf.gov/od/opp/ail/mcmurdo-station','title':'NSF McMurdo Station — Office of Polar Programs','locator':'L120 largest U.S. year-round station and central logistical hub; L132 Ross Island; L153 primary logistics hub for USAP.','coverage':'Personally reread the saved complete NSF page and the complete relevant station/location/role section L120-L176. It supports McMurdo as a U.S. year-round station and USAP hub on Ross Island.','reuse':True}
]
raw=[]
for s in source_specs:
 p=s['path']; assert p.is_file(),p
 r={'path':str(p),'url':s['url'],'sha256':file_sha(p),'title':s['title'],'locator':s['locator'],
    'captureReadProvenance':{'reusedWithoutRefetchOrBodyCopy':s['reuse'],'personalReadNativeId':UID,'personalReadCoverage':s['coverage']}}
 if p.suffix=='.json':
  d=load(p); assert d.get('url')==s['url']
  r.update({'completeOutputPointer':d['completeOutputPointer'],'completeOutputSHA256':d['completeOutputSHA256'],
   'captureReadProvenance':{**r['captureReadProvenance'],'originalSourceNativeId':d['sourceNativeId'],'nativeJournal':d['nativeJournal'],'nativeRecordLine':d['nativeRecordLine']}})
 raw.append(r)
byurl={x['url']:x for x in raw}; IPEV=byurl['https://institut-polaire.fr/en/antarctica/concordia-station/'];USAP=byurl['https://www.usap.gov/videoclipsandmaps/spwebcam.cfm'];BAS=byurl['https://www.bas.ac.uk/wp-content/uploads/2026/05/Antarctic-factsheet_A4_Feb26-1.pdf'];NSF=byurl['https://www.nsf.gov/od/opp/ail/mcmurdo-station']

def literal(key,ground,paths,locator):
 value=groups(proposed)[key]
 return {'group':key,'literal':value,'literalSHA256':sha(value),'primaryGround':ground,'sourcePaths':paths,'locator':locator}
literals=[
 literal('prompt_ordered_answers_key','IPEV identifies Concordia as a French-Italian station (L52) built on Dome C (L55), so it alone satisfies both key clues. USAP places Amundsen-Scott at the South Pole (L104,L111); BAS gives Vostok station coordinates/elevation far inland (L50@P1); NSF locates McMurdo on Ross Island (L132).',[IPEV['path'],USAP['path'],BAS['path'],NSF['path']],'IPEV L52,L55; USAP L104,L111; BAS L50@P1; NSF L132.'),
 literal('explanation','IPEV directly calls Concordia French-Italian (L52) and says it is built on Dome C (L55). The two sentences state these facts and the resulting unique fit without an additional unsupported claim.',[IPEV['path']],'IPEV L52,L55.'),
 literal('note0','USAP L104-L111 identifies Amundsen-Scott at the Earth axis/geographic South Pole; that distinguishes it from Concordia on Dome C.',[USAP['path']],'USAP L104,L111.'),
 literal('note1','BAS L50@P1 gives Vostok station coordinates 79ºS,107ºE and elevation 3,477 m. The revised note contains these listed values and avoids the SOURCE83-held nationality claim.',[BAS['path']],'BAS L50@P1.'),
 literal('note2','NSF L120 identifies McMurdo as the largest U.S. year-round station and central logistical hub; L132 places it on Ross Island; L153 calls it the primary USAP logistics hub.',[NSF['path']],'NSF L120,L132,L153.'),
 literal('note3','IPEV L52 identifies the joint French-Italian station; L54 says it has been continuously inhabited since 2005 and is important for seismic and geomagnetic networks. These are station-specific facts beyond prompt/key.',[IPEV['path']],'IPEV L52,L54.')]
assess=[
 {'slot':0,'fullPrompt':proposed['prompt'],'answer':proposed['answers'][0]['text'],'note':proposed['answers'][0]['note'],'tripleSHA256':sha({'prompt':proposed['prompt'],'answer':proposed['answers'][0]['text'],'note':proposed['answers'][0]['note']}),'grammar':'Промпт и заметка грамматически корректны; название станции оформлено единообразно.','plausibilityUniqueKeyAndNoteTruthUsefulness':'Амундсен — Скотт — правдоподобная станция Антарктиды. USAP помещает её на географический Южный полюс, а не на купол C; следовательно, даже при общем операторе США она не удовлетворяет обоим условиям. Заметка истинна и полезно различает две локации.','sourcePaths':[USAP['path']],'locator':'USAP L104,L111.'},
 {'slot':1,'fullPrompt':proposed['prompt'],'answer':proposed['answers'][1]['text'],'note':proposed['answers'][1]['note'],'tripleSHA256':sha({'prompt':proposed['prompt'],'answer':proposed['answers'][1]['text'],'note':proposed['answers'][1]['note']}),'grammar':'Заметка построена как грамматически корректное предложение с координатами и высотой.','plausibilityUniqueKeyAndNoteTruthUsefulness':'Восток — правдоподобная антарктическая исследовательская станция. BAS приводит для неё координаты 79ºS,107ºE и высоту 3,477 м, отличные от положения Конкордии на Dome C; заметка правдива и полезна как конкретный ориентир.','sourcePaths':[BAS['path']],'locator':'BAS L50@P1.'},
 {'slot':2,'fullPrompt':proposed['prompt'],'answer':proposed['answers'][2]['text'],'note':proposed['answers'][2]['note'],'tripleSHA256':sha({'prompt':proposed['prompt'],'answer':proposed['answers'][2]['text'],'note':proposed['answers'][2]['note']}),'grammar':'Промпт и заметка грамматически корректны; «круглогодичная станция» и «логистический узел» согласованы.','plausibilityUniqueKeyAndNoteTruthUsefulness':'Мак-Мердо — правдоподобная антарктическая станция, в том числе сильный американский дистрактор. NSF подтверждает её роль узла USAP, но локализует её на острове Росса, не на куполе C; это отличает её от ключа. Заметка точна и объясняет дистрактор полезным operational контекстом.','sourcePaths':[NSF['path']],'locator':'NSF L120,L132,L153.'},
 {'slot':3,'fullPrompt':proposed['prompt'],'answer':proposed['answers'][3]['text'],'note':proposed['answers'][3]['note'],'tripleSHA256':sha({'prompt':proposed['prompt'],'answer':proposed['answers'][3]['text'],'note':proposed['answers'][3]['note']}),'grammar':'Промпт и заметка грамматически корректны; составное название Concordia передано последовательно как «Конкордия».','plausibilityUniqueKeyAndNoteTruthUsefulness':'Конкордия — правдоподобная станция Антарктиды. Только IPEV описывает её одновременно как французско-итальянскую и расположенную на Dome C, поэтому ключ единственный. Заметка правдива; непрерывное обитание с 2005 года и связь с сейсмическими и геомагнитными сетями дают собственные полезные факты сверх вопроса и ответа.','sourcePaths':[IPEV['path']],'locator':'IPEV L52,L54.'}
]
proof={'owner':OWNER,'sourceNativeId':UID,'stage':'FRESH_PERSONAL_SOURCE85_COMPLETE','cycle':0,'qualityCredit':0,'rawSources':raw,
 'sourceIndex':'Unique saved path/URL inventory checked in SOURCE82 retained-reuse and SOURCE84. Reused IPEV Concordia, USAP South Pole, BAS factsheet, and successful NSF McMurdo complete contexts; no fetch or body copy. Duplicate COMNAP82 capture and all fenced claims were not used. Vostok is grounded only by the BAS station row, with its held nationality assertion omitted.',
 'sourceAttempts':[],
 'entries':[{'id':before['id'],'status':'READY_FOR_INDEPENDENT_REVIEW','beforeHash':sha(before),'literalGroups':literals,'fourFullPromptAnswerNoteAssessments':assess,
  'correctNoteNewFact':'IPEV says Concordia has been continuously inhabited since 2005 and is important for seismic and geomagnetic networks (L54); these are distinct station-specific facts beyond the prompt and answer.',
  'absoluteDifficulty':'MEDIUM for adults with ordinary interest in geography: the options are all Antarctic stations and the question requires matching a less widely known station to both Dome C and the French-Italian operators. The pair of clues makes the answer unique without specialist science knowledge or multi-step reasoning.'}],
 'limitations':['All primary contexts are retained full captures; no source fetch or retry was made.','The Vostok note omits nationality and uses BAS station-row coordinates/elevation only, preserving the SOURCE83 hold fence.','No quality credit, independent review, catalog application, or integration is claimed.']}

qby={q['id']:(i,q) for i,q in enumerate(qs,1)}
selected=['polar-regions-dome-a-highest-ice','polar-regions-mount-erebus-active','polar-regions-amundsen-scott-south-pole','polar-regions-vostok-russian','polar-regions-mcmurdo-largest','polar-regions-rothera-uk','polar-regions-neumayer-germany','polar-regions-princess-elisabeth-belgium','polar-regions-halley-vi-modules']
peerfacts={
'polar-regions-dome-a-highest-ice':('Dome C / East Antarctic ice sheet','surface elevation comparison','Dome C listed at 3,233 m while Dome A is highest','ice-sheet landform elevation','Both questions contain Dome C, but this peer compares surface elevations among landforms and keys Dome A; candidate asks for a station on Dome C and French-Italian management. Different entity/relation/value.','Knowing Dome A is the highest landform does not identify a station jointly run by France and Italy on Dome C; the candidate answer does not solve the elevation comparison.'),
'polar-regions-mount-erebus-active':('Mount Erebus','active-volcano location','active volcano on Ross Island','Ross Island volcanology','The shared Antarctic/Ross Island context is distinct: peer asks which active volcano is on Ross Island; candidate asks station identity/operators at Dome C.','Knowing which volcano is on Ross Island does not identify Concordia or its management/location.'),
'polar-regions-amundsen-scott-south-pole':('Amundsen-Scott South Pole Station','station location','geographic South Pole','Antarctic station geography','Amundsen-Scott is one candidate option, but this peer asks which station occupies the South Pole. Candidate asks for the station on Dome C operated by France and Italy.','The South Pole station fact does not identify Concordia; Concordia’s operator/location does not answer the South Pole question.'),
'polar-regions-vostok-russian':('Vostok station / Lake Vostok','station-to-lake naming association','Vostok gave its name to Lake Vostok','Antarctic station and subglacial lake','Vostok appears as a distractor in the candidate; the peer asks about the station-to-lake naming association, not Dome C or joint French-Italian operation.','Vostok’s lake-name association does not identify Concordia; Concordia does not answer which station is associated with Lake Vostok.'),
'polar-regions-mcmurdo-largest':('McMurdo Station','Ross Island location and USAP logistics role','central logistics hub on Ross Island','Antarctic logistics and station geography','McMurdo is another candidate option; this peer tests its Ross Island logistics relation, while the candidate tests Concordia’s Dome C and French-Italian relation.','McMurdo logistics facts do not identify the joint French-Italian Dome C station; Concordia facts do not answer which station is the Ross Island hub.'),
'polar-regions-rothera-uk':('Rothera Station','British station location','Adelaide Island near Antarctic Peninsula','Antarctic station geography','Same broad category only; the peer concerns Rothera’s location and British identity, not Concordia on Dome C or its operators.','Rothera’s location does not identify Concordia.'),
'polar-regions-neumayer-germany':('Neumayer III','station platform and location','German station on Ekström Ice Shelf','Antarctic station engineering','Same broad station category but distinct entity, engineering relation and location; no shared answer or factual relation.','Neumayer III platform facts do not answer which station is jointly operated by France and Italy on Dome C.'),
'polar-regions-princess-elisabeth-belgium':('Princess Elisabeth Station','energy design and operator','Belgian zero-emissions/renewable energy station','Antarctic station energy design','Same broad station category only. The peer concerns Belgian energy design, not Concordia’s site or joint operation.','Princess Elisabeth energy design does not identify Concordia.'),
'polar-regions-halley-vi-modules':('Halley VI','station mobility and engineering','British station with ski-mounted hydraulic modules','Antarctic station engineering','Same broad station category only; peer tests Halley VI mobility, not Dome C or Concordia operators.','Halley VI engineering does not identify Concordia or answer its location/operator combination.')}
closest=[]; comparisons=[]
for pid in selected:
 order,q=qby[pid]; h=sha(q); closest.append({'id':pid,'topicId':'polar-regions','sourceOrder':order,'card':q,'sha256':h})
 ent,rel,val,ctx,cp,pc=peerfacts[pid]
 comparisons.append({'kind':'CURRENT_MAIN','peerId':pid,'peerFullCardSHA256':h,
  'candidateERVC':{'entity':'Concordia station','relation':'site and joint operation','value':'Dome C; French-Italian','context':'Antarctic permanent research station'},
  'peerERVC':{'entity':ent,'relation':rel,'value':val,'context':ctx},'candidateToPeer':cp,'peerToCandidate':pc,'isDuplicate':False})
actual=[{'id':q['id'],'topicId':'polar-regions','sourceOrder':i,'card':q,'sha256':sha(q)} for i,q in enumerate(qs,1)]
topic_path=ROOT/'src/content/topics/polar-regions.json'
hit_ids={'polar-regions-dome-a-highest-ice','polar-regions-amundsen-scott-south-pole','polar-regions-vostok-russian','polar-regions-mcmurdo-largest'}
hits=[]
for ident in sorted(hit_ids,key=lambda x:qby[x][0]):
 order,q=qby[ident];hits.append({'topicId':'polar-regions','sourceOrder':order,'id':ident,'card':q,'cardCanonicalSHA256':sha(q),'sourceFilePath':str(topic_path),'sourceFileSHA256':inv['sameTopicMAIN']['fileSHA256']})
peer={'owner':OWNER,'sourceNativeId':UID,'stage':'FRESH_PERSONAL_SOURCE85_COMPLETE','cycle':0,'qualityCredit':0,
 'candidate':{'id':before['id'],'topicId':'polar-regions','sourceOrder':85,'beforeCard':before,'beforeCardCanonicalSHA256':sha(before),'proposedCard':proposed,'proposedCardCanonicalSHA256':sha(proposed),'frozen':{'id':before['id'],'topicId':'polar-regions','sourceOrder':85,'difficulty':'medium','correctIndex':3},'semanticEntity':'Concordia station','semanticRelation':'site on Dome C and joint French-Italian operation','semanticValue':'Concordia is the French-Italian station on Dome C','semanticContext':'Antarctic station geography and international operators'},
 'globalMAIN':{'topicFileCount':inv['globalMAIN']['topicFileCount'],'questionCount':inv['globalMAIN']['questionCount'],'projectionShape':'{topicId,id,prompt,answers:[four text],correctIndex}; sorted topic filenames and original question order','rowsCanonicalSHA256':inv['globalMAIN']['rowsCanonicalSHA256'],'allCurrentFileByteBindings':inv['globalMAIN']['allCurrentFileByteBindings'],'readDate':'2026-10-21'},
 'sameTopicMAIN':inv['sameTopicMAIN'],'fullClosestCurrentPeers':closest,
 'currentGuardRows':{'candidateLiveMainBinding':{'sourceFilePath':str(topic_path),'sourceFileSHA256':inv['sameTopicMAIN']['fileSHA256'],'sourceOrder':85,'card':before,'cardCanonicalSHA256':sha(before)}},
 'bilateralCurrentComparisons':comparisons,'globalLiteralRetrievalOnlyHits':hits,'genuineProposalPairs':[],'observedNonmatchingProposals':[],
 'proposalSearchLimitations':'No live competing proposal inventory was designated. Fresh global MAIN retrieval used distinctive strings Concordia, Dome C and Russian/Antarctic station names, then read every full matching same-topic card and nearest station/location peers listed here. All selected peers have full current bodies and bilateral direct-reverse checks; none duplicates the candidate.',
 'limitations':['All 100 current same-topic card bodies/hashes are included in actualCurrentPeers; nine relevant full station/location peers are separately read and assessed.','Global MAIN binds 11,000 rows across 110 topic files to fresh file-byte hashes. Exact Dome C/Concordia/station-option retrieval hits are included above.','No quality credit, independent review, catalog change, or integration is claimed.'],'actualCurrentPeers':actual}
for name,obj in [('candidate.json',candidate),('sourceproof.json',proof),('peer-snapshot.json',peer)]: (OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'beforeHash':sha(before),'afterHash':sha(proposed),'sources':len(raw),'groups':len(literals),'variantAssessments':len(assess),'actualPeers':len(actual),'closestPeers':len(closest),'bilateral':len(comparisons),'globalHits':len(hits)},ensure_ascii=False))
