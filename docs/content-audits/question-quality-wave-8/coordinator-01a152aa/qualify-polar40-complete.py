"""Qualify completed original40 personal SOURCE; no quality credit."""
import pathlib,importlib.util,json,subprocess,hashlib,re
D=pathlib.Path(__file__).parent;C=D.parents[3]
def mod(n,p):
 s=importlib.util.spec_from_file_location(n,p);x=importlib.util.module_from_spec(s);s.loader.exec_module(x);return x
m=mod('o',D/'owned-tools.py');a=mod('a',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a.P=m.P
R=D/'source-polar40-complete';B=D/'qualified-polar40-complete';freeze='ceebce65445cd30c8c5b4b18e9e071bef9bd93e5';author='01a152f1-2607-7d71-9ef8-56c47c471fb9'
for uid in [m.O,author,'01a150d1-3383-7d30-ad23-76d70ec18813']:
 j=next(pathlib.Path('/Users/eaafonasev/.codex/sessions/2026/10/19').glob('*'+uid+'.jsonl'));assert sum(json.loads(l).get('type')=='compacted' for l in j.open())<2
for n in ['candidate.json','sourceproof.json','peer-snapshot.json']:
 p=R/n;assert p.read_bytes()==subprocess.check_output(['git','-C',str(C),'show',freeze+':'+str(p.relative_to(C))])
original=m.read(R/'candidate.json');sp=m.read(R/'sourceproof.json');ps=m.read(R/'peer-snapshot.json');assert sp['sourceNativeId']==ps['sourceNativeId']==author
candidate={'owner':m.O,'sourceNativeId':author,'cycle':0,'entries':[original],'technicalSingleRecordWrapper':{'path':str((R/'candidate.json').relative_to(C)),'rawSHA256':m.raw(R/'candidate.json'),'freeze':freeze,'operation':'Exact original single record under entries; no field or judgment changes.'}}
b=original['beforeCard'];c=original['proposedCard'];assert m.sha(b)==original['beforeHash']=='20b1eb9b7a6f96ad67394318b413549b7dba3d5f28d84bf436a19e51cc7fe239';assert m.sha(c)==original['afterHash']=='91a8dcd22d2b3bcd4220ed88be57ca5d470e8da64c75e2e3470df8b9ea2c7173';assert c['answers'][2]==b['answers'][2] and all(c[k]==b[k] for k in ['id','difficulty','correctIndex']) and [v['text'] for v in c['answers']]==[v['text'] for v in b['answers']]
for source in sp['rawSources']:
 p=pathlib.Path(source['path']);assert m.raw(p)==source['fileSHA256'];v=m.read(p) if source.get('jsonPointer') else p.read_text()
 if source.get('jsonPointer'):
  for part in source['jsonPointer'].split('/')[1:]:v=v[int(part)] if isinstance(v,list) else v[part]
 assert isinstance(v,str) and hashlib.sha256(v.encode()).hexdigest()==source['capturedTextSHA256'] and source['captureReadProvenance'] and source['coverage'] and source['locator']
 expected=187 if 'caribou3' in source['url'] else 143 if 'cervides-deer' in source['url'] else 140 if 'wapiti' in source['url'] else 258
 assert {int(n) for n in re.findall(r'L(\d+):',v)}==set(range(expected))
 if 'wapiti' in source['url']:assert 'Cervus canadensis' not in v and 'Shawnee for "white rump."' in v
 source['sha256']=source['fileSHA256'];source['technicalFileHashAlias']='Existing exact whole-file digest aliased; jsonPointer/capturedTextSHA256 distinguish retained body. No full primary copy.'
rows=[];cat={}
for sf in ps['global11000MainAudit']['fileInventory']:
 p=C/sf['path'];assert m.raw(p)==sf['fileSha256'];t=m.read(p);assert len(t['questions'])==sf['questionCount']
 for q in t['questions']:cat[q['id']]={'topicId':t['id'],'card':q};rows.append({'topicId':t['id'],'id':q['id'],'prompt':q['prompt'],'answers':[v['text'] for v in q['answers']],'correctIndex':q['correctIndex']})
assert len(rows)==11000 and len(ps['global11000MainAudit']['fileInventory'])==110 and m.sha(rows)==ps['global11000MainAudit']['rowsCanonicalSHA256']=='551dbca3a5e583a27e9ac58f5109b86ccac43fc83de5400a96f981770ec542f6'
actual={}
for p in ps['actualCurrentPeers']+ps['animalsTopicSnapshot']['cards']+ps['crossCatalogClosestFullBodies']:
 digest=p.get('sha256',p.get('canonicalSHA256'));assert p['card']==cat[p['id']]['card'] and m.sha(p['card'])==digest;actual[p['id']]={**p,'sha256':digest}
assert len(ps['actualCurrentPeers'])==99 and len(ps['animalsTopicSnapshot']['cards'])==100
assert ps['currentTopicSnapshot']['targetCurrentCard']==b==cat[b['id']]['card'];actual[b['id']]={'id':b['id'],'topicId':'polar-regions','sourceOrder':40,'card':b,'sha256':m.sha(b)}
for pair in ps['bilateralCurrentAssessments']:
 assert pair['pair'][0]==b['id'] and pair['pair'][1] in actual and pair['entityRelationValueContext'] and pair['forward'] and pair['directReverse'] and pair['overlap']
delta=ps['currentCatalogNoteOnlyDelta'];assert delta['currentCard']==cat['national-parks-nature-029']['card'] and m.sha(delta['currentCard'])==delta['currentCardCanonicalSHA256']=='f2fbff276915fceb19ffde3eb5a849ec7dd36ebca7a1f2f8d55c035848b064ee'
ps['actualCurrentPeers']=list(actual.values());ps['technicalNormalization']={'operation':'Lossless union of99same-topic+focus+100animal+onefullcross bodies, verified exact CURRENT. Existing7jointbilateral SOURCE grounds and current29author-owned note-only delta retained. Original sorted11000 projection verified; no ROOT semantic judgment.'}
B.mkdir(exist_ok=True)
for n,v in [('candidate.json',candidate),('sourceproof.json',sp),('peer-snapshot.json',ps)]:m.write(B/n,v)
concerns=['Original40 FIRSTINITIAL neverreviewed/noindependentcycle. Old510b rawcf422 partialpost2 INPUT only noSOURCEapproval. Fresh52f1 personalSOURCEraw dcd7 had unsupportedCervuscanadensis attributiontoBanff despiteactualtextabsent; authorcompletedceebbeforeINITIAL andchangedonlythatnote0fromdcd7 toretainedShawneeetymology, allaffected6/4groundsaligned. Finalexact91a8 fromoriginal20b1 scopesMAINwildanimal; same4labels/key1/EASY/goodmoosenote preserved, correctnoteaddsWapuskherds, explanationregionalnaming/sourceofficial/muskoxnoteArctichabitat. No primaryproofinheritancefromoldauthor/ROOTdiagnostic.', 'Independent all6literal/4WHOLEvariants FOURseparategrammar/plausibility/truthUniqueKey/noteTruthUsefulness. FullretainedofficialParkCanadaWapusk187labels0-186 substantiveL22-29/L63-67; Jasper1430-142/L24-28 mooselargestdeerfamily; Banff1400-139/L27-29 wapitiShawneewhiterump, NO Cervuscanadensis statement; NOAAFAQ2580-257/L147 muskoxArctic. PrimarysavedonceasrawJSONfile+jsonPointer/capturedTextSHA distinctwholefileSHA, qualifiedsha aliaspointswholefile not#fakepath; personallydecodewholebodies, notsnippets. KeycaribouNorthAmericawildRangifer vsEurope/Asia reindeertypicalname; do notuniversalize domesticatedorallNorthAmericanlanguageusage. Correctnote2namedherdsusingWapuskregion concreteownextra beyondwholeprompt/key; moosenoteownlargestfact preserved, muskoxownArcticoccurrenceusefulness/plausibledistractor independentlyjudge, etymologynoteowntruefact notmandatoryclassification. Directanswernaming2sentences/formatlimits/absolutebroadadultEASY regionalcommonname andgeographytaxonomy independentlyjudge notSOURCEgradeinheritance/noblanketanimalban; no arbitrarymath/genre/format/crossnoteban.', 'Freshsorted11000MAIN hash551dbca excludes sourceOrder anddiffersfromtaxonomymanifestdcbd bydocumentedorderonly; 110filebytes CURRENT including29f2fb solecycle1notedelta personallyread. Same100full inclfocusbefore+animals100/full7closest jointbilateralERVC/directreverse; soleotherlexicalmention yakmountainpackanimal wrongnote notsameMAIN, incidentalnotevsMAINnoblanketban. Polarcontextbearrange/orcarange/sealclass/penguinhemisphere/krillfoodweb/narwhaltooth differententities/relations; fullsource30placehazenaming irrelevant probe retained notforcedfakepair. Readerfreshglobal/allclosestcurrentandgenuineproposals ifactuallyrelevant; nootherqualityinheritance. OriginalBritannicamissingstatusfile remainsNotRun notfalsefailedfetch. OnlyROOTstrictbindingafterapply/QA19/INITIALPASS counts888->889, alloldHOLDs retained0/noordinarycycle2.']
r=a.apply(B,author,[40],D/'apply-polar40-complete.json',D/'qa-polar40-complete.json',pathlib.Path(__file__),qualifyOnly=True,peerSnapshot={'actualCurrentPeers':[p for p in actual.values() if p['topicId']=='polar-regions']},concerns=concerns)
r.update(rawSourceFreeze=freeze,rawFirstFreshSource='dcd7e2cdc999226f58cae2c113ccf99c0cdfcaca',CURRENT=888,remaining=1112,fullGoal=2000,cycle=0,qualityCredit=0)
m.write(D/'qualification-polar40-complete.json',r);print(m.savecode(list(B.glob('*.json'))+[D/'qualification-polar40-complete.json',pathlib.Path(__file__)],'Qualify correctedpersonalSOURCE40 exactBanffownfact fourwholeprimaries and currentMAIN'))
