"""Apply SOURCE7 INITIAL and SOURCE9 terminology cycle1 from same verified before snapshot."""
import pathlib,importlib.util,subprocess
D=pathlib.Path(__file__).parent;C=D.parents[3]
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('own',D/'owned-tools.py');app=load('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');app.P=m.P
tp=C/'src/content/topics/polar-regions.json';before=tp.read_bytes();assert before==subprocess.check_output(['git','-C',str(C),'show','refs/heads/codex/question-quality-wave-6:'+str(tp.relative_to(C))]);topic=m.read(tp);results=[];replace={};files=[]
jobs=[('polar7',C/'docs/content-audits/question-quality-wave-8/process-v2-polar2-10-fresh-01a142a3/author/next-rest',7,'d8e2c5ced9481960a933b2474d258b3a03532b0b','INITIAL'),('polar9-cycle1',D/'qualified-polar9-cycle1-sourced0',9,'13df5a882d7cb0ad9d5c10ba1b560a0843a859cd','FINAL')]
for name,B,order,freeze,stage in jobs:
 ps=m.read(B/'peer-snapshot.json')
 for p in ps['actualCurrentPeers']:
  t=m.read(C/f"src/content/topics/{p['topicId']}.json");assert p['card']==next(q for q in t['questions']if q['id']==p['id'])and m.sha(p['card'])==p.get('sha256',p.get('canonicalSHA256'))
 out=D/f'apply-{name}.json';r=app.apply(B,'01a142d0-3ae4-7d93-a1f3-ad8038c4254d',[order],out,D/'qa-polar7-9-cycle1.json',pathlib.Path(__file__),qualifyOnly=True,peerSnapshot={'actualCurrentPeers':[{**p,'sha256':p.get('sha256',p.get('canonicalSHA256'))}for p in ps['actualCurrentPeers']if p['topicId']=='polar-regions']});r.update(sourceFreeze=freeze,independentStage=stage,applicationMode='Both SOURCE preimage/actualpeer checks on identical before catalog; one joint topicwrite/schema validation',qualityCredit=0,qaSelection={'command':'node node_modules/vitest/vitest.mjs run tests/unit/catalog-topics.test.ts tests/unit/content.test.ts tests/unit/content-answer-notes.test.ts --reporter=json --outputFile=docs/content-audits/question-quality-wave-8/coordinator-01a142a3/qa-polar7-9-cycle1.json','reason':'Only two data cards: parallel-category distractor/notes correction on7 and three exact ice-shelf terms on9; catalog schema/IDs/frozen metadata/notes. No runtime/build/fullsuite.'});results.append((out,r));files+=list(B.iterdir())
 for e in r['applied']:assert e['id']not in replace;replace[e['id']]=e['proposedCard']
proposed={**topic,'questions':[replace.get(q['id'],q)for q in topic['questions']]};assert len(replace)==2 and app.read_issues(proposed)==[];assert tp.read_bytes()==before;m.write(tp,proposed)
for out,r in results:m.write(out,r);files.append(out)
print('catalogCommit',m.savecode(files+[tp,pathlib.Path(__file__),D/'qualification-polar7.json',D/'qualification-polar9-cycle1.json'],'Apply joint exactSOURCE polar7 INITIAL and polar9 precise ice-shelf cycle1; quality0'))
