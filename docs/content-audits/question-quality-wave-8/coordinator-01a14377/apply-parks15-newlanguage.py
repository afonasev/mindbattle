"""Exact concreteNEWlanguage solution; originalFINALHOLD0 preserved, nofacts changed."""
import pathlib,importlib.util,sys
D=pathlib.Path(__file__).parent;C=D.parents[3]
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('own',D/'owned-tools.py');a=load('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a.P=m.P;B=D/'qualified-parks15-newlanguage';ps=m.read(B/'peer-snapshot.json');e=m.read(B/'candidate.json')['entries'][0];assert {k:v for k,v in e['beforeCard'].items() if k!='prompt'}=={k:v for k,v in e['proposedCard'].items() if k!='prompt'}
for p in ps['actualCurrentPeers']:
 live=next(q for q in m.read(C/f"src/content/topics/{p['topicId']}.json")['questions'] if q['id']==p['id']);assert p['card']==live and m.sha(live)==p['sha256']
g=load('primary',D/'primary-inspectability-preflight.py');assert not any(x['headerOnlyNoVisiblePageBody'] for x in g.inspect_packet(C,B));q=m.read(D/'qualification-parks15-newlanguage.json')
a.apply(B,'01a143ee-4310-7b72-bd13-773da4151e3a',[15],D/'apply-parks15-newlanguage.json',D/'qa-parks15-newlanguage.json',pathlib.Path(__file__),peerSnapshot={'actualCurrentPeers':[p for p in ps['actualCurrentPeers'] if p['topicId']=='national-parks-nature']},concerns=q['editorialConcernsForOTHER']+['14SOURCEcoherenttechnicalrecoverypending, notapplied andnoQUALITY. Allknownhistorical14Kili/fire1f846proposals retained; invalidmixed44c416ROOTrejected mustnotpromoteasqualifiedSOURCE. Latestcoherent14proposal mustreadwhenavailable, MAINfire vsfoundobject meaningunchanged.'])
