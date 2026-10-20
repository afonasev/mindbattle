import json, hashlib, copy
from pathlib import Path
ROOT=Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle')
OUT=ROOT/'docs/content-audits/question-quality-wave-8/coordinator-01a15bab/source-polar84'
UID='01a15bb6-f7ab-7b41-a966-d26e37a5094c'
OWNER='01a15bab-dac7-7741-aafb-9f7eeddc5513'
sha=lambda x: hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
file_sha=lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
load=lambda p: json.loads(Path(p).read_text())
inv=load(OUT/'fresh-inventory.json')
assert inv['globalMAIN']['topicFileCount']==110 and inv['globalMAIN']['questionCount']==11000
assert inv['sameTopicMAIN']['topicId']=='polar-regions' and len(inv['sameTopicMAIN']['questions'])==100
before=next(q for q in inv['sameTopicMAIN']['questions'] if q['id']=='polar-regions-mcmurdo-largest')
assert sha(before)=='52ce5664d9ecd4d75c8a4986a5e5cb818ea56448a4ae8567a7f56f9725b76131'
proposed=copy.deepcopy(before)
proposed['answers'][1]['note']='Станция Восток находится во внутренней части Восточной Антарктиды.'
proposed['answers'][3]['note']='Мак-Мердо — крупнейшая круглогодичная станция США; летом за неделю здесь может находиться до 1 100 человек.'
proposed['explanation']='Мак-Мердо — центральный логистический узел программы USAP; станция поддерживает исследования на континенте и на станции Амундсен — Скотт.'
proposed['source']={'title':'NSF — McMurdo Station','url':'https://www.nsf.gov/od/opp/ail/mcmurdo-station','verifiedAt':'2026-10-21'}
assert proposed['difficulty']=='medium' and proposed['correctIndex']==3

def groups(card):
    return {'prompt_ordered_answers_key':{'prompt':card['prompt'],'answers':[a['text'] for a in card['answers']],'correctIndex':card['correctIndex']},
            'explanation':card['explanation'], **{'note'+str(i):a['note'] for i,a in enumerate(card['answers'])}}
bg,ag=groups(before),groups(proposed)
field_groups={k:{'beforeCanonicalSHA256':sha(bg[k]),'afterCanonicalSHA256':sha(ag[k])} for k in bg}
entry={'id':before['id'],'topicId':before.get('topicId','polar-regions'),'sourceOrder':84,
       'status':'READY_FOR_INDEPENDENT_REVIEW','beforeCard':before,'beforeHash':sha(before),
       'proposedCard':proposed,'afterHash':sha(proposed),'fieldGroups':field_groups,
       'proposedCardCanonicalSHA256':sha(proposed)}
candidate={'owner':OWNER,'sourceNativeId':UID,'stage':'FRESH_PERSONAL_SOURCE84_COMPLETE','cycle':0,'qualityCredit':0,
           'scope':{'id':before['id'],'topicId':'polar-regions','sourceOrder':84,
                    'frozen':{'id':before['id'],'topicId':'polar-regions','sourceOrder':84,'difficulty':'medium','correctIndex':3}},
           'history':{'preimage':'Fresh inventory from current code MAIN; exact card preimage SHA256 matches assigned frozen hash 52ce5664d9ecd4d75c8a4986a5e5cb818ea56448a4ae8567a7f56f9725b76131.','previousEvidence':'No prior author/reviewer verdict inherited. The old McMurdo USAP URL had two recorded TypeError checks; this packet uses one complete current official NSF page as the official alternative. Vostok nationality claim removed in light of SOURCE83 HOLD; no retry or adjacent workaround.'},
           'entries':[entry]}

