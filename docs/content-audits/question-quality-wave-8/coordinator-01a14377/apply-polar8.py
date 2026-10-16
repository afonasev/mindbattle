"""Apply exact originalpolar8 qualifiedsource; creditzero untilindependent INITIAL."""
import pathlib,importlib.util,sys
D=pathlib.Path(__file__).parent;C=D.parents[3]
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('own',D/'owned-tools.py');a=load('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a.P=m.P;B=D/'source-polar8-10/order8-source-corrected';ps=m.read(B/'peer-snapshot.json')
for p in ps['actualCurrentPeers']+ps['relevantCrossTopicCurrentPeers']:
 q=next(q for q in m.read(C/f"src/content/topics/{p['topicId']}.json")['questions'] if q['id']==p['id']);assert q==p['card'] and m.sha(q)==p['sha256']
r=a.apply(B,'01a14381-0dc6-7740-9baf-4bc1f33f27ba',[8],D/'apply-polar8.json',D/'qa-polar8.json',pathlib.Path(__file__),qualifyOnly='--qualify-only' in sys.argv,peerSnapshot={'actualCurrentPeers':ps['actualCurrentPeers']},concerns=['Original8 firstINITIAL; sourcequalification corrected monthground beforeapply, no independentfixcycle yet. ActualsouthJune winterpolarNight/December summerpolarDay exactliterals+fullAAP locators, all6literal4variants independentlyjudge.','Fullcurrent7NorthernCircle boundaryofpossiblepolarday and8SouthernCircle latitude identity mustcompare fullERVC bothways, not hemispherelabelsalone. Source7 historicalproposal retained; checkactual7body/hash andstate, no inheritedsourcePASS.','Fouralternatives actualnamedparallels not poles, correctownnote DecemberpolarDayproperty beyondprompt/key; sourceURLNOAAlatitude exact, fullAAP secondarycontext retained. Absoluteeasy/onekey/protectedpolar taxonomy independentlyjudge.'])
if '--qualify-only' in sys.argv:
 m.write(D/'qualification-polar8.json',r);print(m.savecode([D/'qualification-polar8.json',D/'sourcefreeze-polar8.json',pathlib.Path(__file__)],'Qualify exactpolar8 source6literal4variants peers currentpreimage'))
