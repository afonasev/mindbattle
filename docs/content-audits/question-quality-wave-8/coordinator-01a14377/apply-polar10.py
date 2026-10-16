"""Apply exact originalpolar10 sourcepacket; noqualitycredit before independentPASS."""
import pathlib,importlib.util,sys,json
D=pathlib.Path(__file__).parent;C=D.parents[3]
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('own',D/'owned-tools.py');a=load('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a.P=m.P;B=D/'source-polar8-10/order10';ps=m.read(B/'peer-snapshot.json')
for p in ps['actualCurrentPeers']+ps['relevantCrossTopicCurrentPeers']:
 q=next(q for q in m.read(C/f"src/content/topics/{p['topicId']}.json")['questions'] if q['id']==p['id']);assert q==p['card'] and m.sha(q)==p['sha256']
assert 'polar-regions-antarctic-circle-south' in m.read(m.P/'openspec/changes/question-quality-future-waves/current-checkpoint.json')['currentEligibleCompletedIds']
r=a.apply(B,'01a14381-0dc6-7740-9baf-4bc1f33f27ba',[10],D/'apply-polar10.json',D/'qa-polar10.json',pathlib.Path(__file__),qualifyOnly='--qualify-only' in sys.argv,peerSnapshot={'actualCurrentPeers':ps['actualCurrentPeers']},concerns=['Originalpolar10 firstINITIAL. Sourceproperownnote glacierformation snow/firn/ice beyondpromptgravityflow; fullNSIDCglacier/seaice/iceshelf personalprimary all6literal4wholevariants required.','Fullactual9+historicalproposal/actual8 andclosestcrossgeology glacierdefinition mustcompare bothwaysERVC/directreverse; generic polar/ice wrapper insufficient, distinguish landflowdefinition vs floatingice/formation/globalglacierpeers.','AbsoluteEASY/onekey/distractorplausibility andcorrectnotefact/wholevarianttruth judgedindependently, no sourceorQAinheritance.'])
if '--qualify-only' in sys.argv:
 m.write(D/'qualification-polar10.json',r);print(m.savecode([D/'qualification-polar10.json',D/'sourcefreeze-polar10.json',pathlib.Path(__file__)],'Qualify exactoriginalpolar10 source6literal4variants/currentpeers'))
