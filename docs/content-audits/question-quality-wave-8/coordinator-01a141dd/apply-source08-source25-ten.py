"""Apply10 exact SOURCE candidates; no editorial credit. Affected19 follows separately."""
import pathlib,importlib.util,subprocess
C=pathlib.Path(__file__).resolve().parents[4];D=pathlib.Path(__file__).parent
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('own',D/'owned-tools.py');app=load('app',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');app.P=m.P
A=C/'docs/content-audits/question-quality-wave-8/process-v2-preservation5-fresh-01a141dd/author';B=D/'qualified-books6-source25';qa=D/'qa-source08-source25-ten.json'
ps=m.read(A/'peer-snapshot.json');pp=[]
for p in ps['actualCurrentGlobalMAINComparisons']:
 t=m.read(C/f"src/content/topics/{p['peerTopicId']}.json");c=next(q for q in t['questions'] if q['id']==p['peerId']);assert c==p['peerCard'] and m.sha(c)==p['peerCanonicalSHA256'];pp.append({'id':p['peerId'],'topicId':p['peerTopicId'],'card':c,'sha256':m.sha(c)})
bps=m.read(B/'peer-snapshot.json')['actualCurrentPeers']
for p in bps:
 t=m.read(C/f"src/content/topics/{p['topicId']}.json");assert p['card']==next(q for q in t['questions'] if q['id']==p['id']) and m.sha(p['card'])==p['sha256']
kw=[(A,'01a14208-996a-7b33-9397-bad2658d0551',[97,98,100],D/'apply-preservation3-source08.json',{'actualCurrentPeers':[p for p in pp if p['topicId']=='books-publishing']},None),(A/'cycle1-96','01a14208-996a-7b33-9397-bad2658d0551',[96],D/'apply-frbr96-cycle1-source08.json',{'actualCurrentPeers':m.read(A/'cycle1-96/peer-snapshot.json')['actualCurrentPeers96']},A/'repair-02/peer96-current-addendum.json'),(B,'01a14225-6301-72d2-9e92-1e1b62912ca2',[6,53,62,70,71,72],D/'apply-books6-source25.json',{'actualCurrentPeers':[p for p in bps if p['topicId']=='books-publishing']},None)]
for b,actor,orders,out,peers,add in kw:
 z=app.apply(b,actor,orders,out,qa,pathlib.Path(__file__),peerAddendum=add,qualifyOnly=True,peerSnapshot=peers);print('PREFLIGHT',orders,len(z['finalGroupBindings']),len(z['finalVariantBindings']))
tp=C/'src/content/topics/books-publishing.json';assert tp.read_bytes()==subprocess.check_output(['git','-C',str(C),'show','refs/heads/codex/question-quality-wave-6:src/content/topics/books-publishing.json'])
for b,actor,orders,out,peers,add in kw:app.apply(b,actor,orders,out,qa,pathlib.Path(__file__),peerAddendum=add,peerSnapshot=peers)
