"""Qualify exact original polar26-original SOURCE with fullbody aliases only; zero quality credit."""
import pathlib,importlib.util,subprocess
D=pathlib.Path(__file__).parent;C=D.parents[3];OLD=D.parent/'coordinator-01a14377'
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('own',D/'owned-tools.py');a=load('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a.P=m.P;g=load('primary',D/'primary-inspectability-preflight.py')
R=D/'source-polar25-26-original';B=D/'qualified-polar26-original';B.mkdir(exist_ok=True);freeze='830c2becd0381555e71593e277a96c28d58f8576'
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
concerns=['Originalpolar26 FIRSTINITIAL, no priorreview. MAIN/all4labels/key0/EASY retained; correctnote repeatsdefinition replacedownseaiceopticalproperty greaterusualsolarreflectionthanopenocean, concretefactbeyondwholeprompt/key directfreeze. Shelfnote addedusually torespectcompleteNSIDC shelfexceptions, othergoodtextretained. No25HOLD/NotReviewedpromotion25stillunreviewed.', 'FourfullretainedNSIDC QuickFactsSeaIce192line/glaciers318line/shelves192line/originalLarsenOPEN666fullarticle personallyreadSOURCE7f exactnew26claim applicability, no newfetch/PASSinheritance. QuickFactsL70oceanfreezes vslandorigin genotypes/L75-L76reflection qualitativeusually no fabricatedallconditionspercent. ShelfdefinitionL68-L78 andLarsenL123 acknowledges someshelvesentireseaice vsmostlandfed; independentlyjudgewhole26explanationicebergcontrastandnote1 under scientificscope ratherthansilentlyignoreexception. FullMAIN directgenesis term vsstablecoastmorphologicalshelf category.', 'All6literal4wholevariants/4credibleiceforms/unique/namebydirectorigin vsicebergcalving/glacierlandflow/shelfextension/grammar/taxonomy, broadadultEASY formationno physicalspecialist jargon. Hard25fraizl comparisonactualoldbody notSOURCEdecision. Global11000/same100/fullactualwholepeerhashes and22meaningfulbilateralERVC/directreverse; closest ocean27phaseprocessterm vs26materialname distinction explicitlyjudge, physicsicestate/freezingtemperature notgenetictype, current9iceberg10glacier27shelf definitions differentobjects/relations notautomaticallysameMAINtemplate/no crossnoteban.', 'SOURCE7fpre2critical3/raw830c allhistoricalrawcontexts unchangedandlineagefrozen, testedtopicQA19/independentINITIAL/root<2/preleaseCAS beforecredit. FirstINITIALFIX one directedSOURCEcycle thenFINAL unresolvedHOLD0/noordinary2/reset. Source25stillunreviewedinput noquality; boundedTreaty21/22HOLD remainsindependentnotreopened.']
r=a.apply(B,'01a1447f-53aa-73f0-b307-03a735f3bb43',[26],D/'apply-polar26-original.json',D/'qa-polar26-original.json',pathlib.Path(__file__),qualifyOnly=True,peerSnapshot={'actualCurrentPeers':[p for p in m.read(B/'peer-snapshot.json')['actualCurrentPeers'] if p['topicId']=='polar-regions']},concerns=concerns);r.update(primaryInspectabilityPreflight=pre,allActualFullBodiesVerified=len(m.read(B/'peer-snapshot.json')['actualCurrentPeers']),sourceOriginalFreeze=freeze);m.write(D/'qualification-polar26-original.json',r)
print(m.savecode([p for p in B.rglob('*') if p.is_file()]+[D/'qualification-polar26-original.json',pathlib.Path(__file__),D/'primary-inspectability-preflight.py'],'Qualify original polar26-original exact SOURCE fullbody bindings no quality credit'))
