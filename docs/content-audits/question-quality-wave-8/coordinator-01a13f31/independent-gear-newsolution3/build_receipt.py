"""Mechanical binding of this reader's INITIAL judgments; never changes catalog or Git."""
import datetime
import hashlib
import itertools
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).resolve().parent
BASE = ROOT / 'docs/content-audits/question-quality-wave-8'
AUTHOR = BASE / 'process-v2-gear-newsolution-cornerfix-01a13f31/author/qualified/final'
APPLY = BASE / 'coordinator-01a13f31/apply-gear-newsolution3.json'
QA = BASE / 'coordinator-01a13f31/qa-gear-newsolution3.json'

def read(p):
    return json.loads(p.read_text())

def canonical(x):
    return json.dumps(x, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')

def sha(x):
    return hashlib.sha256(canonical(x)).hexdigest()

def rawsha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()

def save(name, data):
    (OUT / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')

apply = read(APPLY)
catalog_path = 'src/content/topics/engineering-machines.json'
topic = read(ROOT / catalog_path)
cards = {q['id']: q for q in topic['questions']}
sourceproof = read(AUTHOR / 'sourceproof.json')
author_peers = read(AUTHOR / 'peer-snapshot.json')
source_dir = BASE / 'process-v2-engineering11-20-01a13e5e/author/sources'
sources = {s['key']: s for s in sourceproof['rawSources']}

def loc(key, locator):
    s = sources[key]
    return {'path': s['path'], 'url': s['url'], 'locator': locator}

spur = loc('spur', 'KHK retained page L37-L41; especially L37 and L39')
helical = loc('dims', 'KHK section 4.3, L250-L268; normal-system definition L257-L258, hob L264, mating L268')
axial = loc('helicalPdf', 'KHK P1 L217 and P2 L344-L346')
zerol = loc('dims', 'KHK L422 and Gleason Zerol section L568-L572')
worm = loc('worm', 'Retained complete bounded section ② Self-locking of worm gears, physical line 6')
worm_main = loc('dims', 'KHK L683-L690 and L845-L847')

# These are independent judgments written after reading CURRENT, not author verdicts.
judgments = {
 11: {
  'level': 'Hard is defensible for the axial-force distinction: the player must connect tooth direction with a force component. No calculation is required. The bevel/worm choices can be eliminated by the shaft geometry, leaving a substantive spur/helical distinction.',
  'extra': 'PASS: typical 20° pressure angle and common industrial involute form are independent of absence of axial force; KHK spur L39 supports both. They are not merely prompt/key restatement.',
  'groups': [
   'Unique key is spur under the stated ideal parallel-axis cylindrical context: KHK spur L37 says tooth faces are parallel to the axis and no axial thrust. Helical generates thrust (PDF P2 L344-L346). However answer3 is a whole transmission while the prompt requests a wheel type; see variants.',
   'The tooth-direction reason is supported by KHK spur L37. Qualification about other elements avoids claiming the entire assembly can never carry axial load.',
   'KHK spur L39 independently supports typical 20° pressure angle and industrial involute prevalence; useful own-option fact beyond main.',
   'KHK dimensions L250-L265 defines normal/transverse systems and modules. Compatible tooth profiles are necessary; this note describes the helical option itself.',
   'FIX: KHK L569 supports zero spiral angle and applicability of straight-bevel calculation equations, but does not support the added assertion that Zerol teeth are straight. L422 lists straight and Zerol separately; L569 also retains left/right handedness. Applicability of equations is not proof of straight tooth geometry.',
   'Source gap: retained dimensions L683-L690 describes worm construction and axes; section ② relates material to self-locking. Neither passage establishes the specific KHK attribution that material pairing is important for reducing friction/wear. Do not infer this from the screw-gear wear discussion L675-L678, which concerns another mesh.'
  ],
  'variants': [
   ('PASS: independent nominative label agrees with the requested wheel type.', 'Strong candidate: spur and helical are both cylindrical parallel-axis gears.', 'KEY, and unique among supplied choices in this context; spur L37.', 'PASS: pressure angle and involute are true useful own-option extra facts (L39).', [spur, axial]),
   ('PASS: nominative wheel label.', 'Strong distractor: same shaft arrangement; knowledge of axial thrust distinguishes it.', 'WRONG: helical thrust follows the helix; PDF P2 L344-L346.', 'PASS: normal/transverse module distinction belongs to this helical option, not to the spur key.', [helical, axial]),
   ('PASS: nominative wheel label.', 'Related gear family; informed readers can eliminate it because bevel axes intersect. This is context-based narrowing, not another valid answer.', 'WRONG: bevel pitch surfaces and intersecting axes differ from the cylindrical parallel-axis condition (L422).', 'FIX: zero spiral angle is supported; straight teeth is an unsupported and misleading inference from the equations. Needs correction or precise primary proof.', [zerol]),
   ('FIX category: «Червячная передача» names a transmission, whereas the question asks «тип зубчатого колеса» and the other three labels name wheels. Sentence is syntactically readable but the answer categories are inconsistent.', 'Worm gearing is related, but its ordinary skew-axis geometry does not fit the stated pair. Weaker than the helical distractor.', 'WRONG: ordinary worm mesh has nonparallel nonintersecting axes; L689.', 'HOLD factual attribution pending exact source: plausible mechanical fact is not established by the retained passages. Do not credit KHK material-pairing/wear claim from self-locking material factors alone.', [worm_main, worm])
  ],
  'defects': [
   {'code': 'ZEROL_STRAIGHT_TEETH_NOT_PROVEN', 'field': 'answers[2].note', 'ground': 'The new clause «у него прямые зубья» does not follow from KHK L569. The saved source establishes zero spiral angle, not straight tooth geometry.', 'requiredAction': 'Remove the unsupported clause or replace it with a precisely supported own-option fact; do not equate zero mean spiral angle with straight tooth shape.'},
   {'code': 'ANSWER_CATEGORY', 'field': 'prompt + answers[3].text', 'ground': 'A transmission is offered as a type of wheel; the other choices are wheels.', 'requiredAction': 'Make question/answers one consistent category while preserving frozen identity, order, difficulty and key.'},
   {'code': 'WORM_NOTE_SOURCE_GAP', 'field': 'answers[3].note', 'ground': 'The retained rawSources do not establish the attributed KHK material-pairing/friction/wear assertion. L675-L678 concerns screw gears, not evidence for this worm claim.', 'requiredAction': 'Provide exact retained primary context for both clauses, or use a supported own-option fact. This is an evidence gap, not a declaration that the engineering claim is false.'}
  ]
 },
 12: {
  'level': 'Hard is defensible: external versus internal meshing, parallel versus crossed axes, helix-angle equality and opposite hands are specific conditions. Options differ by meaningful technical conditions; this is not an arbitrary-name lottery or mandatory-math issue.',
  'extra': 'PASS in substance: reuse of the same hob for different helix angles in a normal system is a manufacturing fact beyond pair mating. L257-L258 defines the normal system; L264 gives constant module/pressure-angle conditions. The note should name the hob precisely as «червячная фреза» and say «нормальный угол давления» to make the translated conditions explicit; no source falsehood verdict is inferred from KHK rendered αt/at typography.',
  'groups': [
   'KHK L268 directly supports equal helix angles and opposite hands for the parallel external pair. The four statements give one key; zero-helix is outside the specified helical case.',
   'First sentence correctly states L268. Second sentence is editorial process commentary about a neighboring card rather than an engineering explanation; remove it in the targeted wording pass. It does not establish a duplicate.',
   'Manufacturing extra fact is supported by normal-system definition L257-L258 and hob reuse L264-L266. «Червячный инструмент» is vague for gear hob; precise Russian is «червячная фреза». State the normal pressure angle explicitly.',
   'FIX Russian: «при одинаковых руках» is a literal translation of hands, not a clear Russian description of helix direction. The actual geometric rule (same direction fails external parallel pairing) is correct and specific, not an empty negative placeholder.',
   'The note names the exact confused condition, angle equality, and explains this false compound statement. KHK L268 supports the distinction; permitted correction of a false rule.',
   'Zero angle yields straight tooth traces; KHK spur L37 and dimensions L250 describe the distinction. The note is about this limiting-case option, not misattributed to the key.'
  ],
  'variants': [
   ('PASS: parallel noun phrase answers «какое сочетание».', 'Plausible and technically precise; the need to track both magnitude and hand is meaningful.', 'KEY: same helix angle/opposite hands, KHK L268; only supplied combination satisfying the context.', 'PASS factual extra: hob reuse under constant normal-system parameters. FIX precision of Russian tool name/explicit normal pressure angle, not a fabricated manufacturing rule.', [helical]),
   ('PASS answer grammar; FIX note terminology «одинаковых руках».', 'Plausible reversal of the hand condition; a real gear-meshing confusion.', 'WRONG: equal angles with same hands does not meet external parallel-axis mating rule L268.', 'Specific mistaken rule is identified, but «руки» is unclear technical Russian. Use same directions of the tooth helix. This is not rejected merely because it explains why the option is wrong.', [helical]),
   ('PASS: parallel phrase has same syntactic structure as key.', 'Plausible mix-up with crossed-axis screw gearing; differs on one actual mating condition.', 'WRONG: differing angles violate equal-angle requirement L268 in the stated parallel pair.', 'PASS: note names the exact inconsistent angle rule; useful for this false assertion.', [helical]),
   ('PASS: nominative condition phrase is readable with the question.', 'Related limiting case; can be excluded by the word helical without identifying whether equal- or opposite-hand case is right.', 'WRONG: the nonzero helix stipulated by helical gearing is lost at zero angle.', 'PASS: distinction belongs to this straight-tooth option; KHK spur L37 and helical definition L250.', [spur, helical])
  ],
  'defects': [
   {'code': 'RUSSIAN_HANDS_CALQUE', 'field': 'answers[1].note', 'ground': '«При одинаковых руках» is a calque of same hands and does not clearly state the Russian technical condition.', 'requiredAction': 'Say «при одинаковом направлении винтовых линий» or equivalent exact Russian, retaining external parallel-axis context.'},
   {'code': 'EDITORIAL_METATEXT', 'field': 'explanation sentence 2', 'ground': 'The neighboring-card reference describes catalog editing instead of helping the player understand mating.', 'requiredAction': 'Replace with relevant technical explanation while preserving the two-sentence contract.'}
  ],
  'nonBlockingPrecision': 'In note0 replace broad «червячный инструмент» with «червячная фреза» and qualify pressure angle as normal; the normal-system context already supports the underlying fact, so this is not independently a factual HOLD.'
 },
 14: {
  'level': 'FAIL frozen hard: prompt itself specifies that a «червяк» cannot be rotated by the wheel. Of four transmission-family labels only «Червячная» names that component. A player can select it by noun recognition without knowing the mechanics of self-locking, material, friction or lead angle. No objection is based on lack of mathematics. Current difficulty is effectively easy by this cue, even though the uncued mechanical fact could merit a higher level.',
  'extra': 'PASS: usual single-start lead angle ≤4° is an additional numerical/design fact absent from prompt and key. Section ② explicitly qualifies it as usual rather than universal and lists other factors. The note preserves that limitation.',
  'groups': [
   'Worm is factually the sole key among the four families for the specified non-backdriving phenomenon (KHK L846 and section ②). However naming «червяк» in the definition gives away the transmission family and fails hard.',
   'Accurate no-backdrive direction: wheel cannot drive worm. Material, lead, accuracy, bearings, lubrication and supplementary brake are in section ②. Does not claim all worm pairs self-lock.',
   'KHK L569 supports the Zerol designation for zero spiral angle. This note makes no unsupported straight-teeth assertion.',
   'Section ② supports usual single-start ≤4° and the non-guarantee qualification. Useful own-option extra fact beyond main.',
   'KHK spur L40 supports backlash needed for smooth meshing. The additional attributed dependence on center distance lacks an exact retained textual locator; L41 supports involute tolerance of some center-distance error, a different assertion. Need precise primary locator or narrow to supported fact.',
   'KHK L268 supports same angle/opposite hands for the ordinary external parallel-axis pair. Note should retain that context: unrestricted helical gearing also includes other shaft/internal configurations. This is a scope qualification, not MAIN duplication with #12.'
  ],
  'variants': [
   ('PASS: nominative transmission label fits «какой тип передачи».', 'Mechanically related family, but the explicit worm component in the prompt makes this easy to eliminate.', 'WRONG for the stated worm/wheel no-backdrive phenomenon; KHK section ② attributes it to worm gearing.', 'PASS: Zerol zero spiral angle is an own-family fact and does not inherit the erroneous straight-teeth addition in #11.', [zerol, worm]),
   ('PASS: nominative label agrees.', 'Unfairly privileged by exact component/word-root cue in the question.', 'KEY true and unique in this list, but selecting it needs only «червяк» → «червячная», failing the intended hard knowledge test.', 'PASS: source says usual single-start ≤4°; note does not promise all such pairs are safe without brake.', [worm, worm_main]),
   ('PASS: same transmission category.', 'Related family but not a credible competing choice once the question names the worm.', 'WRONG for this phenomenon; ordinary spur mesh is not the worm pair defined in the prompt.', 'PARTIAL: smooth-meshing necessity is supported by spur L40; center-distance dependence needs an exact own-fact passage rather than a nearby involute-tolerance statement.', [spur]),
   ('PASS: same transmission category.', 'Related family; again eliminated by the explicit component cue rather than by knowledge of self-locking.', 'WRONG for the specified worm/wheel phenomenon; no second key in these choices.', 'FIX scope: L268 is used in external parallel-axis helical context. Make that context explicit to avoid applying opposite hands to all helical configurations.', [helical])
  ],
  'defects': [
   {'code': 'PROMPT_REVEALS_KEY_HARD_FAIL', 'field': 'prompt + difficulty', 'ground': '«червяк» in the prompt identifies «Червячная передача» directly. Domain knowledge of self-locking is unnecessary.', 'requiredAction': 'Keep frozen hard/key/ID/order but formulate an uncued substantive engineering task. Merely deleting one noun may remove the cue yet still require a fresh absolute-level assessment.'},
   {'code': 'BACKLASH_SOURCE_LOCATOR_GAP', 'field': 'answers[2].note', 'ground': 'Retained spur L40 supports smooth meshing; the exact KHK center-distance/backlash dependence is not located in rawSources.', 'requiredAction': 'Supply exact retained primary passage or replace only the unsupported clause with a supported own-option fact.'},
   {'code': 'HELICAL_NOTE_SCOPE', 'field': 'answers[3].note', 'ground': 'Opposite-hand/equal-angle condition is stated without external parallel-axis restriction; the source L268 is used under that restriction.', 'requiredAction': 'Include «во внешней паре на параллельных валах» in the note or use another supported own-option fact.'}
  ]
 }
}

entries = []
for a in apply['applied']:
    n = a['sourceOrder']
    assert n in judgments
    q = cards[a['id']]
    assert sha(q) == a['proposedSHA256'] == sha(a['proposedCard'])
    j = judgments[n]
    literals = [('prompt_ordered_answers_key', {'prompt': q['prompt'], 'answers': [x['text'] for x in q['answers']], 'correctIndex': q['correctIndex']}), ('explanation', q['explanation'])]
    literals += [('note' + str(i), x['note']) for i, x in enumerate(q['answers'])]
    variants = []
    for i, (ans, v) in enumerate(zip(q['answers'], j['variants'])):
        triple = {'prompt': q['prompt'], 'answer': ans['text'], 'note': ans['note']}
        variants.append({'slot': i, **triple, 'tripleCanonicalSHA256': sha(triple), **dict(zip(['grammar', 'plausibility', 'truthUniqueKey', 'noteTruthUsefulness', 'sourcesLocators'], v))})
    entries.append({'id': q['id'], 'sourceOrder': n, 'stage': 'INITIAL_CONCRETE_NEW_SOLUTION3', 'currentCard': q, 'currentCardCanonicalSHA256': sha(q), 'matchesAppliedSHA256': True, 'status': 'FIX',
      'sixLiteralCanonicalGroups': [{'group': name, 'literal': lit, 'canonicalSHA256': sha(lit), 'individualGround': ground} for (name, lit), ground in zip(literals, j['groups'])],
      'fourFullPromptAnswerNoteVariants': variants, 'absoluteLevel': j['level'], 'correctNoteExtraFact': j['extra'], 'defects': j['defects'],
      'nonBlockingPrecision': j.get('nonBlockingPrecision'),
      'frozen': {'id': q['id'] == a['beforeCard']['id'], 'difficulty': q['difficulty'] == a['beforeCard']['difficulty'], 'correctIndex': q['correctIndex'] == a['beforeCard']['correctIndex'], 'sourceOrder': topic['questions'][n-1]['id'] == q['id'], 'topicId': topic['id'] == apply['topicId']}})

source_evidence = []
read_scopes = {
 'spur': ('L37-L41', 'Read complete retained spur explanatory context: parallel tooth faces/no thrust; typical 20° and involute; profile shift/backlash consequences. Korean text interpreted in context, not from author English ground.'),
 'dims': ('L245-L269; L422; L568-L577; L675-L690; L845-L849; retained spur dimension context L35-L60', 'Read normal/transverse definitions and hob/mating conditions, bevel/Zerol passage, screw-gear context boundary, worm geometry and self-locking. Normal manufacturing and mating are different relations. Zero spiral angle does not establish straight teeth. Retained file is stitched rendered passages, not every original-page equation/image.'),
 'helicalPdf': ('P1 L210-L223 and P2 L339-L350', 'Read entire retained product-caution/thrust context. Thrust and its direction are separate from mating condition. Product line number-of-teeth condition not generalized to all gears.'),
 'twi': ('L511-L544 Common Joint Configurations', 'Read complete retained joint definitions including inclusive/open boundaries; confirms peer joint family does not duplicate gear MAIN. No reopening of certified joint cards.'),
 'worm': ('physical lines 1-6, complete bounded section ②', 'Read entire retained section: wheel cannot rotate worm, factors, usual single-start ≤4°, supplementary brake. Supplies correctnote extra fact, not a proof of material pairing for wear.')
}
for key, s in sources.items():
    p = ROOT / s['path']
    locator, evidence = read_scopes[key]
    source_evidence.append({'key': key, 'path': s['path'], 'rawReadSHA256': rawsha(p), 'matchesManifestSHA256': rawsha(p) == s['sha256'], 'url': s['url'], 'locator': locator, 'readEvidence': evidence, 'limitations': 'Previously saved rendered text personally read in the relevant complete section; no re-download; no claim of reading absent diagrams or original full binary.'})
nsk_manifest = read(source_dir / 'manifest.json')
for filename, locator, evidence in [
 ('nsk-bearing-basics.txt', 'L350-L407', 'Read bearing types, sliding/rolling distinction, oil film, main load directions; these peer facts do not ask gear mating or gear-force generation.'),
 ('nsk-roller-bearings.txt', 'L415-L495', 'Read roller/ball contact/load/speed and roller-family contexts for peer separation, not to reissue certification.'),
 ('nsk-types-of-rolling-bearings.txt', 'L415-L453', 'Read element and load direction taxonomy; thrust bearing selection is not a reverse of gear axial-force generation.'),
 ('nsk-thrust-bearings.txt', 'L348-L363', 'Read complete thrust-bearing descriptive section; axial load direction differs from the tooth geometry relation.'),
 ('nsk-ball-bearings.txt', 'L415-L425', 'Read retained deep-groove features: point contact, speed, loads and sealing context.')]:
    p = source_dir / filename
    text = p.read_text()
    urls = re.findall(r'https://[^\s)]+', text)
    source_evidence.append({'path': str(p.relative_to(ROOT)), 'rawReadSHA256': rawsha(p), 'url': next((u for u in urls if 'nsk.com/' in u), None), 'locator': locator, 'readEvidence': evidence, 'limitations': 'Peer-context reading only; no protected peer recertification.'})

def main(q):
    return {'entity': q['answers'][q['correctIndex']]['text'], 'prompt': q['prompt'], 'correctIndex': q['correctIndex']}

relations = {11: ['spur gear', 'generates axial force', 'none in ideal tooth mesh', 'parallel-axis cylindrical pair'], 12: ['external helical pair', 'mates under helix geometry', 'equal angle magnitude/opposite hands', 'parallel shafts'], 13: ['bevel pair', 'pitch geometry/shaft arrangement', 'common cone apex/intersecting shafts', 'bevel family'], 14: ['worm pair', 'backdriving', 'wheel cannot rotate worm under suitable conditions', 'conditional self-locking'], 15: ['ball bearing', 'contact/speed choice', 'high-speed point contact', 'comparable rolling-bearing conditions'], 16: ['roller bearing', 'load/speed choice', 'high radial capacity', 'compact node speed secondary'], 17: ['plain bearing', 'support mechanism', 'sliding surface/no rolling bodies', 'sleeve or liner'], 18: ['thrust bearing', 'primary load direction', 'axial', 'rolling bearing taxonomy'], 19: ['lap joint', 'parts arrangement', 'overlap', 'sheet joint'], 20: ['butt joint', 'parts arrangement', 'ends in same plane', 'joint'], 28: ['gear drive', 'power transmission principle', 'meshing toothed wheels', 'generic drive'], 36: ['tee joint', 'parts arrangement', 'end to face near right angle', 'joint']}
peer_numbers = sorted(relations)
actual_peers = [{'sourceOrder': n, 'currentCard': topic['questions'][n-1], 'canonicalSHA256': sha(topic['questions'][n-1]), 'MAIN': relations[n]} for n in peer_numbers]
bilateral = []
for a, b in itertools.combinations(peer_numbers, 2):
    if not ({a,b} & {11,12,14}):
        continue
    reason = 'Different entity-relation-value-context; a shared gear/load vocabulary or a note repeating another key is not MAIN duplication.'
    if (a,b) == (11,12):
        reason = 'Force generated by tooth orientation versus mating condition of two helix geometries. Neither asks the forward/reverse mapping of the other. Knowledge that a pair has opposite hands does not establish absence of axial force, and no-thrust spur identification does not specify mating hands.'
    elif (a,b) in [(11,18),(12,18),(14,18)]:
        reason = 'Gear geometry/meshing/backdriving versus bearing primary-load classification. The common axial vocabulary is not the same entity-relation mapping.'
    elif b == 28:
        reason = 'Specific force/mating/self-locking relation versus generic definition of toothed-wheel transmission; no direct/reverse equivalence.'
    bilateral.append({'a': a, 'b': b, 'aMAIN': relations[a], 'bMAIN': relations[b], 'semanticDuplicate': False, 'directReverse': False, 'ground': reason})

cross = []
topic_hashes = []
for p in sorted((ROOT / 'src/content/topics').glob('*.json')):
    d = read(p)
    topic_hashes.append({'path': str(p.relative_to(ROOT)), 'rawSHA256': rawsha(p)})
    for index,q in enumerate(d.get('questions',[]),1):
        key = q['answers'][q['correctIndex']]
        key = key['text'] if isinstance(key,dict) else key
        if re.search(r'шестер|червяч|косозуб|прямозуб|самоторм|зубчат|осев|винтов|храпов', q['prompt']+' '+key, re.I):
            cross.append({'topicId': d['id'], 'sourceOrder': index, 'currentCard': q, 'canonicalSHA256': sha(q), 'MAINkey': key, 'duplicateWithReviewedMAIN': False, 'ground': 'Read MAIN in actual current catalog; different relation/context. Agriculture, language word roots and geographic ridges are lexical false positives; rail gear/strengthening/icon and generic drive facts are distinct.'})

proposed = [{'sourceOrder': x['sourceOrder'], 'card': x['card'], 'canonicalSHA256': sha(x['card']), 'statusInherited': False, 'includedForCertification': x['sourceOrder'] in [11,12,14]} for x in author_peers['finalProposedCards']]
peer_report = {'actualCurrentPeers': actual_peers, 'bilateralMAINcomparison': bilateral, 'proposedPeersRead': proposed, 'authorSnapshotRawSHA256': rawsha(AUTHOR/'peer-snapshot.json'), 'actualVsAuthorSnapshot': [{'id': x['id'], 'sourceOrder': x['sourceOrder'], 'authorSnapshotCanonicalSHA256': sha(x['card']), 'actualCanonicalSHA256': sha(cards[x['id']]), 'equal': sha(x['card']) == sha(cards[x['id']])} for x in author_peers['actualCurrentPeers']], 'crossCatalogCandidatesRead': cross, 'catalogTopicSnapshots': topic_hashes, 'limitations': 'Lexical selection plus actual full topic MAIN review guides semantic comparison, not an automated semantic proof. Proposed #37 read only as peer; sourceHOLD excluded. No inherited PASS or reopening of protected cards.'}
save('peers.json', peer_report)

qa = read(QA)
head = git('rev-parse','HEAD')
receipt = {'scope': [11,12,14], 'reviewer': '01a13f48-a5b8-7d92-9904-65117a9c5e3b', 'appliedCommit': 'da2ad775aa16dff8ec5576958780d3cb4bbe4dbd', 'qaBaselineCommit': apply['baselineCommit'], 'branch': git('branch','--show-current'), 'freshBranchRefObserved': head, 'createdAt': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'pinnedProcess': '12e5581b:.agents/references/question-revision.md',
 'rules': ['Personally read all three exact CURRENT cards and all 12 full prompt-answer-note triples.', 'INITIAL of concrete new solutions, not another unchanged cycle; former terminal findings retained and not inherited.', 'Frozen IDs/topic/order/difficulty/key; no catalog/index/ref/planning/claim mutations.', 'Hard may require specific knowledge OR substantive reasoning; no mandatory mathematics.', 'Correctnote extra facts may overlap explanation; wrongnote may contain another canonical key fact.', 'Only a concrete addressed fix can use the single substantive fix-cycle; unresolved final findings become HOLD.'], 'hashMethod': 'SHA256 UTF-8 json.dumps(sort_keys=True,separators=(comma,colon),ensure_ascii=False); raw hashes over exact file bytes.', 'entries': entries, 'counts': {'PASS':0,'FIX':3,'HOLD':0}, 'qualityCredit':0,
 'evidence': {'sources': source_evidence, 'peers':'peers.json', 'mainComparisons':'peers.json#bilateralMAINcomparison', 'apply': {'path': str(APPLY.relative_to(ROOT)), 'rawSHA256': rawsha(APPLY)}, 'authorCandidate': {'path': str((AUTHOR/'candidate.json').relative_to(ROOT)), 'rawSHA256': rawsha(AUTHOR/'candidate.json')}, 'sourceproof': {'path': str((AUTHOR/'sourceproof.json').relative_to(ROOT)), 'rawSHA256': rawsha(AUTHOR/'sourceproof.json'), 'warning': 'Author group sourcePaths/grounds are not treated as verdicts; several are mismatched to their literals. Independent locators and gaps recorded above.'}},
 'qaObservedNotReexecuted': {'path': str(QA.relative_to(ROOT)), 'rawSHA256': rawsha(QA), 'success':qa['success'], 'passed':qa['numPassedTests'], 'total':qa['numTotalTests'], 'meaning':'Existing focused QA19 is schema/runtime-contract evidence only, not editorial PASS.'}, 'execution': {'runtimeTests':'NotRun: documentation-only independent content review; existing exact QA read.', 'build':'NotRun', 'deploy':'NotRun', 'ownProcessesStarted':False, 'subagentsStarted':False, 'gitMutated':False, 'ownTemporaryFiles':[], 'sourceDownload':False},
 'nextAction': 'Coordinator adjudicates concrete INITIAL findings and, if accepted, commissions only one targeted fix-cycle. Re-review changed cards and touched dependencies only; unresolved FINAL => HOLD. Coordinator preserves receipt in Git; no credit before root binding.', 'preservation': 'Files left in authorized persistent audit directory for coordinator commit. This reviewer was explicitly forbidden to commit; no claim that review is already in Git or main.'}
save('receipt.json', receipt)
verification = {'currentMatchesExactApply': all(x['matchesAppliedSHA256'] for x in entries), 'entries':len(entries), 'groups':sum(len(x['sixLiteralCanonicalGroups']) for x in entries), 'variants':sum(len(x['fourFullPromptAnswerNoteVariants']) for x in entries), 'allFrozen':all(all(x['frozen'].values()) for x in entries), 'sourceManifestHashes':all(s.get('matchesManifestSHA256',True) for s in source_evidence), 'receiptRawSHA256':rawsha(OUT/'receipt.json'), 'peersRawSHA256':rawsha(OUT/'peers.json'), 'catalogRawSHA256':rawsha(ROOT/catalog_path), 'snapshotRef':head, 'allowedOutputDirectory':str(OUT), 'qualityCredit':0}
assert verification['currentMatchesExactApply'] and verification['allFrozen'] and verification['sourceManifestHashes']
assert (verification['entries'],verification['groups'],verification['variants']) == (3,18,12)
save('verification.json',verification)
print(json.dumps(verification,ensure_ascii=False,indent=2))