# Immutable source references; existing complete captures are reused, never fetched again.
source_specs=[
 {'path':OUT/'raw-nsf-mcmurdo-open.json','url':'https://www.nsf.gov/od/opp/ail/mcmurdo-station','title':'NSF McMurdo Station — Office of Polar Programs','locator':'L120 largest U.S. year-round station/continent and central logistical hub; L132 Hut Point Peninsula, Ross Island; L153 primary USAP logistics hub; L163 summer weekly population up to 1,100.','reuse':False,'coverage':'Personally read the complete opened NSF page and the full lines 120-176; it directly supports McMurdo identity, the Ross Island locator, year-round station size, USAP logistics role, operational support, and the distinct summer population fact.','retrieval':'Official NSF alternative after the assigned USAP page had two recorded TypeError checks.'},
 {'path':ROOT/'docs/content-audits/question-quality-wave-8/coordinator-01a15b80/source-polar82/raw/usap-south-pole-open.json','url':'https://www.usap.gov/videoclipsandmaps/spwebcam.cfm','title':'USAP — South Pole Station Webcams','locator':'L104 identifies McMurdo and Palmer as the other two USAP stations and locates McMurdo on Ross Island; the same passage places Amundsen-Scott at Earth axis; L111 gives Amundsen-Scott station context.','reuse':True,'coverage':'Personally reread the complete captured page and its station-identification passage at L104 plus South Pole station context at L111. No fresh request was made.','retrieval':'Retained full primary capture reused from source-polar82 index; this body supports only the statements identified here.'},
 {'path':ROOT/'docs/content-audits/question-quality-wave-8/coordinator-01a1593a/source-polar42-complete/raw-sources/bas-factsheet-open-turn423.txt','url':'https://www.bas.ac.uk/wp-content/uploads/2026/05/Antarctic-factsheet_A4_Feb26-1.pdf','title':'British Antarctic Survey — Antarctic factsheet','locator':'L50@P1 identifies Vostok station at 79ºS, 107ºE in the Antarctic geographic-statistics table.','reuse':True,'coverage':'Personally read the complete preserved four-page visible factsheet and the full Vostok station row L50@P1. It supports the station identity/location only; no Russian nationality claim is made or used.','retrieval':'Retained full BAS visible page text reused; no fresh request was made.'},
 {'path':ROOT/'docs/content-audits/question-quality-wave-8/coordinator-01a15b80/source-polar82/raw/ipev-concordia-open.json','url':'https://institut-polaire.fr/en/antarctica/concordia-station/','title':'IPEV — Concordia station','locator':'L52 identifies Concordia as a French-Italian station; L54-L56 describes the interior Antarctic location and Dome C; L83-L90 locates it at 75°06′S, 123°21′E.','reuse':True,'coverage':'Personally reread the complete saved IPEV page, especially the station identity and location context at L50-L56 and L83-L90. For this card only the Concordia statements are used; no Vostok nationality evidence is adopted.','retrieval':'Retained full IPEV capture reused from source-polar82; no fresh request was made.'}
]
raw=[]
for s in source_specs:
 p=Path(s['path']); assert p.is_file(),p
 fs=file_sha(p)
 rec={'path':str(p),'url':s['url'],'sha256':fs,'title':s['title'],'captureReadProvenance':{
  'reusedWithoutRefetchOrBodyCopy':s['reuse'],'personalReadNativeId':UID,'personalReadCoverage':s['coverage'],'retrievalNote':s['retrieval']},'locator':s['locator']}
 if p.suffix=='.json':
  d=load(p); assert d.get('url')==s['url']
  rec.update({'completeOutputPointer':d['completeOutputPointer'],'completeOutputSHA256':d['completeOutputSHA256'],
              'captureReadProvenance':{**rec['captureReadProvenance'],'originalSourceNativeId':d['sourceNativeId'],'nativeJournal':d['nativeJournal'],'nativeRecordLine':d['nativeRecordLine']}})
 raw.append(rec)
raw_by_url={x['url']:x for x in raw}
NSF=raw_by_url['https://www.nsf.gov/od/opp/ail/mcmurdo-station']
USAP=raw_by_url['https://www.usap.gov/videoclipsandmaps/spwebcam.cfm']
BAS=raw_by_url['https://www.bas.ac.uk/wp-content/uploads/2026/05/Antarctic-factsheet_A4_Feb26-1.pdf']
IPEV=raw_by_url['https://institut-polaire.fr/en/antarctica/concordia-station/']

def literal(group,card,ground,paths,locator):
 value=groups(card)[group]
 return {'group':group,'literal':value,'literalSHA256':sha(value),'primaryGround':ground,'sourcePaths':paths,'locator':locator}
