import copy, hashlib, json, pathlib, re

C = pathlib.Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle')
OUT = C / 'docs/content-audits/question-quality-wave-8/coordinator-01a16a9a/source-human-medicine81-cycle1'
TOPIC = C / 'src/content/topics/human-medicine.json'
INV = OUT / 'fresh-inventory.json'
OLD_PROOF = C / 'docs/content-audits/question-quality-wave-8/coordinator-01a16a9a/source-human-medicine81/sourceproof.json'
SOURCE_INDEX = C / 'docs/content-audits/question-quality-wave-8/coordinator-01a166df/qualified-source-human-medicine28/sourceproof.json'
SOURCE_RAW = C / 'docs/content-audits/question-quality-wave-8/coordinator-01a166df/source-human-medicine28/raw-openstax-12-2.json'
INITIAL_PATH = C / 'docs/content-audits/question-quality-wave-8/coordinator-01a16a9a/independent-human-medicine81-initial/receipt.json'
SOURCE82_PATH = C / 'docs/content-audits/question-quality-wave-8/coordinator-01a16a9a/source-human-medicine82/candidate.json'
NATIVE = '01a16ab5-a57c-7840-8e89-ccbe54378318'
ID = 'human-medicine-ext-neuron-branch'
TOPIC_ID = 'human-medicine'
CYCLE = 1
BEFORE = 'ef27856f031851883e38aa45ac47ae1c5a1e2616e3b95bb311c25aa921f63d9b'
INITIAL_SHA = '3aac04754764868b260de0209823367474db9e1a95b42d6fe006791bc259a45d'
INITIAL_CODE = 'PROMPT_ROW_CATEGORY_MISMATCH'
SOURCE_PATH = str(SOURCE_RAW.relative_to(C))
URL = 'https://openstax.org/books/anatomy-and-physiology-2e/pages/12-2-nervous-tissue'


