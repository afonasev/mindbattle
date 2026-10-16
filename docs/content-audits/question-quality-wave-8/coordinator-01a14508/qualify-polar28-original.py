"""Qualify pre2 SOURCE28 exact card/primary hashes/live fullpeers; zero credit."""
import pathlib,importlib.util,subprocess,json,re
D=pathlib.Path(__file__).parent;C=D.parents[3]
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('own',D/'owned-tools.py');a=load('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a.P=m.P
R=D/'source-polar28-40-resumed';B=D/'qualified-polar28-original';B.mkdir(exist_ok=True);freeze='8a1b882bee5e68c5ce662c8ccebe0379bab07af3'
counts={}
for uid in [m.O,'01a1447f-53aa-73f0-b307-03a735f3bb43','01a14483-ccd0-7321-bd23-2262fcb11e5b']:
 fs=list(pathlib.Path('/Users/eaafonasev/.codex/sessions/2026/10/16').glob('*'+uid+'.jsonl'));assert len(fs)==1;counts[uid]=sum(json.loads(l).get('type')=='compacted' for l in fs[0].open());assert counts[uid]<2
for p in R.rglob('*'):
 if p.is_file():assert p.read_bytes()==subprocess.check_output(['git','-C',str(C),'show',freeze+':'+str(p.relative_to(C))])
for name in ['candidate.json','sourceproof.json','peer-snapshot.json']:m.write(B/name,m.read(R/name))
ps=m.read(B/'peer-snapshot.json')
for p in ps['actualCurrentPeers']:
 assert m.sha(p['card'])==p['sha256'];live=next(q for q in m.read(C/f"src/content/topics/{p['topicId']}.json")['questions'] if q['id']==p['id']);assert live==p['card']
sp=m.read(B/'sourceproof.json');ci=sp['coverageIndex'];assert m.raw(C/ci['path'])==ci['sha256'];cov=m.read(C/ci['path']);contexts=[]
for c in cov['contexts']:
 for w in c['windows']:assert m.raw(C/w['path'])==w['rawSHA256']
 assert c['completeRelevantArticleOrSectionCaptured'];contexts.append({k:v for k,v in c.items() if k not in ['windows','actualUnionLineIds']})
for p in ps['relevantGenuineProposals']:
 assert m.sha(p['card'])==p['sha256'];doc=m.read(C/p['sourcePath']);e=next(e for e in doc['entries'] if e['id']==p['id']);assert e['proposedCard']==p['card'] and e['afterHash']==p['sha256']
concerns=['Original28 FIRSTINITIAL aftersavedINPUT NotRun completed bysameauthor native1, firstraw8a1b882pre2. MAIN/alllabels/explanation/EASYkey1/Svalbardnote0/Nunavutnote3 preserved. CorrectnoteGreenlandic officiallanguage concreteextra beyondwholeprompt/key RealmDenmark. Danishofficialusage exception respected; membership distinct fromfutureconditionedindependence.', 'Full Statsministeriet153lines union inclsubstantive51-122 andforeignresponsibility/delegation71/94-112/independence122. Norwaywhitepaper680declared, actual0-271 includesCOMPLETE §2.2L161-264; neverclaimfull680chapter. Canada102pagefullsubstantive23-86; NPSAlaska270pagefullarticle21-220. OriginalAlaskaGovfailedone+officialNPSalt success, no retry/thirdsource; note2 changedto exactUtqiagvik northernmostUScity notoldunboundstate+NorthAmerica. Coverage paths/windows locators retained.', 'All6literal4wholevariants; currentofficialfullprimary notsearchsnippet/header; basicadultworldgeographyGreenlandDenmark EASY authorjudgment independentlyassess. FourcredibleArcticterritories unique/grammar/polartaxonomy. 11000MAIN/100same110fullactual/27bilateral/genuine27andparks24 actualbody proposals; distinctfromGreenlandlargestisland/continent/location/politicalterms. No crossnoteban: Svalbard note may key29 elsewhere; notautomaticallyMAINduplicate.', 'No creditbefore exactCURRENT affected19+independentINITIAL; one directedSOURCEfixthenFINAL/HOLD0 noordinary2/reset. Root/source/readeractualguards retained. Reader24currentlyactive: do notapply28 until24consumed or exactnopeerdrift confirmed.']
r=a.apply(B,'01a1447f-53aa-73f0-b307-03a735f3bb43',[28],D/'apply-polar28-original.json',D/'qa-polar28-original.json',pathlib.Path(__file__),qualifyOnly=True,peerSnapshot={'actualCurrentPeers':[p for p in ps['actualCurrentPeers'] if p['topicId']=='polar-regions']},concerns=concerns);r.update(sourceOriginalFreeze=freeze,nativeCompactions=counts,allActualFullBodiesVerified=len(ps['actualCurrentPeers']),primaryContexts=contexts)
m.write(B/'normalization-provenance.json',{'owner':m.O,'originalSOURCEfreeze':freeze,'operations':'Byte-equivalent JSON reserialization only; candidate, proof and peers judgments unchanged. No semantic aliases needed.','files':[{'name':n,'originalRawSHA256':m.raw(R/n),'normalizedRawSHA256':m.raw(B/n)} for n in ['candidate.json','sourceproof.json','peer-snapshot.json']]})
m.write(D/'qualification-polar28-original.json',r)
print(m.savecode([p for p in B.rglob('*') if p.is_file()]+[D/'qualification-polar28-original.json',pathlib.Path(__file__)],'Qualify pre2 exact original polar28 SOURCE full live peer bindings no credit'))
