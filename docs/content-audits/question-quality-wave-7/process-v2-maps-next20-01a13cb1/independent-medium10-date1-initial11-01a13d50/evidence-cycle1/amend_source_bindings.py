import pathlib,json,hashlib,copy,subprocess
R=pathlib.Path.cwd();O=R/'docs/content-audits/question-quality-wave-7/process-v2-maps-next20-01a13cb1/independent-medium10-date1-initial11-01a13d50';E=O/'evidence-cycle1'
def rd(p):return json.loads(p.read_text())
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
original=O/'receipt-cycle1-current9.json';originalSHA=digest(original);assert originalSHA=='ba6a74ec3a5def39a08ffa333d3e0763759a2c75cb59b34946000b8d399094fa';old=rd(original);new=copy.deepcopy(old);corrections={};references=[]
for e in new['entries']:
 for g in e['sixLiteralGroups']:
  p=pathlib.Path(g['fullContextPath']);actual=digest(p);expected=g['fullContextSHA256']
  if expected!=actual:
   raw=p.read_bytes();normalized=raw.decode('utf-8').replace('\r\n','\n').replace('\r','\n');normalSHA=hashlib.sha256(normalized.encode('utf-8')).hexdigest();assert normalSHA==expected
   # This verifies the exact representation used by prior read_text() source reads.
   assert normalized==p.read_text();assert len(raw.decode().splitlines())==len(normalized.splitlines())
   corrections[str(p)]={'path':str(p),'previousFullContextSHA256':expected,'correctFullContextByteSHA256':actual,'previousHashExactlyMatches':'SHA256 of UTF8 decoded content after universal-newline CRLF/CR to LF normalization','normalizedReadSHA256':normalSHA,'rawCRLFCount':raw.count(b'\r\n'),'rawCRCount':raw.count(b'\r'),'decodedSemanticContentUnchanged':True,'splitlinesLocatorLineCountUnchanged':True,'sameExactFileAsPersonallyRead':True,'alternateEvidenceCycle1ExtractionExists':(E/p.name).exists(),'gitHEADFileByteSHA256':hashlib.sha256(subprocess.check_output(['git','show','HEAD:'+str(p.relative_to(R))])).hexdigest()}
   assert corrections[str(p)]['gitHEADFileByteSHA256']==actual
   references.append({'id':e['id'],'group':g['group'],'path':str(p),'oldSHA256':expected,'newSHA256':actual});g['fullContextSHA256']=actual
   g['fullContextHashContract']='SHA256 of read_bytes(), exact saved file bytes, with CRLF preserved'
assert len(corrections)==3
# Bind inventory to the exact 6-group fields, not to a broader inherited source index.
bound={}
for e in new['entries']:
 for g in e['sixLiteralGroups']:
  records=[(g['fullContextPath'],g['fullContextSHA256'],'fullContext')]+[(x['path'],x['sha256'],'rawPrimary') for x in g['rawPrimaryFiles']]
  for p,h,role in records:
   k=(p,h)
   if k not in bound:bound[k]={'path':p,'expectedByteSHA256':h,'actualByteSHA256':digest(pathlib.Path(p)),'roles':[],'referencedBy':[]}
   if role not in bound[k]['roles']:bound[k]['roles'].append(role)
   bound[k]['referencedBy'].append({'id':e['id'],'group':g['group']})
for x in bound.values():x['matches']=x['expectedByteSHA256']==x['actualByteSHA256'];assert x['matches'],x
assert len(bound)==34
previous=rd(E/'source-verification.json')['sources'];previousPaths={x['path'] for x in previous};boundPaths={p for p,h in bound};supplemental=[];previousVerified=[]
for x in previous:
 p=pathlib.Path(x['path']);v={'path':str(p),'previousExpectedByteSHA256':x['expected'],'actualByteSHA256':digest(p),'inReceiptBindingInventory':str(p) in boundPaths};v['matches']=v['previousExpectedByteSHA256']==v['actualByteSHA256'];assert v['matches'];previousVerified.append(v)
 if not v['inReceiptBindingInventory']:supplemental.append(v)
