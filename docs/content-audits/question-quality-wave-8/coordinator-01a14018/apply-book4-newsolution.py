"""Apply a genuine new function route after SOURCE qualification completion."""
import pathlib,json,importlib.util
C=pathlib.Path(__file__).resolve().parents[4];D=pathlib.Path(__file__).parent
P=pathlib.Path('/Users/eaafonasev/Projects/mindbattle/planning')
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('apply_standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');m.P=P
A=C/'docs/content-audits/question-quality-wave-8/process-v2-books4-function-newsolution-01a13f31/author';F=A/'qualification-completion'
B=D/'qualified-book4-newsolution';B.mkdir(exist_ok=True)
for source,dest in [(A/'candidate.json',B/'candidate.json'),(F/'sourceproof.json',B/'sourceproof.json'),(F/'peer-snapshot.json',B/'peer-snapshot.json')]:dest.write_bytes(source.read_bytes())
peers=m.read(B/'peer-snapshot.json');catalog={}
for t in {x['topicId'] for x in peers['actualCurrentPeers']}:
 catalog.update({q['id']:q for q in m.read(C/f'src/content/topics/{t}.json')['questions']})
for p in peers['actualCurrentPeers']:assert p['card']==catalog[p['id']] and m.sha(p['card'])==p['sha256']
for p in peers['targetBilateralMAINComparisons']:
 assert p['peerCard']==catalog[p['peerId']] and m.sha(p['peerCard'])==p['peerSHA256']
 assert p['targetToPeerMAIN'] and p['peerToTargetMAIN']
assert len(peers['targetBilateralMAINComparisons'])==13
same={'actualCurrentPeers':[p for p in peers['actualCurrentPeers'] if p['topicId']=='books-publishing']}
qualified=m.apply(B,'01a1400c-337d-7603-a5da-f45ced91e06e',[4],None,None,None,qualifyOnly=True,peerSnapshot=same)
m.write(D/'qualification-book4-newsolution.json',{'stage':'SOURCE_QUALIFIED_NOT_INDEPENDENTLY_CERTIFIED','sourceCandidate':str((A/'candidate.json').relative_to(C)),'sourceCompletion':str(F.relative_to(C)),'copiedBytesUnchanged':True,'genuineNewSolution':'Prior terminal HOLD asked uncommon term; this proposed route asks physical function from observable location, with independent function choices. No unchanged secondcycle.','verified':{'currentPeers':139,'bilateralTargetMAIN':13,'literalGroups':6,'individualVariants':4},'qualification':qualified,'qualityCredit':0})
m.apply(B,'01a1400c-337d-7603-a5da-f45ced91e06e',[4],D/'apply-book4-newsolution.json',D/'qa-book4-newsolution.json',pathlib.Path(__file__),peerSnapshot=same,concerns=['Genuine new function route after previous term-route terminal HOLD; no unchanged secondcycle. Reader personally judges easy, uniqueness, plausible page-function alternatives, structural joining claim, all sources/notes and current+proposed bilateralMAIN.','Author repaired evidence bindings note0/1+variants0/1 only in completion; exact candidate unchanged. Full6/4 sourceproof personally read retained complete relevant CIEP/Bodleian/PeaceCorps contexts. All139CURRENTpeers+13target bilateral pairs root hash-bound. Canonical wrongnote factpool allowed.'])
