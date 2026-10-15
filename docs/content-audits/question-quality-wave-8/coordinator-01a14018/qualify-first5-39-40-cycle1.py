"""Qualify unchanged-key SOURCE solecycle1 two; bind concurrent note-only peer deltas."""
import pathlib,importlib.util,sys,copy,json
C=pathlib.Path(__file__).resolve().parents[4];D=pathlib.Path(__file__).parent;A=C/'docs/content-audits/question-quality-wave-8/process-v2-first5-39-40-cycle1-01a14018/author';B=D/'qualified-first5-39-40-cycle1';B.mkdir(exist_ok=True)
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');h=load('preserve',D/'preserve-current-slice.py');m.P=h.P
uid='01a14072-7b0b-7d62-840c-d43cd18d4cfc';fs=[f for base in ['sessions','archived_sessions'] for f in (pathlib.Path.home()/'.codex'/base).rglob('*'+uid+'.jsonl')];assert len(fs)==1;actual=sum(json.loads(l).get('type')=='compacted' for l in fs[0].open());assert actual<2,actual
c=m.read(A/'candidate.json');sp=m.read(A/'sourceproof.json');ps=m.read(A/'peer-snapshot.json');snap=ps['fullCurrentTopicSnapshot'];assert m.raw(C/snap['path'])==snap['rawSHA256'] and snap['personalReadEvidence'];full=m.read(C/snap['path'])['cards'];cat={q['id']:q for q in m.read(C/'src/content/topics/books-publishing.json')['questions']};delta=[]
for p in full:
 assert m.sha(p['card'])==p['sha256'];a=cat[p['id']]
 if a!=p['card']:
  assert p['sourceOrder'] in [51,52,54,59,60];old=p['card'];assert old['prompt']==a['prompt'] and old['correctIndex']==a['correctIndex'] and [x['text'] for x in old['answers']]==[x['text'] for x in a['answers']];delta.append({**p,'card':a,'sha256':m.sha(a)})
assert len(delta)==5
for s in sp['rawSources']:assert m.raw(C/s['path'])==s['sha256'] and s['personalread'] and s['readProvenance']
for e in c['entries']:
 assert e['sourceOrder'] in [39,40] and e['status']=='READY_FOR_INDEPENDENT_REVIEW';assert 2<=sum(e['proposedCard']['explanation'].count(x) for x in ['.','!','?'])<=4 and len(e['proposedCard']['explanation'].split())<=70
 # Adjacent certified3 literal cards are never changed by this cycle.
for name,x in [('candidate',c),('sourceproof',sp),('peer-snapshot',ps)]:m.write(B/(name+'.json'),x)
deltaPath=D/'first5-cycle1-current-peer-delta5.json';m.write(deltaPath,{'actualCurrentPeers':delta,'sourceReadSnapshot':snap,'meaning':'Concurrent applied51/52/54 and59/60: only notes/explanations changed, actual MAIN/orderedanswers/key byteidentical to SOURCE-read snapshot. Root technical current binding only; no new semantic authorPASS. SOURCE saved initial33/35/38 proposals are also literal-identical actualCURRENT and certified, not unimplemented cards.','qualityCredit':0})
q=m.apply(B,uid,[39,40],None,None,None,qualifyOnly=True,peerSnapshot={'actualCurrentPeers':full},peerAddendum=deltaPath,concerns=['Sole substantivecycle1 after exact INITIAL FIX39/40. SOURCE39 key-title/medium/continuingresource distinguishes DOI; note8characters/checkX. SOURCE40 anyentityscope distinguishesISBN; newownextraRAmetadata/reference-services beyondnewprompt. OTHER must independently judge factualsource, uniqueness, grammar, ownextra and actualMEDIUM.','SOURCE originalpacket and frozen2 initialraw retained; root technicalpeerDelta5 onlynotes/EXPL noMAINchange; first3certifiedprotected. UnqualifiedSOURCE15 remains paused and unaccepted; no impliedquality fromproposal snapshots.','If unresolvedafterFINAL HOLD0, no second substantivecycle.'])
m.write(D/'qualification-first5-39-40-cycle1.json',{'qualification':q,'qualityCredit':0,'stage':'QUALIFIED_NOT_YET_APPLIED_WAIT_OTHER3','actualSourceCompactions':actual,'sourceOriginal':str(A.relative_to(C))});files=[f for f in A.rglob('*') if f.is_file()]+[f for f in B.rglob('*') if f.is_file()]+[pathlib.Path(__file__),deltaPath,D/'qualification-first5-39-40-cycle1.json'];freeze=h.save(C,'refs/heads/codex/question-quality-wave-6',files,'Freeze qualified SOURCE39/40 solecycle1 exact proofs before final review');m.write(D/'source-freeze-first5-39-40-cycle1.json',{'freeze':freeze,'author':uid,'actualCompactions':actual,'qualityCredit':0});print('SOURCEFREEZE',freeze)
if '--apply' in sys.argv:
 m.apply(B,uid,[39,40],D/'apply-first5-39-40-cycle1.json',D/'qa-first5-39-40-cycle1.json',pathlib.Path(__file__),peerSnapshot={'actualCurrentPeers':full},peerAddendum=deltaPath,concerns=q['editorialConcernsForOTHER'])
