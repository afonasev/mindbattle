import json,hashlib,pathlib,subprocess,os,re,pypdf
from pypdf import PdfReader
from html.parser import HTMLParser
ROOT='/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle'
assert subprocess.check_output(['git','rev-parse','--show-toplevel'],text=True).strip()==ROOT
OUT=pathlib.Path('docs/content-audits/question-quality-wave-6/independent-pilot/resume-2026-10-12-middle-current15-pilot5/turn2-current2-d30a633')
AUTHOR='docs/content-audits/question-quality-wave-6/middle-ages/resume-2026-10-12-current15-repair/turn2-remaining10/current2-correction/author-sourcebound-correction.json'
sha=lambda b:hashlib.sha256(b).hexdigest()
native=lambda x:json.dumps(x,ensure_ascii=False,separators=(',',':'),sort_keys=False).encode()
sortednative=lambda x:json.dumps(x,ensure_ascii=False,separators=(',',':'),sort_keys=True).encode()
r=json.load(open(AUTHOR));assert pathlib.Path(AUTHOR).read_bytes()==subprocess.check_output(['git','show','188514e:'+AUTHOR])
topic=pathlib.Path(r['topicPath']).read_bytes();assert topic==subprocess.check_output(['git','show','d30a633:'+r['topicPath']]);assert sha(topic)==r['topicSHA256']
cards={c['id']:c for c in json.loads(topic)['questions']};scope=r['scope'];assert scope==['middle-ages-reconquista','middle-ages-jihad']
for rec in r['records']:assert sha(native(cards[rec['questionId']]))==rec['recordSHA256']
for f in r['changedFields']:
 c=cards[f['questionId']];key=f['field'];actual=c[key] if key in ['prompt','explanation'] else c['answers'][int(re.search(r'\[(\d)\]',key)[1])]['note'];assert actual==f['literal'];assert sha(native(actual))==f['literalSHA256']
class Text(HTMLParser):
 def __init__(self):super().__init__();self.parts=[];self.skip=0
 def handle_starttag(self,tag,attrs):
  if tag in ['script','style']:self.skip+=1
 def handle_endtag(self,tag):
  if tag in ['script','style']:self.skip-=1
 def handle_data(self,d):
  if not self.skip:self.parts.append(d)
def visible(raw):
 h=Text();h.feed(raw);return ' '.join(' '.join(h.parts).split())
sources={};texts={};manifest=[]
selected={'unibas-seville-almohad.pdf':[1,2,3,4,5],'estevez-toledo-article.pdf':[1,19,20,21,22],'ucdavis-jihad.pdf':[1,6,12,13,14],'glasgow-armed-pilgrimage.pdf':[1,2,21,22,23]}
(OUT/'extractions').mkdir(exist_ok=True)
for o in r['sourceOriginals']:
 p=o['sourceRef'];name=pathlib.Path(p).name;raw=pathlib.Path(p).read_bytes();assert raw==subprocess.check_output(['git','show','188514e:'+p]);assert sha(raw)==o['rawSHA256'];assert subprocess.check_output(['git','hash-object',p],text=True).strip()==o['gitBlob']
 meta={'rawPath':p,'rawSHA256':sha(raw),'gitBlob':o['gitBlob'],'originalPageURL':o['originalPageURL'],'actualCaptureURL':o['actualCaptureURL'],'captureType':o['captureType'],'gitDurableAt':'188514e','rawBytes':len(raw),'originalPageCount':o['pageCount']}
 if name.endswith('pdf'):
  pdf=PdfReader(p);assert len(pdf.pages)==o['pageCount'];meta['pdfMetadata']={k:str(v) for k,v in (pdf.metadata or {}).items()}
  for page in selected[name]:
   txt=pdf.pages[page-1].extract_text(extraction_mode='plain');loc=f'physical page {page}';texts[(name,page)]=txt
   ep=OUT/'extractions'/f'{name[:-4]}-physical{page}.txt';ep.write_bytes(txt.encode('utf8'))
   manifest.append({'source':name,'locator':loc,'path':str(ep),'sha256':sha(ep.read_bytes()),'recipe':f'pypdf {pypdf.__version__} PdfReader(raw).pages[{page-1}].extract_text(extraction_mode=plain), UTF8 exact returned string; no newline collapse, no dehyphenation, no typography replacement','rawSHA256':sha(raw)})
  meta['readPhysicalPages']=selected[name];meta['readExtent']='Personally read relevant complete page context and neighbouring section/pages; Seville all five chapter pages read. Not claiming entire271-page thesis or every page of other works read.'
 elif name.endswith('json'):
  j=json.loads(raw);meta['header']=j['header'];meta['readExtent']='Full JSON header, actual TLFi historical entry and neighbouring analogical senses in content0; no reliance on title alone.'
  for i,e in enumerate(j['content']):
   for n,t in enumerate(e['content']):
    if isinstance(t,str):texts[(name,f'/content/{i}/content/{n} ({e["id"]})')]=visible(t)
 else:
  texts[(name,'HTML visible body')]=visible(raw.decode('utf8'));meta['readExtent']='Actual complete captured HTML page: title/introduction and addressed preamble to journal plus neighbouring opening journal entries. It is an extract from journal, not a complete journal book or standalone letter.'
 sources[name]=meta
