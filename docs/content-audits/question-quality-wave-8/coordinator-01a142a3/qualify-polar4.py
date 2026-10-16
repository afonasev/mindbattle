"""Transport SOURCE4 canonical hashes only; no editorial credit/catalog change."""
import pathlib,importlib.util
D=pathlib.Path(__file__).parent;C=D.parents[3]
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('own',D/'owned-tools.py');S=C/'docs/content-audits/question-quality-wave-8/process-v2-polar2-10-fresh-01a142a3/author/proof-completion4';B=D/'qualified-polar4-sourced0';B.mkdir(exist_ok=True);assert {p.name for p in B.iterdir()} <= {'candidate.json','sourceproof.json','peer-snapshot.json'}
a=m.read(S/'candidate.json');sp=m.read(S/'sourceproof.json');ps=m.read(S/'peer-snapshot.json')
rawPaths={v['path'] for v in sp['rawSources']}
def normpath(v):
 if v in rawPaths:return v
 assert pathlib.Path(v).name=='noaa-cpc-indian-ocean.txt',v
 return next(x for x in rawPaths if pathlib.Path(x).name=='noaa-cpc-indian-ocean-web-output.txt')
for e in sp['entries']:
 for field in ['literalGroups','fourFullPromptAnswerNoteAssessments']:
  for v in e[field]:v['sourcePaths']=[normpath(p) for p in v['sourcePaths']]
 if 'sourcePaths' in e['correctNoteNewFact']:e['correctNoteNewFact']['sourcePaths']=[normpath(p) for p in e['correctNoteNewFact']['sourcePaths']]

def groups(c):return {'prompt_ordered_answers_key':{'prompt':c['prompt'],'answers':[v['text'] for v in c['answers']],'correctIndex':c['correctIndex']},'explanation':c['explanation'],**{'note'+str(k):v['note'] for k,v in enumerate(c['answers'])}}
for e in a['entries']:
 p=next(x for x in sp['entries'] if x['id']==e['id']);c=e['proposedCard'];bg=groups(e['beforeCard']);ag=groups(c)
 for g in p['literalGroups']:
  assert g['literal']==ag[g['group']];g['literalSHA256']=m.sha(g['literal']);e['fieldGroups'][g['group']]={'beforeCanonicalSHA256':m.sha(bg[g['group']]),'afterCanonicalSHA256':g['literalSHA256']}
 for v in p['fourFullPromptAnswerNoteAssessments']:
  assert v['fullPrompt']==c['prompt'] and v['answer']==c['answers'][v['slot']]['text'] and v['note']==c['answers'][v['slot']]['note'];v['tripleSHA256']=m.sha({'prompt':v['fullPrompt'],'answer':v['answer'],'note':v['note']})
for peer in ps['actualCurrentPeers']:
 assert peer['card']==next(q for q in m.read(C/f"src/content/topics/{peer['topicId']}.json")['questions'] if q['id']==peer['id']) and m.sha(peer['card'])==peer['sha256']
for x in [a,sp,ps]:x['rootNormalization']={'original':str(S.relative_to(C)),'originalFreeze':'467656122bd69545c041f9acda856294a14391de','technicalTransforms':['canonicalJSON hashes','stale NOAA CPC wrapper reference maps to same personally read original full12line body preserved by SOURCE in proofcompletion4'],'cardTextAndSourceJudgmentsUnchanged':True,'qualityCredit':0}
for n,x in [('candidate.json',a),('sourceproof.json',sp),('peer-snapshot.json',ps)]:m.write(B/n,x)
app=load('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');app.P=m.P
r=app.apply(B,'01a142d0-3ae4-7d93-a1f3-ad8038c4254d',[4],D/'apply-polar4.json',D/'qa-polar4.json',pathlib.Path(__file__),qualifyOnly=True,peerSnapshot={'actualCurrentPeers':[v for v in ps['actualCurrentPeers'] if v['topicId']=='polar-regions']})
m.write(D/'qualification-polar4.json',{'qualified':True,'literalGroups':len(r['finalGroupBindings']),'wholeVariants':len(r['finalVariantBindings']),'qualityCredit':0,'notApplied':'same topic currently under independent polar2 review','independentConcern':'SOURCE flags close order2 pair; exact full MAIN must be independently judged, not inherited label'})
print(m.savecode([pathlib.Path(__file__),D/'qualification-polar4.json',*B.iterdir()],'Freeze qualified SOURCE polar4 exact full proof pending independent review; credit0'))
