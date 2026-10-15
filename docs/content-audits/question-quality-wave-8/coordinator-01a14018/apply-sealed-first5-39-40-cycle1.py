"""Apply already-qualified pre-boundary SOURCE bytes; never regenerate SOURCE freeze."""
import pathlib,importlib.util,subprocess,json
C=pathlib.Path(__file__).resolve().parents[4];D=pathlib.Path(__file__).parent;B=D/'qualified-first5-39-40-cycle1'
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');h=load('preserve',D/'preserve-current-slice.py');m.P=h.P
freeze=m.read(D/'source-freeze-first5-39-40-cycle1.json')['freeze'];assert freeze=='b62221726b5798b24a77adf90dc68ecd5f72f51d';q=m.read(D/'qualification-first5-39-40-cycle1.json')['qualification'];intent=D/'apply-intent-sealed-first5-cycle1.json';case=D/'audit-case-sealed-first5-cycle1.json';m.write(intent,q);m.write(case,{'sourceFreeze':freeze,'applyPaths':[str(intent.relative_to(C))]})
subprocess.run(['python3',str(D/'bind-current-receipt.py'),str(case),'--audit-source-only'],check=True)
ps=m.read(B/'peer-snapshot.json');full=m.read(C/ps['fullCurrentTopicSnapshot']['path'])['cards'];delta=D/'first5-cycle1-current-peer-delta5.json'
m.apply(B,q['author'],[39,40],D/'apply-first5-39-40-cycle1.json',D/'qa-first5-39-40-cycle1.json',pathlib.Path(__file__),peerSnapshot={'actualCurrentPeers':full},peerAddendum=delta,concerns=q['editorialConcernsForOTHER'])
print('auditEvidence',h.save(C,'refs/heads/codex/question-quality-wave-6',[intent,case],'Preserve successful sealed SOURCE cycle1 lineage audit and application intent'))
