import json,hashlib,pathlib,subprocess,os,re
from html.parser import HTMLParser
ROOT='/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle'
assert subprocess.check_output(['git','rev-parse','--show-toplevel'],text=True).strip()==ROOT
FREEZE='fc2e8ffb350a98d595c5f0710127d80ca34c4916'
OUT=pathlib.Path('docs/content-audits/question-quality-wave-6/independent-pilot/resume-2026-10-12-middle-current15-pilot5/winter-current2-fc2e8ff')
AUTHOR='docs/content-audits/question-quality-wave-6/winter-sports/resume-2026-10-12-fresh-fix3-remaining15/source-only-057058/author-source-only-receipt-v2.json'
CONTEXT=str(pathlib.Path(AUTHOR).parent/'source-context.json')
sha=lambda b:hashlib.sha256(b).hexdigest()
native=lambda x:json.dumps(x,ensure_ascii=False,separators=(',',':'),sort_keys=False).encode()
canon=lambda x:json.dumps(x,ensure_ascii=False,separators=(',',':'),sort_keys=True).encode()
r=json.load(open(AUTHOR));meta=json.load(open(CONTEXT));assert pathlib.Path(AUTHOR).read_bytes()==subprocess.check_output(['git','show',FREEZE+':'+AUTHOR])
assert pathlib.Path(CONTEXT).read_bytes()==subprocess.check_output(['git','show',FREEZE+':'+CONTEXT])
TOPIC='src/content/topics/winter-sports.json';frozenbytes=subprocess.check_output(['git','show',FREEZE+':'+TOPIC]);cards={c['id']:c for c in json.loads(frozenbytes)['questions']};working={c['id']:c for c in json.load(open(TOPIC))['questions']}
scope=['winter-sports-057','winter-sports-058'];assert all(cards[k]==working[k] for k in scope)
for g in r['runtimeMutation']['protectedOther99']:assert sha(canon(cards[g['id']]))==g['sha256']
class Nodes(HTMLParser):
 def __init__(self):super().__init__();self.nodes=[];self.skip=0
 def handle_starttag(self,t,a):
  if t in ['script','style']:self.skip+=1
 def handle_endtag(self,t):
  if t in ['script','style']:self.skip-=1
 def handle_data(self,d):
  if not self.skip and d.strip():self.nodes.append(d.strip())
sources={};nodes={};sourceManifest=[]
for m in meta['sources']:
 p=m['rawCapturePath'];b=pathlib.Path(p).read_bytes();assert b==subprocess.check_output(['git','show',FREEZE+':'+p]);assert sha(b)==m['rawSha256'];assert subprocess.check_output(['git','hash-object',p],text=True).strip()==m['gitBlob']
 key='short' if 'short-track.html' in p else 'long';h=Nodes();h.feed(b.decode('utf8'));nodes[key]=h.nodes
 sources[key]={'originalURL':m['originalUrl'],'actualCaptureURL':m['captureUrl'],'actualType':m['captureType'],'sourceClass':m['sourceClass'],'rawPath':p,'rawSHA256':sha(b),'gitBlob':m['gitBlob'],'rawBytes':len(b),'GitDurableAt':FREEZE,'nodeCount':len(h.nodes),'extractor':'Python html.parser.HTMLParser; ignore script/style handle_data; append each nonempty d.strip() node in document order. Preserve per-node text, punctuation and case; no concatenated quotation.'}
 selection=list(range(55,86)) if key=='short' else list(range(62,98))
 sourceManifest.append({**sources[key],'readExtent':'Personally read complete sport-format overview and surrounding event headings, distances/heats and complete event paragraphs in actual full original. Canadian athlete historical profiles not used as rule proof.','readNodes':[{'index0Based':i,'exactText':h.nodes[i],'SHA256':sha(h.nodes[i].encode())} for i in selection]})
