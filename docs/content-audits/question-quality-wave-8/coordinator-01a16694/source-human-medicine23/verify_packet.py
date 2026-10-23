import hashlib,json
from pathlib import Path
C=Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle')
O=C/'docs/content-audits/question-quality-wave-8/coordinator-01a16694/source-human-medicine23'
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def sha(x):return hashlib.sha256(canon(x)).hexdigest()
def j(name):return json.loads((O/name).read_text(encoding='utf-8'))
c,s,p=j('candidate.json'),j('sourceproof.json'),j('peer-snapshot.json')
assert c['sourceNativeId']==s['sourceNativeId']==p['sourceNativeId']=='01a166c1-3f9d-71e3-9f08-7c44ba06372e'
assert c['topicId']==s['topicId']==p['topicId']=='human-medicine'
assert c['cycle']==s['cycle']==p['cycle']==0
assert len(c['entries'])==len(s['entries'])==1
ce,se=c['entries'][0],s['entries'][0]
assert ce['id']==se['id']=='human-medicine-loop-henle-gradient'
assert ce['status']==se['status']=='HOLD'
assert ce['sourceOrder']==se['sourceOrder']==23
assert sha(ce['beforeCard'])==ce['beforeHash']=='f1c3d29b5910c9ff540e68bec66f2fe8fec0b929eababdcdd2f03906cd895cef'
assert sha(ce['proposedCard'])==ce['afterHash'] and ce['beforeHash']==ce['afterHash']
assert ce['beforeCard']==ce['proposedCard']
def groups(card):
 return {'prompt_ordered_answers_key':{'prompt':card['prompt'],'answers':[a['text'] for a in card['answers']],'correctIndex':card['correctIndex']},'explanation':card['explanation'],**{'note'+str(i):a['note'] for i,a in enumerate(card['answers'])}}
bg,ag=groups(ce['beforeCard']),groups(ce['proposedCard'])
for k in bg:
 assert ce['fieldGroups'][k]['beforeCanonicalSHA256']==sha(bg[k])
 assert ce['fieldGroups'][k]['afterCanonicalSHA256']==sha(ag[k])
assert set(ce['fieldGroups'])=={'prompt_ordered_answers_key','explanation','note0','note1','note2','note3'}
assert len(se['literalGroups'])==6 and len(se['fourFullPromptAnswerNoteAssessments'])==4
assert [v['slot'] for v in se['fourFullPromptAnswerNoteAssessments']]==[0,1,2,3]
for g in se['literalGroups']:
 assert g['literal']==ag[g['group']]
 assert g['literalSHA256']==sha(g['literal'])
for v in se['fourFullPromptAnswerNoteAssessments']:
 assert v['tripleSHA256']==sha({'prompt':v['fullPrompt'],'answer':v['answer'],'note':v['note']})
for entry in s['rawSources']:
 q=C/entry['path']
 assert q.exists() and hashlib.sha256(q.read_bytes()).hexdigest()==entry['sha256'],entry['path']
 if entry.get('completeOutputPointer') and entry.get('completeOutputSHA256'):
  raw=json.loads(q.read_text(encoding='utf-8'))
  value=raw
  for part in entry['completeOutputPointer'].strip('/').split('/'):
   part=part.replace('~1','/').replace('~0','~')
   value=value[int(part)] if isinstance(value,list) else value[part]
  assert hashlib.sha256(value.encode('utf-8')).hexdigest()==entry['completeOutputSHA256'],entry['path']
assert len(p['globalMAIN']['allCurrentFileByteBindings'])==110
assert len(p['globalMAIN']['rows'])==11000
assert p['globalMAIN']['rowsCanonicalSHA256']==sha(p['globalMAIN']['rows'])
assert all(set(r)=={'topicId','id','prompt','answers','correctIndex'} for r in p['globalMAIN']['rows'])
assert len(p['actualCurrentPeers'])==100
assert len(p['relevantSameTopicPairs'])==7 and len(p['relevantCrossTopicPeers'])==1
assert p['candidateCurrent']['sha256']==p['candidateProposed']['sha256']==ce['beforeHash']
for peer in p['actualCurrentPeers']:
 assert peer['sha256']==sha(peer['card'])
for pair in p['relevantSameTopicPairs']:
 assert pair['peerCurrent']['sha256']==sha(pair['peerCurrent']['card'])
# Verify exact native session identity and top-level compaction count only.
uid='01a166c1-3f9d-71e3-9f08-7c44ba06372e'
journal=Path('/Users/eaafonasev/.codex/sessions/2026/10/23/rollout-2026-10-23T08-15-03-01a166c1-3f9d-71e3-9f08-7c44ba06372e.jsonl')
meta=None;compact=0
for line in journal.open(encoding='utf-8'):
 try:x=json.loads(line)
 except:continue
 if x.get('type')=='session_meta':meta=x.get('payload',{}).get('id')
 if x.get('type')=='compacted':compact+=1
assert meta==uid
print(json.dumps({'status':'PASS_MECHANICAL_PACKET_ONLY','card':'human-medicine-loop-henle-gradient','candidate':'HOLD','sourceproof':'HOLD','beforeAfterHashEqual':True,'literalGroups':6,'variants':4,'sameTopicPeers':100,'bilateralPairs':7,'crossTopicPeers':1,'globalRows':11000,'sourceFileHashes':'verified','nativeIdentity':'verified','actualCompactions':compact,'semanticOrIndependentQA':'NOT_RUN','qualityCredit':0},ensure_ascii=False))
