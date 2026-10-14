import json,hashlib,os
b='/tmp/mindbattle-source-01a137d3-c9ba-7260-be2b-42f25ee03ab6/repairs-26-28'
cur=json.load(open(b+'/physics20-29-current.json')); q=json.load(open(b+'/physics20-29-source-qualified.json')); source2=json.load(open(b+'/repair-packet-26-28-source2.json'))
basepath=b+'/physics27-current-neighbor-binding-addendum.json'; corrpath=b+'/physics27-provenance-dedup-correction.json'
H=lambda x:hashlib.sha256(x).hexdigest(); canon=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))
order=q['full100IDOrder']; assert len(order)==100 and len(set(order))==100
other90=q['protectedOther90']; assert len(other90)==90
source2data=source2['identityAndPreservation']; historical97=source2data['protected97Records']
old_by={x['id']:x['canonicalSha256'] for x in historical97}
current_by={c['currentCard']['id']:c for c in cur['cards']}
# Current #20..29 cards except the selected #27 are protected. Preserve all nine exact full current preimages.
currentProtected9=[]
for i in range(20,30):
 if i==27: continue
 c=next(x for x in cur['cards'] if x['index']==i)
 assert c['currentCard']['id']==order[i]
 currentProtected9.append({'index':i,'id':c['currentCard']['id'],'canonicalSha256':c['canonicalSha256'],'whole6Sha256':c['authorWhole6Sha256'],'fullCurrentCard':c['currentCard']})
protected99=other90+[{'id':x['id'],'canonicalSha256':x['canonicalSha256'],'index':None,'preimageIncludedBy':'accepted current-other90 receipt; unchanged'} for x in currentProtected9]
# Above mistakenly includes currentProtected9 nested data, build concise typed records.
protected99=other90+[{'id':x['id'],'canonicalSha256':x['canonicalSha256']} for x in currentProtected9]
assert len(protected99)==99 and len({x['id'] for x in protected99})==99
assert set(x['id'] for x in protected99)==set(order)-{'physics-meissner-effect'}
# Verify the seven prior certified target hashes actually differ from the obsolete protected hashes where noted.
changed=[20,21,22,23,24,25,29]
historicalSuperseded=[]
for i in changed:
 c=next(x for x in cur['cards'] if x['index']==i); id=c['currentCard']['id']
 old=old_by[id]; new=c['canonicalSha256']
 assert old!=new
 historicalSuperseded.append({'index':i,'id':id,'oldPreapplyCanonicalSha256':old,'currentAcceptedCanonicalSha256':new,'currentFullCard':c['currentCard']})
selected=next(x for x in cur['cards'] if x['index']==27)
old27=next(x for x in source2['targets'] if x['index']==27)
assert selected['canonicalSha256']==old27['hashBindings']['currentCanonicalSha256']
# Full baseline order and protected manifest entries use exact UTF-8 sorted-key canonical recipe.
protectedManifest={'schema':'mindbattle-current-protected99-v1','hashRecipe':'SHA-256 of canonical JSON UTF-8 with sorted keys, literal Unicode, compact separators; full current cards for indices 20-26 and 28-29 hash exact card objects. Other90 hashes are copied unchanged from the accepted current-other90 receipt.','targetExcluded':'physics-meissner-effect','records':sorted(protected99,key=lambda x:x['id'])}
correction={'schema':'mindbattle-physics27-protected-guard-correction-v1','producerNativeThreadId':'01a137d3-c9ba-7260-be2b-42f25ee03ab6','correctionOnly':True,'corrects':{'currentNeighborAddendumPath':'physics27-current-neighbor-binding-addendum.json','currentNeighborAddendumSha256':H(open(basepath,'rb').read()),'provenanceDedupCorrectionPath':'physics27-provenance-dedup-correction.json','provenanceDedupCorrectionSha256':H(open(corrpath,'rb').read()),'source2Path':'repair-packet-26-28-source2.json','source2Sha256':H(open(b+'/repair-packet-26-28-source2.json','rb').read()),'source2PreservedByteForByte':True},'guardScope':{'selectedForCandidate':'physics-meissner-effect','currentBaselineTopicSha256':cur['topicRawSha256'],'currentRuntimeCommit':cur['runtimeCommit'],'currentReceiptPath':'physics20-29-current.json','currentReceiptSha256':H(open(b+'/physics20-29-current.json','rb').read()),'frozenCurrent100IdOrder':order,'idOrderCount':len(order),'effectiveCurrentProtectedOther99':protectedManifest,'effectiveProtectedCount':len(protectedManifest['records']),'selectedCurrentCard':{'index':27,'id':selected['currentCard']['id'],'canonicalSha256':selected['canonicalSha256'],'whole6Sha256':selected['authorWhole6Sha256'],'fullCurrentCard':selected['currentCard']},'protectedCurrentTargetCards9':currentProtected9,'unchangedOther90CurrentHashRecords':other90},'supersededHistoricalProtection':{'priorSource2Protected97Records':historical97,'sevenStaleTargetPreimages':historicalSuperseded,'interpretation':'The seven prior hashes remain preserved verbatim as historical pre-apply evidence; they are superseded for current protection and must not be used as the current guard.'},'hashPolicy':{'cardCanonicalRecipe':'SHA-256 UTF-8 canonical JSON object, sorted keys, literal Unicode, compact separators; no newline.','full100IdOrderSha256':H(canon(order).encode()),'protected99ManifestSha256':H(canon(protectedManifest).encode()),'source2HistoricalProtected97Sha256':H(canon(historical97).encode())},'status':{'candidateWordingAndGroupsUnchanged':True,'other26and28FullPreimagesProtectedFor27Scope':True,'currentCount':557,'remaining':1443,'qualityCredit':0,'humanAcceptance':'NOT_PERFORMED','qualification':'Not asserted by this guard correction.'}}
out=b+'/physics27-protected-guard-correction.json';open(out,'w').write(json.dumps(correction,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n')
print('bytes',os.path.getsize(out),'sha256',H(open(out,'rb').read()),'protected',len(protectedManifest['records']),'order',len(order),'stale',len(historicalSuperseded))
print('idOrderHash',correction['hashPolicy']['full100IdOrderSha256'],'protectedManifestHash',correction['hashPolicy']['protected99ManifestSha256'])
