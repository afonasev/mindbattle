"""Normalize exact author critical3 wrapper and qualify complete SOURCE37 only."""
import pathlib,importlib.util,json,subprocess
D=pathlib.Path(__file__).parent;C=D.parents[3]
def mod(n,p):
 s=importlib.util.spec_from_file_location(n,p);x=importlib.util.module_from_spec(s);s.loader.exec_module(x);return x
m=mod('o',D/'owned-tools.py');a=mod('a',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a.P=m.P
R=D/'source-polar37-minimal-complete/critical-3.json';v=m.read(R)
assert v['owner']==m.O and v['sourceNativeId']=='01a1510b-a2de-73e3-ae86-b18b1d2d9827'
for uid in [m.O,v['sourceNativeId'],'01a150d1-3383-7d30-ad23-76d70ec18813']:
 j=next(pathlib.Path('/Users/eaafonasev/.codex/sessions/2026/10/19').glob('*'+uid+'.jsonl'));assert sum(json.loads(l).get('type')=='compacted' for l in j.open())<2
e=v['reconciledCandidate'];c=e['proposedCard'];b=e['beforeCard'];assert m.sha(c)==e['afterHash']==v['candidateAfterHash']=='9907ebea5dc4f0cb3691955874cb04168d6ba599295daa3ea060b8bcfcf304a4'
assert m.sha(b)==e['beforeHash']==v['beforeHash'];assert all(b[k]==c[k] for k in ['id','difficulty','correctIndex','prompt']);assert all(b['answers'][k]==c['answers'][k] for k in [1,3]);assert [x['text'] for x in b['answers']]==[x['text'] for x in c['answers']]
sp=v['reconciledSourceProof'];assert sp['afterHash']==e['afterHash'] and sp['beforeHash']==e['beforeHash']
for source in v['reusedOriginalPrimaryContexts']:assert m.raw(C/source['path'])==source['sha256'] and source['personalReadNativeId']==v['sourceNativeId'] and source['captureReadProvenance']
projection=v['mainProjection'];rows=[];catalog={}
for source in projection['fullTopicFileInventory']:
 p=C/source['path'];assert m.raw(p)==source['fileSha256'];t=m.read(p)
 assert t['id']==source['topicId'] and len(t['questions'])==source['questionCount']
 for q in t['questions']:
  catalog[q['id']]={'topicId':t['id'],'card':q}
  rows.append({'topicId':t['id'],'id':q['id'],'prompt':q['prompt'],'answers':[x['text'] for x in q['answers']],'correctIndex':q['correctIndex']})
assert len(projection['fullTopicFileInventory'])==110 and len(rows)==11000 and rows==projection['rows'] and m.sha(rows)==projection['canonicalRowsSHA256']
assert m.sha(projection['fullTopicFileInventory'])==projection['topicFileInventoryCanonicalSHA256']
actual=v['liveCatalogState']['fullCurrentPeerBodies'];assert len(actual)==100
for p in actual:assert p['card']==catalog[p['id']]['card'] and m.sha(p['card'])==p['sha256']
byid={p['id']:p for p in actual}
for p in v['bilateralCurrentAssessments']:
 assert p['candidateId']==e['id'] and p['candidateCanonicalSHA256']==e['afterHash'];assert byid[p['currentPeerId']]['sha256']==p['currentPeerCanonicalSHA256'];assert p['candidateToPeerAndPeerToCandidateERVC'] and p['directReverse']
assert len(v['bilateralCurrentAssessments'])==11
B=D/'qualified-polar37-minimal';B.mkdir(exist_ok=True)
provenance={'rawWrapperPath':str(R.relative_to(C)),'rawWrapperSHA256':m.raw(R),'operation':'Lossless exact reconciledCandidate/sourceProof entries wrappers; source raw/read provenance and fullactual100/bilateral11 from same author wrapper unchanged. Full11000 MAIN rows stored once in raw wrapper and validated againstlive110files. No new SOURCE judgments or rawprimary duplication.','qualityCredit':0}
candidate={k:v[k] for k in ['owner','sourceNativeId','cycle','frozenSelectionBaseline']};candidate.update(catalogBaseline=v['catalogBaselineHistorical'],entries=[e],qualityCredit=0,technicalNormalization=provenance)
proof={k:v[k] for k in ['owner','sourceNativeId','cycle','stage','nativeJournal']};proof.update(rawSources=v['reusedOriginalPrimaryContexts'],entries=[sp],qualityCredit=0,technicalNormalization=provenance)
peers={'owner':m.O,'sourceNativeId':v['sourceNativeId'],'actualCurrentPeers':actual,'bilateralCurrentAssessments':v['bilateralCurrentAssessments'],'relevantGenuineProposals':v['relevantGenuineProposals'],'globalMAIN':{'count':11000,'canonicalRowsSHA256':projection['canonicalRowsSHA256'],'rowShape':projection['rowShape'],'sourceWrapper':str(R.relative_to(C)),'sourceWrapperRawSHA256':m.raw(R),'personalScreeningGround':projection['personalScreeningGround']},'technicalNormalization':provenance}
for name,data in [('candidate.json',candidate),('sourceproof.json',proof),('peer-snapshot.json',peers)]:m.write(B/name,data)
concerns=['Original37 FIRSTINITIAL not yet reviewed; no fixcycle consumed. Sourcefresh01a1510b native0 personallyfullread retained4primarycontexts, no inherited oldbe37post2 quality. Exact9907 changesonlynote0ownextra650km/note2presentLarsengeography/explanationgroundinglinehistorical2000-15/sourceverifieddate; goodMAIN/labels/key0/MEDIUM/originalnote1southernWeddell andnote3AmeryPrydz preserved. Before1ff rawfirstproposal saved654cbb; prequalification minimal reconciliation rawcritical3 is not INITIALfixcycle.', 'Independent all6literal/4WHOLEvariants fourseparatejudgments, full NASAGetz367science255-301/bounded265, BASRonne199full6-198/L152, originalNSIDCarticle67-155 successfulrecordordinal666/L78/81, AAP376science298-337/316-317. GetzMAINMarieByrdcoast/key0; correctnoteapprox650km extra beyondwholeprompt/key. Explanation definesgroundingline anddatedfullGetzretreat2000-2015, do not extrapolatepresenttrend orclaimunsupportedislandsegmentation. AbsoluteadultMEDIUM thematicregionalgeography/fourrealcomparableiceshelves, grammar/taxonomy/unique-key, no arbitrarymath/format/crossnoteban.', 'Authorfresh11000 fullMAIN projection taxonomymanifestorder hash07e245 (not sortedfilename393c; sameactualrows in differentdocumentedorder) all110files exactlive; same100fullCURRENT and11nearby bilateralMAIN/directreverse. Current34/35/36postimages, parks27now3e0f actual; no inventedsimultaneousproposals. Newparks28 SOURCE mayexist byreader time, assessrealrelevant proposedfullbodies ifneeded, no inherited otherquality. Root qualificationonly source, apply/affected19/independentINITIAL/rootbind remain separate; qualitycredit0.']
r=a.apply(B,v['sourceNativeId'],[37],D/'apply-polar37-minimal.json',D/'qa-polar37-minimal.json',pathlib.Path(__file__),qualifyOnly=True,peerSnapshot={'actualCurrentPeers':actual},concerns=concerns)
r.update(rawWrapper=str(R.relative_to(C)),rawWrapperSHA256=m.raw(R),sourceNativeCompactions=0,qualityCredit=0,fullGoal=2000,CURRENT=883,remaining=1117)
m.write(D/'qualification-polar37-minimal.json',r)
print(m.savecode(list(B.glob('*.json'))+[D/'qualification-polar37-minimal.json',pathlib.Path(__file__)],'Qualify fresh personalSOURCE37 minimal reconciled all6/4 exactglobal proof'))
