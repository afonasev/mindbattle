"""Record manual current-card findings; extraction/hashing does not grade quality."""
import ast, hashlib, json, os, subprocess
from pathlib import Path
from html.parser import HTMLParser
from pypdf import PdfReader
ROOT=Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle')
assert Path.cwd()==ROOT
GIT=lambda *a:subprocess.check_output(['git',*a],text=True).strip()
assert GIT('rev-parse','--show-toplevel')==str(ROOT)
OUT=Path(__file__).parent
AUTHOR_COMMIT='f92f42a13f04494e829af1ec65bc09a0492f5c00'
AUTHOR_PATH='docs/content-audits/question-quality-wave-6/coordinator-continuation-01a12f20/turn2-remaining25/first5-author-whole6.json'
AUTHOR=json.loads(Path(AUTHOR_PATH).read_bytes())
assert subprocess.check_output(['git','show',AUTHOR_COMMIT+':'+AUTHOR_PATH])==Path(AUTHOR_PATH).read_bytes()
assert os.environ['CODEX_THREAD_ID']=='01a12f52-6e07-7ac3-a9e1-d063b8afd3cf'
assert AUTHOR['authorThreadId']!=os.environ['CODEX_THREAD_ID']
sha=lambda x:hashlib.sha256(x).hexdigest()
compact=lambda x,sort=False:json.dumps(x,ensure_ascii=False,sort_keys=sort,separators=(',',':')).encode()
TOPIC='src/content/topics/winter-sports.json'
topic=json.loads(Path(TOPIC).read_bytes())
baseline=json.loads(subprocess.check_output(['git','show',AUTHOR_COMMIT+':'+TOPIC]))
class Nodes(HTMLParser):
 def __init__(self):super().__init__();self.nodes=[];self.skip=0
 def handle_starttag(self,t,a):
  if t in ('script','style'):self.skip+=1
 def handle_endtag(self,t):
  if t in ('script','style'):self.skip-=1
 def handle_data(self,d):
  if not self.skip and d.strip():self.nodes.append(d.strip())
cache={};sources={}
for c in AUTHOR['cards']:
 for f in c['fields']:
  for b in f['proofBindings']:
   p=b['capturePath']
   if p in sources:continue
   raw=Path(p).read_bytes();blob=GIT('hash-object',p)
   assert sha(raw)==b['rawSha256'] and blob==b['gitBlob']
   assert GIT('ls-files',p)==p and subprocess.check_output(['git','cat-file','blob',blob])==raw
   sources[p]={'originalUrl':b['originalUrl'],'actualCaptureUrl':b['actualCaptureUrl'],'rawPath':p,'type':b['rawFormat'],'rawSha256':sha(raw),'gitBlob':blob,'durableTrackedOriginal':True}
   if p.endswith('.pdf'):cache[p]=[x.extract_text() for x in PdfReader(p).pages]
   else:
    parser=Nodes();parser.feed(raw.decode());cache[p]=parser.nodes
