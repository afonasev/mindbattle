"""Apply two sole SOURCE cycle1 candidates; independent FINAL pending, no credit."""
import pathlib,importlib.util,subprocess
C=pathlib.Path(__file__).resolve().parents[4];D=pathlib.Path(__file__).parent
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('own',D/'owned-tools.py');a=load('app',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a.P=m.P
jobs=[('qualified-chetham71-cycle1-source25','01a14225-6301-72d2-9e92-1e1b62912ca2',[71],'apply-final71-cycle1-source25.json'),('qualified-foxing98-cycle1-source08','01a14208-996a-7b33-9397-bad2658d0551',[98],'apply-final98-cycle1-source08.json')]
for name,actor,orders,out in jobs:
 B=D/name;ps=m.read(B/'peer-snapshot.json')['actualCurrentPeers']
 for p in ps:
  t=m.read(C/f"src/content/topics/{p['topicId']}.json");assert p['card']==next(q for q in t['questions']if q['id']==p['id']) and m.sha(p['card'])==p['sha256']
 q=a.apply(B,actor,orders,D/out,D/'qa-final71-98-cycle1.json',pathlib.Path(__file__),qualifyOnly=True,peerSnapshot={'actualCurrentPeers':[p for p in ps if p['topicId']=='books-publishing']});print('preflight',orders,len(q['finalGroupBindings']),len(q['finalVariantBindings']))
tp=C/'src/content/topics/books-publishing.json';assert tp.read_bytes()==subprocess.check_output(['git','-C',str(C),'show','refs/heads/codex/question-quality-wave-6:src/content/topics/books-publishing.json'])
for name,actor,orders,out in jobs:
 B=D/name;ps=m.read(B/'peer-snapshot.json')['actualCurrentPeers'];a.apply(B,actor,orders,D/out,D/'qa-final71-98-cycle1.json',pathlib.Path(__file__),peerSnapshot={'actualCurrentPeers':[p for p in ps if p['topicId']=='books-publishing']})
