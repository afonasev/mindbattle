"""Qualify pre2 parks25 SOURCE exact current peers and decoded fullpage captures; no credit."""
import pathlib,importlib.util,subprocess,json,hashlib,re
D=pathlib.Path(__file__).parent;C=D.parents[3]
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('own',D/'owned-tools.py');a=load('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a.P=m.P
R=D/'source-parks25-40-original';B=D/'qualified-parks25-original';B.mkdir(exist_ok=True);freeze='79fe5b979073fc7bfcb38a80a8bc5c94ca272044';counts={}
for uid in [m.O,'01a1443a-30c4-73f1-bbf5-2df86115a910','01a14483-ccd0-7321-bd23-2262fcb11e5b']:
 fs=list(pathlib.Path('/Users/eaafonasev/.codex/sessions/2026/10/16').glob('*'+uid+'.jsonl'));assert len(fs)==1;counts[uid]=sum(json.loads(l).get('type')=='compacted' for l in fs[0].open());assert counts[uid]<2
for p in R.rglob('*'):
 if p.is_file():assert p.read_bytes()==subprocess.check_output(['git','-C',str(C),'show',freeze+':'+str(p.relative_to(C))])
pre=[];sp=m.read(R/'sourceproof.json')
for source in sp['rawSources']:
 p=pathlib.Path(source['path']);assert m.raw(p)==source['sha256'];body=m.read(p);assert isinstance(body,str);assert hashlib.sha256(body.encode()).hexdigest()==source['decodedVisibleBodySHA256'];ids={int(n) for n in re.findall(r'\bL([0-9]+):',body)};declared=int(re.search(r'Total lines: ([0-9]+)',body)[1]);assert ids==set(range(declared));pre.append({'path':str(p.relative_to(C)),'rawSHA256':m.raw(p),'decodedBodySHA256':source['decodedVisibleBodySHA256'],'actualVisibleLineIds':len(ids),'declaredTotal':declared,'missingLabels':[],'decodedJSONstringBeforeLineParsing':True})
ps=m.read(R/'peer-snapshot.json');seen={};combined=[]
for p in ps['actualCurrentPeers']+ps['fullRelevantHits']:
 p=dict(p);p['sha256']=p.get('sha256',p.get('canonicalSHA256'));assert m.sha(p['card'])==p['sha256']
 if p['id'] in seen:assert seen[p['id']]==p['card'];continue
 seen[p['id']]=p['card'];live=next(q for q in m.read(C/f"src/content/topics/{p['topicId']}.json")['questions'] if q['id']==p['id']);assert live==p['card'];combined.append(p)
ps['actualCurrentPeers']=combined
for p in ps['latestProposals']:
 assert m.sha(p['card'])==p['canonicalSHA256'];e=next(e for e in m.read(pathlib.Path(p['path']))['entries'] if e['id']==p['id']);assert e['proposedCard']==p['card'] and e['afterHash']==p['canonicalSHA256']
g=ps['fullGlobalPromptKeyRetrieval'];assert m.raw(pathlib.Path(g['basePath']))==g['baseRawSHA256'];base=m.read(pathlib.Path(g['basePath']))['cards'];delta={r['id']:r for r in ps['currentCDeltaAgainstRetrieval']['changedRows']};rows=[delta.get(r['id'],r) for r in base];cat={}
for tp in sorted((C/'src/content/topics').glob('*.json')):
 t=m.read(tp)
 for q in t['questions']:cat[q['id']]={'topicId':t['id'],'id':q['id'],'prompt':q['prompt'],'answers':[v['text'] for v in q['answers']],'correctIndex':q['correctIndex']}
assert len(rows)==len(cat)==11000 and rows==[cat[r['id']] for r in rows];assert m.sha(rows)==g['freshCanonicalRowsSHA256']
for name in ['candidate.json','sourceproof.json']:m.write(B/name,m.read(R/name))
m.write(B/'peer-snapshot.json',ps)
concerns=['Original25 FIRSTINITIAL, actualdefectonly/goodtextpreserve MAIN/all4labels/explanation/frozenEASYkey0 retained. Correctnotepluralunsupportedmountainranking narrowed tohighestmountainEngland andglaciallakes concreteextra beyondWindermere/Romanticpoetsprompt/key. Donananote delta narrowed estuary. Cinquecoastalvillages referscoastallandscape notall5waterfront (Cornigliahighpromontory), do notassertallUNESCOpropertyequalnationalpark.', '8fullprimarycaptures originalwebtoolresult JSONstrings, rawhash+decodedhash exact/actualvisiblelineIDscomplete rootchecked, no headers/snippets/TotalLinesalone: UNESCO422164lines, LakeFacts221, Poetry83, geologyexactcapture, Cinqueparkdescription499, UNESCO826233/685206/33175. Exact fullsubstantivearticles andownsourceindex/provenance retained; no newfetchjustreader, no retryknownfailedroutes.', 'AuthorEASY calibration explicitlyLARGE British/Englishculturalgroup nottinyregionalpopulation/tourist/poetryspecialistcommunity. Independentlyjudge factualbroadfamiliarity ofLakeDistrict/Windermere+Romanticlandscapeclue; NationalPoetryDay/link alone andvisitorcounts/area/UNESCOdesignation notautomaticEASY proof, no surveyclaim. Fourrealprotectedplaces samecategory/credible/unique/grammar/taxonomy; do not automaticallyrejectpropernames or inheritauthorlevel.', 'All6literal/4wholevariants/ownoptionnewfacts sourcegrounded. Global11000MAIN exactauthorbase+delta reconstructedandallcurrentrowsstillidentical; polarfilebytehash drift only laternotes30, no MAINdrift. Same100/full10closestactualwholebodies/genuine21-24proposals bilateralERVC/directreverse, latestnew24soapnotoldb7/oldIDinference; parks26currentlyoriginalunreviewed nofakeHOLD. SOURCEfirstraw79fe5pre2/root/source/OTHER<2; no qualitybeforeexactapply/QA19/independentFIRSTINITIAL/preleasedbinding; one directedfixthenFINAL/HOLD0 noordinary2/reset.']
r=a.apply(B,'01a1443a-30c4-73f1-bbf5-2df86115a910',[25],D/'apply-parks25-original.json',D/'qa-parks25-original.json',pathlib.Path(__file__),qualifyOnly=True,peerSnapshot={'actualCurrentPeers':[p for p in ps['actualCurrentPeers'] if p['topicId']=='national-parks-nature']},concerns=concerns);r.update(sourceOriginalFreeze=freeze,nativeCompactions=counts,allActualFullBodiesVerified=len(combined),primaryDecodedCaptureAudit=pre,global11000MAINStillExact=True)
m.write(B/'normalization-provenance.json',{'owner':m.O,'originalSOURCEfreeze':freeze,'operations':'Union existing authorfullactual same-topic and cross-topic hit bodies and sha alias only. Candidate/claims/judgments unchanged. JSONstring fullcaptures decoded IN MEMORY for precise linecoverage; originalrawfiles unchanged. GlobalMAIN completebase+authordelta still exactcurrent despite polar note-onlybytechange.','files':[{'name':n,'originalRawSHA256':m.raw(R/n),'normalizedRawSHA256':m.raw(B/n)} for n in ['candidate.json','sourceproof.json','peer-snapshot.json']]});m.write(D/'qualification-parks25-original.json',r)
print(m.savecode([p for p in B.rglob('*') if p.is_file()]+[D/'qualification-parks25-original.json',pathlib.Path(__file__)],'Qualify original parks25 exact full decoded source contexts and live globalMAIN no credit'))
