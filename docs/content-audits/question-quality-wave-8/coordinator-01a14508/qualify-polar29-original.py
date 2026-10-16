"""Qualify pre2 SOURCE29 exact card/primary hashes/live fullpeers; zero credit."""
import pathlib,importlib.util,subprocess,json,re
D=pathlib.Path(__file__).parent;C=D.parents[3]
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('own',D/'owned-tools.py');a=load('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a.P=m.P
R=D/'source-polar29-40-continuation';B=D/'qualified-polar29-original';B.mkdir(exist_ok=True);freeze='d02ff711cc9bf2e3b2a09f4f888dea4ce1e67b34'
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
concerns=['Original29 FIRSTINITIAL; concrete originalMAIN duplicate withactualislands45NorwegianSvalbard identified, genuine authored newTreaty equalhunting/fishing guarantee MAIN. FrozenMEDIUM/key1/id/topic/order/labels; no arbitrarylevelchange. Sourcefirstraw d02ffpre2, fullprimary reusedinplace withpersonalread; no sourcefetchretry.', 'Norway§2.2L215-220nondiscrimination/equalrightsforTreatypartynationals/companies onhunting/fishing, localregulation/prohibitionstillpossibleL217/219. No unlimitedhunting/maritimeEEZinterpretation/generalimmigrationright claim. Entire§2.2L161-264 actual0-271of680chapter; nevercallfull680. Other3fullcontexts ascoverage-index Greenland153/Canada102/NPS270; Alaskagovoncefailed+officialNPSalternative no retry. Note2 changed toexactnorthernmostcityUtqiagvik only.', 'All6literal/4wholevariants sourcegrounded, uniquecredible4Arcticterritories/grammar/polartaxonomy/absoluteMEDIUM coreTreatythematicrule notrarearticleindex/courtcase. CorrectnoteNorwegiansovereignty concreteown-optionfact beyondnewwholeprompt/keyhuntingfishing; overlapMAINelsewherepermitted/no crossnoteban. All112actualwholebodies/33bilateral/global11000/same100/relevantgenuine28 exact465d actual. Directreverse compareislands45explicitly new29 resourceequalityvsoldgeography/specialTreatyname, Greenland28jurisdiction/Framdrift/economicterms all distinctrelations.', 'No contentapply whilepolar28FIRSTINITIALactive: source29fullactualpeer28mustremainstable; wait28consume then apply29 withfresh112wholebodypreimage. One directedfixcycle thenFINAL/HOLD0/noordinary2/reset. Root/source/reader<2 andmandatoryprelease beforecertification retained.']
r=a.apply(B,'01a1447f-53aa-73f0-b307-03a735f3bb43',[29],D/'apply-polar29-original.json',D/'qa-polar29-original.json',pathlib.Path(__file__),qualifyOnly=True,peerSnapshot={'actualCurrentPeers':[p for p in ps['actualCurrentPeers'] if p['topicId']=='polar-regions']},concerns=concerns);r.update(sourceOriginalFreeze=freeze,nativeCompactions=counts,allActualFullBodiesVerified=len(ps['actualCurrentPeers']),primaryContexts=contexts)
m.write(B/'normalization-provenance.json',{'owner':m.O,'originalSOURCEfreeze':freeze,'operations':'Byte-equivalent JSON reserialization only; candidate, proof and peers judgments unchanged. No semantic aliases needed.','files':[{'name':n,'originalRawSHA256':m.raw(R/n),'normalizedRawSHA256':m.raw(B/n)} for n in ['candidate.json','sourceproof.json','peer-snapshot.json']]})
m.write(D/'qualification-polar29-original.json',r)
print(m.savecode([p for p in B.rglob('*') if p.is_file()]+[D/'qualification-polar29-original.json',pathlib.Path(__file__)],'Qualify pre2 exact original polar29 SOURCE full live peer bindings no credit'))
