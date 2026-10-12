import json,pathlib,subprocess,hashlib,os,re
from html.parser import HTMLParser
ROOT='/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle'
assert subprocess.check_output(['git','rev-parse','--show-toplevel'],text=True).strip()==ROOT
FREEZE='ae39ad3';OUT=pathlib.Path('docs/content-audits/question-quality-wave-6/independent-pilot/resume-2026-10-12-middle-current15-pilot5/winter-current058-ae39ad3')
AUTHOR='docs/content-audits/question-quality-wave-6/winter-sports/resume-2026-10-12-fresh-fix3-remaining15/explanation-precision-058/author-current058-explanation-receipt.json';CTX=str(pathlib.Path(AUTHOR).parent/'source-context.json');TOPIC='src/content/topics/winter-sports.json'
sha=lambda b:hashlib.sha256(b).hexdigest()
native=lambda x:json.dumps(x,ensure_ascii=False,separators=(',',':'),sort_keys=False).encode()
canonical=lambda x:json.dumps(x,ensure_ascii=False,separators=(',',':'),sort_keys=True).encode()
r=json.load(open(AUTHOR));ctx=json.load(open(CTX))
for p in [AUTHOR,CTX]:assert pathlib.Path(p).read_bytes()==subprocess.check_output(['git','show',FREEZE+':'+p])==subprocess.check_output(['git','show','HEAD:'+p])
frozen={c['id']:c for c in json.loads(subprocess.check_output(['git','show',FREEZE+':'+TOPIC]))['questions']};working={c['id']:c for c in json.load(open(TOPIC))['questions']};head={c['id']:c for c in json.loads(subprocess.check_output(['git','show','HEAD:'+TOPIC]))['questions']};c=working['winter-sports-058'];assert c==frozen[c['id']]==head[c['id']]==r['cardAfter']
ac=r['cards'][0];assert sha(canonical(c))==ac['canonicalCardSha256']
class Nodes(HTMLParser):
 def __init__(self):super().__init__();self.nodes=[];self.skip=0
 def handle_starttag(self,t,a):
  if t in ['script','style']:self.skip+=1
 def handle_endtag(self,t):
  if t in ['script','style']:self.skip-=1
 def handle_data(self,d):
  if not self.skip and d.strip():self.nodes.append(d.strip())
src={};texts={};contexts=[]
for m in ctx['sources']:
 p=m['rawCapturePath'];raw=pathlib.Path(p).read_bytes();assert raw==subprocess.check_output(['git','show',FREEZE+':'+p])==subprocess.check_output(['git','show','HEAD:'+p]);assert sha(raw)==m['rawSha256'];blob=subprocess.check_output(['git','hash-object',p],text=True).strip();assert blob==m['gitBlob']
 key='short' if 'short-track' in p else 'long';h=Nodes();h.feed(raw.decode('utf8'));texts[key]=h.nodes
 src[key]={'originalURL':m['originalUrl'],'actualCaptureURL':m['captureUrl'],'actualType':m['captureType'],'rawPath':p,'rawSHA256':sha(raw),'gitBlob':blob,'rawBytes':len(raw),'diskFrozenHEADByteEquality':True,'filteredNodeCount':len(h.nodes),'extractor':'HTMLParser handle_data outside script/style; each nonempty d.strip() appended in document order, 0-based. No original bytes normalized; exact derived per-node text quoted unjoined.'}
 rg=range(55,86) if key=='short' else range(62,98)
 contexts.append({**src[key],'readExtent':'Personally reread entire relevant sport-format overview and neighbouring event labels/distances/paragraphs from full raw original. No old author/reader grades imported.','nodes':[{'index':i,'text':h.nodes[i],'SHA256':sha(h.nodes[i].encode())} for i in rg]})
def proof(k,n):
 t=texts[k];q=t[n]
 return {**src[k],'locator':{'filteredNonemptyHTMLDataNodeIndex0Based':n},'exactQuote':q,'quoteSHA256':sha(q.encode()),'quoteRecipe':'SHA256 UTF8 exact independently derived stripped HTML data node; not raw-file substring; original bytes preserved.','contextBefore':[{'index':i,'text':t[i]} for i in range(max(0,n-2),n)],'contextAfter':[{'index':i,'text':t[i]} for i in range(n+1,min(n+3,len(t)))]}
