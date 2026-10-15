"""Qualify personal fresh SOURCE adoption, unchanged five cards; no catalog write."""
import pathlib,importlib.util,copy,json
C=pathlib.Path(__file__).resolve().parents[4];D=pathlib.Path(__file__).parent;A=C/'docs/content-audits/question-quality-wave-8/process-v2-first5-current-source-adoption-01a14018/author'
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');m.P=pathlib.Path('/Users/eaafonasev/Projects/mindbattle/planning');h=load('preserve',D/'preserve-current-slice.py')
a=m.read(A/'candidate.json');sp=m.read(A/'sourceproof.json');ps=m.read(A/'peer-snapshot.json');f=ps['fullCurrentTopicSnapshot'];assert m.raw(C/f['path'])==f['rawSHA256'] and f['personalReadEvidence'];full=m.read(C/f['path'])['cards'];assert len(full)==100
for e in a['entries']:assert e['beforeCard']==e['proposedCard'] and e['beforeHash']==e['afterHash']
for s in sp['rawSources']:assert s['personalread'] and s['readEvidence'] and m.raw(C/s['path'])==s['sha256']
cat={q['id']:q for q in m.read(C/'src/content/topics/books-publishing.json')['questions']};delta=[]
for peer in full:
 assert m.sha(peer['card'])==peer['sha256'];actual=cat[peer['id']]
 if peer['card']!=actual:
  assert peer['sourceOrder'] in [59,60];old=peer['card'];assert old['prompt']==actual['prompt'] and old['correctIndex']==actual['correctIndex'] and [a['text'] for a in old['answers']]==[a['text'] for a in actual['answers']]
  delta.append({**peer,'card':actual,'sha256':m.sha(actual)})
assert {p['sourceOrder'] for p in delta}=={59,60}
for peer in ps['crossTopicCandidates']:
 topic=m.read(C/f"src/content/topics/{peer['topicId']}.json");actual=next(q for q in topic['questions'] if q['id']==peer['id']);assert actual==peer['card'] and m.sha(actual)==peer['sha256']
for pair in ps['relevantProposedPairs']:
 assert pair['candidateCard']==cat[pair['candidateId']] and m.sha(pair['candidateCard'])==pair['candidateSHA256'];assert pair['bilateralMAIN']
 # Cross peers are validated above; all within-topic counterparts are exact CURRENT.
 if pair['peerId'] in cat:assert pair['peerCard']==cat[pair['peerId']] and m.sha(pair['peerCard'])==pair['peerSHA256']
deltaPath=D/'first5-fresh-source-peer-delta-small2.json';m.write(deltaPath,{'actualCurrentPeers':delta,'meaning':'Root mechanical binding of the concurrently applied same-cycle1 small2. MAIN prompt/orderedanswer/key are byteidentical to SOURCE-read original peer snapshot. Only scoped notes/explanation changed; no root semantic/source PASS invented.','sourceSnapshot':f['path'],'appliedSmall2Receipt':str((D/'apply-small59-60-fresh-cycle1.json').relative_to(C)),'qualityCredit':0})
q=m.apply(A,'01a14072-7b0b-7d62-840c-d43cd18d4cfc',[33,35,38,39,40],None,None,None,qualifyOnly=True,peerSnapshot={'actualCurrentPeers':full},peerAddendum=deltaPath,concerns=['Fresh personal SOURCE5 adoption exactCURRENT no literalchange; old postsecondcompaction SOURCE receipts not used.','Raw8 completeprimarycontexts,30literal groups20individualvariants,full100source snapshot+crossUPC and6relevantpairs. Initial wrongprovenance fixed personally beforequalification. Independent reader must assess actual truth/onekey/level/MAIN without inheriting SOURCE PASS.','Concurrent small2 changes onlyscopednote/explanation; original SOURCE-readMAIN unchanged, explicitrootpeerDelta2 binds actualcurrent.'])
q['stage']='SOURCE_ADOPTION_EXACT_CURRENT_NO_CATALOG_CHANGE';q['verified']={'cards':5,'literalGroups':30,'variants':20,'sourceReadFullTopicCards':100,'rootPeerDelta2':2,'actualSourceCompactions':0};out=D/'adoption-first5-fresh-current-source.json';m.write(out,q)
files=[p for p in A.rglob('*') if p.is_file()]+[pathlib.Path(__file__),out,deltaPath];freeze=h.save(C,'refs/heads/codex/question-quality-wave-6',files,'Freeze qualified personal fresh SOURCE adoption exact CURRENT five; no catalog change');m.write(D/'source-freeze-first5-fresh-adoption.json',{'freeze':freeze,'author':'01a14072-7b0b-7d62-840c-d43cd18d4cfc','qualityCredit':0});print('SOURCEFREEZE',freeze)
