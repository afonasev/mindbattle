"""Explicit-owned evidence saves, private Git index, leased planning projection."""
import pathlib,importlib.util,hashlib,json,datetime
C=pathlib.Path(__file__).resolve().parents[4];P=pathlib.Path('/Users/eaafonasev/Projects/mindbattle/planning');D=pathlib.Path(__file__).parent;O='01a14018-7b8d-7301-ad28-95ee8d812e97'
def module(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
h=module('private_save',P/'evidence/question-revision-process-v2/private-save-helper-01a13cb1.py');flow=module('flow',C/'tools/flow.py').Flow(P)
def save(root,ref,paths,msg):
 files=sorted(set(str(pathlib.Path(p).relative_to(root)) for p in paths));idx=root/h.git(root,'rev-parse','--git-path','index');return h.save(root,ref,files,msg,hashlib.sha256(idx.read_bytes()).hexdigest())
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def preserve(index,paths,message):
 now=datetime.datetime.now(datetime.timezone.utc).isoformat();index['at']=now;write(D/'coordinator-continuation-index.json',index)
 code=save(C,'refs/heads/codex/question-quality-wave-6',paths+[D/'coordinator-continuation-index.json',pathlib.Path(__file__)],message)
 with flow.locked():flow.lease('acquire','planning',O)
 try:
  statepath=P/'evidence/question-revision-process-v2/coordinator-state.json';s=json.loads(statepath.read_text());s.update(threadId=O,counts={'CURRENT':index['CURRENT'],'remaining':index['remaining']},codeBranch='codex/question-quality-wave-6',codeCommit=code,mainIntegrated=False,asOf=now,next=index['next'],ownActualCompactions=index['ownActualCompactions'],continuationIndex=str((D/'coordinator-continuation-index.json').relative_to(C)),activeAuthors=[index[k] for k in ['SOURCEfirst5FreshAdoption','SOURCEsmallCycle1Fresh']],activeIndependentReview=index['OTHERcurrent']);write(statepath,s)
  plan=save(P,'refs/heads/codex/question-revision-resume-20261014',[statepath],message+' planning projection')
 finally:
  with flow.locked():flow.lease('release','planning',O)
 return {'codeBranch':'codex/question-quality-wave-6','codeCommit':code,'planningBranch':'codex/question-revision-resume-20261014','planningCommit':plan,'mainIntegrated':False}
if __name__=='__main__':
 i=json.loads((D/'coordinator-continuation-index.json').read_text());i['ownActualCompactions']=1;i['SOURCEfirst5FreshAdoption'].update(status='SOURCE_READY5_RECEIVED_NOTQUALIFIED: concrete variant source locator mismatch sent for initial proof repair',cursor='e3bf0303-f112-4cc6-8999-d41f084f33ce:1');i['SOURCEsmallCycle1Fresh'].update(status='SOURCE_READY2_RECEIVED_NOTQUALIFIED: correctNoteNewFact59 incorrectly mapped to glossary; sent proof mapping repair same cycle1',cursor='fd52c20f-8bd1-40e0-ab1a-0a64f3a9f99c:1');i['next']='Intake personally authored proof repairs; qualify small2, apply exactcycle1/affected19/OTHERFINAL. First5adoption then OTHERINITIAL. Fullgoal CURRENT761 remaining1239, HOLD notcompletion.'
 a=C/i['SOURCEsmallCycle1Fresh']['path'];b=C/i['SOURCEfirst5FreshAdoption']['path'];files=[p for p in a.rglob('*') if p.is_file()]+[p for p in b.rglob('*') if p.is_file()]
 print(json.dumps(preserve(i,files,'Preserve first-compaction slice and unqualified fresh SOURCE7 evidence'),ensure_ascii=False))