(OUT/'source-reading-context.json').write_text(json.dumps(sourceManifest,ensure_ascii=False,indent=2)+'\n')
def proof(key,i):
 q=nodes[key][i]
 return {**sources[key],'locator':{'filteredNonemptyHTMLDataNodeIndex0Based':i},'exactExtractQuote':q,'quoteSHA256':sha(q.encode()),'quoteRecipe':'SHA256 UTF8 exact stripped node string returned by independent filtered HTMLParser; raw original unchanged.','adjacentBefore':[{'index':n,'text':nodes[key][n]} for n in range(max(0,i-2),i)],'adjacentAfter':[{'index':n,'text':nodes[key][n]} for n in range(i+1,min(i+3,len(nodes[key])))]}
# Source selection comes from this reader's direct full-context reading, not author proof lists.
P=[[('long',76),('short',67),('short',68),('short',69),('short',70),('short',71),('short',72),('long',89),('long',90),('long',91),('long',94),('long',95),('long',96),('long',97)], [('long',76)],[('long',76)],[('short',67),('short',68),('short',69),('short',70),('short',71),('short',72)],[('long',75),('long',89),('long',90),('long',91)],[('long',94),('long',95),('long',96),('long',97)], [('short',67),('short',68),('short',69),('short',70),('short',71),('short',72),('long',75),('long',89),('long',90),('long',91)], [('short',67),('long',75),('long',89),('long',90),('long',91)], [('long',76)],[('short',67)],[('long',75),('long',89),('long',90),('long',91)],[('long',75),('long',94),('long',95),('long',96),('long',97)]]
S=[
 'Long node76 directly states individual distance events, pairs against clock, once-per-lap lane change. Short context68–72 identifies500/1000m heats with usuallyfour; long89–91 pack massstart and94–97 two3-skater pursuit teams establish distinct alternatives. Only key matches all3 stem features.',
 'Long76 explicitly states racing pairs against clock and lane changes to equalize distance. Current explanation accurately states purpose rather than invented timing benefit.',
 'Long76 expressly grants right-of-way to outside-lane skater when both reach crossover together. Current correct note includes same condition and rule, not broad unconditional outside-lane priority.',
 'Short67 gives smaller111.12m oval compared with long track; joined contextual nodes68–72—not detached node72 alone—identify500/1000m usuallyfour-at-time races. Current broad simultaneous-racing statement is supported, no all-distance four-skater assertion.',
 'Long75 states all long events400m oval;89/90 identify mass start;91 says all competitors on ice at same time. Both pack and long-oval clauses directly supported.',
 'Long94–97 names team pursuit, gives two teams of3 simultaneously starting on opposite sides. Exact current note appropriately states team size and opposite starts.',
 'Short67 identifies oval marked within international-sized rink, with smaller size;68–72 and73–75 show multiple skaters together. Long75 and89–91 distinguish400m pack massstart. Venue+group cues yield unique short-track key.',
 'FIX precision: short67 says international-sized ice rink, referring to rink SIZE. Current explanation says внутри международного катка, omitting размера and assigning international adjective to venue itself. Full original does not establish international venue status. Massstart group and long oval clause otherwise directly supported by75/89–91. Frozen status is not quality proof.',
 'Long76 directly describes individual distances in pairs against clock. This own long-distance option fact remains distinct from prompt’s short oval/group racing.',
 'Short67 directly gives111.12m oval marked on international-sized rink. Current new note preserves decimal in Russian111,12 and size qualifier; it does not invent rink width/length or international competition status.',
 'Long75 supports400m standard long-track oval and89–91 identifymassstart/all-at-once. Statement combines actual two explicit pieces, not dimension inference from source title.',
 'Long75 establishes longoval for alllong events;94–97 expressly shows teams begin from opposite sides. Current note does not imply paired individual time trial or shorttrack pursuit.']
