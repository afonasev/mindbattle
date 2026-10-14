import json,hashlib,os
b='/tmp/mindbattle-source-01a137d3-c9ba-7260-be2b-42f25ee03ab6/repairs-26-28'; root='/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle'
basep=b+'/physics27-current-neighbor-binding-addendum.json'; base=json.load(open(basep)); receipt=json.load(open(b+'/physics20-29-current.json')); qualified=json.load(open(b+'/physics20-29-source-qualified.json'))
H=lambda b:hashlib.sha256(b).hexdigest(); canon=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))
ids=qualified['full100IDOrder']; idxs=(16,24,38,68); relevant=[]
byid={n['currentFullCard']['id']:n for n in receipt['fullCurrentSemanticNeighbors']}
for i in idxs:
 cid=ids[i]
 if cid in byid:
  n=byid[cid]; full=n['currentFullCard']; ch=n['canonicalSha256']
 else:
  n=next(c for c in receipt['cards'] if c['index']==i); full=n['currentCard']; ch=n['canonicalSha256']; assert full['id']==cid
 relevant.append({'zeroBasedCurrentIndex':i,'id':cid,'canonicalSha256':ch,'fullCurrentCard':full})
notes={
16:{'claim':'physics-electromagnetic-induction-condition asks which emf appears when coil flux changes in an open circuit.','distinction':'That is the ordinary Faraday induction condition. #27 asks whether a material transition expels pre-existing magnetic flux; it does not ask for emf in an open circuit.'},
24:{'claim':'physics-lenz-law-direction asks for induced-current direction when a magnet approaches and recedes.','distinction':'That is a direction-of-current response to changing flux. #27 contrasts superconducting expulsion with ideal-conductor flux freezing across cooling.'},
38:{'claim':'physics-magnet-like-poles asks whether two like poles attract, repel, demagnetize, or switch poles.','distinction':'That is a static interaction between magnets. #27 is about field history inside a sample across a superconducting transition.'},
68:{'claim':'physics-ext-magnetic-flux asks which field-through-contour quantity appears in Faraday’s law.','distinction':'That is a definition of magnetic flux. #27 uses flux conservation as one premise but tests the distinct material-response contrast with the Meissner effect.'}}
for x in relevant:x['manualComparison']=notes[x['zeroBasedCurrentIndex']]
card27=next(c for c in receipt['cards'] if c['index']==27)
cap=card27['primaryEvidence']['sourceCapture']; passages=card27['primaryEvidence']['typedPrimaryContextPassages']; origin=next(x for x in qualified['targets'] if x['index']==27)['evidenceCommitObjects']
sourceproof={'rawBodyPath':cap['bodyPath'],'rawBodySha256':cap['sha256'],'rawBodyGitBlob':cap['bodyGitBlob'],'fullRangeManifestPath':cap['fullRangeManifestPath'],'fullRangeManifestSha256':cap['fullRangeManifestSha256'],'fullRangeManifestGitBlob':cap['fullRangeManifestGitBlob'],'initialHeadersPath':cap['initialHeadersPath'],'initialHeadersSha256':cap['initialHeadersSha256'],'initialHeadersGitBlob':cap['initialHeadersGitBlob'],'captureOriginCommit': origin['sourceCommit'],'captureOriginTree':origin['sourceCommitTree'],'currentReceiptCommit':'251c6b40f397c847e05c4c5eb59ce1b985a93488','currentReceiptTreeBytes':'Existing raw capture files are present in the 8a7522 capture commit; 8a7522 is not the original capture transaction. Capture-origin metadata identifies 4467eb2dc9ba1d1641a95206bf6eb15b257f206f.'}
# exact source commit/tree values are receipt facts; record copied values where available, with spelling copied programmatically below.
sourceproof['captureOriginCommit']=origin['sourceCommit']
sourceproof['captureOriginTree']=origin['sourceCommitTree']
sourceproof['normalizedLiteralSourceContexts']=passages
# verify raw entity against context/hash using current read-only existing file
rawpath=root+'/'+cap['bodyPath']; raw=open(rawpath,'rb').read(); assert H(raw)==cap['sha256']
rangeChecks=[]
for c in passages:
 sl=raw[c['startByte']:c['endByteExclusive']]
 assert sl==c['literalUtf8'].encode('utf-8')
 rangeChecks.append({'path':c['path'],'startByte':c['startByte'],'endByteExclusive':c['endByteExclusive'],'domLocator':c.get('domNodeType'),'literalSha256':H(sl),'bodySha256':c['bodySha256']})
correction={'schema':'mindbattle-physics27-provenance-dedup-correction-v1','producerNativeThreadId':'01a137d3-c9ba-7260-be2b-42f25ee03ab6','correctsAddendum':{'path':'physics27-current-neighbor-binding-addendum.json','sha256':H(open(basep,'rb').read()),'correctionType':'metadata/provenance and semantic-dedup elaboration only; no card wording or group changes'},'source2':{'path':'repair-packet-26-28-source2.json','sha256':H(open(b+'/repair-packet-26-28-source2.json','rb').read()),'immutable':True},'currentTarget':{'index':27,'id':'physics-meissner-effect','canonicalSha256':card27['canonicalSha256'],'whole6Sha256':card27['authorWhole6Sha256'],'sourceBinding':sourceproof,'exactRangeChecks':rangeChecks},'rawProvenanceCorrection':{'invalidEarlierPointer':'docs/content-audits/question-quality-wave-7/coordinator-continuation-01a13772/capture-only/physics20-29-current.json#cards[index=27].primaryEvidence.typedPrimaryContextPassages','correctCurrentRawBodyPath':cap['bodyPath'],'bodyExistsAndHashVerified':True,'bodySha256':cap['sha256'],'originCommit':origin['sourceCommit'],'originTree':origin['sourceCommitTree'],'transportCommit':'8a7522ee69dea7abd4ccbe17f4ecff95d7d599e5','transportCommitMeaning':'This commit carries the already captured source/body/evidence files; it is not misrepresented as the original source capture transaction.'},'currentRelatedMagneticNeighbors':{'indicesAreZeroBased':True,'indices':[16,24,38,68],'fullCards':relevant,'manualDistinctnessAnalysis':'#27 compares field history inside a sample during superconducting transition. Index16 covers ordinary Faraday emf in an open coil; index24 covers Lenz-law current direction when a magnet moves; index38 covers static repulsion of like magnetic poles; index68 defines magnetic flux in Faraday law. These four are magnetism-adjacent in vocabulary but test different predicates and response objects. The list/range hashes are provenance aids; this explicit comparison supplies the semantic review.'},'actualCurrentCardsBoundByBaseAddendum':{'addendumSha256':H(open(basep,'rb').read()),'fullCards20to29Included':10,'allFullSemanticNeighborsIncluded':14,'actualCurrent26Sha256':'5fdfcda0291cdfb4e744256d24fbc1c2baaa721a5891baaa978794605ab7b653','actualCurrent28Sha256':'df47f44bfa0fec86948f487b6c49b8e62853392bb9de7756daeea037af8366b8'},'status':{'wordingChanged':False,'qualityCredit':0,'humanAcceptance':'NOT_PERFORMED','coordinateWithCoordinatorBeforeAnyFurtherChange':True}}
out=b+'/physics27-provenance-dedup-correction.json';open(out,'w').write(json.dumps(correction,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n')
print('bytes',os.path.getsize(out),'sha256',H(open(out,'rb').read()),'neighbors',len(relevant),'ranges',len(rangeChecks))
print('origin',sourceproof['captureOriginCommit'],sourceproof['captureOriginTree'])
