import hashlib, json, pathlib

C = pathlib.Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle')
COORD = C / 'docs/content-audits/question-quality-wave-8/coordinator-01a15f0b'
OUT = COORD / 'source-history-russia35-cycle1'
RAW = OUT / 'raw'
TASK = json.load(open(COORD / 'source-history-russia35-cycle1-task.json'))
INV = json.load(open(RAW / 'fresh-inventory.json'))
OWNER = TASK['owner']; NATIVE = TASK['authorNativeId']
INITIAL_PATH = COORD / 'independent-history-russia35-initial/receipt.json'
PREVIOUS_SOURCE = COORD / 'source-history-russia35/sourceproof.json'
PREVIOUS_PEERS = COORD / 'source-history-russia35/peer-snapshot.json'
PREVIOUS_AUTHOR = COORD / 'source-history-russia35/candidate.json'


def sha(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')).hexdigest()

def file_sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

actual = next(x for x in INV['actualCurrentPeers'] if x['id'] == TASK['id'])
before = json.loads(json.dumps(actual['card'], ensure_ascii=False))
assert sha(before) == TASK['beforeHash'] == actual['sha256']
proposed = json.loads(json.dumps(before, ensure_ascii=False))
proposed['prompt'] = 'Как была устроена введённая Петром I Табель о рангах?'
proposed['answers'] = [
    {'text': 'Она устанавливала единые наименования чинов во всех классах трёх видов службы.', 'note': 'У каждого вида службы были свои наименования рангов и знаки различия; общего набора названий Табель не устанавливала.'},
    {'text': 'Она ставила военные, гражданские и придворные чины на равные места в каждом классе.', 'note': 'Военные чины ставились выше соответствующих гражданских и придворных, поэтому их положение в классе не было равным.'},
    {'text': 'Она задавала единые правила перехода между классами всех трёх видов службы.', 'note': 'Для каждого вида службы предусматривались собственные правила получения следующего чина, а не единый порядок.'},
    {'text': 'Она распределяла чины по классам военной, гражданской и придворной службы.', 'note': 'Каждый из трёх видов службы делился на 14 классов: I класс был высшим, а XIV — низшим.'},
]
proposed['correctIndex'] = 3
# Preserve the independently accepted explanation and source as unchanged facts.
assert proposed['explanation'] == before['explanation']
assert proposed['source'] == before['source']
assert proposed['difficulty'] == 'medium' and proposed['correctIndex'] == 3
assert all(len(a['text'].encode('utf-16-le')) // 2 <= 140 for a in proposed['answers'])
assert all(len(a['note'].split()) <= 35 for a in proposed['answers'])
assert len(proposed['explanation'].split()) <= 70

before_groups = {
    'prompt_ordered_answers_key': {'prompt':before['prompt'],'answers':[a['text'] for a in before['answers']],'correctIndex':before['correctIndex']},
    'explanation':before['explanation'], **{f'note{i}':before['answers'][i]['note'] for i in range(4)}
}
after_groups = {
    'prompt_ordered_answers_key': {'prompt':proposed['prompt'],'answers':[a['text'] for a in proposed['answers']],'correctIndex':proposed['correctIndex']},
    'explanation':proposed['explanation'], **{f'note{i}':proposed['answers'][i]['note'] for i in range(4)}
}
field_groups = {k:{'beforeCanonicalSHA256':sha(before_groups[k]),'afterCanonicalSHA256':sha(after_groups[k])} for k in before_groups}

sourceproof_old = json.load(open(PREVIOUS_SOURCE))
alt = next(x for x in sourceproof_old['rawSources'] if x['url']=='https://www.prlib.ru/node/619004')
primary = next(x for x in sourceproof_old['rawSources'] if x['url']=='https://www.prlib.ru/item/454265')
source_ref = 'docs/content-audits/question-quality-wave-8/coordinator-01a15f0b/source-history-russia35/raw/prlib-tableofranks-official-alternative.json'
primary_ref = 'docs/content-audits/question-quality-wave-8/coordinator-01a15f0b/source-history-russia35/raw/prlib-tableofranks-primary.json'
source_paths = [source_ref]
loc = 'Президентская библиотека, «Петром I утверждена „Табель о рангах“», L47-L48.'
grounds = {
 'prompt_ordered_answers_key': ('В L47 перечислены все три вида службы и сообщается, что каждый делился на 14 классов; там же сказано, что у каждого вида были собственные особенности, названия рангов и правила повышения. L48 прямо устанавливает преимущество военных чинов над соответствующими гражданскими и придворными. Поэтому единый истинный вариант описывает распределение по классам; варианты 0, 1 и 2 отдельно опровергаются источником по названию, старшинству и правилам продвижения.', 'Президентская библиотека, L44-L48; особенности видов службы L47, старшинство L48.'),
 'explanation': ('Без изменений сохранён текст INITIAL35: L47 прямо подтверждает три названных вида службы и их 14-классную структуру; L48 подтверждает преимущество военных чинов над соответствующими гражданскими и придворными.', 'Президентская библиотека, L47-L48; literal SHA и текст совпадают с INITIAL35 receipt.'),
 'note0': ('L47 сообщает, что у каждого вида службы были собственные наименования рангов и знаки различия. Справка опровергает конкретное предположение об общих наименованиях.', 'Президентская библиотека, L47.'),
 'note1': ('L48 прямо говорит, что военные чины ставились выше соответствовавших им гражданских и придворных; поэтому утверждение о равном положении неверно.', 'Президентская библиотека, L48.'),
 'note2': ('L47 сообщает, что у каждого вида службы были собственные правила получения следующего чина; справка объясняет, почему общий порядок повышения неверен.', 'Президентская библиотека, L47.'),
 'note3': ('L47 говорит, что каждый из трёх видов службы делился на 14 классов; L48 уточняет, что I был высшим, XIV — низшим. Число и границы классов остаются дополнительным фактом сверх prompt и keyed answer.', 'Президентская библиотека, L47-L48.')
}
literal_groups=[]
for group,literal in after_groups.items():
 g,locator=grounds[group]
 literal_groups.append({'group':group,'literal':literal,'literalSHA256':sha(literal),'primaryGround':g,'locator':locator,'sourcePaths':source_paths})

assessment_texts = [
 'Ответ грамматически продолжает вопрос «Как была устроена»: «Она…» относится к Табели (женский род). Все варианты используют одинаковую повествовательную рамку, перечисляют те же три вида службы и предлагают отдельный, сопоставимый аспект организации чинов. Источник прямо опровергает общие названия: у каждого вида были свои наименования рангов и знаки различия. Справка даёт именно этот факт.',
 'Ответ грамматически продолжает вопрос «Как была устроена» и сопоставим с соседними утверждениями по субъекту, охвату и детализации. Источник опровергает равенство: военные чины ставились выше соответствующих гражданских и придворных. Справка объясняет конкретный неверный тезис.',
 'Ответ грамматически продолжает вопрос и описывает тот же аспект служебной системы, что и соседние утверждения. Источник опровергает общий порядок продвижения: у каждого вида службы были свои правила получения следующего чина. Справка учит именно этому различию.',
 'Ответ грамматически продолжает вопрос и сопоставим по рамке и охвату с тремя альтернативами. Источник прямо указывает классификацию чинов по классам в военной, гражданской и придворной службе; другие варианты называют отдельные свойства, которые источник прямо различает. Справка добавляет число классов и их крайние места.'
]
assessments=[]
for i,a in enumerate(proposed['answers']):
 assessments.append({'slot':i,'fullPrompt':proposed['prompt'],'answer':a['text'],'note':a['note'],'grammar':'Вопрос «Как была устроена…?» и все четыре полных ответа образуют грамматически завершённые пары. Единая рамка «Она…» согласована с «Табель», род и число согласованы; списки военной, гражданской и придворной службы параллельны.','plausibilityUniqueKeyAndNoteTruthUsefulness':assessment_texts[i],'sourcePaths':source_paths,'locator':'Президентская библиотека, L47-L48.' if i in (1,3) else 'Президентская библиотека, L47.','tripleSHA256':sha({'prompt':proposed['prompt'],'answer':a['text'],'note':a['note']})})

identity={
 'sourceNativeId':NATIVE,'nativeJournal':TASK['authorNativeJournal'],'sessionMetaRecordLine':1,
 'verification':'Лично проверено: session_meta.payload.id == session_meta.payload.session_id == sourceNativeId; owner является координатором и не подменяет автора.',
 'actualCompactionsObserved':0
}
entry={'id':TASK['id'],'topicId':TASK['topicId'],'sourceOrder':TASK['sourceOrder'],'status':'READY_FOR_SAME_READER_FINAL','beforeCard':before,'beforeHash':sha(before),'proposedCard':proposed,'afterHash':sha(proposed),'fieldGroups':field_groups,'proposedCardCanonicalSHA256':sha(proposed)}
candidate={
 'owner':OWNER,'sourceNativeId':NATIVE,'stage':'SOURCE35_CYCLE1_READY_FOR_SAME_READER_FINAL','cycle':1,'qualityCredit':0,
 'scope':{'id':TASK['id'],'topicId':TASK['topicId'],'sourceOrder':35,'difficulty':'medium','correctIndex':3,'baselineCode':TASK['baselineCode'],'catalogCandidate':TASK['catalogCandidate']},
 'history':[{'stage':'INITIAL35','status':'FIX','receipt':str(INITIAL_PATH.relative_to(C)),'finding':'ANSWER_ROW_QUANTIFIER_FULL_SET_CUE'},{'stage':'SOLE_CYCLE1','status':'READY_FOR_SAME_READER_FINAL','note':'Сопоставлены четыре утверждения об организации одной и той же системы; все варианты покрывают все три вида службы, отличаются отдельными проверяемыми аспектами и имеют индивидуальные источниковые основания.'}],
 'entries':[entry],
 'identityVerification':identity
}

correct_note_fact={'fact':'Каждый из трёх видов службы делился на 14 классов; первый класс был высшим, XIV — низшим. Факт о числе классов и границах остаётся дополнительным к prompt и ответу slot3, который говорит только о распределении по классам.','sourcePaths':source_paths,'locator':'Президентская библиотека, L47-L48.'}
sourceproof_entry={'id':TASK['id'],'status':'READY_FOR_SAME_READER_FINAL','beforeHash':sha(before),'literalGroups':literal_groups,'fourFullPromptAnswerNoteAssessments':assessments,'correctNoteNewFact':correct_note_fact,'absoluteDifficulty':{'frozenLevel':'medium','audienceGround':'Для решения нужно знать устройство конкретной петровской системы чинов: источнику соответствуют классификация по видам службы и классам, а не одинаковая номенклатура, равное межвидовое старшинство или единое правило повышения. Это тематическая знакомость, не общеизвестная биография и не многошаговое рассуждение.'}}
sourceproof={
 'owner':OWNER,'sourceNativeId':NATIVE,'stage':'SOURCE35_CYCLE1_READY_FOR_SAME_READER_FINAL','cycle':1,'qualityCredit':0,
 'rawSources':[
   {'path':primary_ref,'url':primary['url'],'sha256':primary.get('fileSHA256',primary['sha256']),'completeOutputSHA256':primary['completeOutputSHA256'],'completeOutputPointer':primary['completeOutputPointer'],'captureReadProvenance':primary['captureReadProvenance'],'reuse':'UNCHANGED retained original; no reopen.'},
   {'path':source_ref,'url':alt['url'],'sha256':alt.get('fileSHA256',alt['sha256']),'completeOutputSHA256':alt['completeOutputSHA256'],'completeOutputPointer':alt['completeOutputPointer'],'captureReadProvenance':alt['captureReadProvenance'],'reuse':'Personally reread L44-L48 for this directed cycle; no reopen or copy.'}
 ],
 'sourceIndex':{'priorAuthorSourceproof':str(PREVIOUS_SOURCE.relative_to(C)),'previousInitialReceipt':str(INITIAL_PATH.relative_to(C)),'previousAuthorPacket':str(PREVIOUS_AUTHOR.relative_to(C)),'directedReuse':'SOURCE35 INITIAL source locations and full relevant official context reused at the exact original JSON Pointer. The primary scan catalog record remains metadata-only, not proof of the law text. No web/search calls in cycle1.'},
 'entries':[sourceproof_entry],
 'reusedInitialAssessments':[
  {'field':'explanation','previousReceiptPath':str(INITIAL_PATH.relative_to(C)),'previousReceiptLocator':'entries[0].sixLiteralCanonicalGroups[group=explanation]','previousCanonicalSHA256':next(x['canonicalSHA256'] for x in json.load(open(INITIAL_PATH))['entries'][0]['sixLiteralCanonicalGroups'] if x['group']=='explanation'),'reason':'Literal unchanged; source and interpretation still apply.'},
  {'field':'note3','previousReceiptPath':str(INITIAL_PATH.relative_to(C)),'previousReceiptLocator':'entries[0].sixLiteralCanonicalGroups[group=note3]','previousCanonicalSHA256':next(x['canonicalSHA256'] for x in json.load(open(INITIAL_PATH))['entries'][0]['sixLiteralCanonicalGroups'] if x['group']=='note3'),'reason':'The retained note still states the additional 14-class fact and highest/lowest endpoints; prompt and answer do not give the number or endpoints.'}
 ],
 'limitations':['Cycle1 is a directed author response for same-reader FINAL, not independent review or catalog application.','No new source calls, tests, QA, catalog writes, or quality credit.'],
 'immutableFullOriginalToolOutputs':[{'path':primary_ref,'sha256':primary.get('fileSHA256',primary['sha256']),'jsonPointer':primary['completeOutputPointer']},{'path':source_ref,'sha256':alt.get('fileSHA256',alt['sha256']),'jsonPointer':alt['completeOutputPointer']}],
 'networkAttemptLedger':{'cycle1NewCalls':0,'reusedNativeSources':[{'url':primary['url'],'nativeJournal':primary['captureReadProvenance']['nativeJournal'],'nativeRecordLine':primary['captureReadProvenance']['nativeRecordLine'],'disposition':'metadata only; no claim support'},{'url':alt['url'],'nativeJournal':alt['captureReadProvenance']['nativeJournal'],'nativeRecordLine':alt['captureReadProvenance']['nativeRecordLine'],'disposition':'full official alternative context; reused without refetch'}]},
 'identityVerification':identity,
 'mechanicalIntake':{'status':'NOT_RUN','reason':'Author output only; coordinator owns intake and application.'}
}

# Fresh snapshots: all same-topic cards and all 11,000 global MAIN projections from helper.
source_files={}
for f in (C/'src/content/topics').glob('*.json'):
 try:
  topic=json.load(open(f))
  for q in topic.get('questions',[]):source_files[q['id']]=(f,topic,q)
 except Exception:pass
selected_same={3,19,64,66,74,96}
selected_global={'history-india-mansabdari','history-china-easy-04a-01','history-united-states-pendleton-reform','government-politics-civil-service'}
selected=[]
for x in INV['actualCurrentPeers']:
 if x['sourceOrder'] in selected_same and x['id']!=TASK['id']:
  selected.append({'id':x['id'],'topicId':x['topicId'],'sourceOrder':x['sourceOrder'],'card':x['card'],'sha256':sha(x['card'])})
for qid in selected_global:
 if qid not in source_files:continue
 f,topic,q=source_files[qid]
 so=next(n for n,z in enumerate(topic['questions'],1) if z['id']==qid)
 selected.append({'id':qid,'topicId':topic['id'],'sourceOrder':so,'card':q,'sha256':sha(q),'sourceFilePath':str(f.relative_to(C)),'sourceFileSHA256':file_sha(f)})
candidate_ervc={'entity':'Табель о рангах Петра I','relation':'как систематизировала виды чинов','value':'распределение по классам; разные наименования и правила по видам; военные выше соответствующих статских и придворных','context':'Российская империя, 1722'}
peer_ervc={
 'history-russia-peter-title':{'entity':'Пётр I','relation':'получил прозвание','value':'Великий','context':'после победы в Северной войне'},
 'history-russia-peter-capital':{'entity':'Санкт-Петербург','relation':'стал столицей России','value':'перенос столицы при Петре I','context':'начало XVIII века'},
 'history-russia-senate-founder':{'entity':'Правительствующий сенат','relation':'учреждён кем','value':'Пётр I','context':'1711'},
 'history-russia-ministries-founder':{'entity':'российские министерства','relation':'учреждены кем','value':'Александр I','context':'1802'},
 'history-russia-supreme-privy-council':{'entity':'Верховный тайный совет','relation':'создан при','value':'Екатерина I','context':'1726'},
 'history-russia-state-council-reformer':{'entity':'Государственный совет','relation':'статус','value':'высший законосовещательный орган при императоре','context':'1810, план М. Сперанского'},
 'history-india-mansabdari':{'entity':'могольский мансаб','relation':'обозначение частей','value':'личный ранг и норма конницы','context':'империя Великих Моголов'},
 'history-china-easy-04a-01':{'entity':'экзамены императорского Китая','relation':'отбирали','value':'чиновников для госслужбы','context':'императорский Китай'},
 'history-united-states-pendleton-reform':{'entity':'Акт Пендлтона','relation':'ввёл','value':'конкурсный отбор чиновников','context':'федеральная служба США, 1883'},
 'government-politics-civil-service':{'entity':'государственная служба','relation':'определение','value':'профессиональный аппарат, выполняющий решения органов власти','context':'общее понятие'}
}
comparisons=[]
for peer in selected:
 qid=peer['id']; pe=peer_ervc[qid]
 comparisons.append({'kind':'same-topic' if peer['topicId']==TASK['topicId'] else 'global-semantic-peer','peerId':qid,'peerFullCardSHA256':peer['sha256'],'candidateERVC':candidate_ervc,'peerERVC':pe,'candidateToPeer':'Нет дубликата: у SOURCE35 отношение — классификация чинов Табелью 1722 года, а у peer другое событие, орган, понятие или другая административно-военная система. Все три категории и классовая структура не совпадают с проверяемой величиной peer.','peerToCandidate':'Обратная проверка: peer-карточка не отвечает, как Табель классифицировала виды чинов, а SOURCE35 не отвечает на конкретный факт peer; общего только исторический/служебный контекст либо имя Петра I.','isDuplicate':False})
rows=INV['globalMAIN']['rows']; terms=['табель о рангах','мансаб','государственные экзамены','государственной службы','чинопроизводство']; hits={}
for term in terms:
 for row in rows:
  if term.lower() in json.dumps(row,ensure_ascii=False).lower():
   qid=row['id']
   if qid in source_files:
    f,topic,q=source_files[qid]; so=next(n for n,z in enumerate(topic['questions'],1) if z['id']==qid)
    item=hits.setdefault(qid,{'topicId':topic['id'],'sourceOrder':so,'id':qid,'card':q,'cardCanonicalSHA256':sha(q),'sourceFilePath':str(f.relative_to(C)),'sourceFileSHA256':file_sha(f),'retrievalTerms':[]})
   else:item=hits.setdefault(qid,{'topicId':row['topicId'],'id':qid,'mainRow':row,'retrievalTerms':[]})
   item['retrievalTerms'].append(term)
actual_peers=[{'id':x['id'],'topicId':x['topicId'],'sourceOrder':x['sourceOrder'],'card':x['card'],'sha256':sha(x['card'])} for x in INV['actualCurrentPeers']]
peer_snapshot={
 'owner':OWNER,'sourceNativeId':NATIVE,'stage':'SOURCE35_CYCLE1_READY_FOR_SAME_READER_FINAL','cycle':1,'qualityCredit':0,
 'candidate':{'id':TASK['id'],'topicId':TASK['topicId'],'sourceOrder':35,'beforeCard':before,'beforeCardCanonicalSHA256':sha(before),'proposedCard':proposed,'proposedCardCanonicalSHA256':sha(proposed),'frozen':TASK['frozen'],'semanticEntity':candidate_ervc['entity'],'semanticRelation':candidate_ervc['relation'],'semanticValue':candidate_ervc['value']},
 'globalMAIN':{k:INV['globalMAIN'][k] for k in ('topicFileCount','questionCount','rowsCanonicalSHA256','allCurrentFileByteBindings')}|{'projectionShape':'Each row {topicId,id,prompt,answers:[four ordered texts],correctIndex}; excludes notes, explanation, source, sourceOrder.','readDate':'2026-10-21'},
 'sameTopicMAIN':INV['sameTopicMAIN'],'fullClosestCurrentPeers':selected,
 'currentGuardRows':{'currentTargetBeforeCard':{'id':TASK['id'],'topicId':TASK['topicId'],'sourceOrder':35,'card':before,'sha256':sha(before)}},
 'bilateralCurrentComparisons':comparisons,'globalLiteralRetrievalOnlyHits':list(hits.values()),
 'genuineProposalPairs':[],'observedNonmatchingProposals':[],
 'proposalSearchLimitations':'No other semantic author proposals were assigned for comparison in this directed cycle; current inventory covers 11,000 MAIN prompt/answer rows.',
 'limitations':['Literal global retrieval includes this target and close different systems (Mansabdar, Chinese exams); no exact cross-topic Table-of-Ranks duplicate was found.','The 100 actualCurrentPeers list includes the target as a current-card guard row, but it is excluded from peer comparison counts.'],
 'actualCurrentPeers':actual_peers,'identityVerification':identity,
 'previousInitialPeerSnapshot':str(PREVIOUS_PEERS.relative_to(C))
}

for name,data in [('candidate.json',candidate),('sourceproof.json',sourceproof),('peer-snapshot.json',peer_snapshot)]:
 (OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'beforeHash':sha(before),'afterHash':sha(proposed),'status':entry['status'],'frozen':{k:proposed[k] for k in ('id','difficulty','correctIndex')},'fieldGroups':list(field_groups),'fullTopicCards':len(actual_peers),'globalMAINRows':len(rows),'bilateralComparisons':len(comparisons),'retrievalHits':list(hits),'newSourceCalls':0,'qualityCredit':0},ensure_ascii=False,indent=2))
