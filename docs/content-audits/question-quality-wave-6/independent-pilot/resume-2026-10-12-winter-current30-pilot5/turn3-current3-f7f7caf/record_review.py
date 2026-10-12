"""Store current manual findings. Integrity code derives hashes/quotes, not quality verdicts."""
import hashlib,json,os,re,subprocess
from pathlib import Path
from pypdf import PdfReader
ROOT=Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle')
assert Path.cwd()==ROOT
GIT=lambda *a:subprocess.check_output(['git',*a],text=True).strip()
assert GIT('rev-parse','--show-toplevel')==str(ROOT)
OUT=Path(__file__).parent
AUTHOR_COMMIT='f7f7caf03f6f67739437d79ada7a4facf6966b6f'
BASE=Path('docs/content-audits/question-quality-wave-6/winter-sports/resume-2026-10-12-fresh-fix3-remaining15')
AP=BASE/'author-current3-receipt-v2.json';SP=BASE/'source-context-v2.json'
author=json.loads(AP.read_bytes());source_context=json.loads(SP.read_bytes())
for p in [AP,SP]:assert p.read_bytes()==subprocess.check_output(['git','show',AUTHOR_COMMIT+':'+str(p)])
assert os.environ['CODEX_THREAD_ID']=='01a12f52-6e07-7ac3-a9e1-d063b8afd3cf'
assert author['authorIdentity']['nativeThreadId']=='01a12f7f-61a0-7062-904d-bbbb787deefc'
assert os.environ['CODEX_THREAD_ID']!=author['authorIdentity']['nativeThreadId']
sha=lambda b:hashlib.sha256(b).hexdigest()
compact=lambda v,sort=False:json.dumps(v,ensure_ascii=False,sort_keys=sort,separators=(',',':')).encode()
TOPIC='src/content/topics/winter-sports.json';topic_bytes=Path(TOPIC).read_bytes();topic=json.loads(topic_bytes)
frozen=json.loads(subprocess.check_output(['git','show',AUTHOR_COMMIT+':'+TOPIC]))
sources={};pages={}
for b in source_context['sources']:
 p=b['rawCapturePath']
 if p in sources:continue
 raw=Path(p).read_bytes();blob=GIT('hash-object',p)
 assert sha(raw)==b['rawSha256'] and blob==b['gitBlob']
 assert GIT('ls-files',p)==p and subprocess.check_output(['git','cat-file','blob',blob])==raw
 sources[p]={'originalUrl':b['originalUrl'],'actualCaptureUrl':b['captureUrl'],'rawType':b['captureType'],'rawPath':p,'rawSha256':sha(raw),'gitBlob':blob,'rawSizeBytes':len(raw),'durableTrackedOriginal':True}
 # Parse complete captures; retain relevant original page text without altering any capture.
 reader=PdfReader(p);numbers={e['locator']['pdfPhysicalPage1Based'] for entry in source_context['sources'] if entry['rawCapturePath']==p for e in entry['extracts']}
 pages[p]={n:reader.pages[n-1].extract_text() for n in numbers}
