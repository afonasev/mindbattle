import json, hashlib, subprocess, os, re
from pathlib import Path
import html
class BeautifulSoup:
 def __init__(self,s,parser):self.s=s.decode('utf-8',errors='replace') if isinstance(s,bytes) else s
 def __call__(self,tags):return []
 def get_text(self,sep=' ',strip=True):
  s=re.sub(r'<(script|style)\b[^>]*>.*?</\1>', '', self.s, flags=re.S|re.I)
  return html.unescape(re.sub('<[^>]+>',sep,s))
from pypdf import PdfReader
ROOT=Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle')
OWN=ROOT/'docs/content-audits/question-quality-wave-6/independent-pilot/resume-2026-10-12-architecture16-fresh-current'
AUTHOR=ROOT/'docs/content-audits/question-quality-wave-6/architecture/resume-2026-10-12-fresh-rework16'
OLD=ROOT/'docs/content-audits/question-quality-wave-6/independent-pilot/resume-2026-10-12-architecture16-current'
def guard():
 assert Path.cwd()==ROOT
 assert subprocess.check_output(['git','rev-parse','--show-toplevel'],cwd=ROOT,text=True).strip()==str(ROOT)
def write(p,b):
 guard();assert p.is_relative_to(OWN);p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
def dump(p,x):write(p,(json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode())
def sha(x):return hashlib.sha256(x).hexdigest()
def canonical(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def plain(x):return re.sub(r'\s+',' ',BeautifulSoup(x,'html.parser').get_text(' ',strip=True)).strip()
reader=os.environ['CODEX_THREAD_ID'];assert reader=='01a12eb9-b319-7d72-8748-170744fe01eb'
source=ROOT/'src/content/topics/architecture.json'; frozen=source.read_bytes();qs={x['id']:x for x in json.loads(frozen)['questions']}
a=json.loads((AUTHOR/'author-review.json').read_bytes()); rules=json.loads((OLD/'approved-rules.json').read_bytes())['rules']
# The following 96 analyses are individually authored judgments after reading current literals and original source sections.
analyses={
'skyscraper-definition':[
('Leade carries water from gutter to ground; only pipe names that downstream channel. Cornice crowns, gutter collects, flashing seals. Familiar household drainage fits easy; all four noun phrases fit the stem.', 'PASS','PASS'),
('First sentence matches Leade. Second makes metal categorical although the original says usually made of metal. Two useful Russian sentences, but preserve the material qualifier.', 'FIX','PASS'),
('Cornice explicitly projects and tops its attached element; wall/building paraphrase is faithful. Own variant fact, concise and grammatical.', 'PASS','PASS'),
('Gutter entry specifies a channel below and along eaves catching rainwater. Its collection function is an independent useful fact for the gutter option.', 'PASS','PASS'),
('Flashing definition gives sheet-metal strips fitted between roof and projections such as chimney; wall junction is the same construction relation. Own variant function is useful.', 'PASS','PASS'),
('Leade explicitly allows horizontal or vertical cylinders, an additional orientation fact beyond the stem. However usually metal was changed into unqualified metal in the claimed glossary definition.', 'FIX','PASS')],
'alhambra':[
('Awning is fabric on a metal frame over openings/storefront. Grille is openwork, cornice molding, parapet wall: none is the fabric canopy. Easy household feature; four comparable building parts with no grammatical key cue.', 'PASS','PASS'),
('Awning entry includes both window/door and storefront, supporting both sentences. Storefront placement adds a concrete use; two sentences meet the format.', 'PASS','PASS'),
('Retractable Awning explicitly folds or rolls against facade. This subtype behavior adds a fact beyond naming the cloth canopy.', 'PASS','PASS'),
('Grille is protective openwork grating, usually iron, for window or door. May be metal is restrained; own variant protection fact.', 'PASS','PASS'),
('Cornice projects and tops its attached element. This is a useful definition of the distractor, with no requirement to explain wrongness.', 'PASS','PASS'),
('Parapet is low wall at roof/terrace edge. Both height and location are present; own option fact.', 'PASS','PASS')],
'mont-saint-michel':[
('Facade entry supports the literal and unique key within these four choices; easy class is appropriate. However protected architecture-burj-khalifa-city asks the same exterior-face definition with key Фасад. Adding главная does not create a new tested fact.', 'PASS','FIX'),
('Facade entry explicitly distinguishes elaborate architecture/ornament from other faces; both sentences supported and Russian agreement acceptable. Decoration adds useful explanation.', 'PASS','PASS'),
('Source says sometimes distinguished by ornamental detail. Note retains иногда and adds decoration beyond the exterior-face stem, so it is not a bare key repetition.', 'PASS','PASS'),
('Cornice entry supports projecting crowning molding; wall/other element remains faithful. Own useful distractor fact.', 'PASS','PASS'),
('Parapet entry supports low barrier at roof/terrace edge. Protective wording follows barrier; own fact.', 'PASS','PASS'),
('Awning entry supports fabric frame above windows/doors. Accurate independent distractor definition.', 'PASS','PASS')],
'machu-picchu':[
('Landings section identifies level landings between runs. Only Площадка names horizontal area; sloping run, rail, edge are distinct ramp components. Familiar horizontal/inclined reasoning fits approved easy logic.', 'PASS','PASS'),
('Landings required at top/bottom of each run and intermediate where direction changes support both sentences. Two sentences explain placement without importing a numerical limit.', 'PASS','PASS'),
('Rise section states 30-inch maximum run rise. Height denotes vertical rise here, not ramp length; explicitly scoped ADA numeric fact belongs to this run option.', 'PASS','PASS'),
('Handrails section states both sides for rise greater than 6 inches. Correct threshold and strict greater-than; coherent ADA context of adjacent notes, useful rail fact.', 'PASS','PASS'),
('Landings section requires clear 60 by 60 where direction changes. Size adds genuinely new content beyond horizontal platform definition; no conversion errors.', 'PASS','PASS'),
('Edge Protection explicitly lists casters/crutch tips and curbs/barriers/extended surfaces. Both function and alternatives are supported; useful own-edge information.', 'PASS','PASS')],
'parthenon-city':[
('Colonnade entry expressly contrasts horizontal members with arches. Only colonnade is row of columns; arcade is nearest plausible alternative, architrave/column are parts. Easy familiar whole-versus-part distinction, no key leak.', 'PASS','PASS'),
('Colonnade and Architrave entries support horizontal row and classical beam name. Two sentences; no unsupported historical example.', 'PASS','PASS'),
('The source names horizontal members architrave. Naming those beams adds terminology absent from stem, despite repeating row of columns; accepted useful addition.', 'PASS','PASS'),
('Arcade source says series of arches on columns or piers. Both structure and supports supported, own option fact.', 'PASS','PASS'),
('Architrave source explicitly combines spans between columns and lowest member of entablature. Both assertions supported, useful own option detail.', 'PASS','PASS'),
('Column source cylindrical support and LPC vertical cylindrical support jointly support the orientation. Обычно accommodates decorative examples; useful definition.', 'PASS','PASS')],
'colosseum-city':[
('Mausoleum source says freestanding structure for tomb; crypt underground, brass plate commemorative, catacombs subterranean burial. Key unique; all funeral forms plausible, independent grammatical noun phrases, easy familiar type distinction.', 'PASS','PASS'),
('Definition plus photo caption Mausoleum of Theodoric Ravenna Italy support two sentences. The example is an additional fact, no unsupported above-ground claim.', 'PASS','PASS'),
('Full catacomb entry states burial use and Christian services under Roman persecution. Both claims explicitly supported; own variant information.', 'PASS','PASS'),
('Theodoric/Ravenna photo caption supports the specific example. Adds a named instance beyond defining a mausoleum, even though explanation also uses it.', 'PASS','PASS'),
('Memorial brass full entry engraved metal plate, usually flush church pavement to mark tomb. Could be installed retains possibility and location, useful own option.', 'PASS','PASS'),
('Crypt entry underground chamber for relics or tombs supports both functions. Useful independent definition of this distractor.', 'PASS','PASS')],
'hagia-sophia-original-purpose':[
('UNESCO synthesis links dome expertise to sixth century and criterion i dates design 532-537 in Byzantine context. V versus VI offers meaningful neighboring period; Ottoman/XIX remain historical alternatives, medium knowledge required.', 'PASS','PASS'),
('UNESCO explicitly pairs architectural and decorative expertise of sixth century, supporting both sentences. Two sentences, second retains separate decorative aspect without invented purpose.', 'PASS','PASS'),
('Synthesis says peninsula walls built initially by Theodosius early fifth century. Concrete same-period example belongs to early Byzantine option; own useful fact.', 'PASS','PASS'),
('Synthesis explicitly names Suleymaniye, chief architect Sinan and Ottoman peak in sixteenth century. Own option period/example, all claims supported.', 'PASS','PASS'),
('Synthesis says Topkapi continually extended until nineteenth century. Example of nineteenth-century extensions belongs to this option, not an assertion about Sophia.', 'PASS','PASS'),
('Full criterion i dates Sophia design 532-537; synthesis identifies sixth-century dome expertise in Byzantine skyline. Building date adds a construction fact beyond period attribution; accepted even with related subject.', 'PASS','PASS')],
'entasis-effect':[
('Archivolt is bands/moldings around arched opening. Keystone at apex, voussoir wedge, tympanum enclosed field are plausible adjacent parts, hard specialist terminology permits narrowing by shape/location; no arbitrary geography cue.', 'PASS','PASS'),
('Archivolt definition and full arch entry wedge-shaped elements/parts voussoir jointly support framing versus constructing arch. Two explanatory sentences, both claims sourced.', 'PASS','PASS'),
('Keystone entry states top voussoir and rib-vault intersections. Both locations supported, useful own variant detail.', 'PASS','PASS'),
('Arch definition plus list parts voussoir identifies wedge elements. Own variant construction fact, no unrelated comparison necessary.', 'PASS','PASS'),
('Tympanum entry basically semicircular enclosed by arch above lintel supports note. Source qualifies basically; ordinary generic semicircle description acceptable for this glossary type.', 'PASS','PASS'),
('Archivolt and arch full entries together support framing and wedge voussoirs. The latter adds a constructive contrast beyond stem; must bind both sources, not only archivolt as author did.', 'PASS','PASS')],
'cantilever-support':[
('UNESCO identifies cantilever arms from towers and suspended spans between them. Arch span/suspended span/pylon cannot name lateral arms in this stem. Medium bridge vocabulary and close structural choices provide meaningful distinction.', 'PASS','PASS'),
('Full synthesis sentence explicitly states 207 m arms and 107 m suspended spans. Both quantities supported despite author quote omitting second; two clear sentences.', 'PASS','PASS'),
('Arch full entry turns vertical pressure into lateral pressure through wedge elements. Lateral-support paraphrase gives own arch-span mechanism, not a Forth arch claim.', 'PASS','PASS'),
('Synthesis explicitly says each arm projects 207 m. Number adds information absent from prompt, useful correct-note addition.', 'PASS','PASS'),
('Synthesis says each of two suspended spans 107 m long. Own option length, not obsolete cable claim; exactly supported.', 'PASS','PASS'),
('Full synthesis states three double-cantilever towers with arms to each side; source supports number/function. Note describes these tower-like supports in Forth context; belongs to pylon option.', 'PASS','PASS')],
'empire-state-city':[
('Gutter below/along eaves catches rainwater, Leade carries it to ground, flashing joins surfaces, cornice crowns. Only gutter collects along roof edge; easy household fact with plausible neighboring pieces.', 'PASS','PASS'),
('Gutter and Leade entries support collection then conveyance to ground. Two sentences, no unsupported intermediary hopper/funnel.', 'PASS','PASS'),
('Function matches Leade, but metallic channel is categorical while source says usually made of metal. Preserve qualifier or omit material; useful own pipe fact editorially.', 'FIX','PASS'),
('Cornice entry says projecting molding especially roof/crowning entablature. Finishing wall/roof member paraphrase remains within stated role, own fact.', 'PASS','PASS'),
('Flashing entry explicitly sheet-metal strips fitted roof/projection angle e.g. chimney. Both material and example supported; own variant fact.', 'PASS','PASS'),
('Gutter entry explicitly shallow metal-or-wood channel along eaves. Depth/material add new information beyond prompt collecting function; accepted correct-note addition.', 'PASS','PASS')],
'statue-liberty-city':[
('Restoration entry returns original form/condition; rehabilitation permit repair, window repair prior deterioration, repointing mortar. Specific original appearance makes restoration sole intended term. Easy known practice; related alternatives plausible.', 'PASS','PASS'),
('Restoration entry supports achievable original form/condition for building or parts. Second sentence clarifies scope; two sentences satisfy format.', 'PASS','PASS'),
('Building or parts and as nearly as possible add scope/limit absent from prompt. Source exact definition supports both; not only key repetition.', 'PASS','PASS'),
('Rehabilitation entry defines permit-requiring repair. Note explicitly limits to LPC, avoiding a global legal claim, own useful definition.', 'PASS','PASS'),
('Repair full entry specifically windows, damage/decay and prior condition supports all note claims. Scope is correctly window, own fact.', 'PASS','PASS'),
('Repointing renews mortar joints; masonry wording follows pointing cross-reference. Accurate own-operation fact.', 'PASS','PASS')],
'fez':[
('Arcade and blind arcade definitions distinguish supported open sequence from decorative arches applied to wall. Open excludes blind; colonnade horizontal, architrave beam. Medium adjacent terminology, one key and compatible noun phrases.', 'PASS','PASS'),
('Arcade definition plus blind arcade wall definition supports both sentences. Contrast explains key; two sentences, no format defect.', 'PASS','PASS'),
('Blind arcade definition row decorative arches applied to wall exactly supports own variant note.', 'PASS','PASS'),
('Colonnade entry horizontal members rather than arches directly supports note, own useful distinction.', 'PASS','PASS'),
('Architrave definition flat member spans columns supports beam fact; own useful distractor note.', 'PASS','PASS'),
('Arcade and blind arcade entries jointly explain distinction from wall-applied decorative row. Although open is in stem, contrast to blind subtype adds a relationship; accepted, bind both originals.', 'PASS','PASS')],
'cartagena':[
('UNESCO states channels/passes as natural defenses, but same defense paragraph also names San Felipe rocky crag east of city protecting isthmus access. Broad stem asks geographic features in defense description and therefore also fits option0. Actual class is one-answer ambiguity, not difficulty; medium unchanged.', 'PASS','FIX'),
('Synthesis explicitly taking advantage of natural defenses and all passes eventually dominated by fortresses supports both sentences. Two sentences; factual explanation does not repair broad stem.', 'PASS','PASS'),
('Synthesis places San Felipe on rocky crag dominating city east. All location claims supported, belongs to this rocky-ridge distractor.', 'PASS','PASS'),
('Full synthesis narrow walled-city streets civil/religious/residential monuments supports all three types. Own street-option fact.', 'PASS','PASS'),
('UNESCO essential link route of West Indies supports important-link paraphrase. Own trade-position fact.', 'PASS','PASS'),
('Synthesis explicitly all natural harbor passes dominated by fortresses. Adds later defensive control beyond naming geographic channels/passes.', 'PASS','PASS')],
'durham':[
('Durham description explicitly innovative vaulting foreshadowed Gothic. Aachen Carolingian octagon, Chartres French Gothic, Cologne High Gothic are plausible comparison monuments but do not share this pre-Gothic Norman claim in originals. Hard architectural chronology supports narrowing.', 'PASS','PASS'),
('Full Durham description expressly says Norman finest/largest and innovative vaults foreshadow Gothic. Both sentences supported; no unsupported early-ribbed assertion.', 'PASS','PASS'),
('Aachen description octagonal basilica and cupola, synthesis octagonal plan roofed dome, support palatine chapel note. Own actual Aachen variant, not old Peterborough.', 'PASS','PASS'),
('Chartres description marks high point French Gothic art; one of highest examples faithful. Own cathedral fact.', 'PASS','PASS'),
('Durham full description built to house Cuthbert and Venerable Bede relics. Both identities/function supported, new purpose beyond vault innovation.', 'PASS','PASS'),
('Cologne description explicitly begun1248, not complete until1880. Both dates supported for actual Cologne option, no old Norwich substitution.', 'PASS','PASS')],
'samarkand':[
('UNESCO says Registan mosque/madrasahs originally mud brick covered decorated ceramic tiles. Four real construction materials give hard specific masonry distinction; original-under-cover reading supported without asserting modern reconstruction.', 'PASS','PASS'),
('Source supports original mud brick and tile cover; distinguishing veneer from underlying structure is direct material-layer inference. Two sentences, no new invented material.', 'PASS','PASS'),
('Taj source synthesis explicitly brick-in-lime mortar veneered sandstone/marble and central marble tomb. This supports облицован, unlike only white-marble headline; own material example.', 'PASS','PASS'),
('NPS full physical PDF page1 What is Adobe discusses adobe versus kiln-fired clay and Southwest/North America. No Xinjiang wall-material trend is stated anywhere on that page. Current Russian claim is unsupported by bound proof; retain HOLD pending real source or authorized rewrite.', 'HOLD','PASS'),
('UNESCO explicitly includes Registan mosque as well as madrasahs with mud brick/tile cover. Mosque extends tested madrasah scope with a second building class; accept useful extra fact even though related to main explanation.', 'PASS','PASS'),
('USGS identifies limestone sedimentary calcium-carbonate fossils/fragments in calcite matrix. Granular carbonate paraphrase retains composition and rock class, own material definition.', 'PASS','PASS')],
'bam':[
('UNESCO names Arg-e Bam representative fortified medieval mud-layer/mud-brick town. Qaleh separate fortress nearest plausible option; mausolea/qanats allow narrowing by type, then local knowledge distinguishes two fortifications. Hard rule permits this substantive narrowing; no arbitrary unrelated choices.', 'PASS','PASS'),
('Full synthesis states representative town and other protected Qaleh/mausolea outside core. Both sentences supported; region shorthand not universal largest-city assertion.', 'PASS','PASS'),
('Full source outside core other protected structures includes Qaleh Dokhtar fortress. Distinct local fortress fact belongs to own option.', 'PASS','PASS'),
('Outside core explicit Zeyd and Asiri mausoleums supports both names and location. Own mausoleum facts.', 'PASS','PASS'),
('Full synthesis explicitly citadel contains governor quarters and fortified residential area. Both assertions supported, extra internal functions beyond stem material/type.', 'PASS','PASS'),
('Full synthesis underground irrigation qanats sustain life and continued agriculture/land use in integrity. Supports underground, cultivation and oasis life; own canal fact.', 'PASS','PASS')]
}
# Proof extraction is only preservation; the judgments above never depend on script-matched strings.
manifest=json.loads((AUTHOR/'sources-manifest.json').read_bytes()); originals={}
for m in manifest:
 rel=m['localCapture'];b=(AUTHOR/rel).read_bytes();write(OWN/rel,b)
 originals[rel]=dict(m,sha256=sha(b),bytes=len(b),resolvedAuthorPath=str(AUTHOR/rel),readerCapture=str((OWN/rel).relative_to(ROOT)),sourceClass='official heritage agency' if 'unesco' in rel else 'university glossary' if 'pitt-' in rel else 'official government source',captureMode='reused complete frozen original; no new fetch claimed')
write(OWN/'.gitattributes',b'sources/** -text\n')
for name in ['author-review.json','manual-analysis.json','duplicate-analysis.json','scope-lock.json','qa-evidence.json','roundtrip.json']:
 write(OWN/'author-history'/name,(AUTHOR/name).read_bytes())
write(OWN/'historical-reader-receipt.json',(OLD/'independent-receipt.json').read_bytes())
dump(OWN/'sources-manifest.json',list(originals.values()));dump(OWN/'approved-rules.json',{'source':'/Users/eaafonasev/Projects/mindbattle-planning/docs/GAME_SPEC.md','rules':rules})
# Full originals are resolved, normalized solely for quote reading, never substituted for raw bytes.
texts={}
for rel in originals:
 p=OWN/rel
 if p.suffix=='.json':texts[rel]={k:plain(str(v)) for k,v in json.loads(p.read_bytes())['results'][0].items()}
 elif p.suffix=='.pdf':texts[rel]={'physical-page-1':re.sub(r'\s+',' ',PdfReader(p).pages[0].extract_text()).strip()}
 else:
  soup=BeautifulSoup(p.read_bytes(),'html.parser')
  for el in soup(['script','style']):el.decompose()
  texts[rel]={'document':re.sub(r'\s+',' ',soup.get_text(' ',strip=True)).strip()}
# Each original quoted context retains the complete cited section/entry; missing historical strings stay visible.
def proof(rel,locator,quote=None):
 m=originals[rel];t=texts[rel]
 if rel.endswith('.json'):
  k=locator.split('/')[-1]; passage=t[k]; loc={'jsonPointer':locator,'section':k}
 elif rel.endswith('.pdf'):
  passage=t['physical-page-1'];loc={'physicalPage':1,'printedPage':'unnumbered first page','section':'What is Adobe?'}
 else:
  full=t['document'];q=plain(quote or '')
  # Preserve a broad complete context around supplied entry; where quote is absent preserve full document and flag mismatch.
  at=full.find(q);passage=full[max(0,at-250):min(len(full),at+len(q)+700)] if at>=0 else full
  loc={'htmlLocator':locator,'historicalAuthorQuoteFound':at>=0,'normalizedDocumentCharOffset':at,'contextMode':'normalized text context from complete frozen original'}
 return {'rawCapture':rel,'actualCaptureUrl':m['actualCaptureUrl'],'sourceUrl':m['url'],'sourceClass':m['sourceClass'],'rawFormat':m['rawFormat'],'rawCaptureSha256':m['sha256'],'frozenGitBlob':m['gitBlob'],'locator':loc,'quotedPassage':passage,'quotedPassageSha256':sha(passage.encode()),'quoteEncoding':'UTF-8 normalized original parsed text; raw bytes independently preserved'}
cards=[];history=json.loads((OLD/'independent-receipt.json').read_bytes())
for ac in a['cards']:
 q=qs[ac['id']]; key=ac['id'].removeprefix('architecture-'); judgments=analyses[key];fields=[]
 for i,af in enumerate(ac['fields']):
  field=af['field'];lit={'prompt':q['prompt'],'answers':[x['text'] for x in q['answers']],'correctIndex':q['correctIndex'],'key':q['answers'][q['correctIndex']]['text']} if field=='prompt-key' else q['explanation'] if field=='explanation' else q['answers'][int(field[-1])]['note']
  desc,sv,ev=judgments[i]; proofs=[]
  for ap in af['sourceProofs']:
   rel=ap['rawCapture'];loc=ap['locator'];loc=loc if isinstance(loc,str) else next(iter(loc.values()))
   if rel.endswith('.json') and not loc.startswith('/'):loc='/results/0/justification_en'
   proofs.append(proof(rel,loc,ap['quotedPassage']))
  extras=[]
  if key=='parthenon-city' and field=='note3':extras=[('sources/lpc-compressed.html','Column','A vertical, cylindrical support.')]
  if key=='entasis-effect' and field=='note3':extras=[('sources/pitt-arch.htm','arch and parts voussoir','The wedge shaped elements')]
  if key=='fez' and field=='note3':extras=[('sources/pitt-arcade.htm','arcade','A series of arches supported by columns or piers.')]
  if key=='samarkand' and field=='note0':extras=[('sources/unesco-252.json','/results/0/justification_en',None)]
  for rel,loc,quo in extras:proofs.append(proof(rel,loc,quo))
  verdict='HOLD' if sv=='HOLD' or ev=='HOLD' else 'FIX' if sv=='FIX' or ev=='FIX' else 'PASS'
  findings=[]
  if verdict!='PASS':
   cls='unsupported-source-claim' if sv=='HOLD' else 'source-qualifier-overclaim' if sv=='FIX' else 'meaningful-tested-fact-duplicate' if key=='mont-saint-michel' else 'one-answer-ambiguity'
   rule='notes' if field.startswith('note') else 'duplicates' if cls=='meaningful-tested-fact-duplicate' else 'unique'
   findings=[{'actualClass':cls,'specificDefect':desc,'approvedRule':rules[rule],'difficultyChangeRequested':False}]
  fields.append({'field':field,'currentLiteral':lit,'currentLiteralSha256':sha(canonical(lit)),'wholeCardCurrentSha256':sha(canonical(q)),'readerNativeIdentity':reader,'authorNativeIdentity':a['nativeAuthorIdentity'],'sourceVerdict':sv,'editorialVerdict':ev,'roleVerdict':verdict,'individualSourceAndEditorialAnalysis':desc,'sourceProofs':proofs,'findings':findings,'historicalAuthorClassification':{k:v for k,v in af.items() if k.startswith('historical')},'authorCurrentVerdicts':{'source':af.get('currentAuthorSourceVerdict'),'editorial':af.get('currentAuthorEditorialVerdict')},'authorAnalysisNotInherited':True})
 statuses=[f['roleVerdict'] for f in fields];whole='HOLD' if 'HOLD' in statuses else 'FIX' if 'FIX' in statuses else 'PASS'
 cards.append({'id':q['id'],'difficulty':q['difficulty'],'currentCard':q,'wholeCardCurrentSha256':sha(canonical(q)),'wholeCardVerdict':whole,'fields':fields})
from collections import Counter
counts={'cards':len(cards),'fields':sum(len(x['fields']) for x in cards),'wholeCard':dict(Counter(x['wholeCardVerdict'] for x in cards)),'field':dict(Counter(f['roleVerdict'] for x in cards for f in x['fields'])),'source':dict(Counter(f['sourceVerdict'] for x in cards for f in x['fields'])),'editorial':dict(Counter(f['editorialVerdict'] for x in cards for f in x['fields']))}
receipt={'role':'distinct actual native independent reader; coordinator alone certifies paired proof','readerNativeIdentity':reader,'authorNativeIdentity':a['nativeAuthorIdentity'],'sourceSnapshotCommit':'8011c201c864ae7ac788e784c53288c2629782a1','sourceFileSha256':sha(frozen),'sourceFileGitBlob':subprocess.check_output(['git','hash-object',str(source)],text=True).strip(),'authorPackageResolvedAbsolutePath':str(AUTHOR),'sourceReadMode':'complete frozen originals reused; personally read current 16x6 literals and cited original sections; no new fetch or snippet evidence','historicalReaderResults':'0 whole PASS/16 HOLD; field58PASS38HOLD; source85PASS11HOLD; not inherited','counts':counts,'cards':cards,'certificationClaimed':False}
dump(OWN/'independent-receipt.json',receipt);dump(OWN/'manual-analysis.json',{'readerNativeIdentity':reader,'counts':counts,'cards':cards});dump(OWN/'frozen-cards.json',[x['currentCard'] for x in cards])
partner=qs['architecture-burj-khalifa-city'];bagan=qs['architecture-bagan']
dump(OWN/'duplicate-analysis.json',{'catalogSearch':'read-only all src/content/topics/*.json stems and keyed answers; focused architecture all100 manually read','currentDuplicate':{'left':qs['architecture-mont-saint-michel'],'right':partner,'rightSha256':sha(canonical(partner)),'finding':'Both test exterior-face definition with key Фасад; main adjective does not diversify tested relation. Protected partner unchanged.'},'historicalDuplicateResolved':{'left':qs['architecture-skyscraper-definition'],'protectedPartner':bagan,'finding':'Drainpipe downstream conveyance now differs from building addition; historical Bagan duplicate is resolved. Bam is not this partner.'},'nearbyIndependentFacts':['pipe conveys gutter-to-ground versus gutter collects at eaves: distinct components/functions, not direct/reverse same relation','colonnade columns with beams versus arcade arches: contrasting different terms','landing between ramp runs versus ramp inclined passage: different component/function','Bam city composition versus regional earthen construction: not same tested relation'],'noSourceEdits':True})
assert len(cards)==16 and counts['fields']==96
assert source.read_bytes()==frozen
assert subprocess.check_output(['git','show','8011c20:src/content/topics/architecture.json'])==frozen
scope=json.loads((ROOT/'docs/content-audits/question-quality-wave-6/coordinator-continuation-01a12cda/architecture-remaining16-scope.json').read_bytes())
assert len(scope['protected84'])==84
assert all(sha(canonical(qs[x['questionId']]))==x['cardCanonicalSha256'] for x in scope['protected84'])
dump(OWN/'validation.json',{'counts':counts,'protected84CanonicalHashesUnchanged':True,'currentLiteralsRebound':True,'all16x6Present':True,'sourceEdits':False,'fullSuiteBuildPlayerDeployMergeArchive':False,'qa':'evidence integrity only; current topic literals/source hashes/96 coverage/raw preservation, not gameplay QA','knownUnrelatedQA':'Winter007008 old content-check issue not changed or retested here','testsSelected':'Python receipt integrity and raw Git roundtrip only; evidence-only changes'})
write(OWN/'REPORT.md',f'''# Fresh independent Architecture16 reader\n\nReader `{reader}` differs from author `{a['nativeAuthorIdentity']}`. Source literals frozen from architecture blob `{receipt['sourceFileGitBlob']}` after 8011c20/6ee675d.\n\nCounts: {json.dumps(counts)}. These are independent judgments, not paired certification. All 96 current literals were manually read and examined against complete frozen originals and their cited sections. Script only serializes explicit decisions and checks preservation; hashes never produce grades.\n\nRemaining findings:\n- mont-saint-michel prompt duplicates protected burj-khalifa-city exterior-face/Фасад relation. Change only owned card via authorized author, not partner.\n- Cartagena broad geography-in-defense stem also fits rocky crag option0 described as protecting isthmus access. Narrow criterion or replace competing option with authorized author.\n- Samarkand note1 claims Xinjiang wall-material trend; NPS physical page1 (unnumbered, What is Adobe?) has no Xinjiang support. HOLD pending full supporting original or authorized rewrite.\n- skyscraper explanation/note3 and empire note0 omit LPC's usually-metal qualifier. Preserve qualifier or omit categorical material.\n\nCurrent additions accepted: Theodoric example; correct facade decoration; colonnade beam name; Sophia construction date; archivolt-versus-voussoir structure; Forth207/107m; restoration partial scope; Bam governor quarters; Registan mosque scope. Overlap with explanation is allowed. Old one-sentence/cable/crypt/material classifications stay in author-history and historical reader receipt without being reused. Author current verdicts/old individualAnalysis contain stale mismatches (especially Xinjiang); independent proof resolves originals directly.\n\n29 full raw original files preserved with -text and exact byte hashes; no new fetch claimed. Each field stores current literal SHA, whole-card SHA, role identities, manual judgment, actual source URL/format/class/blob, full original context quotes and precise locator. PDF physical page and printed-page status recorded.\n\nNext step: coordinator reviews these independent findings and requests source-author fixes inside exact16 scope, then pairs genuinely current author/reader receipts. No source fix, full suite, build, Player, deploy, merge, archive or human acceptance was performed.\n'''.encode())
print(json.dumps(counts));print('sourceSha',sha(frozen))
