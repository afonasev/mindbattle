"""Lossless FINAL schema aliases only; no editorial judgments."""
import pathlib,importlib.util,subprocess
D=pathlib.Path(__file__).parent;C=D.parents[3]
s=importlib.util.spec_from_file_location('o',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
R=D/'independent-polar32-33-cycle1-final';F=D/'bound-independent-polar32-33-cycle1-final';F.mkdir(exist_ok=True);freeze='ef587091d09cef3f0356d66ee57bee8806e6d4e3'
for p in R.glob('*.json'):assert p.read_bytes()==subprocess.check_output(['git','-C',str(C),'show',freeze+':'+str(p.relative_to(C))])
docs={n:m.read(R/n) for n in ['receipt.json','sources.json','peers.json','verification.json']};ps=docs['peers.json'];actual={p['id']:{**p,'sha256':p['canonicalSHA256']} for p in ps['actualCurrentPeers']}
for e in docs['receipt.json']['entries']:
 assert m.sha(e['currentCard'])==e['currentCardCanonicalSHA256'];actual[e['id']]={'id':e['id'],'topicId':'polar-regions','card':e['currentCard'],'sha256':e['currentCardCanonicalSHA256']}
pairs=[]
for row in ps['bilateralMAINComparisons']:
 left=actual[row['leftId']];right=actual[row['rightId']];assert left['sha256']==row['leftCardSHA256'] and right['sha256']==row['rightCardSHA256'];assert row['status']=='DISTINCT_MAIN' and row['directReverseAssessment']
 pairs.append({'left':{**left,'state':'ACTUAL_CURRENT','MAIN':row['leftERVC']},'right':{**right,'state':'ACTUAL_CURRENT','MAIN':row['rightERVC']},'leftToRight':row['leftToRight'],'rightToLeft':row['rightToLeft'],'originalAssessment':row})
ps['actualCurrentPeers']=list(actual.values());ps['bilateralMainComparisons']=pairs;assert not ps['relevantGenuineProposals'];ps['latestProposalSnapshots']=[]
src=docs['sources.json'];src['sources']=[dict(s) for s in src['rawSources'] if s['claimProof']]
for source in src['sources']:
 loc=[]
 for e in docs['receipt.json']['entries']:
  for g in e['sixLiteralCanonicalGroups']:
   for ref in g['sourcesLocators']:
    if ref.get('path')==source['path'] and ref['locator'] not in loc:loc.append(ref['locator'])
 source['locators']=loc;source['personalReadEvidence']=source['readEvidence'];assert loc and source['personalReadEvidence']
v=docs['verification.json'];v['catalogRawSHA256']=v['bindingChecks']['topicRawSHA256'];v['existingQA19']={'rawSHA256':v['bindingChecks']['QA19RawSHA256']}
for n,x in docs.items():
 x['technicalBindingProvenance']={'originalPath':str((R/n).relative_to(C)),'originalRawSHA256':m.raw(R/n),'originalCommit':freeze,'operation':'Exact pre2 reader originals retained. canonicalSHA256->sha256 alias; both focuscard/hash from exactreceipt as actualbody aliases. Pair left/right IDs and hash bind existing wholebodies, originaldirections/ERVC/directreverse unchanged. ClaimProofrawsources indexed with readEvidence alias and exact verbatim receiptlocators. No semanticjudgment or corebinderchange.'};m.write(F/n,x)
print('BOUND',len(actual),len(pairs))
