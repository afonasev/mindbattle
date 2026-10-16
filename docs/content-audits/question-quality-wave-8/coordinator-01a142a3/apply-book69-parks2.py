"""Preflight two exact SOURCE packets then apply their two topics; zero quality credit."""
import pathlib,importlib.util,subprocess
D=pathlib.Path(__file__).parent;C=D.parents[3]
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('owned',D/'owned-tools.py');a=load('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a.P=m.P
jobs=[(C/'docs/content-audits/question-quality-wave-8/process-v2-terminal-hold3-fresh-01a141dd/author/phaseB69/repair-note0','01a14262-85b3-7bd3-be22-0c76b96bbc5a',[69],'book69','6c54ac64a204e20c43e6910e864a9b012364eef5','FINAL'),(D/'qualified-parks2-source62','01a14262-8bca-7a42-9ef8-31c73fb38274',[2],'parks2','f886b9c66d411353c0521f4990c4d971ae1ccae4','INITIAL')]
results=[];files=[]
for B,actor,orders,name,freeze,stage in jobs:
 ps=m.read(B/'peer-snapshot.json');topicId=m.read(B/'candidate.json')['entries'][0]['topicId'];tp=C/f'src/content/topics/{topicId}.json';before=tp.read_bytes();assert before==subprocess.check_output(['git','-C',str(C),'show','refs/heads/codex/question-quality-wave-6:'+str(tp.relative_to(C))])
 for p in ps['actualCurrentPeers']:
  t=m.read(C/f"src/content/topics/{p['topicId']}.json");assert p['card']==next(q for q in t['questions']if q['id']==p['id']) and m.sha(p['card'])==p.get('sha256',p.get('canonicalSHA256'))
 r=a.apply(B,actor,orders,D/f'apply-{name}.json',D/'qa-book69-parks2.json',pathlib.Path(__file__),qualifyOnly=True,peerSnapshot={'actualCurrentPeers':[p for p in ps['actualCurrentPeers']if p['topicId']==topicId]});r.update(sourceFreeze=freeze,independentStage=stage,qualityCredit=0,qaSelection={'command':'node node_modules/vitest/vitest.mjs run tests/unit/catalog-topics.test.ts tests/unit/content.test.ts tests/unit/content-answer-notes.test.ts --reporter=json --outputFile=docs/content-audits/question-quality-wave-8/coordinator-01a142a3/qa-book69-parks2.json','reason':'Two content cards only: schema, stable metadata, notes; no runtime/build/fullsuite.'})
 topic=m.read(tp);replace={x['id']:x['proposedCard']for x in r['applied']};proposed={**topic,'questions':[replace.get(q['id'],q)for q in topic['questions']]};assert a.read_issues(proposed)==[];results.append((tp,before,proposed,D/f'apply-{name}.json',r));files += [p for p in B.iterdir()if p.is_file()]
for tp,before,proposed,out,r in results:assert tp.read_bytes()==before
for tp,before,proposed,out,r in results:m.write(tp,proposed);m.write(out,r);files += [tp,out]
files += [pathlib.Path(__file__),D/'qualification-book69.json']
print('catalogCommit',m.savecode(files,'Apply exact book69 new-primary FINAL and SOURCE-normalized park2 INITIAL candidates; credit0'))