reasons={
'030':[
'The complete Hockey Canada facial-protector page expressly labels visor a partial protector shielding only the eyes. It lists wire cage, high-impact polycarbonate shield and their combination as three full-face styles. Unlike the earlier mask umbrella category, the current four style names form the intended partial/full contrast with a unique key. Familiar visor coverage is suitable easy knowledge for the large hockey-viewing/helmet-using adult group; the question does not require the CSA table.',
'The original partial-eye versus three-full-face-style distinction directly supports both sentences. The old disjoint mask/cage assertion is absent. Two grammatical sentences clearly give the reason for the key.',
'The original explicitly includes wire cage among the three full-face styles. This own-alternative coverage fact explains its distinction from the partial eye protector.',
'The table explicitly associates eye protectors/visors for people aged 18 or older with C or 4 and Yellow CSA sticker. The note qualifies the classification to Hockey Canada, so it does not claim a universal world age policy. Age/category/sticker are useful verified extra facts beyond the prompt asking coverage.',
'The original explicitly includes high-impact polycarbonate shield as a full-face style. Material and full-face classification belong to this particular alternative, not to a different type.',
'The original explicitly includes a combination of wire cage and polycarbonate shield among the full-face styles. This own-style fact makes the combined protector useful context rather than a stray helmet fact.'],
'031':[
'FIS 3.7 directly supports the eye-protection key. The editorial problem is the actual current distractors: glasses protecting hands or shin are obviously impossible, while head is a broader area containing eyes. An adult can discard hands/shin without knowing alpine equipment. GAME_SPEC line138 explicitly requires plausible wrong options even for easy. FIX prompt/options at the preserved level/key slot; no difficulty reclassification or technical-term HOLD. Narrow external comparison also finds inverse eyes–protective-glasses cards in laboratories-measurement and engineering-machines; this wording asks no skiing-specific distinction beyond the same basic function.',
'FIS 3.7 explicitly states eye protection against weather/rays, optically correct lenses and good visibility in all weather. The new explanation says good visibility and no longer asserts contrast vision. The lens characteristic is part of the FIS definition; no unsupported optical performance metric is added. Two grammatical sentences.',
'FIS 3.6.1 explicitly requires crash helmets at all FIS alpine events and event-specific safety standards. A helmet is ordinary head protection; that body-to-equipment relation connects this fact to the head alternative. This is a useful sport-specific head-protection fact, not unrelated equipment trivia, although it does not make head a strong distractor in the prompt.',
'FIS 3.8 explicitly describes gloves as protective covering against weather and external forces. Gloves are hand equipment by ordinary lexical meaning. That directly connects the note to hands; the neighboring-section introduction is unnecessary but accurate and does not invalidate the useful own-option fact.',
'Optically correct lenses are expressly stated in 3.7 and supplement the prompt asking which body part is protected. The note can repeat this detail from explanation under GAME_SPEC line143; it is not just eyes from prompt/key.',
'FIS 3.5.4 explicitly forbids additional rigid parts worn as shin pads inside the boot; the adjacent medical exception concerns soft flexible padding, not rigid shields. The current note is specifically about shin protection in boots, so it is a relevant own-body-part fact, not a general skiing fact.'],
'032':[
'The complete shin-pad page states knee down to top of skate. Top of skate uniquely matches the full lower endpoint; midpoint shin and lower kneecap stop short, and ankle is a different anatomical reference from boot top. Four location alternatives remain comparable. Familiar coverage/fit is suitable easy knowledge.',
'The complete page expressly supports knee-to-skate coverage and knee centered in the donut. Two concise grammatical sentences accurately explain the fit.',
'The source states the two coverage endpoints. The current note explicitly marks midpoint-in-range as an inference from those endpoints, not a verbatim Hockey Canada midpoint rule. This simple anatomical inference is valid and useful: it concerns the named midpoint and shows it is an interior point, not the lower boundary. The old unrelated sock/shorts fact has been removed.',
'The original explicitly gives about two finger widths between foot top and pad bottom. This is a useful precise lower-fit detail connected to the ankle/foot-region alternative; no unsupported distance in centimetres is asserted.',
'The original explicitly says knee comfortably in the central donut. This is a kneecap-related placement fact for that alternative, not a claim that the pad ends below the kneecap.',
'The original explicitly requires snug but comfortable straps and no slipping. This secure-fit fact adds information beyond the prompt asking the lower endpoint.']}
reference_count=0
cards=[]
for a in author['cards']:
 q=next(x for x in topic['questions'] if x['id']==a['questionId']);old=next(x for x in frozen['questions'] if x['id']==q['id']);assert q==old
 short=q['id'][-3:];native=sha(compact(q));sorted_hash=sha(compact(q,True))
 assert native==a['cardCanonicalSha256'] and sorted_hash==a['sortedCardSha256']
 fields=[]
 for i,f in enumerate(a['fields']):
  name=f['field']
  if name=='prompt-key':
   author_literal={'prompt':q['prompt'],'options':[x['text'] for x in q['answers']],'correctIndex':q['correctIndex'],'key':q['answers'][q['correctIndex']]['text']}
   literal=[q['prompt'],q['correctIndex'],q['answers'][q['correctIndex']]['text']]
  else:author_literal=literal=q['explanation'] if name=='explanation' else q['answers'][int(name[4:])]['note']
  assert author_literal==f['literal']
  author_lh=sha(compact(author_literal) if isinstance(author_literal,dict) else author_literal.encode());assert author_lh==f['literalSha256']
  reader_lh=sha(compact(literal) if isinstance(literal,list) else literal.encode())
  proofs=[]
  for ref in f['proofs']:
   match=re.fullmatch(r'source-context-v2.json#sources\[(\d+)\].extracts\[(\d+)\]',ref);assert match
   b=source_context['sources'][int(match[1])];e=b['extracts'][int(match[2])];p=b['rawCapturePath'];loc=e['locator'];n=loc['pdfPhysicalPage1Based'];quote=pages[p][n]
   assert sha(e['exactQuote'].encode())==e['exactQuoteSha256'] and e['exactQuote'] in quote
   proofs.append({**sources[p],'locator':loc,'exactQuote':quote,'exactQuoteSha256':sha(quote.encode()),'quoteDerivation':'Independent exact pypdf original-page extraction with whitespace retained; complete page gives author-excerpt context.','authorExcerptSha256':e['exactQuoteSha256'],'authorSourceContextPointer':str(SP)+'#/sources/'+match[1]+'/extracts/'+match[2]});reference_count+=1
  fields.append({'field':name,'literal':literal,'readerLiteralSha256':reader_lh,'authorNativeLiteral':author_literal,'authorNativeLiteralSha256':author_lh,'sourceVerdict':'SUPPORTED_BY_EXPLICIT_ENDPOINTS_WITH_DECLARED_INFERENCE' if (short,name)==('032','note0') else 'SUPPORTED','editorialVerdict':'FIX' if (short,name)==('031','prompt-key') else 'PASS','manualSourceAndEditorialReason':reasons[short][i],'sourceProofs':proofs})
 cards.append({'questionId':q['id'],'difficulty':q['difficulty'],'correctIndex':q['correctIndex'],'authorNativeUnsortedCardSha256':native,'readerSortedCardSha256':sorted_hash,'currentExactlyMatchesF7f7caf':True,'wholeCardVerdict':'FIX' if short=='031' else 'PASS','checks':{'sourceEntailment':'PASS','difficulty':'PASS (easy retained; known fact appropriate)','parallelPlausibleUniqueOneKey':'FIX (hands and shin implausible for goggles)' if short=='031' else 'PASS','noArtificialLexicalCue':'PASS (no copied eye word in stem; semantic obviousness separately flagged)','ownWrongNotes':'PASS','correctNoteUsefulExtra':'PASS','russianGrammar':'PASS','duplicates':'FIX (inverse glasses-eye protective relation external partners)' if short=='031' else 'PASS'},'individualFields':fields})
