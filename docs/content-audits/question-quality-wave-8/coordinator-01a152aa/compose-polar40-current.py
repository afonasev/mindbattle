"""Losslessly compose completed SOURCE40 with its author's current30 delta."""
import pathlib,importlib.util,json,subprocess
D=pathlib.Path(__file__).parent;C=D.parents[3]
def mod(n,p):
 s=importlib.util.spec_from_file_location(n,p);x=importlib.util.module_from_spec(s);s.loader.exec_module(x);return x
m=mod('o',D/'owned-tools.py');a=mod('a',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a.P=m.P
R=D/'qualified-polar40-complete';B=D/'qualified-polar40-current';A=D/'source-polar40-current-parks30-delta/current-delta.json';author='01a152f1-2607-7d71-9ef8-56c47c471fb9'
for uid in [m.O,author,'01a150d1-3383-7d30-ad23-76d70ec18813']:
 j=next(pathlib.Path('/Users/eaafonasev/.codex/sessions/2026/10/19').glob('*'+uid+'.jsonl'));assert sum(json.loads(l).get('type')=='compacted' for l in j.open())<2
for n in ['candidate.json','sourceproof.json','peer-snapshot.json']:
 p=R/n;assert p.read_bytes()==subprocess.check_output(['git','-C',str(C),'show','efe26cd28b83cf1ae2d8b9f64099a969c0127959:'+str(p.relative_to(C))])
assert A.read_bytes()==subprocess.check_output(['git','-C',str(C),'show','bc528d143a967a6f534e8e7fc663491d493616fc:'+str(A.relative_to(C))])
delta=m.read(A);candidate=m.read(R/'candidate.json');sp=m.read(R/'sourceproof.json');ps=m.read(R/'peer-snapshot.json');assert delta['sourceNativeId']==author and delta['source40']['immutableCandidateSHA256']==candidate['entries'][0]['afterHash']=='91a8dcd22d2b3bcd4220ed88be57ca5d470e8da64c75e2e3470df8b9ea2c7173'
app=m.read(D/'apply-parks30-fresh.json')['applied'][0];cur=delta['currentCard'];assert m.raw(pathlib.Path(delta['applyReceipt']['path']))==delta['applyReceipt']['fileSHA256'];assert cur['card']==app['proposedCard'] and m.sha(cur['card'])==cur['cardCanonicalSHA256']=='c1e2c453858cd3da3c98b64282a570ca6618cbc4ced80d32a4e35290ac6a06af'
tp=C/'src/content/topics/national-parks-nature.json';old=json.loads(subprocess.check_output(['git','-C',str(C),'show','d6ba5eb5a71de2f78f255eb9a18550b503910185:src/content/topics/national-parks-nature.json']));live=m.read(tp);assert m.raw(tp)==cur['sourceFileSHA256'];assert all(q==old['questions'][i] for i,q in enumerate(live['questions']) if q['id']!=app['id']);assert old['questions'][29]==app['beforeCard'] and live['questions'][29]==cur['card']
b=app['beforeCard'];c=app['proposedCard'];assert b['prompt']==c['prompt'] and b['correctIndex']==c['correctIndex'] and [v['text'] for v in b['answers']]==[v['text'] for v in c['answers']]
rows=[];cat={}
for sf in delta['currentGlobalMAIN']['allCurrentFileByteBindings']:
 p=C/sf['path'];assert m.raw(p)==sf['fileSha256'];t=m.read(p);assert len(t['questions'])==sf['questionCount']
 for q in t['questions']:cat[q['id']]={'topicId':t['id'],'card':q};rows.append({'topicId':t['id'],'id':q['id'],'prompt':q['prompt'],'answers':[v['text'] for v in q['answers']],'correctIndex':q['correctIndex']})
assert len(rows)==11000 and m.sha(rows)==delta['currentGlobalMAIN']['rowsCanonicalSHA256']==ps['global11000MainAudit']['rowsCanonicalSHA256']=='551dbca3a5e583a27e9ac58f5109b86ccac43fc83de5400a96f981770ec542f6'
for p in ps['actualCurrentPeers']:assert cat[p['id']]['card']==p['card'] and m.sha(p['card'])==p['sha256']
rel=delta['bilateralRelevance'];assert rel['source40']['id']==candidate['entries'][0]['id'] and rel['current30']['id']==cur['id'] and rel['source40To30'] and rel['30ToSource40'] and rel['directReverse']
ps['actualCurrentPeers'].append({'id':cur['id'],'topicId':cur['topicId'],'sourceOrder':30,'card':cur['card'],'sha256':cur['cardCanonicalSHA256']});ps['historicalGlobalManifestNotice']='Original SOURCE40 global11000MainAudit fileInventory is the personally read pre30-note-change snapshot; its MAIN projection is byte-identical. Current author-owned delta below supplies current110 file byte bindings and full30 postimage.'
ps['currentPersonalSOURCEManifestDelta']={'path':str(A.relative_to(C)),'rawSHA256':m.raw(A),'freeze':'bc528d143a967a6f534e8e7fc663491d493616fc','originalAuthorAddendum':delta,'operation':'Lossless original SOURCE author current30 note-only personalread/110file MAIN delta; no ROOT semantic judgment or inherited30 grade.'}
B.mkdir(exist_ok=True)
for n,v in [('candidate.json',candidate),('sourceproof.json',sp),('peer-snapshot.json',ps)]:m.write(B/n,v)
q=m.read(D/'qualification-polar40-complete.json');concerns=q['editorialConcernsForOTHER']+['Author-owned post30 note-only delta bc528 preservescomplete40SOURCEceeb/efe26 all6/4/primaries unchanged. Newcurrent30c1e2 notes0/2/explanation/source only applyd87b; historicalparks961a file notcurrent nowef1c115. Exactauthorpersonal30fullbody andbothwaysERVC/directreverse plusfresh110manifest verifiesMAIN551 unchanged. CurrentManifestAddendum inqualifiedpeerpacket isauthorown notROOTinference; readerfreshcurrent global after40apply required. No30qualityapproval.']
r=a.apply(B,author,[40],D/'apply-polar40-current.json',D/'qa-polar40-current.json',pathlib.Path(__file__),qualifyOnly=True,peerSnapshot={'actualCurrentPeers':[p for p in ps['actualCurrentPeers'] if p['topicId']=='polar-regions']},concerns=concerns);r.update(rawSourceFreeze='ceebce65445cd30c8c5b4b18e9e071bef9bd93e5',personalCurrent30DeltaFreeze='bc528d143a967a6f534e8e7fc663491d493616fc',CURRENT=888,remaining=1112,fullGoal=2000,qualityCredit=0);m.write(D/'qualification-polar40-current.json',r);print(m.savecode(list(B.glob('*.json'))+[D/'qualification-polar40-current.json',pathlib.Path(__file__)],'Compose fullpersonalSOURCE40 and owncurrent30 noteonlymanifest delta READY0'))
