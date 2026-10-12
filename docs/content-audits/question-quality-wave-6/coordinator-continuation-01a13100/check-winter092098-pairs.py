"""Frozen evidence integrity only. Editorial decisions are written separately."""
import hashlib, json, subprocess
from pathlib import Path
from html.parser import HTMLParser
from pypdf import PdfReader

ROOT = Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle')
BASE = ROOT / 'docs/content-audits/question-quality-wave-6'
OUT = BASE / 'coordinator-continuation-01a13100'
AP = BASE / 'winter-sports/resume-2026-10-12-remaining10-fresh-author-01a13060/author-review-v3.json'
RP = BASE / 'independent-pilot/resume-2026-10-12-middle-current15-pilot5/winter-current-remaining10-3476502/reader-receipt.json'
IDS = ['winter-sports-092', 'winter-sports-098']
sha = lambda b: hashlib.sha256(b).hexdigest()
cj = lambda v: json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()
def frozen(rev, path):
    return subprocess.check_output(['git', 'show', rev + ':' + str(path.relative_to(ROOT))], cwd=ROOT)
assert AP.read_bytes() == frozen('3476502', AP) == frozen('HEAD', AP)
assert sha(AP.read_bytes()) == 'f4da4fe3f704b0df80d8ff4b171dd0c329222308aacc7592782883abe903bd9d'
assert RP.read_bytes() == frozen('75df9f6', RP) == frozen('HEAD', RP)
a, r = json.loads(AP.read_text()), json.loads(RP.read_text())
assert a['authorNativeId'] == r['authorIdentity'] != r['readerIdentity']
assert r['authorReceiptSHA256'] == sha(AP.read_bytes())
runtime = ROOT / 'src/content/topics/winter-sports.json'
qs = {q['id']: q for q in json.loads(runtime.read_text())['questions']}
baseline = {q['id']: q for q in json.loads(frozen('a474cc9', runtime))['questions']}
class Visible(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True); self.skip = 0; self.nodes = []
    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'): self.skip += 1
    def handle_endtag(self, tag):
        if tag in ('script', 'style'): self.skip -= 1
    def handle_data(self, data):
        if not self.skip and data.strip(): self.nodes.append(data.strip())
sources, contexts, records = {}, {}, []
for source in r['rawSources']:
    if source['id'] not in ('icr', 'bcs'): continue
    path = ROOT / source['capturePath']; raw = path.read_bytes()
    assert raw == frozen('3476502', path) == frozen('75df9f6', path) == frozen('HEAD', path)
    assert len(raw) == source['rawByteLength'] and sha(raw) == source['rawSha256']
    assert subprocess.check_output(['git', 'hash-object', str(path)], cwd=ROOT, text=True).strip() == source['gitBlobSha1']
    sources[source['id']] = source
    if source['id'] == 'icr':
        text = PdfReader(path, strict=False).pages[82].extract_text()
        contexts['icr'] = ' '.join(text.split())
    else:
        parser = Visible(); parser.feed(raw.decode()); contexts['bcs'] = ' '.join(' '.join(n.split()) for n in parser.nodes)
    records.append({'source': source['id'], 'path': source['capturePath'], 'sha256': sha(raw), 'contextSHA256': sha(contexts[source['id']].encode())})
bindings = []
for id in IDS:
    q = qs[id]; assert q == baseline[id]
    ac = next(c for c in a['cards'] if c['id'] == id)
    rc = next(c for c in r['cards'] if c['id'] == id)
    assert sha(cj(q)) == ac['wholeCardCanonicalSha256'] == rc['canonicalCardSHA256']
    assert rc['wholeSourceVerdict'] == rc['wholeEditorialVerdict'] == rc['wholeVerdict'] == 'PASS'
    expected = {'prompt-answers-key': {'prompt': q['prompt'], 'orderedAnswerTexts': [v['text'] for v in q['answers']], 'correctIndex': q['correctIndex'], 'correctAnswerText': q['answers'][q['correctIndex']]['text']}, 'explanation': q['explanation'], **{'note'+str(i): v['note'] for i,v in enumerate(q['answers'])}}
    assert [g['group'] for g in ac['groups']] == [g['group'] for g in rc['fields']] == list(expected)
    for ag, rg in zip(ac['groups'], rc['fields']):
        name = ag['group']; literal = expected[name]
        assert literal == ag['nativeLiteral'] == rg['currentNativeLiteral']
        assert sha(cj(literal)) == ag['literalSha256'] == rg['canonicalJSONSHA256']
        assert ag['sourceEditorialAnalysis'] and rg['manualSourceReason'] and rg['manualEditorialReason']
        proofs = []
        for p in rg['sourceProofs']:
            source = sources[p['sourceId']]; context = contexts[p['sourceId']]; ip = p['independentProof']
            assert p['rawSourceSHA256'] == source['rawSha256'] and p['sourceGitBlob'] == source['gitBlobSha1']
            assert sha(context.encode()) == ip.get('collapsedPageUTF8SHA256', ip.get('visibleTextSHA256'))
            start = ip['codepointOffset0']; quote = context[start:start+ip['codepointLength']]
            assert quote == ip['exactDerivedQuote'] == p['historicalExactQuote']
            assert sha(quote.encode()) == p['historicalQuoteUTF8SHA256'] == ip.get('derivedQuoteUTF8SHA256', ip.get('quoteUTF8SHA256'))
            ab = next(b for b in ag['sourceBindings'] if b['quoteId'] == p['quoteId'])
            aq = next(v for v in a['quoteRegistry'] if v['id'] == p['quoteId'])
            assert ab['rawSha256'] == source['rawSha256'] and ab['quoteSha256'] == sha(quote.encode())
            assert aq['quote'] == quote
            proofs.append({'quoteId': p['quoteId'], 'sourceSHA256': source['rawSha256'], 'quoteSHA256': sha(quote.encode()), 'offset': start})
        bindings.append({'id': id, 'group': name, 'literalSHA256': sha(cj(literal)), 'cardSHA256': sha(cj(q)), 'proofs': proofs})
all_questions = []
for path in (ROOT/'src/content/topics').glob('*.json'):
    for q in json.loads(path.read_text()).get('questions', []):
        text = q['prompt']+' '+q['answers'][q['correctIndex']]['text']
        if any(t in text.casefold() for t in ['омолога', 'сертификат', 'боб', 'bobsleigh', 'экипаж', 'тормозящ', 'brakeman']):
            all_questions.append({'id': q['id'], 'prompt': q['prompt'], 'key': q['answers'][q['correctIndex']]['text'], 'sha256': sha(cj(q))})
report = {'purpose': 'integrity and catalogue candidate capture, no automated quality scoring', 'ids': IDS, 'roleGroups': 24, 'errors': 0, 'author': a['authorNativeId'], 'reader': r['readerIdentity'], 'authorCommit': '3476502', 'readerCommit': '75df9f6', 'authorReceiptSHA256': sha(AP.read_bytes()), 'readerReceiptSHA256': sha(RP.read_bytes()), 'sources': records, 'bindings': bindings, 'catalogueDuplicateCandidates': all_questions}
(OUT/'winter092098-pair-integrity.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
print({'cards': 2, 'roleGroups': 24, 'proofBindings': sum(len(b['proofs']) for b in bindings), 'fullSources': len(sources), 'catalogueCandidates': len(all_questions), 'errors': 0})
for q in all_questions: print(q['id'], q['prompt'], 'KEY', q['key'])
