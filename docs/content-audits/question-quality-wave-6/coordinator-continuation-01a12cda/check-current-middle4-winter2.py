"""Bind named substantive coordinator decisions; never generate editorial grades."""
import hashlib
import json
import subprocess
from pathlib import Path

BASE = Path('docs/content-audits/question-quality-wave-6')
OUT = BASE / 'coordinator-continuation-01a12cda'
MID = ['middle-ages-great-famine', 'middle-ages-excommunication', 'middle-ages-pilgrimage', 'middle-ages-black-death']
WIN = ['winter-sports-017', 'winter-sports-019']

def sha(raw): return hashlib.sha256(raw).hexdigest()
def cj(value, sort=False): return json.dumps(value, ensure_ascii=False, sort_keys=sort, separators=(',', ':')).encode()
def git(rev, path): return subprocess.check_output(['git', 'show', rev + ':' + str(path)])

records, originals = [], {}
for topic, ids, readings in [
    ('middle-ages', MID, [
        ('author', '01a12ca5-97a5-7860-9e4a-789a3f6bdcab', '4e920af', 'middle-ages/resume-2026-10-12-rework28/remainder23/author-current7-manual/receipt.json'),
        ('independent', '01a12d01-e56f-7e80-af27-3de96030301f', '961f35d', 'independent-pilot/resume-2026-10-12-middle23-current/reader-receipt.json')]),
    ('winter-sports', WIN, [
        ('author', '01a12d03-dca8-7300-bb0f-e5feaef03cc0', '6e23f33', 'winter-sports/resume-2026-10-12-safe-author4/followup2/author-current-repair-receipt.json'),
        ('independent', '01a12e88-841b-7a13-88c1-1b170ce87cbe', '7ca4c74', 'independent-pilot/resume-2026-10-12-winter2-followup-current/reader-receipt.json')])]:
    questions = {c['id']: c for c in json.loads(Path('src/content/topics', topic + '.json').read_text())['questions']}
    for role, identity, rev, rel in readings:
        path = BASE / rel
        raw = git(rev, path)
        d = json.loads(raw)
        if topic == 'middle-ages':
            actual = d['actualAuthorNativeIdentity']['codexThreadId'] if role == 'author' else d['actualNativeAgentIdentity']['CODEX_THREAD_ID']
        else:
            actual = d['agentIdentity'] if role == 'author' else d['readerIdentity']
        assert actual == identity
        cards = {c['questionId']: c for c in d['cards']}
        for qid in ids:
            card, c = questions[qid], cards[qid]
            assert c.get('wholeCardVerdict', c.get('verdict')) == 'PASS'
            assert c['cardCanonicalSha256'] == sha(cj(card))
            if topic == 'winter-sports': assert c['sortedCardSha256'] == sha(cj(card, True))
            lits = {'prompt-key': [card['prompt'], card['correctIndex'], card['answers'][card['correctIndex']]['text']], **{f'note{i}': a['note'] for i, a in enumerate(card['answers'])}, 'explanation': card['explanation']}
            fields = {f['field']: f for f in c['fields']}
            assert fields.keys() == lits.keys()
            for field, literal in lits.items():
                f = fields[field]
                if topic == 'middle-ages':
                    assert f['literal'] == literal and f['literalSha256'] == sha(cj(literal))
                    assert f['sourceVerdict'] == f['editorialVerdict'] == f['verdict'] == 'PASS'
                    assert f['manualAnalysis'] and f['substantiveRead'] if role == 'author' else f['manualIndividualAnalysis'] and f['sourceAnalysis'] and f['editorialAnalysis']
                    proofs = f['sourceProofs'] if role == 'author' else f['proofs']
                else:
                    literal = cj(literal).decode() if field == 'prompt-key' else literal
                    assert f['currentLiteral'] == literal and f['literalSha256'] == sha(literal.encode())
                    assert f['verdict'] == 'PASS' and f['substantiveRead'] if role == 'author' else f['sourceVerdict'] == f['editorialVerdict'] == 'PASS'
                    assert f['manualIndividualAnalysis']
                    proofs = f['proofs']
                assert proofs
                for p in proofs:
                    capture = Path(p['rawCapture'])
                    expected = p['rawCaptureSha256'] if topic == 'middle-ages' else p['rawSha256']
                    assert sha(capture.read_bytes()) == expected == sha(git('HEAD', capture))
                    assert p['sourceClass'] and p['captureFormat']
                    url = p['actualCaptureURL'] if topic == 'middle-ages' else p['actualUrl']
                    assert url.startswith('https://')
                    if topic == 'middle-ages':
                        assert p['quotedPassages']
                        for quote in p['quotedPassages']:
                            assert quote['locator'] and sha(quote['passage'].encode()) == quote['passageSha256']
                        if role == 'independent':
                            assert sha(git(p['frozenGitCommit'], capture)) == expected
                            assert subprocess.check_output(['git', 'rev-parse', p['frozenGitCommit'] + ':' + str(capture)]).decode().strip() == p['frozenGitBlob']
                    else:
                        assert p['locator'] and sha(cj(p['locator'], True)) == p['locatorSha256']
                        assert sha(p['quotedPassage'].encode()) == p['quotedPassageSha256']
                        assert len(capture.read_bytes()) == p['rawBytes']
                        if role == 'independent':
                            reader_capture = Path(p['readerRawCapture'])
                            assert sha(reader_capture.read_bytes()) == expected == sha(git('HEAD', reader_capture))
                            originals[str(reader_capture)] = expected
                            assert subprocess.check_output(['git', 'rev-parse', d['frozenEvidenceCommit'] + ':' + str(capture)]).decode().strip() == p['frozenRawGitBlob']
                    originals[str(capture)] = expected
                records.append({'questionId': qid, 'cardCanonicalSha256': sha(cj(card, True)), 'nativeInsertionOrderCardSha256': sha(cj(card)), 'field': field, 'literalSha256': f['literalSha256'], 'actualRole': role, 'actualNativeIdentity': identity, 'receipt': str(path), 'receiptCommit': rev, 'receiptSha256': sha(raw), 'sourcePointers': proofs})
report = {'method': 'Named substantive decisions Middle4 and Winter2 only. Charter source HOLD and Relic/Interdict correct-note FIX excluded. Native compact-JSON Middle literals and raw-UTF8 Winter note literals are explicit; originals unchanged. Binding assertions do not grade content.', 'cards': 6, 'roleFields': len(records), 'records': records, 'originals': originals, 'errors': 0}
(OUT / 'middle4-winter2-current-bindings.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
print({'cards': 6, 'roleFields': len(records), 'originals': len(originals), 'errors': 0})
