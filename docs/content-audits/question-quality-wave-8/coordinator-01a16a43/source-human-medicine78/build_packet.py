import copy, hashlib, json, pathlib

C = pathlib.Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle')
OUT = C / 'docs/content-audits/question-quality-wave-8/coordinator-01a16a43/source-human-medicine78'
INV = OUT / 'fresh-inventory.json'
NATIVE = '01a16a76-4a35-7b81-94e8-0204db5d83ca'
TOPIC = 'human-medicine'
QID = 'human-medicine-ext-digestion-stomach'
CYCLE = 0

def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')
def sha(value):
    return hashlib.sha256(canonical(value)).hexdigest()
def file_sha(path):
    return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()
def write(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

data = json.loads(INV.read_text())
current_questions = data['sameTopicMAIN']['questions']
source_order = next(i for i, q in enumerate(current_questions, 1) if q['id'] == QID)
before = copy.deepcopy(current_questions[source_order - 1])
assert sha(before) == '5248ddf2fc0573bd8c8b1a24f095954036959b8ef4380f455ce5b87c08b2bf5b'
assert before['id'] == QID and before['correctIndex'] == 2

proposed = copy.deepcopy(before)
proposed['prompt'] = 'В каком органе пищеварительного тракта пища перемешивается с кислым соком и начинается переваривание белков?'
proposed['answers'] = [
    {'text': 'Пищевод', 'note': 'Пищевод соединяет глотку с желудком; перистальтические волны продвигают по нему пищевой комок.'},
    {'text': 'Печень', 'note': 'Печень вырабатывает желчь, которая помогает эмульгировать жиры в тонкой кишке.'},
    {'text': 'Желудок', 'note': 'Желудок вырабатывает внутренний фактор, необходимый для всасывания витамина B12 в тонкой кишке.'},
    {'text': 'Поджелудочная железа', 'note': 'Поджелудочная железа выделяет в двенадцатиперстную кишку сок с пищеварительными ферментами и бикарбонатом.'},
]
proposed['correctIndex'] = 2
proposed['explanation'] = 'Это происходит в желудке. Его сокращения перемешивают пищу с желудочным соком; соляная кислота активирует пепсин, и начинается расщепление белков.'
proposed['source'] = {
    'title': 'OpenStax Anatomy and Physiology 2e: The Stomach',
    'url': 'https://openstax.org/books/anatomy-and-physiology-2e/pages/23-4-the-stomach',
    'verifiedAt': '2026-10-24',
}

stomach = C / 'docs/content-audits/question-quality-wave-8/coordinator-01a16694/source-human-medicine24/raw/openstax-stomach.json'
esophagus = C / 'docs/content-audits/question-quality-wave-8/coordinator-01a1676a/source-human-medicine41/raw/openstax-pharynx-esophagus.json'
liver = C / 'docs/content-audits/question-quality-wave-8/coordinator-01a165b2/source-human-medicine1/raw/openstax-liver.json'
sources = [
    {
        'path': str(esophagus), 'url': 'https://openstax.org/books/anatomy-and-physiology-2e/pages/23-3-the-mouth-pharynx-and-esophagus',
        'sha256': file_sha(esophagus),
        'captureReadProvenance': 'Reused immutable retained original full web.open response from source-human-medicine41. Personally read the exact returned full primary context for this task; relevant esophagus passages L143-L159 and L163-L175; no refetch.',
        'completeOutputPointer': '/originalRecord/payload/output/1/text',
        'completeOutputSHA256': '17790d300c3071bc0b68bd1a13de5773b5e8a1a3c1e2d60f02550eb3168ab83a',
        'locator': 'OpenStax Anatomy and Physiology 2e 23.3, L143-L146: muscular tube from pharynx to stomach, peristalsis moves food toward stomach; L152-L159 summarizes esophageal functions.'
    },
    {
        'path': str(stomach), 'url': 'https://openstax.org/books/anatomy-and-physiology-2e/pages/23-4-the-stomach',
        'sha256': file_sha(stomach),
        'captureReadProvenance': 'Reused immutable retained original full web.open response from source-human-medicine24. Personally read the complete retained body and relevant primary context L31-L36, L46-L52, L102-L111 for this task; no refetch.',
        'completeOutputPointer': '/originalRecord/payload/output/1/text',
        'completeOutputSHA256': 'a2f07c90446272bf0cad6a09f55437dd419a13c636aea0acd7b506cf1ffa5e6c',
        'locator': 'OpenStax Anatomy and Physiology 2e 23.4, L31-L36 (location, mixing with digestive juices, digestion), L46-L52 (gastric glands, HCl, pepsin), L102-L111 (mixing waves and initial protein digestion; intrinsic factor and B12).'
    },
    {
        'path': str(liver), 'url': 'https://openstax.org/books/anatomy-and-physiology-2e/pages/23-6-accessory-organs-in-digestion-the-liver-pancreas-and-gallbladder',
        'sha256': file_sha(liver),
        'captureReadProvenance': 'Reused immutable retained original full web.open response from source-human-medicine1. Personally read the full retained primary context for this task; relevant liver and pancreas passages L31-L35, L52-L55, L64-L75; no refetch.',
        'completeOutputPointer': '/originalRecord/payload/output/1/text',
        'completeOutputSHA256': 'ff19584103354dc6f48b4fa004859bb9a23359e6fdb6cc3e74b136e023407edc',
        'locator': 'OpenStax Anatomy and Physiology 2e 23.6, L31-L35 (liver bile production and pancreas digestive juice), L52-L55 (bile emulsifies lipids), L64-L75 (pancreatic enzymes, bicarbonate, delivery to duodenum).'
    },
]
source_by_path = {s['path']: s for s in sources}
sp = [s['path'] for s in sources]

# The exact values that are hashed here are also written into candidate.json.
def groups(card):
    return {
        'prompt_ordered_answers_key': {'prompt': card['prompt'], 'answers': [a['text'] for a in card['answers']], 'correctIndex': card['correctIndex']},
        'explanation': card['explanation'],
        **{'note' + str(i): a['note'] for i, a in enumerate(card['answers'])},
    }

before_groups, after_groups = groups(before), groups(proposed)
field_groups = {name: {'beforeCanonicalSHA256': sha(before_groups[name]), 'afterCanonicalSHA256': sha(after_groups[name])} for name in before_groups}
candidate = {
    'sourceNativeId': NATIVE, 'topicId': TOPIC, 'cycle': CYCLE,
    'entries': [{
        'id': QID, 'topicId': TOPIC, 'sourceOrder': source_order, 'status': 'READY_FOR_INDEPENDENT_REVIEW',
        'beforeCard': before, 'beforeHash': sha(before), 'proposedCard': proposed, 'afterHash': sha(proposed),
        'fieldGroups': field_groups,
    }],
    'qualityCredit': 0,
}
write('candidate.json', candidate)

literal_ground = {
    'prompt_ordered_answers_key': {
        'primaryGround': 'OpenStax 23.4 directly states that food is mixed with gastric juices (L35), acid activates pepsin (L50-L52), and HCl plus pepsin begin protein breakdown in the stomach (L110). Section 23.3 identifies the esophagus as a transit tube (L143-L159); 23.6 distinguishes liver bile and pancreatic juice roles (L31-L35, L52-L55, L64-L75). Those contrasts make the stomach the unique key. The frozen numeric index 2 is preserved from assignment; it is not treated as evidence.',
        'sourcePaths': sp,
        'locator': 'OpenStax 23.4 L31-L36,L46-L52,L102-L110; 23.3 L143-L159; 23.6 L31-L35,L52-L55,L64-L75.'
    },
    'explanation': {
        'primaryGround': 'Mixing waves soften and mix food with gastric juice (23.4 L102); HCl and pepsin start protein breakdown (L50-L52,L110). The explanation states this and names the stomach.',
        'sourcePaths': [str(stomach)], 'locator': 'OpenStax 23.4 L50-L52,L102,L110.'
    },
    'note0': {'primaryGround': 'The esophagus connects the pharynx to the stomach and peristalsis propels the food bolus toward it.', 'sourcePaths': [str(esophagus)], 'locator': 'OpenStax 23.3 L143-L146,L152-L159.'},
    'note1': {'primaryGround': 'The liver produces bile; bile emulsifies lipids in the small intestine.', 'sourcePaths': [str(liver)], 'locator': 'OpenStax 23.6 L31-L35,L52-L55.'},
    'note2': {'primaryGround': 'Parietal cells in the stomach produce intrinsic factor, necessary for vitamin B12 absorption in the small intestine; this is a useful own-option fact beyond the prompt/key.', 'sourcePaths': [str(stomach)], 'locator': 'OpenStax 23.4 L50-L51.'},
    'note3': {'primaryGround': 'The pancreas delivers enzyme-containing pancreatic juice with bicarbonate to the duodenum; the buffer counters acidic chyme.', 'sourcePaths': [str(liver)], 'locator': 'OpenStax 23.6 L31,L64-L75.'},
}
entries = []
for name, literal in after_groups.items():
    g = literal_ground[name]
    entries.append({'group': name, 'literal': literal, 'literalSHA256': sha(literal), 'primaryGround': g['primaryGround'], 'sourcePaths': g['sourcePaths'], 'locator': g['locator']})
assessment_text = [
    'Грамматика: после «Выберите орган» все варианты стоят в именительном падеже и являются названиями органов пищеварения. Правдоподобие: пищевод проводит пищу, печень и поджелудочная железа участвуют в пищеварении, желудок выполняет названное сочетание функций. Уникальный ключ — желудок: только там пища смешивается с кислым желудочным соком и начинается расщепление белков; другие органы выполняют отличные функции. Справка точно описывает пищевод и его перистальтический транспорт.',
    'Грамматика: все названия органов согласуются с «Выберите орган». Правдоподобие: печень — орган пищеварения, но её основная указанная здесь роль связана с желчью, не с перемешиванием пищи с кислым соком. Уникальный ключ остаётся желудком. Справка сообщает конкретный факт о печени и эмульгировании жиров.',
    'Грамматика: название органа в именительном падеже подходит конструкции. Правдоподобие: желудок прямо выполняет описанное действие; контекст и точные функции отличают его от соседних пищеварительных органов. Уникальный ключ подтверждён первичным текстом о mixing waves, кислоте и пепсине. Справка сообщает отдельный полезный факт о внутреннем факторе и B12, не повторяя prompt/key.',
    'Грамматика: составное название органа корректно стоит после «Выберите орган». Правдоподобие: поджелудочная железа поставляет пищеварительные ферменты в кишечник, поэтому это содержательный дистрактор; однако она не смешивает пищу с кислым желудочным соком, и ключ остаётся единственным. Справка конкретно сообщает о панкреатическом соке и его бикарбонате.',
]
variant_paths = [[str(esophagus), str(stomach)], [str(liver), str(stomach)], [str(stomach), str(liver)], [str(liver), str(stomach)]]
variant_locators = [
    'OpenStax 23.3 L143-L159; contrast 23.4 L31-L35,L102-L110.',
    'OpenStax 23.6 L31-L35,L52-L55; contrast 23.4 L50-L52,L102-L110.',
    'OpenStax 23.4 L31-L36,L46-L52,L102-L111; contrast 23.3 L143-L159 and 23.6 L31-L35,L64-L75.',
    'OpenStax 23.6 L31,L64-L75; contrast 23.4 L50-L52,L102-L110.',
]
variants = []
for i, (a, assess) in enumerate(zip(proposed['answers'], assessment_text)):
    triple = {'prompt': proposed['prompt'], 'answer': a['text'], 'note': a['note']}
    variants.append({'slot': i, 'fullPrompt': proposed['prompt'], 'answer': a['text'], 'note': a['note'], 'grammar': assess.split(' Правдоподобие:')[0].replace('Грамматика: ', ''), 'plausibilityUniqueKeyAndNoteTruthUsefulness': assess, 'sourcePaths': variant_paths[i], 'locator': variant_locators[i], 'tripleSHA256': sha(triple)})
sourceproof = {
    'sourceNativeId': NATIVE, 'topicId': TOPIC, 'cycle': CYCLE, 'id': QID,
    'rawSources': sources,
    'entries': [{
        'id': QID, 'topicId': TOPIC, 'sourceOrder': source_order, 'status': 'READY_FOR_INDEPENDENT_REVIEW',
        'literalGroups': entries, 'fourFullPromptAnswerNoteAssessments': variants,
        'correctNoteNewFact': 'Желудок производит внутренний фактор, без которого нарушается всасывание витамина B12; это факт о самом варианте «Желудок», отсутствующий в prompt/key. OpenStax 23.4 L50-L51.',
        'absoluteDifficulty': 'EASY preserved: identifying the stomach as the familiar organ where food mixes with acidic gastric juice and protein digestion begins is broad adult knowledge, not a specialist or multi-step fact. The four alternatives are comparable digestive organs with distinct familiar roles; the key is not given away by answer style or a named organ in the prompt.',
        'topicFit': 'The tested relation is a basic human digestive function and fits the approved human-medicine topic directly.',
    }],
    'qualityCredit': 0,
}
write('sourceproof.json', sourceproof)

peer_ids = [
    'human-medicine-kidney-main-function', 'human-medicine-insulin-cells', 'human-medicine-bile-production',
    'human-medicine-intrinsic-factor', 'human-medicine-hepatic-portal-vein', 'human-medicine-stomach-system',
    'human-medicine-small-intestine-absorption', 'human-medicine-large-intestine-water',
    'human-medicine-ext-small-intestine-absorption', 'human-medicine-ext-insulin-organ',
    'human-medicine-ext-bile-storage', 'human-medicine-ext-large-intestine-water',
]
peer_cards = {q['id']: q for q in current_questions if q['id'] in peer_ids}
assert set(peer_cards) == set(peer_ids)
peer_analysis = {
    'human-medicine-kidney-main-function': ('Kidney main-function question; its option about protein digestion is a distractor, not the tested organ or process. Proposed item asks the stomach site where acidic gastric mixing and protein digestion begin. Same topic but no duplicate or reverse.', 'Proposed item does not ask what kidneys do; kidney card does not ask where gastric mixing/protein digestion begins. Entity and relation differ.'),
    'human-medicine-insulin-cells': ('This card asks which pancreatic cell produces insulin; proposed item asks where gastric mixing and initial protein digestion occur. Pancreas is not the key and the physiology is distinct.', 'Proposed item does not ask about endocrine cells or insulin; the insulin item does not ask about stomach digestion. No reverse relation.'),
    'human-medicine-bile-production': ('This card asks which organ synthesizes bile; proposed item asks where food is mixed with acidic juice and protein digestion begins. Liver is a plausible organ distractor with a distinct function.', 'Proposed item does not ask where bile is made; bile-production item does not ask where gastric digestion occurs.'),
    'human-medicine-intrinsic-factor': ('This card asks which gastric substance enables B12 absorption; proposed item asks for the organ and a different function. Shared stomach entity is not a duplicate fact.', 'Proposed item does not ask for intrinsic factor or B12; intrinsic-factor item does not ask for the stomach digestion site. No direct reverse.'),
    'human-medicine-hepatic-portal-vein': ('This card asks the direction/source of portal blood flow to liver; proposed item concerns gastric digestion. Both involve digestive anatomy but relations and values differ.', 'Proposed item does not ask about portal circulation; portal-vein item does not ask about gastric juice or protein digestion.'),
    'human-medicine-stomach-system': ('This card classifies the stomach as part of the digestive system; proposed item asks where acidic mixing and initial protein digestion occur. Same entity, different relation/value.', 'Proposed item does not ask which system contains stomach; classification item does not ask the stomach function.'),
    'human-medicine-small-intestine-absorption': ('This card asks where most nutrients are absorbed; proposed item asks where initial protein digestion begins. Digestive sequence is related, but absorption and gastric digestion are distinct relations and values.', 'Proposed item does not ask nutrient absorption; absorption item does not ask the location of initial protein digestion.'),
    'human-medicine-large-intestine-water': ('This card asks what the large intestine absorbs; proposed item asks about acid mixing and initial protein digestion in stomach. Distinct organ, function, and process.', 'Proposed item does not ask water/salt absorption; large-intestine item does not ask gastric digestion.'),
    'human-medicine-ext-small-intestine-absorption': ('This card asks where most nutrient absorption occurs; proposed item asks where initial protein digestion begins. Related digestive-tract sequence, but not the same fact. This assessment does not adopt or certify any prior status for either absorption card.', 'Proposed item does not ask absorption; the absorption card does not ask gastric mixing or protein digestion. No direct reverse.'),
    'human-medicine-ext-insulin-organ': ('This card asks which organ combines digestive-enzyme secretion and insulin secretion; proposed item asks the stomach site of acidic mixing and initial protein digestion. Pancreas is a plausible distractor but its secretions act in the intestine.', 'Proposed item does not ask which organ produces insulin and digestive enzymes; that item does not ask about stomach mixing. Distinct relation/value.'),
    'human-medicine-ext-bile-storage': ('This card asks which organ stores and concentrates bile; proposed item asks where acidic mixing and initial protein digestion occur. Gallbladder is a plausible digestive-organ distractor but does not perform the target function.', 'Proposed item does not ask about bile storage; the bile-storage item does not ask gastric digestion.'),
    'human-medicine-ext-large-intestine-water': ('This card asks which tract section absorbs water and forms feces; proposed item asks where acidic mixing and initial protein digestion begin. Distinct organ and relation. No status or prior judgment is imported.', 'Proposed item does not ask water absorption or feces formation; the large-intestine card does not ask gastric digestion.'),
}
actual_peers = [{'id': q['id'], 'topicId': TOPIC, 'sourceOrder': i, 'card': copy.deepcopy(q), 'sha256': sha(q)} for i,q in enumerate(current_questions,1)]
relevant = []
for qid in peer_ids:
    q = peer_cards[qid]
    order = next(i for i, x in enumerate(current_questions,1) if x['id'] == qid)
    a, b = peer_analysis[qid]
    relevant.append({'id': qid, 'topicId': TOPIC, 'sourceOrder': order, 'card': copy.deepcopy(q), 'sha256': sha(q), 'existingToProposedMAIN': a, 'proposedToExistingMAIN': b})

cross_defs = [
    ('agriculture','agriculture-17-1','This asks which animal is a ruminant based on repeated chewing and multi-chamber stomach; the proposed human card asks an organ function. Species, entity scope and relation differ.','The proposed card does not ask about rumination or animal stomach structure; the agriculture card does not ask where human food mixes with acid.'),
    ('agriculture','agriculture-17-2','This asks for the animal stomach type like a pig; the proposed card asks where human protein digestion begins. Monogastric classification is not the same relation.','The proposed card does not classify animal stomachs; the agriculture card does not ask about human gastric juice or protein digestion.'),
    ('agriculture','agriculture-17-3','This asks which farm animal uses a muscular gizzard; the proposed card concerns human stomach mixing. Species and function differ.','The proposed card does not ask which animal has a gizzard; the gizzard item does not ask about human gastric digestion.'),
    ('animals','animals-ruminant-rumen','This asks for the cow rumen chamber that hosts microbial fermentation; the proposed card asks where human food is mixed with acid and pepsin begins protein digestion. Same broad stomach theme, different species, structure and function.','The proposed card does not ask for a ruminant chamber; the rumen item does not ask the location of human gastric digestion. No direct reverse.'),
]
cross = []
for topic, qid, a, b in cross_defs:
    t = json.loads((C / f'src/content/topics/{topic}.json').read_text())
    q = next(x for x in t['questions'] if x['id'] == qid)
    order = next(i for i,x in enumerate(t['questions'],1) if x['id'] == qid)
    cross.append({'id':qid,'topicId':topic,'sourceOrder':order,'card':q,'sha256':sha(q),'existingToProposedMAIN':a,'proposedToExistingMAIN':b})

peer_snapshot = {
    'sourceNativeId': NATIVE, 'topicId': TOPIC, 'cycle': CYCLE,
    'globalMAIN': data['globalMAIN'],
    'sameTopicMAIN': data['sameTopicMAIN'],
    'actualCurrentPeers': actual_peers,
    'relevantSameTopicPeers': relevant,
    'relevantCrossTopicPeers': cross,
    'globalMAINSearchAssessment': {
        'query': 'Search current 11000 prompt/answer MAIN rows for stomach, gastric juice, initial protein digestion, acid, enzyme, and equivalent Russian terms; then inspect full current bodies for actual near peers.',
        'crossTopicResult': 'No exact/reverse MAIN match found. Closest cross-topic actual cards are the four full agriculture/animals peers above; they ask about non-human stomach structure or fermentation and differ by entity/relation/value/context. Other lexical hits concern generic enzyme definitions, plant/food fermentation, acidity, contrast agents or unrelated organ functions; no shared stomach digestion claim.',
        'sameTopicResult': 'Read full current cards listed in relevantSameTopicPeers. Nearby stomach-system classification, intrinsic-factor/B12, nutrient absorption, large-intestine absorption, pancreatic secretion/insulin, bile production/storage, portal circulation and kidney function have distinct MAIN relations. Existing 41/42/76 gut holds remain unchanged and are not qualified by this comparison.',
    },
    'proposedPairs': [],
    'inventoryBinding': {'path': str(INV), 'fileSHA256': file_sha(INV), 'globalMAINRowsCanonicalSHA256': data['globalMAIN']['rowsCanonicalSHA256'], 'sameTopicFileSHA256': data['sameTopicMAIN']['fileSHA256']},
    'qualityCredit': 0,
}
write('peer-snapshot.json', peer_snapshot)

# Deterministic author-side sanity checks only; this is not affected QA or independent review.
assert candidate['entries'][0]['beforeHash'] == '5248ddf2fc0573bd8c8b1a24f095954036959b8ef4380f455ce5b87c08b2bf5b'
assert candidate['entries'][0]['proposedCard']['difficulty'] == 'easy' and candidate['entries'][0]['proposedCard']['correctIndex'] == 2
assert len(proposed['answers']) == 4 and len(variants) == 4 and len(entries) == 6
assert len(proposed['explanation'].split()) <= 70 and 2 <= proposed['explanation'].count('.') <= 4
assert all(len(a['text'].encode('utf-16-le')) // 2 <= 140 for a in proposed['answers'])
assert all(len(a['note'].split()) <= 35 for a in proposed['answers'])
assert all(pathlib.Path(s['path']).exists() and file_sha(s['path']) == s['sha256'] for s in sources)
assert actual_peers[source_order - 1]['sha256'] == candidate['entries'][0]['beforeHash']
print(json.dumps({'candidate':str(OUT/'candidate.json'),'sourceproof':str(OUT/'sourceproof.json'),'peerSnapshot':str(OUT/'peer-snapshot.json'),'sourceOrder':source_order,'beforeHash':sha(before),'afterHash':sha(proposed),'relevantSameTopicPeers':len(relevant),'relevantCrossTopicPeers':len(cross),'globalMAINRows':len(data['globalMAIN']['rows']),'qualityCredit':0},ensure_ascii=False))
