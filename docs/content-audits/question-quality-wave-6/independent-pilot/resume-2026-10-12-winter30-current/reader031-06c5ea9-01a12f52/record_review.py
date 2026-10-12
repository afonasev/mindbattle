"""Serialize manually assessed current031 only. Code validates provenance, not quality."""
import hashlib,json,os,re,subprocess
from pathlib import Path
from html.parser import HTMLParser
ROOT=Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle')
assert Path.cwd()==ROOT
GIT=lambda *a:subprocess.check_output(['git',*a],text=True).strip()
assert GIT('rev-parse','--show-toplevel')==str(ROOT)
OUT=Path(__file__).parent
FREEZE='06c5ea9'
BASE=Path('docs/content-audits/question-quality-wave-6/winter-sports/resume-2026-10-12-fresh-fix3-remaining15/author031-fresh-repair')
AP=BASE/'author-current031-receipt.json';SP=BASE/'source-context.json'
for p in (AP,SP):assert p.read_bytes()==subprocess.check_output(['git','show',FREEZE+':'+str(p)])
author=json.loads(AP.read_bytes());source_context=json.loads(SP.read_bytes());a=author['cards'][0]
assert a['questionId']=='winter-sports-031' and len(author['cards'])==1
READER=os.environ['CODEX_THREAD_ID'];assert READER=='01a12f52-6e07-7ac3-a9e1-d063b8afd3cf'
assert author['authorIdentity']['nativeThreadId']!=READER
sha=lambda b:hashlib.sha256(b).hexdigest()
compact=lambda v,sort=False:json.dumps(v,ensure_ascii=False,sort_keys=sort,separators=(',',':')).encode()
TOPIC='src/content/topics/winter-sports.json';topic=json.loads(Path(TOPIC).read_bytes())
q=next(x for x in topic['questions'] if x['id']==a['questionId'])
frozen=json.loads(subprocess.check_output(['git','show',FREEZE+':'+TOPIC]));assert q==next(x for x in frozen['questions'] if x['id']==q['id'])
cardhash=sha(compact(q,True));assert cardhash==a['canonicalCardSha256']
assert q['difficulty']=='easy' and q['correctIndex']==2
class Nodes(HTMLParser):
 def __init__(self):super().__init__();self.nodes=[];self.skip=0
 def handle_starttag(self,t,a):
  if t in ('script','style'):self.skip+=1
 def handle_endtag(self,t):
  if t in ('script','style'):self.skip-=1
 def handle_data(self,d):
  if not self.skip and d.strip():self.nodes.append(d.strip())
b=source_context['sources'][0];p=b['rawCapturePath'];raw=Path(p).read_bytes();blob=GIT('hash-object',p)
assert len(raw)==813234 and len(raw)==b['rawSizeBytes']
assert sha(raw)==b['rawSha256'] and blob==b['gitBlob']
assert GIT('ls-files',p)==p and subprocess.check_output(['git','cat-file','blob',blob])==raw
parser=Nodes();parser.feed(raw.decode())
source={'originalUrl':b['originalUrl'],'actualCaptureUrl':b['actualCaptureUrl'],'rawType':b['captureType'],'rawPath':p,'rawSha256':sha(raw),'gitBlob':blob,'rawSizeBytes':len(raw),'sourceClass':b['sourceClass'],'durableTrackedOriginal':True}
for e in b['extracts']:
 idx=e['locator']['htmlTextNodeIndex0Based'];assert parser.nodes[idx]==e['exactQuote'] and sha(parser.nodes[idx].encode())==e['exactQuoteSha256']
