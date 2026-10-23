import copy, hashlib, json, pathlib

C = pathlib.Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle')
OUT = C / 'docs/content-audits/question-quality-wave-8/coordinator-01a16a9a/source-human-medicine81'
TOPIC = C / 'src/content/topics/human-medicine.json'
INV = OUT / 'fresh-inventory.json'
SOURCE_INDEX = C / 'docs/content-audits/question-quality-wave-8/coordinator-01a166df/qualified-source-human-medicine28/sourceproof.json'
SOURCE_RAW = C / 'docs/content-audits/question-quality-wave-8/coordinator-01a166df/source-human-medicine28/raw-openstax-12-2.json'
NATIVE = '01a16ab5-a57c-7840-8e89-ccbe54378318'
ID = 'human-medicine-ext-neuron-branch'
TOPIC_ID = 'human-medicine'
CYCLE = 0
EXPECTED_BEFORE = '209e957a99a9326589b10f2367d6d317c7e02e6fadc11284928fcb4fa24f88b5'
SOURCE_PATH = str(SOURCE_RAW.relative_to(C))
URL = 'https://openstax.org/books/anatomy-and-physiology-2e/pages/12-2-nervous-tissue'


def canonical_sha(value):
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')
    return hashlib.sha256(raw).hexdigest()


def file_sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


topic = json.loads(TOPIC.read_text(encoding='utf-8'))
position = next(i for i, q in enumerate(topic['questions'], 1) if q['id'] == ID)
assert position == 81
before = copy.deepcopy(topic['questions'][position - 1])
assert before['topicId'] == TOPIC_ID if 'topicId' in before else True
before_sha = canonical_sha(before)
assert before_sha == EXPECTED_BEFORE, (before_sha, EXPECTED_BEFORE)

proposed = copy.deepcopy(before)
proposed['prompt'] = 'Как называется отросток нейрона, который проводит импульс от тела клетки к клеткам-мишеням?'
proposed['answers'] = [
    {'text': 'Аксон', 'note': 'У большинства нейронов аксон один, но он может ветвиться и передавать сигнал многим клеткам-мишеням.'},
    {'text': 'Дендрит', 'note': 'Дендриты обычно сильно ветвятся и принимают сигналы от других нейронов в местах синаптического контакта.'},
    {'text': 'Тело клетки (сома)', 'note': 'Тело нейрона содержит ядро и большую часть основных органелл клетки.'},
    {'text': 'Синапс', 'note': 'Синапс — контактная область, где окончание аксона взаимодействует с другой клеткой, например дендритом нейрона.'},
]
proposed['correctIndex'] = 0
proposed['explanation'] = 'Аксон выходит из тела нейрона и проводит нервный импульс к клеткам-мишеням. Дендриты, напротив, принимают сигналы от других нейронов.'
proposed['source'] = {
    'title': 'OpenStax Anatomy and Physiology 2e: 12.2 Nervous Tissue',
    'url': URL,
    'verifiedAt': '2026-10-24',
}

source_index = json.loads(SOURCE_INDEX.read_text(encoding='utf-8'))
source_raw_entry = next(s for s in source_index['rawSources'] if s['path'].endswith('raw-openstax-12-2.json'))
assert source_raw_entry['url'] == URL
assert source_raw_entry['sha256'] == file_sha(SOURCE_RAW)
raw_container = json.loads(SOURCE_RAW.read_text(encoding='utf-8'))
raw_text = raw_container['originalRecord']['payload']['output'][1]['text']
body_sha = hashlib.sha256(raw_text.encode('utf-8')).hexdigest()
assert source_raw_entry['completeOutputSHA256'] == body_sha
assert raw_container['sourceNativeId'] == '01a166f4-2c48-7ae0-815f-285f91f5a40c'

