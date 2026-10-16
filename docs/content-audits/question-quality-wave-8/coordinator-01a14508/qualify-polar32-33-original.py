"""Qualify pre2 SOURCE32_33 exact card/primary hashes/live fullpeers; zero credit."""
import pathlib,importlib.util,subprocess,json,re
D=pathlib.Path(__file__).parent;C=D.parents[3]
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('own',D/'owned-tools.py');a=load('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a.P=m.P
R=D/'source-polar32-40-continuation';B=D/'qualified-polar32-33-original';B.mkdir(exist_ok=True);freeze='62e22671d7be59284b54d6aa2dd2fe6938c04228'
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
 p=C/c['path'];assert m.raw(p)==c['rawSHA256'];body=m.read(p) if p.suffix=='.json' else p.read_text();assert isinstance(body,str)
 if c['id']=='nasaAurora':body=body[body.index('turn27view0'):body.index('turn27view1')]
 elif c['id']=='nsidcPermafrost':body=body[body.index('turn27view1'):]
 ids={int(n) for n in re.findall(r'\bL([0-9]+):',body)};assert ids==set(range(c['declaredPageLines'])),(c['id'],len(ids));assert c['completeRelevantContextPersonallyRead'];contexts.append({**c,'rootActualVisibleLineIdsRecomputed':len(ids),'rootMissingLabels':[]})
for p in ps['relevantGenuineProposals']:
 assert m.sha(p['card'])==p['sha256'];doc=m.read(C/p['sourcePath']);e=next(e for e in doc['entries'] if e['id']==p['id']);assert e['proposedCard']==p['card'] and e['afterHash']==p['sha256']
concerns=['Original32/33 paired FIRSTINITIAL, goodMAIN/all4labels/explanations/EASYkey2/3wrongnotes retained. Correctnotes merewholeprompt/key predicate repeats replacedonlywith ownnewconcretefacts:32summerpolarmonthscontinuousdaylightAAP317;33possibleMawsonwintertwilightdespitenoSunriseAAP309-310. No allnightsalwayslight/totalblacknessclaim or exacthorizonrefractionboundary assertion.', 'Fourcompleteprimarycontexts AAP379allIDs0-378/scientificarticle298-339, NOAA258fullpage/completeFAQ114-143+163-176 personallyread, NASAactualfull6IDs0-5science4-5 (fictionfill-in1-2 NOTproof), NSIDC193fullpage/science66-136 temperaturedefinition76-77permafrost>=2years<=0Cnoticecontent. Rootdecoded NASA/NSIDCrawJSONstring exactseparatecitationblocks andlineIDsets notconflated; no TotalLines-only/header/snippetproof. No visibleaudio/videoautoplay/source fetching byroot.', 'All6literal4wholevariants/fullprimary/uniquekey2/grammar/absoluteEASY basicpolarSunpredicate vocabulary. Independently assess ALL FOUR distractors credibility/comparable category with FULL prompt asking a period: permafrost is groundthermalstate andauroraemission ratherthansolarperiod; authorgrounds exclusions do not themselves prove plausiblealternatives. Do not inheritSOURCEPASS or excusetextbecauseoriginalunchanged. Ifactualdefect giveexactboundedscope onefixcycle, notrootinventednewoptions.', 'Global11000/same100/full108actualwholebodies/38bilateral+mutualproposed32versus33 bothdirections/directreverse. Explicitabove/noSunsetday versusbelow/noSunrisenight distinctconditions/values, inverseeachdefinesdifferentphenomenon; no templatealoneban/no crossnoteban forcanonicalothernotes. Independentlyjudgefullmutualpairs asCURRENTbothapplied, notbeforehashes. Sourcefirstraw62e226pre2/root/source/OTHER<2/exactaffected19/independentFIRSTINITIAL/preleasedbinding beforeuniquecredit; one directedfixthenFINAL/unresolvedHOLD0/noordinary2/reset.']
r=a.apply(B,'01a1447f-53aa-73f0-b307-03a735f3bb43',[32,33],D/'apply-polar32-33-original.json',D/'qa-polar32-33-original.json',pathlib.Path(__file__),qualifyOnly=True,peerSnapshot={'actualCurrentPeers':[p for p in ps['actualCurrentPeers'] if p['topicId']=='polar-regions']},concerns=concerns);r.update(sourceOriginalFreeze=freeze,nativeCompactions=counts,allActualFullBodiesVerified=len(ps['actualCurrentPeers']),primaryContexts=contexts)
m.write(B/'normalization-provenance.json',{'owner':m.O,'originalSOURCEfreeze':freeze,'operations':'Byte-equivalent JSON reserialization only; candidate, proof and peers judgments unchanged. No semantic aliases needed.','files':[{'name':n,'originalRawSHA256':m.raw(R/n),'normalizedRawSHA256':m.raw(B/n)} for n in ['candidate.json','sourceproof.json','peer-snapshot.json']]})
m.write(D/'qualification-polar32-33-original.json',r)
print(m.savecode([p for p in B.rglob('*') if p.is_file()]+[D/'qualification-polar32-33-original.json',pathlib.Path(__file__)],'Qualify pre2 exact original polar32-33 SOURCE full live peer bindings no credit'))
