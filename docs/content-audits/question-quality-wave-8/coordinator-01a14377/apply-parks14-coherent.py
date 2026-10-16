"""Exact coherentSOURCE14 pendingfirstFINAL; noqualitycredit fromapply."""
import pathlib,importlib.util
D=pathlib.Path(__file__).parent;C=D.parents[3]
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('own',D/'owned-tools.py');a=load('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a.P=m.P;B=D/'qualified-parks14-coherent';ps=m.read(B/'peer-snapshot.json')
assert len(m.read(m.P/'openspec/changes/question-quality-future-waves/current-checkpoint.json')['currentEligibleCompletedIds'])==852
for p in ps['actualCurrentPeers']:
 live=next(q for q in m.read(C/f"src/content/topics/{p['topicId']}.json")['questions'] if q['id']==p['id']);assert p['card']==live and m.sha(live)==p['sha256']
g=load('primary',D/'primary-inspectability-preflight.py');assert not any(x['headerOnlyNoVisiblePageBody'] for x in g.inspect_packet(C,B));q=m.read(D/'qualification-parks14-coherent.json')
a.apply(B,'01a143ee-4310-7b72-bd13-773da4151e3a',[14],D/'apply-parks14-coherent.json',D/'qa-parks14-coherent.json',pathlib.Path(__file__),peerSnapshot={'actualCurrentPeers':[p for p in ps['actualCurrentPeers'] if p['topicId']=='national-parks-nature']},concerns=q['editorialConcernsForOTHER']+['15NEWlanguage FINALstrictcert852 alreadyconsumed; accepted15hash58c preserved. SOURCE16onlyproposalongoing, no16mutationuntil14receiptconsumed.'])
