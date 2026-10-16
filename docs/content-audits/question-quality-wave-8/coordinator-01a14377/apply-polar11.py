"""Apply originalpolar11 exactfullprimarySOURCE; noqualitycredit withoutindependentPASS."""
import pathlib,importlib.util,sys
D=pathlib.Path(__file__).parent;C=D.parents[3]
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('own',D/'owned-tools.py');a=load('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a.P=m.P;B=D/'qualified-polar11-standard-full-primary';ps=m.read(B/'peer-snapshot.json')
for p in ps['actualCurrentPeers']+ps['relevantCrossTopicCurrentPeers']:
 q=next(q for q in m.read(C/f"src/content/topics/{p['topicId']}.json")['questions'] if q['id']==p['id']);assert q==p['card'] and m.sha(q)==p['sha256']
r=a.apply(B,'01a14381-0dc6-7740-9baf-4bc1f33f27ba',[11],D/'apply-polar11.json',D/'qa-polar11.json',pathlib.Path(__file__),qualifyOnly='--qualify-only' in sys.argv,peerSnapshot={'actualCurrentPeers':ps['actualCurrentPeers']},concerns=['Original11 firstINITIAL. Sourcefirstmanualexcerpts rejected/unapplied, completeexactoriginalnativeFWS/AAPweboutputs transported withprovenance andSourcepersonallyread/adopted atactual1; chosencritical3newfreeze pre2. Independentmustpersonallyreadfullrelevantcontexts, no sourceorrootPASS.','ActualMAIN geographicdistribution ArcticvsAntarctic, notgeneralfeedinganatomy; fullapprovedpolartaxonomy/antiOverlap mustjudge substantively. Fullactualanimals9polarBearhuntingseals+otherpenguin/seal/Antarcticbreeding peers bothdirectionsERVC/directreverse; speciesnamewrapperinsufficient. Owncorrectnoteseaiceplatformhuntingseals beyondgeographicMAIN mayoverlapothercardkey, no crossnoteban.','FWSsourceURLofficialPDF witholdpolicysectionsnotused forcurrentstatus; onlyretainedhabitat/dietgeography facts; actualAAPEmperor/Weddell/Adelie fulloriginalopenbody required forallwrongnotes. Supplementaryheaders/errorsdiagnosticnotproof; no refetch/retry simplynewactor.'])
if '--qualify-only' in sys.argv:
 m.write(D/'qualification-polar11.json',r);print(m.savecode([D/'qualification-polar11.json',pathlib.Path(__file__)],'Qualify originalpolar11 fullprimary6literal4variants/currentpeers'))
