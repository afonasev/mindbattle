"""Transport exact independent polar3 aliases and bind existing semantic judgments only."""
import pathlib,importlib.util,copy
D=pathlib.Path(__file__).parent;C=D.parents[3]
s=importlib.util.spec_from_file_location('m',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
A=D.with_name('coordinator-01a142a3');S=A/'independent-polar3-initial';N=D/'bound-independent-polar3-initial';N.mkdir(exist_ok=False)
for fn in ['receipt.json','sources.json','peers.json','verification.json']:
 x=m.read(S/fn)
 if fn=='sources.json':
  for v in x['sources']:
   assert v['personallyRead'] is True;v['rawReadSHA256']=v['rawSHA256'];v['personalReadEvidence']=v['readingScope']
 if fn=='peers.json':
  for v in x['bilateralMainComparisons']:
   v['left']=copy.deepcopy(v['candidate']);v['right']=copy.deepcopy(v['actualCurrentPeer']);v['leftToRight']=v['candidateToPeer'];v['rightToLeft']=v['peerToCandidate']
 x['rootTransportProvenance']={'original':str((S/fn).relative_to(C)),'originalRawSHA256':m.raw(S/fn),'schemaAliasesOnly':True,'noSemanticChanges':True}
 m.write(N/fn,x)
case={'scope':'polar3-initial','topicId':'polar-regions','applyPaths':[str((A/'apply-polar3.json').relative_to(C))],'sourceFreeze':'ad45312d7b5b66e8c3260cf342998503d5fa277b','readerPath':str(N.relative_to(C)),'qaPath':str((A/'qa-parks13.json').relative_to(C)),'testedCatalogCommit':'386f0a210c8e4a6d67986b58ffd17cbe87c08911','qaReportCommit':'d9d540d3b8a2b5c9d08e6de68e6ceeb08bde578f','acceptedOrders':[3],'stage':'INITIAL','readerNativeId':'01a142fd-779b-70a2-910e-e79decf654cd','expectedCURRENT':840,'wave':8,'reportPath':str((D/'certification-polar3-initial-pass.json').relative_to(C)),'reportBase':{'SOURCEPrimaryFullContexts':True,'sourceFlaggedClosestPairIndependentlyAdjudicated':True},'coordinatorDecision':'Accept exact independent INITIAL PASS for SOURCE polar3 new Arctic majority-ice-sheet predicate. Reader supplies full6literal4wholevariants grounded in complete personally read NSIDC/NASA/NOAA primary contexts; actualEASY grounds distinguish majoritycover recognition from expert figures. Correctnote two existing sheets adds counterpart/count beyond prompt/key. Independent global11000MAINscan,113actualfullpeer bindings and16bilateralpairs include islands001 wholebody; reader explicitly distinguishes independently variable maximumarea rank from majorityicecover, sharedkey/peernote not used as MAIN. Root transports only exactexisting field aliases, binds SOURCEcriticalfreeze before actualsecond, live/tested/raw equality, QA19 and preleased guard. No third rootsemantic rewrite or SOURCE/QA-only credit.'}
m.write(D/'case-polar3.json',case);print(m.savecode([pathlib.Path(__file__),D/'case-polar3.json',*N.glob('*.json')],'Preserve exact polar3 independent PASS and alias-only transport840'))