reason={
'030':[
'IIHF Face Mask supports the intended name. However the four answers are not mutually exclusive: mask is a broad name, while a wire cage is a full-face protector, also available for goaltenders. Hockey Canada physical page 81 even says wire masks. The prompt supplies no distinguishing structural property that makes a cage wrong. FIX the answer taxonomy/prompt; preserve assigned easy and slot.',
'First sentence is supported, and the visor-only-eyes statement is supported. But calling cage and polycarbonate shield other types relative to mask repeats the unsupported disjoint taxonomy. Hockey Canada treats shield/cage as facial protectors and also calls them masks. FIX this explanation together with the prompt/options.',
'Full-face protectors include wire cage, high-impact polycarbonate shield or a combination, explicitly on original page 80. A useful own-alternative fact, even though the whole question has answer overlap.',
'IIHF explicitly says goalkeepers in men/women play or players in the women competition wear the protective mask. Female field-player use supplements the goalie-identification prompt with a new mask-specific fact.',
'The full-face-protector styles explicitly include a high-impact polycarbonate shield. The note is a correct material/category fact for this alternative.',
'Page 80 defines visor as a partial face protector shielding only the eyes. The note accurately describes its limited coverage, not another answer.'],
'031':[
'FIS 3.7 explicitly defines Ski goggles and recommends their use for weather/rays. Separate goggles differs from attached visor, refractive correction and touring eyewear. Actual frozen/runtime difficulty is easy, not medium. Familiar goggles-eye protection is easy; knowing a rare rule number is unnecessary. Repeated alpine wording is domain specification, not a unique copied-term giveaway (visor also says alpine).',
'Weather/rays, optically correct lenses and recommendation are directly supported. The second sentence strengthens good, contrast-free visibility into contrastное зрение; that contrast property is not established by the literal FIS passage. FIX to a faithful good visibility statement rather than inferring a technical contrast claim.',
'The complete uvex visor-helmet product describes an integrated visor and a self-tinting variomatic lens reacting to changing light/weather. The current note qualifies models uvex and does not generalize that all visors self-tint.',
'The complete new uvex mtn tour original product paragraph explicitly says flexible nose-bridge folding and jacket chest-pocket storage. This is a useful fact about the listed sports eyewear, independent of an unsupported claim that FIS recommends it for racing.',
'Optically correct lenses are additional to the prompt/key weather/ray protection function. FIS explicitly states them; explanation overlap is allowed under GAME_SPEC.',
'The complete victorious pro V product paragraph explicitly identifies Over the Glasses (OTG) design. Some goggles rather than all is accurate; the fact concerns wearing corrective glasses with goggles.'],
'032':[
'The original guide says knee down to top of skate. Top of skate is the sole listed lower endpoint matching it; midpoint shin, ankle and lower kneecap are distinct endpoints. Familiar full shin coverage makes easy acceptable.',
'Page 5 explicitly gives knee-to-skate coverage and knee centered in the donut. Two concise grammatical sentences accurately explain fit.',
'The sock-over-pad and Velcro facts are true on page 6, but concern socks and shorts rather than the option До середины голени. They supply no useful fact about the midpoint or that extent of coverage. FIX this own-wrong-note failure under GAME_SPEC line 143; generic shin-equipment context is insufficient.',
'The two-finger clearance between top of foot and bottom of pad directly concerns the lower boundary in the ankle/foot region. It is relevant to this alternative and supplies precise fit information without simply restating the key.',
'Comfortable knee placement in the center donut concerns the kneecap position named by this alternative. It supplies a useful knee-fit fact, rather than claiming the lower pad endpoint is there.',
'Snug but comfortable straps preventing slipping is explicitly stated on page 5. It adds secure fit beyond the prompt asking the endpoint, not merely repeating knee-to-skate coverage.'],
'035':[
'The complete COC pairs short-program list explicitly includes twist lift and throw. Singles, ice dance and synchronized skating are parallel discipline names, not arbitrary unrelated sports. Easy remains appropriate for the broad adult group familiar with televised pairs; no rare numeric requirement is asked.',
'COC supports both pair elements; the complete Skate Canada Throw Jump definition explicitly supports partner-assisted takeoff and unassisted landing. Two concise grammatical sentences; no male/female-only requirement is invented.',
'Actual ice-dance article context names rhythm and free dance and lists lifts, twizzles, steps and choreographic elements. Both named routines and the dance-specific connection are supported; this is not a pairs note misbound as dance evidence.',
'Actual singles paragraph explicitly lists jumping passes, spins and a step sequence. The note has the correct singles binding and useful discipline-specific information.',
'Besides the twist/throw named in the prompt, the pairs short program includes a solo jump performed side-by-side. That is a genuinely additional pairs fact. Repeating twist/throw does not invalidate the note when the new fact is present.',
'The complete current ISU synchronized rules pages 43–44 define Block, Circle, Line and Wheel as team shapes. This factual formation note belongs to synchronized skating.'],
'036':[
'IIHF explicitly identifies overtime after a tie at the conclusion of regulation. Main time and intermission differ from playing an additional period, and a shootout is a distinct resolution phase. Overtime is familiar adult sports knowledge; easy is appropriate.',
'IIHF Overtime and Shootout entries support the name and the conditional shootout after tied overtime. Some formats is appropriately qualified rather than asserting a single worldwide universal rule. Two grammatical sentences.',
'The literal says the IIHF Olympic-2026 page states this sequence, and that complete entry does. It concerns the shootout rather than wrongly equating shootout with overtime. It is not generalized to every possible tournament rule.',
'The Regulation Time entry explicitly states three twenty-minute periods and excludes overtime and shootout. The note is accurate for this phase and does not mislabel an intermission.',
'The Intermission entry explicitly describes a recess between each regulation period. This is a useful definition of the named break and does not imply it is playing time.',
'The complete Overtime entry gives tie-triggered extra play and first-goal sudden death. First-goal termination adds a useful rule beyond the prompt asking the name; the note explicitly qualifies sudden-death format.']}
fix={('030','prompt-key'),('030','explanation'),('031','explanation'),('032','note0')}
# Original supplementary context directly grounds the nested mask/cage finding.
facial=next(p for p in sources if p.endswith('hockeycanada-facial-protectors.pdf'))
def proof(b):
 p=b['capturePath'];loc=dict(b['locator']);is_pdf=p.endswith('.pdf')
 if is_pdf:
  n=loc['pdfPhysicalPage1Based'];quote=cache[p][n-1]
  loc['printedPage']=None if p.endswith('hockeycanada-player-equipment-guide.pdf') else n
  loc['ruleSectionOrHeading']={'030':'EQUIPMENT TIPS / FACIAL PROTECTORS','031':'3.7 Ski goggles','032':'SHIN PADS or SOCKS','035':'Definitions of elements/shapes / Block Circle Line Wheel'}.get(current,'')
 else:quote=cache[p][loc['htmlTextNodeIndex0Based']]
 assert sha(b['exactQuote'].encode())==b['exactQuoteSha256']
 if not is_pdf:assert ' '.join(quote.split())==' '.join(b['exactQuote'].split())
 else:assert ' '.join(b['exactQuote'].split()) in ' '.join(quote.split())
 return {**sources[p],'locator':loc,'exactQuote':quote,'exactQuoteSha256':sha(quote.encode()),'authorQuoteExactBytesEqualToOriginalNode':quote==b['exactQuote'] if not is_pdf else None,'authorQuoteWhitespaceNormalizedMatch':True,'authorQuotedPassageSha256':b['exactQuoteSha256'],'quoteDerivation':'Independent complete original PDF-page or nonempty HTML text-node extraction; script/style excluded. Reader quote preserves original NBSP. Author Throw Jump quotation has NBSP normalized to spaces; its separately declared hash is not presented as an exact raw-node hash.'}
