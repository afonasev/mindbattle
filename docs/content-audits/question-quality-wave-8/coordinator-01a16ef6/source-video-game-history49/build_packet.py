import copy
import hashlib
import json
from pathlib import Path

C = Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle')
OUT = C / 'docs/content-audits/question-quality-wave-8/coordinator-01a16ef6/source-video-game-history49'
INV = OUT / 'fresh-inventory.json'
TOPIC = C / 'src/content/topics/video-game-history.json'
NATIVE = '01a16f1a-0b52-7513-a747-34db0c50e308'
JOURNAL = '/Users/eaafonasev/.codex/sessions/2026/10/24/rollout-2026-10-24T23-09-00-01a16f1a-0b52-7513-a747-34db0c50e308.jsonl'

def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))

def sha(value):
    return hashlib.sha256(canonical(value).encode('utf-8')).hexdigest()

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

def ground(group, literal):
    if group == 'prompt_ordered_answers_key':
        return (
            'Microsoft defines Game Saves as preserving player progression so a game can continue with progress intact across platforms, devices and stores (Microsoft L34-L43). '
            'Unity explicitly calls persistence across application runs a save-game function and documents saving and loading stored state (Unity WorldAnchor L76-L104). '
            'The four choices are distinct game functions: a publisher describes a title with all levels open from the start (Nintendo L88-L103); Unity defines pausing through zero timeScale (Unity Time L239-L246); and Unity separately provides deletion/clearing of saved records (WorldAnchor L104). '
            'Only continuing from recorded state matches the save function asked about.'
        ), ['microsoft', 'nintendo', 'unity_pause', 'unity_worldanchor'], 'Microsoft L32-L43; Unity WorldAnchor L76-L104; Unity Time L239-L246; Nintendo L88-L103.'
    if group == 'explanation':
        return (
            'Microsoft states that Game Saves lets players continue with progress intact when switching platforms, devices or stores (L34) and describes progression continuity and rollback support (L36-L43). '
            'Unity independently gives a concrete save/load example across application runs (WorldAnchor L76-L104).'
        ), ['microsoft', 'unity_worldanchor'], 'Microsoft L32-L43; Unity WorldAnchor L76-L104.'
    if group == 'note0':
        return (
            'Nintendo UK reproduces the publisher description for The Little Mermaid: Wonder Puzzles: all levels are unlocked from the start (L88-L103). '
            'This is a concrete fact about the answer option’s level-unlocking function.'
        ), ['nintendo'], 'Nintendo L88-L103.'
    if group == 'note1':
        return (
            'Microsoft states that Game Saves lets players continue with progress intact when switching across platforms, devices and stores (L34), and that it maintains a consistent point of progression (L36-L43).'
        ), ['microsoft'], 'Microsoft L32-L43.'
    if group == 'note2':
        return (
            'Unity states that setting Time.timeScale to zero makes the application act as if paused when its functions are frame-rate independent (L239-L246).'
        ), ['unity_pause'], 'Unity Time L238-L246.'
    if group == 'note3':
        return (
            'Unity states that WorldAnchorStore provides Delete and Clear methods to remove one saved anchor or all anchors from the store (L104).'
        ), ['unity_worldanchor'], 'Unity WorldAnchor L93-L104.'
    raise ValueError(group)

