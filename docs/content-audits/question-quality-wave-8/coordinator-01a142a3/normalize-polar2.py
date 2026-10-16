"""Canonical JSON string hash normalization only; unchanged SOURCE wording/grounds/raw paths."""
import pathlib,importlib.util
D=pathlib.Path(__file__).parent;C=D.parents[3]
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('own',D/'owned-tools.py');S=C/'docs/content-audits/question-quality-wave-8/process-v2-polar2-10-fresh-01a142a3/author/next-held-resumed';B=D/'qualified-polar2-sourced0';B.mkdir(exist_ok=True);assert {p.name for p in B.iterdir()} <= {'candidate.json','sourceproof.json','peer-snapshot.json'};a=m.read(S/'candidate.json');sp=m.read(S/'sourceproof.json');ps=m.read(S/'peer-snapshot.json');e=a['entries'][0];p=sp['entries'][0];c=e['proposedCard']
def groups(c):return {'prompt_ordered_answers_key':{'prompt':c['prompt'],'answers':[v['text']for v in c['answers']],'correctIndex':c['correctIndex']},'explanation':c['explanation'],**{'note'+str(k):v['note']for k,v in enumerate(c['answers'])}}
bg=groups(e['beforeCard']);ag=groups(c)
for g in p['literalGroups']:
 assert g['literal']==ag[g['group']];g['literalSHA256']=m.sha(g['literal']);e['fieldGroups'][g['group']]={'beforeCanonicalSHA256':m.sha(bg[g['group']]),'afterCanonicalSHA256':g['literalSHA256']}
for v in p['fourFullPromptAnswerNoteAssessments']:
 assert v['fullPrompt']==c['prompt']and v['answer']==c['answers'][v['slot']]['text']and v['note']==c['answers'][v['slot']]['note'];v['tripleSHA256']=m.sha({'prompt':v['fullPrompt'],'answer':v['answer'],'note':v['note']})
for peer in ps['actualCurrentPeers']:
 current=m.read(C/f"src/content/topics/{peer['topicId']}.json");assert peer['card']==next(q for q in current['questions']if q['id']==peer['id']);peer['sha256']=peer.get('sha256',peer.get('canonicalSHA256'));assert peer['sha256']==m.sha(peer['card'])
capture=D/'source-captures/sourced0-polar2-original-opened-contexts.json'
def normpath(path):
 return str(capture.relative_to(C)) if pathlib.Path(path).stem=='national-geographic-continent' else path
for r in sp['rawSources']:
 if pathlib.Path(r['path']).name=='national-geographic-continent.txt':
  r['originalWrapperPath']=r['path'];r['originalWrapperSHA256']=r['sha256'];r['path']=normpath(r['path']);r['sha256']=m.raw(capture);r['captureProvenance']='Exact original full visible SOURCE NationalGeographic educational open, not manual selected quote wrapper.'
 if pathlib.Path(r['path']).name=='noaa-arctic-faq-open.txt':
  assert 'https://pmel.noaa.gov/arctic-zone/faq.html' in (C/r['path']).read_text()
  r['originalMismatchedURL']=r['url'];r['url']='https://pmel.noaa.gov/arctic-zone/faq.html'
for e in sp['entries']:
 for g in e['literalGroups']:g['sourcePaths']=[normpath(x)for x in g['sourcePaths']]
 for v in e['fourFullPromptAnswerNoteAssessments']:v['sourcePaths']=[normpath(x)for x in v['sourcePaths']]
for x in [a,sp,ps]:x['rootNormalization']={'owner':m.O,'sourceOriginal':str(S.relative_to(C)),'sourceOriginalFreeze':'5d8e3f8c6a208faeccc37a86021498de3032d35b','transformations':['CanonicalJSON string quotes normalized; manualNG wrapper and stale html filename alias mapped to full original SOURCE-visible capture; NOAA raw-source URL corrected to actual captured PMEL FAQ; all card text/SOURCE judgments unchanged'],'wordingUnchanged':True,'qualityCredit':0}
for n,x in [('candidate.json',a),('sourceproof.json',sp),('peer-snapshot.json',ps)]:m.write(B/n,x)
a=load('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a.P=m.P;r=a.apply(B,'01a142d0-3ae4-7d93-a1f3-ad8038c4254d',[2],D/'apply-polar2.json',D/'qa-polar2.json',pathlib.Path(__file__),qualifyOnly=True,peerSnapshot={'actualCurrentPeers':[p for p in ps['actualCurrentPeers']if p['topicId']=='polar-regions']});m.write(D/'qualification-polar2.json',{'qualified':True,'groups':len(r['finalGroupBindings']),'variants':len(r['finalVariantBindings']),'qualityCredit':0});print('sourceFreeze',m.savecode([pathlib.Path(__file__),D/'qualification-polar2.json']+list(B.iterdir()),'Freeze canonical normalized SOURCE polar2 full original opened primary proof beforesecond; no credit'))