assert len(previousVerified)==41 and len(supplemental)==8
missing=sorted(boundPaths-previousPaths);assert len(missing)==1 and missing[0].endswith('primary-10.txt')
unionPaths=boundPaths|previousPaths;assert len(unionPaths)==42
proof={'stage':'byte-source-binding amendment only','originalReceipt':str(original),'originalReceiptSHA256':originalSHA,'cause':'The previous primary-read-index hashed read_text().encode(), i.e. universal-newline-normalized text, but used fullContextSHA256 next to a saved file path. Three mixed-LF/CRLF files therefore had a text-representation digest where a byte-file digest was required. There is no alternate extraction under evidence-cycle1. The actual files were personally read at these same initial evidence paths; current raw bytes equal git HEAD.','corrections':list(corrections.values()),'changedGroupReferences':references,'changedGroupReferenceCount':len(references),'locators':'Unchanged: decoding CRLF and splitting lines gives identical content and numbering; relevant passages were personally reread while diagnosing. Prior independent precise locators remain valid.','allSixGroupUniquePathHashPairs':list(bound.values()),'receiptBindingPairCount':34,'receiptBindingMismatches':0,'previous41CheckReconciliation':{'previousCheckedFiles':previousVerified,'previousCheckedCount':41,'overlapWith34ReceiptBindings':33,'supplementalFilesOutsideReceiptBindings':supplemental,'supplementalCount':8,'receiptBindingOmittedPreviously':missing,'uniqueUnionCount':42,'formulaDiagramIsSupplemental':any(x['path'].endswith('noaa-heights.gif') for x in supplemental)},'semanticChanges':False,'currentCardHashesChanged':False,'verdictsChanged':False,'originalReceiptUnchanged':True,'initialEvidenceUnchanged':True,'latitude':'Remains terminal HOLD on the exact unmodified card. Concrete mechanical correction pending: «На южном полушарии» → «В Южном полушарии»; no new product authorization or substantive fix cycle requested.'}
dump(E/'source-binding-correction-record.json',proof)
# Correct a copy of the context index too, leaving its original source file untouched.
idx=rd(E/'primary-read-index.json')
for s in idx['completeContexts']:
 p=R/s['independentReadContext'];s['contextSHA256']=digest(p);s['contextHashContract']='SHA256 exact bytes; read_bytes, no newline normalization'
idx['sourceBindingCorrectionRecord']=str(E/'source-binding-correction-record.json');dump(E/'primary-read-index-source-binding-amended.json',idx)
new['sourceBindingCorrection']={'recordPath':str(E/'source-binding-correction-record.json'),'originalReceiptPath':str(original),'originalReceiptSHA256':originalSHA,'changedFiles':3,'changedGroupReferences':len(references),'cause':'Universal-newline normalized text SHA was mislabeled as saved-file byte SHA. Corrected to actual personally-read file bytes; no path/text/card/verdict changes.','allReceiptSourceBindingPairsVerified':34,'allReceiptSourceBindingMismatches':0,'previous41Reconciled':'33 shared receipt files +8 supplementary files; primary-10.txt was missing from old41. New union42 files, all byte hashes verified.','locatorsUnchanged':True,'sourceReadIndexAmendedPath':str(E/'primary-read-index-source-binding-amended.json')}
new['checks']['sourceHashPairs']=34;new['checks']['sourceHashPairScope']='Unique path+byte-SHA pairs used by 54 sixLiteralGroups fullContextPath/fullContextSHA256 and rawPrimaryFiles; exhaustive34'
new['checks']['sourceHashMismatches']=0;new['checks']['supplementalSourceFilesVerified']=8;new['checks']['allSourceFileUnionVerified']=42;new['checks']['previous41CountReconciled']=True
new['next']='Coordinator qualifies this exact amended receipt, adjudicates PASS7/HOLD2 and preserves output in Git. Latitude stays HOLD until the authorized exact mechanical grammar correction «На южном полушарии» → «В Южном полушарии» is applied and separately hash-bound. Elevation remains terminal HOLD for the stated medium/overlap defects; no automatic further substantive cycle or new product-policy request.'
new['sourceAndPeerLimits']+=' Source-binding-only amendment: exact byte hashes now used for three existing full contexts; original normalized-read representation explained in correction record; no alternate file was substituted.'
newfile=O/'receipt-cycle1-current9-source-binding-amended.json';dump(newfile,new)
assert digest(original)==originalSHA
print(json.dumps({'amendedReceipt':str(newfile),'amendedSHA256':digest(newfile),'originalUnchangedSHA256':digest(original),'correctionFiles':3,'changedReferences':len(references),'bindingPairs':34,'old41Overlap':33,'supplemental':8,'previousMissing':missing,'unionFiles':42,'counts':new['counts']},ensure_ascii=False,indent=2))
