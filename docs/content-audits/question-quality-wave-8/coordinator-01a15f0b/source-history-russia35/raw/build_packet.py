import hashlib, json, pathlib

ROOT = pathlib.Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle')
OUT = ROOT / 'docs/content-audits/question-quality-wave-8/coordinator-01a15f0b/source-history-russia35'
RAW = OUT / 'raw'
TASK = json.load(open(ROOT / 'docs/content-audits/question-quality-wave-8/coordinator-01a15f0b/source-history-russia35-task.json'))
INV = json.load(open(RAW / 'fresh-inventory.json'))
NATIVE = TASK['authorNativeId']
OWNER = TASK['owner']


def canonical_sha(value):
    b = json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')
    return hashlib.sha256(b).hexdigest()


def text_sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

actual = next(x for x in INV['actualCurrentPeers'] if x['id'] == TASK['id'])
before = actual['card']
assert canonical_sha(before) == TASK['beforeHash'] == actual['sha256']
proposed = json.loads(json.dumps(before, ensure_ascii=False))
proposed['prompt'] = 'Что упорядочивала введённая Петром I Табель о рангах?'
proposed['answers'] = [
    {'text': 'Только военные и гражданские чины', 'note': 'Военные и гражданские чины входили в Табель, но это не полный перечень: отдельно указывались и придворные чины.'},
    {'text': 'Только гражданские и придворные чины', 'note': 'Гражданские и придворные чины действительно были в Табели; военные составляли её третий вид чинов.'},
    {'text': 'Только военные и придворные чины', 'note': 'Военные и придворные чины входили в Табель; помимо них документ включал гражданские, или статские, чины.'},
    {'text': 'Военные, гражданские и придворные чины', 'note': 'Каждый из трёх видов службы делился на 14 классов: I класс был высшим, а XIV — низшим.'},
]
proposed['correctIndex'] = 3
proposed['explanation'] = 'Табель о рангах упорядочивала военные, гражданские (статские) и придворные чины. Каждый из этих трёх видов службы делился на 14 классов, а военные чины ставились выше соответствующих гражданских и придворных.'
proposed['source'] = {'title': 'Президентская библиотека имени Б. Н. Ельцина: «Петром I утверждена „Табель о рангах“»', 'url': 'https://www.prlib.ru/node/619004', 'verifiedAt': '2026-10-21'}
assert proposed['id'] == TASK['id'] and proposed['difficulty'] == 'medium' and proposed['correctIndex'] == 3
assert all(len(a['text'].encode('utf-16-le')) // 2 <= 140 for a in proposed['answers'])
assert all(len(a['note'].split()) <= 35 for a in proposed['answers'])
assert len(proposed['explanation'].split()) <= 70 and len(proposed['explanation'].split('. ')) in (2, 3, 4)

before_groups = {
    'prompt_ordered_answers_key': {'prompt': before['prompt'], 'answers': [a['text'] for a in before['answers']], 'correctIndex': before['correctIndex']},
    'explanation': before['explanation'],
    **{f'note{i}': before['answers'][i]['note'] for i in range(4)},
}
after_groups = {
    'prompt_ordered_answers_key': {'prompt': proposed['prompt'], 'answers': [a['text'] for a in proposed['answers']], 'correctIndex': proposed['correctIndex']},
    'explanation': proposed['explanation'],
    **{f'note{i}': proposed['answers'][i]['note'] for i in range(4)},
}
field_groups = {k: {'beforeCanonicalSHA256': canonical_sha(before_groups[k]), 'afterCanonicalSHA256': canonical_sha(after_groups[k])} for k in before_groups}

primary_file = RAW / 'prlib-tableofranks-primary.json'
alt_file = RAW / 'prlib-tableofranks-official-alternative.json'
primary = json.load(open(primary_file)); alternative = json.load(open(alt_file))
primary_rel = str(primary_file.relative_to(ROOT))
alt_rel = str(alt_file.relative_to(ROOT))
alt_locator = 'Президентская библиотека, «Петром I утверждена „Табель о рангах“», L44-L48; особенно L47-L48.'
raw_sources = [
    {
        'path': primary_rel,
        'url': primary['url'],
        'sha256': text_sha(primary_file),
        'completeOutputSHA256': primary['completeOutputSHA256'],
        'completeOutputPointer': primary['completeOutputPointer'],
        'captureReadProvenance': {
            'capturedAt': '2026-10-21', 'originalTool': 'tools.web__run',
            'nativeJournal': primary['nativeJournal'], 'nativeRecordLine': primary['nativeRecordLine'],
            'sourceNativeId': primary['sourceNativeId'], 'pageLocator': 'turn1view0 L43-L53',
            'personallyReadBy': NATIVE, 'readAt': '2026-10-21',
            'personallyReadFullRelevantContext': True,
            'personalReadCoverage': 'Лично прочитано полное возвращённое тело каталожной страницы. L43-L53 идентифицируют автора Петра I, печатное издание 1722 года и электронную копию РГБ; это метаданные первичного документа, не текст самого документа и не содержательное доказательство охвата службы.',
            'limitation': 'Метаданные записи не содержат полного текста/скана Табели.'
        }
    },
    {
        'path': alt_rel,
        'url': alternative['url'],
        'sha256': text_sha(alt_file),
        'completeOutputSHA256': alternative['completeOutputSHA256'],
        'completeOutputPointer': alternative['completeOutputPointer'],
        'captureReadProvenance': {
            'capturedAt': '2026-10-21', 'originalTool': 'tools.web__run',
            'nativeJournal': alternative['nativeJournal'], 'nativeRecordLine': alternative['nativeRecordLine'],
            'sourceNativeId': alternative['sourceNativeId'], 'pageLocator': 'turn3view0 L40-L54',
            'personallyReadBy': NATIVE, 'readAt': '2026-10-21',
            'personallyReadFullRelevantContext': True,
            'personalReadCoverage': 'Лично прочитан полный возвращённый текст страницы. L44 связывает Петра I, 1722 год и порядок государственной службы; L46 описывает содержание Табели; L47 прямо перечисляет военные, статские (гражданские) и придворные чины и 14 классов; L48 задаёт порядок классов и преимущество военных чинов.',
            'note': 'Официальная альтернативная страница Президентской библиотеки; использована после того, как первичная карточка оцифрованного издания вернула только каталоговые метаданные.'
        }
    }
]
source_paths = [alt_rel]

grounds = {
    'prompt_ordered_answers_key': ('Президентская библиотека датирует утверждение Табели Петром I 1722 годом и определяет её как закон о порядке государственной службы (L44). L47 перечисляет ровно три вида чинов: военные, статские (гражданские) и придворные. Три первых варианта содержат по два из этих трёх видов; только вариант 3 включает полный набор.', alt_locator),
    'explanation': ('Официальный текст страницы прямо называет три категории чинов (L47), деление каждого вида службы на 14 классов (L47) и ставит военные чины выше соответствующих гражданских и придворных (L48).', 'Президентская библиотека, L47-L48.'),
    'note0': ('В L47 военные и статские (гражданские) чины названы двумя видами; там же отдельно названы придворные чины, поэтому вариант неполон.', 'Президентская библиотека, L47.'),
    'note1': ('В L47 статские (гражданские) и придворные чины названы двумя видами; там же отдельно названы военные чины, поэтому вариант неполон.', 'Президентская библиотека, L47.'),
    'note2': ('В L47 военные и придворные чины названы видами Табели; там же отдельно названы статские (гражданские) чины, поэтому вариант неполон.', 'Президентская библиотека, L47.'),
    'note3': ('L47 сообщает, что каждый вид службы делился на 14 классов; L48 уточняет: первый был высшим, четырнадцатый — низшим.', 'Президентская библиотека, L47-L48.'),
}
literal_groups = []
for group, literal in after_groups.items():
    ground, locator = grounds[group]
    literal_groups.append({'group': group, 'literal': literal, 'literalSHA256': canonical_sha(literal), 'primaryGround': ground, 'locator': locator, 'sourcePaths': source_paths})

assessments = []
for i, answer in enumerate(proposed['answers']):
    assessments.append({
        'slot': i, 'fullPrompt': proposed['prompt'], 'answer': answer['text'], 'note': answer['note'],
        'grammar': 'Вопрос и варианты читаются как прямой ответ к «что упорядочивала»: однородные группы чинов стоят в винительном падеже, порядок перечисления и согласование параллельны.',
        'plausibilityUniqueKeyAndNoteTruthUsefulness': [
            'Реальный, но неполный набор двух категорий; сопоставим с остальными вариантами. Пропущены придворные чины, поэтому ключ уникален. Справка подтверждает две включённые категории и показывает, какой вид пропущен.',
            'Реальный, но неполный набор двух категорий; сопоставим с остальными вариантами. Пропущены военные чины, поэтому ключ уникален. Справка подтверждает две включённые категории и показывает, какой вид пропущен.',
            'Реальный, но неполный набор двух категорий; сопоставим с остальными вариантами. Пропущены статские чины, поэтому ключ уникален. Справка подтверждает две включённые категории и показывает, какой вид пропущен.',
            'Полный перечень трёх документированных категорий. Ни один другой вариант не содержит все виды; справка добавляет отдельный проверяемый факт о 14-классной структуре.'
        ][i],
        'sourcePaths': source_paths,
        'locator': 'Президентская библиотека, L44-L48; перечень категорий L47.' if i < 3 else 'Президентская библиотека, L47-L48.',
        'tripleSHA256': canonical_sha({'prompt': proposed['prompt'], 'answer': answer['text'], 'note': answer['note']})
    })

entry = {
    'id': TASK['id'], 'topicId': TASK['topicId'], 'sourceOrder': TASK['sourceOrder'],
    'status': 'READY_FOR_INDEPENDENT_REVIEW', 'beforeCard': before, 'beforeHash': canonical_sha(before),
    'proposedCard': proposed, 'afterHash': canonical_sha(proposed), 'fieldGroups': field_groups,
    'proposedCardCanonicalSHA256': canonical_sha(proposed)
}
candidate = {
    'owner': OWNER, 'sourceNativeId': NATIVE, 'stage': 'SOURCE35_AUTHOR_READY', 'cycle': 0,
    'qualityCredit': 0,
    'scope': {'id': TASK['id'], 'topicId': TASK['topicId'], 'sourceOrder': TASK['sourceOrder'], 'difficulty': 'medium', 'correctIndex': 3, 'baselineCode': TASK['baselineCode'], 'catalogCandidate': TASK['catalogCandidate']},
    'history': [{'stage': 'SOURCE35', 'status': 'READY_FOR_INDEPENDENT_REVIEW', 'note': 'Фиксированные поля сохранены; предложены уточнение ключевого охвата и правдоподобные полнотематические варианты с четырьмя справками.'}],
    'entries': [entry]
}

sourceproof_entry = {
    'id': TASK['id'], 'status': 'READY_FOR_INDEPENDENT_REVIEW', 'beforeHash': canonical_sha(before),
    'literalGroups': literal_groups, 'fourFullPromptAnswerNoteAssessments': assessments,
    'correctNoteNewFact': {
        'fact': 'Каждый из трёх видов службы в Табели делился на 14 классов; первый был высшим, четырнадцатый низшим. Это добавляет конкретный факт о структуре самой Табели сверх вопроса и ключевого перечня видов службы.',
        'sourcePaths': source_paths, 'locator': 'Президентская библиотека, L47-L48.'
    },
    'absoluteDifficulty': {
        'frozenLevel': 'medium',
        'audienceGround': 'Это тематический факт истории России: требуется знать состав Табели, а не только широкую общеизвестную биографию Петра I. Знакомый с темой игрок узнает полный перечень видов службы; частичные пары сохраняют правдоподобие для игрока вне темы. Нет специального расчёта или многошаговой логики.'
    }
}
sourceproof = {
    'owner': OWNER, 'sourceNativeId': NATIVE, 'stage': 'SOURCE35_AUTHOR_READY', 'cycle': 0, 'qualityCredit': 0,
    'rawSources': raw_sources,
    'sourceIndex': {
        'assignedSourceIndex': TASK['sourceIndex'],
        'additionalRetainedIndexesRead': TASK['additionalRetainedSourceIndexes'],
        'retainedRawSourceInventory': 'Targeted search across these indexes found no already-retained full primary Table of Ranks context. Existing AAP/Scandinavian/polar/source-attempt fences were preserved without retries.',
        'sourceAttemptDisposition': 'Primary URL opened once; it yielded only catalog metadata for the 1722 scanned document. One official alternative URL was opened once and returned a full relevant explanatory page. No retry/refetch/reset.'
    },
    'entries': [sourceproof_entry],
    'limitations': [
        'Первичная карточка оцифрованной Табели на Президентской библиотеке подтвердила автора/дату/издание, но возвращённое тело не содержало текста самого закона. Содержательные основания привязаны к одной полной официальной альтернативной странице Президентской библиотеки; это явно отражено в rawSources.',
        'Авторский READY не является независимым review, зачётом, применением или редакторским PASS.'
    ],
    'immutableFullOriginalToolOutputs': [
        {'path': primary_rel, 'sha256': text_sha(primary_file), 'jsonPointer': primary['completeOutputPointer']},
        {'path': alt_rel, 'sha256': text_sha(alt_file), 'jsonPointer': alternative['completeOutputPointer']}
    ],
    'mechanicalIntake': {'status': 'NOT_RUN', 'reason': 'Авторский SOURCE-пакет; intake, catalog и проверки находятся вне выданного ownership.'}
}
sourceproof['identityVerification'] = {
    'sourceNativeId': NATIVE,
    'nativeJournal': TASK['authorNativeJournal'],
    'sessionMetaRecordLine': 1,
    'verification': 'Лично проверено session_meta.payload.id == session_meta.payload.session_id == sourceNativeId; coordinator owner остаётся отдельным идентификатором.',
    'actualCompactionsObserved': 0
}
sourceproof['networkAttemptLedger'] = [
    {'kind': 'discovery', 'nativeCallLine': 112, 'nativeOutputLine': 115, 'callId': 'call_31bd9c5761744be8a7c49fefcd64fae2', 'resultRetention': 'Полный исходный multiquery результат находится в неизменённом nativeJournal; использован только для нахождения первичного URL, не как доказательство.'},
    {'kind': 'primary-open', 'nativeCallLine': 119, 'nativeOutputLine': 122, 'callId': 'call_680722c4524a48ef899c932368f936ae', 'url': primary['url'], 'capturedAt': primary_rel, 'disposition': 'Только каталожные метаданные; недостаточно как текст закона.'},
    {'kind': 'official-alternative-discovery', 'nativeCallLine': 142, 'nativeOutputLine': 145, 'callId': 'call_9e80cf06dacf417c9a3e45354025419e', 'resultRetention': 'Полный исходный multiquery результат находится в неизменённом nativeJournal; использован только для нахождения официальной альтернативы, не как доказательство.'},
    {'kind': 'official-alternative-open', 'nativeCallLine': 153, 'nativeOutputLine': 156, 'callId': 'call_afa37a48d05c4dd497ea344b3531226a', 'url': alternative['url'], 'capturedAt': alt_rel, 'disposition': 'Полный релевантный текст; использован как официальный альтернативный источник. Повторов не было.'}
]

# Build complete same-topic and global snapshots from the immutable fresh inventory.
source_files = {}
for f in (ROOT / 'src/content/topics').glob('*.json'):
    try:
        topic = json.load(open(f))
        for q in topic.get('questions', []): source_files[q['id']] = (f, topic, q)
    except Exception: pass

selected_same = {3, 19, 64, 66, 74, 96}
selected_global_ids = {'history-india-mansabdari', 'history-china-easy-04a-01', 'history-united-states-pendleton-reform', 'government-politics-civil-service'}
selected = []
for x in INV['actualCurrentPeers']:
    if x['sourceOrder'] in selected_same and x['id'] != TASK['id']:
        selected.append(dict(x))
for qid in selected_global_ids:
    if qid not in source_files: continue
    f, topic, q = source_files[qid]
    so = next((n for n, candidate_q in enumerate(topic['questions'], 1) if candidate_q['id'] == qid), None)
    selected.append({'id': qid, 'topicId': topic['id'], 'sourceOrder': so, 'card': q, 'sha256': canonical_sha(q), 'sourceFilePath': str(f.relative_to(ROOT)), 'sourceFileSHA256': text_sha(f)})

candidate_ervc = {'entity': 'Табель о рангах, утверждённая Петром I в 1722 году', 'relation': 'упорядочивала / систематизировала виды чинов', 'value': 'военные, статские (гражданские), придворные; по 14 классов каждого вида', 'context': 'Российская империя, 1722 год'}
peer_ervc = {
    'history-russia-peter-title': {'entity': 'Пётр I', 'relation': 'получил почётное прозвание', 'value': 'Великий', 'context': 'после победы в Северной войне'},
    'history-russia-peter-capital': {'entity': 'Санкт-Петербург', 'relation': 'стал столицей России', 'value': 'перенос столицы при Петре I', 'context': 'начало XVIII века'},
    'history-russia-senate-founder': {'entity': 'Правительствующий сенат', 'relation': 'учреждён кем', 'value': 'Пётр I', 'context': '1711 год'},
    'history-russia-ministries-founder': {'entity': 'российские министерства', 'relation': 'учреждены кем', 'value': 'Александр I', 'context': '1802 год'},
    'history-russia-supreme-privy-council': {'entity': 'Верховный тайный совет', 'relation': 'создан кем/когда', 'value': 'Екатерина I, 1726', 'context': 'послепетровский государственный орган'},
    'history-russia-state-council-reformer': {'entity': 'Государственный совет', 'relation': 'получил статус/устройство', 'value': 'высший законосовещательный орган при императоре', 'context': '1810 год, план М. Сперанского'},
    'history-india-mansabdari': {'entity': 'могольский мансаб', 'relation': 'обозначения двух числовых частей', 'value': 'зат — личный ранг; савар — число конных воинов', 'context': 'административно-военная система империи Великих Моголов'},
    'history-china-easy-04a-01': {'entity': 'государственные экзамены императорского Китая', 'relation': 'кого отбирали', 'value': 'кандидатов для государственной службы', 'context': 'императорский Китай'},
    'history-united-states-pendleton-reform': {'entity': 'Акт Пендлтона', 'relation': 'какую практику ввёл', 'value': 'конкурсный/меритократический набор на федеральную службу', 'context': 'США, 1883 год'},
    'government-politics-civil-service': {'entity': 'государственная гражданская служба', 'relation': 'что такое', 'value': 'профессиональный аппарат исполнения решений органов власти', 'context': 'общее понятие, современная государственная система'},
}
comparisons=[]
for peer in selected:
    qid=peer['id']; pe=peer_ervc.get(qid, {'entity': peer['card']['prompt'], 'relation': 'проверяемый факт peer-карточки', 'value': peer['card']['answers'][peer['card']['correctIndex']]['text'], 'context': peer['topicId']})
    comparisons.append({
        'kind': 'same-topic' if peer['topicId']==TASK['topicId'] else 'global-semantic-peer',
        'peerId': qid, 'peerFullCardSHA256': peer['sha256'],
        'candidateERVC': candidate_ervc, 'peerERVC': pe,
        'candidateToPeer': 'Не дубликат: у карточки и peer разные сущности, отношения и проверяемые значения; совпадение ограничено историческим/служебным контекстом или именем Петра I.',
        'peerToCandidate': 'Обратная проверка также различает факты: карточка о Табели не отвечает на вопрос peer и карточка peer не устанавливает категории или классы Табели.',
        'isDuplicate': False
    })

rows = INV['globalMAIN']['rows']
query_terms = ['табель о рангах', 'мансаб', 'государственные экзамены', 'государственной службы', 'чинопроизводство']
hits_by_id = {}
for term in query_terms:
    for row in rows:
        if term.lower() in json.dumps(row, ensure_ascii=False).lower():
            qid=row['id']
            if qid in source_files:
                f, topic, q=source_files[qid]
                so=next((n for n,v in enumerate(topic['questions'],1) if v['id']==qid),None)
                hits_by_id[qid]={'topicId':topic['id'],'sourceOrder':so,'id':qid,'card':q,'cardCanonicalSHA256':canonical_sha(q),'sourceFilePath':str(f.relative_to(ROOT)),'sourceFileSHA256':text_sha(f),'retrievalTerms':[]}
            else:
                hits_by_id.setdefault(qid, {'topicId':row['topicId'],'id':qid,'mainRow':row,'retrievalTerms':[]})
            hits_by_id[qid]['retrievalTerms'].append(term)

same_topic_peers = []
for x in INV['actualCurrentPeers']:
    same_topic_peers.append({'id':x['id'],'topicId':x['topicId'],'sourceOrder':x['sourceOrder'],'card':x['card'],'sha256':canonical_sha(x['card'])})
peer_snapshot = {
    'owner': OWNER, 'sourceNativeId': NATIVE, 'stage': 'SOURCE35_AUTHOR_READY', 'cycle': 0, 'qualityCredit': 0,
    'candidate': {'id': TASK['id'], 'topicId': TASK['topicId'], 'sourceOrder': TASK['sourceOrder'], 'beforeCard': before, 'beforeCardCanonicalSHA256': canonical_sha(before), 'proposedCard': proposed, 'proposedCardCanonicalSHA256': canonical_sha(proposed), 'frozen': TASK['frozen'], 'semanticEntity': candidate_ervc['entity'], 'semanticRelation': candidate_ervc['relation'], 'semanticValue': candidate_ervc['value']},
    'globalMAIN': {k:INV['globalMAIN'][k] for k in ('topicFileCount','questionCount','rowsCanonicalSHA256','allCurrentFileByteBindings')} | {'projectionShape':'Each row {topicId,id,prompt,answers:[four ordered texts],correctIndex}; excludes notes, explanation, source, sourceOrder.','readDate':'2026-10-21'},
    'sameTopicMAIN': INV['sameTopicMAIN'],
    'fullClosestCurrentPeers': selected,
    'currentGuardRows': {'currentTargetBeforeCard': {'id':TASK['id'],'topicId':TASK['topicId'],'sourceOrder':TASK['sourceOrder'],'card':before,'sha256':canonical_sha(before)}},
    'bilateralCurrentComparisons': comparisons,
    'globalLiteralRetrievalOnlyHits': list(hits_by_id.values()),
    'genuineProposalPairs': [],
    'observedNonmatchingProposals': [],
    'proposalSearchLimitations': 'No other simultaneous proposed author cards were assigned or searched; only this SOURCE35 candidate is in scope. The immutable global MAIN inventory contains 11,000 current prompt/answer rows.',
    'limitations': [
        'Exact phrase retrieval for «Табель о рангах» returns only this candidate in global MAIN. Cross-topic close concepts were checked as distinct systems/relations, not treated as duplicates.',
        'All 100 history-russia MAIN cards are retained in sameTopicMAIN and actualCurrentPeers; comparisons exclude this candidate from being counted as its own peer.'
    ],
    'actualCurrentPeers': same_topic_peers
}
peer_snapshot['identityVerification'] = sourceproof['identityVerification']
candidate['identityVerification'] = sourceproof['identityVerification']

for name, data in [('candidate.json', candidate), ('sourceproof.json', sourceproof), ('peer-snapshot.json', peer_snapshot)]:
    (OUT / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')

print(json.dumps({
    'candidate': str(OUT/'candidate.json'), 'sourceproof': str(OUT/'sourceproof.json'), 'peerSnapshot': str(OUT/'peer-snapshot.json'),
    'beforeHash': canonical_sha(before), 'afterHash': canonical_sha(proposed), 'groupNames': list(field_groups),
    'sourceRawHashes': {str(p.relative_to(ROOT)): text_sha(p) for p in (primary_file,alt_file)},
    'currentPeers': len(same_topic_peers), 'selectedRelevantPeers': len(selected), 'retrievalHits': list(hits_by_id), 'qualityCredit': 0
}, ensure_ascii=False, indent=2))
