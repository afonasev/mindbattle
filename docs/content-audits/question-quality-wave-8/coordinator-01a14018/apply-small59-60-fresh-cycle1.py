"""Mechanically normalize personally reauthored SOURCE cycle1; only three flagged fields."""
import pathlib,importlib.util,copy,sys,json
C=pathlib.Path(__file__).resolve().parents[4];D=pathlib.Path(__file__).parent;P=pathlib.Path('/Users/eaafonasev/Projects/mindbattle/planning');A=C/'docs/content-audits/question-quality-wave-8/process-v2-small59-60-cycle1-fresh-source-01a14018/author';B=D/'qualified-small59-60-fresh-cycle1';B.mkdir(exist_ok=True)
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');m.P=P;h=load('preserve',D/'preserve-current-slice.py')
c=m.read(A/'candidate.json');sp=m.read(A/'sourceproof.json');ps=m.read(A/'peer-snapshot.json')
for e in c['entries']:
 e['beforeHash']=e['beforeCardCanonicalSHA256'];e['afterHash']=e['afterCardCanonicalSHA256']
 for g,v in e['fieldGroups'].items():e['fieldGroups'][g]={'beforeCanonicalSHA256':v['before']['canonicalSHA256'],'afterCanonicalSHA256':v['after']['canonicalSHA256']}
 b=e['beforeCard'];a=e['proposedCard'];allowed={'answers'}|({'explanation'} if e['sourceOrder']==60 else set());assert {k for k in b if b[k]!=a[k]}==allowed
 for k,(before,after) in enumerate(zip(b['answers'],a['answers'])):
  if k==(2 if e['sourceOrder']==59 else 3):assert before['text']==after['text'] and before['note']!=after['note']
  else:assert before==after
 assert b['source']==a['source'] and len(a['explanation'].split())<=70
for s in sp['rawSources']:
 s['sha256']=s['rawSHA256'];assert m.raw(C/s['path'])==s['sha256'] and s['personalReadEvidence'] and s['locator']
for e in sp['entries']:
 assert e['absoluteDifficulty'] and e['correctNoteNewFact']['status']=='PASS'
 for v in e['fourFullPromptAnswerNoteAssessments']:v['tripleSHA256']=v['tripleCanonicalSHA256']
peers=ps['actualCurrentPeersFullCardsAndSHA256'];assert len(peers)==100 and len({p['id'] for p in peers})==100
ps['actualCurrentPeers']=peers
for peer in peers:
 topic=m.read(C/f"src/content/topics/{peer['topicId']}.json");actual=next(q for q in topic['questions'] if q['id']==peer['id']);assert peer['card']==actual and m.sha(actual)==peer['sha256']
same={'actualCurrentPeers':[p for p in peers if p['topicId']=='books-publishing']}
for name,x in [('candidate',c),('sourceproof',sp),('peer-snapshot',ps)]:m.write(B/(name+'.json'),x)
q=m.apply(B,'01a14087-3629-7920-b330-2f4e29b4ff7d',[59,60],None,None,None,qualifyOnly=True,peerSnapshot=same)
m.write(D/'qualification-small59-60-fresh-cycle1.json',{'stage':'QUALIFIED_SAME_SOLE_CYCLE1_NOT_YET_APPLIED','sourceOriginal':str(A.relative_to(C)),'mechanicalAliasesOnly':True,'verified':{'cards':2,'groups':12,'variants':8,'currentPeers':100,'onlyFlaggedFieldsChanged':True},'qualification':q,'qualityCredit':0})
files=[p for p in A.rglob('*') if p.is_file()]+[p for p in B.rglob('*') if p.is_file()]+[pathlib.Path(__file__),D/'qualification-small59-60-fresh-cycle1.json']
freeze=h.save(C,'refs/heads/codex/question-quality-wave-6',files,'Freeze qualified fresh SOURCE2 same sole cycle1 proof before application');print('SOURCEFREEZE',freeze)
if '--apply' in sys.argv:
 m.apply(B,'01a14087-3629-7920-b330-2f4e29b4ff7d',[59,60],D/'apply-small59-60-fresh-cycle1.json',D/'qa-small59-60-fresh-cycle1.json',pathlib.Path(__file__),peerSnapshot=same,concerns=['Same sole substantive cycle1 after INITIAL FIX2; only note59[2],note60[3],explanation60 changed. All source/frozen MAIN/key/EASY unchanged.','Scoped Peace Corps no-page-reference description explicit in standalone glossary notes; #59 own correctnote extra fact usualback, sourceproof mapping repaired before apply.','100 exact CURRENT fullpeer cards and23bilateral pairs sourcepersonallychecked, first5 remains CURRENTuncredited awaitingfreshSOURCE/OTHER. FINAL unresolved defects HOLD0, no second substantivecycle.'])
 m.write(D/'source-freeze-small59-60-fresh-cycle1.json',{'freeze':freeze,'sourceNativeId':'01a14087-3629-7920-b330-2f4e29b4ff7d','actualCompactions':0,'qualityCredit':0})
