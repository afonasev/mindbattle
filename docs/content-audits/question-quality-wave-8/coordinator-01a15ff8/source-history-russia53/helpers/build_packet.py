import copy, hashlib, json, pathlib, re
C = pathlib.Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle')
OUT = C / 'docs/content-audits/question-quality-wave-8/coordinator-01a15ff8/source-history-russia53'
NATIVE = '01a16019-7dd2-7241-966f-4d7171bc9f27'
OWNER = '01a15ff8-512c-7111-9672-67fe234a3746'
sha = lambda v: hashlib.sha256(json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')).hexdigest()
file_sha = lambda p: hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()

def groups(card):
    return {
        'prompt_ordered_answers_key': {'prompt': card['prompt'], 'answers': [a['text'] for a in card['answers']], 'correctIndex': card['correctIndex']},
        'explanation': card['explanation'],
        **{'note'+str(k): a['note'] for k, a in enumerate(card['answers'])}
    }

def read_json(p): return json.loads(pathlib.Path(p).read_text())

def body_meta(p):
    d = read_json(p)
    return d, {
        'path': str(pathlib.Path(p).resolve()), 'url': d.get('url'),
        'sha256': file_sha(p), 'sourceNativeId': d.get('sourceNativeId'),
        'nativeRecordLine': d.get('nativeRecordLine'),
        'completeOutputPointer': d.get('completeOutputPointer'),
        'completeOutputSHA256': d.get('completeOutputSHA256')
    }

invpath = OUT / 'fresh-inventory.json'
inv = read_json(invpath)
card = next(copy.deepcopy(e['card']) for e in inv['actualCurrentPeers'] if e['id'] == 'history-russia-monarchy-ended')
assert sha(card) == 'ef6b542d8222803b30a298757d43e577e2ae21496b3c67916b6a9c4dfdfef9a9'
assert [e['sourceOrder'] for e in inv['actualCurrentPeers'] if e['id'] == card['id']] == [53]
proposed = copy.deepcopy(card)
proposed['answers'][0]['note'] = 'Во время Февральской революции забастовки в Петрограде переросли во всеобщую политическую стачку, а затем — в вооружённое восстание.'
proposed['source'] = {
    'title': 'Президентская библиотека имени Б.Н. Ельцина: «В ходе Февральской революции образованы новые органы власти»',
    'url': 'https://www.prlib.ru/history/619088',
    'verifiedAt': '2026-10-22'
}
old_groups, new_groups = groups(card), groups(proposed)
field_groups = {k: {'beforeCanonicalSHA256': sha(old_groups[k]), 'afterCanonicalSHA256': sha(new_groups[k])} for k in old_groups}

paths = {
    'nicholas': 'docs/content-audits/question-quality-wave-8/coordinator-01a15cb9/source-history-russia2/raw/prlib-nicholas-abdication-context.json',
    'october': 'docs/content-audits/question-quality-wave-8/coordinator-01a15cdf/source-history-russia6/raw/prlib-october-revolution-1917.json',
    'decembrists': 'docs/content-audits/question-quality-wave-8/coordinator-01a15cdf/source-history-russia6/raw/prlib-decembrist-uprising.json',
    'february': 'docs/content-audits/question-quality-wave-8/coordinator-01a15fba/source-history-russia47-cycle1/raw/prlib-february-new-authorities.json',
    'journal_attempt': 'docs/content-audits/question-quality-wave-8/coordinator-01a15ff8/source-history-russia53/raw/prlib-journal-metadata-only.json',
    'gazette_attempt': 'docs/content-audits/question-quality-wave-8/coordinator-01a15ff8/source-history-russia53/raw/prlib-newspaper-extracts-metadata-only.json',
}
provenance = {
    'nicholas': 'Previously retained full original President Library PDF web.open output. Personally read the relevant complete event context on P19 L398-L406 and P20 L408-L421 this turn; no refetch. It states the February Revolution culminated in Nicholas II abdication and records the March 1917 abdication context.',
    'october': 'Previously retained complete original President Library web.open body (native 01a15cf4-36b0-7053-a660-735cc46a898b, record line 139). Personally read the complete returned page this turn; no refetch.',
    'decembrists': 'Previously retained complete original President Library web.open body (native 01a15cf4-36b0-7053-a660-735cc46a898b, record line 207). Personally read the complete returned page this turn; no refetch.',
    'february': 'Previously retained complete original President Library web.open body (native 01a15fe5-e974-7173-be13-978bc932d6c7, record line 111). Personally read the complete returned page this turn; no refetch.',
    'journal_attempt': 'Current bounded official primary-source discovery follow-up. Opened the President Library catalog record for RGIA 516/1/25; only archival metadata, not the journal text, was returned. The record is preserved exactly; it is not used as factual proof.',
    'gazette_attempt': 'Current one official alternative for abdication material. Opened the President Library catalog record for GA RF 9505/1/46; only archival metadata, not the newspaper text, was returned. The record is preserved exactly; it is not used as factual proof.'
}
raw_sources=[]
for key in paths:
    d, m = body_meta(C / paths[key])
    m['captureReadProvenance'] = provenance[key]
    m['locator'] = {
        'nicholas': 'PDF pp. 19-20: L398-L406 and L408-L421; use only the event context and archival description actually visible there.',
        'october': 'L40-L55, especially L44, L50-L55: October 1917 Bolshevik seizure of power, overthrow of the Provisional Government, Bolsheviks became the ruling party.',
        'decembrists': 'L40-L45: December 1825 armed Decembrist rising in St Petersburg.',
        'february': 'L50-L60: February 1917 crisis/revolution, strikes escalating to general political strike and armed uprising (L51-L52), Nicholas II abdication (L59), overthrow of autocracy (L60).',
        'journal_attempt': 'L36-L47: catalog identifies the 1917 chamberlain journal and archive record, 13 leaves; no transcription/full journal body.',
        'gazette_attempt': 'L36-L47: catalog identifies 1917 newspaper clippings concerning abdications and Provisional Government orders, 76 leaves; no clipping text.'
    }[key]
    raw_sources.append(m)
raw_by_key = {k: str((C / p).resolve()) for k,p in paths.items()}

literal_specs = [
    ('prompt_ordered_answers_key', 'The prompt asks for the Russian 1917 event leading to Nicholas II’s abdication and the end of monarchy; answer labels are four named Russian political events from distinct dates/contexts. The President Library account links the February 1917 revolution to abdication and overthrow of autocracy (L50, L59-L60); its October account distinguishes the later Bolshevik seizure of power (L44, L50-L55); its Decembrist account dates that rising to 1825 (L40-L45); the retained Nicholas PDF also locates Bloody Sunday in January 1905 in St Petersburg (P17 L368-L374).', [raw_by_key['february'], raw_by_key['october'], raw_by_key['decembrists'], raw_by_key['nicholas']], 'President Library February page L50, L59-L60; October page L44-L55; Decembrist page L40-L45; Nicholas PDF P17 L368-L374 and P19 L402-L406.'),
    ('explanation', 'The February Revolution brought about Nicholas II’s abdication and the overthrow of autocracy; a Provisional Government was formed during the same revolutionary transition. The source describes formation on 2 (15) March and the late-evening abdication that date.', [raw_by_key['february']], 'President Library February page L57-L60; cross-check Nicholas PDF P19 L402-L406.'),
    ('note0', 'The note adds the event’s sequence: Petrograd strikes became a general political strike and then an armed uprising. This is a distinct, useful fact beyond naming the event or restating abdication/fall of monarchy.', [raw_by_key['february']], 'President Library February page L51-L52.'),
    ('note1', 'The named October Revolution was the Bolsheviks’ seizure of power; the Provisional Government was overthrown and the Bolsheviks became the ruling party.', [raw_by_key['october']], 'President Library October page L44, L50-L55.'),
    ('note2', 'The Decembrist armed rising occurred in St Petersburg on 14 (26) December 1825.', [raw_by_key['decembrists']], 'President Library Decembrist page L40-L45.'),
    ('note3', 'In St Petersburg, troops fired on the January 1905 workers’ procession; the page identifies it as Bloody Sunday and dates it 9 (22) January 1905.', [raw_by_key['nicholas']], 'President Library Nicholas PDF P17 L368-L374.')
]
literal_groups=[]
for name, ground, sources, locator in literal_specs:
    literal=new_groups[name]
    literal_groups.append({'group':name,'literal':literal,'literalSHA256':sha(literal),'primaryGround':ground,'sourcePaths':sources,'locator':locator})

full_prompt = proposed['prompt']
variant_specs = [
    {'slot':0,'grammar':'The standalone answer name «Февральская революция» is a valid nominative event title answering «Какое событие…?»; no agreement cue singles it out.','plausibilityUniqueKeyAndNoteTruthUsefulness':'The February Revolution is the only listed event tied by the source to Nicholas II’s abdication and overthrow of autocracy. The revised note is true and useful: it adds the sequence from Petrograd strikes to political strike and armed uprising, rather than repeating the key.', 'paths':[raw_by_key['february']], 'locator':'President Library February page L50-L52 and L59-L60.'},
    {'slot':1,'grammar':'The standalone answer name «Октябрьская революция» is a valid nominative event title, parallel in form and detail to «Февральская революция».','plausibilityUniqueKeyAndNoteTruthUsefulness':'It is a plausible same-year political-event distractor, but the source places the Bolshevik seizure of power in October, after the monarchy had already fallen. Its note accurately teaches that October brought the Bolsheviks to power.', 'paths':[raw_by_key['october']], 'locator':'President Library October page L44-L55; February page L59-L60.'},
    {'slot':2,'grammar':'The standalone answer name «Восстание декабристов» is a valid nominative event title and fits the same question frame.','plausibilityUniqueKeyAndNoteTruthUsefulness':'It is a plausible Russian political uprising but is dated to 1825, not 1917, and cannot be the event causing Nicholas II’s abdication. The note truthfully identifies its place and month/year.', 'paths':[raw_by_key['decembrists']], 'locator':'President Library Decembrist page L40-L45.'},
    {'slot':3,'grammar':'The standalone answer name «Кровавое воскресенье» is a valid nominative historical-event title, comparable in form to the other named events.','plausibilityUniqueKeyAndNoteTruthUsefulness':'It is a plausible Russian revolutionary-era event, but took place in January 1905, not 1917. The note accurately identifies the workers’ procession, St Petersburg, and 9 January 1905, which helps distinguish it.', 'paths':[raw_by_key['nicholas']], 'locator':'President Library Nicholas PDF P17 L368-L374.'}
]
variants=[]
for spec in variant_specs:
    i=spec['slot']; answer=proposed['answers'][i]['text']; note=proposed['answers'][i]['note']
    variants.append({'slot':i,'fullPrompt':full_prompt,'answer':answer,'note':note,'tripleSHA256':sha({'prompt':full_prompt,'answer':answer,'note':note}),
                     'grammar':spec['grammar'],'plausibilityUniqueKeyAndNoteTruthUsefulness':spec['plausibilityUniqueKeyAndNoteTruthUsefulness'],
                     'sourcePaths':spec['paths'],'locator':spec['locator']})

candidate = {
 'owner':OWNER,'sourceNativeId':NATIVE,'topicId':'history-russia','cycle':0,'phase':'SOURCE','qualityCredit':0,
 'entries':[{'id':'history-russia-monarchy-ended','topicId':'history-russia','sourceOrder':53,'status':'READY_FOR_INDEPENDENT_REVIEW',
             'beforeCard':card,'beforeHash':sha(card),'proposedCard':proposed,'afterHash':sha(proposed),'fieldGroups':field_groups}]
}
sourceproof = {
 'owner':OWNER,'sourceNativeId':NATIVE,'topicId':'history-russia','cycle':0,'phase':'SOURCE','qualityCredit':0,
 'sourceIndex':str((C/'docs/content-audits/question-quality-wave-8/coordinator-01a15ff8/qualified-source-history-russia51/sourceproof.json').resolve()),
 'additionalRetainedSourceIndexes':[
   str((C/'docs/content-audits/question-quality-wave-8/coordinator-01a15cb9/source-history-russia2/sourceproof.json').resolve()),
   str((C/'docs/content-audits/question-quality-wave-8/coordinator-01a15cdf/source-history-russia6/sourceproof.json').resolve()),
   str((C/'docs/content-audits/question-quality-wave-8/coordinator-01a15fba/source-history-russia47-cycle1/sourceproof.json').resolve())],
 'rawSources':raw_sources,
 'networkAttemptAccounting':[
   {'kind':'discovery','query':'site:prlib.ru/item акт отречения Николая II 2 марта 1917 документ','result':'Located official RGIA chamberlain journal record and one official alternative newspaper-clippings record. Search output is discovery metadata, not source proof.'},
   {'kind':'primary-attempt','url':'https://www.prlib.ru/item/465791','path':raw_by_key['journal_attempt'],'result':'The direct official record for RGIA 516/1/25 returned only catalog metadata. Its archive-description mode was also inspected in-session and showed metadata only; the durable capture is the direct item body. No journal text/full primary context was available; no retry planned.'},
   {'kind':'official-alternative','url':'https://www.prlib.ru/item/469709','path':raw_by_key['gazette_attempt'],'result':'Opened official GA RF 9505/1/46 newspaper-clippings record. Returned only catalog metadata; no clipping text/full primary context. No retry planned.'}
 ],
 'entries':[{'id':'history-russia-monarchy-ended','topicId':'history-russia','sourceOrder':53,'cycle':0,'status':'READY_FOR_INDEPENDENT_REVIEW',
             'beforeHash':sha(card),'afterHash':sha(proposed),'frozen':{'id':card['id'],'topicId':'history-russia','sourceOrder':53,'difficulty':'easy','correctIndex':0},
             'literalGroups':literal_groups,'fourFullPromptAnswerNoteAssessments':variants,
             'correctNoteNewFact':{'fact':'During the February Revolution, strikes in Petrograd grew into a general political strike and then an armed uprising. This process detail is additional to the prompt/key, which ask only for the event leading to abdication and monarchy’s fall.',
                                   'sourcePaths':[raw_by_key['february']],'locator':'President Library February page L51-L52.'},
             'absoluteDifficulty':{'level':'easy','audience':'Russian-speaking adults with broad school-level historical knowledge.',
                                   'ground':'The card tests recognition of the widely taught event that ended the Russian monarchy in 1917. It requires no rare date or terminology; the distractors are recognizable Russian political events, with the two 1917 revolutions providing a plausible distinction.',
                                   'qualification':'This is an editorial audience judgement under the pinned EASY definition, not a measured population survey.'}}]
}

# Current exact peers, full cards, hashes, and bilateral semantic tests.
peer_ids=['history-russia-last-emperor','history-russia-revolution-1917-month','history-russia-romanov-dynasty','history-russia-dual-power-1917','history-russia-bloody-sunday-event','history-russia-abdication-emperor']
peer_compare={
 'history-russia-last-emperor':('Nicholas II','last Russian emperor','person','Russian monarchy ending','CandidateToPeer: candidate asks which event caused abdication/fall; peer asks who was last emperor. Distinct event vs person relation. PeerToCandidate: being last emperor does not ask which event led to abdication. Not duplicate.'),
 'history-russia-revolution-1917-month':('October Revolution','the meaning of its name','Bolshevik seizure of power','Russia, October 1917','CandidateToPeer: February Revolution and October Revolution are separate events in the same year; only February led to abdication and monarchy’s fall. PeerToCandidate: the name of October Revolution does not ask which event ended monarchy. Not duplicate.'),
 'history-russia-romanov-dynasty':('Romanov dynasty','ruled Russia until a named revolution','dynastic endpoint','Russia, 1613-1917','CandidateToPeer: this peer asks which dynasty ruled up to the February Revolution; candidate asks which event caused abdication/fall. Distinct relation and answer. PeerToCandidate: the dynasty-duration fact does not answer which event caused abdication. Not duplicate.'),
 'history-russia-dual-power-1917':('February Revolution / post-revolutionary institutions','formed dual power','Provisional Government and Petrograd Soviet','Russia, March 1917','CandidateToPeer: candidate asks the preceding event; peer asks the two centers that formed after it. Related context, different relation/value. PeerToCandidate: naming dual-power institutions does not ask which event caused abdication. Not duplicate.'),
 'history-russia-bloody-sunday-event':('Bloody Sunday','workers’ procession was fired on','named 1905 event','St Petersburg, 9 January 1905','CandidateToPeer: candidate concerns the 1917 revolution; peer identifies a 1905 event. This is a distractor in candidate, not the same fact. PeerToCandidate: Bloody Sunday identification does not ask which event caused 1917 abdication. Not duplicate.'),
 'history-russia-abdication-emperor':('Nicholas II','person who abdicated','monarch identity','Russia, March 1917','CandidateToPeer: candidate asks which event led to abdication; peer asks who abdicated. Complementary but distinct fact, not a direct reverse. PeerToCandidate: identifying the person does not answer which event caused the abdication. Not duplicate.')
}
relevant=[]
for e in inv['actualCurrentPeers']:
    if e['id'] not in peer_ids: continue
    ent,rel,val,ctx,assessment=peer_compare[e['id']]
    relevant.append({'id':e['id'],'sourceOrder':e['sourceOrder'],'topicId':e['topicId'],'actualCurrentCard':e['card'],'actualCurrentCanonicalSHA256':e['sha256'],
                     'bilateralMAIN':{'candidateERVC':{'entity':'February Revolution of 1917','relation':'led to Nicholas II abdication and fall of monarchy','value':'event answering causal/identification prompt','context':'Russia, February-March 1917'},
                                      'peerERVC':{'entity':ent,'relation':rel,'value':val,'context':ctx},
                                      'candidateToPeer':assessment.split(' PeerToCandidate:')[0].replace('CandidateToPeer: ',''),
                                      'peerToCandidate':assessment.split(' PeerToCandidate:')[1].replace(' Not duplicate.',''),
                                      'isDuplicate':False}})

# Find the one cross-topic MAIN row with a comparable abdication-to-end-of-monarchy relation, then read full CURRENT card.
china=json.loads((C/'src/content/topics/history-china.json').read_text())
china_card=next(copy.deepcopy(q) for q in china['questions'] if q['id']=='history-china-easy-04a-05')
china_order=next(i for i,q in enumerate(china['questions'],1) if q['id']==china_card['id'])
china_hash=sha(china_card)
cross_comp={'id':china_card['id'],'topicId':'history-china','sourceOrder':china_order,'actualCurrentCard':china_card,'actualCurrentCanonicalSHA256':china_hash,
 'candidateERVC':{'entity':'Russian February Revolution / Nicholas II','relation':'event leads to Russian abdication and fall of monarchy','value':'Russia’s 1917 event','context':'Russia, 1917'},
 'peerERVC':{'entity':'Puyi / Qing dynasty','relation':'asks what abdication meant','value':'end of Chinese imperial rule','context':'China, 1912'},
 'candidateToPeer':'The peer has the same broad theme (an abdication ending monarchy) but a different country, monarch, date, and historical event; candidate concerns Russia in 1917. Not a semantic duplicate.',
 'peerToCandidate':'Puyi’s 1912 abdication and the end of Qing imperial rule do not answer which Russian event led to Nicholas II’s abdication in 1917. Not a direct reverse or duplicate.', 'isDuplicate':False}

snapshot = {
 'owner':OWNER,'sourceNativeId':NATIVE,'topicId':'history-russia','cycle':0,'id':'history-russia-monarchy-ended','sourceOrder':53,'stage':'SOURCE','qualityCredit':0,
 'candidate':{'beforeCard':card,'beforeCanonicalSHA256':sha(card),'proposedCard':proposed,'proposedCardCanonicalSHA256':sha(proposed),'frozen':{'id':card['id'],'topicId':'history-russia','sourceOrder':53,'difficulty':'easy','correctIndex':0},
             'semanticEntity':'February Revolution of 1917','semanticRelation':'led to Nicholas II abdication and fall of Russian monarchy','semanticValue':'named Russian political event','semanticContext':'Russia, 1917'},
 'immutableInventoryRaw':{'path':str(invpath.resolve()),'fileSHA256':file_sha(invpath)},
 'globalMAINRetrieval':{'path':str(invpath.resolve()),'rowCount':11000,'topicFileCount':110,'rowsCanonicalSHA256':inv['globalMAIN']['rowsCanonicalSHA256'],'query':'Exact prompt/answer and same-event/entity/date/relation scan over all current MAIN rows.','inventoryFileSHA256':file_sha(invpath)},
 'globalMAIN':inv['globalMAIN'],'sameTopicMAIN':inv['sameTopicMAIN'],'actualCurrentPeers':inv['actualCurrentPeers'],
 'relevantCurrentPairs':relevant,
 'crossTopicRelevantRowsBilateralComparisons':[cross_comp],
 'genuineProposalPairs':[],
 'inventoryScan':{'exactMAINMatchesOtherThanSelf':[],'query':'Candidate prompt and all four answer labels compared to all 11000 MAIN rows; no other exact matches. Cross-topic scan for February/October Revolution, Nicholas II, abdication, and monarchy-ending relations returned the Puyi abdication row as the closest distinct analogy.',
                  'result':'No exact duplicate outside the candidate self row. Same-topic related contexts are represented in relevantCurrentPairs.',
                  'crossTopicQuery':'Cross-topic MAIN rows with an abdication/monarch or February/October Revolution/Nicholas II reference, followed by full-card semantic comparison.',
                  'crossTopicResult':'The China Puyi 1912 question shares the broad monarchy-ending theme but concerns a different empire, monarch, year, and event; not duplicate.',
                  'crossTopicRelatedRows':[{'topicId':'history-china','id':'history-china-easy-04a-05','sourceOrder':china_order,'prompt':china_card['prompt'],'answers':[a['text'] for a in china_card['answers']],'correctIndex':china_card['correctIndex']}]},
 'sameTopicMAINRetrieval':{'path':inv['sameTopicMAIN']['path'],'fileSHA256':inv['sameTopicMAIN']['fileSHA256'],'topicId':'history-russia','rowCount':100,'rowsCanonicalSHA256':sha([{'id':q['id'],'prompt':q['prompt'],'answers':[a['text'] for a in q['answers']],'correctIndex':q['correctIndex']} for q in inv['sameTopicMAIN']['questions']]),'query':'Scan all 100 current cards for Russia 1917 revolutions, monarchy/abdication, and the candidate’s named event distractors.'}
}

for name,obj in [('candidate.json',candidate),('sourceproof.json',sourceproof),('peer-snapshot.json',snapshot)]:
    (OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'nativeId':NATIVE,'baselineHash':sha(card),'afterHash':sha(proposed),'fieldGroupCount':len(field_groups),'variantCount':len(variants),'currentPeerCount':len(inv['actualCurrentPeers']),'globalMAINCount':len(inv['globalMAIN']['rows']),'relevantSameTopicPairs':len(relevant),'crossTopicPairs':1,'rawSourceCount':len(raw_sources),'files':[str(OUT/n) for n in ['candidate.json','sourceproof.json','peer-snapshot.json']],'qualityCredit':0},ensure_ascii=False))