assert len(cards)==3 and sum(len(c['individualFields']) for c in cards)==18
partners=[]
for topic_id,qid,decision in [('laboratories-measurement','laboratories-measurement-goggles-eye-protection','031 inverse basic protective-glasses→eyes relation. Chemicals instead of weather changes hazard context but current031 asks no independent skiing detail; flagged meaningful duplicate, no partner edit.'),('engineering-machines','engineering-machines-safety-goggles','031 inverse protective-glasses→eyes relation. Workshop chips instead of weather gives another context for the same directly asked function; flagged meaningful duplicate, no partner edit.'),('combat-sports','combat-sports-023','No duplicate with032: body-region identification differs from precise hockey-pad lower endpoint.'),('motorsport','motorsport-b3-e09','No duplicate with current030: helmet/head protection differs from partial-versus-full facial protector. Current031 head note is supporting context, not a helmet prompt/key.')]:
 p=Path('src/content/topics')/(topic_id+'.json');data=json.loads(p.read_bytes());q=next(x for x in data['questions'] if x['id']==qid)
 partners.append({'path':str(p),'topicFileSha256':sha(p.read_bytes()),'card':q,'sortedCardSha256':sha(compact(q,True)),'manualDuplicateDecision':decision,'partnerEdited':False,'comparisonScope':'Semantic current-card comparison only; not a factual certification of partner sources.'})
