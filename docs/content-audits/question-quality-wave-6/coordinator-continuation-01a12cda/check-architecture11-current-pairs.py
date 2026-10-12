"""Preserve bindings for named substantive coordinator decisions, no auto grading."""
import hashlib
import json
import subprocess
from pathlib import Path

BASE = Path('docs/content-audits/question-quality-wave-6')
IDS = ['architecture-alhambra', 'architecture-machu-picchu', 'architecture-parthenon-city', 'architecture-colosseum-city', 'architecture-hagia-sophia-original-purpose', 'architecture-entasis-effect', 'architecture-cantilever-support', 'architecture-statue-liberty-city', 'architecture-fez', 'architecture-durham', 'architecture-bam']
def sha(raw): return hashlib.sha256(raw).hexdigest()
def cj(value): return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()
def git(rev, path): return subprocess.check_output(['git', 'show', rev + ':' + str(path)])
questions = {c['id']: c for c in json.loads(Path('src/content/topics/architecture.json').read_text())['questions']}
reads = [('author', '01a12e95-b8fd-7430-8c4b-e7117a71a378', '8011c20', 'architecture/resume-2026-10-12-fresh-rework16/author-review.json'), ('independent', '01a12eb9-b319-7d72-8748-170744fe01eb', 'c681e35', 'independent-pilot/resume-2026-10-12-architecture16-fresh-current/independent-receipt.json')]
records, originals = [], {}
for role, identity, rev, rel in reads:
    path = BASE / rel
    raw = git(rev, path)
    receipt = json.loads(raw)
    assert receipt['nativeAuthorIdentity' if role == 'author' else 'readerNativeIdentity'] == identity
    if role == 'independent': assert receipt['authorNativeIdentity'] == reads[0][1] != identity
    cards = {c['id']: c for c in receipt['cards']}
    for qid in IDS:
        q, c = questions[qid], cards[qid]
        assert c['currentCardSha256' if role == 'author' else 'wholeCardCurrentSha256'] == sha(cj(q))
        if role == 'independent': assert c['wholeCardVerdict'] == 'PASS'
        literals = {'prompt-key': {'prompt': q['prompt'], 'answers': [a['text'] for a in q['answers']], 'correctIndex': q['correctIndex'], 'key': q['answers'][q['correctIndex']]['text']}, 'explanation': q['explanation'], **{f'note{i}': a['note'] for i, a in enumerate(q['answers'])}}
        fields = {f['field']: f for f in c['fields']}
        assert fields.keys() == literals.keys()
        for name, literal in literals.items():
            f = fields[name]
            assert f['currentLiteral'] == literal and f['currentLiteralSha256'] == sha(cj(literal))
            if role == 'author':
                assert f['currentAuthorSourceVerdict'] == f['currentAuthorEditorialVerdict'] == 'PASS'
                assert f['authorAnalysis'] and f['individualAnalysis']
            else:
                assert f['sourceVerdict'] == f['editorialVerdict'] == f['roleVerdict'] == 'PASS'
                assert f['readerNativeIdentity'] == identity and f['authorNativeIdentity'] == reads[0][1]
                assert f['individualSourceAndEditorialAnalysis'] and f['authorAnalysisNotInherited']
            assert f['sourceProofs']
            for proof in f['sourceProofs']:
                # Both native schemas declare paths relative to their own receipt.
                capture = path.parent / proof['rawCapture']
                expected = proof['rawCaptureSha256']
                assert sha(capture.read_bytes()) == expected == sha(git('HEAD', capture)) == sha(git(rev, capture))
                blob = subprocess.check_output(['git', 'rev-parse', rev + ':' + str(capture)]).decode().strip()
                assert blob == proof['frozenGitBlob']
                assert proof['actualCaptureUrl'].startswith('https://') and proof['sourceUrl'].startswith('https://')
                # Retained UNESCO provenance blocks use captureFormat; other
                # current author proofs and all current reader proofs use rawFormat.
                fmt = proof['rawFormat'] if 'rawFormat' in proof else proof['captureFormat']
                assert fmt and proof['locator']
                assert sha(proof['quotedPassage'].encode()) == proof['quotedPassageSha256']
                if role == 'independent': assert proof['sourceClass'] and proof['quoteEncoding']
                originals[str(capture)] = expected
            records.append({'questionId': qid, 'cardCanonicalSha256': sha(cj(q)), 'field': name, 'literalSha256': f['currentLiteralSha256'], 'nativeLiteralRecipe': 'UTF-8 compact sorted JSON including strings and full prompt/answers/key object', 'actualRole': role, 'actualNativeIdentity': identity, 'receipt': str(path), 'receiptCommit': rev, 'receiptSha256': sha(raw), 'sourcePointers': f['sourceProofs']})
result = {'method': 'Explicit coordinator approval of these eleven current whole6 source/editorial readings after examining individual analyses/literals; source and native bindings only checked by script. Five current FIX/HOLD cards excluded. Relative raw paths and compact-sorted-JSON recipes preserved. Author rawFormat/captureFormat schemas explicitly adapted; nested historical nativeReaderIdentity/semanticSupportVerdict provenance is retained and is not the current author or reader role/verdict. No normalization of originals or generated grade.', 'cards': 11, 'roleFields': len(records), 'records': records, 'originals': originals, 'errors': 0}
(BASE / 'coordinator-continuation-01a12cda/architecture11-current-bindings.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print({'cards': 11, 'roleFields': len(records), 'originals': len(originals), 'errors': 0})
