import json,hashlib,subprocess,os,re,pypdf
from pathlib import Path
from html.parser import HTMLParser
from pypdf import PdfReader
ROOT='/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle';assert subprocess.check_output(['git','rev-parse','--show-toplevel'],text=True).strip()==ROOT
assert pypdf.__version__=='6.19.0'
OUT=Path(__file__).parent;AUTHOR='docs/content-audits/question-quality-wave-6/middle-ages/resume-2026-10-12-current-fix3-indulgence-reconquista-jihad/author-sourcebound-freeze-v4-01a12fe9.json';FREEZE='b420f9b';RUNTIME='88c84f4'
sha=lambda b:hashlib.sha256(b).hexdigest();nat=lambda x:json.dumps(x,ensure_ascii=False,separators=(',',':'),sort_keys=False).encode();can=lambda x:json.dumps(x,ensure_ascii=False,separators=(',',':'),sort_keys=True).encode();git=lambda r,p:subprocess.check_output(['git','show',r+':'+p])
a=json.loads(Path(AUTHOR).read_bytes());assert Path(AUTHOR).read_bytes()==git(FREEZE,AUTHOR);TOPIC=a['topicPath'];scope=a['scopeIds']
load=lambda b:{c['id']:c for c in json.loads(b)['questions']}
frozen=load(git(RUNTIME,TOPIC));working=load(Path(TOPIC).read_bytes());head=load(git('HEAD',TOPIC));baseline=load(git(a['baselineFreeze'],TOPIC))
assert all(frozen[k]==working[k]==head[k]==next(x['currentRecord'] for x in a['records'] if x['id']==k) for k in scope)
protected=[k for k in baseline if k not in scope];assert len(protected)==97;assert all(baseline[k]==frozen[k] for k in protected)
class H(HTMLParser):
 def __init__(self):super().__init__();self.nodes=[];self.skip=0
 def handle_starttag(self,t,a):
  if t in ('script','style'):self.skip+=1
 def handle_endtag(self,t):
  if t in ('script','style'):self.skip-=1
 def handle_data(self,s):
  if not self.skip and s.strip():self.nodes.append(s.strip())
raws={};sources=[];pageTexts={};extractions=[];contexts=[]
for s in a['completeOriginalSources']:
 p=s['path'];b=Path(p).read_bytes();assert b==git(FREEZE,p)==git('HEAD',p);assert sha(b)==s['rawSHA256'];assert subprocess.check_output(['git','hash-object',p],text=True).strip()==s['gitBlob'];raws[p]=b
 rec={'path':p,'originalURL':s['url'],'captureURL':s['url'],'URLBasis':'Preserved original resource/landing URL from source register. No live replacement or inferred redirect.','rawSHA256':sha(b),'GitBlob':s['gitBlob'],'bytes':len(b),'diskFreezeHEADEqual':True,'durableAt':FREEZE,'captureType':s['extent']};sources.append(rec)
 if p.endswith('.pdf'):
  pdf=PdfReader(p);pages=[16,17,18] if 'schmoelz' in p else [1,2] if 'unibas' in p else [19,20,21] if 'estevez' in p else [1,11,12,13] if 'ucdavis' in p else [1,2,3,4]
  for n in pages:
   t=pdf.pages[n-1].extract_text();pageTexts[(p,n)]=t;extractions.append({'sourcePath':p,'physicalPage1':n,'pageText':t,'exactPageTextUTF8SHA256':sha(t.encode()),'recipe':'pypdf6.19.0 PdfReader(path).pages[n-1].extract_text(); exact returned string, no normalization.','sourceRawSHA256':sha(b),'sourceGitBlob':s['gitBlob']})
 else:
  h=H();h.feed(b.decode());selected=set()
  for i,t in enumerate(h.nodes):
   if any(w in t for w in ['1471','An indulgence','An\nindulgence','whole life','living in a monastery','brought to an end','Extracts from Journal']):selected.update(range(max(0,i-2),min(len(h.nodes),i+4)))
  contexts.append({'source':rec,'recipe':'HTMLParser convert_charrefs=True, omit script/style, strip each nonempty data node; indexed zero-based; derived text SHA distinct from original rawHTML SHA.','nodes':[{'index0':i,'text':h.nodes[i],'exactNodeUTF8SHA256':sha(h.nodes[i].encode())} for i in sorted(selected)]})
for p in a['pdfDerivationMap']['pages']:
 t=pageTexts[(p['sourcePath'],p['physicalPage'])];assert sha(t.encode())==p['originalPageTextSHA256']
