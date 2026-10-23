import copy
import hashlib
import json
from pathlib import Path

ROOT = Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle')
OUT = ROOT / 'docs/content-audits/question-quality-wave-8/coordinator-01a1676a/source-human-medicine38'
NATIVE = '01a16829-277a-75a1-89d3-811804e51f6f'
URL_MAIN = 'https://www.nhlbi.nih.gov/health/heart/blood-flow'
URL_LEGS = 'https://www.nhlbi.nih.gov/health/varicose-veins'
URL_OPENSTAX = 'https://openstax.org/books/anatomy-and-physiology-2e/pages/20-1-structure-and-function-of-blood-vessels'
RAW_REL = 'docs/content-audits/question-quality-wave-8/coordinator-01a1676a/source-human-medicine38/raw/nhlbi-blood-flow.json'
RAW = ROOT / RAW_REL

def canonical_sha(value):
    body = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')
    return hashlib.sha256(body).hexdigest()

def file_sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def groups(card):
    return {
        'prompt_ordered_answers_key': {
            'prompt': card['prompt'],
            'answers': [a['text'] for a in card['answers']],
            'correctIndex': card['correctIndex'],
        },
        'explanation': card['explanation'],
        **{'note' + str(k): a['note'] for k, a in enumerate(card['answers'])},
    }