P=[[('short',67),('short',68),('short',69),('short',70),('short',71),('short',72),('short',73),('short',74),('short',75),('long',75),('long',89),('long',90),('long',91)],[('short',67),('long',75),('long',89),('long',90),('long',91)],[('long',76)],[('short',67)],[('long',75),('long',89),('long',90),('long',91)],[('long',75),('long',94),('long',95),('long',96),('long',97)]]
S=[
 'Short67 explicitly describes111.12m oval marked within international-sized rink, smaller than longtrack. Actual68–75 context identifies500/1000 heats usuallyfour and1500 usuallysix. Long75/89–91 establishes competing400m massstart pack. Both small venue and group format specifically match shorttrack, with no invented exact group count.',
 'Current first sentence now correctly says катка международного размера, matching international-sized rink in short67 without attributing international venue status. Long75 identifies400m for alllong events;89–91 explicitly labelsmassstart and all-at-once racing. Both explanation clauses directly supported by original context.',
 'Long76 expressly says individual distance events race in pairs againstclock. Current note accurately ties this to longtrack individual option and does not make all longtrack events pair races.',
 'Short67 directly states111.12m oval marked on international-sized ice rink. Russian decimal111,12 conveys same length; current text adds no unsupported rink width/length or venue status.',
 'Long75 states400m oval for longtrack events;89/90 identifiesmassstart,91 says allcompetitors on ice atonce. Current note’s pack+standard400m longoval is an explicit combination of two actual source statements.',
 'Long94–97 names bothgender team pursuit and says two teams of3 begin simultaneously on opposite sides. Long75 establishes longoval. Current own pursuit note correctly identifies opposite-side start, without inference about individual lane swaps.']
E=[
 'Actual easy: recognises widely watched shorttrack format from group racing and small in-rink oval. No rare-date/secondary-rule requirement. Four plausible adjacent skatingformats; massstart pack does not fit small markedin-rink oval, pursuit team starts do not fit individual pack. Exactlyonekey, no absurd option or literal key echo. No difficulty change.',
 'Russian now clear and source-precise. Corrected размер qualifier removes previous ambiguity. Main explanation properly contrasts packmassstart longoval and shorttrack smalloval, matching current question and all options. PASS based on fresh reading, not changed-word check alone.',
 'Own longtrack individual option: pair-clock fact is useful distinct information from stem’s pack/smalloval. Not unrelated skating trivia.',
 'Own correct shorttrack option:111.12m length is an independently useful addition beyond prompt/key’s generic smalleroval. Rink-size context may overlap explanation under approved rule; additional length is absent from current prompt/explanation. Clear measuredfact.',
 'Own massstart option:400m longoval venue adds concrete distinction to familiar pack racing. Useful option-specific fact, clear Russian.',
 'Own team pursuit option:opposite sides start is meaningful event-format detail distinct from stem’s shorttrack group. No unrelated collective athlete statistic.']
fields=[]
for i,key in enumerate(['prompt-key','explanation','note0','note1','note2','note3']):
 if i==0:lit={'prompt':c['prompt'],'options':[a['text'] for a in c['answers']],'correctIndex':c['correctIndex'],'key':c['answers'][c['correctIndex']]['text']};b=native(lit);recipe='UTF8 compact unsorted prompt-key dict insertion prompt,options,correctIndex,key; no newline'
 else:lit=c['explanation'] if i==1 else c['answers'][i-2]['note'];b=lit.encode();recipe='UTF8 exact literal string, no JSON quotation/no newline'
 af=next(x for x in ac['fields'] if x['field']==key);assert lit==af['literal'];assert sha(b)==af['literalSha256']
 fields.append({'field':key,'currentLiteral':lit,'nativeLiteralSHA256':sha(b),'nativeRecipe':recipe,'sourceVerdict':'PASS','editorialVerdict':'PASS','verdict':'PASS','manualSourceReason':S[i],'manualEditorialReason':E[i],'actualProofs':[dict(proof(k,n),manualEntailment=S[i]) for k,n in P[i]]})
spec=pathlib.Path('/Users/eaafonasev/Projects/mindbattle-planning/docs/GAME_SPEC.md').read_text().splitlines()
near=[];external=[]
for q in working.values():
 if re.search('шорт.?трек|конькобеж|масс.?старт|длинной дорожк|короткой дорожк',q['prompt']+' '+q['answers'][q['correctIndex']]['text'],re.I):near.append({'id':q['id'],'prompt':q['prompt'],'key':q['answers'][q['correctIndex']]['text'],'role':'semantic partner evidence only;057 not recertified'})