(OUT/'extraction-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
def quote(name,loc,start,end,printed=None):
 t=texts[(name,loc)];a=t.index(start);b=t.index(end,a+len(start));q=t[a:b]
 return {**sources[name],'locator':f'{loc}; printed {printed}' if printed else str(loc),'nativeExtractionCharacterRange':[a,b],'exactExtractQuote':q,'quoteSHA256':sha(q.encode()),'quoteRecipe':'SHA256 UTF8 of exact substring of independently extracted text. PDF linebreaks and hyphenated wraps deliberately retained. HTML/JSON visible text uses HTMLParser suppress script/style then whitespace collapse. No author quote copied.','contextBefore':t[max(0,a-350):a],'contextAfter':t[b:b+650]}
Q={
 'seville-key':quote('unibas-seville-almohad.pdf',1,'Isbiliya, as capital','Thanks to the written',594),
 'seville-build':quote('unibas-seville-almohad.pdf',1,'The city\n1. New urban','The city\nUrban fortification',594),
 'seville-infra':quote('unibas-seville-almohad.pdf',4,'- In 1171 the caliph','- Palaces built',597),
 'cordoba':quote('unibas-seville-almohad.pdf',1,'3. A new Friday mosque','4. The creation',594),
 'toledo':quote('estevez-toledo-article.pdf',20,'Finalmente, en 1085','A ello',42),
 'granada':quote('fordham-columbus-1492.html','HTML visible body','Whereas, Most Christian','and in the present month'),
 'journal-label':quote('fordham-columbus-1492.html','HTML visible body','Medieval Sourcebook: Christopher Columbus','The meaning of this voyage'),
 'jihad-scope':quote('ucdavis-jihad.pdf',6,'Given the diffuse nature','6.  O',140),
 'jihad-duty':quote('ucdavis-jihad.pdf',13,'The transformation of jihad','In contrast to Kâsânî',147),
 'jihad-defense':quote('ucdavis-jihad.pdf',13,'satisfied through','There is one thing',147),
 'jihad-collective':quote('ucdavis-jihad.pdf',12,'The obligation of jihad rests','In other words',146),
 'croisade':quote('cnrtl-croisade.json','/content/0/content/0 (tlfi)','CROISADE','— P. anal.'),
 'pilgrim-title':quote('glasgow-armed-pilgrimage.pdf',2,'The Infrastructure','Submitted in fulfilment'),
 'pilgrim-definition':quote('glasgow-armed-pilgrimage.pdf',22,'For the purposes of this thesis','Of course,',14)}
proofkeys=[['seville-key'],['toledo'],['seville-build','seville-infra'],['cordoba'],['journal-label','granada'],['seville-key'],['jihad-scope','jihad-duty','jihad-defense'],['croisade'],['jihad-collective','jihad-defense'],['journal-label','granada'],['pilgrim-title','pilgrim-definition'],['jihad-scope','jihad-defense','jihad-duty']]
S=[
 'Chapter title, author and physical1/printed594 explicitly identify Isbiliya as Seville, capital of Almohads in al-Andalus; complete transformation especially1156–1199. Dates are not converted into conquest dates. One matching city.',
 'Estevez physical20/printed42 explicitly gives1085 AlfonsoVI conquest; same paragraph describes resources from governing populated former taifa. Neighbouring19/21 contextualise raids, parias and subsequent reorganisation. Exact date and consequence supported.',
 'Seville-specific numbered city/outskirts list, not just empire-wide opening generalisation, gives urban walls, Friday mosque, bazaar, bridges and aqueduct reconstruction. Physical4/printed597 directly identifies multiple bridges and aqueduct. Current plural categories describe programme, not an exact number of mosques; bridge/water supply details supported independently of generic paragraph.',
 'The chapter physically says huge Seville Friday mosque had dimensions of the one found in Córdoba. Author named on physical1 and PDFmetadata. Current attributed comparison is a direct architectural relation to the Cordoba mosque, not evidence Cordoba was capital.',
 'FIX source attribution: Granada/date/banners are explicitly supported by addressed preamble, but page identifies this as Christopher Columbus: Extracts from Journal and says document is from journal of1492. Current literal calls it Письмо. Refer to journal/preamble rather than silently classify as standalone letter.',
 'Chapter page594 explicitly supports capital and transformation interval. Explanation attributes author properly and names city corresponding to Arabic Isbiliya introduced immediately above.',
 'Syed chapter physical6/printed140 explicitly narrows analysis to Hanafi and Shafii traditions. Physical12/13 gives ordinary collective obligation, defensive invasion-triggered personal duty. Source also varies affected persons by school and proximity; prompt does not assert every person universally liable. Historical conceptual summary supported.',
 'Actual JSON /content/0/content/0 idtlfi historicalA1, not Academie9/title inference, defines medieval European Christian expedition to liberate Holy Land. Note gives that lexicographical definition without claiming every crusade targeted Holy Land; neighbouring analogical crusades are separately labelled.',
 'Syed146/147 explains duty falls from rest when some successfully perform and objectives sufficiently satisfied. Достаточное число is a functional sufficiency summary, not invented fixed numerical threshold. Additional definition of collective performance supported.',
 'FIX source attribution: same actual journal preamble supports ending war in Granada and1492 banners. It provides a concrete Reconquista end event, but current sentence again misnames journal excerpt a letter. Current question ID does not license replacing this with a different unrelated event.',
 '271-page original title page explicitly names Aoife Haberlin and Latin East thesis. Page22/printed14 Approaches defines pilgrim for purposes of this thesis as unarmed and consequently unable to defend themselves; adjacent text acknowledges crusaders can become unarmed pilgrims. Current note appropriately limits operational definition to thesis, not all historical pilgrims.',
 'Hanafi/Shafii scope explicitly in140;147 describes both Kasani fear/invasion rule and Mawardi proximity/intent/actual invasion rule with differing scope of individual liability. Current могла becoming individual is a qualified common summary, not claim allfour Sunni schools were proven.']
E=[
 'Medium city-history fact requires Almohad urban context; all4 plausible Iberian cities of appropriate historical geography. No lexical key in prompt. Precision of dates supported; no obscurity-only HOLD. Actual accepted new Seville fact assessed independently of Reconquista ID label.',
 'Own Toledo option has useful conquest/resources fact, neutral clear Russian. Neither general expedition trivia nor copied key fact.',
 'Own keyed Seville note adds concrete structures beyond capital/date asked. Rich programme useful even if note overlaps context. It concerns correct answer; receipt still says This distractor note in amended prose, minor stale metadata label recorded separately.',
 'Own Córdoba option: direct mosque-size comparison supplies architectural relationship to Cordoba mosque. Comparative facts about another city can concern both objects; not an unrelated group fact. Author attribution keeps limited comparison honest. It does not claim exact numerical dimensions.',
 'FIX: source genre is wrong despite correct own-Granada fact. Replace Письмо Колумба with вступление к журналу Колумба or equivalent accurate attribution; retain January1492/banners.',
 'Concise explanation repeats core asked fact appropriately; extra detail is supplied by keyed note. No grammar/key ambiguity.',
 'HOLD medium: Sunni-law stem lets reader dismiss Крестовый поход and Реконкиста as Christian history categories; Паломничество is sacred-site travel, not an invasion-triggered military obligation. Джихад is sole plausible Islamic warfare duty. One can choose without knowing collective→individual rule, contrary to actual medium requirement. Replace competing concepts/ask rule differently within scope; no reclassification/exclusion.',
 'Own crusade option supplies independent medieval Christian expedition fact. May be familiar, but note informative; option-set defect is assessed at prompt-key rather than hiding it in note grade.',
 'Own correct jihad note adds how collective duty is discharged, beyond asking label and invasion-triggered transformation. Additional useful fact supported, clear Russian.',
 'Own Reconquista option uses concrete conquest-end event, useful independent historical fact; attribution requires same journal correction as other card. Shared Granada fact in notes is not a duplicate core question.',
 'Own pilgrimage option gives explicitly thesis-specific operational definition and names actual scholar; Latin author name remains readable bibliographic attribution. Not false universal equation pilgrim=unarmed. Useful related traveller-protection fact.',
 'Clear qualified school-specific explanation; unlike earlier allfour claim, limits to actual two schools. Does not cure weak medium option set by itself.']
rows=[]
for ci,k in enumerate(scope):
 c=cards[k];fs=[]
 for fi,field in enumerate(['prompt-key','note0','note1','note2','note3','explanation']):
  if fi==0:literal={'prompt':c['prompt'],'answers':c['answers'],'correctIndex':c['correctIndex'],'key':c['answers'][c['correctIndex']]['text']}
  elif fi==5:literal={'explanation':c['explanation']}
  else:literal={'answer':c['answers'][fi-1]['text'],'note':c['answers'][fi-1]['note']}
  ix=ci*6+fi;sv='FIX' if ix in [4,9] else 'PASS';ev='HOLD' if ix==6 else 'FIX' if ix in [4,9] else 'PASS'
  fs.append({'field':field,'currentLiteral':literal,'nativeLiteralSHA256':sha(native(literal)),'nativeRecipe':r['fieldLiteralRecipe'],'sourceVerdict':sv,'editorialVerdict':ev,'verdict':ev if ev!='PASS' else sv,'manualSourceAnalysis':S[ix],'manualEditorialAnalysis':E[ix],'actualProofs':[dict(Q[q],manualAnalysis=S[ix]) for q in proofkeys[ix]]})
 rows.append({'id':k,'difficulty':c['difficulty'],'wholeVerdict':'FIX' if ci==0 else 'HOLD','currentRecordNativeSHA256':sha(native(c)),'currentRecordSortedRegistrySHA256':sha(sortednative(c)),'fields':fs})
# Current100: personally read narrow related neighbour questions and examine every prompt/key for related core facts.
neighbours=[]
for c in cards.values():
 if re.search('Севиль|Альмохад|джихад|Гранад|Реконкист|коллектив|обязанност|паломнич|крестов',c['prompt']+' '+c['answers'][c['correctIndex']]['text'],re.I):neighbours.append({'id':c['id'],'prompt':c['prompt'],'key':c['answers'][c['correctIndex']]['text'],'nativeSHA256':sha(native(c))})
external=[]
for p in pathlib.Path('src/content/topics').glob('*.json'):
 if p==pathlib.Path(r['topicPath']):continue
 for c in json.load(open(p))['questions']:
  if re.search('Альмохад|Севиль|суннит|коллективной|индивидуальной|джихад',c['prompt']+' '+c['answers'][c['correctIndex']]['text'],re.I):external.append({'topic':str(p),'id':c['id'],'prompt':c['prompt'],'key':c['answers'][c['correctIndex']]['text'],'nativeSHA256':sha(native(c)),'assessment':'Keyword match unrelated to Almohad capital or Sunni military-duty rule; not direct/reverse same fact.'})
spec=pathlib.Path('/Users/eaafonasev/Projects/mindbattle-planning/docs/GAME_SPEC.md').read_text().splitlines()
report={'readerIdentity':{'nativeThreadId':os.environ['CODEX_THREAD_ID'],'origin':'Actual current native CODEX_THREAD_ID; same independent reader, no new agent'},'authorIdentity':r['authorIdentity'],'runtimeFreezeCommit':'d30a633','authorReceiptFreezeCommit':'188514e','historicalWrongProofMap':'f1c652b not used for current assessment','authorReceipt':{'path':AUTHOR,'rawSHA256':sha(pathlib.Path(AUTHOR).read_bytes()),'gitBlob':subprocess.check_output(['git','hash-object',AUTHOR],text=True).strip()},'scope':scope,'topicPath':r['topicPath'],'topicRawSHA256':sha(topic),'nativeRecipe':r['nativeQuestionRecordRecipe'],'separateSortedRecipe':'UTF8 ensure_ascii=False separators comma/colon sort_keys=True; never substituted for author insertion order','sources':list(sources.values()),'extractionManifest':'extraction-manifest.json','extractionIndependence':'All selected PDF pages extracted with declared pypdf version/plain algorithm from raw originals; exact own passage slices retain linewrap/dehyphenation. Author quotes and quote-derivation companion not copied or used as read-proof. HTML and lexical entries independently extracted with actual components.','visualChecks':['Sevillephysical1 printed594, both columns read','Toledophysical20 printed42: rendered controlar is one word, raw extraction contr olar retained','Syedphysical13 printed147, both schools actual liability distinctions read'],'cards':rows,'approvedRules':{'medium':{'path':'/Users/eaafonasev/Projects/mindbattle-planning/docs/GAME_SPEC.md:139','exactQuote':spec[138]},'notes':{'path':'/Users/eaafonasev/Projects/mindbattle-planning/docs/GAME_SPEC.md:143','exactQuote':spec[142]}},'semanticNeighbourCheck':{'currentTopicCount':len(cards),'currentTopicNeighbours':neighbours,'externalNarrowMatches':external,'assessment':'No direct/reverse duplicate of Seville capital or collective-to-individual jihad rule found. Existing pilgrimage practice and Clermont crusade event ask independent facts. Shared Granada facts in option notes are acknowledged but do not make the core questions duplicates. No external partner edited.'},'metadataAnnotation':'188514e amended Seville correct-note reasoning still uses phrase This distractor note before explaining keyed city. Field belongs to correct answer; independent reading grades keyed note, not stale label. Metadata cleanup recommended; no source verdict inferred from prose.','guards':{'currentTopicBytesEqualD30a633':True,'authorReceiptBytesEqual188514e':True,'all12AuthorCurrentScalarLiteralHashesMatch':True,'all2AuthorNativeRecordsMatch':True,'all6RawSourcesByteSHAAndBlobMatch188514e':True,'quoteSlicesExact':True,'runtimeReviewhashCountersPlanningWrites':0,'sourceCountIncrement':0},'summary':{'fields':12,'source':{'PASS':10,'FIX':2,'HOLD':0},'editorial':{'PASS':9,'FIX':2,'HOLD':1},'whole':{'PASS':0,'FIX':1,'HOLD':1}},'cleanup':{'ownedBackgroundProcessesAfterFinish':0,'ownedIgnoredUntrackedAfterCommit':0,'originalsGitDurable':True,'retainedOwnProofs':'selected raw text extractions and3 inspected source page renders, needed for provenance/visual verification','foreignBenedictPreserved':True},'nextStep':'Coordinator assesses FIX/HOLD; author stopped after second compaction, so any runtime correction requires fresh authorized author. Other8 not started; same reader chat remains available. No count increment.'}
assert report['readerIdentity']['nativeThreadId']!=report['authorIdentity']
(OUT/'author-current2-native.json').write_bytes(native([cards[k] for k in scope])+b'\n')
(OUT/'reader-receipt.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(report['summary']);print([(c['id'],c['currentRecordNativeSHA256'],c['wholeVerdict']) for c in rows])
