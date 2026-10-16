"""Qualify both SOURCE packets against one actual before snapshot, then one topic write."""
import pathlib,importlib.util,subprocess
D=pathlib.Path(__file__).parent;C=D.parents[3]
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('own',D/'owned-tools.py');a=load('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a.P=m.P;tp=C/'src/content/topics/national-parks-nature.json';before=tp.read_bytes();assert before==subprocess.check_output(['git','-C',str(C),'show','refs/heads/codex/question-quality-wave-6:'+str(tp.relative_to(C))]);topic=m.read(tp);results=[];replace={};files=[]
for name,packet,actor,order,freeze,stage in [('parks4-cycle1','qualified-parks4-cycle1-sourceb7','01a142b7-50b2-7d11-8dd8-0585e2e11218',4,'93c64eb92752de4955030ea4762390d8119fd69c','FINAL'),('parks5','qualified-parks5-source62','01a14262-8bca-7a42-9ef8-31c73fb38274',5,'f2f45081616bfa2e720ae1905ce48762037ed43e','INITIAL')]:
 B=D/packet;ps=m.read(B/'peer-snapshot.json')
 for p in ps['actualCurrentPeers']:
  t=m.read(C/f"src/content/topics/{p['topicId']}.json");assert p['card']==next(q for q in t['questions']if q['id']==p['id'])and m.sha(p['card'])==p['sha256']
 out=D/f'apply-{name}.json';r=a.apply(B,actor,[order],out,D/'qa-parks4-cycle1-5.json',pathlib.Path(__file__),qualifyOnly=True,peerSnapshot={'actualCurrentPeers':[p for p in ps['actualCurrentPeers']if p['topicId']=='national-parks-nature']});r.update(sourceFreeze=freeze,independentStage=stage,qualityCredit=0,applicationMode='Both SOURCE packet peer/preimage checks on same actual before snapshot; joint topic write and schema validation.',qaSelection={'command':'node node_modules/vitest/vitest.mjs run tests/unit/catalog-topics.test.ts tests/unit/content.test.ts tests/unit/content-answer-notes.test.ts --reporter=json --outputFile=docs/content-audits/question-quality-wave-8/coordinator-01a142a3/qa-parks4-cycle1-5.json','reason':'Only two data cards changed, one note3 fix plus Serengeti country rewrite. Affected schema/catalog/key/difficulty/notes, no runtime/build/fullsuite.'});results.append((out,r));files+=list(B.iterdir())
 for e in r['applied']:assert e['id']not in replace;replace[e['id']]=e['proposedCard']
proposed={**topic,'questions':[replace.get(q['id'],q)for q in topic['questions']]};assert len(replace)==2 and a.read_issues(proposed)==[];assert tp.read_bytes()==before;m.write(tp,proposed)
for out,r in results:m.write(out,r);files.append(out)
print('catalogCommit',m.savecode(files+[tp,pathlib.Path(__file__)],'Apply joint exactSOURCE parks4 wilderness cycle1 and parks5 country INITIAL; no quality credit'))
