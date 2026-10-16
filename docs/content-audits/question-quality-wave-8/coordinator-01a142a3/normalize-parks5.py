"""Mechanical path, assessment alias and canonical JSON hash normalization; no wording change."""
import pathlib,importlib.util,copy
D=pathlib.Path(__file__).parent;C=D.parents[3]
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('owned',D/'owned-tools.py');S=C/'docs/content-audits/question-quality-wave-8/process-v2-parks-4-7-01a142a3/author/next5-7';B=D/'qualified-parks5-source62';B.mkdir(exist_ok=True);assert {p.name for p in B.iterdir()} <= {'candidate.json','sourceproof.json','peer-snapshot.json'}
a=m.read(S/'candidate.json');sp=m.read(S/'sourceproof.json');ps=m.read(S/'peer-snapshot.json');e=a['entries'][0];p=sp['entries'][0];c=e['proposedCard'];original=copy.deepcopy(c)
def groups(c):return {'prompt_ordered_answers_key':{'prompt':c['prompt'],'answers':[v['text']for v in c['answers']],'correctIndex':c['correctIndex']},'explanation':c['explanation'],**{'note'+str(k):v['note']for k,v in enumerate(c['answers'])}}
bg=groups(e['beforeCard']);ag=groups(c)
capture=D/'source-captures/source62-parks5-original-opened-sanparks-contexts.json'
def normalizepath(x):
 p=pathlib.Path(x)
 return str((capture if p.name=='sanparks-kruger-giriyondo-context.txt'else p).relative_to(C))
for r in sp['rawSources']:
 path=pathlib.Path(r['path']);assert m.raw(path)==r['sha256'];r['path']=normalizepath(str(path))
 if path.name=='sanparks-kruger-giriyondo-context.txt':r['originalWrapperPath']=str(path.relative_to(C));r['sha256']=m.raw(capture);r['captureReadProvenance']='Exact original opened SANParks full visible context from same SOURCE journal; replace manuallyselected wrapper, retain exact URL/locator.'
for g in p['literalGroups']:
 assert g['literal']==ag[g['group']];g['literalSHA256']=m.sha(g['literal']);e['fieldGroups'][g['group']]={'beforeCanonicalSHA256':m.sha(bg[g['group']]),'afterCanonicalSHA256':g['literalSHA256']};g['sourcePaths']=[normalizepath(x) for x in g['sourcePaths']]
for v in p['fourFullPromptAnswerNoteAssessments']:
 v['sourcePaths']=[normalizepath(x)for x in v['sourcePaths']]
 if 'plausibilityUniqueKeyAndNoteTruthfulness'in v:v['plausibilityUniqueKeyAndNoteTruthUsefulness']=v.pop('plausibilityUniqueKeyAndNoteTruthfulness')
 assert v['fullPrompt']==c['prompt']and v['answer']==c['answers'][v['slot']]['text']and v['note']==c['answers'][v['slot']]['note'];v['tripleSHA256']=m.sha({'prompt':v['fullPrompt'],'answer':v['answer'],'note':v['note']})
for peers in [ps['actualCurrentPeers'],p.get('actualCurrentPeers',[])]:
 for peer in peers:
  current=m.read(C/f"src/content/topics/{peer['topicId']}.json");assert peer['card']==next(q for q in current['questions']if q['id']==peer['id']);assert m.sha(peer['card'])==peer.get('sha256',peer.get('canonicalSHA256'));peer['sha256']=m.sha(peer['card'])
assert c==original and m.sha(c)==e['afterHash']
for x in [a,sp,ps]:x['rootNormalization']={'owner':m.O,'sourceOriginal':str(S.relative_to(C)),'sourceOriginalFreeze':'603d2296ffcc9f65f28a4daa7393f52cb3d8c601','transformations':['Absolute source paths made code-relative preserving same fullraw bytes','Canonical JSON group/triple hashes computed with stringquotes','Assessment field alias normalized preserving prose'],'wordingUnchanged':True,'qualityCredit':0}
for n,x in [('candidate.json',a),('sourceproof.json',sp),('peer-snapshot.json',ps)]:m.write(B/n,x)
app=load('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');app.P=m.P;r=app.apply(B,'01a14262-8bca-7a42-9ef8-31c73fb38274',[5],D/'apply-parks5.json',D/'qa-parks5.json',pathlib.Path(__file__),qualifyOnly=True,peerSnapshot={'actualCurrentPeers':[p for p in ps['actualCurrentPeers']if p['topicId']=='national-parks-nature']});m.write(D/'qualification-parks5.json',{'qualified':True,'groups':len(r['finalGroupBindings']),'variants':len(r['finalVariantBindings']),'qualityCredit':0})
print('sourceFreeze',m.savecode([pathlib.Path(__file__),D/'qualification-parks5.json']+list(B.iterdir()),'Freeze mechanically normalized SOURCE park5 beforesecond; unchanged wording quality0'))