inventory = json.loads(INV.read_text())
before = json.loads(TOPIC.read_text())['questions'][48]
assert before['id'] == 'video-game-history-save-game'
assert sha(before) == '91c24f8f3161ba5b6da53f4afbbda0a82c5154e5bd53755d4b436497b102844a'
proposed = copy.deepcopy(before)
proposed['answers'][0]['text'] = 'Открыть все уровни'
proposed['answers'][0]['note'] = 'В описании издателя игры The Little Mermaid: Wonder Puzzles сказано, что все уровни открыты с самого начала.'
proposed['answers'][1]['note'] = 'Microsoft Game Saves позволяет продолжить игру с сохранённым прогрессом при переходе между платформами, устройствами и магазинами.'
proposed['answers'][2]['text'] = 'Временно приостановить игру'
proposed['answers'][2]['note'] = 'В Unity при Time.timeScale = 0 приложение ведёт себя как на паузе, если все функции независимы от частоты кадров.'
proposed['answers'][3]['text'] = 'Удалить сохранённые данные'
proposed['answers'][3]['note'] = 'В Unity WorldAnchorStore методы Delete и Clear удаляют один сохранённый якорь или все записи якорей.'
proposed['explanation'] = (
    'Правильный ответ — продолжить игру с записанного состояния: сохранение фиксирует прогресс, который можно восстановить позднее. '
    'Microsoft описывает Game Saves как способ продолжить игру с сохранённым прогрессом при переходе между платформами, устройствами и магазинами.'
)
proposed['source'] = {
    'title': 'Microsoft Learn: Game Saves overview',
    'url': 'https://learn.microsoft.com/en-us/gaming/playfab/player-progression/game-saves/overview',
    'verifiedAt': '2026-10-24',
}
before_groups, after_groups = groups(before), groups(proposed)
field_groups = {
    key: {'beforeCanonicalSHA256': sha(before_groups[key]), 'afterCanonicalSHA256': sha(after_groups[key])}
    for key in before_groups
}
candidate = {
    'sourceNativeId': NATIVE,
    'topicId': 'video-game-history',
    'cycle': 0,
    'entries': [{
        'id': 'video-game-history-save-game',
        'topicId': 'video-game-history',
        'sourceOrder': 49,
        'status': 'READY_FOR_INDEPENDENT_REVIEW',
        'beforeCard': before,
        'beforeHash': sha(before),
        'proposedCard': proposed,
        'afterHash': sha(proposed),
        'fieldGroups': field_groups,
    }],
}

source_defs = {
    'unity_worldanchor': {
        'path': OUT / 'unity-worldanchor-capture.json',
        'url': 'https://docs.unity3d.com/cn/2018.3/Manual/windowsholographic-persistence.html',
        'locator': 'L76-L79: persistence saves WorldAnchor state across runs and is described as save-game functionality; L93-L104: saved state is loaded and can be deleted/cleared.',
        'title': 'Unity Manual: HoloLens WorldAnchor persistence',
    },
    'microsoft': {
        'path': OUT / 'microsoft-gamesaves-capture.json',
        'url': 'https://learn.microsoft.com/en-us/gaming/playfab/player-progression/game-saves/overview',
        'locator': 'L32-L43: Game Saves lets players continue with progress intact across platforms, devices and stores; it maintains a consistent point of progression and supports rollback.',
        'title': 'Microsoft Learn: Game Saves overview',
    },
    'nintendo': {
        'path': OUT / 'nintendo-levels-capture.json',
        'url': 'https://www.nintendo.com/en-gb/Games/Nintendo-Switch-download-software/The-Little-Mermaid-Wonder-Puzzles-2626292.html',
        'locator': 'L88-L103: publisher description says all levels in The Little Mermaid: Wonder Puzzles are unlocked from the start.',
        'title': 'Nintendo UK: The Little Mermaid: Wonder Puzzles',
    },
    'unity_pause': {
        'path': OUT / 'unity-pause-capture.json',
        'url': 'https://docs.unity3d.com/ScriptReference/Time-timeScale.html',
        'locator': 'L238-L246: when Time.timeScale is zero, the application acts as if paused if all functions are frame-rate independent.',
        'title': 'Unity Scripting API: Time.timeScale',
    },
}
raw_sources = []
for key, spec in source_defs.items():
    cap = json.loads(spec['path'].read_text())
    raw_sources.append({
        'path': spec['path'].relative_to(C).as_posix(),
        'url': spec['url'],
        'title': spec['title'],
        'sha256': file_sha(spec['path']),
        'captureReadProvenance': (
            f"Full web.open response personally read; sourceNativeId {NATIVE}, native journal {JOURNAL}, "
            f"native record line {cap['nativeRecordLine']}; pointer {cap['completeOutputPointer']}, "
            f"complete output SHA256 {cap['completeOutputSHA256']}; captured once."
        ),
        'locator': spec['locator'],
        'completeOutputPointer': cap['completeOutputPointer'],
        'completeOutputSHA256': cap['completeOutputSHA256'],
    })