for p in pathlib.Path('src/content/topics').glob('*.json'):
 if p==pathlib.Path(TOPIC):continue
 for q in json.load(open(p))['questions']:
  if re.search('шорт.?трек|конькобеж|масс.?старт|длинной дорожк|короткой дорожк',q['prompt']+' '+q['answers'][q['correctIndex']]['text'],re.I):external.append({'topic':str(p),'id':q['id'],'prompt':q['prompt'],'key':q['answers'][q['correctIndex']]['text']})
report={'readerIdentity':{'nativeThreadId':os.environ['CODEX_THREAD_ID'],'origin':'Actual active native CODEX_THREAD_ID, same independent reader; no new chat/model/agent'},'authorIdentity':r['authorIdentity'],'authorFreeze':FREEZE,'authorReceipt':{'path':AUTHOR,'rawSHA256':sha(pathlib.Path(AUTHOR).read_bytes()),'gitBlob':subprocess.check_output(['git','hash-object',AUTHOR],text=True).strip()},'scope':['winter-sports-058'],'personallyReadCurrentFields':6,'topicPath':TOPIC,'card':{'id':c['id'],'difficulty':c['difficulty'],'authorCanonicalSortedSHA256':sha(canonical(c)),'readerInsertionSHA256':sha(native(c)),'canonicalRecipe':r['hashRecipes']['canonicalCard'],'readerInsertionRecipe':'UTF8 compact json.dumps ensure_ascii=False separators comma/colon sort_keys=False; no newline','wholeSourceVerdict':'PASS','wholeEditorialVerdict':'PASS','wholeVerdict':'PASS','wholeRule':'All6 fresh manually read current fields source+editorialPASS','fields':fields},'sourceReadingContext':contexts,'approvedRules':{'easy':{'path':'/Users/eaafonasev/Projects/mindbattle-planning/docs/GAME_SPEC.md:138','exactQuote':spec[137]},'ownAdditiveNotes':{'path':'/Users/eaafonasev/Projects/mindbattle-planning/docs/GAME_SPEC.md:143','exactQuote':spec[142]}},'semanticCheck':{'current100Count':len(working),'relatedPartners':near,'narrowExternalPartners':external,'analysis':'058 smaller marked-in-rink oval+pack tests different fact from057 pairclocklane format and059 direction. No direct/reverse core fact duplicate found;057 inspected only as partner, not regraded/recounted. No external partner writes.'},'guards':{'current058DiskFrozenHEADRecordEquality':True,'sourceOriginalsDiskFrozenHEADRawByteHashBlobEquality':True,'authorCurrentReceiptDiskFrozenHEADBytesEqual':True,'all6NativeFieldHashesEqualAuthor':True,'canonicalCurrentCardHashEqualsAuthor':True,'originalSourceBytesNotTrimmedOrChanged':True,'oldProofsNotChanged':True,'ownRuntimeCountersSourceAuthorPlanningReviewhashWrites':0,'counterIncrement':0},'summary':{'sourcePASS':6,'sourceFIX':0,'sourceHOLD':0,'editorialPASS':6,'editorialFIX':0,'editorialHOLD':0,'wholePASS':1},'checks':'JSON syntax, fresh current6 literals/card hashes, complete original source disk/frozen/HEAD bytes+SHA/blob, independent node quotes, semantic neighbours, own whitespace/scope diff. No full/npmQA/contentcheck/build/Player/browsergame/release/deploy/acceptance.','cleanup':{'ownedProcesses':0,'ownIgnoredUntrackedAfterCommit':0,'sourceOriginalsGitDurable':True,'sharedGitForeignWorkPreserved':True},'nextStep':'Coordinator performs paired binding/counter decision separately. Reader stops after committed receipt/cleanup; no057 recertification or counter mutation.'}
assert report['readerIdentity']['nativeThreadId']!=r['authorIdentity']['nativeThreadId']
(OUT/'reader-receipt.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');(OUT/'current-card-canonical.json').write_bytes(canonical(c)+b'\n');(OUT/'current-card-insertion.json').write_bytes(native(c)+b'\n')
print(report['summary']);print('Canonical',sha(canonical(c)),'Insertion',sha(native(c)))
