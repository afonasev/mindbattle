"""Qualify pre2 SOURCE32_33 exact card/primary hashes/live fullpeers; zero credit."""
import pathlib,importlib.util,subprocess,json,re
D=pathlib.Path(__file__).parent;C=D.parents[3]
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('own',D/'owned-tools.py');a=load('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a.P=m.P
R=D/'source-polar32-33-cycle1';B=D/'qualified-polar32-33-cycle1';B.mkdir(exist_ok=True);freeze='e8a82eef1758da6a5e3fdcbf2caa255ff2a62525'
counts={}
for uid in [m.O,'01a1447f-53aa-73f0-b307-03a735f3bb43','01a14483-ccd0-7321-bd23-2262fcb11e5b']:
 fs=list(pathlib.Path('/Users/eaafonasev/.codex/sessions/2026/10/16').glob('*'+uid+'.jsonl'));assert len(fs)==1;counts[uid]=sum(json.loads(l).get('type')=='compacted' for l in fs[0].open());assert counts[uid]<2
for p in R.rglob('*'):
 if p.is_file():assert p.read_bytes()==subprocess.check_output(['git','-C',str(C),'show',freeze+':'+str(p.relative_to(C))])
for name in ['candidate.json','sourceproof.json','peer-snapshot.json']:
 doc=m.read(R/name)
 if name=='candidate.json':
  for e in doc['entries']:
   assert e['status']=='READY_FOR_INDEPENDENT_FINAL';e['originalSOURCEReadinessStatus']=e['status'];e['status']='READY_FOR_INDEPENDENT_REVIEW' # generic technical application adapter; cycle1/FINAL retained, no new verdict
 m.write(B/name,doc)
ps=m.read(B/'peer-snapshot.json')
for p in ps['actualCurrentPeers']:
 assert m.sha(p['card'])==p['sha256'];live=next(q for q in m.read(C/f"src/content/topics/{p['topicId']}.json")['questions'] if q['id']==p['id']);assert live==p['card']
sp=m.read(B/'sourceproof.json');ci=sp['coverageIndex'];assert m.raw(C/ci['path'])==ci['sha256'];cov=m.read(C/ci['path']);contexts=[]
for c in cov['contexts']:
 p=C/c['path'];assert m.raw(p)==c['rawSHA256'];body=m.read(p) if p.suffix=='.json' else p.read_text();assert isinstance(body,str)
 if c['id'].startswith('nasa'):
  hs=list(re.finditer(r'cite[^]+ \[wordlim:[^\n]*Total lines: ([0-9]+)',body));selected=[k for k,h in enumerate(hs) if int(h.group(1))==c['declaredPageLines']];assert len(selected)==1;ix=selected[0];body=body[hs[ix].start():hs[ix+1].start() if ix+1<len(hs) else len(body)]
 ids={int(n) for n in re.findall(r'\bL([0-9]+):',body)};assert ids==set(c['actualUnionLineIds']) and len(ids)==c['distinctActualVisibleLineIds'],(c['id'],len(ids));assert c['completeRelevantContextPersonallyRead']
 if c['completePageCaptured']:assert ids==set(range(c['declaredPageLines']))
 else:
  needed=set(c['relevantCompleteLineIds']);assert needed and needed<=ids and needed==set(range(min(needed),max(needed)+1))
 contexts.append({'id':c['id'],'url':c['url'],'path':c['path'],'rawSHA256':c['rawSHA256'],'declaredPageLines':c['declaredPageLines'],'rootActualVisibleLineIdsRecomputed':len(ids),'fullPageCaptured':c['completePageCaptured'],'completeRelevantArticleLineIds':c.get('relevantCompleteLineIds'),'scopeAndLimits':c['selector']})
for p in ps['relevantGenuineProposals']:
 assert m.sha(p['card'])==p['sha256'];doc=m.read(C/p['sourcePath']);e=next(e for e in doc['entries'] if e['id']==p['id']);assert e['proposedCard']==p['card'] and e['afterHash']==p['sha256']
concerns=['SOLEcycle1 afterqualifiedFIRSTINITIAL32/33 FIX_DISTRACTORS_NOT_COMPARABLE_TO_SOLAR_PERIOD consumed86c56/66b72. Sourceonlyslots1/3 labels+notes changed tosummerwhiteNights anddaysofequinoxes plusnecessarysourcemetadata; prompt/key2/EASY/validsolarconditions/explanations/oppositeperiod0/newcorrectnote2preserved. Notmerelyperiod→phenomenon, nocorrectkeySynonyms; FINAL independentlywhetherall4arecrediblecomparableperiods anduniquekey.', 'Fourfullprimarycontexts: AAP379fullcaptured/scientific298-339 personallyread andNOAA258completeFAQ114-143/163-176 reusedinplace. NASA GSFC559declared page actual202visiblelabels only; COMPLETErelevantFAQ288L262-273 personallyread. NASA Marshall352declared page actual78visiblelabels only; COMPLETEscientificarticle254-267 includingbyline personallyread. Bothpartialpages explicitly NOTfull559/352, wholeoriginaltoolwindowsretained withaccuratecoverage; unrelatedFAQ/navigation/footer notclaimedcomplete. WhiteNightsSunSETS/dailyreturn longsummerTWILIGHT; equinoxnearlyequaldaynight withpolarqualification, no imported2022dateas2026. No exacteverylat12hours/equinoxSunatpolenormaldayassertion.', 'Slot1summerwhiteNights plausibleconfusion brightnight vscontinuousSunabove/noSunrise, butSunsetsandreturnsdailysofalseforboth>24hconditions. Slot3nameddaysofequinoxescivilcalendar/solar-time periods, nearlybalancedday/nightoutsidepoles; independentlyscopeandcredibility notpretendinstant/always12h everywhere. Notetruth andkey-extra AAP317polarmonths/309-310possiblewintertwilight unchanged. All6literal4wholevariants perID/fullprimary/grammar/unique/broadadultEASY; claimsnotinNASAscienceexcluded.', 'Global11000/same100/108fullactualbodies/38bilateral+mutualpairedproposedbothdirections/directreverse, authorcurrent32/33baselinea68/9cdfullbefore andcycle1after8e61/c463 distinctbindings. No templateban/no crossnoteban; sourcegenuine26courtesy16e3unappliedandunrelatedSolarperiod queriedasdiscoveryifapplicable. Root/source/reader<2, sourcefirstrawe8a82pre2/exactaffected19 thenindependentFINAL/preleasedbinding onlyquality. UnresolvedFINALHOLD0/noordinarycycle2/reset.']
for e in m.read(B/'candidate.json')['entries']:
 before=e['beforeCard'];after=e['proposedCard'];assert all(after[k]==before[k] for k in ['id','difficulty','correctIndex','prompt','explanation']);assert after['answers'][0]==before['answers'][0] and after['answers'][2]==before['answers'][2]

r=a.apply(B,'01a1447f-53aa-73f0-b307-03a735f3bb43',[32,33],D/'apply-polar32-33-cycle1.json',D/'qa-polar32-33-cycle1.json',pathlib.Path(__file__),qualifyOnly=True,peerSnapshot={'actualCurrentPeers':[p for p in ps['actualCurrentPeers'] if p['topicId']=='polar-regions']},concerns=concerns);r.update(sourceOriginalFreeze=freeze,nativeCompactions=counts,allActualFullBodiesVerified=len(ps['actualCurrentPeers']),primaryContexts=contexts)
m.write(B/'normalization-provenance.json',{'owner':m.O,'originalSOURCEfreeze':freeze,'operations':'Only READY_FOR_INDEPENDENT_FINAL→generic READY_FOR_INDEPENDENT_REVIEW technical application alias, original status/cycle1/FINAL retained. No content, source judgment, group/triplehash or semantic verdict changed. Accurate partial NASA page scopes audited, no full-page claim.','files':[{'name':n,'originalRawSHA256':m.raw(R/n),'normalizedRawSHA256':m.raw(B/n)} for n in ['candidate.json','sourceproof.json','peer-snapshot.json']]})
m.write(D/'qualification-polar32-33-cycle1.json',r)
print(m.savecode([p for p in B.rglob('*') if p.is_file()]+[D/'qualification-polar32-33-cycle1.json',pathlib.Path(__file__)],'Qualify pre2 exact original polar32-33 SOURCE full live peer bindings no credit'))