literals=[
 literal('prompt_ordered_answers_key',proposed,'NSF L120 and L132 identify McMurdo as the central logistical hub on Ross Island, making it the unique answer. USAP L104 places Amundsen-Scott at Earth axis/the South Pole; BAS L50@P1 locates Vostok in the Antarctic interior; IPEV L52,L54-L55,L85 places Concordia at inland Dome C. The prompt retains one specific station/geography relation; no other option satisfies the Ross Island hub description.',[NSF['path'],USAP['path'],BAS['path'],IPEV['path']],'NSF L120,L132; USAP L104; BAS L50@P1; IPEV L52,L54-L55,L85.'),
 literal('explanation',proposed,'NSF directly calls McMurdo the central logistical hub for USAP and says it supports continental research and Amundsen-Scott South Pole Station (L120); L153 independently specifies primary logistics hub.',[NSF['path']],'NSF L120,L153.'),
 literal('note0',proposed,'USAP L104 says Amundsen-Scott sits at Earth axis; L111 gives the South Pole station profile. This is true and distinguishes the first option from the Ross Island station.',[USAP['path']],'USAP L104,L111.'),
 literal('note1',proposed,'BAS geographic-statistics row names Vostok station and gives 79ºS,107ºE (L50@P1), placing it in interior East Antarctica. The revised note deliberately omits Russian nationality, which is under SOURCE83 HOLD.',[BAS['path']],'BAS L50@P1.'),
 literal('note2',proposed,'IPEV identifies Concordia as French-Italian (L52), inland at Dome C (L54-L55) and at 75°06′S,123°21′E (L85); these facts distinguish it from McMurdo on Ross Island.',[IPEV['path']],'IPEV L52,L54-L55,L83-L90.'),
 literal('note3',proposed,'NSF L120 says McMurdo is the largest U.S. year-round station and largest on the continent; L132 locates it on Ross Island; L163 states up to 1,100 people may be there during a summer week. The note preserves a supported scale fact and adds its own useful population fact beyond the prompt/key.',[NSF['path']],'NSF L120,L132,L163.')]

