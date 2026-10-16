"""Qualify exact original polar25-original SOURCE with fullbody aliases only; zero quality credit."""
import pathlib,importlib.util,subprocess
D=pathlib.Path(__file__).parent;C=D.parents[3];OLD=D.parent/'coordinator-01a14377'
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('own',D/'owned-tools.py');a=load('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a.P=m.P;g=load('primary',D/'primary-inspectability-preflight.py')
R=D/'source-polar25-original';B=D/'qualified-polar25-original';B.mkdir(exist_ok=True);freeze='0dbc8f634dd6ea2e698493cd70dbc18cd6211ea7'
for p in R.rglob('*'):
 if p.is_file():assert p.read_bytes()==subprocess.check_output(['git','-C',str(C),'show',freeze+':'+str(p.relative_to(C))])
provenance=[]
for name in ['candidate.json','sourceproof.json','peer-snapshot.json']:
 doc=m.read(R/name)
 if name=='peer-snapshot.json':
  peers=doc['actualCurrentPeers'];seen=set();combined=[]
  for p in peers:
   p=dict(p);p['sha256']=p.get('sha256',p.get('canonicalSHA256'));assert p['id'] not in seen;seen.add(p['id']);assert m.sha(p['card'])==p['sha256']
   live=next(q for q in m.read(C/f"src/content/topics/{p['topicId']}.json")['questions'] if q['id']==p['id']);assert p['card']==live;combined.append(p)
  doc['actualCurrentPeers']=combined
 m.write(B/name,doc);provenance.append({'file':name,'rawSource':str((R/name).relative_to(C)),'rawSHA256':m.raw(R/name),'normalizedSHA256':m.raw(B/name)})
m.write(B/'normalization-provenance.json',{'owner':m.O,'originalSOURCEfreeze':freeze,'operations':'Only existing full actual body/hash rows copied without semantic change. All judgments and candidate unchanged.','files':provenance})
pre=g.inspect_packet(C,B);assert not any(x['headerOnlyNoVisiblePageBody'] for x in pre)
concerns=['Originalpolar25 FIRSTINITIAL firstactualSOURCE fromearlierunreviewednotHOLD. FrozenHARD/key3/all4labels preserved. Sameinitialloosemarinecrystalbeforecontinuoussheet MAIN, removedonlyunestablishedsupercooledadjective withoutclaimfalse. WMOoriginallibraryheader/shell notprimaryproof, soleofficialNSIDCScienceSeaIcefull541linealternative completecontext currentfacts, no failedroute retry/bypass/snippetproof.', 'FullNSIDC articleL65-L74categories/L78-L93formation/L108-L124saltbrine/L161-L176polynyas/L191-L194fastice personallyreadSOURCE. L84initialsmallneedlelikefrazilcrystals floataccumulatebondandexpelsalt/nearlyfresh; L85continuousnilas/L88wavepancakedisksraisededges/L171shorebottomanchoredfastice. No unverifiednilaselasticmatte/fasticeicefrontclause retained. Owncorrectnote nearlysaltfreeCRYSTALS expelsalttosurroundingwater beyondWHOLEprompt/keymorphology; surroundingliquidbrinepockets betweencrystals distinctfrombulknewsaltyice, do notclaimallnewseaicefresh.', 'All6literal4wholevariants/4credibleiceforms/unique/directinitialcrystalterm /HARDspecificknowledgeactualnotmathgate/approvedpolarphysicaltaxonomy/grammar. IndependentlyjudgeRussian descriptivekeyледяныеиглы mappingneedlelikefrazilinactualmarinecontext, notclaimverifiedofficialWMORussiantranslation; distinguishatmosphericice-needlecontexts/main ifrelevant. Global11000/same100/allactualwholepeers/genuineproposals/mutual25/26/bothdirectionsERVC/directreverse; genericseaice26directfreeze material vs25initialcrystalmorphology/premadesheet, nilas/pancake/fasticeetc distinguishspecificrelations nottemplateban/no crossnoteban.', 'Original26CURRENTcf49body underFIRSTINITIALpendingexplanationFIX/FINALreceipt notyetconsumed atqualification; no25applyuntiltopicfencelift. Source25raw0dbc/fullcritical3native0pre2, one affected19QA/independentINITIAL/root<2/preleasedCAS beforecredit. Rootwillapply25BEFOREfuture26SOURCEcycle1 fix so25sourcefull26peerbodyhash remainsactual through25FIRSTINITIAL. 26fix sourcewillread25newactual, but26actualfixapply waits25INITIALconsumed toavoidpeerdrift. One directedSOURCEfixthenFINAL unresolvedHOLD0/noordinary2/reset.']
r=a.apply(B,'01a1447f-53aa-73f0-b307-03a735f3bb43',[25],D/'apply-polar25-original.json',D/'qa-polar25-original.json',pathlib.Path(__file__),qualifyOnly=True,peerSnapshot={'actualCurrentPeers':[p for p in m.read(B/'peer-snapshot.json')['actualCurrentPeers'] if p['topicId']=='polar-regions']},concerns=concerns);r.update(primaryInspectabilityPreflight=pre,allActualFullBodiesVerified=len(m.read(B/'peer-snapshot.json')['actualCurrentPeers']),sourceOriginalFreeze=freeze);m.write(D/'qualification-polar25-original.json',r)
print(m.savecode([p for p in B.rglob('*') if p.is_file()]+[D/'qualification-polar25-original.json',pathlib.Path(__file__),D/'primary-inspectability-preflight.py'],'Qualify original polar25-original exact SOURCE fullbody bindings no quality credit'))
