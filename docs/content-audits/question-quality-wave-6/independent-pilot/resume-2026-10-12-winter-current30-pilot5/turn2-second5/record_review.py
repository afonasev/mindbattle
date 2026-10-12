"""Serialize manually read editorial judgments; code validates evidence, never grades content."""
import hashlib,json,os,subprocess
from pathlib import Path
from html.parser import HTMLParser
ROOT=Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle')
assert Path.cwd()==ROOT
GIT=lambda *a:subprocess.check_output(['git',*a],text=True).strip()
assert GIT('rev-parse','--show-toplevel')==str(ROOT)
OUT=Path(__file__).parent
AUTHOR_COMMIT='5555068b7d62b49188b2aa6410f5ce8c59763e43'
AUTHOR_PATH='docs/content-audits/question-quality-wave-6/coordinator-continuation-01a12f20/turn2-remaining25/second5-author-whole6.json'
raw_author=Path(AUTHOR_PATH).read_bytes()
assert raw_author==subprocess.check_output(['git','show',AUTHOR_COMMIT+':'+AUTHOR_PATH])
author=json.loads(raw_author)
assert os.environ['CODEX_THREAD_ID']=='01a12f52-6e07-7ac3-a9e1-d063b8afd3cf'
assert os.environ['CODEX_THREAD_ID']!=author['authorThreadId']
sha=lambda b:hashlib.sha256(b).hexdigest()
compact=lambda v,sort=False:json.dumps(v,ensure_ascii=False,sort_keys=sort,separators=(',',':')).encode()
TOPIC='src/content/topics/winter-sports.json'
current_bytes=Path(TOPIC).read_bytes();topic=json.loads(current_bytes)
frozen=json.loads(subprocess.check_output(['git','show',AUTHOR_COMMIT+':'+TOPIC]))
immutable=json.loads(subprocess.check_output(['git','show','8825c76:'+TOPIC]))
class Nodes(HTMLParser):
 def __init__(self):super().__init__();self.nodes=[];self.skip=0
 def handle_starttag(self,t,a):
  if t in ('script','style'):self.skip+=1
 def handle_endtag(self,t):
  if t in ('script','style'):self.skip-=1
 def handle_data(self,d):
  if not self.skip and d.strip():self.nodes.append(d.strip())
sources={};nodes={}
for c in author['cards']:
 for f in c['fields']:
  for b in f['proofBindings']:
   p=b['capturePath']
   if p in sources:continue
   raw=Path(p).read_bytes();blob=GIT('hash-object',p)
   assert sha(raw)==b['rawSha256'] and blob==b['gitBlob']
   assert GIT('ls-files',p)==p and subprocess.check_output(['git','cat-file','blob',blob])==raw
   sources[p]={'originalUrl':b['originalUrl'],'actualCaptureUrl':b['actualCaptureUrl'],'rawPath':p,'rawType':b['rawFormat'],'rawSha256':sha(raw),'gitBlob':blob,'rawSizeBytes':len(raw),'durableTrackedOriginal':True}
   parser=Nodes();parser.feed(raw.decode());nodes[p]=parser.nodes
