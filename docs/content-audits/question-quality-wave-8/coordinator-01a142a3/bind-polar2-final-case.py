"""Exact fresh OTHER polar4 schema transport and case, no new semantic judgment."""
import pathlib,importlib.util,copy
D=pathlib.Path(__file__).parent;C=D.parents[3]
s=importlib.util.spec_from_file_location('m',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
S=D/'independent-polar2-url-cycle1-final';N=D/'bound-independent-polar2-url-cycle1-final';N.mkdir(exist_ok=True)
for fn in ['receipt.json','sources.json','peers.json','verification.json']:
 x=m.read(S/fn)
 if fn=='sources.json':
  for v in x['sources']:
   assert v['personallyRead'] is True;v['rawReadSHA256']=v['rawSHA256'];v['personalReadEvidence']=v['readingMethod']
 if fn=='peers.json':
  by={}
  for p in x['actualCurrentPeers']+x.get('additionalCurrentPeers',[]):
   if p['id'] in by:assert p==by[p['id']]
   by[p['id']]=p
  x['actualCurrentPeers']=list(by.values())
  for v in x['bilateralMainComparisons']:
   v['left']=copy.deepcopy(v['candidate']);v['right']=copy.deepcopy(v['actualCurrentPeer']);v['leftToRight']=v['candidateToPeer'];v['rightToLeft']=v['peerToCandidate']
 x['rootTransportProvenance']={'original':str((S/fn).relative_to(C)),'originalRawSHA256':m.raw(S/fn),'schemaAliasesOnly':True,'noSemanticChanges':True}
 m.write(N/fn,x)
case={'scope': 'polar2-url-cycle1-final', 'topicId': 'polar-regions', 'applyPaths': ['docs/content-audits/question-quality-wave-8/coordinator-01a142a3/apply-polar2-url-cycle1.json'], 'sourceFreeze': '59582b742218c7e605ce53dce474a4a9bef675a6', 'readerPath': 'docs/content-audits/question-quality-wave-8/coordinator-01a142a3/bound-independent-polar2-url-cycle1-final', 'qaPath': 'docs/content-audits/question-quality-wave-8/coordinator-01a142a3/qa-polar2-url-cycle1.json', 'testedCatalogCommit': '13dedbbb641a61aba3ddb83bbbcc887eb98bac3c', 'qaReportCommit': 'a2235cea9276b9268f53dda42676bc62fc631344', 'acceptedOrders': [2], 'stage': 'FINAL', 'readerNativeId': '01a142fd-779b-70a2-910e-e79decf654cd', 'expectedCURRENT': 839, 'wave': 8, 'reportPath': 'docs/content-audits/question-quality-wave-8/coordinator-01a142a3/certification-polar2-url-cycle1-final-pass.json', 'reportBase': {'oneDirectedFixCycle': 1, 'soleDefectSourceURLTitleClosed': True, 'initialFIX': 'docs/content-audits/question-quality-wave-8/coordinator-01a142a3/independent-polar2-initial/receipt.json', 'allCardTextUnchanged': True}, 'coordinatorDecision': 'Accept independent FINAL PASS after one directedSOURCE cycle1 solely source.url/title to exact NOAA PMEL FAQ L214 queriedSouthPole inAntarctica. Fullcardtext incl ownnoteicecover unchanged and all6literal4wholevariants/sourceclaims independently rechecked or personallyreadunchangedfullbodies rebound with actualhashes, not SOURCE/QAverdict. Complete Antarctic continent/ice, Eurasia educationalcontinent convention/largestlandmass, NorthAmerican Arcticcoast and Australia smallestlandmass primarygrounds retained. Full114actualpeer snapshots/bilateral MAIN plus11000prompt/key globalretrieval bound, actualcurrent4 sameexactbody strictcertified839 differs SouthPole->continent vsAntarctica->surroundingocean. Independent MAIN judgment not inherited SOURCEreciprocallabel. Frozenmetadata, exactlive/reader/testedraw, SOURCEcriticalfreeze beforetrue2 andpreleasedguard mandatory; no remainingmetadata/text defect or ordinarysecondcycle.'}
m.write(D/'case-polar2-url-cycle1.json',case);print(m.savecode([pathlib.Path(__file__),D/'case-polar2-url-cycle1.json',*S.glob('*.json'),*N.glob('*.json')],'Preserve independent FINAL polar2 sole sourceURL fix original and schema transport'))
