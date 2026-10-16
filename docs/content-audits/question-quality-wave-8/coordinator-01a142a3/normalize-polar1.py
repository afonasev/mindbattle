"""Canonical JSON string hash normalization only; unchanged SOURCE wording/grounds/raw paths."""
import pathlib,importlib.util
D=pathlib.Path(__file__).parent;C=D.parents[3]
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('own',D/'owned-tools.py');S=C/'docs/content-audits/question-quality-wave-8/process-v2-polar-first10-01a142a3/author/source-completion2';B=D/'qualified-polar1-source62';B.mkdir(exist_ok=False);a=m.read(S/'candidate.json');sp=m.read(S/'sourceproof.json');ps=m.read(S/'peer-snapshot.json');e=a['entries'][0];p=sp['entries'][0];c=e['proposedCard']
def groups(c):return {'prompt_ordered_answers_key':{'prompt':c['prompt'],'answers':[v['text']for v in c['answers']],'correctIndex':c['correctIndex']},'explanation':c['explanation'],**{'note'+str(k):v['note']for k,v in enumerate(c['answers'])}}
bg=groups(e['beforeCard']);ag=groups(c)
for g in p['literalGroups']:
 assert g['literal']==ag[g['group']];g['literalSHA256']=m.sha(g['literal']);e['fieldGroups'][g['group']]={'beforeCanonicalSHA256':m.sha(bg[g['group']]),'afterCanonicalSHA256':g['literalSHA256']}
for v in p['fourFullPromptAnswerNoteAssessments']:
 assert v['fullPrompt']==c['prompt']and v['answer']==c['answers'][v['slot']]['text']and v['note']==c['answers'][v['slot']]['note'];v['tripleSHA256']=m.sha({'prompt':v['fullPrompt'],'answer':v['answer'],'note':v['note']})
for peer in ps['actualCurrentPeers']:
 current=m.read(C/f"src/content/topics/{peer['topicId']}.json");assert peer['card']==next(q for q in current['questions']if q['id']==peer['id']);peer['sha256']=peer.get('sha256',peer.get('canonicalSHA256'));assert peer['sha256']==m.sha(peer['card'])
for x in [a,sp,ps]:x['rootNormalization']={'owner':m.O,'sourceOriginal':str(S.relative_to(C)),'sourceOriginalFreeze':'f778937777a8a64fde87c47b453af1ebf7cd1587','transformations':['CanonicalJSON string hashes include quotes; fullcard/triple digests recomputed from identical literals'],'wordingUnchanged':True,'qualityCredit':0}
for n,x in [('candidate.json',a),('sourceproof.json',sp),('peer-snapshot.json',ps)]:m.write(B/n,x)
a=load('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a.P=m.P;r=a.apply(B,'01a14262-85b3-7bd3-be22-0c76b96bbc5a',[1],D/'apply-polar1.json',D/'qa-parks4-5-polar1.json',pathlib.Path(__file__),qualifyOnly=True,peerSnapshot={'actualCurrentPeers':[p for p in ps['actualCurrentPeers']if p['topicId']=='polar-regions']});m.write(D/'qualification-polar1.json',{'qualified':True,'groups':len(r['finalGroupBindings']),'variants':len(r['finalVariantBindings']),'qualityCredit':0});print('sourceFreeze',m.savecode([pathlib.Path(__file__),D/'qualification-polar1.json']+list(B.iterdir()),'Freeze canonical normalized SOURCE polar1 full opened primary proofs beforesecond; no credit'))