reasons={
'038':[
'The complete IIHF Boards or Wall definition encloses the playing surface and places shatterproof glass above it. End boards are only the end sections, not the entire surrounding structure; glass itself and a goal cage do not enclose and support it. Familiar rink architecture fits easy; no copied key word is in the prompt.',
'Boards surrounding the surface and glass above them are directly stated. The adjacent Goal Cage/Goal Line context places the frame at the goal rather than around the surface; the contrast is ordinary rink geometry, not a claim about never-displaced equipment during play. Two grammatical sentences.',
'The End Boards entry explicitly says boards at each end of the rink. This location concerns the particular alternative; it also explains why only end boards cannot answer the whole-perimeter question.',
'Material (fibreglass/composite) and approximate 1.2m height are expressly stated. Both are useful board-specific extra facts absent from the question about perimeter and glass support.',
'The complete Boards entry says shatterproof glass rises above boards to provide additional protection. This is a useful glass-specific property rather than a note misattributed to goalposts.',
'The Goal Cage definition expressly comprises a crossbar and two goalposts with a net attached. This structural fact belongs to the goal frame, not to the boards.'],
'039':[
'The complete Stick entry distinguishes the straight hand-held shaft from the curved blade used to carry, pass and shoot the puck. Heel and toe are explicitly local areas of the blade, not alternative names for the whole curved component. The prompt naturally asks that named component; familiar hockey-stick shape and function fit easy without rare rule recall.',
'The same complete entry explicitly provides shaft/blade shape and heel nearest shaft versus toe furthest. Two clear grammatical sentences explain the distinction; no unsupported material or curvature measurement is added.',
'The original explicitly says a straight shaft held by players. This useful shaft-specific fact does not instead describe the blade.',
'The entry explicitly defines heel as the area closest to the shaft. This spatial relationship is specific to the heel and accurately distinguishes it from the toe.',
'The original explicitly says a goalkeeper stick has a wider blade and shaft and is primarily used to defend the goal. Wider goalie blade is useful additional blade information beyond the curved puck-handling part asked in the prompt. The note also mentions shaft as context without replacing the blade-specific fact.',
'The entry explicitly defines toe as the area furthest from the shaft. This is an independently useful position fact for the named alternative.'],
'043':[
'COC divides events into speed/technical categories; Super-G has slightly less vertical drop than downhill and more gates requiring technical skill, while both are speed events. Downhill cannot be lower than itself; slalom/giant slalom are the technical events. Four genuine alpine disciplines are plausible. Medium is appropriate: knowing speed-versus-technical classification and the Super-G comparison needs topic familiarity, not merely absurd-option elimination.',
'The full downhill/Super-G/technical-event context supports both speed classification and the drop/gate/technical comparison. Two grammatical sentences faithfully paraphrase slightly lower drop as lower drop; no universal numeric difference is invented.',
'Slalom explicitly has the most gates and a high technical-skill requirement, and the following paragraph labels slalom/giant slalom the technical events. The note concerns slalom itself rather than giving a stray Super-G detail.',
'COC explicitly describes giant slalom as combining long, medium and short turns. The note is a useful discipline-specific fact and does not incorrectly call it a speed-category event.',
'COC states that in both speed events the fastest single-run time wins. This one-run scoring format supplements the prompt asking drop/gates/speed classification, even though downhill is also mentioned for comparison.',
'The complete Downhill passage explicitly states highest speeds and greatest vertical drop. The note correctly concerns this alternative and gives its distinguishing event properties.'],
'057':[
'The complete long-track individual paragraph expressly states pairs racing against the clock and lane changes once per lap. Short-track individuals race together on the smaller oval; long-track mass start is a pack and pursuit has two teams. The format-specific key avoids erroneously treating all long-track events as paired races. Easy is reasonable for widely televised winter-sport knowledge.',
'The long-track paragraph explicitly says lane changes equalize the distance covered. Two readable sentences explain paired timed racing and the geometric reason rather than adding an unsupported safety claim.',
'The actual long-track individual paragraph grants right of way to the outside-lane skater when both reach the crossover simultaneously. This is useful additional procedural detail absent from the prompt/key.',
'The actual short-track original describes the 111.12m smaller oval and four/six simultaneous racers. This note is correctly bound to short-track, not accidentally to the long-track source.',
'The complete long-track article puts all long-track events on a 400m oval and explicitly says all mass-start competitors are on the ice at once. The group/long-oval fact concerns this alternative without implying lane changes like paired time trials.',
'The complete pursuit section says two teams of three begin simultaneously on opposite sides. Both team size and start placement are supported; this is a pursuit-specific fact, not a mass-start fact.'],
'058':[
'The actual short-track original states a 111.12m oval marked on an international-sized rink; its individual-race paragraph supplies four/six racers at a time. Long-track individuals race in pairs, mass start has a pack but uses 400m, and pursuit teams start at opposite sides. Thus group plus smaller in-rink oval singles out short-track, with plausible speed-skating alternatives. Easy is reasonable for the broad winter-sports viewing audience.',
'The actual short-track passage supports the small in-rink oval; the actual long-track article independently supplies 400m for all long-track events and a simultaneous pack for mass start. These are the correct source directions. Two clear sentences; no swapped long/short citation is used as factual proof.',
'The actual long-track individual paragraph expressly says paired racing against the clock. This useful own-alternative fact is not imported from short-track evidence.',
'The original says international-sized ice rink. The current note abbreviates that as международного ледового катка: beyond the prompt saying merely inside a rink, it specifies the international rink format, a useful venue-standard fact. It is a modest addition and does not supply dimensions; no numeric rink size is silently imported into the literal. Repeated short-oval location does not make the whole note only a prompt/key repetition.',
'400m comes from the actual long-track introduction; simultaneous group racing comes from its mass-start section. Both current literal claims are supported together, rather than claiming short-track itself uses 400m.',
'The actual long-track pursuit section explicitly states simultaneous starts on opposite sides of the oval. This is a own-alternative spatial/start-format fact, not the short-track or mass-start start arrangement.']}
headings={'038':{'prompt-key':'Boards or Wall','explanation':'Boards or Wall / Goal Cage / Goal Line','note0':'End Boards','note1':'Boards or Wall','note2':'Boards or Wall','note3':'Goal Cage'},'039':{x:'Stick' for x in ['prompt-key','explanation','note0','note1','note2','note3']},'043':{'prompt-key':'Alpine speed and technical events / Downhill / Super-G','explanation':'Super-G / speed events','note0':'Slalom / technical events','note1':'Giant slalom','note2':'Speed events / single-run scoring','note3':'Downhill'},'057':{'prompt-key':'Long-track individual distance events','explanation':'Long-track individual distance events','note0':'Long-track crossover right of way','note1':'Short-track individual distance events','note2':'Long-track mass start / 400m introduction','note3':'Long-track team pursuit'},'058':{'prompt-key':'Short-track oval and individual races; long-track mass start contrast','explanation':'Short-track oval / long-track 400m oval and mass start','note0':'Long-track individual distance events','note1':'Short-track oval / international-sized rink','note2':'Long-track 400m introduction / mass start','note3':'Long-track team pursuit'}}
def extract(p,idx,heading):
 quote=nodes[p][idx]
 return {**sources[p],'locator':{'htmlTextNodeIndex0Based':idx,'htmlParserMethod':'HTMLParser handle_data; script/style excluded; nonempty nodes stripped; document order; entity decoding preserved','sectionHeading':heading},'exactQuote':quote,'exactQuoteSha256':sha(quote.encode()),'quoteDerivation':'Independently extracted original text node; not source text generated by a proof list.'}
