"""Atomically apply qualified SOURCE groups against one before snapshot; no editorial credit."""
import pathlib,importlib.util,subprocess
C=pathlib.Path(__file__).resolve().parents[4];D=pathlib.Path(__file__).parent
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('own',D/'owned-tools.py');a=load('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a.P=m.P
tp=C/'src/content/topics/books-publishing.json';beforeRaw=m.raw(tp);before=m.read(tp)
assert tp.read_bytes()==subprocess.check_output(['git','-C',str(C),'show','refs/heads/codex/question-quality-wave-6:src/content/topics/books-publishing.json'])
jobs=[('qualified-terminal6-45-source62','01a14262-85b3-7bd3-be22-0c76b96bbc5a',[6,45],'apply-joint-terminal6-45-source62.json'),('qualified-terminal5-source62','01a14262-8bca-7a42-9ef8-31c73fb38274',[5],'apply-joint-terminal5-source62.json')]
results=[];replace={};files=[]
for name,actor,orders,out in jobs:
 B=D/name;ps=m.read(B/'peer-snapshot.json');ad=ps['relevantProposedPairAddendum'];assert m.raw(C/ad['path'])==ad['rawSHA256']
 for p in ps['actualCurrentPeers']:
  t=m.read(C/f"src/content/topics/{p['topicId']}.json");assert p['card']==next(q for q in t['questions']if q['id']==p['id']) and m.sha(p['card'])==p['sha256']
 r=a.apply(B,actor,orders,D/out,D/'qa-terminal5-6-45-new-primary.json',pathlib.Path(__file__),qualifyOnly=True,peerSnapshot={'actualCurrentPeers':[p for p in ps['actualCurrentPeers']if p['topicId']=='books-publishing']})
 for x in r['applied']:assert x['id']not in replace;replace[x['id']]=x['proposedCard']
 r.update(stage='Applied jointly on one verified before snapshot; pending affected19 and independent FINAL; credit0',sourceMutualMainAddendum=ad,applicationMode='All SOURCE peer/preimage checks ran on the SAME unchanged catalog; no intermediate sibling state. Single joint schema validates all replacements.',qaSelection={'command':'node node_modules/vitest/vitest.mjs run tests/unit/catalog-topics.test.ts tests/unit/content.test.ts tests/unit/content-answer-notes.test.ts --reporter=json --outputFile=docs/content-audits/question-quality-wave-8/coordinator-01a141dd/qa-terminal5-6-45-new-primary.json','reason':'Only three content cards; existing catalog schema, stable key/grade, notes. No runtime/build/fullsuite.'})
 results.append((D/out,r));files += [p for p in B.rglob('*')if p.is_file()];print('qualified',orders,len(r['finalGroupBindings']),len(r['finalVariantBindings']))
proposed={**before,'questions':[replace.get(q['id'],q)for q in before['questions']]};assert len(replace)==3;issues=a.read_issues(proposed);assert issues==[],issues;assert m.raw(tp)==beforeRaw
m.write(tp,proposed)
for out,r in results:m.write(out,r);files.append(out)
files += [tp,pathlib.Path(__file__),C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/validate-proposed-topic.cjs']
print('catalogCommit',m.savecode(files,'Apply exact three new-primary candidates atomically after joint qualification'))
