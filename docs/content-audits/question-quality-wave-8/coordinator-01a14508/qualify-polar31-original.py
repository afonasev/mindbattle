"""Qualify pre2 SOURCE31 exact card/primary hashes/live fullpeers; zero credit."""
import pathlib,importlib.util,subprocess,json,re
D=pathlib.Path(__file__).parent;C=D.parents[3]
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('own',D/'owned-tools.py');a=load('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a.P=m.P
R=D/'source-polar31-40-continuation';B=D/'qualified-polar31-original';B.mkdir(exist_ok=True);freeze='626394334cff0856c39c87d101b04ec289049265'
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
concerns=['Original31 FIRSTINITIAL; MAIN/all4labels/explanation/MEDIUMkey2/correctnote and2otherwrongnotes preserved. ESAofficialgeospatialinstitutionfull48page directL21MostoftheCanadianArcticArchipelagoispartofNunavut; no largestarea/EasternArctic inference substitutedforactualmajorityarchipelagoclaim. OneoriginalnewESAopen succeeded, noaltneeded/newretry.', 'Fivefullprimarycontexts existingGreenland153/Canadaactual150/NPS270/Norwaycomplete§2.2within0-271of680notfullchapter plusESA48fullpage/article18-27. Canada42Iqaluit+April1,1999 and51NunavutAct1993cameintoeffect1999 supportsretainedexplanation, no outdatedpopulation/membercount. CorrectnoteNunavutlargestCanadaterritory adds own-optionarearanking beyondwholeprompt/keymajorityarchipelagoextent. ESA21andCanada25/52directlybind; distinctcomparison notmerekeyrepeat.', 'OnlyAlaskanote3 changed toexactNPSUtqiagviknorthernmostUScity afterpreviousoneAlaskaGovfail+oneofficialNPSsuccess, no oldclausefalseclaim/no retry. NPSstate/UScitycontextqualifiedinference forwrongoptionjurisdiction, GreenlandDenmark/NorwaySvalbard ownnotes directlybound. All6literal4wholevariants/credible4realArcticjurisdictions/unique/grammar/polartaxonomy/absoluteMEDIUMregionalterritoryrecognition no boundarycoordinates/expertstatuteindex.', 'Global11000/same100/full115actualbodies/32bilateral/genuine28-30 exactcurrent. Distinct fromNunavutadministrativeCanadianmembership vs MAIN31majorityarchipelagoextent; allactualclosestandbothinverse relations independentlyjudge, no crossnoteban/genreban. Sourcefirstraw626394pre2/root/source/OTHER<2/exactQA19/independentFIRSTINITIAL/preleasedbinding beforecredit; one directedfixthenFINAL/HOLD0 noordinary2/reset. Parks25cert876 consumed, OTHERidle; apply31onlyfreshallactualpeer match.']
r=a.apply(B,'01a1447f-53aa-73f0-b307-03a735f3bb43',[31],D/'apply-polar31-original.json',D/'qa-polar31-original.json',pathlib.Path(__file__),qualifyOnly=True,peerSnapshot={'actualCurrentPeers':[p for p in ps['actualCurrentPeers'] if p['topicId']=='polar-regions']},concerns=concerns);r.update(sourceOriginalFreeze=freeze,nativeCompactions=counts,allActualFullBodiesVerified=len(ps['actualCurrentPeers']),primaryContexts=contexts)
m.write(B/'normalization-provenance.json',{'owner':m.O,'originalSOURCEfreeze':freeze,'operations':'Byte-equivalent JSON reserialization only; candidate, proof and peers judgments unchanged. No semantic aliases needed.','files':[{'name':n,'originalRawSHA256':m.raw(R/n),'normalizedRawSHA256':m.raw(B/n)} for n in ['candidate.json','sourceproof.json','peer-snapshot.json']]})
m.write(D/'qualification-polar31-original.json',r)
print(m.savecode([p for p in B.rglob('*') if p.is_file()]+[D/'qualification-polar31-original.json',pathlib.Path(__file__)],'Qualify pre2 exact original polar31 SOURCE full live peer bindings no credit'))