cards=[];bindingcount=0
for a in author['cards']:
 q=next(q for q in topic['questions'] if q['id']==a['questionId']);old=next(q for q in frozen['questions'] if q['id']==a['questionId']);assert q==old
 short=q['id'][-3:];h=sha(compact(q,True));assert h==a['currentCanonicalSha256']
 if short=='058':
  orig=next(x for x in immutable['questions'] if x['id']==q['id']);assert q==orig
  assert h=='643d57dca4a05eafdee0400bfc756264df3273838384c7f30634936efc19f132'
 fields=[]
 for i,f in enumerate(a['fields']):
  name=f['field'];literal=[q['prompt'],q['correctIndex'],q['answers'][q['correctIndex']]['text']] if name=='prompt-key' else q['explanation'] if name=='explanation' else q['answers'][int(name[4:])]['note']
  assert literal==f['literal'];lh=sha(compact(literal) if isinstance(literal,list) else literal.encode());assert lh==f['literalSha256']
  proofs=[]
  for b in f['proofBindings']:
   idx=b['locator']['htmlTextNodeIndex0Based'];p=b['capturePath'];pr=extract(p,idx,headings[short][name])
   assert sha(b['exactQuote'].encode())==b['exactQuoteSha256']
   assert ' '.join(pr['exactQuote'].split())==' '.join(b['exactQuote'].split())
   pr['authorPassageSha256']=b['exactQuoteSha256'];pr['authorExactNodeBytesEqual']=pr['exactQuote']==b['exactQuote'];proofs.append(pr);bindingcount+=1
  if (short,name)==('058','prompt-key'):
   p=next(p for p in sources if p.endswith('/short-track.html'));proofs.append(extract(p,72,'Short-track 500/1000m individual group races'))
  if (short,name)==('038','explanation'):
   p=next(p for p in sources if p.endswith('/iihf-olympic-2026-terminology.html'));proofs.append(extract(p,126,'Goal Line between goalposts'))
  fields.append({'field':name,'literal':literal,'literalSha256':lh,'sourceVerdict':'SUPPORTED','editorialVerdict':'PASS','manualSourceAndEditorialReason':reasons[short][i],'sourceProofs':proofs})
 cards.append({'questionId':q['id'],'difficulty':q['difficulty'],'correctIndex':q['correctIndex'],'cardCanonicalSha256':h,'currentExactlyMatches5555068':True,'wholeCardVerdict':'PASS','checks':{'sourceEntailment':'PASS','difficulty':'PASS','parallelPlausibleUniqueOneKey':'PASS','noArtificialLexicalCue':'PASS','ownWrongNotes':'PASS','correctNoteUsefulExtra':'PASS','russianGrammar':'PASS','duplicates':'PASS'},'individualFields':fields})