S=[
 'Vatican1471 full definition gives temporal punishment after guilt is forgiven; the definition directly identifies indulgence.',
 'Oxford thesis1 states whole life of the faithful is penance. Actual complete thesis and following context read.',
 'Schmoelz physical17 frames pilgrimage conditionally through travel to/veneration of relic or image in ecclesiastical building. The note attributes this research definition rather than claiming a universal exclusion of other pilgrimage forms.',
 'Vatican following definition distinguishes partial/plenary by how much temporal punishment is removed.',
 'Fordham complete captured excerpt, chapter1, defines cenobites as living in monastery under rule or abbot; this is an excerpt of Rule, not a full-book capture.',
 'Full Vatican definition supports already forgiven guilt and remaining temporal punishment; distinction is faithful.',
 'Unibas physical1 printed594 explicitly identifies Isbiliya/Seville as Almohad capital in al-Andalus and transformation1156–1199.',
 'Estevez physical20 printed42 complete following paragraph states control and benefit from resources after conquest1085; short binding alone omitted the resources claim, whole page proves it.',
 'Unibas physical1 full construction list, city/outskirts list supports walls, bridges, aqueduct, mosque and luxury alcaiceria bazaar. Market claim requires the full page beyond short quote.',
 'Unibas physical1 explicitly compares new Friday mosque dimensions with Cordoba mosque.',
 'Fordham heading identifies Extracts from Journal. Full opening dated1492 says second January, royal banners on Alhambra towers. Current journal genre correct.',
 'Unibas full physical1 directly supports both city/capital and remodeling dates.',
 'Syed physical11–13 directly identifies jihad as the collective duty and transition to individual duty on invasion. Bonner2–3 also warns terminology overlaps: support for the key is direct; exclusion of qital as another possible label is not established by these passages.',
 'Bonner2–3 explicitly defines qital as fighting and says it sometimes conveys something similar to jihad/ribat, with overlapping semantic ranges. The note acknowledges this.',
 'Syed physical1 directly gives modern martial, personal passions and nonviolent justice/equality uses, independent of classic legal status.',
 'Bonner2 defines ghazw/ghazwa/ghaza as raiding. This is an expedition/activity term, not itself a collective-versus-individual status label.',
 'Bonner3 calls Siyar law of war and an alternative legal-manual section to Book of Jihad with broadly similar contents. It identifies legal field, not a duty status. External relations is a broad paraphrase of this war-law subject, not an extra asserted diplomatic rule.',
 'Syed11–13 supplies collective/individual distinction and differing Hanafi/Shafii formulations. Explanation properly scopes to these traditions and does not claim every detail applies to all jurists.'
]
E=[
 'PASS easy as editorial judgment under138: a basic Catholic teaching recognizable within a large Catholic cultural group; clear one-sentence definition, no date or hidden lexical trap. Penance competes plausibly; pilgrimage and monastic rule remain real religious practices. No empirical familiarity survey claimed. Independent definition association replaces old Luther→indulgences inverse.',
 'Useful specific fact about penance, attributed to thesis1. It is not a bare rejection or fact about another option.',
 'Useful own-option pilgrimage fact, attributed to the research. No need for a universal taxonomy.',
 'Correct note adds partial/plenary classification beyond asked definition/key. Meets additive rule.',
 'Useful own-option monastic rule fact about cenobitic life and authority.',
 'Clear distinction between guilt already forgiven and temporal punishment; no polemical Luther clue remains.',
 'PASS medium: al-Andalus capital and medieval transformation need topical knowledge; four actual Iberian cities are plausible. Dates corroborate location without arithmetic shortcut.',
 'Useful own-Toledo conquest and resource-control fact.',
 'Correct Seville note adds specific building projects and market beyond capital/date asked.',
 'Useful Cordoba-specific comparison links that city to a documented mosque rather than merely calling it wrong.',
 'Useful Granada own-city fact, corrected journal attribution. Fullcontext supports what Columbus recorded, not an independently certified eyewitness claim.',
 'Clear attributed statement of city/capital and period, no overclaim about entire city surviving unchanged.',
 'HOLD unique-key, not medium difficulty: all4 are genuine topical Arabic terms and defeat the former majority shortcut. However Bonner says qital can convey something similar to jihad and all terms overlap. Asking for a military obligation’s legal status distinguishes a duty from a field/raid, but does not itself distinguish qital from jihad as a label for the fighting obligation. Syed12 proves jihad qualifies; it does not prove qital cannot. Needs coordinator adjudication of this precise alternative, no reclassification.',
 'FIX: the own-option fact and overlap acknowledgement are useful, but the closing appeal to legal status is not a demonstrated reason to reject qital. Collective→individual is a status of the duty, not a distinct noun name. It currently purports to resolve the exact ambiguity without source-backed distinction.',
 'Correct jihad note adds modern nonmilitary semantic range beyond asked classic legal duty; source explicitly supports it.',
 'Useful own-ghazw fact about raiding/expedition, distinct from a legal duty category.',
 'Useful own-Siyar fact about legal field. Similar manual contents do not turn a book/field into a named personal duty; this alternative itself is distinguishable.',
 'Explanation accurately states Syed’s legal duty and types of neighbouring concepts. These conceptual roles do not independently settle the qital option overlap; prompt HOLD remains separate.'
]
rows=[];bindingcount=0;fragments=0
for k in scope:
 c=frozen[k];ar=next(x for x in a['records'] if x['id']==k);assert sha(nat(c))==ar['wholeRecordSHA256'];fields=[]
 for g in ['prompt-key','answers[0].note','answers[1].note','answers[2].note','answers[3].note','explanation']:
  lit={'prompt':c['prompt'],'orderedAnswerTexts':[x['text'] for x in c['answers']],'correctIndex':c['correctIndex'],'correctAnswerText':c['answers'][c['correctIndex']]['text']} if g=='prompt-key' else c['explanation'] if g=='explanation' else c['answers'][int(g[8])]['note']
  z=next(z for z in a['fieldReviews'] if z['questionId']==k and z['field']==g);assert lit==z['literal'];assert sha(nat(lit))==z['literalSHA256'];ix=len(rows)*6+len(fields);proof=[]
  for b in z['sourceBindings']:
   bindingcount+=1;assert sha(b['exactQuote'].encode())==b['quoteSHA256'];p=b['sourcePath'];assert sha(raws[p])==b['rawSHA256'];pr={'sourcePath':p,'originalURL':b['url'],'sourceRawSHA256':b['rawSHA256'],'sourceGitBlob':b['gitBlob'],'historicalCitationQuote':b['exactQuote'],'historicalCitationQuoteSHA256':b['quoteSHA256'],'historicalCitationUnchanged':True,'citationSHARecipe':'Exact UTF8 historical quote; not same as native page extraction.','actualProofs':[]}
   if 'pdfDerivation' in b:
    for f in b['pdfDerivation']['fragments']:
     fragments+=1;t=pageTexts[(p,f['physicalPage'])];l,r=f['charRange'];q=t[l:r];assert sha(t.encode())==f['originalPageTextSHA256'];assert q==f['actualDerivedQuote'];assert sha(q.encode())==f['actualDerivedQuoteSHA256'];pr['actualProofs'].append({'physicalPage1':f['physicalPage'],'exactOriginalPageTextSHA256':sha(t.encode()),'UnicodeCodePointRange0':[l,r],'exactActualDerivedQuote':q,'exactActualDerivedQuoteSHA256':sha(q.encode()),'recipe':'pypdf6.19 exact returned page.extract_text, no normalization; range Unicode codepoints. Full page saved in pdf-independent-extractions.json.'})
   else:pr['actualProofs'].append({'kind':'Independently parsed full relevant original HTML entry','contextFile':'html-independent-context.json','sourceRawBytesPreserved':True})
   proof.append(pr)
  ev='HOLD' if ix==12 else 'FIX' if ix==13 else 'PASS'
  fields.append({'field':g,'currentLiteral':lit,'insertionJSONSHA256':sha(nat(lit)),'canonicalJSONSHA256':sha(can(lit)),'sourceVerdict':'PASS','editorialVerdict':ev,'manualSourceReason':S[ix],'manualEditorialReason':E[ix],'bindings':proof})
 rows.append({'id':k,'difficulty':c['difficulty'],'wholeSourceVerdict':'PASS','wholeEditorialVerdict':'HOLD' if k.endswith('jihad') else 'PASS','wholeVerdict':'HOLD' if k.endswith('jihad') else 'PASS','insertionCardSHA256':sha(nat(c)),'canonicalCardSHA256':sha(can(c)),'fields':fields})
