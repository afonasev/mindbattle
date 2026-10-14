import json,hashlib,os,subprocess
b='/tmp/mindbattle-source-01a137d3-c9ba-7260-be2b-42f25ee03ab6/repairs-26-28'; root='/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle'
receipt_rel='docs/content-audits/question-quality-wave-7/coordinator-continuation-01a13772/current-e6-terminal-preservation/owned-tmp/physics20-29-current.json'
body_rel='docs/content-audits/question-quality-wave-7/coordinator-continuation-01a136e6/capture-only/physics-next20-29/27/assembled-original-entity.body'
receipt_path=os.path.join(root,receipt_rel); body_path=os.path.join(root,body_rel)
receipt_bytes=open(receipt_path,'rb').read(); body_bytes=open(body_path,'rb').read()
H=lambda b:hashlib.sha256(b).hexdigest(); canon=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))
receipt=json.loads(receipt_bytes); row=receipt['cards'][7]; assert row['index']==27 and row['id']=='physics-meissner-effect'
cap=row['primaryEvidence']['sourceCapture']; assert cap['bodyPath']==body_rel and cap['sha256']==H(body_bytes)
contexts=row['primaryEvidence']['typedPrimaryContextPassages']; assert len(contexts)==3
for c in contexts: assert c['path']==body_rel and body_bytes[c['startByte']:c['endByteExclusive']]==c['literalUtf8'].encode()
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()
head_body=subprocess.check_output(['git','rev-parse',f'HEAD:{body_rel}'],cwd=root,text=True).strip()
receipt_blob=subprocess.check_output(['git','rev-parse',f'HEAD:{receipt_rel}'],cwd=root,text=True).strip()
receipt_blob_251c=subprocess.check_output(['git','rev-parse',f'251c6b40f397c847e05c4c5eb59ce1b985a93488:{receipt_rel}'],cwd=root,text=True).strip()
body_blob_4467=subprocess.check_output(['git','rev-parse',f'4467eb2dc9ba1d1641a95206bf6eb15b257f206f:{body_rel}'],cwd=root,text=True).strip()
body_blob_8a=subprocess.check_output(['git','rev-parse',f'8a7522ee69dea7abd4ccbe17f4ecff95d7d599e5:{body_rel}'],cwd=root,text=True).strip()
first=subprocess.check_output(['git','log','--diff-filter=A','--format=%H','--',body_rel],cwd=root,text=True).strip().splitlines()[0]
assert head_body==cap['bodyGitBlob']==body_blob_4467==body_blob_8a=='751fa8cb78c60532d0fc2dcd4a86c89df5af0078'
assert receipt_blob==receipt_blob_251c and first=='4467eb2dc9ba1d1641a95206bf6eb15b257f206f'
basepath=b+'/physics27-provenance-dedup-correction.json'; guardpath=b+'/physics27-protected-guard-correction.json'
correction={'schema':'mindbattle-physics27-provenance-origin-correction-v1','producerNativeThreadId':'01a137d3-c9ba-7260-be2b-42f25ee03ab6','correctionOnly':True,'correctsPreviousMetadata':{'path':'physics27-provenance-dedup-correction.json','sha256':H(open(basepath,'rb').read()),'guardCorrectionPath':'physics27-protected-guard-correction.json','guardCorrectionSha256':H(open(guardpath,'rb').read()),'wordingOrGroupChanges':False},'durableCurrentReceipt':{'path':receipt_rel,'commit':'251c6b40f397c847e05c4c5eb59ce1b985a93488','filesystemBytes':len(receipt_bytes),'filesystemSha256':H(receipt_bytes),'gitBlobAt251c':receipt_blob_251c,'gitBlobAtCurrentHEAD':receipt_blob,'targetSelection':{'arrayPath':'cards[7]','index':row['index'],'id':row['id'],'canonicalSha256':row['canonicalSha256']}},'actualPrimarySourceProvenance':{'rawBodyPath':body_rel,'bodyBytes':len(body_bytes),'bodySha256':H(body_bytes),'currentHEAD':head,'bodyGitBlobAtCurrentHEAD':head_body,'firstAdditionCommitFromGitLogDiffFilterA':first,'bodyGitBlobAtFirstAdditionCommit':body_blob_4467,'captureOriginCommit':'4467eb2dc9ba1d1641a95206bf6eb15b257f206f','bodyBlobAtExistingEvidenceCommit8a7522':body_blob_8a,'existingEvidenceCommit8a7522':'8a7522ee69dea7abd4ccbe17f4ecff95d7d599e5','interpretation':'4467eb is the verified first Git addition and capture-origin commit for this source body. 8a7522 is a later evidence-tree commit that contains the same blob; it is not the original capture transaction. Current working HEAD is recorded separately.'},'contextsSelectedFromReceipt':contexts,'contextByteProofs':[{'path':c['path'],'startByte':c['startByte'],'endByteExclusive':c['endByteExclusive'],'literalUtf8Sha256':H(c['literalUtf8'].encode()),'exactRawSliceMatch':True,'bodySha256':c['bodySha256']} for c in contexts],'status':{'source27WordingUnchanged':True,'sourceGroupsUnchanged':True,'sourceQualificationApprovalNotAsserted':True,'qualityCredit':0,'count':557,'remaining':1443}}
out=b+'/physics27-provenance-origin-correction.json';open(out,'w').write(json.dumps(correction,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n')
print('bytes',os.path.getsize(out),'sha256',H(open(out,'rb').read()),'head',head,'first',first,'receiptsha',H(receipt_bytes),'bod ysha',H(body_bytes))