assert len(cards)==5 and sum(len(c['individualFields']) for c in cards)==30
spec=Path('/Users/eaafonasev/Projects/mindbattle-planning/docs/GAME_SPEC.md');lines=spec.read_text().splitlines()
report={'schema':'mindbattle.independent-winter-turn2-second5.reader.v1','readerThreadId':os.environ['CODEX_THREAD_ID'],'readerIdentityOrigin':'Trusted native CODEX_THREAD_ID environment; no parent identity substitution','authorThreadId':author['authorThreadId'],'independentIdentityVerified':True,'authorReceiptPath':AUTHOR_PATH,'authorReceiptSha256':sha(raw_author),'authorReceiptGitBlob':GIT('hash-object',AUTHOR_PATH),'authorReceiptCommit':AUTHOR_COMMIT,'observedHead':GIT('rev-parse','HEAD'),'authorNativeHashRecipesPreservedSeparately':author['hashRecipes'],'readerNativeHashRecipe':'Whole card SHA256 compact sorted-key UTF8 JSON ensure_ascii=false; prompt-key compact UTF8 [prompt,index,key]; notes/explanation exact plain UTF8 with no added newline; quote exact original-node UTF8; raw source exact bytes.','approvedSpecRules':[{'path':str(spec),'line':n,'exactText':lines[n-1]} for n in [138,139,142,143,144,146]],'personalSourceRead':'Complete original HTML captures opened/parsed. Full relevant article descriptions and adjacent original dictionary entries personally read; old author verdicts not used to assign decisions. Unrelated website navigation and historical-medal content not claimed as substantive factual review.','sourceContextsPersonallyRead':{'iihf-olympic-2026-terminology.html':'nonempty nodes 35–42,90–96,116–128,227–234: surrounding Boards, End Boards, Goal Cage/Goal Line and complete Stick entries','alpine-skiing.html':'nonempty nodes 65–88: complete discipline category/drop/gates/turns/scoring/combined context','long-track.html':'nonempty nodes 68–99: 400m introduction, complete individual races and crossover, complete mass-start and team-pursuit descriptions','short-track.html':'nonempty nodes 61–88: 111.12m oval, all individual race pack sizes, same-gender relays and mixed relay description'},'cards':cards,'duplicateReview':{'method':'Read all100 current Winter prompts; narrow all110 current topic JSON search for board/stick/Super-G/long-short-track/mass-start/pursuit relations. Search false positives such as lace and koklyushki excluded.','observedWinterTopicSha256':sha(current_bytes),'winterPromptSnapshot':[{'id':q['id'],'prompt':q['prompt']} for q in topic['questions']],'externalPartners':[{'path':'src/content/topics/olympic-games.json','id':'olympic-games-summer-winter-gold','decision':'No duplicate: athlete winning summer/winter gold and skating medal background do not ask track layout or racing format; partner untouched.'}],'nearbyWinter':'038 surrounding boards differs from 065 icing lines and 066 offside. 039 curved stick component differs from 095 goalie glove. 043 Super-G relative drop/gates differs from 034 downhill maximum speed/drop,041 slalom scoring,090 combined events and092 homologation duration. 057 paired time-trial/crossover procedure and058 short-track pack/111.12m in-rink layout are nearby teaching comparisons but not inverse questions of one identical relation: each tests a different format-specific feature bundle. 059 direction and094 skate hinge remain separate facts. Shared illustrative notes are not themselves duplicated prompt/key cards.'},'integrityDiagnostics':{'authorBindingsValidated':bindingcount,'distinctOriginalsValidated':len(sources),'independentSupplementaryBindings':2,'supplementary058GroupProof':'Actual short-track node72 directly supplies simultaneous group racers; node67 alone is geometry.','supplementary038GoalPositionProof':'Adjacent actual Goal Line node126 supplies relationship to goalposts.'},'summary':{'fields':30,'individualSourceSUPPORTED':30,'individualEditorialPASS':30,'individualEditorialFIX':0,'individualEditorialHOLD':0,'wholeCardPASS':5,'wholeCardFIX':0,'wholeCardHOLD':0,'countIncrement':0,'countersEdited':False},'guards':{'fiveCurrentCardsExactly5555068':True,'058Exactly8825c76':True,'runtimeReviewhashCountersPlanningAuthorReceiptsUntouched':True,'oldReaderReceiptsImmutable':True,'IDLevelKeySlotsOrderUntouched':True,'protectedOther95UntouchedByReader':True},'validationScope':'Syntax/JSON completeness, native independence, exact current literal/card freezing, original SHA/Git durability and quote locator hashes, own-folder diff check only. No runtime/reviewhash/counters/planning edits; no npmQA/contentcheck/full/browsergame/build/Player/release/deploy/archive/human acceptance.','cleanup':{'ownedPersistentProcesses':0,'ownedTemporaryDownloadsCaches':0,'rawSourcesDurableInExistingGit':True,'foreignWorkPreserved':True},'continuation':'Current second5 only; STOP after this atomic evidence/commit. Other15 and fresh first3 require coordinator dispatch.'}
(OUT/'independent-reader-current30.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'summary':report['summary'],'bindings':bindingcount,'originals':len(sources),'cards':[(c['questionId'],c['wholeCardVerdict'],c['cardCanonicalSha256']) for c in cards]},ensure_ascii=False))
