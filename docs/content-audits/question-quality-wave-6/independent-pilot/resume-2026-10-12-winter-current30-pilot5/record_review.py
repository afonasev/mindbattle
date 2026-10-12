"""Serialize the reader's manually assessed decisions; no automatic quality grading."""
import json, hashlib, os, subprocess
from pathlib import Path
from html.parser import HTMLParser
from pypdf import PdfReader
ROOT=Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle')
assert Path.cwd()==ROOT
assert subprocess.check_output(['git','rev-parse','--show-toplevel'],text=True).strip()==str(ROOT)
OUT=Path(__file__).parent
RECEIPT=Path('docs/content-audits/question-quality-wave-6/winter-sports/resume-2026-10-12-current30-repair/author-correction-after-47690a4-native.json')
AUTHOR=json.loads(RECEIPT.read_text())
TOPIC=Path('src/content/topics/winter-sports.json')
TOPIC_BYTES=TOPIC.read_bytes(); topic=json.loads(TOPIC_BYTES)
IDS=['winter-sports-'+x for x in ['007','008','023','026','029']]
sha=lambda b: hashlib.sha256(b).hexdigest()
compact=lambda v,sort=False:json.dumps(v,ensure_ascii=False,separators=(',',':'),sort_keys=sort).encode()
git=lambda *args:subprocess.check_output(['git',*args],text=True).strip()
class Nodes(HTMLParser):
 def __init__(self):super().__init__();self.nodes=[]
 def handle_data(self,d):self.nodes.append(d)
readings={}; sources={}
for c in AUTHOR['cards']:
 for f in c['fields']:
  for b in f['proofBindings']:
   p=b['rawCapture']
   if p in sources:continue
   raw=Path(p).read_bytes(); blob=git('hash-object',p)
   assert git('cat-file','-t',blob)=='blob' and subprocess.check_output(['git','cat-file','blob',blob])==raw
   assert git('ls-files',p)==p
   sources[p]={'url':b['url'],'type':b['rawFormat'],'rawPath':p,'sha256':sha(raw),'gitBlob':blob,'durableInGit':True}
   if p.endswith('.pdf'):readings[p]=[pg.extract_text() for pg in PdfReader(p).pages]
   else:
    parser=Nodes();parser.feed(raw.decode());readings[p]=parser.nodes
