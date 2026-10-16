"""Exact fresh OTHER polar4 schema transport and case, no new semantic judgment."""
import pathlib,importlib.util,copy
D=pathlib.Path(__file__).parent;C=D.parents[3]
s=importlib.util.spec_from_file_location('m',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
S=D/'independent-polar4-initial';N=D/'bound-independent-polar4-initial';N.mkdir(exist_ok=True)
for fn in ['receipt.json','sources.json','peers.json','verification.json']:
 x=m.read(S/fn)
 if fn=='sources.json':
  for v in x['sources']:
   assert v['personallyRead'] is True;v['rawReadSHA256']=v['rawSHA256'];v['personalReadEvidence']=v['readingMethod']
 if fn=='peers.json':
  by={}
  for p in x['actualCurrentPeers']+x['additionalCurrentPeers']:
   if p['id'] in by:assert p==by[p['id']]
   by[p['id']]=p
  x['actualCurrentPeers']=list(by.values())
  for v in x['bilateralMainComparisons']:
   v['left']=copy.deepcopy(v['candidate']);v['right']=copy.deepcopy(v['actualCurrentPeer']);v['leftToRight']=v['candidateToPeer'];v['rightToLeft']=v['peerToCandidate']
 x['rootTransportProvenance']={'original':str((S/fn).relative_to(C)),'originalRawSHA256':m.raw(S/fn),'schemaAliasesOnly':True,'noSemanticChanges':True}
 m.write(N/fn,x)
case={'scope':'polar4-initial','topicId':'polar-regions','applyPaths':[str((D/'apply-polar4.json').relative_to(C))],'sourceFreeze':'71aae6367a38c865a07b564b7c19fc85ad79bb8c','readerPath':str(N.relative_to(C)),'qaPath':str((D/'qa-polar4.json').relative_to(C)),'testedCatalogCommit':'0579726ce1e343cee0ba748962a48fe5bed121e7','qaReportCommit':'ad3a1b7c453f41a83c4897fe4878b93a8d1e03e5','acceptedOrders':[4],'stage':'INITIAL','readerNativeId':'01a142fd-779b-70a2-910e-e79decf654cd','expectedCURRENT':838,'wave':8,'reportPath':str((D/'certification-polar4-initial-pass.json').relative_to(C)),'reportBase':{'SOURCEPrimaryFullContexts':True,'sourceFlaggedClosePairIndependentlyAdjudicated':True},'coordinatorDecision':'Accept independent INITIAL PASS for exact SOURCE4. Full AAP directly grounds surrounding SouthernOcean and correct ownnote additional connectedthreeoceans/currentdirection; NOAA CPC primary full12linebody grounds IndianOcean ownextent. Full6literal4wholevariants and absoluteEASY independently read; reader personally assessed all current18snapshots/17bilateralpairs and11000MAINscan. SOURCE called order2 close reciprocal; independent OTHER actually read bothfullMAIN and found distinct relations SouthPole->continent vsAntarctica->surroundingocean, notdirectreverse ofsameedge; root binds exactversions and doesnotinherit source label or silentlyskip flaggedpair. Root only schema transport original independentgrounds, no new rootsemantictext. FrozenID/topic/order/EASY/key1, sourcecriticalfreeze beforeactualsecond, QA19exacttestedtopicraw and guard/preleased certification required.'}
m.write(D/'case-polar4.json',case);print(m.savecode([pathlib.Path(__file__),D/'case-polar4.json',*S.glob('*.json'),*N.glob('*.json')],'Preserve polar4 independent INITIAL PASS original and schema transport'))
