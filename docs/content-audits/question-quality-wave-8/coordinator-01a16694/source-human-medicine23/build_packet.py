import copy, hashlib, json
from pathlib import Path

C = Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle')
OUT = C / 'docs/content-audits/question-quality-wave-8/coordinator-01a16694/source-human-medicine23'
NATIVE = '01a166c1-3f9d-71e3-9f08-7c44ba06372e'
TOPIC = 'human-medicine'
CARD_ID = 'human-medicine-loop-henle-gradient'

def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')
def sha(value):
    return hashlib.sha256(canonical(value)).hexdigest()
def file_sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def write(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def groups(card):
    return {
        'prompt_ordered_answers_key': {
            'prompt': card['prompt'],
            'answers': [a['text'] for a in card['answers']],
            'correctIndex': card['correctIndex']},
        'explanation': card['explanation'],
        **{'note' + str(k): a['note'] for k, a in enumerate(card['answers'])}}

inv = json.loads((OUT / 'fresh-inventory.json').read_text(encoding='utf-8'))
match = [p for p in inv['actualCurrentPeers'] if p['id'] == CARD_ID]
assert len(match) == 1
before = copy.deepcopy(match[0]['card'])
assert (before['id'], before['difficulty'], before['correctIndex']) == (CARD_ID, 'hard', 1)
assert match[0]['sourceOrder'] == 23 and match[0]['topicId'] == TOPIC
assert sha(before) == 'f1c3d29b5910c9ff540e68bec66f2fe8fec0b929eababdcdd2f03906cd895cef'
proposed = copy.deepcopy(before)

before_groups, after_groups = groups(before), groups(proposed)
field_groups = {
    k: {'beforeCanonicalSHA256': sha(v), 'afterCanonicalSHA256': sha(after_groups[k])}
    for k, v in before_groups.items()
}
assert len(field_groups) == 6

candidate = {
    'sourceNativeId': NATIVE, 'topicId': TOPIC, 'cycle': 0, 'id': CARD_ID,
    'sourceOrder': 23, 'status': 'HOLD', 'qualityCredit': 0,
    'entries': [{
        'id': CARD_ID, 'topicId': TOPIC, 'sourceOrder': 23, 'status': 'HOLD',
        'beforeCard': before, 'beforeHash': sha(before),
        'proposedCard': proposed, 'afterHash': sha(proposed), 'fieldGroups': field_groups,
        'holdReason': 'The central countercurrent-gradient/urine-concentration premise has no usable full source in this pass. The supplied 25.5 URL is not that physiology section; OpenStax 25.6 was captured but its page states that the material may not be ingested into LLM offerings without prior permission, so it is excluded from factual grounds. The one official NCBI/PMC alternative returned only a browser challenge. NIDDK retained context supports general nephron filtration/reabsorption but not this mechanism. Independently, renal pelvis is not part of a nephron under the prompt wording.'
    }]
}

niddk_path = 'docs/content-audits/question-quality-wave-8/coordinator-01a1661f/source-human-medicine14/raw/niddk-kidney-nephron.json'
os25_5_path = 'docs/content-audits/question-quality-wave-8/coordinator-01a165b2/source-human-medicine6/raw/openstax-urine-formation.json'
os25_3_path = 'docs/content-audits/question-quality-wave-8/coordinator-01a165b2/source-human-medicine6/raw/openstax-kidney-gross-anatomy.json'
os25_6_path = 'docs/content-audits/question-quality-wave-8/coordinator-01a16694/source-human-medicine23/openstax-25-6.json'

raw_sources = [
    {
        'path': niddk_path,
        'url': 'https://www.niddk.nih.gov/health-information/kidney-disease/kidneys-how-they-work',
        'sha256': file_sha(C / niddk_path),
        'captureReadProvenance': 'Retained complete official NIDDK page from SOURCE14; native 01a1663c-ae62-7883-8139-0bd72ec0db20 record 342. I personally read the full retained body L0-L227 for SOURCE23. It supports general nephron/filter/tubule facts only; it does not cover the loop of Henle, countercurrent multiplication, medullary gradient, or ADH.',
        'locator': 'Complete returned page L0-L227; relevant scope L183-L190. Limitations: no loop-of-Henle or ADH mechanism.',
        'completeOutputPointer': '/originalRecord/payload/output/1/text',
        'completeOutputSHA256': 'c51647052f079be5e9c12c8876c486ec0402b9085586cd5247c80a19fd540e5e'
    },
    {
        'path': os25_5_path,
        'url': 'https://openstax.org/books/anatomy-and-physiology-2e/pages/25-5-physiology-of-urine-formation',
        'sha256': file_sha(C / os25_5_path),
        'captureReadProvenance': 'Retained complete page from prior SOURCE6 context; prior capture native 01a165d5-dbe9-7f90-ba28-71e56abeb21f record 348. I personally read the whole retained body L0-L152. Excluded from SOURCE23 factual grounds because the page states at L104 that use in LLM offerings requires prior permission.',
        'locator': 'Complete returned page L0-L152. Excluded from claims; original card source URL is recorded in beforeCard.',
        'completeOutputPointer': '/originalRecord/payload/output/1/text',
        'completeOutputSHA256': 'b5a8c15670ccaf154ac81c57b0d51afcbab1d4fc9303d5b15e3be7e76061551c',
        'useStatus': 'EXCLUDED_FROM_FACT_GROUNDS_SOURCE_TERMS'
    },
    {
        'path': os25_3_path,
        'url': 'https://openstax.org/books/anatomy-and-physiology-2e/pages/25-3-gross-anatomy-of-the-kidney',
        'sha256': file_sha(C / os25_3_path),
        'captureReadProvenance': 'Retained complete page from prior SOURCE6 context; prior capture native 01a165d5-dbe9-7f90-ba28-71e56abeb21f record 471. I personally read the whole retained body L0-L118. Excluded from SOURCE23 factual grounds because the page states at L70 that use in LLM offerings requires prior permission.',
        'locator': 'Complete returned page L0-L118. Excluded from claims.',
        'completeOutputPointer': '/originalRecord/payload/output/1/text',
        'completeOutputSHA256': '9849b1ebefd0891fdfbadc21fdf37c1db13b4040f596b12657ce72c10682e1e8',
        'useStatus': 'EXCLUDED_FROM_FACT_GROUNDS_SOURCE_TERMS'
    },
    {
        'path': os25_6_path,
        'url': 'https://openstax.org/books/anatomy-and-physiology-2e/pages/25-6-tubular-reabsorption',
        'sha256': file_sha(OUT / 'openstax-25-6.json'),
        'captureReadProvenance': 'Captured exact full functions.web__run open result in SOURCE23 native 01a166c1-3f9d-71e3-9f08-7c44ba06372e, record 296; complete returned page L0-L211 was personally read. The captured page states at L163 that prior permission is required before material is ingested into LLM offerings; excluded from factual grounds.',
        'locator': 'Complete returned page L0-L211; terms notice L163-L167. Excluded from claims.',
        'completeOutputPointer': '/originalRecord/payload/output/1/text',
        'completeOutputSHA256': '9fbfcf9ba6b3f3987cd5d3e858e2f67fc387bc74a31e2155f6006da6f853771a',
        'useStatus': 'EXCLUDED_FROM_FACT_GROUNDS_SOURCE_TERMS'
    }
]

literal_groups = []
grounds = {
    'prompt_ordered_answers_key': ('HOLD', 'The question asserts that a nephron part creates a countercurrent osmotic gradient for urine concentration. NIDDK L183-L190 does not substantiate that mechanism. The retained page originally cited by the card is 25.5 and is outside the eligible source basis; the only inspected 25.6 OpenStax page is excluded under its stated terms, while the one official NCBI/PMC alternative returned a browser challenge. The exact mechanism/key therefore remains unverified.'),
    'explanation': ('HOLD', 'The explanation depends on the same unsupported gradient premise and additionally attributes water return from collecting ducts to ADH. The retained eligible NIDDK page does not mention either relation. No source-backed explanation can be certified in this cycle.'),
    'note0': ('HOLD', 'The note assigns bulk water and solute reabsorption specifically to the proximal convoluted tubule. Retained eligible NIDDK L190 describes tubule reabsorption generally, not this nephron segment; the segment-specific assertion remains unsupported.'),
    'note1': ('HOLD', 'The keyed note repeats the prompt mechanism and adds no independently verified own-option fact. No eligible retained source establishes countercurrent multiplication by the loop.'),
    'note2': ('PARTIAL_HOLD', 'NIDDK L187 states that the glomerulus passes small molecules, wastes, and fluid into the tubule; it does not state that the glomerular capsule receives the primary filtrate. The capsule-specific claim remains unsupported.'),
    'note3': ('PARTIAL_HOLD', 'NIDDK L167 states that urine flows from kidneys to bladder through ureters, but it does not establish the renal pelvis function asserted here. The pelvis-specific note remains unsupported.')
}
for group, value in after_groups.items():
    status, ground = grounds[group]
    paths = [niddk_path] if group in ('note2', 'note3') else []
    literal_groups.append({
        'group': group, 'literal': value, 'literalSHA256': sha(value),
        'primaryGround': ground, 'sourcePaths': paths,
        'locator': 'NIDDK L167, L183-L190 only for the limited facts stated above; otherwise no eligible source locator. OpenStax evidence was excluded from factual grounds.'
    })

variants = []
variant_details = [
    ('The question and four answers are parallel in grammatical form. The proximal convoluted tubule is a plausible nephron segment; the keyed physiological relation is not source-verified. The note gives a segment-specific reabsorption fact not supported by eligible source.', 'The note is relevant to the proposed alternative but cannot be vouched for from admissible evidence.'),
    ('The question and four answers are parallel in grammatical form. The loop of Henle is a plausible nephron structure, but uniqueness depends on the unverified countercurrent-gradient premise. The answer note merely repeats that premise and adds no sourced new fact.', 'No additional own-option fact is established; this is a substantive note defect as well as a source HOLD.'),
    ('The question and four answers are parallel in grammatical form. The glomerular capsule is a plausible nephron structure; NIDDK supports filtration into the tubule but not the capsule-specific note. Its full relation to the keyed mechanism cannot be evaluated without eligible source support.', 'NIDDK L187 supports the glomerulus/tubule filtration path generally, not this capsule-specific wording.'),
    ('The answer is a kidney structure but not a part of the nephron named by the prompt, so it is less comparable and can be eliminated by category knowledge. Its claimed urine-collection route is not established by the eligible retained NIDDK page.', 'NIDDK L167 supports ureter transport, not the renal-pelvis function asserted in the note.')
]
for slot, a in enumerate(proposed['answers']):
    grammar, plaus = variant_details[slot]
    variants.append({
        'slot': slot, 'fullPrompt': proposed['prompt'], 'answer': a['text'], 'note': a['note'],
        'grammar': 'Grammatically parallel noun phrase: the prompt asks which anatomical part, and the option supplies a structure name.',
        'plausibilityUniqueKeyAndNoteTruthUsefulness': grammar + ' ' + plaus,
        'sourcePaths': [niddk_path] if slot in (2, 3) else [],
        'locator': 'NIDDK L167 and L183-L190 only for stated limited facts; no admissible locator for unsupported parts.',
        'tripleSHA256': sha({'prompt': proposed['prompt'], 'answer': a['text'], 'note': a['note']})
    })

sourceproof = {
    'sourceNativeId': NATIVE, 'topicId': TOPIC, 'cycle': 0, 'id': CARD_ID,
    'sourceOrder': 23, 'status': 'HOLD', 'qualityCredit': 0,
    'sourceSelection': 'The retained NIDDK whole-page context was personally reread and supports only general nephron filtration/tubule claims. OpenStax pages 25.3, 25.5, and the new 25.6 capture were excluded from factual grounds because their pages state that prior permission is required before ingestion into LLM offerings. The official PMC alternative returned only a CAPTCHA/challenge page, not its full content. No retry or adjacent-source workaround was made.',
    'rawSources': raw_sources,
    'networkAttempts': [
        {'role': 'primary discovery', 'tool': 'web__run search_query', 'nativeJournal': '/Users/eaafonasev/.codex/sessions/2026/10/23/rollout-2026-10-23T08-15-03-01a166c1-3f9d-71e3-9f08-7c44ba06372e.jsonl', 'nativeCallRecordLine': 284, 'nativeOutputRecordLine': 287, 'query': 'site:openstax.org/books/anatomy-and-physiology-2e loop of Henle countercurrent multiplier medulla osmotic gradient', 'result': 'Located OpenStax 25.6; discovery only, not a source proof.'},
        {'role': 'primary', 'tool': 'web__run open', 'nativeJournal': '/Users/eaafonasev/.codex/sessions/2026/10/23/rollout-2026-10-23T08-15-03-01a166c1-3f9d-71e3-9f08-7c44ba06372e.jsonl', 'nativeCallId': 'call_de9a93a71ee2492f86c7f31e52cedea0', 'nativeCallRecordLine': 293, 'nativeOutputRecordLine': 296, 'url': 'https://openstax.org/books/anatomy-and-physiology-2e/pages/25-6-tubular-reabsorption', 'returnedExtent': 'Full returned page L0-L211; saved once as openstax-25-6.json. Excluded from factual grounds because of the page terms notice at L163-L167.'},
        {'role': 'official alternative', 'tool': 'web__run open', 'nativeJournal': '/Users/eaafonasev/.codex/sessions/2026/10/23/rollout-2026-10-23T08-15-03-01a166c1-3f9d-71e3-9f08-7c44ba06372e.jsonl', 'nativeCallId': 'call_ce018b3886c046349c6b41e28fe14fe2', 'nativeCallRecordLine': 332, 'nativeOutputRecordLine': 335, 'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC2796244/', 'returnedExtent': 'Only 3 lines, L0-L2, browser reCAPTCHA/challenge; no primary-context body. Exact claim held; no retry.'}
    ],
    'networkAccounting': 'No source-page retry, additional official alternative, reset, or adjacent workaround. Search was used only to identify the official OpenStax section; one primary open and one official-alternative open were performed.',
    'entries': [{
        'id': CARD_ID, 'topicId': TOPIC, 'sourceOrder': 23, 'status': 'HOLD',
        'literalGroups': literal_groups,
        'fourFullPromptAnswerNoteAssessments': variants,
        'correctNoteNewFact': {
            'fact': 'Not established. The current keyed note restates the prompt premise and contributes no distinct source-backed fact about the loop of Henle.',
            'locator': None, 'sourcePaths': [],
            'usefulness': 'A qualifying additional own-option fact cannot be certified until an admissible complete source is available.'
        },
        'absoluteDifficulty': {
            'level': 'hard', 'audience': 'Adult general-knowledge quiz player',
            'ground': 'The required association between a nephron segment and the countercurrent urine-concentrating mechanism requires specific renal physiology rather than broad adult knowledge. This supports the frozen level as an editorial judgment, while the mechanism itself remains HOLD.'
        },
        'defects': [
            {'field': 'prompt_ordered_answers_key', 'status': 'HOLD', 'reason': 'Central countercurrent-gradient premise lacks eligible full-source evidence in this pass.'},
            {'field': 'note1', 'status': 'FIX_NEEDED', 'reason': 'Correct-option note repeats the prompt/key premise and adds no new own-option fact.'},
            {'field': 'answer[3]', 'status': 'FIX_NEEDED', 'reason': 'Renal pelvis is not a nephron part, so it is category-mismatched under the current prompt wording.'},
            {'field': 'source.url', 'status': 'FIX_NEEDED', 'reason': 'The card currently links OpenStax section 25.5, not a source context admitted to substantiate the loop-gradient claim.'}
        ],
        'frozen': {'id': CARD_ID, 'topicId': TOPIC, 'sourceOrder': 23, 'difficulty': 'hard', 'correctIndex': 1}
    }]
}

# Full live same-topic cards are preserved; only selected distinct MAIN pairs receive bilateral judgments.
relevant_ids = [
    'human-medicine-kidney-main-function', 'human-medicine-nephron-unit',
    'human-medicine-glomerular-barrier', 'human-medicine-ext-blood-filter',
    'human-medicine-ext-aldosterone', 'human-medicine-ext-antidiuretic-hormone',
    'human-medicine-ext-kidney-unit'
]
peers = {p['id']: p for p in inv['actualCurrentPeers']}
assert all(i in peers for i in relevant_ids)
comparisons = {
 'human-medicine-kidney-main-function': ('Target MAIN is one nephron segment’s role in a concentrating mechanism; peer MAIN is a broad organ-level kidney function. Different entity granularity and relation.', 'The peer does not ask which nephron structure performs countercurrent multiplication; no reverse formulation of its organ-level water-salt role yields the target fact.'),
 'human-medicine-nephron-unit': ('Target MAIN is the loop’s role in the medullary concentrating mechanism; peer MAIN identifies the nephron as the kidney’s filtering unit. Same broad organ system, different entity/relation/value.', 'The peer asks what the nephron is, not which part creates a gradient; the target does not answer nephron identity.'),
 'human-medicine-glomerular-barrier': ('Target MAIN concerns loop-mediated concentration; peer MAIN concerns which materials cross the glomerular filtration barrier. Different nephron structure and process.', 'The filtration-barrier question does not identify a concentrating mechanism, and the target does not specify filtration-barrier permeability.'),
 'human-medicine-ext-blood-filter': ('Target MAIN concerns a nephron segment and urine concentration; peer MAIN asks which organ filters blood and forms urine. Different scale and relation.', 'The organ-level kidney question does not reduce to the loop-gradient fact; the target does not name which organs form urine.'),
 'human-medicine-ext-aldosterone': ('Target MAIN is a segment-level countercurrent mechanism; peer MAIN is a hormone regulating sodium reabsorption. Related renal physiology but distinct entity and relation.', 'The hormone question does not ask for the loop structure; the loop-gradient question does not name aldosterone or its regulation.'),
 'human-medicine-ext-antidiuretic-hormone': ('Target MAIN is gradient generation by a nephron segment; peer MAIN is ADH-driven water return in collecting ducts. They connect in the explanation but test different causal steps.', 'The ADH question asks for a hormone, not the gradient-generating segment; the target asks for the loop, not the hormone.'),
 'human-medicine-ext-kidney-unit': ('Target MAIN is the loop’s role in concentration; peer MAIN identifies the ureter as the route from kidney to bladder. Different structures and relations.', 'Ureter transport does not answer which nephron part creates a medullary gradient; the target does not identify the urine outflow tube.')
}
relevant_pairs = []
for peer_id in relevant_ids:
    peer = peers[peer_id]
    actual, reverse = comparisons[peer_id]
    relevant_pairs.append({
        'candidateCurrent': {'id': CARD_ID, 'topicId': TOPIC, 'sourceOrder': 23, 'card': before, 'sha256': sha(before)},
        'candidateProposed': {'id': CARD_ID, 'topicId': TOPIC, 'sourceOrder': 23, 'card': proposed, 'sha256': sha(proposed), 'sameAsPreimage': True},
        'peerCurrent': peer,
        'actualBilateralMAIN': {'candidateToPeer': actual, 'directReverseCheck': reverse},
        'proposedBilateralMAIN': {'candidateToPeer': actual, 'directReverseCheck': reverse},
        'distinctPeerRule': 'This is one existing current peer. The unchanged candidate proposal is not counted as a second distinct catalog peer.'
    })

animals_path = C / 'src/content/topics/animals.json'
animals = json.loads(animals_path.read_text(encoding='utf-8'))
animal = next(q for q in animals['questions'] if q['id'] == 'animals-kangaroo-rat-metabolic-water')
animal_peer = {'id': animal['id'], 'topicId': 'animals', 'sourceOrder': next(i for i,q in enumerate(animals['questions'],1) if q['id']==animal['id']), 'card': animal, 'sha256': sha(animal)}
cross = [{
    'peerCurrent': animal_peer,
    'candidateToPeer': 'Target MAIN is which nephron segment creates a concentrating gradient. This peer asks which process creates new metabolic water in a kangaroo rat; concentrated urine appears only as a wrong option. Different relation, value, and ecological context, not a semantic duplicate.',
    'directReverseCheck': 'The kangaroo-rat question cannot be answered by naming the loop of Henle; the target does not identify metabolic oxidation as the source of new water.'
}]

peer_snapshot = {
    'sourceNativeId': NATIVE, 'topicId': TOPIC, 'cycle': 0, 'id': CARD_ID, 'sourceOrder': 23,
    'globalMAIN': inv['globalMAIN'],
    'actualCurrentPeers': inv['actualCurrentPeers'],
    'relevantSameTopicPairs': relevant_pairs,
    'relevantCrossTopicPeers': cross,
    'candidateCurrent': {'id': CARD_ID, 'topicId': TOPIC, 'sourceOrder': 23, 'card': before, 'sha256': sha(before)},
    'candidateProposed': {'id': CARD_ID, 'topicId': TOPIC, 'sourceOrder': 23, 'card': proposed, 'sha256': sha(proposed), 'sameAsPreimage': True},
    'inventoryBinding': {'path': 'docs/content-audits/question-quality-wave-8/coordinator-01a16694/source-human-medicine23/fresh-inventory.json', 'globalMAINRows': 11000, 'sameTopicCards': 100, 'targetSha256': sha(before)},
    'semanticSearch': 'Russian/English kidneys, nephron, urine concentration, countercurrent, osmolality, medulla, ADH, PCT, collecting-duct terms were used to select candidates. The animal kangaroo-rat metabolic-water question was retained as the only relevant cross-topic contextual peer; substring-only unrelated hits were excluded.'
}

write('candidate.json', candidate)
write('sourceproof.json', sourceproof)
write('peer-snapshot.json', peer_snapshot)
print(json.dumps({
    'status': 'HOLD', 'files': ['candidate.json','sourceproof.json','peer-snapshot.json'],
    'beforeHash': sha(before), 'afterHash': sha(proposed),
    'fieldGroupCount': len(field_groups), 'variantCount': len(variants),
    'sameTopicCurrentPeers': len(inv['actualCurrentPeers']), 'bilateralPairs': len(relevant_pairs),
    'crossTopicPeers': len(cross), 'globalMAINRows': len(inv['globalMAIN']['rows']),
    'qualityCredit': 0
}, ensure_ascii=False))