# Human-authored claim grounds are recorded separately from mechanically produced hashes.
grounds = {
    'prompt_ordered_answers_key': (
        'OpenStax L37 identifies the axon as a process emerging from the cell body and projecting to target cells; '
        'L38 says it propagates the nerve impulse, while dendrites receive information. This directly supports the key '
        'and distinguishes the nearest distractor. All choices name parts/structures of a neuron or its signaling contact.'),
    'explanation': (
        'OpenStax L37-L39 states that the axon emerges from the cell body and propagates impulses toward target cells, '
        'while dendrites receive information and flow is described from dendrites across the cell body down the axon.'),
    'note0': (
        'OpenStax L37 says neurons are usually described as having one axon; L38 says that axon may branch repeatedly '
        'to communicate with many target cells. This is an additional fact about the correct option beyond the prompt/key.'),
    'note1': (
        'OpenStax L38 says dendrites are usually highly branched and receive information from other neurons at synapses.'),
    'note2': (
        'OpenStax L37 says the soma/cell body contains the nucleus and most major organelles.'),
    'note3': (
        'OpenStax L38-L42 describes synapses as specialized contact areas and each connection between an axon branch '
        'and a dendrite as a synapse.'),
}
locators = {
    'prompt_ordered_answers_key': 'OpenStax 12.2 L37-L39.',
    'explanation': 'OpenStax 12.2 L37-L39.',
    'note0': 'OpenStax 12.2 L37-L38.',
    'note1': 'OpenStax 12.2 L38.',
    'note2': 'OpenStax 12.2 L37.',
    'note3': 'OpenStax 12.2 L38-L42.',
}

def group_values(card):
    return {
        'prompt_ordered_answers_key': {
            'prompt': card['prompt'],
            'answers': [a['text'] for a in card['answers']],
            'correctIndex': card['correctIndex'],
        },
        'explanation': card['explanation'],
        **{'note' + str(i): a['note'] for i, a in enumerate(card['answers'])},
    }

before_groups = group_values(before)
after_groups = group_values(proposed)
field_groups = {
    name: {
        'beforeCanonicalSHA256': canonical_sha(before_groups[name]),
        'afterCanonicalSHA256': canonical_sha(after_groups[name]),
    }
    for name in before_groups
}
assert len(field_groups) == 6
candidate = {
    'sourceNativeId': NATIVE,
    'topicId': TOPIC_ID,
    'cycle': CYCLE,
    'entries': [{
        'id': ID,
        'topicId': TOPIC_ID,
        'sourceOrder': 81,
        'status': 'READY_FOR_INDEPENDENT_REVIEW',
        'beforeCard': before,
        'beforeHash': before_sha,
        'proposedCard': proposed,
        'afterHash': canonical_sha(proposed),
        'fieldGroups': field_groups,
    }],
    'qualityCredit': 0,
}

assessments_text = [
    'Грамматика: вопрос «Как называется отросток…?» согласуется с краткими названиями частей нейрона; все четыре варианта относятся к нейронным структурам, а не к разным органам. Правдоподобие: дендрит — ближайший функциональный дистрактор, тело клетки и синапс — другие соседние структуры нейрона. Единственный ключ — аксон: источник связывает его с проведением импульса от тела к клеткам-мишеням. Справка верна и добавляет факт о ветвлении аксона и нескольких клетках-мишенях.',
    'Грамматика: «Как называется отросток…?» допускает название части нейрона в именительном падеже. Правдоподобие: дендрит — отросток того же нейрона, но источник говорит, что он принимает сигналы; импульс к клеткам-мишеням проводит аксон. Справка точно сообщает, что дендриты обычно сильно ветвятся и принимают информацию от других нейронов в синапсах.',
    'Грамматика: «тело клетки (сома)» — согласованное название структуры нейрона. Правдоподобие ниже, чем у дендрита, но это близкая часть клетки, а не посторонний орган; она не является отростком, который проводит сигнал к мишеням. Источник подтверждает, что тело клетки содержит ядро и большинство основных органелл; справка полезно определяет эту структуру.',
    'Грамматика: «синапс» — корректное название структуры, связанной с передачей сигнала между клетками. Он тематически правдоподобен, но обозначает контакт, а не отросток, проводящий импульс от тела нейрона. Источник описывает синаптический контакт аксона с дендритом; справка сообщает именно этот факт о варианте.',
]
variants = []
for i, answer in enumerate(proposed['answers']):
    triple = {'prompt': proposed['prompt'], 'answer': answer['text'], 'note': answer['note']}
    variants.append({
        'slot': i,
        'fullPrompt': proposed['prompt'],
        'answer': answer['text'],
        'note': answer['note'],
        'grammar': assessments_text[i].split(' Правдоподобие:')[0].replace('Грамматика: ', ''),
        'plausibilityUniqueKeyAndNoteTruthUsefulness': assessments_text[i],
        'sourcePaths': [SOURCE_PATH],
        'locator': locators['note' + str(i)] + ' Prompt/key: ' + locators['prompt_ordered_answers_key'],
        'tripleSHA256': canonical_sha(triple),
    })

literal_groups = []
for name, literal in after_groups.items():
    literal_groups.append({
        'group': name,
        'literal': literal,
        'literalSHA256': canonical_sha(literal),
        'primaryGround': grounds[name],
        'sourcePaths': [SOURCE_PATH],
        'locator': locators[name],
    })

