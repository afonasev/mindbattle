import json,hashlib,os
b='/tmp/mindbattle-source-01a137d3-c9ba-7260-be2b-42f25ee03ab6/repairs-26-28'
cur=json.load(open(b+'/physics20-29-current.json')); qualified=json.load(open(b+'/physics20-29-source-qualified.json')); src2=json.load(open(b+'/repair-packet-26-28-source2.json'))
canon=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')); H=lambda x:hashlib.sha256(x.encode()).hexdigest()
# Verify the current card hashes in the copied e6 receipt against its full card preimages.
for c in cur['cards']:
 assert H(canon(c['currentCard']))==c['canonicalSha256'],(c['index'],'current card canonical hash mismatch')
# Bundle full actual current cards 20-29, including authoritative actual 26/28, and actual 27 itself.
current10=[{'index':c['index'],'id':c['id'],'canonicalSha256':c['canonicalSha256'],'whole6Sha256':c['authorWhole6Sha256'],'fullCurrentCard':c['currentCard']} for c in cur['cards']]
# Include every full current semantic neighbor from the authoritative e6 receipt.
neighbors=cur['fullCurrentSemanticNeighbors']
assert len(neighbors)==14
relevant={'physics-photon-energy-frequency','physics-ext-photoelectric-effect','physics-ext-debroglie-wavelength','physics-ext-work-function'}
reviewedRelevant=[]
for n in neighbors:
 c=n['currentFullCard']
 if c['id'] in relevant:
  reviewedRelevant.append({'id':c['id'],'canonicalSha256':n['canonicalSha256'],'reason':'Reviewed full card; same/general vocabulary only, distinct predicate from magnetic field exclusion/history.'})
assert {x['id'] for x in reviewedRelevant}==relevant
q27=next(x for x in qualified['targets'] if x['index']==27)
packet27=next(x for x in src2['targets'] if x['index']==27)
current27=next(x for x in cur['cards'] if x['index']==27)
assert packet27['id']==current27['id'] and packet27['hashBindings']['currentCanonicalSha256']==current27['canonicalSha256']
# Exact array identity is auxiliary only; the substantive comparison below carries the dedup review.
neighbor_list_hash=hashlib.sha256(canon(neighbors).encode()).hexdigest()
manual_reason=(
"#27 tests a material’s magnetic-field response when cooling through Tc with a field already present. In the actual current within-10 set, #26 asks for photoelectron maximum energy and emission rate under changed illumination, while #28 asks for electron matter-wave wavelength/diffraction from acceleration; neither shares the magnetic-flux-history predicate. Among the full semantic neighbors, the potentially adjacent photon-energy, photoelectric-effect, work-function, and de Broglie cards ask about photon energy, a named emission process, a binding-energy threshold, and naming λ=h/p. #27 instead contrasts Meissner field expulsion with ideal-conductor flux conservation. Other listed neighbors concern time dilation, spectra, uncertainty, magnetic-force direction/magnitude, Lenz-law current, Carnot bounds, entropy, SI mass, magnet polarity, specific/latent heat, or thermal conductivity. No same-predicate or inverse-duplicate current neighbor was found. This conclusion is based on reading the full current cards and individual predicates; the neighbor-array hash is only an integrity aid."
)
# Preserve old pre-apply neighbor binding distinctly, not as current evidence.
old_cards=q27['neighborBinding']['previousAndNextCurrentCards']
old_neighbors=[{'id':c['id'],'canonicalSha256':H(canon(c)),'fullCard':c} for c in old_cards]
addition={'schema':'mindbattle-physics27-current-neighbor-binding-addendum-v1','producerNativeThreadId':'01a137d3-c9ba-7260-be2b-42f25ee03ab6','target':{'index':27,'id':packet27['id'],'class':'hard','correctIndex':2,'wordingChanges':False,'candidateRuntimeCard':packet27['proposedRuntimeCard'],'candidateRuntimeCardSha256':packet27['hashBindings']['proposedCanonicalSha256'],'immutableSource2':{'path':'repair-packet-26-28-source2.json','sha256':hashlib.sha256(open(b+'/repair-packet-26-28-source2.json','rb').read()).hexdigest()}},'authoritativeCurrent':{'receiptSchema':cur['schema'],'receiptPath':'physics20-29-current.json','receiptSha256':hashlib.sha256(open(b+'/physics20-29-current.json','rb').read()).hexdigest(),'baselineTopicSha256':cur['topicRawSha256'],'runtimeCommit':cur['runtimeCommit'],'actualFullCurrentCard':current27['currentCard'],'actualCanonicalSha256':current27['canonicalSha256'],'actualWhole6Sha256':current27['authorWhole6Sha256'],'currentNeighborIndices':current27['dedup']['currentNeighborIndices']},'historicalQualificationNeighbors':{'qualificationReceiptSha256':hashlib.sha256(open(b+'/physics20-29-source-qualified.json','rb').read()).hexdigest(),'status':'Historical pre-apply/pre-opaque-runtime neighbors. These are not current evidence.','oldNeighborCards':old_neighbors},'currentScopeForIndependentDedup':{'fullCurrentCards20to29':current10,'all14FullCurrentSemanticNeighbors':neighbors,'fullRelevantNeighborRecords':reviewedRelevant,'currentSemanticNeighborArraySha256':neighbor_list_hash,'ownManualDedupReason':manual_reason,'verdict':'PASS_DISTINCT_CURRENT_SEMANTIC_SCOPE'},'sourceBindingUnchanged':packet27.get('sourceBinding'),'fieldReasonsUnchanged':packet27.get('groups'),'qualityStatus':{'count':557,'remaining':1443,'qualityCredit':0,'humanAcceptance':'NOT_PERFORMED','qualificationStatus':'Coordinator qualification pending; this addendum updates only current-neighbor binding.'},'currentRepairsHeld':{'26':'HOLD pending a source-complete I/(hf) proof and meaningful Hard redesign','28':'HOLD pending a meaningfully Hard theory-to-experiment redesign'},'future3049SourceStatus':'Captured sources available, not qualified; this addendum does not author that batch.'}
out=b+'/physics27-current-neighbor-binding-addendum.json';open(out,'w').write(json.dumps(addition,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n')
print('bytes',os.path.getsize(out),'sha256',hashlib.sha256(open(out,'rb').read()).hexdigest(),'current10',len(current10),'semanticNeighbors',len(neighbors),'relevantNeighbors',len(reviewedRelevant),'historicalNeighbors',len(old_neighbors))
print('current26sha',current10[6]['canonicalSha256'],'current28sha',current10[8]['canonicalSha256'],'actual27sha',current27['canonicalSha256'])