E=[
 'Actual easy: familiar television/Olympic longtrack format from pair/clock/lane combination; no rare numerical/regulation recall. Four parallel plausible skating formats, none nonsense, one key. No repeated label or isolated Russian term trap.',
 'Russian clear; main explanation may repeat asked facts and explains equal-distance reason. No unsupported rule and no accidental alternative key.',
 'Own correct option and useful crossover right-of-way detail beyond prompt/key. Condition simultaneous arrivals retained; approved additive-note requirement met.',
 'Own shorttrack alternative: simultaneous pack and smalleroval helpful defining fact beyond paired-time-trial question. Plain Russian.',
 'Own massstart alternative: pack on longoval distinguishes it from paired individual distances and shorttrack. Useful fact rather than generic group trivia.',
 'Own pursuit option: three-person/opposite-start facts add concrete teamformat knowledge. Clear grammatical note.',
 'Actual easy: shorttrack recognizable from small in-rink oval and pack. Longtrack individual, massstart and pursuit are plausible adjacent formats; massstart pack alone does not fit smaller in-rink oval. Distinct from057 pairedclocklane fact; not direct/reverse of same association.',
 'FIX Russian/source precision: международный каток is not same precise meaning as каток международного размера. Replace with размер phrase or simply катка if source-compatible within newly authorized scope. This current frozen explanation stays unmodified; source-backed sport contrast otherwise clear.',
 'Own longtrack individual option fact explains paired-clock format unlike shorttrack pack; meaningful and clear.',
 'Own correct shorttrack option now adds measured oval111.12m beyond prompt’s generic smalleroval cue. New size phrase accurate; additive content fulfilled even if broad rink context overlaps explanation.',
 'Own massstart option adds400m dimension and longoval venue, directly useful contrasting packformats. Clear.',
 'Own pursuit option provides opposite-side start rather than unrelated skating statistic; relevant plain Russian.']
rows=[]
for ci,k in enumerate(scope):
 c=cards[k];ac=next(x for x in r['cards'] if x['questionId']==k);assert sha(canon(c))==ac['canonicalCardSha256'];fields=[]
 for fi,key in enumerate(['prompt-key','explanation','note0','note1','note2','note3']):
  if fi==0:lit={'prompt':c['prompt'],'options':[a['text'] for a in c['answers']],'correctIndex':c['correctIndex'],'key':c['answers'][c['correctIndex']]['text']};bytes_=native(lit);recipe='UTF8 compact unsorted prompt-key JSON insertion order prompt,options,correctIndex,key; no newline'
  else:lit=c['explanation'] if fi==1 else c['answers'][fi-2]['note'];bytes_=lit.encode();recipe='UTF8 exact current field string; no JSON quoting/no newline'
  af=next(x for x in ac['fields'] if x['field']==key);assert af['literal']==lit;assert sha(bytes_)==af['literalSha256'];ix=ci*6+fi;v='FIX' if ix==7 else 'PASS'
  fields.append({'field':key,'currentLiteral':lit,'authorNativeLiteralSHA256':sha(bytes_),'authorNativeLiteralRecipe':recipe,'sourceVerdict':v,'editorialVerdict':v,'verdict':v,'manualSourceAnalysis':S[ix],'manualEditorialAnalysis':E[ix],'actualProofs':[dict(proof(s,n),manualEntailment=S[ix]) for s,n in P[ix]]})
 rows.append({'id':k,'difficulty':c['difficulty'],'wholeVerdict':'PASS' if ci==0 else 'FIX','wholeVerdictRule':'All6 current fields must pass both source and editorial; frozen field is still read/graded','authorCanonicalCardSHA256':sha(canon(c)),'readerInsertionCardSHA256':sha(native(c)),'fields':fields})
# Narrow current100/catalog neighbour evidence, no partner mutations.
related=[];external=[];rx=re.compile('шорт.?трек|конькобеж|масс.?старт|длинной дорожк|короткой дорожк|преследован',re.I)
for c in working.values():
 if rx.search(c['prompt']+' '+c['answers'][c['correctIndex']]['text']):related.append({'id':c['id'],'prompt':c['prompt'],'key':c['answers'][c['correctIndex']]['text'],'nativeSHA256':sha(native(c))})
for p in pathlib.Path('src/content/topics').glob('*.json'):
 if p==pathlib.Path(TOPIC):continue
 for c in json.load(open(p))['questions']:
  if re.search('шорт.?трек|конькобеж|масс.?старт|длинной дорожк|короткой дорожк',c['prompt']+' '+c['answers'][c['correctIndex']]['text'],re.I):external.append({'topic':str(p),'id':c['id'],'prompt':c['prompt'],'key':c['answers'][c['correctIndex']]['text'],'nativeSHA256':sha(native(c))})
