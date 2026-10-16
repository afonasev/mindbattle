"""Lossless exact reader body/hash/pair/source locator aliases. No new judgments."""
import pathlib,importlib.util,subprocess
D=pathlib.Path(__file__).parent;C=D.parents[3]
s=importlib.util.spec_from_file_location('o',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
R=D/'independent-polar31-initial';F=D/'bound-independent-polar31-initial';F.mkdir(exist_ok=True);freeze='a44efdc6d1735bbff9f0cf2ced8410c8527998cb'
for p in R.iterdir():
 if p.is_file():assert p.read_bytes()==subprocess.check_output(['git','-C',str(C),'show',freeze+':'+str(p.relative_to(C))])
docs={n:m.read(R/n) for n in ['receipt.json','sources.json','peers.json','verification.json']};ps=docs['peers.json'];actual={p['id']:{**p,'sha256':p['canonicalSHA256']} for p in ps['actualCurrentPeers']};focus=docs['receipt.json']['entries'][0];assert m.sha(focus['currentCard'])==focus['currentCardCanonicalSHA256'];actual[focus['id']]={'id':focus['id'],'topicId':'polar-regions','card':focus['currentCard'],'sha256':focus['currentCardCanonicalSHA256']};target=actual[focus['id']];pairs=[]
for row in ps['bilateralMAINComparisons']:
 peer=actual[row['peerId']];assert peer['sha256']==row['peerCanonicalSHA256'] and row['status']=='DISTINCT_MAIN';assert row['directReverseAssessment']
 pairs.append({'left':{**target,'state':'ACTUAL_CURRENT','MAIN':row['currentERVC']},'right':{**peer,'state':'ACTUAL_CURRENT','MAIN':row['peerERVC']},'leftToRight':row['currentToPeer'],'rightToLeft':row['peerToCurrent'],'originalAssessment':row})
ps['latestProposalSnapshots']=[]
for hist in ps['relevantGenuineProposals']:
 assert m.sha(hist['card'])==hist['canonicalSHA256'];live=next(q for q in m.read(C/f"src/content/topics/{'national-parks-nature' if hist['id'].startswith('national-parks') else 'polar-regions'}.json")['questions'] if q['id']==hist['id']);assert hist['card']==live
 if hist['id'] in actual:assert actual[hist['id']]['card']==hist['card'] and actual[hist['id']]['sha256']==hist['canonicalSHA256']
 else:actual[hist['id']]={'id':hist['id'],'topicId':'national-parks-nature' if hist['id'].startswith('national-parks') else 'polar-regions','card':hist['card'],'sha256':hist['canonicalSHA256']}
ps['actualCurrentPeers']=list(actual.values());ps['bilateralMainComparisons']=pairs
src=docs['sources.json'];src['sources']=[s for s in src['rawSources'] if s['claimProof']] # Explicit discovery-only stays in rawSources/hash checks, never promoted to claim proof
for source in src['sources']:
 loc=[]
 for entry in docs['receipt.json']['entries']:
  for group in entry['sixLiteralCanonicalGroups']:
   for ref in group['sourcesLocators']:
    if (ref.get('path',ref.get('source'))==source['path'] or source['path'] in ref.get('paths',[])) and ref['locator'] not in loc:loc.append(ref['locator'])
 source['locators']=loc;source['personalReadEvidence']=source.get('personalReadEvidence') or source.get('readScope');assert loc and source['personalReadEvidence']
v=docs['verification.json'];v['catalogRawSHA256']=v['bindingChecks']['topicRawSHA256'];v['existingQA19']={'rawSHA256':v['bindingChecks']['QA19RawSHA256']}
for name,doc in docs.items():doc['technicalBindingProvenance']={'originalPath':str((R/name).relative_to(C)),'originalRawSHA256':m.raw(R/name),'originalCommit':freeze,'operation':'Receipt6groups/4variants alreadyexact unchanged. canonicalSHA→sha alias; focus exactreceiptcard/hash as actualrow; bilateral schema aliases preserve originaldirections/ERVC/reverse; source locators exactverbatim samepath refs. Personally-read proposal history bodies verified exactlive and linked asactual body/hash aliases only. Five claimProof raw sources indexed as sources; explicit discovery-only preserved underrawSources but notclaimedproof. Existing personalReadEvidence preserved; readScope only fallback alias; locators from exactreceipt refs pathsarray. Nunavutactual150 percoverage corrected fromtask102 shorthand; no newsource/contentchange. No newsemanticjudgments/corebinderchanges.'};m.write(F/name,doc)
print('BOUND',len(actual),len(pairs))