reasons=[
'Complete Julbo Ventilation section says airflow prevents fogging. The same personally read article assigns light adaptation to photochromic lenses, snow/ice glare reduction to polarization, and peripheral vision to wider frames. The four current options are real comparable visibility functions, not body-part absurdities; only fog reduction is the described ventilation function. GAME_SPEC138 easy is met through the familiar practical link of airflow to condensation/fogging for adults who wear glasses or know winter sports; no rare product/model term is needed. The question is no longer the goggles→eyes relation tested inversely in laboratory/workshop partners. No stem/key copied-word cue.',
'Full article context explicitly supplies airflow, fog prevention and additional comfortable face temperature; Lens Types and wider-frame paragraphs supply the three contrasting functions. Both current sentences are supported, with no universal model-specific performance percentage. Two readable grammatical sentences distinguish the alternatives and explain the key.',
'The original Photochromic heading plus adjacent full text states automatic adaptation to light changes. The note assigns the current wrong light-adaptation function to its actual lens technology, making a useful own-function fact rather than unrelated lens trivia.',
'The original Polarized heading plus adjacent paragraph describes eliminating glare from snow and ice. The current reduces glare claim is a conservative paraphrase. It is a useful own-function fact explicitly tied to the glare-reduction alternative.',
'The full Ventilation section explicitly gives comfortable internal temperature for the face as an additional airflow benefit. Temperature comfort is absent from current prompt/key, so this note supplies useful extra information beyond anti-fogging. Its presence also in explanation is permitted by GAME_SPEC143.',
'The complete mens-goggle paragraph explicitly says wider frames offer increased peripheral vision. The current may increase wording is appropriately cautious. It directly explains the side-view function offered by this wrong alternative, without pretending ventilation widens the field of view.'
]
fields=[];bindings=0
for i,f in enumerate(a['fields']):
 name=f['field']
 if name=='prompt-key':
  native={'prompt':q['prompt'],'options':[x['text'] for x in q['answers']],'correctIndex':q['correctIndex'],'key':q['answers'][q['correctIndex']]['text']};literal=[q['prompt'],q['correctIndex'],q['answers'][q['correctIndex']]['text']]
 else:native=literal=q['explanation'] if name=='explanation' else q['answers'][int(name[4:])]['note']
 assert native==f['literal'];nh=sha(compact(native) if isinstance(native,dict) else native.encode());assert nh==f['literalSha256']
 rh=sha(compact(literal) if isinstance(literal,list) else literal.encode())
 proofs=[]
 for ref in f['proofs']:
  m=re.fullmatch(r'source-context.json#sources\[0\].extracts\[(\d+)\]',ref);assert m
  e=b['extracts'][int(m[1])];idx=e['locator']['htmlTextNodeIndex0Based'];quote=parser.nodes[idx]
  proofs.append({**source,'locator':{**e['locator'],'description':e['description']},'exactQuote':quote,'exactQuoteSha256':sha(quote.encode()),'quoteDerivation':'Independent HTMLParser extraction of original response-body text node; script/style excluded, nonempty nodes stripped, entities decoded, document order. Full surrounding section personally read.','authorSourceContextPointer':str(SP)+'#/sources/0/extracts/'+m[1]});bindings+=1
 fields.append({'field':name,'literal':literal,'readerLiteralSha256':rh,'authorNativeLiteral':native,'authorNativeLiteralSha256':nh,'sourceVerdict':'SUPPORTED','editorialVerdict':'PASS','manualSourceAndEditorialReason':reasons[i],'sourceProofs':proofs})
assert len(fields)==6
assert q['source']==a['sourceLiteral'] and sha(compact(q['source']))==a['sourceLiteralSha256']
partners=[]
for topic_id,qid in [('laboratories-measurement','laboratories-measurement-goggles-eye-protection'),('engineering-machines','engineering-machines-safety-goggles')]:
 pp=Path('src/content/topics')/(topic_id+'.json');data=json.loads(pp.read_bytes());item=next(x for x in data['questions'] if x['id']==qid)
 partners.append({'path':str(pp),'currentCard':item,'sortedCardSha256':sha(compact(item,True)),'editorialComparison':'No current031 duplicate: partner tests protective goggles identifying eye protection in a work hazard; current031 tests ventilation/anti-fog function among competing real optical functions, an independent relation. Partner unchanged.','comparisonScope':'Semantic comparison only; partner source truth not certified here.'})
narrow=[]
for pp in Path('src/content/topics').glob('*.json'):
 for item in json.loads(pp.read_bytes())['questions']:
  if re.search(r'запотев|фотохром|вентиляц|периферич.{0,20}обзор',json.dumps(item,ensure_ascii=False),re.I):narrow.append({'path':str(pp),'id':item['id'],'prompt':item['prompt']})
