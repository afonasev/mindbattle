import pathlib,json,importlib.util,copy
D=pathlib.Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle/docs/content-audits/question-quality-wave-8/coordinator-01a142a3')
spec=importlib.util.spec_from_file_location('owned',D/'owned-tools.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
S=D/'independent-parks6-8-cycle1-final';N=D/'bound-independent-parks6-8-cycle1-final';N.mkdir(exist_ok=True)
for fn in ['receipt.json','sources.json','peers.json','verification.json']:
 x=m.read(S/fn)
 if fn=='sources.json':
  for v in x['sources']:
   v['rawReadSHA256']=v['rawSHA256'];v['personalReadEvidence']=v['readingMethod'];assert v['personallyRead'] is True
 if fn=='peers.json':
  for v in x['bilateralMainComparisons']:
   v['left']=copy.deepcopy(v['candidate']);v['right']=copy.deepcopy(v['actualCurrentPeer']);v['leftToRight']=v['candidateToPeer'];v['rightToLeft']=v['peerToCandidate']
  x['proposedBilateralMAINComparisons']=copy.deepcopy(x['all3CurrentMutualPairs'])
  for v in x['proposedBilateralMAINComparisons']:
   for side in ['left','right']:v[side]['id']=v[side]['card']['id']
 x['rootTransportProvenance']={'original':str((S/fn).relative_to(m.C)),'originalRawSHA256':m.raw(S/fn),'mappingOnly':True,'noNewSemanticJudgment':True}
 m.write(N/fn,x)
case=m.read(D/'case-parks6-8-cycle1.json');case['readerPath']=str(N.relative_to(m.C));m.write(D/'case-parks6-8-cycle1.json',case)
print(m.savecode([*S.glob('*.json'),*N.glob('*.json'),D/'case-parks6-8-cycle1.json'],'Preserve fresh OTHER FINAL3 original and exact schema transport'))
