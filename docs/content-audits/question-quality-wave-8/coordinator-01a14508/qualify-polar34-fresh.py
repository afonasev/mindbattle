"""Qualify exact personally completed SOURCE34; current26 promotion is separately audited."""
import pathlib,json,re,subprocess,importlib.util
D=pathlib.Path(__file__).parent;C=D.parents[3]
def mod(n,p):
 s=importlib.util.spec_from_file_location(n,p);x=importlib.util.module_from_spec(s);s.loader.exec_module(x);return x
m=mod('o',D/'owned-tools.py');a=mod('a',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a.P=m.P
R=D/'source-polar34-preservation-complete';B=D/'qualified-polar34-fresh';B.mkdir(exist_ok=True);freeze='f6bbffbb59c4489b960d1c3ce14a85ce7dececa6';author='01a150be-8a21-7a73-a0c7-6358f1abe716';counts={}
for u,date in [(m.O,'16'),('01a14483-ccd0-7321-bd23-2262fcb11e5b','16'),(author,'19')]:
 j=next(pathlib.Path('/Users/eaafonasev/.codex/sessions/2026/10/'+date).glob('*'+u+'.jsonl'));counts[u]=sum(json.loads(l).get('type')=='compacted' for l in j.open());assert counts[u]<2
for p in R.rglob('*'):
 if p.is_file():assert p.read_bytes()==subprocess.check_output(['git','-C',str(C),'show',freeze+':'+str(p.relative_to(C))])
candidate=m.read(R/'candidate.json');sp=m.read(R/'sourceproof.json');ps=m.read(R/'peer-snapshot.json');entry=candidate['entries'][0];assert candidate['sourceNativeId']==sp['sourceNativeId']==ps['sourceNativeId']==author;assert entry['afterHash']=='88c9468abc1cee4409b48966b0784a003ecfe4ef878bcfd84bab41131748eff4';assert entry['proposedCard']['answers'][3]['note']==entry['beforeCard']['answers'][3]['note']
contexts=[]
for source in sp['rawSources']:
 p=C/source['path'];assert m.raw(p)==source['sha256'];body=m.read(p);assert isinstance(body,str);headers=list(re.finditer(r'cite[^]+ \[wordlim:[^\n]*Total lines: ([0-9]+)',body));target=6 if 'spaceplace' in source['url'] else 67;ix=next(k for k,h in enumerate(headers) if int(h.group(1))==target);segment=body[headers[ix].start():headers[ix+1].start() if ix+1<len(headers) else len(body)];ids={int(n) for n in re.findall(r'\bL([0-9]+):',segment)};assert ids==set(range(target));contexts.append({'path':source['path'],'rawSHA256':source['sha256'],'actualVisibleLineIds':target,'completeContext':'NASA6 science4-5 only; fictional fill-in1-2 excluded' if target==6 else 'GSFC67 complete page; scientificbody36-43 and48-50','fullPageCaptured':True})
cat={};topicFiles={}
for p in (C/'src/content/topics').glob('*.json'):
 t=m.read(p);topicFiles[t['id']]=p
 for n,q in enumerate(t['questions'],1):cat[q['id']]={'topicId':t['id'],'sourceOrder':n,'card':q}
actual={}
def addpeer(i,tid,c,sha):
 assert c==cat[i]['card'] and m.sha(c)==sha;row={'id':i,'topicId':tid,'sourceOrder':cat[i]['sourceOrder'],'card':c,'sha256':sha}
 if i in actual:assert actual[i]['card']==c
 actual[i]=row
for p in ps['actualCurrentPeers']:addpeer(p['id'],p['topicId'],p['card'],p['sha256'])
g=m.read(R/'global-main-search.json');b=R/g['baselineMainSnapshotPath'];assert m.raw(b)==g['baselineMainSnapshotFileSHA256'];rows=m.read(b)['rows'];assert len(rows)==g['baselineMainCount']==11000 and m.sha(rows)==g['baselineMainCanonicalSHA256'];assert len(g['inputFiles'])==110
for inp in g['inputFiles']:
 original=subprocess.check_output(['git','-C',str(C),'show',candidate['catalogBaseline']+':'+inp['path']]);import hashlib;assert hashlib.sha256(original).hexdigest()==inp['rawSHA256']
patterns={k:v['regex'] for k,v in g['patterns'].items()};assert all(chr(92)*2+'w' not in v for v in patterns.values());assert re.search(patterns['hemisphericRange'],'в северном и южном полушариях',re.I)
retrieved=[];drift=[]
for row in rows:
 assert m.sha(row['main'])==row['mainSHA256'];q=cat[row['id']]['card'];live={'prompt':q['prompt'],'answers':[v['text'] for v in q['answers']],'correctIndex':q['correctIndex']}
 if row['main']!=live:drift.append(row['id'])
 if any(re.search(v,json.dumps(row['main'],ensure_ascii=False),re.I) for v in patterns.values()):retrieved.append(row['id'])
assert set(retrieved)=={r['id'] for r in g['hits']} and len(retrieved)==11
pr=m.read(R/'proposal-provenance.json');p26=pr['explicitlyNamedUnrelatedProposal'];assert m.raw(C/p26['manifestPath'])==p26['manifestSHA256'];assert m.sha(p26['proposedCard'])==p26['proposedWholeCardSHA256'];e26=next(e for e in m.read(C/p26['manifestPath'])['entries'] if e['id']=='national-parks-nature-026');assert e26['proposedCard']==p26['proposedCard']==cat[e26['id']]['card'];assert drift==['national-parks-nature-026'];assert p26['actualCurrentWholeCardSHA256']==e26['beforeHash'] and m.sha(p26['actualCurrentCard'])==e26['beforeHash']
for p in pr['adjacentFinalProposals32_33']:
 assert m.raw(C/p['manifestPath'])==p['manifestSHA256'];assert p['proposedCard']==p['actualCurrentCard']==cat[p['id']]['card'] and m.sha(p['proposedCard'])==p['proposedWholeCardSHA256']
read=m.read(R/'same-topic-main-read-receipts.json');assert read['count']==len(read['receipts'])==100
for rr in read['receipts']:
 assert rr['personallyReadByNativeId']==author and rr['mainSHA256']==m.sha(rr['main']) and rr['wholeCurrentCardSHA256']==actual[rr['id']]['sha256'];c=actual[rr['id']]['card'];assert rr['main']=={'prompt':c['prompt'],'answers':[v['text'] for v in c['answers']],'correctIndex':c['correctIndex']}
for hit in ps['globalSearch']['hits']:
 addpeer(hit['id'],hit['topicId'],hit['fullCurrentCard'],hit['wholeCurrentCardSHA256']);assert m.sha(hit['main'])==hit['mainSHA256'];assert all(hit[k] and hit[k]['directAnswer'] and hit[k]['verdict'] for k in ['candidateToPeerERVC','peerToCandidateERVC'])
ps['actualCurrentPeers']=list(actual.values());ps['ROOTKnownProposalPromotion']={'id':'national-parks-nature-026','sourceBeforeHash':p26['actualCurrentWholeCardSHA256'],'sourceReadProposalHash':p26['proposedWholeCardSHA256'],'nowActualHash':m.sha(cat['national-parks-nature-026']['card']),'ROOTapplyCommit':'0d0e115bac0d5a943033fad542a0288f35888603','operation':'Only ROOT promotion of exact author-personally-read unrelated proposal4794 toCURRENT; original SOURCE11000baseline remainshistorical16e3. SOURCEalreadyreadboth fullbodies, no newSOURCEjudgmentinvented. IndependentINITIALmustrefreshCURRENTglobal.','sourceHistoricalTerminologyCorrection':'Source qualification text post-cycle-2 refers retiredc606 input history; linkedmanifest is freshSOURCE7d native0 personaladoption andwasnotyetROOTqualified at SOURCEread. Samebody contentbinding unchanged.'}
for n,x in [('candidate.json',candidate),('sourceproof.json',sp),('peer-snapshot.json',ps)]:m.write(B/n,x)
concerns=['Original34 identityofauroraduplicatesweather-climate31; newMAIN asks hemisphericdistribution. Originalgoodkeynotechargedparticlesexcitinggases restoredverbatim, concreteextra beyondwholeprompt/keybothhemispheres. FrozenEASY/key3, all6literal4wholevariants independently assess all4credible/comparablegeographicranges/unique/grammar/polartaxonomy/absoluteadultLARGEculture level; no template/crossnoteban.', 'NASA SpacePlace originalJSONstring firstfull6lineblock scientific4-5 supportshemispheres/names/chargedparticlesexciteatmosphericgases; fictionfill-in1-2NOTproof, separateNSIDC193blocknotconflated. NASA GSFC67fullpage personallyread/actualallIDs, fullscience36-43/48-50: geomagneticovalsvsgeographicpoles; overgeographicpolesrare notnever; nooccurrence-onlywinter or allaurorasonlynearhighlatitude claim. Preserveexactqualifications andownnotetruth.', 'SOURCEfull11000MAINsnapshot76fd/raw andcanonical45890;110topicfilehashes verifiedatSOURCEcatalogf8becca, own100MAINreceipts/allfullclosest11hitsbilateralERVC/directreverse andoriginalbeforeduplicatepairdistinctfromnewcandidate. ActualcatalogchangedONLYparks26afterSOURCEread: exact4794SOURCEownfullread unrelatedproposal promotedROOT0d0e; prior16e3actual and4794proposal bodyhashes retained, metadataROOTreconciliation explicit, no SOURCEclaimedfreshpostapplyread. IndependentINITIALfreshglobalCURRENTrequired. Latest32/33actual8e61/c463 preserved andprovenancefull; SOURCE34first8d099thenpreservationf6bb actual0/noINITIAL/fixcycleyet, root/reader<2. NoQUALITYcreditfromSOURCE/QA. One directedfixthenFINAL/unresolvedHOLD0/noordinary2/reset.']
r=a.apply(B,author,[34],D/'apply-polar34-fresh.json',D/'qa-polar34-fresh.json',pathlib.Path(__file__),qualifyOnly=True,peerSnapshot={'actualCurrentPeers':[p for p in actual.values() if p['topicId']=='polar-regions']},concerns=concerns);r.update(sourceOriginalFreeze=freeze,nativeCompactions=counts,primaryContexts=contexts,allActualFullBodiesVerified=len(actual),globalSnapshotCount=11000,globalInputFiles=110,ROOTKnownProposalPromotion=ps['ROOTKnownProposalPromotion'],qualityCredit=0)
m.write(D/'qualification-polar34-fresh.json',r);m.write(B/'normalization-provenance.json',{'sourceFreeze':freeze,'sourceOriginalPath':str(R.relative_to(C)),'operation':'Exactcandidate/sourceproof unchanged. Union fullcurrentclosest11hit bodies+same100authorpeers; knownsameauthor-read4794proposal promotedtoCURRENT afterSOURCEread separatelyROOT-audited, no newSOURCEjudgments. Originalsourcewhole11k snapshot/110hashes/readreceipts canonicalref unchanged. Source originaldefectpair notpromotedtocandidatePASS.','qualityCredit':0});print(m.savecode(list(B.glob('*.json'))+[D/'qualification-polar34-fresh.json',pathlib.Path(__file__)],'Qualify fresh polar34 fullprimary actualpeer and knownproposalpromotion bindings'))
