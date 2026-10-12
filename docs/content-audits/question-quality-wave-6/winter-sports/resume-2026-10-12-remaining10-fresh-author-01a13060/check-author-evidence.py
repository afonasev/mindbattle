#!/usr/bin/env python3
"""Bounded WinterSports remaining10 source, native-group and preservation check."""
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle')
assert Path.cwd().resolve() == ROOT.resolve(), f'wrong cwd: {Path.cwd()}'
assert Path(subprocess.run(['git', 'rev-parse', '--show-toplevel'], check=True, capture_output=True, text=True).stdout.strip()).resolve() == ROOT.resolve()
SCOPE = Path('docs/content-audits/question-quality-wave-6/coordinator-continuation-01a12fcd/winter-remaining10-fresh-author-01a13060-scope.json')
REPORT = Path('docs/content-audits/question-quality-wave-6/winter-sports/resume-2026-10-12-remaining10-fresh-author-01a13060/author-review.json')
RUNTIME = Path('src/content/topics/winter-sports.json')
REGISTER = Path('docs/content-audits/question-quality-wave-6/winter-sports/resume-2026-10-12-remaining10-after-first5-pair/primary-source-register.json')

def load(path):
    return json.loads(Path(path).read_text())

def canonical_hash(value):
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()
    return hashlib.sha256(raw).hexdigest()

def git(*args):
    return subprocess.run(['git', *args], check=True, capture_output=True, text=True).stdout.strip()

scope, report, current, register = load(SCOPE), load(REPORT), load(RUNTIME), load(REGISTER)
ids = scope['scopeIds']
assert len(ids) == 10 and len(set(ids)) == 10
assert report['scope'] == ids
baseline = json.loads(subprocess.run(['git', 'show', 'd4df6be:' + str(RUNTIME)], check=True, capture_output=True, text=True).stdout)
assert current['id'] == baseline['id'] and current['title'] == baseline['title']
assert [q['id'] for q in current['questions']] == [q['id'] for q in baseline['questions']]
assert len(current['questions']) == 100
byid = {q['id']: q for q in current['questions']}
basebyid = {q['id']: q for q in baseline['questions']}
assert set(byid) == set(basebyid)
assert len(scope['protected90']) == 90
for qid, expected in scope['protected90'].items():
    assert qid not in ids
    assert canonical_hash(byid[qid]) == expected, f'protected card changed: {qid}'
    assert canonical_hash(basebyid[qid]) == expected, f'protected baseline mismatch: {qid}'
for qid, slot in scope['preservedSlots'].items():
    assert byid[qid]['difficulty'] == slot['difficulty'], f'difficulty drift: {qid}'
    assert byid[qid]['correctIndex'] == slot['correctIndex'], f'key-index drift: {qid}'
for qid, expected in scope['baselineCards'].items():
    assert canonical_hash(basebyid[qid]) == canonical_hash(expected), f'scope baseline mismatch: {qid}'
assert len(report['cards']) == 10 and [c['id'] for c in report['cards']] == ids
for proof in report['cards']:
    c = byid[proof['id']]
    group = proof['nativeGroup']
    assert proof['difficulty'] == c['difficulty']
    assert proof['canonicalGroupSha256'] == canonical_hash(c)
    assert group['prompt'] == c['prompt']
    assert group['orderedAnswerTexts'] == [a['text'] for a in c['answers']]
    assert group['correctIndex'] == c['correctIndex']
    assert group['correctAnswerText'] == c['answers'][c['correctIndex']]['text']
    assert group['explanation'] == c['explanation']
    assert group['notes'] == [a['note'] for a in c['answers']]
    assert len(group['orderedAnswerTexts']) == 4 and len(group['notes']) == 4
    assert all(proof['editorialReview']['allFourAlternatives'])
    assert all(proof['editorialReview']['note0To3IndividualSupportAndAddedValue'])
assert [q['difficulty'] for q in current['questions']].count('easy') == 40
assert [q['difficulty'] for q in current['questions']].count('medium') == 40
assert [q['difficulty'] for q in current['questions']].count('hard') == 20
key_counts = {i: sum(q['correctIndex'] == i for q in current['questions']) for i in range(4)}
assert key_counts == {0: 25, 1: 25, 2: 25, 3: 25}, key_counts
source_rows = {s['id']: s for s in report['sourceCaptureVerification']}
assert len(source_rows) == 5
for prior in register['sources']:
    source = source_rows[prior['id']]
    p = Path(source['path'])
    data = p.read_bytes()
    assert len(data) == source['rawByteLength'] == prior['rawByteLength']
    assert hashlib.sha256(data).hexdigest() == source['rawSha256'] == prior['rawSha256']
    assert git('hash-object', str(p)) == source['gitBlobSha1'] == prior['gitBlobSha1']
    assert source['matchesPriorRegister'] is True
    assert p.as_posix() in git('ls-files', '--error-unmatch', str(p))
assert all(c['sourceReview']['sourceId'] in source_rows for c in report['cards'])
# Exact PDF page-text checks from the original register (one-based physical page numbers).
from pypdf import PdfReader
for source_id, pages in register['pdfPageDerivations'].items():
    source = source_rows[source_id]
    reader = PdfReader(str(source['path']), strict=False)
    for _, info in pages.items():
        text = ' '.join((reader.pages[info['physicalPageOneBased'] - 1].extract_text() or '').split())
        assert len(text) == info['derivedTextLengthCodePoints']
        assert hashlib.sha256(text.encode()).hexdigest() == info['derivedTextSha256']
for context in report['supplementalPdfPageContexts']:
    reader = PdfReader(context['rawSourcePath'], strict=False)
    text = ' '.join((reader.pages[context['physicalPageOneBased'] - 1].extract_text() or '').split())
    assert len(text) == context['normalizedTextLengthCodePoints']
    assert hashlib.sha256(text.encode()).hexdigest() == context['normalizedTextSha256']
print(json.dumps({'result':'PASS','runtimeCards':100,'scopeCards':10,'protected90':'exact','difficultyCounts':{'easy':40,'medium':40,'hard':20},'keyIndexCounts':key_counts,'sourceOriginals':len(source_rows),'nativeGroups':'10 with prompt+4 answers+key+explanation+4 notes','pdfExtracts':'registered pages and SHA verified'},ensure_ascii=False))
