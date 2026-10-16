"""Exact two originalSOURCEcards on distincttopics; sharedaffected19snapshot, nocredit."""
import pathlib,importlib.util
D=pathlib.Path(__file__).parent;C=D.parents[3]
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('own',D/'owned-tools.py');a=load('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a.P=m.P;g=load('primary',D/'primary-inspectability-preflight.py')
for name,topic,order,uid in [('polar14','polar-regions',14,'01a14413-e1e7-7e71-a582-eeacf3b53189'),('parks16','national-parks-nature',16,'01a1443a-30c4-73f1-bbf5-2df86115a910')]:
 B=D/('qualified-'+name);ps=m.read(B/'peer-snapshot.json');assert not any(x['headerOnlyNoVisiblePageBody'] for x in g.inspect_packet(C,B))
 for p in ps['actualCurrentPeers']:
  live=next(q for q in m.read(C/f"src/content/topics/{p['topicId']}.json")['questions'] if q['id']==p['id']);assert p['card']==live and m.sha(live)==p['sha256']
 r=m.read(D/('qualification-'+name+'.json'));a.apply(B,uid,[order],D/('apply-'+name+'.json'),D/'qa-original14-16.json',pathlib.Path(__file__),peerSnapshot={'actualCurrentPeers':[p for p in ps['actualCurrentPeers'] if p['topicId']==topic]},concerns=r['editorialConcernsForOTHER']+['Sharedaffected19coversbothdistincttopicchanges afterbothapplies. OnlyINITIALnoqualitycredityet. No readeractiveon either topic; prior12strictcert853 consumed.'])
