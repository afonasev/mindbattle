"""Bind handwritten decisions and explicitly selected source lines; creates no verdicts."""
import hashlib
import json
import os
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
AUTHOR = REPO / 'docs/content-audits/question-quality-wave-6/middle-ages/resume-2026-10-11-fix5'
IDENTITY = '01a12b98-1551-7a63-9e63-d1555b6ae364'
assert os.environ['CODEX_THREAD_ID'] == IDENTITY

def sha(data):
    return hashlib.sha256(data).hexdigest()

def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()

def write(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

decisions = json.loads((HERE / 'manual-decisions.json').read_text())
author_receipt = json.loads((AUTHOR / 'author-current.json').read_text())
assert {r['questionId'] for r in decisions} == {r['questionId'] for r in author_receipt['cards']}
topic_path = REPO / 'src/content/topics/middle-ages.json'
topic = json.loads(topic_path.read_text())
catalog = {c['id']: c for c in topic['questions']}
baseline = json.loads(subprocess.check_output(['git', 'show', '0f97808:src/content/topics/middle-ages.json'], cwd=REPO))
old = {c['id']: c for c in baseline['questions']}
for row in decisions:
    qid = row['questionId']
    assert catalog[qid] == old[qid], f'Concurrent drift: {qid}'

manifest = json.loads((AUTHOR / 'sources/capture-manifest.json').read_text())
metadata = {Path(m['file']).name: m for m in manifest}
sources = {
    'cleeve': 'cleeve-source.txt', 'lill': 'lilleshall-source.txt',
    'tyne': 'tynemouth-source.txt', 'castle': 'castle-acre-source.txt',
    'finch': 'web-open-finchale.txt', 'lind': 'web-open-lindisfarne.txt',
    'richard': 'web-open-richard-i.txt', 'john': 'web-open-john.txt',
    'edward': 'web-open-edward-confessor.txt', 'met': 'web-open-frederick.txt'
}
source_text = {}
source_meta = {}
inventory = []
for key, filename in sources.items():
    raw = AUTHOR / 'sources' / filename
    data = raw.read_bytes()
    meta = metadata[filename]
    assert sha(data) == meta['rawCaptureSha256']
    text = data.decode()
    lines = [int(n) for n in re.findall(r'\bL(\d+):', text)]
    missing = sorted(set(range(max(lines) + 1)) - set(lines))
    assert not missing, (filename, missing)
    source_text[key] = text
    source_meta[key] = dict(sourceClass=meta['sourceClass'], title=meta['title'], url=meta['url'],
        rawCapture=os.path.relpath(raw, HERE), rawCaptureSha256=sha(data),
        captureFormat=meta['captureFormat'],
        captureMethod=f"Previously committed complete original web.open extraction, all source lines 0..{max(lines)} present. Independently opened and read relevant original passages in this thread; no inherited verdict. Original capture metadata: {meta['captureMethod']}")
    inventory.append(dict(key=key, path=os.path.relpath(raw, HERE), sha256=sha(data),
        sourceLines=[0, max(lines)], missingLines=missing, sourceRole='institution original',
        readRole='independent', readerIdentity=IDENTITY))

extra = HERE / 'sources/additional-original-web-response.txt'
parts = extra.read_text().split('\n--------------------------------------------------------------------------------\n')
assert len(parts) == 2
for key, part, url, title, last in [
    ('royal', parts[0], 'https://www.royal.uk/richard-i', 'Richard I | The Royal Household', 221),
    ('nla', parts[1], 'https://nla.niedersachsen.de/startseite/landesgeschichte/aus_den_magazinen_des_landesarchivs/2022/aus-den-magazinen-des-landesarchivs-juni-2022-206223.html', 'Aus den Magazinen des Landesarchivs (Juni 2022) | NLA', 191)
]:
    lines = {int(n) for n in re.findall(r'\bL(\d+):', part)}
    assert lines == set(range(last + 1))
    source_text[key] = part
    source_meta[key] = dict(sourceClass='institution original', title=title, url=url,
        rawCapture=str(extra.relative_to(HERE)), rawCaptureSha256=sha(extra.read_bytes()),
        captureFormat='text original full fetched response or fully documented original extracted content',
        captureMethod=f'Actual complete web.run open response saved unchanged by functions store/apply_patch on 2026-10-11. Response contains two complete source extractions; this one has all lines L0..L{last}. No selected-quote assembly.')
    inventory.append(dict(key=key, path=str(extra.relative_to(HERE)), sha256=sha(extra.read_bytes()),
        sourceLines=[0, last], missingLines=[], sourceRole='institution original',
        readRole='independent', readerIdentity=IDENTITY))

proof_index = {}
for row in decisions:
    for _, _, _, refs in row['fields']:
        for ref in refs:
            if ref in proof_index:
                continue
            key, line = re.fullmatch(r'([a-z]+)(\d+)', ref).groups()
            match = re.search(r'\bL' + line + r':\s?(.*?)(?=\bL\d+:|\Z)', source_text[key], re.S)
            assert match, ref
            passage = match[1].strip()
            assert passage
            proof_index[ref] = dict(source_meta[key],
                locator={'sourceKey': key, 'sourceLine': int(line), 'extraction': 'original web.open rendered line, unaltered scalar'},
                passage=passage, passageSha256=sha(passage.encode()))

receipt = dict(role='independent', agentIdentity=IDENTITY, reviewedAt='2026-10-11',
    authorIdentity=author_receipt['agentIdentity'], authorCommit='0f97808',
    scope='Only five explicitly assigned current cards, all 30 fields. Handwritten independent judgments; zero coordinator certifications.',
    cards=[])
assert receipt['agentIdentity'] != receipt['authorIdentity']
snapshot = []
for row in decisions:
    card = catalog[row['questionId']]
    chash = sha(canonical(card))
    snapshot.append(card)
    vals = {'prompt-key': canonical([card['prompt'], card['correctIndex'], card['answers'][card['correctIndex']]['text']]),
        'explanation': card['explanation'].encode(),
        **{f'note{i}': answer['note'].encode() for i, answer in enumerate(card['answers'])}}
    assert {f[0] for f in row['fields']} == set(vals)
    bound = dict(questionId=row['questionId'], cardCanonicalSha256=chash,
        verdict=row['verdict'], editorialAnalysis=row['editorialAnalysis'], fields=[])
    for name, verdict, analysis, refs in row['fields']:
        literal_hash = sha(vals[name])
        bound['fields'].append(dict(field=name, literalSha256=literal_hash, verdict=verdict,
            substantiveRead=True, claimAnalysis=analysis,
            proofs=[dict(proof_index[ref], proofId=ref, readerRole='independent', readerIdentity=IDENTITY,
                boundCardCanonicalSha256=chash, boundFieldLiteralSha256=literal_hash,
                proofAnalysis=analysis) for ref in refs]))
    receipt['cards'].append(bound)

write('independent-current.json', receipt)
write('proof-index.json', proof_index)
write('source-read-inventory.json', inventory)
write('freeze.json', dict(baselineCommit='0f97808', catalogPath=str(topic_path.relative_to(REPO)),
    topicByteSha256=sha(topic_path.read_bytes()), cards=snapshot,
    cardHashes={c['id']: sha(canonical(c)) for c in snapshot}, readerIdentity=IDENTITY))
print(json.dumps({'cards': len(receipt['cards']), 'fields': sum(len(c['fields']) for c in receipt['cards']),
    'manualCardVerdicts': [c['verdict'] for c in receipt['cards']], 'scriptCreatedVerdicts': 0}))
