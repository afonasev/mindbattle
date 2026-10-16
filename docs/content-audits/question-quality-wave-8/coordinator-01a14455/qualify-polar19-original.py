"""Qualify exact original polar19-original SOURCE with fullbody aliases only; zero quality credit."""
import pathlib,importlib.util,subprocess
D=pathlib.Path(__file__).parent;C=D.parents[3];OLD=D.parent/'coordinator-01a14377'
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('own',D/'owned-tools.py');a=load('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a.P=m.P;g=load('primary',D/'primary-inspectability-preflight.py')
R=D/'source-polar19-sol-original';B=D/'qualified-polar19-original';B.mkdir(exist_ok=True);freeze='e682f261b29cf02d4b361db3867895f524e6f461'
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
m.write(B/'normalization-provenance.json',{'owner':m.O,'originalSOURCEfreeze':freeze,'operations':'Only existing101 full actual body/hash rows copied without semantic change. All judgments and candidate unchanged.','files':provenance})
pre=g.inspect_packet(C,B);assert not any(x['headerOnlyNoVisiblePageBody'] for x in pre)
concerns=['Originalpolar19 FIRSTINITIAL. Originalunfinishedsourcegap addressed bynarrowing geographicalpredicatetosouthernendWeddell perBASL152, labels/id/topic/order/MEDIUM/key3retained. Unsupportedmajorityarea/two-partsdivideclaim omitted notdeclaredfalse. No newindependentMAIN/reset/cycle: sameidentifyFilchnerRonnebysouthernWeddell relationship beforefirstreview.', 'PersonallyfullofficialBAShandbook198lines, completeBerknercontextL139-L159 andRonnecoastL78-L96; L142BerkneroneasternRonne icecoveredisland exactownkeynoteadditionalgeography beyondwholeprompt/key, L152southernendWeddellMAIN. No BASPDFchallenge/DOI retry/bypass/snippetproof. NSIDC fulloriginalOPEN666article supports remainingLarsenpresenttense easternPeninsula. FullAAP/NASAAmeryPrydzEastAntarctica andGetzMarieByrdLand retainedpreciseclaims independentlygrounded.', 'All6literal/4wholevariants, 4credibleAntarcticshelves andunique southernendgeography; MEDIUMthematicpolar mapknowledge, optionalBerknerfact notasked. Approvedpolarphysicalgeographytaxonomy. Global11000/all100sameMAIN/full101actualbodies+semanticbilateralMAINAssessments ERVC/directreverse incl20exactnewaftere259 vs19distinctrelation, sharednotesnotMAINdup/no crossnoteban. Actual20SOURCE/readerPASSdoesnotaccept19.', 'SOURCE7fpre2critical3/fullrawe682, testedtopicexactCURRENT/QA19/independentINITIAL required. One directedSOURCEfixafterINITIAL thenFINAL unresolvedHOLD0/noordinarycycle2/reset. Sourceproof allraworiginalread personallyinownnative0, no newrequests required.']
r=a.apply(B,'01a1447f-53aa-73f0-b307-03a735f3bb43',[19],D/'apply-polar19-original.json',D/'qa-polar19-original.json',pathlib.Path(__file__),qualifyOnly=True,peerSnapshot={'actualCurrentPeers':[p for p in m.read(B/'peer-snapshot.json')['actualCurrentPeers'] if p['topicId']=='polar-regions']},concerns=concerns);r.update(primaryInspectabilityPreflight=pre,allActualFullBodiesVerified=101,sourceOriginalFreeze=freeze);m.write(D/'qualification-polar19-original.json',r)
print(m.savecode([p for p in B.rglob('*') if p.is_file()]+[D/'qualification-polar19-original.json',pathlib.Path(__file__),D/'primary-inspectability-preflight.py'],'Qualify original polar19-original exact SOURCE fullbody bindings no quality credit'))