path_by_key = {k: v['path'].relative_to(C).as_posix() for k, v in source_defs.items()}
literal_groups = []
for key, literal in after_groups.items():
    primary_ground, keys, locator = ground(key, literal)
    literal_groups.append({
        'group': key,
        'literal': literal,
        'literalSHA256': sha(literal),
        'primaryGround': primary_ground,
        'sourcePaths': [path_by_key[k] for k in keys],
        'locator': locator,
    })

variant_specs = [
    ('Nintendo publisher describes all levels as available from the start; this is a level-access state, distinct from restoring saved progression. The alternatives are parallel infinitive game functions, and only the key describes resuming recorded progress.', ['nintendo', 'microsoft'], 'Nintendo L88-L103; Microsoft L32-L43.'),
    ('This is the unique key: it alone describes continuing from stored progress. Microsoft explicitly says Game Saves preserves progression for continuation across devices/platforms. The note adds that cross-device/platform scope.', ['microsoft'], 'Microsoft L32-L43.'),
    ('Unity documents Time.timeScale = 0 as making the application act as if paused, which is a temporary runtime stop and does not restore a saved state. The wording is a parallel infinitive and is a plausible neighboring game function.', ['unity_pause'], 'Unity Time L238-L246.'),
    ('This option describes deletion, not recording and later restoration. Unity documents Delete/Clear as removal operations on saved WorldAnchor records; it cannot be confused with the continuation purpose stated for Game Saves.', ['unity_worldanchor', 'microsoft'], 'Unity WorldAnchor L93-L104; Microsoft L32-L43.'),
]
variants = []
for slot, answer_obj in enumerate(proposed['answers']):
    triple = {'prompt': proposed['prompt'], 'answer': answer_obj['text'], 'note': answer_obj['note']}
    assessment, keys, locator = variant_specs[slot]
    variants.append({
        'slot': slot,
        'fullPrompt': proposed['prompt'],
        'answer': answer_obj['text'],
        'note': answer_obj['note'],
        'grammar': 'The prompt takes a parallel infinitive completion; all four answers use an infinitive verb phrase with a consistent accusative object or complement.',
        'plausibilityUniqueKeyAndNoteTruthUsefulness': assessment,
        'sourcePaths': [path_by_key[k] for k in keys],
        'locator': locator,
        'tripleSHA256': sha(triple),
    })

sourceproof = {
    'sourceNativeId': NATIVE,
    'topicId': 'video-game-history',
    'cycle': 0,
    'id': 'video-game-history-save-game',
    'rawSources': raw_sources,
    'entries': [{
        'id': 'video-game-history-save-game',
        'status': 'READY_FOR_INDEPENDENT_REVIEW',
        'literalGroups': literal_groups,
        'fourFullPromptAnswerNoteAssessments': variants,
        'correctNoteNewFact': {
            'fact': 'Microsoft Game Saves lets a player continue with progress intact when switching between platforms, devices and stores.',
            'whyAdditional': 'The prompt/key state the basic save-and-continue function; the note adds the specific cross-platform/device/store use case.',
            'sourcePaths': [path_by_key['microsoft']],
            'locator': 'L32-L43, especially L34 and L40.',
        },
        'absoluteDifficulty': {
            'level': 'easy',
            'audienceAndReasoningGround': 'For a broad adult audience, the ordinary idea of saving a game to continue later is familiar and requires no specialist knowledge or multistep reasoning. The alternative actions are recognizable game functions but differ from preserving progress.',
            'sourcePaths': [path_by_key['microsoft'], path_by_key['unity_worldanchor']],
            'locator': 'Microsoft L32-L43; Unity WorldAnchor L76-L104.',
        },
        'frozen': {
            'id': 'video-game-history-save-game',
            'topicId': 'video-game-history',
            'sourceOrder': 49,
            'difficulty': 'easy',
            'correctIndex': 1,
        },
    }],
    'sourceAccounting': {
        'sourceSearches': 'Discovery searches were used to identify official documentation; their result snippets are not treated as evidence. The cited facts above come from personally read full web.open captures.',
        'boundedRequests': 'Each captured page was checked against exact URL fences before opening. All four page bodies were captured once and retained; no failed-source retry or adjacent HOLD adoption was used.',
        'unusedDiscoveryCapture': 'The Unity Application.targetFrameRate page was opened during exploration but was not used in the proposal; its owned capture is excluded from rawSources and quality claims.',
    },
}