spec=Path('/Users/eaafonasev/Projects/mindbattle-planning/docs/GAME_SPEC.md');lines=spec.read_text().splitlines()
report={'schema':'mindbattle.independent-current031-06c5ea9.reader.v1','scopeIds':['winter-sports-031'],'readerThreadId':READER,'readerIdentityOrigin':'Trusted native CODEX_THREAD_ID execution environment','actualAuthorIdentity':author['authorIdentity'],'independentIdentityVerified':True,'coordinatorDispatchThreadId':'01a12fcd-2bbd-72a3-b127-23455e847ca7','freezeCommit':GIT('rev-parse',FREEZE),'observedHead':GIT('rev-parse','HEAD'),'authorReceiptPath':str(AP),'authorReceiptSha256':sha(AP.read_bytes()),'authorReceiptGitBlob':GIT('hash-object',str(AP)),'authorSourceContextPath':str(SP),'authorSourceContextSha256':sha(SP.read_bytes()),'authorNativeHashRecipesPreservedSeparately':author['hashRecipes'],'readerNativeHashRecipe':'Complete current card SHA256 compact sorted-key UTF8 JSON ensure_ascii=false; grouped prompt-key compact UTF8 [stem,index,key]; notes/explanation exact plain UTF8 without added newline. Author unsorted prompt-key object containing all options is independently derived/verified and retained separately. Original/source quotes exact UTF8 with declared parser extraction.','canonicalCardSha256':cardhash,'difficulty':'easy','correctIndex':2,'wholeCardVerdict':'PASS','checks':{'sourceEntailment':'PASS','easySpec138AdultAudience':'PASS','fourParallelPlausibleUniqueOptions':'PASS','noArtificialLexicalCue':'PASS','wrongNotesOwnFunctionFacts':'PASS','correctNoteUsefulExtra':'PASS','russianGrammar':'PASS','duplicates':'PASS'},'individualFields':fields,'approvedSpecRules':[{'path':str(spec),'line':n,'exactText':lines[n-1]} for n in [138,142,143,144,146]],'honestPersonalReadExtent':'Read current complete six grouped native fields personally. Opened and parsed full 813234-byte original Julbo HTML capture; personally read the complete relevant article text nodes467–525, including product context, protection, visual safety, men/women framing, Lens Types, Lens Treatments, Ventilation, Materials and OTG context. Unrelated full product catalogue/site navigation not claimed as substantive personal review. No old031 PASS inherited.','sourceContextPersonallyRead':[{'htmlTextNodeIndex0Based':i,'text':parser.nodes[i]} for i in range(475,515)],'duplicateReview':{'externalPartners':partners,'narrowCurrentAll110TopicMatches':narrow,'decision':'Only current031 asks ventilation reducing lens fog. Other search matches concern greenhouse/tunnel/cabin ventilation rather than goggles; the two previous eye-protection partner relations are no longer asked. No partner edits.'},'integrityDiagnostics':{'current031CardExactly06c5ea9':True,'groupedCurrentFieldsVerified':6,'sourceLiteralSeparatelyVerifiedNotSeventhGradedField':True,'distinctOriginals':1,'originalBytes':len(raw),'distinctOriginalQuoteNodes':8,'fieldQuoteBindings':bindings,'allRawAndQuotesRoundtripped':True,'rawCaptureDurableInGit':True},'summary':{'fields':6,'sourceSUPPORTED':6,'editorialPASS':6,'editorialFIX':0,'editorialHOLD':0,'wholeCardPASS':1,'wholeCardFIX':0,'wholeCardHOLD':0,'readerCountIncrement':0,'counterFilesEdited':False},'guards':{'runtimeReviewhashCountersPlanningAuthorReceiptsNotEdited':True,'onlyCurrent031ComparedToFreeze':'Whole-topic equality intentionally not asserted because concurrent authorized058 explanation may change.','oldReaderProofsPreserved':True},'validationScope':'Syntax/JSON completeness/native independence/current031 freeze and literal recipes/raw original SHA/Git blob/8 quote-node hashes/own-folder diff only. No full tests/npmQA/contentcheck/build/Player/release/deploy/archive/human acceptance.','cleanup':{'ownedPersistentProcesses':0,'ownedTemporaryDownloadsOrCaches':0,'originalRawSourceRetainedInGit':True,'foreignWorkPreserved':True},'continuation':'Stop at this current031 receipt plus cleanup/handoff; coordinator decides any certification/counter update or subsequent dispatch.'}
(OUT/'independent-current031-whole6.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'card':cardhash,'summary':report['summary'],'bindings':bindings,'originalBytes':len(raw)},ensure_ascii=False))
