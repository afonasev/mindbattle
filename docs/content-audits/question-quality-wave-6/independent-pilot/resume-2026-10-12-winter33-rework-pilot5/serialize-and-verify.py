"""Serialize already-written manual verdicts; never infer editorial PASS from hashes."""
import copy
from collections import Counter
import hashlib
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import subprocess
import sys
from pypdf import PdfReader

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[4]
FREEZE = '4799684e9adf86532c13423abfe9f559840751ce'
AUTHOR_PATH = 'docs/content-audits/question-quality-wave-6/winter-sports/resume-2026-10-12-rework33/author-receipt.json'
TOPIC_PATH = 'src/content/topics/winter-sports.json'
IDS = ['winter-sports-' + x for x in ['007', '008', '017', '019', '024']]

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')

def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)

class VisibleNodes(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.skip = 0
        self.nodes = []

    def handle_starttag(self, tag, attrs):
        if tag in ['script', 'style', 'noscript']:
            self.skip += 1

    def handle_endtag(self, tag):
        if tag in ['script', 'style', 'noscript']:
            self.skip -= 1

    def handle_data(self, data):
        if not self.skip and data.strip():
            self.nodes.append(data.strip())

cache = {}
def passage(path, locator):
    if path not in cache:
        raw = (ROOT / path).read_bytes()
        if path.endswith('.pdf'):
            cache[path] = [p.extract_text() for p in PdfReader(ROOT / path).pages]
        else:
            parser = VisibleNodes()
            parser.feed(raw.decode('utf-8'))
            cache[path] = parser.nodes
    if 'pdfPage' in locator:
        return cache[path][locator['pdfPage'] - 1]
    selected = cache[path][locator['textNodeStart']:locator['textNodeEnd'] + 1]
    return ' '.join(' '.join(selected).split())

CLASSES = {
    'fis-equipment-2026.pdf': 'FIS — international ski and snowboard governing federation; equipment specifications',
    'figure-skating.html': 'Canadian Olympic Committee — national Olympic institution; sport overview, not ISU governing rules',
    'snowboard.html': 'Canadian Olympic Committee — national Olympic institution; sport overview, not FIS governing rules',
    'long-track.html': 'Canadian Olympic Committee — national Olympic institution; Olympic sport overview',
    'curling.html': 'World Curling — international curling governing federation; official sport explanation',
    'iihf-terminology.html': 'IIHF — international ice hockey governing federation; official terminology reference',
    'hockey-equipment-guide.pdf': 'Hockey Canada with Bauer — national hockey governing institution; player equipment fitting guide',
    'maine-ropeway-statute.html': 'Maine Legislature — official state statutory definitions of tramways',
    'isu-speed-skating-rules-2026.pdf': 'ISU — international skating governing federation; 2026 Speed Skating Sports Rules',
}

def proof_from_original(old):
    p = copy.deepcopy(old)
    raw = (ROOT / p['rawCapture']).read_bytes()
    assert sha(raw) == old['rawCaptureSha256'], p['rawCapture']
    actual = passage(p['rawCapture'], p['locator'])
    assert actual == old['passage'], (p['rawCapture'], p['locator'], 'author passage does not reproduce')
    assert sha(actual.encode()) == old['passageSha256']
    p['sourceClass'] = CLASSES[Path(p['rawCapture']).name]
    p['passage'] = actual
    p['passageSha256'] = sha(actual.encode('utf-8'))
    p['captureMethod'] = 'Complete unmodified original from committed bundle; independently opened and read. Passage re-extracted from full file, not author excerpt.'
    return p

def new_pdf_proof(path, url, title, page):
    text = passage(path, {'pdfPage': page})
    return {'sourceClass': CLASSES[Path(path).name], 'title': title, 'url': url,
            'rawCapture': path, 'rawCaptureSha256': sha((ROOT / path).read_bytes()),
            'captureFormat': 'pdf complete original bytes',
            'captureMethod': 'Complete original PDF; pypdf physical page extract_text(), unchanged UTF-8 output',
            'locator': {'pdfPage': page}, 'passage': text, 'passageSha256': sha(text.encode())}

author_raw = (ROOT / AUTHOR_PATH).read_bytes()
author = json.loads(author_raw)
assert author['agentIdentity'] == '01a12cc1-9d5d-74a1-99ba-6377bdfaed21'
assert sha(author_raw) == '71ca894abdd8bb39d27ee9604c07ec00b44fb3d5c2012b3a868fd3613e45ea00'
topic_raw = (ROOT / TOPIC_PATH).read_bytes()
frozen_topic_raw = git('show', FREEZE + ':' + TOPIC_PATH)
assert topic_raw == frozen_topic_raw, 'Winter topic source changed since freeze'
questions = json.loads(topic_raw)['questions']
selected = {q['id']: q for q in questions if q['id'] in IDS}
assert list(selected) == IDS and len(selected) == 5
manual = json.loads((OUT / 'manual-verdicts.json').read_text())

cards = []
for c in author['cards']:
    q = selected[c['questionId']]
    card_sha = sha(canonical(q))
    assert card_sha == c['cardCanonicalSha256']
    literals = [json.dumps([q['prompt'], q['correctIndex'], q['answers'][q['correctIndex']]['text']], ensure_ascii=False, separators=(',', ':'))]
    literals += [a['note'] for a in q['answers']] + [q['explanation']]
    decisions = manual[q['id'][-3:]]
    fields = []
    for i, (f, literal, decision) in enumerate(zip(c['fields'], literals, decisions['fields'], strict=True)):
        assert f['literal'] == literal
        assert f['literalSha256'] == sha(literal.encode('utf-8'))
        proofs = [proof_from_original(p) for p in f['proofs']]
        if q['id'] == 'winter-sports-007' and i in [0, 5]:
            p = proofs[0]
            proofs.append(new_pdf_proof(p['rawCapture'], p['url'], p['title'], 25))
        if q['id'] == 'winter-sports-007' and i == 4:
            p = proofs[0]
            proofs.append(new_pdf_proof(p['rawCapture'], p['url'], p['title'], 15))
        if q['id'] == 'winter-sports-008' and i == 1:
            path = str((OUT / 'current-url-originals/isu-speed-skating-rules-2026.pdf').relative_to(ROOT))
            url = next(s['url'] for s in json.loads((OUT / 'current-url-readback.json').read_text())['sources'] if '2026-Speed-Skating-Sports-Rules' in s['url'])
            proofs.append(new_pdf_proof(path, url, 'ISU Sports Rules — Speed Skating, effective 12 June 2026; Rules 203–206', 9))
        fields.append({'field': f['field'], 'literal': literal, 'literalSha256': sha(literal.encode()),
                       'verdict': decision[0], 'substantiveRead': True, 'claimAnalysis': decision[1], 'proofs': proofs})
    cards.append({'questionId': q['id'], 'cardCanonicalSha256': card_sha, 'verdict': 'FIX',
                  'editorialAnalysis': decisions['editorialAnalysis'], 'duplicateAnalysis': decisions['duplicateAnalysis'], 'fields': fields})

protected = [{'questionId': q['id'], 'cardCanonicalSha256': sha(canonical(q))} for q in questions if q['id'] not in IDS]
assert len(protected) == 95
duplicate_matches = {}
for qid, q in selected.items():
    matches = []
    for path in (ROOT / 'src/content/topics').glob('*.json'):
        data = json.loads(path.read_bytes())
        for other in data['questions']:
            if other['id'] != qid and other['prompt'].casefold().strip() == q['prompt'].casefold().strip():
                matches.append(other['id'])
    duplicate_matches[qid] = matches

identity = os.environ['CODEX_THREAD_ID']
assert identity == '01a12ccb-4877-7e60-93e1-5718382ba57f'
receipt = {'agentIdentity': identity, 'role': 'independent', 'actualAuthorIdentity': author['agentIdentity'],
           'authorReceiptPath': AUTHOR_PATH, 'authorReceiptSha256': sha(author_raw), 'authorCommit': FREEZE,
           'sourceFreezeCommit': FREEZE, 'checkedAt': '2026-10-12', 'scopeCount': 5, 'literalFieldCount': 30,
           'scopeExactIds': IDS, 'canonicalRecipes': {
               'cardCanonicalSha256': 'SHA256(UTF8(json.dumps(card, ensure_ascii=False, sort_keys=True, separators=(comma,colon)))); no newline',
               'prompt-key': 'UTF8 compact JSON array [prompt,correctIndex,answers[correctIndex].text]; ensure_ascii=False; no newline',
               'note/explanation': 'Exact decoded JSON string encoded UTF8; no newline added; no normalization',
               'HTML passage': 'HTMLParser(convert_charrefs=True); exclude script/style/noscript; nonempty data.strip() nodes zero-based; inclusive range; join nodes then collapse Unicode whitespace for passage only; raw bytes unchanged',
               'PDF passage': 'pypdf.PdfReader complete original; physical 1-based page; extract_text() string encoded UTF8 unchanged',
           }, 'readScope': 'All 30 current literal fields, all eight complete original publications (visible text/all PDF pages), exact current quoted passages independently read. Supplemental ISU full original captured, relevant Rule203–206 page9 plus pages27,29–32 read; no claim of reading every unrelated ISU rule.',
           'boundary': 'No future28 editorial reading; no source67 certification; no source/planning/ledger edits. Verdict history preserved. Mechanical duplicate scan does not certify global semantic absence.',
           'fieldVerdictCounts': dict(Counter(f['verdict'] for c in cards for f in c['fields'])),
           'cardVerdictCounts': {'FIX': 5, 'PASS': 0, 'HOLD': 0}, 'exactPromptDuplicateMatches': duplicate_matches,
           'currentUrlNote': 'Seven primary originals GET200 and byte-identical; World Curling curl GET403, web open succeeds and supports node41 claim. Supplemental ISU GET200. HTTP and SHA do not establish editorial PASS.',
           'cards': cards}

all_paths = sorted({p['rawCapture'] for c in cards for f in c['fields'] for p in f['proofs']})
source_readback = {'sourceFreezeCommit': FREEZE, 'topicWorkingSha256': sha(topic_raw), 'topicGitFreezeSha256': sha(frozen_topic_raw),
                   'protected95Count': 95, 'protected95CanonicalHashes': protected,
                   'protected95AggregateSha256': sha(canonical(protected)), 'fullOriginals': []}
for path in all_paths:
    raw = (ROOT / path).read_bytes()
    new_owned = path.startswith(str(OUT.relative_to(ROOT)) + '/')
    git_bytes = None if new_owned else git('show', FREEZE + ':' + path)
    if git_bytes is not None:
        assert raw == git_bytes
    source_readback['fullOriginals'].append({'rawCapture': path, 'sizeBytes': len(raw), 'workingSha256': sha(raw),
                                           'gitFreezeSha256': None if git_bytes is None else sha(git_bytes),
                                           'expectedGitBlobSha1': git('hash-object', path).decode().strip(),
                                           'newOwnedCapture': new_owned, 'workingEqualsGitFreeze': None if git_bytes is None else True})

def verify_stored():
    assert json.loads((OUT / 'reader-receipt.json').read_text()) == receipt
    assert json.loads((OUT / 'source-readback.json').read_text()) == source_readback
    for source in source_readback['fullOriginals']:
        path = source['rawCapture']
        git_bytes = git('show', 'HEAD:' + path)
        assert git_bytes == (ROOT / path).read_bytes(), path
        assert sha(git_bytes) == source['workingSha256']
    for path in OUT.rglob('*'):
        if path.is_file():
            relative = str(path.relative_to(ROOT))
            assert git('show', 'HEAD:' + relative) == path.read_bytes(), relative
    print('PASS: committed owned artifacts, 30 literals/proofs, 9 full original byte roundtrips, protected95 unchanged')

if '--verify-committed' in sys.argv:
    verify_stored()
else:
    (OUT / 'reader-receipt.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n')
    (OUT / 'source-readback.json').write_text(json.dumps(source_readback, ensure_ascii=False, indent=2) + '\n')
    print('PASS mechanical reproduction:', receipt['fieldVerdictCounts'], 'all five editorial FIX; protected95 unchanged')
