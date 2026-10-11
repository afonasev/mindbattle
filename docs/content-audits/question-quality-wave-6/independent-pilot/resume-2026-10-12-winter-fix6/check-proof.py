"""Mechanical serialization/readback only. Manual judgments live in manual-decisions.json.

Run from repository root. Never edits catalog, author receipts, or root ledger.
"""
import hashlib
import json
import os
import subprocess
from html.parser import HTMLParser
from pathlib import Path
from pypdf import PdfReader

OWN = Path(__file__).resolve().parent
ROOT = Path.cwd().resolve()
AUTHOR = ROOT / 'docs/content-audits/question-quality-wave-6/resume-2026-10-11-repair14/winter-sports'
FREEZE = 'bb1075e'
IDENTITY = '01a12c65-7c69-74d1-a107-6d7c4e58c621'


def sha(b):
    return hashlib.sha256(b).hexdigest()


def canonical(v):
    return json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()


def git(*args):
    return subprocess.check_output(['git', *args])


def write(name, value):
    (OWN / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


class Nodes(HTMLParser):
    def __init__(self):
        super().__init__()
        self.nodes = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self.skip += 1

    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self.skip -= 1

    def handle_data(self, data):
        if not self.skip and data.strip():
            self.nodes.append(data.strip())


manual = json.loads((OWN / 'manual-decisions.json').read_text())
author = json.loads((AUTHOR / 'author-receipt.json').read_text())
frozen = json.loads((AUTHOR / 'freeze.json').read_text())
topic_path = 'src/content/topics/winter-sports.json'
topic_bytes = (ROOT / topic_path).read_bytes()
assert topic_bytes == git('show', FREEZE + ':' + topic_path)
assert sha(topic_bytes) == frozen['topicByteSha256']
catalog = {q['id']: q for q in json.loads(topic_bytes)['questions']}
assert set(manual['cards']) == {c['questionId'] for c in frozen['cards']}
snapshot = git('rev-parse', 'HEAD').decode().strip()
sources = {}
parsed = {}


def source(path):
    path = path.resolve()
    rel = str(path.relative_to(ROOT))
    if rel not in sources:
        raw = path.read_bytes()
        blob = git('show', FREEZE + ':' + rel)
        assert raw == blob
        sources[rel] = dict(path=rel, rawSha256=sha(raw), committedSha256=sha(blob),
                            gitBlob=git('rev-parse', FREEZE + ':' + rel).decode().strip(),
                            bytes=len(raw), workingEqualsCommittedBlob=True,
                            originalFormat=path.suffix[1:])
        if path.suffix == '.pdf':
            parsed[rel] = PdfReader(path)
        else:
            parser = Nodes()
            parser.feed(raw.decode())
            parsed[rel] = parser.nodes
    return rel


def proof(raw_proof):
    rel = source(AUTHOR / raw_proof['rawCapture'])
    loc = dict(raw_proof['locator'])
    if 'pdfPage' in loc:
        # Observed author page numbers match one-based physical pages.
        number = loc['pdfPage']
        loc = dict(pdfPhysicalPageOneBased=number, pdfPageIndexZeroBased=number - 1)
        quote = parsed[rel].pages[number - 1].extract_text()
        assert ' '.join(quote.split()) == ' '.join(raw_proof['passage'].split())
        method = 'pypdf from full original PDF; corrected explicit page bases'
    else:
        quote = '\n'.join(parsed[rel][loc['textNodeStart']:loc['textNodeEnd'] + 1])
        assert ' '.join(quote.split()) == ' '.join(raw_proof['passage'].split())
        method = 'HTMLParser nonempty stripped data nodes excluding script/style; zero-based inclusive range from full original HTML'
    title = raw_proof['title']
    source_class = raw_proof['sourceClass']
    if rel.endswith('wtgf-snowboard.html'):
        title = 'World Transplant Games Federation — Snowboarding'
        source_class = 'primary sporting event institution explanatory guide; not a snowboarding governing federation'
    return dict(readerIdentity=IDENTITY, role='independent-reader', sourceClass=source_class,
                title=title, url=raw_proof['url'], rawPath=rel,
                rawSha256=sources[rel]['rawSha256'], gitBlob=sources[rel]['gitBlob'],
                committedGitBlobSha256=sources[rel]['committedSha256'],
                locator=loc, quote=quote, quoteSha256=sha(quote.encode()), extractionMethod=method)


cards = []
for c in author['cards']:
    qid = c['questionId']
    q = catalog[qid]
    assert sha(canonical(q)) == c['cardCanonicalSha256']
    decision = manual['cards'][qid]
    fields = []
    for field in c['fields']:
        name = field['field']
        if name == 'prompt-key':
            literal = [q['prompt'], q['correctIndex'], q['answers'][q['correctIndex']]['text']]
        elif name == 'explanation':
            literal = q[name]
        else:
            literal = q['answers'][int(name[-1])]['note']
        assert literal == field['literal']
        literal_hash = sha(canonical(literal))
        # Author uses canonical JSON for arrays, UTF-8 plain text for strings.
        if isinstance(literal, str):
            literal_hash = sha(literal.encode())
        assert literal_hash == field['literalSha256']
        verdict, analysis = decision['fields'][name]
        proofs = [proof(p) for p in field['proofs']]
        # Additional original passages actually read by this reader.
        extra = []
        if qid == 'winter-sports-008' and name == 'note0':
            extra = [('fis-equipment-2026.pdf', {'pdfPage': 24})]
        if qid == 'winter-sports-017' and name in ('note1', 'explanation'):
            extra = [('fis-equipment-2026.pdf', {'pdfPage': 17})]
        if qid == 'winter-sports-019' and name in ('note0', 'explanation'):
            extra = [('alpine-skiing.html', {'textNodeStart': 71, 'textNodeEnd': 85})]
        if qid == 'winter-sports-019' and name == 'note3':
            extra = [('ski-jumping.html', {'textNodeStart': 69, 'textNodeEnd': 71})]
        if qid == 'winter-sports-024' and name in ('note0', 'explanation'):
            extra = [('maine-ropeway-statute.html', {'textNodeStart': 140, 'textNodeEnd': 140})]
        for filename, locator in extra:
            p = next(p for ac in author['cards'] for f in ac['fields'] for p in f['proofs'] if p['rawCapture'].endswith(filename)).copy()
            rel = source(AUTHOR / p['rawCapture'])
            p['locator'] = locator
            if 'pdfPage' in locator:
                p['passage'] = parsed[rel].pages[locator['pdfPage'] - 1].extract_text()
            else:
                p['passage'] = '\n'.join(parsed[rel][locator['textNodeStart']:locator['textNodeEnd'] + 1])
            proofs.append(proof(p))
        fields.append(dict(field=name, literal=literal, literalSha256=literal_hash,
                           readerIdentity=IDENTITY, role='independent-reader',
                           verdict=verdict, substantiveRead=True, manualAnalysis=analysis, proofs=proofs))
    assert len(fields) == 6
    cards.append(dict(questionId=qid, cardCanonicalSha256=sha(canonical(q)),
                      readerIdentity=IDENTITY, role='independent-reader',
                      verdict=decision['verdict'], editorialAnalysis=decision['editorialAnalysis'], fields=fields))

receipt = dict(readerIdentity=IDENTITY, role='independent-reader', nativeIdentityEvidence='CODEX_THREAD_ID',
               distinctFromAuthor=True, actualAuthorThreadFromDispatch='01a12c2b-8908-7971-8d70-7dbac0316099',
               historicalAuthorIdentityInFrozenMetadata=author['agentIdentity'],
               reviewedDate='2026-10-12', timezone='Asia/Yekaterinburg',
               sourceReadMode='Committed full originals, not a new live HTTP capture; original capture/verifiedAt dates retained.',
               authorFreezeCommit=git('rev-parse', FREEZE).decode().strip(),
               authorFreezeChain=['3b4a8f2','753ab51','b5e7375','bb1075e'],
               readSnapshotHead=snapshot, topicByteSha256=sha(topic_bytes),
               manualDecisionMethod=manual['decisionMethod'], cards=cards,
               counts=dict(read=6, fieldsRead=36, PASS=0, FIX=6, HOLD=0, newCertified=0,
                           repeatedCurrentCards=6, newPreviouslyUnreadCards=0, remainingUnreadAssigned=0,
                           remainingCardsNeedingFix=6),
               rootCertificationAction=False, humanAcceptance=False)
write('independent-receipt.json', receipt)
write('source-roundtrip.json', dict(readerIdentity=IDENTITY, date='2026-10-12', freeze=FREEZE,
                                   sources=list(sources.values()), topicGitBlob=git('rev-parse',FREEZE+':'+topic_path).decode().strip(),
                                   topicByteSha256=sha(topic_bytes), workingTopicEqualsCommitted=True,
                                   allSixCardHashesMatchFreeze=True,
                                   actualSourceLiteralRoleGitRoundtripBeforeManualDecision=True,
                                   pdfLocatorCorrection='Frozen author pdfPage is one-based physical despite its zero-based captureMethod label.',
                                   wtgfMetadataCorrection='HTML title and metadata identify World Transplant Games Federation, not World Snowboard Guide.'))
print(json.dumps(dict(cards=len(cards), fields=sum(len(c['fields']) for c in cards),
                      proofs=sum(len(f['proofs']) for c in cards for f in c['fields']),
                      sourceOriginals=len(sources), sourceBytesEqualGit=True,
                      manualCardVerdicts={c['questionId']:c['verdict'] for c in cards})))
