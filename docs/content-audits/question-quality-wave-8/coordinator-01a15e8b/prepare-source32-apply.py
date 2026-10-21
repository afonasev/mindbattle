"""Bind SOURCE32 originals and select affected checks; no editorial judgment."""
import pathlib,json,importlib.util
D=pathlib.Path(__file__).parent
s=importlib.util.spec_from_file_location('m',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
x=m.read(D/'manifest.json');R=D/'source-history-russia32';combined=m.read(R/'raw/native-web-attempts.json');rr=[json.loads(l) for l in pathlib.Path(x['actors']['author32']['nativeJournal']).open()]
assert combined['actualWebCallCount']==len(combined['calls'])==4
for c in combined['calls']:
 for key,typ in [('callRecord','custom_tool_call'),('resultRecord','custom_tool_call_output')]:
  found=[r for r in rr if r.get('payload',{}).get('type')==typ and r['payload'].get('call_id')==c['callId']]
  assert len(found)==1 and found[0]==c[key]
rep={'owner':m.O,'actualWebCalls':4,'actualOpenedURLs':4,'allFourOriginalCallsAndResultsAlreadyRetained':True,'combinedRaw':str(R/'raw/native-web-attempts.json'),'sha256':m.raw(R/'raw/native-web-attempts.json'),'meaning':'verify-network produced individual wrappers from exact native network0 because combined calls/resultRecord container is not a standalone originalRecord wrapper. No original loss/refetch/retry.','ownContainerDiagnostic':'First own check assumed prior31 requestRecord container and failed KeyError; shape inspection proved explicit callRecord. This script checks same exact native record equality; raw unchanged.','qualityCredit':0}
m.write(D/'history-russia32-network-container-verification.json',rep)
x['qaSelectionHistoryRussia32']={'baseline':m.h.git(m.C,'rev-parse','HEAD'),'beforeHash':'1051ef7519ed6dcceb71f4d8037527516965f705e02b12c826c78adb86a314c5','afterHash':'9cc6e1c955910cdc9f390215d132a1c9de616248bafbcaf04fee2ba24e8585e0','diff':'Only explanation and source metadata for one content card; ID/order/key/difficulty/prompt/answers unchanged.','command':'node node_modules/vitest/vitest.mjs run tests/unit/catalog-topics.test.ts tests/unit/content.test.ts tests/unit/content-answer-notes.test.ts --reporter=json --outputFile='+str(D/'qa-qualified-source-history-russia32.json'),'typecheck':'NotRun JSON-only card change','runtime':'NotRun prohibited','reason':'Affected catalog/content/answer-note contracts; preserve exact19 scope, no full suite.'}
m.write(D/'manifest.json',x)
print(m.savecode([D/'manifest.json',D/'history-russia32-network-container-verification.json',D/'source32-intake-attempt1.json',pathlib.Path(__file__)],'Record SOURCE32 originals and minimal affected QA selection'))