def triple_hash(prompt,answer,note): return sha({'prompt':prompt,'answer':answer,'note':note})
prompt=proposed['prompt']
assess=[
 {'slot':0,'fullPrompt':prompt,'answer':proposed['answers'][0]['text'],'note':proposed['answers'][0]['note'],'tripleSHA256':triple_hash(prompt,proposed['answers'][0]['text'],proposed['answers'][0]['note']),'grammar':'Грамматически корректная самостоятельная фраза; название станции и указание на географический Южный полюс согласованы.','plausibilityUniqueKeyAndNoteTruthUsefulness':'Амундсен — Скотт — правдоподобная американская антарктическая станция и потому сильный дистрактор для условия «американская». Но USAP L104 помещает её у земной оси/географического Южного полюса, не на острове Росса; ключ остаётся уникальным. Заметка точна и полезно различает место этой станции и Мак-Мердо.', 'sourcePaths':[USAP['path']],'locator':'USAP L104,L111.'},
 {'slot':1,'fullPrompt':prompt,'answer':proposed['answers'][1]['text'],'note':proposed['answers'][1]['note'],'tripleSHA256':triple_hash(prompt,proposed['answers'][1]['text'],proposed['answers'][1]['note']),'grammar':'Фраза грамматически естественна: подлежащее «станция Восток» согласуется со сказуемым «находится».','plausibilityUniqueKeyAndNoteTruthUsefulness':'Восток — правдоподобное название антарктической станции; BAS L50@P1 подтверждает станцию и её внутреннее положение по координатам 79ºS,107ºE. Это исключает её из условия об острове Росса. Заметка истинна и полезна, не повторяя неподтверждённое утверждение о российской принадлежности.', 'sourcePaths':[BAS['path']],'locator':'BAS L50@P1.'},
 {'slot':2,'fullPrompt':prompt,'answer':proposed['answers'][2]['text'],'note':proposed['answers'][2]['note'],'tripleSHA256':triple_hash(prompt,proposed['answers'][2]['text'],proposed['answers'][2]['note']),'grammar':'Промпт и заметка грамматически корректны; составное название станции оформлено последовательно.','plausibilityUniqueKeyAndNoteTruthUsefulness':'Конкордия — правдоподобная антарктическая станция. IPEV L52,L54-L55,L85 относит её к французско-итальянской станции на удалённом внутреннем Dome C, поэтому она не соответствует Мак-Мердо на острове Росса. Заметка истинна и добавляет полезные страну/место для этого дистрактора.', 'sourcePaths':[IPEV['path']],'locator':'IPEV L52,L54-L55,L83-L90.'},
 {'slot':3,'fullPrompt':prompt,'answer':proposed['answers'][3]['text'],'note':proposed['answers'][3]['note'],'tripleSHA256':triple_hash(prompt,proposed['answers'][3]['text'],proposed['answers'][3]['note']),'grammar':'Промпт и заметка грамматически корректны; имя «Мак-Мердо» последовательно используется как название станции.','plausibilityUniqueKeyAndNoteTruthUsefulness':'Мак-Мердо — правдоподобная американская антарктическая станция. NSF L120 прямо подтверждает её центральную логистическую роль и первенство среди круглогодичных станций США, а L132 — остров Росса; вместе это делает ключ уникальным. Заметка истинна и полезна: добавляет максимум людей за летнюю неделю, которого нет в промпте или названии ответа.', 'sourcePaths':[NSF['path']],'locator':'NSF L120,L132,L163.'}
]
proof={'owner':OWNER,'sourceNativeId':UID,'stage':'FRESH_PERSONAL_SOURCE84_COMPLETE','cycle':0,'qualityCredit':0,
       'rawSources':raw,'sourceIndex':'Fresh source inventory checked by unique raw-path/URL. Reused USAP, BAS, and IPEV full captures without fetching; the exact old McMurdo USAP URL had two TypeError attempts in source-url-check-strict-2026-09-04.json, so no retry was made. One current official NSF alternative capture supplies the full McMurdo facts. COMNAP duplicate82, AAP79, and ESA78 material was not promoted. SOURCE83 Vostok nationality HOLD was respected by removing that clause.',
       'sourceAttempts':[{'sequence':1,'kind':'historical_primary_attempts','url':'https://www.usap.gov/aboutthecontinent/au_mcmurdo.cfm','outcome':'source-url-check-strict-2026-09-04.json records TypeError twice for polar-regions-mcmurdo-largest; no retry by SOURCE84.'},{'sequence':2,'kind':'official_alternative','url':'https://www.nsf.gov/od/opp/ail/mcmurdo-station','outcome':'Complete official NSF page opened and saved once; personally read relevant full context. This completes the evidence chain; no further fetch.'}],
       'entries':[{'id':before['id'],'status':'READY_FOR_INDEPENDENT_REVIEW','beforeHash':sha(before),'literalGroups':literals,'fourFullPromptAnswerNoteAssessments':assess,
                   'correctNoteNewFact':'The correct-option note adds the distinct station-specific summer-week population: NSF L163 says McMurdo can have up to 1,100 people during a week in summer. This is an extra factual detail beyond prompt/key and makes the note useful.',
                   'absoluteDifficulty':'MEDIUM for adult readers with ordinary geography interest: all four choices are Antarctic research stations, and the key requires identifying a less commonly recalled station-to-location/operations link (McMurdo on Ross Island as USAP logistics hub). The distractors include a strong US-station rival (Amundsen-Scott), and the question requires one specific Antarctic geography fact rather than broad country elimination, specialist science, or multi-step reasoning.'}],
       'limitations':['The retired USAP page URL was not retried after two recorded TypeErrors; the independent official NSF alternative now directly supports the target claim.','Vostok nationality remains outside this packet because SOURCE83 terminal HOLD exhausted its source chain; the option note was narrowed to BAS-supported station/location facts.','No quality credit, independent review, catalog change, or application is claimed.']}

