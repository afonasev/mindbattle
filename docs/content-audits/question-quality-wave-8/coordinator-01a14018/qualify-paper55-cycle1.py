"""Seal sole-cycle paper55 SOURCE action relation; no catalog mutation while OTHER5 runs."""
import pathlib,json,importlib.util,copy
C=pathlib.Path(__file__).resolve().parents[4];D=pathlib.Path(__file__).parent;A=C/'docs/content-audits/question-quality-wave-8/process-v2-books55-cycle1-01a14018/author';B=D/'qualified-paper55-cycle1';B.mkdir(exist_ok=True)
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');h=load('preserve',D/'preserve-current-slice.py');m.P=h.P;uid='01a140af-57d4-71f2-b8fc-631403e1aaf2';fs=[f for base in ['sessions','archived_sessions'] for f in (pathlib.Path.home()/'.codex'/base).rglob('*'+uid+'.jsonl')];assert len(fs)==1;actual=sum(json.loads(l).get('type')=='compacted' for l in fs[0].open());assert actual<2
c=m.read(A/'candidate.json');sp=m.read(A/'sourceproof.json');p=m.read(A/'current-main-peer-delta.json');delta=m.read(A/'exact-current-completion-ready5-delta.json');assert len(c['entries'])==len(sp['entries'])==1 and c['entries'][0]['sourceOrder']==55;assert c['entries'][0]['status']=='READY_FOR_INDEPENDENT_REVIEW';ex=c['entries'][0]['proposedCard']['explanation'];assert 2<=sum(ex.count(x) for x in ['.','!','?'])<=4 and len(ex.split())<=70
for s in sp['rawSources']:assert m.raw(C/s['path'])==s['sha256']
assert delta['ownSourceReadEvidence'] and delta['relevantMAINJudgments'];assert m.raw(C/delta['catalogPath'])==delta['catalogRawSHA256'];replacements={e['id']:e for e in delta['entries']}
for e in replacements.values():assert e['currentCardValueExactlyMatchesOwnProposal'] and e['currentCard']==e['authorProposal'] and m.sha(e['currentCard'])==e['currentCanonicalSHA256']==e['authorProposalCanonicalSHA256']
oldTopic=m.read(A/'books-publishing-current100.json');topic=m.read(C/'src/content/topics/books-publishing.json');assert len(oldTopic['questions'])==len(topic['questions'])==100;current={q['id']:q for q in topic['questions']};updated=[]
for before in oldTopic['questions']:
 after=current[before['id']]
 if before!=after:assert before['id'] in replacements and after==replacements[before['id']]['currentCard'];updated.append(before['id'])
assert set(updated)==set(replacements)
full=[{'id':q['id'],'topicId':'books-publishing','sourceOrder':n,'card':q,'sha256':m.sha(q)} for n,q in enumerate(topic['questions'],1)];cross=[]
for hit in p['allTopicFullCardHits']:
 tid=pathlib.Path(hit['topicFile']).stem;t=m.read(C/f'src/content/topics/{tid}.json');q=next(q for q in t['questions'] if q['id']==hit['card']['id']);old=hit['card']
 if q!=old:assert q['id'] in replacements and q==replacements[q['id']]['currentCard']
 if tid!='books-publishing':cross.append({'id':q['id'],'topicId':tid,'sourceOrder':t['questions'].index(q)+1,'card':q,'sha256':m.sha(q)})
peer={'actualCurrentPeers':full+cross,'sourceOriginalPeerAudit':str((A/'current-main-peer-delta.json').relative_to(C)),'sourceOwnProposalPromotion5':str((A/'exact-current-completion-ready5-delta.json').relative_to(C)),'sourceMainJudgments':delta['relevantMAINJudgments'],'sourceMainDistinctness':sp['entries'][0]['mainDistinctness'],'technicalComposition':'Only exact ownSOURCE proposal→CURRENT promotion and full snapshot adapters; no root semantic judgments.'}
for e in c['entries']:e['topicId']=c['topicId']
for e in sp['entries']:
 for g in e['literalGroups']:
  assert all(x in sp['rawSources'] for x in g['sourcePaths']);g['sourcePaths']=[x['path'] for x in g['sourcePaths']]
 for v in e['fourFullPromptAnswerNoteAssessments']:
  v['fullPrompt']=v['prompt'];v['tripleSHA256']=v['tripleCanonicalSHA256'];assert all(x in sp['rawSources'] for x in v['sourcePaths']);v['sourcePaths']=[x['path'] for x in v['sourcePaths']]
for name,x in [('candidate',c),('sourceproof',sp),('peer-snapshot',peer)]:m.write(B/(name+'.json'),x)
q=m.apply(B,uid,[55],None,None,None,qualifyOnly=True,peerSnapshot={'actualCurrentPeers':full});m.write(D/'qualification-paper55-cycle1.json',{'qualification':q,'stage':'QUALIFIED_WAIT_OTHER5_END_BEFORE_APPLY','qualityCredit':0,'actualSourceCompactions':actual,'sourceOriginal':str(A.relative_to(C)),'oneSubstantiveCycle':1,'verified':{'cards':1,'literalGroups':6,'individualVariants':4,'ownSourcePromotion5':5},'mustIndependentlyJudge':'Distinct sheet-feed action vsmaterials6 substrate, actualEASY/onekey/fourplausible/ownnoteextra/grammar/source truth, not assumed fromSOURCE.'});files=[f for f in A.rglob('*') if f.is_file()]+[f for f in B.rglob('*') if f.is_file()]+[pathlib.Path(__file__),D/'qualification-paper55-cycle1.json'];freeze=h.save(C,'refs/heads/codex/question-quality-wave-6',files,'Freeze qualified solecycle1 SOURCEpaper55 real sheet-feed relation before actual2');m.write(D/'source-freeze-paper55-cycle1.json',{'freeze':freeze,'author':uid,'actualCompactions':actual,'qualityCredit':0});print('SOURCEFREEZE',freeze)
