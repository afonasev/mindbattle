"""Qualify exact original parks21-original SOURCE with fullbody aliases only; zero quality credit."""
import pathlib,importlib.util,subprocess
D=pathlib.Path(__file__).parent;C=D.parents[3];OLD=D.parent/'coordinator-01a14377'
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('own',D/'owned-tools.py');a=load('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a.P=m.P;g=load('primary',D/'primary-inspectability-preflight.py')
R=D/'source-parks21-22-original';B=D/'qualified-parks21-original';B.mkdir(exist_ok=True);freeze='cf025128a3bcb8c37eaef57d888ee74d7a013f98'
for p in R.rglob('*'):
 if p.is_file():assert p.read_bytes()==subprocess.check_output(['git','-C',str(C),'show',freeze+':'+str(p.relative_to(C))])
provenance=[]
for name in ['candidate.json','sourceproof.json','peer-snapshot.json']:
 doc=m.read(R/name)
 if name=='peer-snapshot.json':
  peers=doc['actualCurrentPeers']+doc['fullRelevantHits'];seen=set();combined=[]
  for p in peers:
   p=dict(p);p['sha256']=p.get('sha256',p.get('canonicalSHA256'));assert m.sha(p['card'])==p['sha256']
   if p['id'] in seen:
    assert next(x for x in combined if x['id']==p['id'])['card']==p['card'];continue
   seen.add(p['id'])
   live=next(q for q in m.read(C/f"src/content/topics/{p['topicId']}.json")['questions'] if q['id']==p['id']);assert p['card']==live;combined.append(p)
  doc['actualCurrentPeers']=combined
 m.write(B/name,doc);provenance.append({'file':name,'rawSource':str((R/name).relative_to(C)),'rawSHA256':m.raw(R/name),'normalizedSHA256':m.raw(B/name)})
m.write(B/'normalization-provenance.json',{'owner':m.O,'originalSOURCEfreeze':freeze,'operations':'Only actualCurrentPeers unions existing full actual same-topic and relevant global hit bodies and adds sha256 alias from existing canonicalSHA256. All judgments and candidate unchanged.','files':provenance})
pre=g.inspect_packet(C,B);assert not any(x['headerOnlyNoVisiblePageBody'] for x in pre)
concerns=['Originalparks21 FIRSTINITIAL, no priorindependentreview. Preservegoodprompt/all4labels/EASYkey0/explanation. Correctnoteunsupportedwestpartsimplification replacedexplicitUNESCO303/355 sharedsignificantAtlanticForestremnant beyondwholeprompt/keyDevilsThroatArgentinapark. Brazilnote unsupportedexacteastbank replacedUNESCO355L51Parana+adjacency. Vatnajokullnotelargesticelandrank notgrounded replacesonlysuperlativewithsame-nameicecapandactualsubglacialactivevolcanoes. Plitviceaccuratetravertineunchanged.', 'Full6officialprimarycontexts personallyreadSOURCE: UNESCO303/355/98/1604 fullOUV/integrity/management context, APNArgentinagovactivities/node284859 actualGargantadelDiablo inIguazunationalpark, municipalDestinoFozBrazil officialattractions+authorityfooter. APNL46-L48/94/sidebar115-129 connectnamedfallandArgentinepark. UNESCO303forest/subtropicalcascades plusBrazil275falls supportsunchangedbroadhundreds no precisevariablecount. Exactclaimgeographicwording no west/eastbank inference/rankfallback.', 'Whole4variants crediblewaterfall/waterlandscapeprotectedparks, Argentinacondition distinguishesunqualifiedIguazu fromexplicitBrazil label notsecondkey; 21promptdoesnotgiveIguazuname. AbsoluteEASY groundedlargeArgentine/Brazilian culturaladultdemographic iconicIguazu/DevilsThroat (broadadultorlargeculturaldemographicallowed), notclaimuniversaleveryRussianorrelativeEASY. Independentlyjudge realcalibration/credibleVatnajokull vswaterfalllabel, no changefrozengrade. Approvedprotectednaturetaxonomy.', 'Global11000/same100/fullclosestwholeactualbodyhashes+genuineproposals/mutual21/22/bothdirectionERVC/directreverse, specificwaterfallparks vsriver/waterfallidentity. Original22 SOURCEHOLD source-majorityofcascades missing andpromptgivesname+country almostsolelabel, cannotpromotebecause21PASS orsharedsource. All22oldcardunchanged/zero; noautomaticreset/genuineNEWrequiresactualsolution. All6literal4wholevariantper21critical3pre2cf025/source3aactual1/testedtopicQA19/independentINITIAL required. One directedSOURCEfixthenFINAL unresolvedHOLD0/noordinary2/reset.']
r=a.apply(B,'01a1443a-30c4-73f1-bbf5-2df86115a910',[21],D/'apply-parks21-original.json',D/'qa-parks21-original.json',pathlib.Path(__file__),qualifyOnly=True,peerSnapshot={'actualCurrentPeers':[p for p in m.read(B/'peer-snapshot.json')['actualCurrentPeers'] if p['topicId']=='national-parks-nature']},concerns=concerns);r.update(primaryInspectabilityPreflight=pre,allActualFullBodiesVerified=len(m.read(B/'peer-snapshot.json')['actualCurrentPeers']),sourceOriginalFreeze=freeze);m.write(D/'qualification-parks21-original.json',r)
print(m.savecode([p for p in B.rglob('*') if p.is_file()]+[D/'qualification-parks21-original.json',pathlib.Path(__file__),D/'primary-inspectability-preflight.py'],'Qualify original parks21-original exact SOURCE fullbody bindings no quality credit'))