reasons={
'007':[
'Firm enclosure of the foot and steering transfer uniquely identify the boot, rather than ski edges, binding or poles. This familiar footwear relation is easy without specialist rule recall.',
'The complete boot definition supports enclosure, ankle flexibility and steering transfer. Two grammatical sentences explain the function; ankle flexibility adds useful detail.',
'The note describes the edges themselves: wear-resistant material and lateral forces. It does not falsely describe boot fit. Its overlap with 023 is explanatory context, not a repeated boot-function question.',
'Release at preset load is the specific function of the binding, not the boot. Concise neutral fact with a concrete connection to this distractor.',
'Ankle room for flexion is absent from the prompt/key and supplements firm foot enclosure. It may also occur in explanation under the approved rule.',
'Metal baskets being forbidden is a checkable pole-specific equipment detail; the FIS context is supplied. It need not explain why a pole is not footwear.'],
'008':[
'Singles and pairs advance from short program to free skating, while the other listed judged winter disciplines use runs/jumps. All alternatives name sports or disciplines; familiar broadcast terminology makes easy appropriate.',
'Article context explicitly distinguishes singles/pairs from rhythm/free dance and gives 2:40 ±10 seconds and seven elements. Two clear sentences, with the ice-dance exception preventing overgeneralization.',
'Distance and body position in flight and landing are explicitly stated in the jumping article. This is non-exhaustive (depends on, not solely determined by); wind/gate context does not contradict it.',
'The halfpipe paragraph explicitly lists variety, difficulty, style and execution. The note is attached to snowboard halfpipe rather than a general skating fact.',
'The moguls paragraph assigns 60% to turns and 20% to speed (remaining 20% aerial tricks). It correctly excludes the different dual-moguls weights.',
'The seven elements and 2:40 ±10-second length supplement the program-sequence question with a specific verified fact. Explanation overlap is permitted.'],
'023':[
'Hard wear-resistant material and lateral-force transmission identify edges in FIS 3.1.2.1. Interface, release binding and brake have distinct functions; technical construction/function knowledge reasonably fits medium.',
'Location along the edges of the running surface is supported by the complete ski definition, along with force transmission and wear resistance. Two readable sentences; no runtime change needed.',
'The interface is explicitly mounted between ski and release binding; this useful spatial relationship concerns that alternative.',
'The binding releases the boot when load reaches preset values; no unsupported claim that the edge itself releases.',
'Besides repeating material/function, the note locates these edges on the running surface. The prompt/key does not supply that location. That is useful additional spatial information, so the note is not only a prompt/key restatement; overlap with explanation is allowed.',
'The retention-device definition states that a ski brake slows a ski after binding release. The note correctly describes this alternative rather than implying it transmits lateral force.'],
'026':[
'Repeated turning around oneself on the ice is a spin, distinguished from an airborne jump, travelling step sequence and pair lift. Turns/rotation is a necessary ordinary semantic definition, not an artificial copied-word cue. Easy is appropriate.',
'Rule 610 of the actual 2026 Single & Pair rules explicitly excludes fewer than three rotations; this is not inferred from synchronized skating. The remaining sentence uses supported singles/pairs program contents.',
'The singles short program lists three jumping passes including one combination; ISU 611 context confirms the same three jump-element slots. The note concerns jumps.',
'The exact under-three-rotations boundary adds a rule threshold beyond the general repeated-turning prompt. No overclaim that every three-turn movement automatically has value: other spin requirements remain in context.',
'One step sequence is explicit in the singles short program list and in ISU 611. A short useful fact attached to that skating element.',
'The pairs short-program list separately names one lift and one twist lift; the note says one lift, not that the program contains no twist lift. This is a valid program detail for the listed element.'],
'029':[
'Chinstrap identifies the fastening below the chin. The guide explicitly distinguishes chinstrap fit from chin cup contact; below-chin location is ordinary anatomical interpretation of chinstrap, not a verbatim location claim. The cup, shell and certification sticker are helmet-related alternatives; only the strap fastens. Easy recognition is appropriate.',
'The helmet paragraph supports snug strap preventing wobble, cup contacting chin and helmet height. The below-chin wording is the ordinary anatomical interpretation of chinstrap. Two grammatical, concrete sentences.',
'Snugness preventing wobble adds fit/function beyond the prompt asking which part fastens under the chin. Source explicitly states this benefit.',
'Comfortable chin contact and no gap are explicitly stated for the chin cup; they are not incorrectly attributed to the strap.',
'One to two fingers above eyebrows is a checkable fitting detail for the helmet shell. It does not claim the shell is a fastening.',
'The guide directs checking the CSA certification sticker. Calling it certification follows the explicitly named CSA certification sticker, with no unsupported protection guarantee.']}
assert set(reasons)=={'007','008','023','026','029'}
cards=[]
for q in topic['questions']:
 if q['id'] not in IDS:continue
 a=next(c for c in AUTHOR['cards'] if c['questionId']==q['id'])
 h=sha(compact(q,True)); assert h==a['cardCanonicalSha256']
 if q['id'].endswith('023'):
  baseline=json.loads(subprocess.check_output(['git','show','8825c76:src/content/topics/winter-sports.json']))
  old=next(c for c in baseline['questions'] if c['id']==q['id']);assert q==old
 fields=[]
 for j,f in enumerate(a['fields']):
  name=f['field']; literal=[q['prompt'],q['correctIndex'],q['answers'][q['correctIndex']]['text']] if name=='prompt-key' else q['explanation'] if name=='explanation' else q['answers'][int(name[4:])]['note']
  assert literal==f['literal']
  fieldhash=sha(compact(literal) if isinstance(literal,list) else literal.encode())
  assert fieldhash==f['literalSha256']
  proofs=[]
  for b in f['proofBindings']:
   loc=b['locator'];p=b['rawCapture'];idx=loc.get('pdfPhysicalPage',0)-1 if p.endswith('.pdf') else loc['htmlTextNodeIndex0Based']
   quote=readings[p][idx]
   proofs.append({**sources[p],'locator':loc,'exactQuote':quote,'exactQuoteSha256':sha(quote.encode()),'quoteDerivation':'Independent extraction of complete original PDF page or HTMLParser text node; not author quotation copied as evidence.','authorPassageQuoteSha256':b['exactQuoteSha256']})
  fields.append({'field':name,'literal':literal,'literalSha256':fieldhash,'sourceVerdict':'SUPPORTED','editorialVerdict':'PASS','manualSourceAndEditorialReason':reasons[q['id'][-3:]][j],'sourceProofs':proofs})
 cards.append({'questionId':q['id'],'difficulty':q['difficulty'],'correctIndex':q['correctIndex'],'cardCanonicalSha256':h,'wholeCardVerdict':'PASS','individualFields':fields,'checks':{'sourceEntailment':'PASS (029 anatomical location is stated as interpretation)','difficulty':'PASS','parallelPlausibleOneKey':'PASS','noArtificialLexicalCue':'PASS','ownWrongNotes':'PASS','correctNoteExtra':'PASS','russianGrammar':'PASS','duplicates':'PASS'},'duplicateReview':'Read all 100 current Winter prompts; narrowly searched all 110 current topic JSONs for new boot/edges/program/spin/chinstrap facts. 007 boot fit/function differs from 023 edge construction, 073 binding release and 076 assembled mass. 008 sequence differs from 026 spin identification. Supporting notes may overlap; no direct/reverse duplicate prompt-key relationship found.'})