uniqueFragments={(b["sourcePath"],f["physicalPage"],tuple(f["charRange"]),f["actualDerivedQuoteSHA256"]) for z in a["fieldReviews"] for b in z["sourceBindings"] if "pdfDerivation" in b for f in b["pdfDerivation"]["fragments"]}
assert bindingcount==22;assert fragments==18;assert len(uniqueFragments)==13
partners=[]
for p in Path('src/content/topics').glob('*.json'):
 for c in json.loads(p.read_bytes())['questions']:
  if any(t in (c['prompt']+' '+c['answers'][c['correctIndex']]['text']).lower() for t in ['индульген','джихад','севиль','альмохад','киталь','сияр']):partners.append({'topic':str(p),'id':c['id'],'prompt':c['prompt'],'key':c['answers'][c['correctIndex']]['text'],'canonicalCardSHA256':sha(can(c))})
spec=Path('/Users/eaafonasev/Projects/mindbattle-planning/docs/GAME_SPEC.md').read_text().splitlines();reader=os.environ['CODEX_THREAD_ID'];assert reader=='01a12f3d-8ec1-78b3-b153-5f2a62967421';assert a['authorIdentity']=='01a12fe9-74d9-7272-a1d2-f26317e06001';assert reader!=a['authorIdentity']
r={'recordType':'Independent current whole18 source/editorial reread, not preservation-only audit','readerIdentity':reader,'authorIdentity':a['authorIdentity'],'identityBasis':'Actual reader native CODEX_THREAD_ID matches trusted coordinator ID; author separate trusted fe9. No delegation/model/chat changes.','authorReceipt':AUTHOR,'authorFreeze':FREEZE,'authorReceiptSHA256':sha(Path(AUTHOR).read_bytes()),'runtimeFreeze':RUNTIME,'scope':scope,'cards':rows,'sources':sources,'sourceReadExtent':'All18 current groups/12 optiontexts/key personally read. Original complete source captures byte verified. Full relevant PDF physical pages personally read: Schmoelz17; Unibas1; Estevez20; Syed1,11–13; Bonner2–3, with surrounding extractions saved. Full relevant HTML entries read including heading+genre and catechism definition+classification. No entire316/28/22/19-page book reading claimed.','pdfExtractor':'pypdf6.19.0 exact returned text, no normalization; historical citation SHA and native fragment/page SHA separately preserved.','dispatchCountAnnotation':'Actual v4 field bindings contain18 native fragment bindings and13 unique (source,page,range,SHA) fragments. Dispatch described16 PDF fragments; record actual counts, do not rewrite historical quote identity.', 'renderQA':{'inspectedPages':['Unibas physical1 printed594 two-column page','Bonner physical2–3 terminology transition and BookSiyar context','Syed physical12 printed146 duty-transition context'],'files':[{'path':str(p),'SHA256':sha(p.read_bytes())} for p in sorted((OUT/'rendered').glob('*.png'))]},'bindingCounts':{'groups':18,'sourceBindings':bindingcount,'PDFNativeFragmentBindings':fragments,'PDFNativeUniqueFragments':len(uniqueFragments),'completeOriginals':9},'approvedRules':[{'path':'/Users/eaafonasev/Projects/mindbattle-planning/docs/GAME_SPEC.md','line1':n,'quote':spec[n-1]} for n in [138,139,142,143,144]],'duplicates':{'partners':partners,'analysis':'Current Indulgence tests definition→term, independent of history-germany Luther→opposed practice and old reversed author draft. Shared answer term alone is not repeated tested association. Current Reconquista tests Almohad Seville capital/date; own-city notes are not prompt duplicates. Jihad tests classic collective→individual duty, not general jihad translation or modern sense. No external partner edited/count increment.'},'guards':{'current3DiskFrozenHEADAuthorEqual':True,'protected97FrozenBaselineEqual':True,'protected97CurrentChangedIds':[k for k in protected if working[k]!=baseline[k]],'all9RawSourceSHAblobDiskFreezeHEADEqual':True,'all18NativeAuthorGroupHashesMatch':True,'allHistoricalCitationSHAand18NativeFragmentBindings13UniqueVerified':True,'runtimeSourceAuthorPlanningReviewhashCounterMutations':0,'counterIncrement':0},'summary':{'source':{'PASS':18,'FIX':0,'HOLD':0},'editorial':{'PASS':16,'FIX':1,'HOLD':1},'whole':{'PASS':2,'FIX':0,'HOLD':1}},'testsBuildFullQABrowserDeploy':0,'cleanup':{'ownedProcessesExpectedAfterRenderCompletion':0,'ownedTemporaryResources':0,'ownedUntrackedIgnoredExpectedAfterCommit':0,'foreignFilesIndexProcessesPreserved':True,'retainedEvidence':'Own native snapshots, independent exact PDF extracts, HTMLcontexts, inspected page renders and receipt/helper committed.'},'nextStep':'Coordinator adjudicates current Jihad qital uniqueness HOLD and note0 FIX. Other6Middle held. Reader stops after atomic receipt/commit/cleanup; no automatic new source cycles or counter certification.'}
(OUT/'pdf-independent-extractions.json').write_text(json.dumps(extractions,ensure_ascii=False,indent=2)+'\n');(OUT/'html-independent-context.json').write_text(json.dumps(contexts,ensure_ascii=False,indent=2)+'\n');(OUT/'reader-receipt.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');(OUT/'current3-insertion.json').write_bytes(nat([frozen[k] for k in scope])+b'\n');(OUT/'current3-canonical.json').write_bytes(can([frozen[k] for k in scope])+b'\n')
print(r['summary']);print([(x['id'],x['wholeVerdict']) for x in rows])