cards=[]
for a in AUTHOR['cards']:
 q=next(x for x in topic['questions'] if x['id']==a['questionId']);frozen=next(x for x in baseline['questions'] if x['id']==q['id'])
 assert q==frozen;current=q['id'][-3:];h=sha(compact(q,True));assert h==a['currentCanonicalSha256']
 if current=='035':assert h=='74ae42c5d799e4cbbbd24016267cda9e6184ef1f8d162ebe117110fc6fa123ae'
 fields=[]
 for i,f in enumerate(a['fields']):
  name=f['field'];literal=[q['prompt'],q['correctIndex'],q['answers'][q['correctIndex']]['text']] if name=='prompt-key' else q['explanation'] if name=='explanation' else q['answers'][int(name[4:])]['note']
  assert literal==f['literal'];lh=sha(compact(literal) if isinstance(literal,list) else literal.encode());assert lh==f['literalSha256']
  proofs=[proof(b) for b in f['proofBindings']]
  if current=='030' and name in ('prompt-key','explanation'):
   quote=cache[facial][80]
   proofs.append({**sources[facial],'locator':{'pdfPhysicalPage1Based':81,'printedPage':81,'ruleSectionOrHeading':'FACIAL PROTECTORS / FITTING / PROTECTIVE QUALITY'},'exactQuote':quote,'exactQuoteSha256':sha(quote.encode()),'quoteDerivation':'Supplementary independently read adjacent original page explicitly says wire masks.'})
  fields.append({'field':name,'literal':literal,'literalSha256':lh,'sourceVerdict':'PARTIAL_UNSUPPORTED_CONTRAST_CLAIM' if (current,name)==('031','explanation') else 'PARTIAL_UNSUPPORTED_DISJOINT_TAXONOMY' if (current,name)==('030','explanation') else 'SUPPORTED','editorialVerdict':'FIX' if (current,name) in fix else 'PASS','manualSourceAndEditorialReason':reason[current][i],'sourceProofs':proofs})
 checks={'sourceEntailment':'FIX' if current in ('030','031') else 'PASS','difficulty':'PASS (actual easy retained)','parallelPlausibleOneKey':'FIX (mask/cage overlap)' if current=='030' else 'PASS','noArtificialLexicalCue':'PASS','ownWrongNotes':'FIX (note0 about socks, not midpoint)' if current=='032' else 'PASS','correctNoteExtra':'PASS','russianGrammar':'PASS','duplicates':'PASS'}
 cards.append({'questionId':q['id'],'difficulty':q['difficulty'],'correctIndex':q['correctIndex'],'cardCanonicalSha256':h,'currentExactlyMatchesAuthorCommit':True,'wholeCardVerdict':'FIX' if current in ['030','031','032'] else 'PASS','checks':checks,'individualFields':fields})