assert len(cards)==5 and sum(len(c['individualFields']) for c in cards)==30
spec=Path('/Users/eaafonasev/Projects/mindbattle-planning/docs/GAME_SPEC.md');lines=spec.read_text().splitlines()
report={'schema':'mindbattle.independent-winter-current30-pilot5.reader.v1','readerThreadId':os.environ['CODEX_THREAD_ID'],'readerIdentityOrigin':'CODEX_THREAD_ID from native execution environment in this delegated reader chat','authorThreadId':AUTHOR['authorThreadId'],'independentIdentityVerified':os.environ['CODEX_THREAD_ID']!=AUTHOR['authorThreadId'],'authorReceipt':str(RECEIPT),'authorReceiptGitBlob':git('hash-object',str(RECEIPT)),'authorReceiptCommit':'aff2efa','runtimeSourceCommit':'88c1651','observedHead':git('rev-parse','HEAD'),'wholeTopicSha256':sha(TOPIC_BYTES),'nativeHashRecipes':AUTHOR['hashRecipes'],'declaredReaderHashRecipe':'whole card: UTF8 compact JSON ensure_ascii=false sort_keys=true; prompt-key: UTF8 compact [prompt,correctIndex,key text]; other fields exact UTF8 without added newline; SHA256','manualReadScope':'Complete original captures parsed; substantive source passages and surrounding article/adjacent rule pages personally read, not old grades or source quote lists. Full unrelated rules/history not represented as personally read.','sourceContextsPersonallyRead':{'fis-equipment-2026-10-08.pdf':[15,16,17,23,24,25,26,27],'isu-single-pair-skating-rules-2026.pdf':[64,65,66,67],'hockeycanada-player-equipment-guide.pdf':[12,13,14],'fis-ski-jumping-current.pdf':[70,71,72],'fis-wc-jumping-men-2026-27.pdf':[13],'coc HTML documents':'article text nodes 385–450; skating disciplines, singles/pairs/ice dance and scoring; jumping scoring; halfpipe and moguls context'},'approvedSpecRules':[{'path':str(spec),'line':n,'exactText':lines[n-1]} for n in [142,143,144,146]],'cards':cards,'summary':{'individualSourceSupported':30,'individualEditorialPass':30,'wholeCardPASS':5,'FIX':0,'HOLD':0,'countIncrement':0,'countersChangedByReader':False,'007008HistoricalCountNotIncremented':True,'certificationCounterUpdate':'Coordinator responsibility; reader adds no count.'},'guards':{'topicUnmodified':TOPIC.read_bytes()==TOPIC_BYTES,'protected95Unmodified':True,'IDsDifficultySlotsOrderUnmodified':True,'023ExactlyEquals8825c76':True,'reviewRuntimePlanningCounterFilesNotEdited':True},'validationScope':'JSON syntax, current literal/card binding, raw source SHA/Git durability, immutable023, own-folder diff check only; no content-check/npm/full/browser/build/Player/release/deploy/archive/human acceptance.','cleanup':{'ownedProcesses':0,'temporaryCachesOrDownloadsCreated':False,'originalSourcesDurableInExistingGit':True,'foreignWorkPreserved':True},'continuation':'Future25 only on coordinator authorization; this chat remains available, no automatic dispatch.'}
(OUT/'independent-reader-current30.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'cards':[(c['questionId'],c['cardCanonicalSha256'],c['wholeCardVerdict']) for c in cards],'sources':len(sources),'fields':30},ensure_ascii=False))
