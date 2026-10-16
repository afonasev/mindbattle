"""Lossless exact reader body/hash/pair/source locator aliases. No new judgments."""
import pathlib,importlib.util,subprocess
D=pathlib.Path(__file__).parent;C=D.parents[3]
s=importlib.util.spec_from_file_location('o',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
R=D/'independent-parks24-initial';F=D/'bound-independent-parks24-initial';F.mkdir(exist_ok=True);freeze='eeeef884d32867c2ecde04e2463506715fdb8322'
for p in R.iterdir():
 if p.is_file():assert p.read_bytes()==subprocess.check_output(['git','-C',str(C),'show',freeze+':'+str(p.relative_to(C))])
docs={n:m.read(R/n) for n in ['receipt.json','sources.json','peers.json','verification.json']};ps=docs['peers.json'];actual={p['id']:{**p,'sha256':p['canonicalSHA256']} for p in ps['actualCurrentPeers']};focus=docs['receipt.json']['entries'][0];assert m.sha(focus['currentCard'])==focus['currentCardCanonicalSHA256'];actual[focus['id']]={'id':focus['id'],'topicId':'national-parks-nature','card':focus['currentCard'],'sha256':focus['currentCardCanonicalSHA256']};target=actual[focus['id']];pairs=[]
for row in ps['bilateralMAINComparisons']:
 peer=actual[row['peerId']];assert peer['sha256']==row['peerCanonicalSHA256'] and row['status']=='DISTINCT_MAIN';assert row['directReverseAssessment']
 pairs.append({'left':{**target,'state':'ACTUAL_CURRENT','MAIN':row['currentERVC']},'right':{**peer,'state':'ACTUAL_CURRENT','MAIN':row['peerERVC']},'leftToRight':row['currentToPeer'],'rightToLeft':row['peerToCurrent'],'originalAssessment':row})
ps['latestProposalSnapshots']=[];qualified=m.read(D/'qualified-parks24-new-independent/peer-snapshot.json')
for hist in ps['relevantGenuineProposals']:
 assert m.sha(hist['card'])==hist['canonicalSHA256']
 if hist['id'] in actual and hist['canonicalSHA256']==actual[hist['id']]['sha256']:assert hist['card']==actual[hist['id']]['card'];continue
 ref=next(p for p in qualified['latestProposals'] if p['id']==hist['id'] and p['canonicalSHA256']==hist['canonicalSHA256']);assert ref['card']==hist['card'];path=pathlib.Path(ref['path']);entry=next(e for e in m.read(path)['entries'] if e['id']==hist['id']);assert entry['proposedCard']==hist['card'] and entry['afterHash']==hist['canonicalSHA256']
 prop={**hist,'sha256':hist['canonicalSHA256'],'state':'HISTORICAL_'+hist['state']};ps['latestProposalSnapshots'].append({'sourcePath':str(path.relative_to(C)),'sourceRawSHA256':m.raw(path),'proposal':prop});pairs.append({'left':{**target,'state':'ACTUAL_CURRENT'},'right':prop,'leftToRight':hist['bothDirections'],'rightToLeft':hist['bothDirections'],'originalJointBothDirectionAssessment':hist['bothDirections']})
ps['actualCurrentPeers']=list(actual.values());ps['bilateralMainComparisons']=pairs
src=docs['sources.json'];src['sources']=src['rawSources']
for source in src['sources']:
 loc=[]
 for entry in docs['receipt.json']['entries']:
  for group in entry['sixLiteralCanonicalGroups']:
   for ref in group['sourcesLocators']:
    if ref.get('path',ref.get('source'))==source['path'] and ref['locator'] not in loc:loc.append(ref['locator'])
 source['locators']=loc;assert loc and source['personalReadEvidence']
v=docs['verification.json'];v['catalogRawSHA256']=v['bindingChecks']['topicRawSHA256'];v['existingQA19']={'rawSHA256':v['bindingChecks']['QA19RawSHA256']}
for name,doc in docs.items():doc['technicalBindingProvenance']={'originalPath':str((R/name).relative_to(C)),'originalRawSHA256':m.raw(R/name),'originalCommit':freeze,'operation':'Receipt6groups/4variants alreadyexact unchanged. canonicalSHA→sha alias; focus exactreceiptcard/hash as actualrow; bilateral schema aliases preserve originaldirections/ERVC/reverse; source locators exactverbatim samepath refs. Historical b7body exactreader/authorproposal linked tooriginalimmutableSOURCEcandidate forcorebinding only, notaccepted/current; raw HISTORICALHOLD state retained. No newsemanticjudgments/corebinderchanges.'};m.write(F/name,doc)
print('BOUND',len(actual),len(pairs))