raw_source = {
    'path': SOURCE_PATH,
    'url': URL,
    'sha256': file_sha(SOURCE_RAW),
    'captureReadProvenance': (
        'Reused immutable retained original complete web.open response from the qualified SOURCE28 source index. '
        'This author personally read the full returned primary context L0-L177 on 2026-10-24; no network call or refetch. '
        'Original web call belongs to native 01a166f4-2c48-7ae0-815f-285f91f5a40c, record line 254.'),
    'completeOutputPointer': '/originalRecord/payload/output/1/text',
    'completeOutputSHA256': body_sha,
    'locator': 'OpenStax Anatomy and Physiology 2e, section 12.2; exact claims are localized per literal group and answer variant.',
    'sourceCaptureNativeId': raw_container['sourceNativeId'],
}
sourceproof = {
    'sourceNativeId': NATIVE,
    'topicId': TOPIC_ID,
    'cycle': CYCLE,
    'id': ID,
    'rawSources': [raw_source],
    'entries': [{
        'id': ID,
        'topicId': TOPIC_ID,
        'sourceOrder': 81,
        'status': 'READY_FOR_INDEPENDENT_REVIEW',
        'literalGroups': literal_groups,
        'fourFullPromptAnswerNoteAssessments': variants,
        'correctNoteNewFact': {
            'fact': 'У большинства нейронов аксон обычно один; он может ветвиться и передавать сигнал многим клеткам-мишеням.',
            'sourcePaths': [SOURCE_PATH],
            'locator': 'OpenStax 12.2 L37-L38.',
        },
        'absoluteDifficulty': (
            'MEDIUM preserved: the question tests the foundational but topic-specific distinction between the axon, '
            'which conducts impulses toward target cells, and neighboring neuron structures such as dendrites. '
            'A player familiar with basic human biology can likely answer; a general adult without that familiarity '
            'cannot rely on broad everyday knowledge alone. The four choices are comparable neuron/signaling structures, '
            'and the nearest distractor is plausible but contradicted by its direction/function.'),
        'topicFit': 'The tested structure and its role in neuronal signaling belong directly to human medicine/anatomy.',
    }],
    'qualityCredit': 0,
    'networkCalls': 0,
    'sourceReuseDecision': 'The exact primary claim is fully covered by the saved OpenStax 12.2 body; no new source attempt was needed.',
}

inventory = json.loads(INV.read_text(encoding='utf-8'))
assert inventory['globalMAIN']['topicFileCount'] == 110 and inventory['globalMAIN']['questionCount'] == 11000
assert len(inventory['actualCurrentPeers']) == 100
peer_by_id = {p['id']: p for p in inventory['actualCurrentPeers']}
main_rows = {r['id']: r for r in inventory['globalMAIN']['rows']}
relevant_ids = [
    'human-medicine-cranial-nerve-pairs',
    'human-medicine-purkinje-fibers',
    'human-medicine-cns-myelin-cell',
    'human-medicine-ext-balance-ear',
    'human-medicine-ext-vision-receptors',
    'human-medicine-ext-heart-pacemaker',
    'human-medicine-ext-control-brain',
    'human-medicine-ext-synapse-junction',
]
assert all(x in peer_by_id for x in relevant_ids)
peer_assessments = {
    'human-medicine-cranial-nerve-pairs': 'Bilateral MAIN ERVC: that card tests the count of paired cranial nerves (entity=cranial-nerve set; relation=count; value=12; context=human anatomy). This proposal tests one neuron process and its signal direction. Neither card asks the other relation; direct reverse check is negative.',
    'human-medicine-purkinje-fibers': 'Bilateral MAIN ERVC: that card tests what cardiac Purkinje fibers do in ventricular myocardium (entity=cardiac conduction fibers; relation=transmit excitation to ventricular muscle; context=heart). This proposal tests axon identity in a neuron (entity=axon; relation=conduct impulse from soma to targets; context=nervous tissue). Different entity, relation, value and context; direct reverse check is negative.',
    'human-medicine-cns-myelin-cell': 'Bilateral MAIN ERVC: that card tests which CNS glial cell myelinates axons (entity=oligodendrocyte; relation=provide myelin; value=CNS axons; context=glia). This proposal tests what an axon is/function of the axon (entity=axon; relation=conduct impulse from cell body to targets). The shared word axon is contextual only; neither is a rephrasing or reverse of the other.',
    'human-medicine-ext-balance-ear': 'Bilateral MAIN ERVC: that card tests which inner-ear structures register rotational head movement (entity=semicircular canals; relation=detect rotation; context=vestibular system). This proposal tests neuronal axon anatomy and signal direction. Different entities and relations; direct reverse check is negative.',
    'human-medicine-ext-vision-receptors': 'Bilateral MAIN ERVC: that card tests where rods and cones are located (entity=photoreceptors; relation=location; value=retina; context=vision). Its note mentions signals through the optic nerve, but the tested relation is photoreceptor location. This proposal tests the axon as a neuron process; no direct/reverse duplicate.',
    'human-medicine-ext-heart-pacemaker': 'Bilateral MAIN ERVC: that card tests which cardiac structure usually sets heart rhythm (entity=sinoatrial node; relation=pace cardiac rhythm; context=heart). This proposal concerns a neuronal process, not cardiac conduction; direct reverse check is negative.',
    'human-medicine-ext-control-brain': 'Bilateral MAIN ERVC: that card tests the organ managing nervous-system function and sensory processing (entity=brain; relation=control/process; context=organ-level). This proposal tests a neuron substructure and impulse direction (cell-level). Different granularity and relation; no direct/reverse duplicate.',
    'human-medicine-ext-synapse-junction': 'Bilateral MAIN ERVC: that card tests the name of the contact where a signal passes between a neuron and another cell (entity=synapse; relation=intercellular contact/transmission; context=cell junction). This proposal tests the axon as the conducting process; synapse is only a plausible wrong option and has its own note. The relation/value differ and direct reverse check is negative.',
}
proposed_pairs = []
for peer_id in relevant_ids:
    peer = peer_by_id[peer_id]
    proposed_pairs.append({
        'topicId': peer['topicId'],
        'id': peer['id'],
        'sourceOrder': peer['sourceOrder'],
        'actualCurrentCard': copy.deepcopy(peer['card']),
        'actualCurrentCardCanonicalSHA256': peer['sha256'],
        'proposedCard': copy.deepcopy(proposed),
        'proposedCardCanonicalSHA256': canonical_sha(proposed),
        'bilateralMainAssessment': peer_assessments[peer_id],
    })

