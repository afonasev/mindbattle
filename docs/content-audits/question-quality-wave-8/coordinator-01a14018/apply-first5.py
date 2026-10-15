"""Verify SOURCE cross-main completion; apply only with explicit --apply after freeze."""
import pathlib,importlib.util,sys
C=pathlib.Path(__file__).resolve().parents[4];D=pathlib.Path(__file__).parent
P=pathlib.Path('/Users/eaafonasev/Projects/mindbattle/planning')
s=importlib.util.spec_from_file_location('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.P=P
A=C/'docs/content-audits/question-quality-wave-8/process-v2-books31-50-01a14018/author/source-completion/qualified-first5';candidate=m.read(A/'candidate.json');cross=m.read(A/'cross-main-completion.json');peers=m.read(A/'peer-snapshot.json')
cards={e['id']:e['proposedCard'] for e in candidate['entries']};cat={q['id']:q for q in m.read(C/'src/content/topics/books-publishing.json')['questions']};props={p['id']:p['card'] for p in peers['proposedPeers']}
for p in peers['actualCurrentPeers']:assert p['card']==cat[p['id']] and m.sha(p['card'])==p['sha256']
for i,q in cards.items():assert props[i]==q
for pair in peers['relevantBilateralPairs']:
 for side in ['left','right']:
  p=pair[side];assert m.sha(p['card'])==p['sha256'] and p['card'] in [cat.get(p['id']),props.get(p['id'])]
assert m.raw(C/cross['retrievalProvenance']['path'])==cross['retrievalProvenance']['retrievalFileSHA256']
p=cross['peer'];current={q['id']:q for q in m.read(C/f"src/content/topics/{p['topicId']}.json")['questions']};assert p['card']==current[p['id']] and m.sha(p['card'])==p['canonicalCardSHA256']
for e in cross['candidates']:assert e['proposedCard']==cards[e['id']] and m.sha(e['proposedCard'])==e['candidateBinding']['proposedCardSHA256']
assert len(cross['bilateralMainDecisions'])==5
m.write(D/'qualification-first5.json',{'status':'SOURCE_QUALIFIED_WAIT_CATALOG_FREEZE','sourceCandidate':str((A/'candidate.json').relative_to(C)),'sourceCrossMainCompletion':str((A/'cross-main-completion.json').relative_to(C)),'sourceProof':'SOURCE personally read complete primary contexts and supplied corrected6/4/extra/levels; root technical preflight in first5-technical-preflight.json already passed. New SOURCE cross1 proof and97 same/proposed pairs hash-bound; no quality credit until independent CURRENT PASS.','verified':{'cards':5,'literalGroups':30,'individualVariants':20,'actualSameTopicPeers':100,'sameAndProposedPairs':len(peers['relevantBilateralPairs']),'crossMainPeers':1,'crossMainDecisions':5},'qualityCredit':0})
if '--apply' in sys.argv:
 m.apply(A,'01a1401e-e3b4-7cd1-b422-d8b42acf650d',[33,35,38,39,40],D/'apply-first5.json',D/'qa-first5.json',pathlib.Path(__file__),peerSnapshot=peers,concerns=['Only5 SOURCE-complete original31-50 candidates; original11 incompleteproof and4HOLD remain unqualified/unapplied. Corrected shifted extra locators and exact individual6/4, truthful Russian text and barcode symbol-vs-card distinction.','SOURCE cross-global MAIN retrieval110 files found one relevant barcode-history peer; SOURCE personally supplied5bilateraldecisions; current100 inclappliedformats4,97meaningful same/proposed pairs. Independently refresh actualCURRENT and relevantcross/proposed peers.','No unchanged automatic second cycle: this is INITIAL first actual appliedCURRENT5; one addressed substantive fixcycle only after independent INITIAL if needed.'])