assert len(cards)==5 and sum(len(c['individualFields']) for c in cards)==30
spec=Path('/Users/eaafonasev/Projects/mindbattle-planning/docs/GAME_SPEC.md');lines=spec.read_text().splitlines()
report={'schema':'mindbattle.independent-winter-turn2-first5.reader.v1','readerThreadId':os.environ['CODEX_THREAD_ID'],'readerIdentityOrigin':'Trusted native CODEX_THREAD_ID execution environment','authorThreadId':AUTHOR['authorThreadId'],'independentIdentityVerified':True,'authorReceiptPath':AUTHOR_PATH,'authorReceiptGitBlob':GIT('hash-object',AUTHOR_PATH),'authorReceiptCommit':AUTHOR_COMMIT,'observedHead':GIT('rev-parse','HEAD'),'frozenSourceScope':'Only 030031032035036 full cards; whole topic file may change through concurrent authorized work on other cards.','authorNativeHashRecipesPreservedSeparately':AUTHOR['hashRecipes'],'readerNativeHashRecipe':'SHA256 UTF8 compact sorted-key complete card JSON ensure_ascii=false; prompt-key compact [prompt,correctIndex,key text]; plain UTF8 notes/explanation without extra newline; quotes exact extraction UTF8; source exact bytes.','approvedSpecRules':[{'path':str(spec),'line':n,'exactText':lines[n-1]} for n in [138,139,142,143,144,146]],'personalSourceRead':'Complete original PDF/HTML capture bytes opened and parsed; substantive source sections plus adjacent original rule/article context personally read. Not old author grades or quote list certification. Unrelated full-document sections not claimed as personally read.','sourceContextsRead':{'hockeycanada-facial-protectors.pdf':'physical/printed 79–81, helmets/facial styles/goalie and non-goalie categories/fitting/wire masks','fis-equipment-2026-10-08.pdf':'physical/printed 34–35, helmet context and 3.7 Goggles plus 3.8 Gloves','hockeycanada-player-equipment-guide.pdf':'physical 4–7 Jock/Jill, Shin Pads, Socks, Pants; unnumbered printed pages','isu-sys-rules-2026.pdf':'physical/printed 42–45, definitions and team-shape context','coc-figure-skating.html':'all normalized nonempty nodes 65–99, complete main discipline/program/scoring description','iihf-olympic-2026-terminology.html':'Face Mask 93–97, Intermission 141–145, Overtime 166–175 including durations and sudden death, Regulation Time 205–209, Shootout 217–221','skate-throw-complete.html':'complete main Throw Jump definition and neighboring navigation','uvex-wanted-visor-pro-v.html':'normalized nonempty nodes 54–62, complete main product description and features','uvex-mtn-tour.html':'normalized nonempty nodes 52–60, complete product folding/optics/UV/mountaineering description','uvex-victorious-pro-v-goggles.html':'normalized nonempty nodes 53–61, complete main product/OTG description and features'},'cards':cards,'duplicateReview':{'method':'Personally read current 100 Winter prompts; narrow current all-110-topic search for goalie mask, goggles, shin-pad coverage, pair throws/twist lifts and overtime. Search false positives about emissions not treated as matches.','currentWinterTopicObservedSha256':sha(Path(TOPIC).read_bytes()),'winterPromptSnapshot':[{'id':q['id'],'prompt':q['prompt']} for q in topic['questions']],'externalPartners':[{'path':'src/content/topics/combat-sports.json','id':'combat-sports-023','decision':'No duplicate: body region for combat shin guards differs from the precise hockey-pad lower endpoint; no partner edit.'},{'path':'src/content/topics/sports.json','id':'sports-basketball-free-throw-point','decision':'No duplicate: NBA overtime length differs from naming the hockey extra period; no partner edit.'}],'nearbyWinter':'030 face mask differs from 029 chinstrap. 031 goggles differs from 007 boots and 023 edges. 032 pad endpoint differs from helmet fit. 035 pair element identification differs from 022 Rodnina discipline, 008 program order and 026 spin identification; 035 note sync formations overlaps 060 supporting material, not the pair prompt/key. 036 overtime name differs from 004 regulation period count and 012 penalty shot. No direct/reverse duplicate question found.'},'difficultyScopeNote':'All five actual f92f42a/current cards are easy, including 031. Review did not substitute medium from task prose and did not reclassify anything; no difficulty HOLD.','summary':{'fields':30,'individualSourceSupported':28,'individualSourcePartial':2,'individualEditorialPASS':26,'individualEditorialFIX':4,'individualEditorialHOLD':0,'wholeCardPASS':2,'wholeCardFIX':3,'wholeCardHOLD':0,'countIncrement':0,'countersEdited':False},'validationScope':'Syntax/JSON completeness/native identity/literal/card frozen guard/source-byte SHA and Git-blob durability/quote locator integrity/own-folder diff only. No runtime/reviewhash/counter/planning edits; no npm QA/full/contentcheck/browsergame/build/Player/release/deploy/archive or human acceptance.','cleanup':{'ownedProcesses':0,'temporaryDownloadsOrCachesCreated':False,'originalSourcesTrackedInGit':True,'foreignFilesAndOldFirst5ReceiptPreserved':True},'continuation':'Stop at first5 freeze. Coordinator may authorize fixes and later other20 separately; no autonomous dispatch.'}
report['integrityDiagnostics']={'authorBindingsValidated': 38, 'distinctOriginalsValidated': 10, 'supplementaryOriginalPage81Bindings': 2, 'authorThrowJumpQuoteUsesNormalizedSpaces': True, 'readerThrowJumpQuotePreservesOriginalNBSP': True, 'pdfExtractionDiagnostic': 'pypdf emitted missing fontTools warnings while parsing complete Hockey Canada capture; all cited original-page passages successfully roundtripped. No missing cited text or malformed PDF output used.'}
(OUT/'independent-reader-current30.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'summary':report['summary'],'cards':[(c['questionId'],c['wholeCardVerdict'],c['cardCanonicalSha256']) for c in cards],'sources':len(sources)},ensure_ascii=False))