# Build full actual peer capture and targeted exact ERVC comparisons.
qs=inv['sameTopicMAIN']['questions']; qby={q['id']:(i,q) for i,q in enumerate(qs,1)}
selected=['polar-regions-mount-erebus-active','polar-regions-amundsen-scott-south-pole','polar-regions-vostok-russian','polar-regions-concordia-france-italy','polar-regions-rothera-uk','polar-regions-neumayer-germany','polar-regions-princess-elisabeth-belgium','polar-regions-halley-vi-modules']
closest=[]; comparisons=[]
peer_facts={
'polar-regions-mount-erebus-active':('Mount Erebus','active-volcano location','Ross Island, Antarctica','Ross Island geography / volcanology','The only shared specific place is Ross Island; this peer asks which active volcano is there, whereas candidate asks which station is the USAP hub. Candidate answer does not identify the volcano.','Knowing Erebus is on Ross Island does not identify the station serving as USAP hub. The relation and requested value are different.'),
'polar-regions-amundsen-scott-south-pole':('Amundsen-Scott South Pole Station','station location','geographic South Pole','Antarctic station geography','The shared station set contains Amundsen-Scott, but this peer asks for the station at the South Pole; candidate asks for McMurdo as Ross Island logistics hub. The entities/relations differ.','The South Pole station fact does not identify McMurdo’s Ross Island logistics role; candidate answer does not answer which station is at the South Pole.'),
'polar-regions-vostok-russian':('Vostok station / Lake Vostok','station-to-lake naming association','Vostok gave its name to the lake','Antarctic stations and subglacial lake naming','The shared option Vostok is only a distractor here; the peer asks about its named-lake association, not Ross Island logistics.','Knowing McMurdo’s logistics role does not identify Vostok or its lake relation; the peer’s naming association does not answer the candidate.'),
'polar-regions-concordia-france-italy':('Concordia station','joint operation and location','French-Italian station at Dome C','Antarctic station geography and operators','Concordia appears only as a distractor; this peer identifies the operator/location of Concordia, while candidate identifies McMurdo’s logistics relation.','Concordia’s operator/location does not identify McMurdo; McMurdo’s hub status does not answer which station is French-Italian.'),
'polar-regions-rothera-uk':('Rothera Station','station location and national operator','British station on Adelaide Island','Antarctic station geography','Both are station identification questions, but entities, relations, values, and site contexts differ; this peer concerns British Rothera, not USAP logistics.','Rothera’s island location does not identify McMurdo or its logistics role.'),
'polar-regions-neumayer-germany':('Neumayer III','station infrastructure and location','German station on Ekström Ice Shelf platform','Antarctic station engineering','Same broad station category only. The peer asks about platform engineering/location; candidate asks about McMurdo’s Ross Island logistics.','The Neumayer platform fact does not answer which Ross Island station is the USAP hub.'),
'polar-regions-princess-elisabeth-belgium':('Princess Elisabeth Station','energy design and national operator','Belgian station designed for near-zero emissions / renewables','Antarctic station energy design','Same broad station category only; a Belgian energy-design question does not overlap the USAP hub relation.','The answer about Princess Elisabeth does not identify McMurdo or its logistics role.'),
'polar-regions-halley-vi-modules':('Halley VI','station mobility / engineering','British station with ski-mounted hydraulic modules','Antarctic station engineering','Same broad station category only; the relation is mobile engineering, not Ross Island logistics.','Halley VI mobility does not identify McMurdo or answer the candidate.')}
for pid in selected:
 order,q=qby[pid]; h=sha(q)
 closest.append({'id':pid,'topicId':'polar-regions','sourceOrder':order,'card':q,'sha256':h})
 e,r,v,c,ctop,ptoc=peer_facts[pid]
 comparisons.append({'kind':'CURRENT_MAIN','peerId':pid,'peerFullCardSHA256':h,
  'candidateERVC':{'entity':'McMurdo Station','relation':'location and logistical role','value':'Ross Island; central USAP logistics hub','context':'U.S. Antarctic research support and station geography'},
  'peerERVC':{'entity':e,'relation':r,'value':v,'context':c},
  'candidateToPeer':ctop,'peerToCandidate':ptoc,'isDuplicate':False})