spec=Path('/Users/eaafonasev/Projects/mindbattle-planning/docs/GAME_SPEC.md');lines=spec.read_text().splitlines()
report={'schema':'mindbattle.independent-winter-turn3-current3.reader.v1','scopeIds':author['scopeExactIds'],'scopeMeaning':'3 current cards ×6 fields =18 fields. Other15 frozen cards are not independently reviewed or counted in this receipt.','readerThreadId':os.environ['CODEX_THREAD_ID'],'readerIdentityOrigin':'Trusted native CODEX_THREAD_ID environment','authorIdentitySuppliedByCoordinatorNativeCreateWait':author['authorIdentity'],'independentIdentityVerified':True,'authorReceiptPath':str(AP),'authorReceiptSha256':sha(AP.read_bytes()),'sourceContextPath':str(SP),'sourceContextSha256':sha(SP.read_bytes()),'authorReceiptCommit':AUTHOR_COMMIT,'observedHead':GIT('rev-parse','HEAD'),'authorNativeHashRecipesPreservedSeparately':author['hashRecipes'],'readerNativeHashRecipe':'Complete card: SHA256 compact UTF8 JSON sorted keys ensure_ascii=false; prompt-key: compact array [stem,index,key], options retained in separately preserved author-native prompt object; notes/explanation exact plain UTF8; no added newline. Author native unsorted card and native prompt object hashes independently derived and separately verified.','approvedSpecRules':[{'path':str(spec),'line':n,'exactText':lines[n-1]} for n in [138,142,143,144,146]],'personalSourceRead':'Current18 field literals personally reread from current JSON. Complete original PDF captures opened; cited complete original pages and adjacent source contexts personally read, not merely author quote lists/old grades. Fresh receipt is v2 f7f7caf, not old c14 receipt.','sourceContextsPersonallyRead':{'hockeycanada-facial-protectors.pdf':'physical/printed79–81; partial/full styles, intended age/type/yellow CSA table, adjacent mask nomenclature and fitting','fis-equipment-2026-10-08.pdf':'physical/printed32–35; cut-resistant equipment context,3.5.4 rigid/soft shin pads,3.6.1 compulsory helmets/event standards,3.7 goggles,3.8 gloves','hockeycanada-player-equipment-guide.pdf':'physical4–6 (printed unnumbered); Jock/Jill context, complete Shin Pads page5, Socks page6'},'cards':cards,'duplicateReview':{'method':'Narrow current all110 topic JSON search and full current literals of four relevant external partners; current Winter100 prompt context retained for continuity.','winterTopicObservedSha256':sha(topic_bytes),'currentWinterPromptSnapshot':[{'id':q['id'],'prompt':q['prompt']} for q in topic['questions']],'externalPartners':partners,'nearbyWinter':'030 now tests partial eye versus full-face styles, distinct from029 chinstrap fastening.032 lower pad endpoint differs from combat-sports body-region question.031 current rewrite newly collapses to the basic goggles-eye function; source verification and sports wording do not remove the external inverse-relation defect.'},'integrityDiagnostics':{'authorSourceReferencesRoundtripped':reference_count,'distinctDurableOriginalPDFs':len(sources),'currentNativeAndSortedCardHashesVerified':3,'currentAuthorNativeAndReaderFieldHashesVerified':18,'exactOriginalSourceExcerptSubstringChecks':True},'summary':{'cards':3,'fields':18,'sourceSUPPORTED':18,'editorialPASS':17,'editorialFIX':1,'editorialHOLD':0,'wholeCardPASS':2,'wholeCardFIX':1,'wholeCardHOLD':0,'sourceCounterAtDispatch':470,'readerCountIncrement':0,'counterFilesEdited':False},'guards':{'onlyOwnNewFolderEdits':True,'runtimeReviewHashesPlanningCountersAuthorReceiptsNotEdited':True,'remaining15NotReviewedOrCounted':True,'oldReaderReportsImmutable':True,'IDsEasyKeySlots1_2_3AnswerOrderPreserved':True,'other97RuntimeCardsUntouchedByReader':True},'checksScope':'Syntax, evidence completeness/native identity, exact frozen3 literals/native and reader recipes/source SHA and durable Git blobs/quote locators, own-folder diff only. No full tests/npmQA/contentcheck/build/Player/release/deploy/archive/human acceptance.','cleanup':{'ownedTemporaryDownloadsOrCaches':0,'ownedPersistentProcesses':0,'originalSourcesDurableInExistingGit':True,'foreignWorkPreserved':True},'nextStep':'Coordinator may authorize bounded031 repair preserving easy/key slot2, then exact-current rereview. No independent work on remaining15 without coordinator dispatch.'}
(OUT/'independent-reader-current18.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'summary':report['summary'],'sourceReferences':reference_count,'rawOriginals':len(sources),'cards':[(c['questionId'],c['wholeCardVerdict'],c['readerSortedCardSha256'],c['authorNativeUnsortedCardSha256']) for c in cards]},ensure_ascii=False))