spec=pathlib.Path('/Users/eaafonasev/Projects/mindbattle-planning/docs/GAME_SPEC.md').read_text().splitlines()
report={'readerIdentity':{'nativeThreadId':os.environ['CODEX_THREAD_ID'],'origin':'Actual current native CODEX_THREAD_ID, same independent reader, no old otherWinter reader imported'},'authorIdentity':r['authorIdentity'],'sourceCurrentAuthorFreeze':FREEZE,'authorReceipt':{'path':AUTHOR,'rawSHA256':sha(pathlib.Path(AUTHOR).read_bytes()),'gitBlob':subprocess.check_output(['git','hash-object',AUTHOR],text=True).strip()},'scope':scope,'topicPath':TOPIC,'frozenTopicRawSHA256':sha(frozenbytes),'hashRecipes':{'authorCard':r['hashRecipes']['canonicalCard'],'authorField':r['hashRecipes']['fieldLiteral'],'readerCard':'UTF8 compact JSON, ensure_ascii=False sort_keys=False; author canonical sorted recipe retained separately'},'sources':sourceManifest,'cards':rows,'approvedRules':{'easy':{'path':'/Users/eaafonasev/Projects/mindbattle-planning/docs/GAME_SPEC.md:138','exactQuote':spec[137]},'notes':{'path':'/Users/eaafonasev/Projects/mindbattle-planning/docs/GAME_SPEC.md:143','exactQuote':spec[142]}},'semanticNeighbourCheck':{'currentCount':len(working),'currentNeighbours':related,'externalMatches':external,'assessment':'057 pairs/time/lane changes,058 smaller in-rink oval+pack,059 direction are separate tested facts. Biathlon pursuit/massstart facts are independent discipline facts. No direct/reverse same fact found in narrow catalog partners; no external partner changed.'},'specificFinding':{'card':'winter-sports-058','field':'explanation','currentLiteral':cards['winter-sports-058']['explanation'],'sourceNode':67,'defect':'international-sized is rink-size qualifier, current международного катка omits size and risks venue-status meaning. Correct note1 does not repair frozen explanation. Only precise explanation-language fix required; no easy HOLD or reclassification.'},'guards':{'all12CurrentAuthorNativeFieldHashesMatch':True,'all2CurrentAuthorCanonicalCardHashesMatch':True,'current2WorkingRecordsEqualFreeze':True,'protected99FrozenCanonicalHashesMatch':True,'protected99WorkingChangesByOtherActors':[g['id'] for g in r['runtimeMutation']['protectedOther99'] if sha(canon(working[g['id']]))!=g['sha256']],'twoCompleteRawHTMLByteSHAAndBlobEqualFreeze':True,'independentNodeQuotesExact':True,'ownRuntimeSourceAuthorPlanningCounterReviewhashWrites':0,'sourceCounterBefore':472,'sourceCounterIncrement':0},'summary':{'fields':12,'source':{'PASS':11,'FIX':1,'HOLD':0},'editorial':{'PASS':11,'FIX':1,'HOLD':0},'wholeCards':{'PASS':1,'FIX':1,'HOLD':0}},'checks':'Native literal/current2/card/source/node hashes, JSON syntax and own Git diff whitespace/scope. No fulltests/npmQA/content-check/build/Player/browsergame/release/deploy/human acceptance.','cleanup':{'ownUntrackedIgnoredAfterCommit':0,'ownedBackgroundProcesses':0,'rawOriginalsGitDurable':True,'foreignWIPPreserved':True},'nextStep':'Coordinator decides precise authorization to correct058 frozen explanation and requests actual new author/reader binding if approved. PASS057 alone causes0 count increment. Same reader remains available; no further work dispatched.'}
assert report['readerIdentity']['nativeThreadId']!=r['authorIdentity']['nativeThreadId']
(OUT/'author-canonical-cards.json').write_bytes(canon([cards[k] for k in scope])+b'\n');(OUT/'reader-insertion-cards.json').write_bytes(native([cards[k] for k in scope])+b'\n')
(OUT/'reader-receipt.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(report['summary']);print([(x['id'],x['authorCanonicalCardSHA256'],x['readerInsertionCardSHA256']) for x in rows])
