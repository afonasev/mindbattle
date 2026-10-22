import copy
import hashlib
import json
from pathlib import Path

C = Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle')
OUT = C / 'docs/content-audits/question-quality-wave-8/coordinator-01a16329/source-history-russia92'
INV = OUT / 'fresh-inventory.json'
NATIVE_ID = '01a16515-b407-74e2-b71b-1809a490cd2f'
NATIVE_JOURNAL = '/Users/eaafonasev/.codex/sessions/2026/10/23/rollout-2026-10-23T00-28-03-01a16515-b407-74e2-b71b-1809a490cd2f.jsonl'
TASK = C / 'docs/content-audits/question-quality-wave-8/coordinator-01a16329/source-history-russia92-task.json'


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')


def canonical_sha(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_json(path):
    return json.loads(Path(path).read_text())


def relative_to_c(path):
    return Path(path).resolve().relative_to(C).as_posix()


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


def source_record(path, url, title, intended_claim, prior_provenance=None, personal_coverage=None):
    p = C / path
    record = read_json(p)
    output_pointer = record['completeOutputPointer']
    # The capture helper's supported pointer is /originalRecord/payload/output/N/text.
    output_index = int(output_pointer.split('/')[4])
    body = record['originalRecord']['payload']['output'][output_index]['text']
    body_sha = hashlib.sha256(body.encode('utf-8')).hexdigest()
    assert body_sha == record['completeOutputSHA256']
    provenance = {
        'capturedAt': '2026-10-23',
        'originalTool': 'tools.web__run open',
        'sourceNativeId': NATIVE_ID,
        'nativeJournal': NATIVE_JOURNAL,
        'nativeRecordLine': record['nativeRecordLine'],
        'completeOutputPointer': output_pointer,
        'completeOutputSHA256': body_sha,
        'personalReadBy': NATIVE_ID,
        'readAt': '2026-10-23',
        'personalReadCoverage': personal_coverage,
        'limitation': intended_claim,
        'originalArgs': {'open': [{'ref_id': url}], 'response_length': 'long'},
    }
    return {
        'path': relative_to_c(p),
        'url': url,
        'title': title,
        'fileSHA256': file_sha(p),
        'sha256': file_sha(p),
        'completeOutputPointer': output_pointer,
        'completeOutputSHA256': body_sha,
        'locator': None,
        'captureReadProvenance': provenance,
    }


def reused_source(index_path, entry_index, current_coverage, claim_limit):
    index = read_json(index_path)
    source = index['rawSources'][entry_index]
    p = C / source['path']
    assert p.is_file()
    assert file_sha(p) == source.get('fileSHA256', source['sha256'])
    return {
        'path': source['path'],
        'url': source['url'],
        'title': source['title'],
        'fileSHA256': file_sha(p),
        'sha256': file_sha(p),
        'completeOutputPointer': source['completeOutputPointer'],
        'completeOutputSHA256': source['completeOutputSHA256'],
        'locator': source.get('locator'),
        'captureReadProvenance': copy.deepcopy(source['captureReadProvenance']),
        'currentAuthorReadEvidence': {
            'sourceNativeId': NATIVE_ID,
            'nativeJournal': NATIVE_JOURNAL,
            'readAt': '2026-10-23',
            'coverage': current_coverage,
            'limitation': claim_limit,
        },
    }


inventory = read_json(INV)
task = read_json(TASK)
assert task['authorNativeId'] == NATIVE_ID
assert task['id'] == 'history-russia-collective-farms-policy'
assert task['sourceOrder'] == 92 and task['topicId'] == 'history-russia'
assert inventory['globalMAIN']['topicFileCount'] == 110
assert inventory['globalMAIN']['questionCount'] == 11000
assert inventory['sameTopicMAIN']['questionCount'] == 100
before = copy.deepcopy(inventory['sameTopicMAIN']['questions'][91])
assert before['id'] == task['id']
assert canonical_sha(before) == task['beforeHash']
assert inventory['actualCurrentPeers'][91]['sha256'] == task['beforeHash']

proposed = copy.deepcopy(before)
proposed['answers'][0]['note'] = 'Первый пятилетний план СССР (1928–1932 гг.) ставил задачу превратить страну из аграрно-индустриальной в индустриальную.'
# The exact post-Stalin association in this note is inherited as an exhausted claim; preserve it and HOLD.
proposed['answers'][1]['note'] = before['answers'][1]['note']
proposed['answers'][2]['note'] = 'На XXVII съезде КПСС в 1986 году «гласность» была названа одним из основных лозунгов перестройки.'
proposed['answers'][3]['note'] = 'В статье «Головокружение от успехов» Сталин критиковал нарушения принципа добровольности вступления в колхозы.'
proposed['explanation'] = ('Коллективизация проводилась через вступление крестьянских хозяйств в колхозы. '
                          'По данным Президентской библиотеки, к 1 июля 1930 года в колхозы объединили '
                          '23,6% крестьянских хозяйств.')
proposed['source'] = {
    'title': 'В СССР началась массовая коллективизация | Президентская библиотека имени Б.Н. Ельцина',
    'url': 'https://www.prlib.ru/node/618998',
    'verifiedAt': '2026-10-23',
}

assert proposed['id'] == before['id']
assert proposed['difficulty'] == before['difficulty'] == 'medium'
assert proposed['correctIndex'] == before['correctIndex'] == 3
assert all(proposed['answers'][i]['text'] == before['answers'][i]['text'] for i in range(4))
assert len(proposed['answers']) == 4
assert len(proposed['explanation'].split()) <= 70
assert 2 <= len([x for x in proposed['explanation'].split('. ') if x.strip()]) <= 4
assert all(len(a['text'].encode('utf-16-le')) // 2 <= 140 for a in proposed['answers'])
assert all(len(a['note'].split()) <= 35 for a in proposed['answers'])

source48_index = C / 'docs/content-audits/question-quality-wave-8/coordinator-01a15fba/qualified-source-history-russia48/sourceproof.json'
source52_index = C / 'docs/content-audits/question-quality-wave-8/coordinator-01a15ff8/qualified-source-history-russia52/sourceproof.json'
source48_path = 'docs/content-audits/question-quality-wave-8/coordinator-01a15fba/source-history-russia48/raw/prlib-collectivization.json'
source52_path = 'docs/content-audits/question-quality-wave-8/coordinator-01a15d80/source-history-russia13/raw/prlib-gorbachev-1985.json'
primary_path = 'docs/content-audits/question-quality-wave-8/coordinator-01a16329/source-history-russia92/raw/first-five-year-primary.json'
alt_path = 'docs/content-audits/question-quality-wave-8/coordinator-01a16329/source-history-russia92/raw/first-five-year-official-alt.json'

raw_sources = [
    reused_source(
        source48_index, 1,
        'Personally read the full retained 123-line Presidential Library article. L40 gives the article heading and event date; L44-L51 describes collectivization measures and reports 23.6% of peasant households in kolkhozes by 1 July 1930.',
        'Supports the prompt/key, the additional correct-note fact, and the explanation only within the returned article.'),
    reused_source(
        source52_index, 0,
        'Personally read the full retained 135-line Presidential Library article. L50-L51 states the 1986 XXVII Congress policy was called perestroika and lists glasnost among its slogans.',
        'Supports the revised glasnost distractor note; it does not establish thaw claims.'),
    source_record(
        primary_path, 'https://www.prlib.ru/item/335419', 'Итоги первой пятилетки | Президентская библиотека имени Б.Н. Ельцина',
        'Insufficient primary attempt: the returned page is catalogue metadata for a 1933 report (157 pages), not its text; it does not verify the proposed date or industrialization claim.',
        personal_coverage='Personally read the complete returned 118-line page. L36-L46 identifies the report and its bibliographic data, but the report body is absent.'),
    source_record(
        alt_path, 'https://www.prlib.ru/sites/default/files/u535/12_sovetskoe_gosudarstvo_v_1920-1930-e_gg.pdf', 'Социалистическая модернизация СССР в середине 1920-х – 1930-е гг. | Президентская библиотека имени Б.Н. Ельцина',
        'Official alternative supports the revised first-five-year distractor note at page 6, lines 8-9 and 13-14; only the returned page-6 text is used.',
        personal_coverage='Personally read the complete returned extraction (15 lines from PDF page 6). L8-L9 states the transformation goal; L13-L14 gives the first five-year plan and 1928-1932 dates.'),
]
source_paths = [s['path'] for s in raw_sources]
path48 = source48_path
path52 = source52_path
path_primary = primary_path
path_alt = alt_path

before_groups, proposed_groups = groups(before), groups(proposed)
field_groups = {
    name: {
        'beforeCanonicalSHA256': canonical_sha(before_groups[name]),
        'afterCanonicalSHA256': canonical_sha(proposed_groups[name]),
    }
    for name in before_groups
}

literal_ground = {
    'prompt_ordered_answers_key': (
        'The retained official Presidential Library article is headed “В СССР началась массовая коллективизация” (L40) and '
        'describes the policy and kolkhoz entry (L44-L51), supporting the prompt and unique key. The official library PDF '
        'identifies the first five-year plan and its dates (page 6, L13-L14); the retained Gorbachev biography lists glasnost '
        'as a perestroika slogan (L50-L51). The current distractor note about the thaw repeats an exhausted post-Stalin association '
        'and remains unresolved, so this six-field group cannot be certified.'),
    'explanation': 'The retained Presidential Library primary article supports the collective-farm policy and the 1930 statistic (L40, L44-L51).',
    'note0': 'The official Presidential Library alternative gives 1928–1932 and the industrialization goal (page 6, L8-L9, L13-L14).',
    'note1': 'HOLD: this text states the exact post-Stalin thaw association inherited as exhausted in SOURCE76; no retry, alternative, or adjacent workaround is allowed. No adequate allowed retained body supports this literal.',
    'note2': 'The retained Presidential Library biography states that at the 1986 XXVII Congress glasnost was one of the slogans of perestroika (L50-L51).',
    'note3': 'The retained Presidential Library primary article says Stalin’s 2 March 1930 article criticized violations of the voluntary-entry principle (L50). This distinct own-option fact avoids repeating the current GOELRO peer’s identical 1930 statistic note.',
}
source_path_by_group = {
    'prompt_ordered_answers_key': [path48, path_alt, path52],
    'explanation': [path48],
    'note0': [path_alt],
    'note1': [],
    'note2': [path52],
    'note3': [path48],
}

literal_groups = [
    {
        'group': name,
        'literal': proposed_groups[name],
        'literalSHA256': canonical_sha(proposed_groups[name]),
        'primaryGround': literal_ground[name],
        'sourcePaths': source_path_by_group[name],
        'locator': {
            'prompt_ordered_answers_key': 'source48 L40, L44-L51; official PDF page 6 L7-L14; source52 L50-L51; thaw limitation: task priorSourceAttemptMetadata.boundary and predecessor handoff source82 fence.',
            'explanation': 'source48 complete returned page L40, L44-L51.',
            'note0': 'official-alternative PDF page 6 L8-L9, L13-L14.',
            'note1': 'HOLD: exact inherited SOURCE76 post-Stalin-thaw association; no permitted retry or alternative.',
            'note2': 'source52 complete returned page L50-L51.',
            'note3': 'source48 complete returned page L50.',
        }[name],
    }
    for name in proposed_groups
]

variant_evidence = [
    {
        'slot': 0,
        'fullPrompt': proposed['prompt'],
        'answer': proposed['answers'][0]['text'],
        'note': proposed['answers'][0]['note'],
        'tripleSHA256': canonical_sha({'prompt': proposed['prompt'], 'answer': proposed['answers'][0]['text'], 'note': proposed['answers'][0]['note']}),
        'grammar': 'The feminine singular answer label fits “Как называлась политика”; all four answer labels are feminine singular noun phrases.',
        'plausibilityUniqueKeyAndNoteTruthUsefulness': 'A named Soviet plan is a plausible but distinct agricultural-policy distractor. The official PDF dates the first five-year plan to 1928–1932 and says it aimed to transform the country into an industrial one; this note is specific to the distractor and does not make it answer the farm-policy question.',
        'sourcePaths': [path_alt],
        'locator': 'official-alternative PDF page 6 L8-L9, L13-L14.',
    },
    {
        'slot': 1,
        'fullPrompt': proposed['prompt'],
        'answer': proposed['answers'][1]['text'],
        'note': proposed['answers'][1]['note'],
        'tripleSHA256': canonical_sha({'prompt': proposed['prompt'], 'answer': proposed['answers'][1]['text'], 'note': proposed['answers'][1]['note']}),
        'grammar': 'The feminine singular answer label fits the prompt.',
        'plausibilityUniqueKeyAndNoteTruthUsefulness': '“Оттепель” is a recognizable Soviet-era period and is a plausible distractor among named Soviet policies and periods. The retained note asserts the exact post-Stalin association already fenced as exhausted; it is not personally requalified here and prevents READY.',
        'sourcePaths': [],
        'locator': 'HOLD: task priorSourceAttemptMetadata.boundary and predecessor handoff SOURCE76 attempt fence; no reattempt permitted.',
    },
    {
        'slot': 2,
        'fullPrompt': proposed['prompt'],
        'answer': proposed['answers'][2]['text'],
        'note': proposed['answers'][2]['note'],
        'tripleSHA256': canonical_sha({'prompt': proposed['prompt'], 'answer': proposed['answers'][2]['text'], 'note': proposed['answers'][2]['note']}),
        'grammar': 'The feminine singular answer label fits the prompt.',
        'plausibilityUniqueKeyAndNoteTruthUsefulness': 'Glasnost is a plausible named Soviet political policy and is distinct from rural collectivization. The retained source supports its role as a slogan of perestroika; the revised note adds a concrete fact about the option.',
        'sourcePaths': [path52],
        'locator': 'source52 complete returned page L50-L51.',
    },
    {
        'slot': 3,
        'fullPrompt': proposed['prompt'],
        'answer': proposed['answers'][3]['text'],
        'note': proposed['answers'][3]['note'],
        'tripleSHA256': canonical_sha({'prompt': proposed['prompt'], 'answer': proposed['answers'][3]['text'], 'note': proposed['answers'][3]['note']}),
        'grammar': 'The feminine singular answer label completes “Как называлась политика” naturally.',
        'plausibilityUniqueKeyAndNoteTruthUsefulness': 'The official source describes mass collectivization and states that Stalin’s 2 March 1930 article criticized violations of voluntary kolkhoz entry. This uniquely matches the prompt; the note adds a concrete policy context beyond the prompt and key, without duplicating the current GOELRO peer’s note.',
        'sourcePaths': [path48],
        'locator': 'source48 complete returned page L40, L44-L51; key at L40/L44 and additional fact at L50.',
    },
]

entries = [{
    'id': task['id'],
    'topicId': task['topicId'],
    'sourceOrder': task['sourceOrder'],
    'status': 'HOLD',
    'beforeCard': before,
    'beforeHash': canonical_sha(before),
    'proposedCard': proposed,
    'afterHash': canonical_sha(proposed),
    'fieldGroups': field_groups,
}]

candidate = {
    'sourceNativeId': NATIVE_ID,
    'topicId': task['topicId'],
    'cycle': 0,
    'id': task['id'],
    'qualityCredit': 0,
    'entries': entries,
}

sourceproof = {
    'sourceNativeId': NATIVE_ID,
    'topicId': task['topicId'],
    'cycle': 0,
    'id': task['id'],
    'qualityCredit': 0,
    'rawSources': raw_sources,
    'inventory': {
        'path': relative_to_c(INV),
        'sha256': file_sha(INV),
        'purpose': 'Fresh immutable machine inventory for actual current peers and MAIN snapshot; no quality credit.',
    },
    'entries': [{
        'id': task['id'],
        'topicId': task['topicId'],
        'sourceOrder': task['sourceOrder'],
        'status': 'HOLD',
        'literalGroups': literal_groups,
        'fourFullPromptAnswerNoteAssessments': variant_evidence,
        'correctNoteNewFact': {
            'fact': 'In his 2 March 1930 article “Dizziness from Success,” Stalin criticized violations of the voluntary-entry principle for kolkhozes.',
            'primaryLocator': {'sourcePath': path48, 'locator': 'L50'},
            'whyAdditional': 'This quantitative progress snapshot is not stated by the prompt or by the answer label.',
        },
        'absoluteDifficulty': {
            'frozen': 'medium',
            'assessment': 'A history-familiar adult can identify the Soviet agrarian policy, while an adult outside the topic still has to recognize its name; the alternatives are plausible Soviet-era policy/program labels rather than absurd choices. The prompt provides some contextual help, but the key is not simply selected by an implausible option. Keep the frozen MEDIUM level.',
        },
        'defects': [
            {
                'type': 'source_attempt_fence',
                'group': 'note1',
                'detail': 'The unchanged note asserts the exact post-Stalin thaw association already exhausted under SOURCE76. It cannot be re-fetched or repaired through an adjacent claim in this assignment; the card remains HOLD0.',
            }
        ],
        'frozen': task['frozen'],
    }],
    'limitations': [
        'The SOURCE76 thaw association is inherited as exhausted; no new source attempt was made for that claim and no neighboring card is used to bypass it.',
        'The first primary page was only archival catalogue metadata. The single official alternative is used only within its returned PDF page-6 text.',
        'SOURCE82 remains AUTHORHOLD_UNQUALIFIED_UNAPPLIED with quality credit 0; this packet does not adopt or certify SOURCE82.',
        'Candidate HOLD means no independent review, affected QA, coordinator binding, integration, or quality credit is claimed.',
    ],
}

peer_ids = {38, 48, 52, 76, 82, 90, 91, 93, 94, 100}
peer_assessments = {
    38: ('The NEP card asks which economic policy replaced war communism in 1921; this card asks for the rural collectivization policy. Different event, relation, and value.', 'No reverse relation: neither card asks for the other policy or the same event.'),
    48: ('The GOELRO card asks the purpose of electrification; the shared agricultural reference is only a distractor note. Different entity and relation.', 'No reverse relation: neither card asks whether collectivization was the purpose of GOELRO.'),
    52: ('The perestroika-leader card asks which leader is associated with reforms; this card asks the name of the collectivization policy. Their contexts and answer relations differ.', 'No reverse relation: this card does not ask for the leader of perestroika.'),
    76: ('The thaw-leader card asks which leader is associated with the thaw; “Оттепель” is only a distractor here. The thaw-note evidence fence remains separate from this card’s agricultural relation.', 'No reverse relation: this card does not identify the leader associated with the thaw.'),
    82: ('The industrialization-plan card asks for the first state industrialization plan; this card asks for the agricultural collectivization policy. They share Soviet-era context and some answer labels, but entity, relation, and value differ.', 'No reverse relation: neither answer is the value requested by the other card.'),
    90: ('The Port Arthur card asks which war the siege occurred in; this card concerns collectivization. Different event, relation, and period.', 'No reverse relation.'),
    91: ('The Kronstadt card asks which event occurred in March 1921; this card concerns late-1920s/1930 collectivization. Different event and requested value.', 'No reverse relation.'),
    93: ('The 1977 Constitution card asks who led the USSR at adoption; this card asks for an agricultural policy name. Different entity, relation, and context.', 'No reverse relation.'),
    94: ('The glasnost card asks for the policy of open public discussion; “Гласность” is only a distractor here. Collectivization is a distinct agrarian relation.', 'No reverse relation: this card does not ask for glasnost.'),
    100: ('The Kosygin-reform card asks which 1965 economic reform expanded enterprise autonomy; this card asks for the mass collective-farm policy. Different policy, relation, and period.', 'No reverse relation.'),
}
actual = {p['sourceOrder']: p for p in inventory['actualCurrentPeers']}
relevant_pairs = []
for order in sorted(peer_ids):
    peer = actual[order]
    forward, reverse = peer_assessments[order]
    relevant_pairs.append({
        'id': peer['id'],
        'topicId': peer['topicId'],
        'sourceOrder': order,
        'actualPeerCard': peer['card'],
        'actualPeerCanonicalSHA256': peer['sha256'],
        'proposedCard': proposed,
        'proposedCardCanonicalSHA256': canonical_sha(proposed),
        'bilateralMAIN': {
            'proposedToActual': forward,
            'actualToProposed': reverse,
            'entityRelationValueContextDirectReverse': 'No semantic duplicate or direct reverse.',
        },
    })

peer_snapshot = {
    'sourceNativeId': NATIVE_ID,
    'topicId': task['topicId'],
    'cycle': 0,
    'id': task['id'],
    'sourceOrder': task['sourceOrder'],
    'qualityCredit': 0,
    'globalMAIN': inventory['globalMAIN'],
    'sameTopicMAIN': inventory['sameTopicMAIN'],
    'actualCurrentPeers': inventory['actualCurrentPeers'],
    'relevantProposedPairs': relevant_pairs,
    'crossTopicScreen': {
        'searchedCurrentRowsFor': ['collectivization/kolkhoz', 'first five-year plan', 'thaw', 'glasnost', 'collective peasant farms'],
        'falsePositiveRows': [
            {
                'topicId': 'history-china',
                'id': 'history-china-hard-01-05',
                'row': next(r for r in inventory['globalMAIN']['rows'] if r['id'] == 'history-china-hard-01-05'),
                'assessment': 'Shared distractor text “Первая пятилетка”; its prompt concerns China’s Third Front and a 1960s-1970s industrial relocation program, not Soviet collectivization. No ERVC duplicate or reverse.',
            },
            {
                'topicId': 'tv-series',
                'id': 'tv-series-thaw-director',
                'row': next(r for r in inventory['globalMAIN']['rows'] if r['id'] == 'tv-series-thaw-director'),
                'assessment': 'The title “Оттепель” refers to a Russian television series; its prompt asks for a director. It is not the Soviet-era thaw claim and not a duplicate.',
            },
        ],
        'result': 'No relevant cross-topic semantic duplicate or direct reverse found in the fresh 11,000-row MAIN snapshot.',
    },
}

outputs = {
    'candidate.json': candidate,
    'sourceproof.json': sourceproof,
    'peer-snapshot.json': peer_snapshot,
}
for name, value in outputs.items():
    path = OUT / name
    assert not path.exists(), f'Preserve original packet file: {path}'
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

print(json.dumps({
    'outputs': {name: {'path': str(OUT / name), 'sha256': file_sha(OUT / name)} for name in outputs},
    'beforeHash': canonical_sha(before),
    'afterHash': canonical_sha(proposed),
    'status': 'HOLD',
    'qualityCredit': 0,
    'rawSourceCount': len(raw_sources),
    'actualCurrentPeerCount': len(inventory['actualCurrentPeers']),
    'relevantBilateralPairs': len(relevant_pairs),
}, ensure_ascii=False))
