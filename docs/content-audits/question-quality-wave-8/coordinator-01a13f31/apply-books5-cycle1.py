"""Apply qualified exact solecycle1 SOURCE5, no quality credit."""
import pathlib,json,importlib.util,hashlib,subprocess
C=pathlib.Path(__file__).resolve().parents[4];D=pathlib.Path(__file__).parent;P=pathlib.Path('/Users/eaafonasev/Projects/mindbattle/planning')
s=importlib.util.spec_from_file_location('a',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.P=P
A=C/'docs/content-audits/question-quality-wave-8/process-v2-books7-cycle1-01a13f31/author';peers=json.loads((A/'peer-snapshot.json').read_text());catalog={}
for t in {x['topicId'] for x in peers['actualCurrentPeers']}:catalog.update({q['id']:q for q in json.loads((C/f'src/content/topics/{t}.json').read_text())['questions']})
for p in peers['actualCurrentPeers']:assert p['card']==catalog[p['id']] and m.sha(p['card'])==p['sha256']
ad=json.loads((A/'simultaneous-books11-14-addendum.json').read_text());assert ad
# Retain complete cross-topic/proposed SOURCE evidence; helper accepts same-topic peers.
subset={**peers,'actualCurrentPeers':[p for p in peers['actualCurrentPeers'] if p['topicId']=='books-publishing']}
m.apply(A,'01a13f98-8be4-7fd3-a70f-dc0ea9b54b27',[1,4,5,7,9],D/'apply-books5-cycle1.json',D/'qa-books5-cycle1.json',pathlib.Path(__file__),peerSnapshot=subset,concerns=['Substantive SOURCE cycle1 READY5 only; SOURCE HOLD3/6 excluded. Fresh FINAL must judge ownextra/plausibility/absoluteEASY, MAINbackcover vscoveranime and existingbookpeers.','Simultaneous books11–14 proposals addendum read bySOURCE; proposals notCURRENT yet and version11 may furtherchange; independent must compare actualCURRENT and relevant proposedversions explicitly.','Canonical wrongnote factpool allowed; nocrossnoteban. Scope fullbook5, sixgroups/fourvariants allsource/current exact.'])