actual=[{'id':q['id'],'topicId':'polar-regions','sourceOrder':i,'card':q,'sha256':sha(q)} for i,q in enumerate(qs,1)]
# Direct global literal retrieval from the current 11,000-row projection; only same-topic exact retrieval hits require full card bindings.
hit_ids={'polar-regions-mount-erebus-active','polar-regions-amundsen-scott-south-pole','polar-regions-vostok-russian','polar-regions-concordia-france-italy'}
hits=[]
topic_path=ROOT/'src/content/topics/polar-regions.json'
for ident in sorted(hit_ids,key=lambda x:qby[x][0]):
 order,q=qby[ident]
 hits.append({'topicId':'polar-regions','sourceOrder':order,'id':ident,'card':q,'cardCanonicalSHA256':sha(q),'sourceFilePath':str(topic_path),'sourceFileSHA256':inv['sameTopicMAIN']['fileSHA256']})
peer={'owner':OWNER,'sourceNativeId':UID,'stage':'FRESH_PERSONAL_SOURCE84_COMPLETE','cycle':0,'qualityCredit':0,
 'candidate':{'id':before['id'],'topicId':'polar-regions','sourceOrder':84,'beforeCard':before,'beforeCardCanonicalSHA256':sha(before),'proposedCard':proposed,'proposedCardCanonicalSHA256':sha(proposed),'frozen':{'id':before['id'],'topicId':'polar-regions','sourceOrder':84,'difficulty':'medium','correctIndex':3},'semanticEntity':'McMurdo Station','semanticRelation':'location on Ross Island and role as primary USAP logistics hub','semanticValue':'McMurdo is the central logistics hub on Ross Island','semanticContext':'Antarctic station geography and U.S. Antarctic research support'},
 'globalMAIN':{'topicFileCount':inv['globalMAIN']['topicFileCount'],'questionCount':inv['globalMAIN']['questionCount'],'projectionShape':'{topicId,id,prompt,answers:[four text],correctIndex}; sorted topic file names and original question order','rowsCanonicalSHA256':inv['globalMAIN']['rowsCanonicalSHA256'],'allCurrentFileByteBindings':inv['globalMAIN']['allCurrentFileByteBindings'],'readDate':'2026-10-21'},
 'sameTopicMAIN':inv['sameTopicMAIN'],
 'fullClosestCurrentPeers':closest,
 'currentGuardRows':{'candidateLiveMainBinding':{'sourceFilePath':str(topic_path),'sourceFileSHA256':inv['sameTopicMAIN']['fileSHA256'],'sourceOrder':84,'card':before,'cardCanonicalSHA256':sha(before)}},
 'bilateralCurrentComparisons':comparisons,
 'globalLiteralRetrievalOnlyHits':hits,
 'genuineProposalPairs':[],
 'observedNonmatchingProposals':[],
 'proposalSearchLimitations':'No concurrent proposal inventory was designated in this one-card task. Search covered exact station names, Ross Island and station/geography terms in fresh global MAIN and all 100 topic cards. The only close current MAIN relations are the explicit station peers and the Mount Erebus Ross Island question listed above; each is checked bilaterally and none duplicates the candidate.',
 'limitations':['All 100 current same-topic card bodies and hashes are preserved in actualCurrentPeers; full closest station/location peers are separately assessed.','The current global MAIN projection contains 11,000 prompt/answer/key rows from 110 topic files with fresh byte bindings; exact thematic retrieval hits are included above.','No actual peer is treated as the candidate itself; all peer comparisons are distinct IDs. No quality credit or independent review is claimed.'],
 'actualCurrentPeers':actual}
for name,obj in [('candidate.json',candidate),('sourceproof.json',proof),('peer-snapshot.json',peer)]:
 (OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'outputs':[str(OUT/x) for x in ['candidate.json','sourceproof.json','peer-snapshot.json']], 'beforeHash':sha(before),'afterHash':sha(proposed),'sourceCount':len(raw),'actualCurrentPeers':len(actual),'closestPeers':len(closest),'literalGroups':len(literals),'fourVariantAssessments':len(assess)},ensure_ascii=False))
