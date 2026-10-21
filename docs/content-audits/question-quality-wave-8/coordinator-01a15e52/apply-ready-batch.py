"""Apply independent READY candidates atomically after complete unchanged-preimage qualification."""
import pathlib,importlib.util,sys
D=pathlib.Path(__file__).parent
s=importlib.util.spec_from_file_location('owned',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
s=importlib.util.spec_from_file_location('apply_standard',m.C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a=importlib.util.module_from_spec(s);s.loader.exec_module(a);a.P=m.P
x=m.read(D/'manifest.json');assert m.read(pathlib.Path(x['canonicalCheckpoint']))['owner']==m.O
assert all(m.flow.get(cid)[1]['owner']==m.O for cid in x['claims'])
reports=[];replacements={};files=[pathlib.Path(__file__)]
qa=D/'qa-source28-29-shared.json';baseline=m.h.git(m.C,'rev-parse','HEAD')
for name in sys.argv[1:]:
 B=D/name;c=m.read(B/'candidate.json');e=c['entries'][0];topic=e['topicId'];assert topic=='history-russia';ps=m.read(B/'peer-snapshot.json')
 report=a.apply(B,c['sourceNativeId'],[e['sourceOrder']],D/(name+'-apply.json'),qa,pathlib.Path(__file__),qualifyOnly=True,peerSnapshot={'actualCurrentPeers':[p for p in ps['actualCurrentPeers'] if p['topicId']==topic]})
 for entry in report['applied']:
  assert entry['id'] not in replacements;replacements[entry['id']]=entry['proposedCard']
 reports.append((name,report));files += [p for p in B.rglob('*') if p.is_file()]
tp=m.C/'src/content/topics/history-russia.json';before=m.read(tp);after={**before,'questions':[replacements.get(q['id'],q) for q in before['questions']]};assert a.read_issues(after)==[]
selection={'command':'node node_modules/vitest/vitest.mjs run tests/unit/catalog-topics.test.ts tests/unit/content.test.ts tests/unit/content-answer-notes.test.ts --reporter=json --outputFile='+str(qa.relative_to(m.C)),'reason':'Only exact SOURCE28+29 JSON candidates; full preimages/six/four/frozen contracts individually qualified against same baseline, combined catalog validation passed. One minimal affected19 run on exact common version, no full/runtime/build.'}
for name,report in reports:
 report.update(stage='Applied exact author CURRENT pending affected19 and independent INITIAL',qualityCredit=0,qaSelection=selection,sharedBatch={'baselineCatalogCommit':baseline,'ids':list(replacements),'applyCount':len(replacements),'catalogFrozenUntilIndependentVerdicts':True});p=D/(name+'-apply.json');m.write(p,report);files.append(p)
m.write(tp,after);files.append(tp)
rp=D/'source28-29-shared-apply.json';m.write(rp,{'owner':m.O,'baseline':baseline,'ids':list(replacements),'rawBeforeSHA256':m.sha(before),'rawAfterSHA256':m.sha(after),'perCardApplyReports':[str((D/(name+'-apply.json')).relative_to(m.C)) for name,_ in reports],'qaSelection':selection,'qualityCredit':0});files.append(rp)
print(m.savecode(files,'Apply exact qualified SOURCE28 and29 candidates on one catalog version without quality credit'))
