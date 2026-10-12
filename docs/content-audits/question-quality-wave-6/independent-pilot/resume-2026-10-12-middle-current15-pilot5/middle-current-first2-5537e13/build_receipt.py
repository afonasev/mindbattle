import json,pathlib,subprocess,hashlib,os,re,pypdf
from pypdf import PdfReader
from html.parser import HTMLParser
ROOT='/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle';assert subprocess.check_output(['git','rev-parse','--show-toplevel'],text=True).strip()==ROOT
OUT=pathlib.Path('docs/content-audits/question-quality-wave-6/independent-pilot/resume-2026-10-12-middle-current15-pilot5/middle-current-first2-5537e13');FREEZE='5537e13';TOPIC='src/content/topics/middle-ages.json'
BASE='docs/content-audits/question-quality-wave-6/middle-ages/resume-2026-10-12-current-first2-fullproof/';AUTHOR=BASE+'author-current-receipt-01a12fe9.json';BIND=BASE+'source-bindings-01a12fe9.json'
sha=lambda b:hashlib.sha256(b).hexdigest()
native=lambda x:json.dumps(x,ensure_ascii=False,separators=(',',':'),sort_keys=False).encode()
canon=lambda x:json.dumps(x,ensure_ascii=False,separators=(',',':'),sort_keys=True).encode()
r=json.load(open(AUTHOR));m=json.load(open(BIND));assert r['authorThreadId']=='01a12fe9-74d9-7272-a1d2-f26317e06001'
for p in [AUTHOR,BIND]:assert pathlib.Path(p).read_bytes()==subprocess.check_output(['git','show',FREEZE+':'+p])
frozen={c['id']:c for c in json.loads(subprocess.check_output(['git','show',FREEZE+':'+TOPIC]))['questions']};working={c['id']:c for c in json.load(open(TOPIC))['questions']};head={c['id']:c for c in json.loads(subprocess.check_output(['git','show','HEAD:'+TOPIC]))['questions']};scope=['middle-ages-shrine','middle-ages-indulgence'];assert all(frozen[k]==working[k]==head[k] for k in scope)
class H(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.n=[];self.skip=0
 def handle_starttag(self,t,a):
  if t in ['script','style']:self.skip+=1
 def handle_endtag(self,t):
  if t in ['script','style']:self.skip-=1
 def handle_data(self,d):
  if not self.skip and d.strip():self.n.append(d.strip())
def text(raw):
 h=H();h.feed(raw);return ' '.join(' '.join(h.n).split())
sources={};contexts={};pdfPages={};pdfrecords=[]
for o in m['completeRawOriginals']:
 k=o['id'];p=o['path'];raw=pathlib.Path(p).read_bytes();assert raw==subprocess.check_output(['git','show',FREEZE+':'+p])==subprocess.check_output(['git','show','HEAD:'+p]);assert sha(raw)==o['rawSha256'];blob=subprocess.check_output(['git','hash-object',p],text=True).strip();assert blob==o['gitBlobSha1']
 meta={'sourceId':k,'originalURL':o['url'],'actualCaptureURL':o['url'],'captureURLMeaning':'Preserved direct requested resource URL in corrected source register; no unrecorded final redirect URL invented.','rawPath':p,'rawSHA256':sha(raw),'gitBlob':blob,'rawBytes':len(raw),'diskFrozenHEADByteEquality':True}
 if p.endswith('pdf'):
  pdf=PdfReader(p);meta.update({'actualType':'Complete original thesis PDF','physicalPages':len(pdf.pages),'readExtent':'Physical1(title) and16–18; entire relevant page17 and adjacent context, not all thesis chapters.'})
  for n in [1,16,17,18]:
   a=pdf.pages[n-1].extract_text();d=' '.join(a.split());pdfPages[(k,n)]=d;pdfrecords.append({'sourceId':k,'physicalPage1Based':n,'printedPage':n if n>1 else None,'rawExtractText':a,'rawExtractSHA256':sha(a.encode()),'derivedText':d,'derivedTextSHA256':sha(d.encode()),'recipe':f'pypdf{pypdf.__version__} PdfReader(raw).pages[n-1].extract_text(); exact " ".join(rawText.split()), UTF8 hashes. Physical numbering; offsets Unicode in derived string.'})
 elif p.endswith('json'):
  j=json.loads(raw);meta.update({'actualType':'Complete original CNRTL JSON lexical API response','header':j['header'],'readExtent':'Full header and TLFi REPENTIR2 religious definition with neighbouring extension/example senses; supplementary context, not proof of Luther words.'})
  for i,e in enumerate(j['content']):
   for n,v in enumerate(e['content']):
    if isinstance(v,str):contexts[(k,f'/content/{i}/content/{n} ({e["id"]})')]=text(v)
 else:
  v=text(raw.decode('utf8'));contexts[(k,'HTML decoded visible body')]=v
  extent={'toronto-rpo':'Full General Prologue captured body available; headnote, line17 annotation and surrounding textual notes personally read. Not all RPO corpus.','st-edmund-heritage-partnership':'Complete heritage page body, Edmund tomb/shrine paragraph and surrounding abbey narrative.','oxford-luther-edition':'Complete edition body available; theses1–3 and26–32 with corresponding notes personally read, including27/note18. Not claiming every thesis examined.','vatican-catechism':'Complete captured Indulgences1471–1479 page read with footnotes. Not entire Catechism.','fordham-benedict':'Complete captured page of extended Rule excerpts; cenobite/common-rule, abbot, obedience/humility and property/community passages read. Not complete Rule book.','bede-book1':'Complete BookI HTML body captured; I.VII opening Alban passage and subsequent persecution narrative, chapter attribution and surrounding transitions read. Not all five-book history.','bede-book4':'Complete BookIV HTML body captured; IV.XXVII Cuthbert/Farne/bishopric narrative and adjoining chapter transitions read. Not all history.'}[k]
  meta.update({'actualType':'Complete original HTML page (extended Rule excerpts, not full book)' if k=='fordham-benedict' else 'Complete original HTML page/book body','readExtent':extent,'HTMLDecodedVisibleBodySHA256':sha(v.encode()),'HTMLDecodedVisibleBodyUnicodeLength':len(v),'extractor':'HTMLParser convert_charrefs=True; ignore script/style; stripped nonempty data nodes joined with space; " ".join(split()) over derived body. Raw bytes unchanged.'})
  if k.startswith('bede'):assert b'</html>' in raw.lower() and b'</body>' in raw.lower();meta['completeRawBodyClosingTags']=True
 sources[k]=meta
(OUT/'pdf-independent-extractions.json').write_text(json.dumps(pdfrecords,ensure_ascii=False,indent=2)+'\n')
def hq(k,start,stop,loc='HTML decoded visible body'):
 d=contexts[(k,loc)];a=d.index(start);b=d.index(stop,a+len(start));q=d[a:b]
 return {**sources[k],'locator':{'context':loc,'UnicodeCodePointOffset0Based':a,'UnicodeCodePointLength':b-a},'exactDerivedQuote':q,'quoteSHA256':sha(q.encode()),'quoteRecipe':'SHA256 UTF8 exact displayed derived-body substring with independently decoded entities/whitespace collapse; not raw HTML byte slice.','contextBefore':d[max(0,a-400):a],'contextAfter':d[b:b+600]}
def pq(k,n,start,stop):
 d=pdfPages[(k,n)];a=d.index(start);b=d.index(stop,a+len(start));q=d[a:b];e=next(x for x in pdfrecords if x['sourceId']==k and x['physicalPage1Based']==n)
 return {**sources[k],'locator':{'physicalPage1Based':n,'printedPage':n,'UnicodeCodePointOffset0Based':a,'UnicodeCodePointLength':b-a},'exactDerivedQuote':q,'quoteSHA256':sha(q.encode()),'quoteRecipe':e['recipe'],'rawExtractSHA256':e['rawExtractSHA256'],'derivedPageSHA256':e['derivedTextSHA256'],'contextBefore':d[max(0,a-400):a],'contextAfter':d[b:b+600]}
Q={
 'rpo-pilgrims':hq('toronto-rpo','The Canterbury Tales are a series','A general Prologue'),
 'rpo-thomas':hq('toronto-rpo','martir: Thomas A Becket','Back to Line 18]'),
 'alban':hq('bede-book1','This Alban, being yet a pagan','The aforesaid clergyman'),
 'cuthbert':hq('bede-book4','THE same year that King Egfrid','From his very childhood'),
 'edmund':hq('st-edmund-heritage-partnership','Edmund was the King of the East Angles','One of the exciting'),
 'luther27':hq('oxford-luther-edition','27 Those who say that the soul','28 What is certain'),
 'luther1':hq('oxford-luther-edition','1 When our Lord and master','2 This word cannot'),
 'vatican':hq('vatican-catechism','1471 The doctrine','The punishments of sin'),
 'pilgrimage':pq('schmoelz-pilgrimage',17,'If pilgrimage is to be defined','The assumption therefore'),
 'benedict':hq('fordham-benedict','1. Concerning the Kinds','Then the second kind'),
 'benedict-common':hq('fordham-benedict','The eighth degree of humility','The ninth degree'),
 'repentir':hq('cnrtl-repentir','REPENTIR2','— P. ext.', '/content/0/content/0 (tlfi)')}
P=[['rpo-pilgrims','rpo-thomas'],['rpo-pilgrims','rpo-thomas'],['alban'],['rpo-thomas'],['cuthbert'],['edmund'],['luther27'],['luther27','vatican'],['luther1','repentir'],['pilgrimage'],['vatican'],['benedict','benedict-common']]
S=[
 'RPO headnote explicitly says the band of pilgrims is travelling to St Thomas’s shrine at Canterbury. Line17 annotation identifies this Thomas as Becket. Together they support one keyed saint, not an inference from the title alone.',
 'The same headnote and annotation explicitly give pilgrims, Canterbury, Thomas Becket and murdered1170. Current explanation matches these facts.',
 'BedeI.VII introduces Alban as pagan, says persecution was directed at Christians, and states that he sheltered a clergyman fleeing persecutors. Subsequent concealment/substitution narrative confirms the role. По рассказу Беды is appropriately attributed.',
 'RPO line17 annotation expressly states Archbishop of Canterbury, murdered1170, canonized1173. The new note preserves both dates, without falsely dating the literary journey to those years.',
 'BedeIV.XXVII expressly names Lindisfarne bishopric and many years of solitary life in the small island called Farne. Current note’s island/bishop/life sequence is supported by full passage, not just a clipped bishopric quote.',
 'The heritage page says Edmund’s body came to Bury and that the shrine attracted pilgrims from all over Europe. Current note accurately describes the own saint/site.',
 'Oxford thesis27 condemns the coin-to-purgatory-release promise as fiction; immediately associated note18 explicitly attributes the saying to indulgence preachers. Context is criticism of that promise, not a claim that Luther rejected every Catholic doctrine indiscriminately.',
 'Oxford27 and note18 support the criticism; Vatican1471 defines remission of temporal punishment for sins whose guilt is already forgiven. Explanation distinguishes criticized promise from doctrinal definition and preserves temporary punishment versus guilt.',
 'Oxford thesis1 explicitly says the whole life of the faithful is penance; its note explains repentance/change of life rather than isolated sacramental acts. CNRTL is only supplementary semantic context, not proof that Luther said it.',
 'Schmoelz physical/printed17 defines pilgrimage as travelling to and venerating a relic/image in an ecclesiastical building, then describes local journeys. This supports a religious journey to a venerated sacred destination; the note invents no minimum distance or international travel condition.',
 'Vatican1471 explicitly gives already-forgiven guilt, temporal punishment, and partial/plenary distinction. Current correct note preserves the distinction; it does not equate indulgence with purchasing forgiveness of guilt.',
 'The complete captured Benedict page is explicitly extended excerpts. Its cenobite definition places monks under a rule/abbot, and humility section says the common rule governs action. This supports shared rules for communal monastic life without claiming the capture is the entire Rule book.']
E=[
 'Easy accepted under actual138: pilgrimage to Becket is the central journey/frame of this canonical work, a familiar association within the large English-language literary/educational culture. It is not a minor character/date detail. Source confirmation alone is not the difficulty argument. Four real English saints and shrines are plausible parallel options; one key, no lexical answer cue.',
 'Clear Russian, direct explanation of the literary journey. Extra death date is verified; main explanation may overlap the notes.',
 'Own Alban option: attributed sheltering of a persecuted priest is a useful independent biographical fact, not generic pilgrimage trivia.',
 'Own correct Becket option: archbishopric, murder1170 and especially canonization1173 add information beyond current shrine destination prompt/key. Overlap of1170 with explanation is allowed.',
 'Own Cuthbert option: Farne eremitic life and subsequent Lindisfarne bishopric provide useful independent saint-specific facts.',
 'Own Edmund option: Bury shrine’s Europe-wide pilgrimage reach is useful information about that saint/site.',
 'FIX meaningful duplicate, not difficulty HOLD: current question tests Luther→criticized indulgences. history-germany-easy-02a-01 supplies indulgence criticism and asks for Luther, reversing the same association. The coin/purgatory description adds context but one can answer current question from that association alone. Easy is otherwise credible as a central Reformation theme; no reclassification or automatic book ban.',
 'Clear explanation with accurately separated thesis criticism and Catechism definition. It does not remove the core association duplicate.',
 'Own penance option: Luther’s thesis1 supplies a precise useful statement about this option, rather than an unsupported claim about indulgence revenue.',
 'Own pilgrimage option: definition concerns its religious journey purpose, a useful standalone fact. It is broad but materially informative and source-supported.',
 'Own correct indulgence option: doctrine of already-forgiven guilt/temporal punishment and full-versus-partial adds useful facts beyond coin-promise criticism. It may overlap explanation under approved143.',
 'Own monastic-rule option: communal rule function is independently useful and supported by cenobite/common-rule context. It is not a claim that every monastery used Benedict’s text.']
rows=[]
for ci,k in enumerate(scope):
 c=frozen[k];ar=next(x for x in r['cards'] if x['id']==k);fs=[]
 for fi,g in enumerate(['prompt-key','explanation','note0','note1','note2','note3']):
  lit={'prompt':c['prompt'],'answerTexts':[a['text'] for a in c['answers']],'correctIndex':c['correctIndex']} if fi==0 else c['explanation'] if fi==1 else c['answers'][fi-2]['note'];ag=next(x for x in ar['groups'] if x['name']==g);assert lit==ag['literal'];b=canon(lit) if fi==0 else lit.encode();assert sha(b)==ag['sha256'];ix=ci*6+fi;ev='FIX' if ix==6 else 'PASS'
  fs.append({'field':g,'currentLiteral':lit,'keyedAnswer':c['answers'][c['correctIndex']]['text'] if fi==0 else None,'authorNativeLiteralSHA256':sha(b),'authorRecipe':r['literalHashRecipe']['prompt-key' if fi==0 else 'scalar'],'readerInsertionJSONSHA256':sha(native(lit)),'readerRecipe':'UTF8 JSON ensure_ascii=False,separators comma/colon,sort_keys=False, no newline; scalar JSONquotes retained separately from author scalar UTF8 recipe.','sourceVerdict':'PASS','editorialVerdict':ev,'verdict':ev,'manualSourceReason':S[ix],'manualEditorialReason':E[ix],'actualProofs':[dict(Q[q],manualEntailment=S[ix]) for q in P[ix]]})
 rows.append({'id':k,'difficulty':c['difficulty'],'wholeSourceVerdict':'PASS','wholeEditorialVerdict':'PASS' if ci==0 else 'FIX','wholeVerdict':'PASS' if ci==0 else 'FIX','canonicalCardSHA256':sha(canon(c)),'insertionCardSHA256':sha(native(c)),'fields':fs})
partners=[];rx=re.compile(r'\bЛютер\w*|\bиндульген\w*|\bБекет\w*|\bЧосер\w*|Кентерберийск\w* рассказ',re.I)
for p in pathlib.Path('src/content/topics').glob('*.json'):
 for q in json.load(open(p))['questions']:
  if rx.search(q['prompt']+' '+q['answers'][q['correctIndex']]['text']):partners.append({'topic':str(p),'id':q['id'],'prompt':q['prompt'],'answerTexts':[a['text'] for a in q['answers']],'correctIndex':q['correctIndex'],'key':q['answers'][q['correctIndex']]['text'],'canonicalSHA256':sha(canon(q))})
dup=next(x for x in partners if x['id']=='history-germany-easy-02a-01')
spec=pathlib.Path('/Users/eaafonasev/Projects/mindbattle-planning/docs/GAME_SPEC.md').read_text().splitlines();a=spec[143].index('Прямой и обратный');b=spec[143].index('Если полезно',a);duplicateRule=spec[143][a:b].strip()
trusted='01a12f3d-8ec1-78b3-b153-5f2a62967421';env=os.environ['CODEX_THREAD_ID']
report={'readerIdentity':{'trustedNativeThreadId':trusted,'trustedIdentityOrigin':'Direct native coordinator dispatch for existing actual independent reader','environmentThreadId':env,'identityDiscrepancy':None if env==trusted else 'Environment id differs from trusted actual reader handle; neither coordinator nor inherited env id stamped as reader identity.'},'authorIdentity':{'trustedNativeThreadId':r['authorThreadId'],'source':'Corrected suffix01a12fe9 packet and direct native dispatch','environmentThreadIdReportedByAuthor':r['environmentThreadId'],'identityDiscrepancyReportedByAuthor':r['identityDiscrepancy']},'runtimeFreeze':FREEZE,'scope':scope,'authorPacket':{'receipt':AUTHOR,'receiptRawSHA256':sha(pathlib.Path(AUTHOR).read_bytes()),'bindings':BIND,'bindingsRawSHA256':sha(pathlib.Path(BIND).read_bytes()),'wrongNoSuffixHistoricalReceiptUsed':False},'cards':rows,'completeRawOriginals':list(sources.values()),'pdfExtractFile':'pdf-independent-extractions.json','renderedSourcePage':{'path':str(OUT/'rendered/schmoelz-physical17.png'),'SHA256':sha((OUT/'rendered/schmoelz-physical17.png').read_bytes()),'visuallyRead':True},'approvedRules':{'easy':{'path':'/Users/eaafonasev/Projects/mindbattle-planning/docs/GAME_SPEC.md:138','exactQuote':spec[137]},'ownNotes':{'path':'/Users/eaafonasev/Projects/mindbattle-planning/docs/GAME_SPEC.md:143','exactQuote':spec[142]},'duplicates':{'path':'/Users/eaafonasev/Projects/mindbattle-planning/docs/GAME_SPEC.md:144','exactQuote':duplicateRule}},'semanticDuplicateCheck':{'currentCount':len(working),'partners':partners,'actualDuplicatePartner':dup,'concreteDefect':'Luther criticizes indulgences: current asks criticized practice given Luther, Germany asks Luther given indulgence criticism. Coin context does not prevent association-only answering. A core independent fact is needed; external partner not edited.','nonDuplicates':'Literature asks Chaucer authorship rather than pilgrimage destination; worldhistory asks century and faith doctrine; MLK is unrelated. Shrine main fact is independent of general pilgrimage-practice definition.'},'guards':{'all12CurrentNativeAuthorLiteralHashesMatch':True,'current2DiskFrozenHEADCanonicalRecordsMatch':True,'all9OriginalsDiskFrozenHEADRawSHABlobMatch':True,'BedeCompleteRawBodyClosingTags':True,'independentDerivedHTMLPDFQuoteOffsetsExact':True,'noExpectedQuoteHashSubstituted':True,'originalBytesNotTrimmed':True,'runtimeSourceAuthorPlanningReviewhashCountersWrites':0,'counterIncrement':0},'summary':{'fields':12,'source':{'PASS':12,'FIX':0,'HOLD':0},'editorial':{'PASS':11,'FIX':1,'HOLD':0},'whole':{'PASS':1,'FIX':1,'HOLD':0}},'checks':'JSONsyntax,current12literal/nativecard/sourceSHA/blob/quoteoffset integrity, independent original contexts, source page render, semantic literal partners, owned Git whitespace/scope. No tests/full/npmQA/build/Player/browsergame/deploy/release/acceptance.','cleanup':{'ownProcesses':0,'ownedIgnoredUntrackedAfterCommit':0,'sourceOriginalsGitDurable':True,'retainedOwnedEvidence':'independent page extraction, source-context quotes and one inspected source render','foreignBenedictAndSharedIndexPreserved':True},'nextStep':'Coordinator adjudicates Indulgence direct/reverse duplicate and chooses authorized independent main fact/rework. No external partner edit or count mutation by reader. Stop receipt+cleanup.'}
assert trusted!=r['authorThreadId'];assert len(sources)==9
(OUT/'reader-receipt.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');(OUT/'current2-canonical.json').write_bytes(canon([frozen[k] for k in scope])+b'\n');(OUT/'current2-insertion.json').write_bytes(native([frozen[k] for k in scope])+b'\n')
print(report['summary']);print([(c['id'],c['canonicalCardSHA256'],c['wholeVerdict']) for c in rows]);print('Trusted reader',trusted,'Env',env,'Author',r['authorThreadId'])
