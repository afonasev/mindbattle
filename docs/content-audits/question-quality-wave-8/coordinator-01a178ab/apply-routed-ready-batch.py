"""Apply independent READY candidates atomically after complete unchanged-preimage qualification."""
import pathlib,importlib.util,sys
D=pathlib.Path(__file__).parent
s=importlib.util.spec_from_file_location('owned',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
s=importlib.util.spec_from_file_location('apply_standard',m.C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');a=importlib.util.module_from_spec(s);s.loader.exec_module(a);a.P=m.P
x=m.read(D/'manifest.json');assert m.read(pathlib.Path(x['canonicalCheckpoint']))['owner']==m.O
assert all(m.flow.get(cid)[1]['owner']==m.O for cid in x['claims'])
reports=[];replacements={};files=[pathlib.Path(__file__)]
assert len(sys.argv[1:])==2  # existing READY queue bound
assert x['activeRoute']['wave']==9 and x['activeRoute']['topicId']=='cars-road-transport'
assert not x['actors']['reviewer']['stage'].startswith('START'), 'Catalog frozen during independent verdict'
assert m.read(m.P/'.flow-leases.json')=={}
for root,key in [(m.C,'code'),(m.P,'planning')]:
 assert m.raw(pathlib.Path(m.h.git(root,'rev-parse','--path-format=absolute','--git-path','index')))==x['foreignIndexes'][key]
batch_orders=[m.read(D/name/'candidate.json')['entries'][0]['sourceOrder'] for name in sys.argv[1:]]
batch_cycles={m.read(D/name/'candidate.json')['cycle'] for name in sys.argv[1:]}
assert batch_cycles <= {0,1}  # each exact initial/sole-cycle1 lineage is qualified independently
batch_label='-'.join(str(m.read(D/name/'candidate.json')['entries'][0]['sourceOrder'])+'cycle'+str(m.read(D/name/'candidate.json')['cycle']) for name in sys.argv[1:])
qa=D/f'qa-source{batch_label}-shared.json';baseline=m.h.git(m.C,'rev-parse','HEAD')
assert not qa.exists(), 'Never overwrite an earlier exact QA report'
for name in sys.argv[1:]:
 B=D/name;c=m.read(B/'candidate.json');e=c['entries'][0];topic=e['topicId'];assert topic=='cars-road-transport';ps=m.read(B/'peer-snapshot.json')
 if c['cycle']==1:
  initial=m.read(D/('independent-cars-road-transport'+str(e['sourceOrder'])+'-initial/receipt.json'))
  assert initial['entries'][0]['status']=='FIX' and initial['entries'][0]['currentCard']==e['beforeCard']
 report=a.apply(B,c['sourceNativeId'],[e['sourceOrder']],D/(name+'-apply.json'),qa,pathlib.Path(__file__),qualifyOnly=True,peerSnapshot={'actualCurrentPeers':[p for p in ps['actualCurrentPeers'] if p['topicId']==topic]})
 for entry in report['applied']:
  assert entry['id'] not in replacements;replacements[entry['id']]=entry['proposedCard']
 reports.append((name,report));files += [p for p in B.rglob('*') if p.is_file()]
tp=m.C/'src/content/topics/cars-road-transport.json';before_raw_sha=m.raw(tp);before=m.read(tp);after={**before,'questions':[replacements.get(q['id'],q) for q in before['questions']]};assert a.read_issues(after)==[]
selection={'command':'node node_modules/vitest/vitest.mjs run tests/unit/catalog-topics.test.ts tests/unit/content.test.ts tests/unit/content-answer-notes.test.ts --reporter=json --outputFile='+str(qa.relative_to(m.C)),'reason':f'Only exact SOURCE{batch_label} JSON candidates; full preimages/six/four/frozen contracts individually qualified against same baseline, combined catalog validation passed. One minimal affected19 run on exact common version, no full/runtime/build.'}
for name,report in reports:
 report.update(stage='Applied exact author CURRENT pending affected19 and exact independent stage',qualityCredit=0,qaSelection=selection,sharedBatch={'baselineCatalogCommit':baseline,'ids':list(replacements),'applyCount':len(replacements),'catalogFrozenUntilIndependentVerdicts':True});p=D/(name+'-apply.json');m.write(p,report);files.append(p)
m.write(tp,after);files.append(tp)
rp=D/f'source{batch_label}-shared-apply.json';m.write(rp,{'owner':m.O,'baseline':baseline,'ids':list(replacements),'rawBeforeSHA256':before_raw_sha,'rawAfterSHA256':m.raw(tp),'beforeCanonicalSHA256':m.sha(before),'afterCanonicalSHA256':m.sha(after),'perCardApplyReports':[str((D/(name+'-apply.json')).relative_to(m.C)) for name,_ in reports],'qaSelection':selection,'qualityCredit':0});files.append(rp)
print(m.savecode(files,f'Apply exact qualified SOURCE{batch_label} candidates on one catalog version without quality credit'))
