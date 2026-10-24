import copy
import hashlib
import json
from pathlib import Path

C = Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle')
BASE = C / 'docs/content-audits/question-quality-wave-8/coordinator-01a16ef6'
OUT = BASE / 'source-video-game-history49-cycle1'
INITIAL_DIR = BASE / 'source-video-game-history49'
INV = OUT / 'fresh-inventory.json'
NATIVE = '01a16f1a-0b52-7513-a747-34db0c50e308'
STATUS = 'READY_FOR_INDEPENDENT_REVIEW'

def canon(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))

def sha(value):
    return hashlib.sha256(canon(value).encode('utf-8')).hexdigest()

def file_sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def write(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

def groups(card):
    return {
        'prompt_ordered_answers_key': {
            'prompt': card['prompt'],
            'answers': [a['text'] for a in card['answers']],
            'correctIndex': card['correctIndex'],
        },
        'explanation': card['explanation'],
        **{'note' + str(i): a['note'] for i, a in enumerate(card['answers'])},
    }

def pointer_path(relative):
    return str((C / relative).resolve())

before_candidate = json.loads((INITIAL_DIR / 'candidate.json').read_text())
before_entry = before_candidate['entries'][0]
before = copy.deepcopy(before_entry['proposedCard'])
assert before_entry['afterHash'] == '19c30b4b5a7686429e9971e1d352d6dd1a39e9cb0ccde035654185102d896b3a'
assert sha(before) == before_entry['afterHash']
inventory = json.loads(INV.read_text())
live = inventory['sameTopicMAIN']['questions'][48]
assert sha(live) == before_entry['afterHash']

proposed = copy.deepcopy(before)
proposed['answers'][2]['note'] = (
    'В Unity параметр Time.timeScale задаёт темп игрового времени относительно реального. '
    'При нулевом значении игра действует как на паузе, если результат работы её функций не зависит от числа кадров в секунду.'
)
proposed['answers'][3]['note'] = (
    'В руководстве Unity 2018.3 для HoloLens сохранённый World Anchor — точка в физическом мире, например место игрового поля. '
    'Это руководство описывает удаление одного якоря методом Delete и всех якорей методом Clear.'
)

before_groups, after_groups = groups(before), groups(proposed)
candidate = {
    'sourceNativeId': NATIVE,
    'topicId': 'video-game-history',
    'cycle': 1,
    'entries': [{
        'id': 'video-game-history-save-game',
        'topicId': 'video-game-history',
        'sourceOrder': 49,
        'status': STATUS,
        'beforeCard': before,
        'beforeHash': sha(before),
        'proposedCard': proposed,
        'afterHash': sha(proposed),
        'fieldGroups': {
            key: {'beforeCanonicalSHA256': sha(before_groups[key]), 'afterCanonicalSHA256': sha(after_groups[key])}
            for key in before_groups
        },
    }],
}

sourceproof = json.loads((INITIAL_DIR / 'sourceproof.json').read_text())
sourceproof['sourceNativeId'] = NATIVE
sourceproof['cycle'] = 1
sourceproof['sourceInventoryPath'] = str(INV)
sourceproof['sourceInventorySHA256'] = file_sha(INV)
sourceproof['mechanicalIntake'] = {
    'rawPacket': 'source-video-game-history49-cycle1',
    'priorPacket': 'source-video-game-history49/sourceproof.json',
    'operation': 'One directed cycle1 clarity repair to note2 and note3; existing source bodies and all other card fields retained unchanged.',
}
entry = sourceproof['entries'][0]
entry['status'] = STATUS
entry['cycle'] = 1
new_note2 = proposed['answers'][2]['note']
new_note3 = proposed['answers'][3]['note']
literal_by_group = {k: v for k, v in after_groups.items()}
ground_by_group = {
    'note2': (
        'Unity defines Time.timeScale as the rate of in-game time relative to real time (L239). '
        'It states that at zero the application behaves as paused when its functions are frame-rate independent (L243-L246). '
        'The revised Russian explains both the time-scale expression and this material condition in plain language.'
    ),
    'note3': (
        'The Unity 2018.3 HoloLens manual defines WorldAnchor persistence as saving physical-world locations across application runs, '
        'with remembering a game board location as its example (L5,L74-L79). It separately says Delete removes one anchor and Clear removes all anchors (L104). '
        'The revision names the historical HoloLens context, identifies the stored item as a real-world point, and accurately scopes the deletion fact to that example.'
    ),
}
locator_by_group = {
    'note2': 'Unity Time L238-L246, especially L239 and L243.',
    'note3': 'Unity WorldAnchor L5, L74-L79 and L104.',
}
for item in entry['literalGroups']:
    name = item['group']
    item['literal'] = literal_by_group[name]
    item['literalSHA256'] = sha(item['literal'])
    if name in ground_by_group:
        item['primaryGround'] = ground_by_group[name]
        item['locator'] = locator_by_group[name]
for item in entry['fourFullPromptAnswerNoteAssessments']:
    slot = item['slot']
    item['note'] = proposed['answers'][slot]['note']
    item['tripleSHA256'] = sha({'prompt': proposed['prompt'], 'answer': proposed['answers'][slot]['text'], 'note': item['note']})
    item['sourcePaths'] = [
        'docs/content-audits/question-quality-wave-8/coordinator-01a16ef6/source-video-game-history49/unity-pause-capture.json'
        if slot == 2 else
        'docs/content-audits/question-quality-wave-8/coordinator-01a16ef6/source-video-game-history49/unity-worldanchor-capture.json'
        if slot == 3 else path
        for path in item['sourcePaths']
    ]
    if slot == 2:
        item['grammar'] = 'The answer remains a parallel infinitive completion. The Russian note is two complete clauses; Time.timeScale is immediately defined as the rate of game time relative to real time, and the documented condition is retained in ordinary terms.'
        item['plausibilityUniqueKeyAndNoteTruthUsefulness'] = 'Pause is a plausible neighboring game action, but it temporarily halts the running session while saving preserves state for later restoration. Unity says zero timeScale acts as pause if functions are frame-rate independent (L239-L246); the note now explains the parameter and condition for a general reader.'
        item['locator'] = locator_by_group['note2']
    elif slot == 3:
        item['grammar'] = 'The answer remains a parallel infinitive completion. The two-sentence Russian note clearly identifies the Unity 2018.3 HoloLens example, defines a World Anchor as a physical-world point, and states the delete/clear distinction.'
        item['plausibilityUniqueKeyAndNoteTruthUsefulness'] = 'Deletion is a plausible save-management action but differs from recording and restoring progress. The retained manual is explicitly a Unity 2018.3 HoloLens example; it describes saving physical locations such as a game-board position and deleting one/all anchors (L5,L74-L79,L104). The revised note no longer implies that these are generic player-progress files.'
        item['locator'] = locator_by_group['note3']

snapshot0 = json.loads((INITIAL_DIR / 'peer-snapshot.json').read_text())
current_peers = inventory['actualCurrentPeers']
assert len(current_peers) == 100 and all(x['topicId'] == 'video-game-history' for x in current_peers)
current_by_id = {p['id']: p for p in current_peers}
pair_assessments = {
    'video-game-history-ext-pause-term': {
        'leftToRight': 'The proposed target concerns persisting and later restoring game progress; this peer concerns the term for a temporary halt. Both may precede resumed play, but persistence versus in-session pause differs in relation and temporal context.',
        'rightToLeft': 'The pause peer does not identify save/load behavior; the proposed target does not define the name of a temporary pause. They are related functions, not the same fact.',
        'directReverseCheck': 'No direct reverse. A pause does not persist state, and saving is not simply a temporary halt.',
    },
    'video-game-history-controller-purpose': {
        'leftToRight': 'The proposed target concerns storing game progress for later continuation; this peer asks what a controller does and distinguishes it from storage. They share the broad game-data domain but have different entities and relations.',
        'rightToLeft': 'The controller-purpose peer is about player input hardware, while the proposed target is about persistent game state. Neither states or reverses the other.',
        'directReverseCheck': 'No direct reverse. Controller input and save-state persistence are distinct functions.',
    },
}
proposed_pairs = []
for peer_id, assessment in pair_assessments.items():
    peer = current_by_id[peer_id]
    proposed_pairs.append({
        'left': {
            'id': proposed['id'],
            'topicId': 'video-game-history',
            'sourceOrder': 49,
            'card': proposed,
            'canonicalSHA256': sha(proposed),
        },
        'right': peer,
        'mainAssessment': assessment,
    })
snapshot = {
    'sourceNativeId': NATIVE,
    'topicId': 'video-game-history',
    'cycle': 1,
    'id': 'video-game-history-save-game',
    'baselineCode': 'd8fe389b1b793cfd7b9f0b246dbffe6ee75dfb5b',
    'globalMAIN': {
        'topicFileCount': inventory['globalMAIN']['topicFileCount'],
        'questionCount': inventory['globalMAIN']['questionCount'],
        'rowsCanonicalSHA256': inventory['globalMAIN']['rowsCanonicalSHA256'],
        'allCurrentFileByteBindings': inventory['globalMAIN']['allCurrentFileByteBindings'],
        'rows': inventory['globalMAIN']['rows'],
    },
    'topicFile': {
        'path': inventory['sameTopicMAIN']['path'],
        'fileSHA256': inventory['sameTopicMAIN']['fileSHA256'],
        'questionCount': inventory['sameTopicMAIN']['questionCount'],
    },
    'actualCurrentPeers': current_peers,
    'relevantPeerReadings': snapshot0['relevantPeerReadings'],
    'relevantProposedPairs': proposed_pairs,
    'inventoryProvenance': {
        'path': str(INV),
        'freshInventorySHA256': file_sha(INV),
        'sourceOrder': 49,
        'targetPointer': '/sameTopicMAIN/questions/48',
        'globalMAINPointer': '/globalMAIN/rows',
        'fullTopicPeersPointer': '/actualCurrentPeers',
        'targetPreimageSHA256': sha(live),
        'selfIsNotDistinctPeer': True,
        'relevantPeerJudgmentsRetainedFromInitial': 'Only the two directed note defects changed; prompt, answers, key, explanation and peer relation judgments are unchanged. The exact INITIAL49 receipt is preserved by the coordinator and is not copied or replaced here.',
    },
}

write('candidate.json', candidate)
write('sourceproof.json', sourceproof)
write('peer-snapshot.json', snapshot)
print(json.dumps({
    'cycle': 1,
    'status': STATUS,
    'beforeHash': sha(before),
    'afterHash': sha(proposed),
    'changedFields': ['answers[2].note', 'answers[3].note'],
    'groups': len(entry['literalGroups']),
    'variants': len(entry['fourFullPromptAnswerNoteAssessments']),
    'topicPeers': len(current_peers),
    'globalRows': len(inventory['globalMAIN']['rows']),
    'qualityCredit': 0,
}, ensure_ascii=False))