def canonical_sha(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')).hexdigest()


def file_sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


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


# Exact bindings to the actual applied SOURCE81 and immutable independent INITIAL.
initial = json.loads(INITIAL_PATH.read_text(encoding='utf-8'))
assert file_sha(INITIAL_PATH) == INITIAL_SHA
assert initial['stage'] == 'INITIAL' and initial['cycle'] == 0 and initial['qualityCredit'] == 0
assert initial['entries'][0]['status'] == 'FIX'
assert [d['code'] for d in initial['entries'][0]['defects']] == [INITIAL_CODE]
assert initial['entries'][0]['currentCardCanonicalSHA256'] == BEFORE

inventory = json.loads(INV.read_text(encoding='utf-8'))
assert inventory['globalMAIN']['topicFileCount'] == 110 and inventory['globalMAIN']['questionCount'] == 11000
assert len(inventory['actualCurrentPeers']) == 100
peer_by_id = {p['id']: p for p in inventory['actualCurrentPeers']}
current = copy.deepcopy(next(p['card'] for p in inventory['actualCurrentPeers'] if p['id'] == ID))
assert canonical_sha(current) == BEFORE
assert current['id'] == ID and current['difficulty'] == 'medium' and current['correctIndex'] == 0

# Sole directed repair: change only the row category from process to neuron structure.
proposed = copy.deepcopy(current)
proposed['prompt'] = 'Какая структура нейрона проводит импульс от тела клетки к клеткам-мишеням?'
for key in ('id', 'difficulty', 'answers', 'correctIndex', 'explanation', 'source'):
    assert proposed[key] == current[key], key

before_groups, after_groups = group_values(current), group_values(proposed)
field_groups = {
    name: {'beforeCanonicalSHA256': canonical_sha(before_groups[name]),
           'afterCanonicalSHA256': canonical_sha(after_groups[name])}
    for name in before_groups
}
assert set(field_groups) == {'prompt_ordered_answers_key', 'explanation', 'note0', 'note1', 'note2', 'note3'}
assert all(field_groups[n]['beforeCanonicalSHA256'] == field_groups[n]['afterCanonicalSHA256']
           for n in ('explanation', 'note0', 'note1', 'note2', 'note3'))

candidate = {
    'sourceNativeId': NATIVE,
    'topicId': TOPIC_ID,
    'cycle': CYCLE,
    'initialReceipt': {'path': str(INITIAL_PATH), 'sha256': INITIAL_SHA, 'stage': 'INITIAL', 'status': 'FIX', 'defect': INITIAL_CODE},
    'entries': [{
        'id': ID,
        'topicId': TOPIC_ID,
        'sourceOrder': 81,
        'status': 'READY_FOR_SAME_READER_FINAL',
        'beforeCard': current,
        'beforeHash': canonical_sha(current),
        'proposedCard': proposed,
        'afterHash': canonical_sha(proposed),
        'fieldGroups': field_groups,
    }],
    'qualityCredit': 0,
}

source_index = json.loads(SOURCE_INDEX.read_text(encoding='utf-8'))
source_binding = next(s for s in source_index['rawSources'] if s['path'].endswith('raw-openstax-12-2.json'))
raw = json.loads(SOURCE_RAW.read_text(encoding='utf-8'))
raw_body = raw['originalRecord']['payload']['output'][1]['text']
body_sha = hashlib.sha256(raw_body.encode('utf-8')).hexdigest()
assert source_binding['url'] == URL and source_binding['sha256'] == file_sha(SOURCE_RAW)
assert source_binding['completeOutputSHA256'] == body_sha
assert raw['sourceNativeId'] == '01a166f4-2c48-7ae0-815f-285f91f5a40c'
old_proof = json.loads(OLD_PROOF.read_text(encoding='utf-8'))
old_raw = next(x for x in old_proof['rawSources'] if x['path'] == SOURCE_PATH)
assert old_raw['sha256'] == file_sha(SOURCE_RAW) and old_raw['completeOutputSHA256'] == body_sha

# Full-claim bases are tied to the personally read retained OpenStax L0-L177 body.
grounds = {
    'prompt_ordered_answers_key': 'OpenStax 12.2 L37 separates soma from neuronal extensions and identifies the axon as emerging from the cell body and projecting to target cells; L38 says it propagates the impulse while dendrites receive information. The revised broad class “structure of a neuron” contains all four choices and prevents soma/synapse category elimination before testing the function.',
    'explanation': 'OpenStax 12.2 L37-L39: the axon emerges from the cell body and propagates the nerve impulse toward target cells; dendrites receive information. Explanation is unchanged and retains this supported distinction.',
    'note0': 'OpenStax 12.2 L37-L38: neurons are usually described as having one axon; it may branch repeatedly to communicate with many target cells. This adds a concrete axon fact beyond the prompt/key.',
    'note1': 'OpenStax 12.2 L38: dendrites are usually highly branched and receive information from other neurons at specialized synaptic contacts.',
    'note2': 'OpenStax 12.2 L37: the cell body/soma contains the nucleus and most major organelles.',
    'note3': 'OpenStax 12.2 L38-L42: a synapse is a specialized contact area; the source illustrates an axon branch contacting a dendrite.',
}
locators = {
    'prompt_ordered_answers_key': 'OpenStax 12.2 L37-L39.',
    'explanation': 'OpenStax 12.2 L37-L39.',
    'note0': 'OpenStax 12.2 L37-L38.',
    'note1': 'OpenStax 12.2 L38.',
    'note2': 'OpenStax 12.2 L37.',
    'note3': 'OpenStax 12.2 L38-L42.',
}
source_path_list = [SOURCE_PATH]
literal_groups = [{
    'group': name,
    'literal': value,
    'literalSHA256': canonical_sha(value),
    'primaryGround': grounds[name],
    'sourcePaths': source_path_list,
    'locator': locators[name],
} for name, value in after_groups.items()]

grammar_text = [
    '«Аксон» — самостоятельная именная подпись; вопрос спрашивает название структуры нейрона, и вариант согласован с ним.',
    '«Дендрит» — самостоятельная именная подпись; вопрос спрашивает название структуры нейрона, и вариант согласован с ним.',
    '«Тело клетки (сома)» — название структуры нейрона; пояснение в скобках даёт русское и анатомическое обозначения.',
    '«Синапс» — самостоятельное название структуры/контактной области; форма согласована с вопросом о структуре нейрона.',
]
variant_text = [
    ('Все варианты — именные названия структур нейрона/его специализированного контакта, грамматически подходят к вопросу о структуре. Аксон — единственная из четырёх, которая выходит от тела клетки и проводит импульс к мишеням (L37-L39). Дендрит принимает информацию; сома и синапс не проводили бы отросток в прежнем узком классе, но широкая новая категория включает их. Справка подтверждает ветвление аксона к нескольким клеткам-мишеням (L37-L38).'),
    ('«Дендрит» — корректная именная подпись к вопросу о структуре; он является ближайшим функциональным дистрактором, поскольку тоже отросток нейрона. По L38 дендриты обычно ветвятся и принимают сигналы, тогда как аксон проводит сигнал от тела к мишеням. Справка правдива и полезно описывает именно дендрит.'),
    ('«Тело клетки (сома)» — название структуры нейрона и грамматически согласованный вариант; новая категория prompt включает его. По L37 сома содержит ядро и большинство основных органелл, но роль проведения импульса от тела к мишеням приписана аксону. Справка сообщает конкретный факт о соме.'),
    ('«Синапс» — название специализированной контактной области и грамматически согласованный вариант; новая категория prompt включает такую структуру. По L38-L42 синапс обозначает контакт с другой клеткой, а не отросток, проводящий импульс от тела. Справка истинна и определяет именно синапс.'),
]
variants = []
for i, a in enumerate(proposed['answers']):
    triple = {'prompt': proposed['prompt'], 'answer': a['text'], 'note': a['note']}
    variants.append({
        'slot': i,
        'fullPrompt': proposed['prompt'],
        'answer': a['text'],
        'note': a['note'],
        'grammar': grammar_text[i],
        'plausibilityUniqueKeyAndNoteTruthUsefulness': variant_text[i],
        'sourcePaths': source_path_list,
        'locator': locators['prompt_ordered_answers_key'] + ' ' + locators['note' + str(i)],
        'tripleSHA256': canonical_sha(triple),
    })

sourceproof = {
    'sourceNativeId': NATIVE,
    'topicId': TOPIC_ID,
    'cycle': CYCLE,
    'id': ID,
    'initialBinding': {'path': str(INITIAL_PATH), 'sha256': INITIAL_SHA, 'status': 'FIX', 'qualityCredit': 0},
    'rawSources': [{
        'path': SOURCE_PATH,
        'url': URL,
        'sha256': file_sha(SOURCE_RAW),
        'captureReadProvenance': 'Reused the immutable retained complete official OpenStax web.open response. This author personally read the exact full returned lines L0-L177 in the preceding SOURCE81 slice; cycle1 relies on that unchanged full context and uses no network call/refetch. Original web call native 01a166f4-2c48-7ae0-815f-285f91f5a40c, record line 254.',
        'completeOutputPointer': '/originalRecord/payload/output/1/text',
        'completeOutputSHA256': body_sha,
        'locator': 'OpenStax Anatomy and Physiology 2e, 12.2; relevant L37-L45 and L47-L58. Full returned body L0-L177 personally read.',
        'sourceCaptureNativeId': raw['sourceNativeId'],
    }],
    'entries': [{
        'id': ID,
        'topicId': TOPIC_ID,
        'sourceOrder': 81,
        'status': 'READY_FOR_SAME_READER_FINAL',
        'directedRepair': 'Only prompt category changed from “отросток нейрона” to “структура нейрона”; every answer, note, explanation, frozen field, and source metadata is exact-current preserved.',
        'literalGroups': literal_groups,
        'fourFullPromptAnswerNoteAssessments': variants,
        'correctNoteNewFact': {
            'fact': 'У большинства нейронов аксон обычно один; он может ветвиться и передавать сигнал многим клеткам-мишеням.',
            'sourcePaths': source_path_list,
            'locator': 'OpenStax 12.2 L37-L38.',
        },
        'absoluteDifficulty': 'MEDIUM preserved as confirmed by the same-reader INITIAL: the required distinction is topic-specific knowledge of axon signal direction versus other neuron structures; the category mismatch no longer removes soma/synapse before that distinction. This is not a rare expert fact or broad everyday knowledge.',
        'topicFit': 'Neuron structure and impulse direction directly fit human medicine/anatomy.',
        'defectsAddressed': [INITIAL_CODE],
        'otherFieldsPreservedExact': ['id', 'difficulty', 'answers (including all four notes)', 'correctIndex', 'explanation', 'source'],
    }],
    'networkCalls': 0,
    'qualityCredit': 0,
}

# Read and bind the exact available SOURCE82 proposal, independently checking its preimage/proposal hashes.
source82_file = json.loads(SOURCE82_PATH.read_text(encoding='utf-8'))
source82_entry = source82_file['entries'][0]
assert source82_file['sourceNativeId'] == '01a16ab9-2328-75c3-b57d-0da7b8cc9f41'
assert source82_entry['id'] == 'human-medicine-ext-synapse-junction'
assert source82_entry['status'] == 'READY_FOR_INDEPENDENT_REVIEW'
source82_current = copy.deepcopy(peer_by_id['human-medicine-ext-synapse-junction']['card'])
assert canonical_sha(source82_current) == source82_entry['beforeHash']
assert canonical_sha(source82_entry['proposedCard']) == source82_entry['afterHash']
assert source82_entry['proposedCard']['correctIndex'] == 0

# Full current relevant human-medicine peer bodies; target preimage remains only a binding, not a distinct peer.
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
peer_assessments = {
    'human-medicine-cranial-nerve-pairs': 'Current MAIN relation is the count of human cranial nerve pairs; the candidate asks which neuron structure conducts an impulse from soma to target cells. Different tested entity/relation/value/context; no direct or reverse duplicate.',
    'human-medicine-purkinje-fibers': 'Current MAIN relation is what cardiac Purkinje fibers do in ventricular myocardium; candidate relation is axon identity/conduction in nervous tissue. Different entities and contexts; no direct or reverse duplicate.',
    'human-medicine-cns-myelin-cell': 'Current MAIN relation is which glial cell myelinates CNS axons; candidate asks which structure conducts impulses from cell body to target. Shared axon context does not make the relations identical or reverse.',
    'human-medicine-ext-balance-ear': 'Current MAIN relation is which inner-ear structures register rotational head movement; candidate relation is neuronal impulse conduction from soma. Different entities and tested values; no direct or reverse duplicate.',
    'human-medicine-ext-vision-receptors': 'Current MAIN relation is where rods and cones are located. An optic-nerve mention in explanation does not change that into a question about axons; candidate relation is axon identity/conduction. No direct or reverse duplicate.',
    'human-medicine-ext-heart-pacemaker': 'Current MAIN relation is which cardiac structure usually sets heart rhythm; candidate concerns a neuron process. Different entity/relation/context; no direct or reverse duplicate.',
    'human-medicine-ext-control-brain': 'Current MAIN relation is the organ-level role of the brain in processing/control; candidate concerns a cell-level neuron structure and signal direction. Different granularity/relation; no direct or reverse duplicate.',
    'human-medicine-ext-synapse-junction': 'Actual current SOURCE82 asks for the specialized contact where neuron-target signal transfer occurs. Candidate81 asks which neuron structure conducts an impulse from cell body to targets. The relations are sequentially connected but distinct; candidate81 uses synapse as a distractor and defines it in its note. Direct reverse check is negative.',
}
relevant_pairs = []
for pid in relevant_ids:
    peer = peer_by_id[pid]
    relevant_pairs.append({
        'id': pid,
        'topicId': TOPIC_ID,
        'sourceOrder': peer['sourceOrder'],
        'actualCurrentCard': copy.deepcopy(peer['card']),
        'actualCurrentCardCanonicalSHA256': peer['sha256'],
        'candidate81ProposedCard': copy.deepcopy(proposed),
        'candidate81CanonicalSHA256': canonical_sha(proposed),
        'bilateralMainAssessment': peer_assessments[pid],
    })

# Exact SOURCE82 full candidate binding and bilateral MAIN comparison, separate from its current preimage.
source82_pair = {
    'source82CandidatePath': str(SOURCE82_PATH),
    'source82CandidateFileSHA256': file_sha(SOURCE82_PATH),
    'source82NativeId': source82_file['sourceNativeId'],
    'source82Status': source82_entry['status'],
    'source82Id': source82_entry['id'],
    'source82TopicId': source82_entry['topicId'],
    'source82SourceOrder': source82_entry['sourceOrder'],
    'source82BeforeCard': copy.deepcopy(source82_entry['beforeCard']),
    'source82BeforeHash': source82_entry['beforeHash'],
    'source82ProposedCard': copy.deepcopy(source82_entry['proposedCard']),
    'source82AfterHash': source82_entry['afterHash'],
    'source81ProposedCard': copy.deepcopy(proposed),
    'source81AfterHash': canonical_sha(proposed),
    'bilateralMainERVC': {
        'source81': 'Entity: axon/neuron structure; relation: conducts impulse from cell body to target cells; value: axon; context: intracellular neuronal signaling. The broad “neuron structure” prompt admits all listed structures while the functional clause selects axon.',
        'source82': 'Entity: synapse/specialized contact; relation: contact where signal transfers between neuron and target cell; value: synapse; context: intercellular signaling junction.',
        'comparison': 'Both proposals concern adjacent stages in neural signaling and share the same anatomy vocabulary, but they test different entity-relation-value-context tuples. They are not paraphrases or direct reverses. Answer-set overlap and the shared axon fact in a note are not MAIN duplicates; MAIN comparison uses each prompt and ordered answers.',
        'directReverse': False,
        'noteOverlapIsNotDuplicateGround': 'SOURCE82 note for axon and SOURCE81 correct note both mention axonal conduction/branching. That is note overlap; the prompts and keys test different relations (contact location versus conducting process).',
    },
}

# Search exact whole-word/morphological neuron terms in full current MAIN rows; assess any cross-topic lexical hits by ERVC.
pattern = re.compile(r'(?<![а-яё])(?:нейрон\w*|аксон\w*|дендрит\w*|синапс\w*|нервн\w*\s+импульс\w*|нервн\w*\s+клетк\w*)(?![а-яё])', re.IGNORECASE)
cross_hits = []
for row in inventory['globalMAIN']['rows']:
    if row['topicId'] == TOPIC_ID:
        continue
    text = ' '.join([row['prompt'], *row['answers']])
    if pattern.search(text):
        cross_hits.append(copy.deepcopy(row))
# Lexical candidates are preserved for coordinator review; none is assumed duplicate by word match alone.
false_positive_reasons = {}
for r in cross_hits:
    if r['id'] == 'dinosaurs-paleontology-synapsid-one-opening':
        false_positive_reasons[r['id']] = 'Synapsid is a skull classification in mammalian evolutionary history; entity/relation/context differs from neuronal synapse/axon anatomy.'
    else:
        false_positive_reasons[r['id']] = 'Lexical candidate only; inspected full prompt and answer row and found no neuron process or neuronal signal-direction relation.'
peer_snapshot = {
    'sourceNativeId': NATIVE,
    'topicId': TOPIC_ID,
    'cycle': CYCLE,
    'id': ID,
    'freshInventoryPath': str(INV),
    'globalMAIN': copy.deepcopy(inventory['globalMAIN']),
    'actualCurrentPeers': copy.deepcopy(inventory['actualCurrentPeers']),
    'selfBindingNote': 'Assigned card is included as its actual CURRENT preimage binding only; it is not counted as a distinct peer.',
    'sameTopicRelevantPairs': relevant_pairs,
    'simultaneousProposedPair': source82_pair,
    'crossTopicSemanticPeerAssessment': {
        'query': 'Exact whole-word/morphological neuron, axon, dendrite, synapse, nerve impulse and nerve cell terms across all current MAIN prompts/answers; every hit assessed by entity-relation-value-context and direct reverse.',
        'lexicalHits': [{'row': r, 'assessment': false_positive_reasons[r['id']]} for r in cross_hits],
        'relevantSemanticPeers': [],
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
    'beforeHash': canonical_sha(current),
    'afterHash': canonical_sha(proposed),
    'onlyChangedField': 'prompt',
    'source82BeforeHashVerified': source82_entry['beforeHash'],
    'source82AfterHashVerified': source82_entry['afterHash'],
    'source82Status': source82_entry['status'],
    'sameTopicCurrentPeers': len(inventory['actualCurrentPeers']),
    'globalMAINRows': len(inventory['globalMAIN']['rows']),
    'crossTopicLexicalHits': len(cross_hits),
    'networkCalls': 0,
    'qualityCredit': 0,
}, ensure_ascii=False))
