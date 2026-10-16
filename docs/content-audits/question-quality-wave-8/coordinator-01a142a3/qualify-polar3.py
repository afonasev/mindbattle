"""Transport SOURCE3 canonical hashes only; no editorial credit/catalog change."""
import pathlib,importlib.util
D=pathlib.Path(__file__).parent;C=D.parents[3]
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('own',D/'owned-tools.py');S=C/'docs/content-audits/question-quality-wave-8/process-v2-polar2-10-fresh-01a142a3/author/remaining5-current839';B=D/'qualified-polar3-sourced0';B.mkdir(exist_ok=True);assert {p.name for p in B.iterdir()} <= {'candidate.json','sourceproof.json','peer-snapshot.json'}
a=m.read(S/'candidate.json');sp=m.read(S/'sourceproof.json');ps=m.read(S/'peer-snapshot.json')
def groups(c):return {'prompt_ordered_answers_key':{'prompt':c['prompt'],'answers':[v['text'] for v in c['answers']],'correctIndex':c['correctIndex']},'explanation':c['explanation'],**{'note'+str(k):v['note'] for k,v in enumerate(c['answers'])}}
for e in a['entries']:
 p=next(x for x in sp['entries'] if x['id']==e['id']);c=e['proposedCard'];bg=groups(e['beforeCard']);ag=groups(c)
 for g in p['literalGroups']:
  assert g['literal']==ag[g['group']];g['literalSHA256']=m.sha(g['literal']);e['fieldGroups'][g['group']]={'beforeCanonicalSHA256':m.sha(bg[g['group']]),'afterCanonicalSHA256':g['literalSHA256']}
 for v in p['fourFullPromptAnswerNoteAssessments']:
  assert v['fullPrompt']==c['prompt'] and v['answer']==c['answers'][v['slot']]['text'] and v['note']==c['answers'][v['slot']]['note'];v['tripleSHA256']=m.sha({'prompt':v['fullPrompt'],'answer':v['answer'],'note':v['note']})
for peer in ps['actualCurrentPeers']:
 assert peer['card']==next(q for q in m.read(C/f"src/content/topics/{peer['topicId']}.json")['questions'] if q['id']==peer['id']) and m.sha(peer['card'])==peer['sha256']
for x in [a,sp,ps]:x['rootNormalization']={'original':str(S.relative_to(C)),'originalFreeze':'6be3145d73ccf0ffac7c14ca3f00864275f967b8','technicalTransforms':['canonicalJSON hashes only, no text/source/judgment changes'],'cardTextAndSourceJudgmentsUnchanged':True,'qualityCredit':0}
for n,x in [('candidate.json',a),('sourceproof.json',sp),('peer-snapshot.json',ps)]:m.write(B/n,x)
app=load('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');app.P=m.P
r=app.apply(B,'01a142d0-3ae4-7d93-a1f3-ad8038c4254d',[3],D/'apply-polar3.json',D/'qa-polar3.json',pathlib.Path(__file__),qualifyOnly=True,peerSnapshot={'actualCurrentPeers':[v for v in ps['actualCurrentPeers'] if v['topicId']=='polar-regions']})
m.write(D/'qualification-polar3.json',{'qualified':True,'literalGroups':len(r['finalGroupBindings']),'wholeVariants':len(r['finalVariantBindings']),'qualityCredit':0,'notApplied':'not yet applied pending root exactSOURCE binding','independentConcern':'SOURCE names islands-001 sameGreenland answer but different size-rank vs icecover predicate; independent fullMAIN and absolutegrade judgment required'})
print(m.savecode([pathlib.Path(__file__),D/'qualification-polar3.json',*B.iterdir()],'Freeze qualified SOURCE polar3 exact full proof pending independent review; credit0'))