# Broad substring retrieval can surface Saxony/Synapsid false positives; exact semantic review found none cross-topic.
false_positive_ids = [
    'biology-sister-group',
    'dinosaurs-paleontology-diapsid-two-openings',
    'dinosaurs-paleontology-synapsid-one-opening',
    'dinosaurs-paleontology-anapsid-no-opening',
]
false_positive_rows = [copy.deepcopy(main_rows[x]) for x in false_positive_ids]
peer_snapshot = {
    'sourceNativeId': NATIVE,
    'topicId': TOPIC_ID,
    'cycle': CYCLE,
    'id': ID,
    'freshInventoryPath': str(INV),
    'globalMAIN': copy.deepcopy(inventory['globalMAIN']),
    'actualCurrentPeers': copy.deepcopy(inventory['actualCurrentPeers']),
    'selfBindingNote': 'The assigned card is included only as its actual CURRENT preimage binding; it is not counted as a distinct peer.',
    'sameTopicRelevantPairs': proposed_pairs,
    'crossTopicSemanticPeerAssessment': {
        'relevantPeers': [],
        'method': 'Reviewed the complete current MAIN prompt/answer rows for exact neuron, axon, dendrite, nerve-impulse and neuron-process terminology, then checked entity-relation-value-context and direct reverse against the candidate.',
        'lexicalFalsePositives': [
            {'row': row, 'reason': 'The apparent match is a substring/lexical lookalike (phylogenetic branch or synapsid skull classification), not a neuron/process or signal-direction relation.'}
            for row in false_positive_rows
        ],
        'directReverseFound': False,
    },
    'qualityCredit': 0,
}

dump(OUT / 'candidate.json', candidate)
dump(OUT / 'sourceproof.json', sourceproof)
dump(OUT / 'peer-snapshot.json', peer_snapshot)
print(json.dumps({
    'outputDirectory': str(OUT),
    'candidate': str(OUT / 'candidate.json'),
    'sourceproof': str(OUT / 'sourceproof.json'),
    'peerSnapshot': str(OUT / 'peer-snapshot.json'),
    'beforeHash': before_sha,
    'afterHash': canonical_sha(proposed),
    'sourceFileSHA256': raw_source['sha256'],
    'sourceBodySHA256': body_sha,
    'topicCards': 100,
    'globalMAINRows': 11000,
    'relevantSameTopicPeers': len(proposed_pairs),
    'crossTopicSemanticPeers': 0,
    'qualityCredit': 0,
}, ensure_ascii=False))