def write_json(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

inv_path = OUT / 'fresh-inventory.json'
inv = json.loads(inv_path.read_text())
current = next(copy.deepcopy(x['card']) for x in inv['actualCurrentPeers'] if x['id'] == 'human-medicine-vein-direction')
assert current['id'] == 'human-medicine-vein-direction'
assert canonical_sha(current) == '9c7209cd4d8d5d45620dd9e28a12c394e8c7833790a3b297c88080e30f17e13b'
assert (current['difficulty'], current['correctIndex']) == ('easy', 1)
assert RAW.exists()
raw_meta = json.loads(RAW.read_text())
S37_CANDIDATE_PATH = ROOT / 'docs/content-audits/question-quality-wave-8/coordinator-01a1676a/source-human-medicine37/candidate.json'
S37_RAW_PATH = ROOT / 'docs/content-audits/question-quality-wave-8/coordinator-01a1676a/source-human-medicine37/raw/openstax-blood-vessels.json'
s37 = json.loads(S37_CANDIDATE_PATH.read_text())
s37_entry = s37['entries'][0]
s37_raw = json.loads(S37_RAW_PATH.read_text())
assert s37_entry['id'] == 'human-medicine-artery-direction' and s37_entry['sourceOrder'] == 37 and s37_entry['status'] == 'HOLD'
assert canonical_sha(s37_entry['beforeCard']) == s37_entry['beforeHash'] == '6170ed79b059bfe5b2afcc608ab9895dd98de6fee08345d627953e6ceb0fffa8'
assert canonical_sha(s37_entry['proposedCard']) == s37_entry['afterHash'] == '92d87b4a2c7f513df3dc928be39ec1ababa4806e8c1d2a0d40b01f694ce80312'
assert s37_raw['url'] == URL_OPENSTAX
assert raw_meta['sourceNativeId'] == NATIVE
assert raw_meta['completeOutputPointer'] == '/originalRecord/payload/output/1/text'
assert URL_MAIN in raw_meta['originalRecord']['payload']['output'][1]['text']
assert URL_LEGS in raw_meta['originalRecord']['payload']['output'][1]['text']

proposed = copy.deepcopy(current)
proposed['answers'] = [
    {'text': 'От сердца', 'note': 'Артерии уносят кровь от сердца; аорта направляет её к органам тела.'},
    {'text': 'К сердцу', 'note': 'Верхняя и нижняя полые вены приносят кровь из тела в правое предсердие.'},
    {'text': 'К лёгким', 'note': 'К лёгким кровь отводит лёгочная артерия, выходящая из сердца.'},
    {'text': 'К органам', 'note': 'Аорта направляет кровь из сердца к остальным тканям организма.'},
]
proposed['explanation'] = 'Вены несут кровь к сердцу. Верхняя и нижняя полые вены приносят кровь из тела в правое предсердие, а лёгочные вены — из лёгких в левое.'
proposed['source'] = {
    'title': 'National Heart, Lung, and Blood Institute (NHLBI), NIH: How the Heart Works — How Blood Flows through the Heart',
    'url': URL_MAIN,
    'verifiedAt': '2026-10-23',
}

before_groups = groups(current)
after_groups = groups(proposed)
field_groups = {k: {'beforeCanonicalSHA256': canonical_sha(before_groups[k]), 'afterCanonicalSHA256': canonical_sha(after_groups[k])} for k in before_groups}
entry = {
    'id': proposed['id'], 'topicId': 'human-medicine', 'sourceOrder': 38,
    'status': 'HOLD', 'beforeCard': current, 'beforeHash': canonical_sha(current),
    'proposedCard': proposed, 'afterHash': canonical_sha(proposed), 'fieldGroups': field_groups,
}
write_json('candidate.json', {
    'sourceNativeId': NATIVE, 'topicId': 'human-medicine', 'cycle': 0,
    'baselineCode': '3f874b1f49615c18cf5ca14cb65899a1945bac1d',
    'catalogCandidate': '3f874b1f49615c18cf5ca14cb65899a1945bac1d',
    'entries': [entry], 'qualityCredit': 0,
})

source_paths = [RAW_REL]
locators = {
    'main': 'NHLBI page: L93 defines veins as bringing blood to the heart and arteries as carrying blood away; L114-L116 describe superior/inferior vena cava returning blood from the body to the right atrium and pulmonary veins returning oxygen-rich blood from lungs; L118 says the aorta carries blood from the heart to the rest of the body.',
    'legs': 'NHLBI page: L83-L85 defines veins as carrying blood from organs and limbs back to the heart; L107 and L109 state one-way valves in leg veins keep blood moving toward the heart and prevent flow back down.',
}
raw_source_base = {
    'path': RAW_REL, 'sha256': file_sha(RAW),
    'captureReadProvenance': {
        'sourceNativeId': NATIVE,
        'nativeJournal': '/Users/eaafonasev/.codex/sessions/2026/10/23/rollout-2026-10-23T14-48-10-01a16829-277a-75a1-89d3-811804e51f6f.jsonl',
        'nativeRecordLine': 313,
        'originalTool': 'tools.web__run open (two official NHLBI pages in one call)',
        'completeOutputPointer': raw_meta['completeOutputPointer'],
        'completeOutputSHA256': raw_meta['completeOutputSHA256'],
        'personalReadEvidence': 'Personally read the complete returned relevant contexts for both pages: blood-flow L89-L144 and varicose-veins L77-L122. Used only statements at the locators listed per URL.',
        'limitations': 'The blood-flow page output reports 156 total lines and the varicose-veins page 168 total lines; both complete returned page bodies are present in this combined output.',
    },
}
raw_sources = [
    {**raw_source_base, 'url': URL_MAIN, 'locator': locators['main'], 'completeOutputPointer': raw_meta['completeOutputPointer'], 'completeOutputSHA256': raw_meta['completeOutputSHA256']},
    {**raw_source_base, 'url': URL_LEGS, 'locator': locators['legs'], 'completeOutputPointer': raw_meta['completeOutputPointer'], 'completeOutputSHA256': raw_meta['completeOutputSHA256']},
]
source_evidence = {
    'sourceNativeId': NATIVE, 'topicId': 'human-medicine', 'cycle': 0,
    'id': proposed['id'], 'sourceOrder': 38, 'status': 'HOLD', 'qualityCredit': 0,
    'sourceSelection': {
        'selected': URL_MAIN,
        'reason': 'Official NIH page directly defines direction of venous and arterial blood flow and gives major systemic/pulmonary examples.',
        'supportingContext': URL_LEGS,
        'unusedOpenedSource': {
            'url': 'https://openstax.org/books/anatomy-and-physiology-2e/pages/20-1-structure-and-function-of-blood-vessels',
            'result': 'Full page was opened, but not used as evidence; the page itself states a reuse restriction for ingestion into generative AI offerings. No question claim relies on it.',
        },
    },
    'rawSources': raw_sources,
    'networkAttempts': [
        {'kind': 'web.open', 'url': 'https://openstax.org/books/anatomy-and-physiology-2e/pages/20-1-structure-and-function-of-blood-vessels', 'result': 'Full page returned; excluded from evidence and no claims rely on it.'},
        {'kind': 'web.search', 'query': 'site:nhlbi.nih.gov veins carry blood back to the heart pulmonary veins; site:medlineplus.gov veins carry blood toward the heart pulmonary veins', 'result': 'Discovery only; no search snippet used as source proof.'},
        {'kind': 'web.open', 'urls': [URL_MAIN, URL_LEGS], 'result': 'Both official page bodies returned in one combined output and preserved once in rawSources path.'},
    ],
    'entries': [{
        'id': proposed['id'], 'status': 'HOLD',
        'literalGroups': [
            {'group': 'prompt_ordered_answers_key', 'literal': after_groups['prompt_ordered_answers_key'], 'literalSHA256': canonical_sha(after_groups['prompt_ordered_answers_key']), 'primaryGround': 'The NHLBI definition directly says veins bring blood to the heart and arteries take blood away. Venae cavae and pulmonary veins are concrete examples; only the heartward direction answers the general question. All four options are short directional phrases, with one key.', 'sourcePaths': source_paths, 'locator': 'NHLBI blood-flow L93, L114-L118.'},
            {'group': 'explanation', 'literal': after_groups['explanation'], 'literalSHA256': canonical_sha(after_groups['explanation']), 'primaryGround': 'The first sentence states the main directional fact. The second gives the superior/inferior vena cava route to the right atrium and pulmonary vein route from the lungs, preserving the distinction that vein direction is defined relative to the heart rather than oxygen content.', 'sourcePaths': source_paths, 'locator': 'NHLBI blood-flow L93-L96 and L114-L116.'},
            {'group': 'note0', 'literal': after_groups['note0'], 'literalSHA256': canonical_sha(after_groups['note0']), 'primaryGround': 'NHLBI defines arteries as taking blood away from the heart and states that the aorta carries blood from the heart to the rest of the body.', 'sourcePaths': source_paths, 'locator': 'NHLBI blood-flow L93 and L118.'},
            {'group': 'note1', 'literal': after_groups['note1'], 'literalSHA256': canonical_sha(after_groups['note1']), 'primaryGround': 'NHLBI states that the superior and inferior vena cava bring oxygen-poor blood from the body to the right atrium; this is a concrete route fact beyond the prompt/key.', 'sourcePaths': source_paths, 'locator': 'NHLBI blood-flow L114.'},
            {'group': 'note2', 'literal': after_groups['note2'], 'literalSHA256': canonical_sha(after_groups['note2']), 'primaryGround': 'NHLBI says the pulmonary artery takes blood from the heart to the lungs; the option is a destination reached by a pulmonary artery, not the general direction of veins.', 'sourcePaths': source_paths, 'locator': 'NHLBI blood-flow L114-L115.'},
            {'group': 'note3', 'literal': after_groups['note3'], 'literalSHA256': canonical_sha(after_groups['note3']), 'primaryGround': 'NHLBI says the aorta carries blood leaving the heart to the rest of the body; this gives a concrete arterial route for the destination distractor.', 'sourcePaths': source_paths, 'locator': 'NHLBI blood-flow L118.'},
        ],
        'fourFullPromptAnswerNoteAssessments': [],
        'correctNoteNewFact': {'hasAdditionalFact': True, 'fact': 'The superior and inferior vena cava return blood from the body to the right atrium.', 'primaryLocator': 'NHLBI blood-flow L114.', 'beyondPromptAndKey': True},
        'absoluteDifficulty': {'frozenLevel': 'easy', 'assessment': 'Single-step recognition of the direction of venous blood flow, a broad adult-level circulation fact. The options are all short directional phrases. This does not require specialist knowledge or a multistep inference.', 'locator': 'NHLBI blood-flow L93, L114-L118.'},
    }],
    'peerAssessmentScope': 'Fresh globalMAIN 11000 rows plus all 100 actual current human-medicine cards; current SOURCE37 card and frozen unapplied proposal both assessed bilaterally. Full relevant cards included in peer-snapshot.json.',
    'proceduralDiagnostics': [
        'The proposed general vein-direction MAIN duplicates the actual current human-medicine-ext-vein-heart MAIN at sourceOrder 67: both ask that veins return blood to the heart. This is a direct entity-relation-value-context duplicate, so SOURCE status is HOLD until the question is reframed to test a distinct fact while preserving frozen difficulty/key constraints.',
        'The current human-medicine-artery-direction card and the frozen SOURCE37 proposal were each compared bilaterally with current/proposed38. SOURCE37 remains AUTHORHOLD0 and unapplied; its proposed systemic artery route is a direct reverse of the generic vein-direction proposal in the same circuit. This is recorded as related reciprocal context, not as adoption or application.',
        'A SOURCE38 web.open of the same OpenStax URL happened before the existing SOURCE37 capture was surfaced; that result was not used as evidence and is recorded as unused. After the exact saved SOURCE37 capture was supplied, it was reused for peer-context verification without further network calls. Its full output reports 236 lines and returns L0-L201 (202 line markers); relevant definitions are L31-L34, L91-L93 and L133-L140.',
    ],
}
for slot, a in enumerate(proposed['answers']):
    triple = {'prompt': proposed['prompt'], 'answer': a['text'], 'note': a['note']}
    if slot == 0:
        ground, locator, paths = 'The answer is a plausible arterial direction, but not the direction of veins. NHLBI explicitly distinguishes arteries moving blood away from the heart.', 'NHLBI blood-flow L93 and L118.', source_paths
        grammar = 'The bare prepositional phrase completes the question naturally: veins carry blood away from the heart.'
        plaus = 'A coherent reverse-direction distractor: arteries carry blood away from the heart; veins bring blood to it.'
        unique = 'Wrong for veins because it reverses the direction stated in the primary source.'
        useful = 'The note identifies the arterial route away from the heart and names the aorta as an example.'
    elif slot == 1:
        ground, locator, paths = 'The correct answer is the general heartward direction of veins. The specific vena cava route adds a concrete fact about this option.', 'NHLBI blood-flow L93 and L114.', source_paths
        grammar = 'The phrase completes the question naturally and agrees with the prompt.'
        plaus = 'The general venous direction is uniquely heartward; pulmonary and systemic examples both return blood to the heart.'
        unique = 'Only this option gives the general direction for veins; the other directions describe arterial routes.'
        useful = 'The note gives a specific return route from the body into the right atrium.'
    elif slot == 2:
        ground, locator, paths = 'The pulmonary artery carries blood from the heart to the lungs; it is not a vein and does not answer the question.', 'NHLBI blood-flow L114-L115.', source_paths
        grammar = 'The destination phrase is a natural completion of the question.'
        plaus = 'The lungs are a real destination in pulmonary circulation, making this a plausible circulation distractor.'
        unique = 'The official page assigns this heart-to-lung route to the pulmonary artery, while veins return blood to the heart.'
        useful = 'The note identifies the pulmonary artery as the vessel carrying blood from the heart to the lungs.'
    else:
        ground, locator, paths = 'The aorta carries blood away from the heart to the rest of the body, so organs are a destination for arterial rather than venous flow.', 'NHLBI blood-flow L93 and L118.', source_paths
        grammar = 'The destination phrase is a natural completion of the question.'
        plaus = 'Organs are a familiar destination in systemic circulation, so this is a plausible direction distractor.'
        unique = 'NHLBI identifies the aorta as taking blood from the heart to the body; the question asks about veins.'
        useful = 'The note names the aorta as the arterial route distributing blood from the heart to body tissues.'
    source_evidence['entries'][0]['fourFullPromptAnswerNoteAssessments'].append({
        'slot': slot, 'fullPrompt': proposed['prompt'], 'answer': a['text'], 'note': a['note'],
        'grammar': grammar, 'plausibilityUniqueKeyAndNoteTruthUsefulness': f'{ground} {plaus} {unique} {useful}',
        'sourcePaths': paths, 'locator': locator, 'tripleSHA256': canonical_sha(triple),
    })
write_json('sourceproof.json', source_evidence)

peer_ids = ['human-medicine-artery-direction', 'human-medicine-ext-artery-heart', 'human-medicine-ext-vein-heart', 'human-medicine-hepatic-portal-vein']
peer_rows = [copy.deepcopy(x) for x in inv['actualCurrentPeers'] if x['id'] in peer_ids]
assert len(peer_rows) == 4
peer_by_id = {x['id']: x for x in peer_rows}
pair_assessments = [
    {
        'peerId': 'human-medicine-ext-vein-heart', 'peerSourceOrder': 67,
        'candidateCard': proposed, 'candidateCanonicalSHA256': canonical_sha(proposed),
        'actualCurrentPeer': peer_by_id['human-medicine-ext-vein-heart'],
        'candidateToPeer': 'Both ask which direction veins carry blood / which vessels return blood to the heart. Entity=veins; relation=return/carry; value=toward heart; context=general circulation. Direct semantic duplicate.',
        'peerToCandidate': 'The peer answer names veins as returning blood to the heart; this candidate asks the same generic direction fact. Exact reverse/converse test does not distinguish them because the directions align identically.',
        'directReverseCheck': 'No direct reverse between these two cards; they are same-direction duplicates.',
        'verdict': 'DUPLICATE_HOLD',
    },
    {
        'peerId': 'human-medicine-artery-direction', 'peerSourceOrder': 37,
        'candidateCard': proposed, 'candidateCanonicalSHA256': canonical_sha(proposed),
        'actualCurrentPeer': peer_by_id['human-medicine-artery-direction'],
        'candidateToPeer': 'Shared broad context is vessel-flow direction, but entity differs: veins return blood toward the heart; arteries carry it away. The value is a reciprocal contrast rather than the same fact.',
        'peerToCandidate': 'The artery question does not answer the vein question; its source and direction are the opposite vessel class. Readers must know both categories.',
        'directReverseCheck': 'Explicitly checked as a reciprocal pair; distinct entities and physiological roles make the pair complementary rather than duplicate.',
        'verdict': 'RELATED_COMPLEMENTARY',
    },
    {
        'peerId': 'human-medicine-ext-artery-heart', 'peerSourceOrder': 66,
        'candidateCard': proposed, 'candidateCanonicalSHA256': canonical_sha(proposed),
        'actualCurrentPeer': peer_by_id['human-medicine-ext-artery-heart'],
        'candidateToPeer': 'The peer asks which vessels carry blood away from the heart; this candidate asks about venous flow toward the heart. Opposite vessel class and direction.',
        'peerToCandidate': 'The artery answer cannot answer the venous direction question; it is the reciprocal relation, not the same MAIN.',
        'directReverseCheck': 'Checked; the pair is complementary by vessel class and flow direction.',
        'verdict': 'RELATED_COMPLEMENTARY',
    },
    {
        'peerId': 'human-medicine-hepatic-portal-vein', 'peerSourceOrder': 25,
        'candidateCard': proposed, 'candidateCanonicalSHA256': canonical_sha(proposed),
        'actualCurrentPeer': peer_by_id['human-medicine-hepatic-portal-vein'],
        'candidateToPeer': 'The peer asks for the specific hepatic portal route from digestive organs to the liver; this candidate asks the general direction of veins relative to the heart. Entity subtype/context and relation differ.',
        'peerToCandidate': 'Knowing the hepatic portal route does not answer the generic venous direction prompt; portal blood then continues through liver veins, a distinct pathway.',
        'directReverseCheck': 'No direct reverse; the hepatic portal pathway is a distinct circulation route.',
        'verdict': 'RELATED_NOT_DUPLICATE',
    },
]
pair_assessments.extend([
    {
        'peerId': 'human-medicine-artery-direction', 'peerSourceOrder': 37,
        'peerStage': 'SOURCE37_CURRENT', 'candidateCard': proposed, 'candidateCanonicalSHA256': canonical_sha(proposed),
        'actualCurrentPeer': peer_by_id['human-medicine-artery-direction'],
        'concurrentProposal': s37_entry['proposedCard'], 'concurrentProposalCanonicalSHA256': canonical_sha(s37_entry['proposedCard']),
        'concurrentProposalStatus': 'HOLD_UNAPPLIED',
        'candidateToPeer': 'The SOURCE37 proposed prompt narrows arteries to the systemic circuit and asks for heart-to-body direction. The proposed38 general vein-to-heart direction is its direct reverse in the same circulation context.',
        'peerToCandidate': 'Systemic arteries move blood from heart to body; veins return it toward the heart. Each answer tests the reciprocal half of the same circuit, so the pair is a high-overlap/direct-reverse relationship that needs adjudication before either is counted.',
        'directReverseCheck': 'Checked current37 and proposed37 against current38 and proposed38. Current artery direction and proposed systemic artery direction are each reciprocal to vein heartward flow. Proposal37 remains unapplied and is not treated as certified evidence.',
        'verdict': 'RELATED_DIRECT_REVERSE_HOLD',
        'concurrentTaskEvidence': {
            'candidatePath': str(S37_CANDIDATE_PATH), 'candidateFileSHA256': file_sha(S37_CANDIDATE_PATH),
            'rawPath': str(S37_RAW_PATH), 'rawFileSHA256': file_sha(S37_RAW_PATH),
            'sourceNativeId': s37_raw['sourceNativeId'], 'nativeRecordLine': s37_raw['nativeRecordLine'],
            'completeOutputPointer': s37_raw['completeOutputPointer'], 'completeOutputSHA256': s37_raw['completeOutputSHA256'],
            'reportedPageLines': 236, 'returnedPageLines': 'L0-L201', 'returnedLineCount': 202,
            'reusedLocators': 'L31-L34, L91-L93, L133-L140',
        },
    },
    {
        'peerId': 'human-medicine-artery-direction', 'peerSourceOrder': 37,
        'peerStage': 'SOURCE37_CURRENT', 'candidateCard': current, 'candidateCanonicalSHA256': canonical_sha(current),
        'actualCurrentPeer': peer_by_id['human-medicine-artery-direction'],
        'concurrentProposal': s37_entry['proposedCard'], 'concurrentProposalCanonicalSHA256': canonical_sha(s37_entry['proposedCard']),
        'concurrentProposalStatus': 'HOLD_UNAPPLIED',
        'candidateToPeer': 'The current vein card asks the generic direction of veins; the current artery card asks the generic direction of arteries. They test reciprocal directions in a shared vessel-flow frame.',
        'peerToCandidate': 'The current artery card asks which way blood moves in arteries; the current vein card asks the opposite direction in veins. This relationship is distinct by vessel type but an explicit reciprocal pair.',
        'directReverseCheck': 'Both original/current cards personally compared. Proposed37 was inspected but not applied to current MAIN.',
        'verdict': 'RELATED_DIRECT_REVERSE',
        'concurrentTaskEvidence': {'candidatePath': str(S37_CANDIDATE_PATH), 'candidateFileSHA256': file_sha(S37_CANDIDATE_PATH), 'status': 'HOLD_UNAPPLIED'},
    },
])

write_json('peer-snapshot.json', {
    'sourceNativeId': NATIVE, 'topicId': 'human-medicine', 'cycle': 0,
    'inventory': {'path': str(inv_path), 'fileSHA256': file_sha(inv_path)},
    'globalMAIN': inv['globalMAIN'],
    'sameTopicMAIN': inv['sameTopicMAIN'],
    'actualCurrentPeers': inv['actualCurrentPeers'],
    'relevantPeerIds': peer_ids,
    'relevantPairs': pair_assessments,
    'concurrentSource37': {'candidatePath': str(S37_CANDIDATE_PATH), 'candidateFileSHA256': file_sha(S37_CANDIDATE_PATH), 'status': 'AUTHORHOLD0', 'catalog37': 'UNCHANGED', 'proposal': 'UNAPPLIED', 'proposedCard': s37_entry['proposedCard'], 'proposedCardCanonicalSHA256': canonical_sha(s37_entry['proposedCard']), 'beforeHash': s37_entry['beforeHash'], 'afterHash': s37_entry['afterHash']},
    'reusedPeerSourceContext': {'path': str(S37_RAW_PATH), 'fileSHA256': file_sha(S37_RAW_PATH), 'sourceNativeId': s37_raw['sourceNativeId'], 'url': s37_raw['url'], 'nativeRecordLine': s37_raw['nativeRecordLine'], 'completeOutputPointer': s37_raw['completeOutputPointer'], 'completeOutputSHA256': s37_raw['completeOutputSHA256'], 'reportedTotalLines': 236, 'returnedLines': 'L0-L201', 'usedLocators': 'L31-L34, L91-L93, L133-L140'},
    'simultaneousProposalAvailability': 'Frozen SOURCE37 proposal was available for bilateral comparison; its AUTHORHOLD0/unapplied state is preserved and not adopted.',
    'qualityCredit': 0,
})

print(json.dumps({
    'status': 'HOLD', 'id': proposed['id'], 'beforeHash': canonical_sha(current), 'afterHash': canonical_sha(proposed),
    'inventoryFileSHA256': file_sha(inv_path), 'globalMAINRows': len(inv['globalMAIN']['rows']),
    'topicPeers': len(inv['actualCurrentPeers']), 'rawSourceFileSHA256': file_sha(RAW),
    'outputs': ['candidate.json', 'sourceproof.json', 'peer-snapshot.json'], 'qualityCredit': 0,
}, ensure_ascii=False, indent=2))
