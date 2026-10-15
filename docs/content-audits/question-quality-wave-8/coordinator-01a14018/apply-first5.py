"""Verify SOURCE cross-main completion; apply only with explicit --apply after freeze."""
import pathlib,importlib.util,sys,copy
C=pathlib.Path(__file__).resolve().parents[4];D=pathlib.Path(__file__).parent
P=pathlib.Path('/Users/eaafonasev/Projects/mindbattle/planning')
s=importlib.util.spec_from_file_location('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.P=P
A=C/'docs/content-audits/question-quality-wave-8/process-v2-books31-50-01a14018/author/source-completion/qualified-first5';candidate=m.read(A/'candidate.json');cross=m.read(A/'cross-main-completion.json');peers=m.read(A/'peer-snapshot.json')
cards={e['id']:e['proposedCard'] for e in candidate['entries']};cat={q['id']:q for q in m.read(C/'src/content/topics/books-publishing.json')['questions']};props={p['id']:p['card'] for p in peers['proposedPeers']}
oldActual={p['id']:p for p in peers['actualCurrentPeers']};deltaPath=A/'peer-delta-formats66-68.json';deltaDoc=m.read(deltaPath) if deltaPath.exists() else None;delta={p['id']:p for p in deltaDoc['actualCurrentPeers']} if deltaDoc else {}
for old in peers['actualCurrentPeers']:
 p=delta.get(old['id'],old);assert p['card']==cat[p['id']] and m.sha(p['card'])==p['sha256']
if deltaDoc:
 assert len(delta)==2 and m.raw(C/'src/content/topics/books-publishing.json')==deltaDoc['currentTopicRawSHA256']
 for p in deltaDoc['priorCurrentPeers']:assert p==oldActual[p['id']]
 for p in deltaDoc['targetBindings']:
  assert m.sha(cards[p['targetId']])==p['proposedCardSHA256'] and m.sha(cat[p['targetId']])==p['actualBeforeCardSHA256']
 assert {(p['targetId'],p['peerId']) for p in deltaDoc['bilateralMainDecisions']}=={(i,j) for i in cards for j in delta}
 for p in deltaDoc['bilateralMainDecisions']:assert all(p['meaningfulBilateralMAIN'].values()) and p['decision']=='DISTINCT_NONCOLLIDING_MAIN'
 old68=copy.deepcopy(oldActual['books-publishing-azw-format']['card']);old68['answers'][1]['note']=delta['books-publishing-azw-format']['card']['answers'][1]['note'];assert old68==delta['books-publishing-azw-format']['card']
for i,q in cards.items():assert props[i]==q
for pair in peers['relevantBilateralPairs']:
 for side in ['left','right']:
  p=pair[side];assert m.sha(p['card'])==p['sha256'] and p['card'] in [oldActual.get(p['id'],{}).get('card'),props.get(p['id'])]
assert m.raw(C/cross['retrievalProvenance']['path'])==cross['retrievalProvenance']['retrievalFileSHA256']
p=cross['peer'];current={q['id']:q for q in m.read(C/f"src/content/topics/{p['topicId']}.json")['questions']};assert p['card']==current[p['id']] and m.sha(p['card'])==p['canonicalCardSHA256']
for e in cross['candidates']:assert e['proposedCard']==cards[e['id']] and m.sha(e['proposedCard'])==e['candidateBinding']['proposedCardSHA256']
assert len(cross['bilateralMainDecisions'])==5
m.write(D/'qualification-first5.json',{'status':'SOURCE_QUALIFIED_WAIT_CATALOG_FREEZE','sourceCandidate':str((A/'candidate.json').relative_to(C)),'sourceCrossMainCompletion':str((A/'cross-main-completion.json').relative_to(C)),'sourcePeerDelta':str(deltaPath.relative_to(C)) if deltaDoc else None,'sourcePeerDeltaAuthorNativeId':'01a1401e-e3b4-7cd1-b422-d8b42acf650d','sourcePeerDeltaMetadataCaveat':'SOURCE sourceOwner.task labels the coordinator UUID; actual author is the retained native SOURCE01a1401e that produced this assigned file and returned it. Original metadata preserved.','sourceProof':'SOURCE personally read complete primary contexts and supplied corrected6/4/extra/levels; root technical preflight already passed. SOURCE cross1 and97 original same/proposed pairs hash-bound; changed66/68 superseded by explicit SOURCE2delta/10bilateralMAIN, not root semantic inference. No quality credit until independent CURRENT PASS.','verified':{'cards':5,'literalGroups':30,'individualVariants':20,'actualSameTopicPeers':100,'sameAndProposedPairs':len(peers['relevantBilateralPairs']),'crossMainPeers':1,'crossMainDecisions':5,'changedPeerDelta':len(delta),'freshChangedPeerBilateralDecisions':10 if deltaDoc else 0},'qualityCredit':0})
if '--apply' in sys.argv:
 m.apply(A,'01a1401e-e3b4-7cd1-b422-d8b42acf650d',[33,35,38,39,40],D/'apply-first5.json',D/'qa-first5.json',pathlib.Path(__file__),peerSnapshot=peers,peerAddendum=deltaPath if deltaDoc else None,concerns=['Only5 SOURCE-complete original31-50 candidates; original11 incompleteproof and4HOLD remain unqualified/unapplied. Corrected shifted extra locators and exact individual6/4, truthful Russian text and barcode symbol-vs-card distinction.','SOURCE cross-global MAIN retrieval110 files found one relevant barcode-history peer; SOURCE personally supplied5bilateraldecisions; current100 withSOURCE66/68delta/10freshbilateralMAIN supersedingold2peerhashes. Independently refresh actualCURRENT and relevantcross/proposed peers.','No unchanged automatic second cycle: this is INITIAL first actual appliedCURRENT5; one addressed substantive fixcycle only after independent INITIAL if needed.'])
