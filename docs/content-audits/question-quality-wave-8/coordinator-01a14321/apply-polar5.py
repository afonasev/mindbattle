"""Apply exact freshSOURCE5 only after complete proof preflight; no quality credit."""
import pathlib,importlib.util,subprocess,sys
D=pathlib.Path(__file__).parent;C=D.parents[3]
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('own',D/'owned-tools.py');a=load('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a.P=m.P;B=D.parent/'process-v2-polar5-6-8-10-fresh-01a14321/author/proof-completion5';ps=m.read(B/'peer-snapshot.json')
for p in ps['actualCurrentPeers']:assert p['card']==next(q for q in m.read(C/f"src/content/topics/{p['topicId']}.json")['questions'] if q['id']==p['id']) and m.sha(p['card'])==p['sha256']
sp=m.read(B/'sourceproof.json');e=m.read(B/'candidate.json')['entries'][0];q=e['proposedCard'];proof=sp['entries'][0]
assert proof['correctNoteNewFact']['noteLiteral']==q['answers'][q['correctIndex']]['note']
assert set(p['id'] for p in ps['actualCurrentPeers'])==set(p['id'] for p in ps['bilateralMainAssessments'])
for p in ps['bilateralMainAssessments']:assert p['candidateToPeer'] and p['peerToCandidate']
tp=C/'src/content/topics/polar-regions.json';assert tp.read_bytes()==subprocess.check_output(['git','-C',str(C),'show','refs/heads/codex/question-quality-wave-6:'+str(tp.relative_to(C))])
r=a.apply(B,'01a14327-fb48-70e1-8d55-3db044c2d83b',[5],D/'apply-polar5.json',D/'qa-polar5.json',pathlib.Path(__file__),qualifyOnly='--qualify-only' in sys.argv,peerSnapshot={'actualCurrentPeers':[p for p in ps['actualCurrentPeers'] if p['topicId']=='polar-regions']},concerns=['FreshSOURCE5 personally repaired decimal SouthMagnetic coordinate and supplied actualNorthPole extra ownnote; initial freshproof singlechar fields/wrongoptionextra/genericreverse were explicitly superseded by personallycompleted new proof-completion5.','Independent must assess whole actual geographic vs magneticpole alternatives under promptgeographic90N, broadadultEASY, all6literal4wholevariants/fullprimary and globalMAIN/fullactualpeers. Source5 may beclose to source6Southlatitude but frozenunique realrelations need meaningful bilateral assessment, no sharedtemplateautomaticPASS.'])
if '--qualify-only' in sys.argv:
 p=D/'qualification-polar5.json';m.write(p,{'qualified':True,'qualityCredit':0,'sourceFreeze':'f8b298b0cbddfddb03fa08a8d78dad868a4c0431','groups':len(r['finalGroupBindings']),'wholeVariants':len(r['finalVariantBindings']),'fullActualPeers':len(ps['actualCurrentPeers']),'crossTopicPeersVerifiedSeparately':True});print(m.savecode([p,pathlib.Path(__file__)],'Qualify exact freshSOURCE5 fullgroup/variant/crosspeer bindings no credit'))
