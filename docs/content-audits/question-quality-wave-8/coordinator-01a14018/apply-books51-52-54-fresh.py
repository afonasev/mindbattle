"""Alias a genuine SOURCE ready portion3; retain sourceHOLD53 and ten unverified."""
import pathlib,importlib.util,copy,sys
C=pathlib.Path(__file__).resolve().parents[4];D=pathlib.Path(__file__).parent;A=C/'docs/content-audits/question-quality-wave-8/process-v2-books-remaining14-fresh-source-01a14018/author';B=D/'qualified-books51-52-54-fresh';B.mkdir(exist_ok=True)
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');h=load('preserve',D/'preserve-current-slice.py');m.P=h.P
c=m.read(A/'candidate.json');sp=m.read(A/'sourceproof.json');ps=m.read(A/'peer-snapshot.json');assert [e['sourceOrder'] for e in sp['items']]==[51,52,54];sources={s['url']:s for s in sp['rawSources']};entries=[]
for s in sp['rawSources']:assert s['path'] and s['sha256']==m.raw(C/s['path']) and s['readEvidence']
for e in sp['items']:
 ce=next(x for x in c['entries'] if x['id']==e['id']);card=ce['proposedCard'];vs=[]
 for v0 in e['variantAudit']:
  v=copy.deepcopy(v0);s=sources[v['source']];g=next(g for g in e['literalGroups'] if g['group']=='note'+str(v['answerIndex']));v.update(slot=v['answerIndex'],grammar=v['grammarReview']['assessment'],plausibilityUniqueKeyAndNoteTruthUsefulness=v['assessment']+'\n'+v['sourceGround'],locator=g['locator'],sourcePaths=g['sourcePaths']);vs.append(v)
 correct=next(g for g in e['literalGroups'] if g['group']=='note'+str(card['correctIndex']))
 entries.append({**e,'fourFullPromptAnswerNoteAssessments':vs,'correctNoteNewFact':{'literal':correct['literal'],'sourceAssessmentVerbatim':correct['primaryGround'],'locator':correct['locator'],'sourcePaths':correct['sourcePaths'],'technicalFieldComposition':'Existing SOURCE correct-note literal and concrete primary judgment, preserved verbatim. Independent reader verifies actual extra beyond prompt/key; root adds no facts.'}})
peer=ps['actualCurrentTopic']['cards'];assert len(peer)==100 and len({p['id'] for p in peer})==100
for ce in c['entries']:
 if ce['sourceOrder'] in [51,52,54]:assert ce['status']=='READY_FOR_INDEPENDENT_REVIEW'
for name,v in [('candidate',c),('sourceproof',{'rawSources':sp['rawSources'],'entries':entries,'sourceOriginal':str((A/'sourceproof.json').relative_to(C)),'technicalComposition':'Only explicit field aliases/composition of existing SOURCE judgments; originals retained.'}),('peer-snapshot',{**ps,'actualCurrentPeers':peer})]:m.write(B/(name+'.json'),v)
q=m.apply(B,'01a14087-3629-7920-b330-2f4e29b4ff7d',[51,52,54],None,None,None,qualifyOnly=True,peerSnapshot={'actualCurrentPeers':peer});m.write(D/'qualification-books51-52-54-fresh.json',{'qualityCredit':0,'qualification':q,'notQualified':{'SOURCE_HOLD':[53],'pendingUnverified':[55,56,57,58,61,62,63,64,69,70]},'technicalAliasesOnly':True,'readerMustAssess':['own-extra relative to whole prompt and key','truth and grammar of each actual variant','MAIN disjointness actual plus latest proposals']})
files=[f for f in A.rglob('*') if f.is_file()]+[f for f in B.rglob('*') if f.is_file()]+[pathlib.Path(__file__),D/'qualification-books51-52-54-fresh.json'];freeze=h.save(C,'refs/heads/codex/question-quality-wave-6',files,'Freeze qualified SOURCE51/52/54 full contexts and individual12 variants');print('SOURCEFREEZE',freeze)
if '--apply' in sys.argv:
 m.apply(B,'01a14087-3629-7920-b330-2f4e29b4ff7d',[51,52,54],D/'apply-books51-52-54-fresh.json',D/'qa-books51-52-54-fresh.json',pathlib.Path(__file__),peerSnapshot={'actualCurrentPeers':peer},concerns=['INITIAL ONLY3 ready from14. SOURCE53HOLD missingcompletepageprimarycontext and10unverified NOT completion.','SOURCE DAISYfull chapter context replaces unavailable MW chapter route; note52page unsupportedleafdefinition replacedbyDAISY chapter-firstpage fact beforeapplication. All12 grammarreviewed and54slot2 assessesactualChapter.','Correctnote existing primary judgments composedverbatim; OTHER personally judge extra beyondprompt/key, source truth/usefulness, actualEASY, onekey and MAIN current/proposals. No root newfactualgrounds.'])
 m.write(D/'source-freeze-books51-52-54-fresh.json',{'freeze':freeze,'author':'01a14087-3629-7920-b330-2f4e29b4ff7d','qualityCredit':0})