peers = inventory['actualCurrentPeers']
assert len(peers) == 100 and all(x['topicId'] == 'video-game-history' for x in peers)
by_id = {x['id']: x for x in peers}
target = by_id['video-game-history-save-game']
assert target['sha256'] == sha(before)
relevant_ids = ['video-game-history-ext-pause-term', 'video-game-history-controller-purpose']
relevant = [by_id[i] for i in relevant_ids]
peer_snapshot = {
    'sourceNativeId': NATIVE,
    'topicId': 'video-game-history',
    'cycle': 0,
    'id': 'video-game-history-save-game',
    'baselineCode': 'b8193ec1c533e06195db28f392504e36039d814f',
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
    'actualCurrentPeers': peers,
    'relevantPeerReadings': [
        {
            'peer': p,
            'mainAssessment': (
                'The peer asks for the purpose of a controller and includes game-data storage as a distinct device function. '
                'The target asks what saving enables. They share the general game-data domain but not entity/relation/value/context; neither restates nor reverses the other.'
                if p['id'] == 'video-game-history-controller-purpose' else
                'The peer defines a temporary pause; the target defines persistent recording and later continuation. '
                'Both can let play resume, but their relations and time contexts differ (temporary in-session halt versus restoration from stored state). Neither is a direct reverse or semantic duplicate.'
            ),
            'directReverse': 'No. The target concerns persisting/reloading progress; this peer concerns controller input.' if p['id'] == 'video-game-history-controller-purpose' else 'No. A pause does not persist a state, and saving does not merely halt the active session.',
        }
        for p in relevant
    ],
    'relevantProposedPairs': [],
    'inventoryProvenance': {
        'path': INV.relative_to(C).as_posix(),
        'freshInventorySHA256': file_sha(INV),
        'sourceOrder': 49,
        'targetPointer': '/sameTopicMAIN/questions/48',
        'globalMAINPointer': '/globalMAIN/rows',
        'fullTopicPeersPointer': '/actualCurrentPeers',
        'selfIsNotDistinctPeer': True,
        'relevantCrossTopicSearch': 'In the two relevant game catalog topics (modern-video-games and video-game-history), only the target and a pause-term question matched exact save/progress/state terms; the other matches concerned The Sims 4 interactions and Prince of Persia memory shards and were not semantically relevant.',
    },
}

write('candidate.json', candidate)
write('sourceproof.json', sourceproof)
write('peer-snapshot.json', peer_snapshot)

print(json.dumps({
    'candidate': str(OUT / 'candidate.json'),
    'sourceproof': str(OUT / 'sourceproof.json'),
    'peerSnapshot': str(OUT / 'peer-snapshot.json'),
    'beforeHash': sha(before),
    'afterHash': sha(proposed),
    'sixGroups': len(literal_groups),
    'fourVariants': len(variants),
    'topicPeers': len(peers),
    'globalRows': len(inventory['globalMAIN']['rows']),
    'rawSources': len(raw_sources),
    'qualityCredit': 0,
}, ensure_ascii=False))
