"""Prepare exact metadata for one already-applied solecycle1 SOURCE; no content judgments."""
import pathlib, importlib.util, sys
D = pathlib.Path(__file__).parent
s = importlib.util.spec_from_file_location('owned', D/'owned-tools.py')
m = importlib.util.module_from_spec(s)
s.loader.exec_module(m)
order, catalog_commit, raw_freeze, qualified_freeze = sys.argv[1:5]
order = int(order)
assert m.h.git(m.C,'rev-parse','--verify',catalog_commit+'^{commit}')==catalog_commit, 'Exact full tested catalog commit required'
label = 'fashion' + str(order) + '-cycle1'
packet_name=sys.argv[6] if len(sys.argv)>6 else 'source-'+label
assert packet_name.startswith('source-fashion'+str(order)) and packet_name.endswith('-cycle1') and pathlib.Path(packet_name).name==packet_name
B = D/('qualified-' + packet_name)
e = m.read(B/'candidate.json')['entries'][0]
q = m.read(m.C/'src/content/topics/fashion.json')['questions'][order-1]
assert q == e['proposedCard'] and m.sha(q) == e['afterHash']
qa_path = pathlib.Path(sys.argv[5]).resolve() if len(sys.argv)>5 else D/('qa-qualified-source-' + label + '.json')
assert qa_path.is_relative_to(D)
qa = m.read(qa_path)
assert qa['success'] and qa['numPassedTests'] == 19
assert qa['numFailedTests'] == qa['numPendingTests'] == 0
qa_commit = m.savecode([qa_path], 'Preserve exact '+label+' affected content QA19 PASS')
x = m.read(D/'manifest.json')
cp = m.read(m.P/'openspec/changes/question-quality-future-waves/current-checkpoint.json')
assert cp['owner'] == m.O and len(cp['currentEligibleCompletedIds']) == x['CURRENT']
t = m.read(D/('reader-fashion'+str(order)+'-initial-task.json'))
t.update(topicId='fashion', owner=m.O, manifest=str(D/'manifest.json'),
         binderSchemaReference=str(D/'bind-current-receipt.py'), role='independent reviewer one exact directed FINAL '+label,
         phase='START_FINAL_'+label.upper(), stage='FINAL', cycle=1, previousIndependentInitial=str(D/('independent-fashion'+str(order)+'-initial/receipt.json')), id=q['id'], sourceOrder=order,
         catalogCommit=catalog_commit, cardHash=m.sha(q),
         sourceFreeze=qualified_freeze, rawAuthorFreeze=raw_freeze,
         authorNativeId=m.read(B/'candidate.json')['sourceNativeId'],
         authorPacket=str(B), immutableRawAuthorPacket=str(D/packet_name),
         applyReport=str(D/('qualified-'+packet_name+'-apply.json')),
         qa=str(qa_path), qaSHA256=m.raw(qa_path), qaReportCommit=qa_commit,
         outputDirectory=str(D/('independent-'+label+'-final')),
         frozen={'id':q['id'], 'topicId':'fashion', 'sourceOrder':order,
                 'difficulty':q['difficulty'], 'correctIndex':q['correctIndex']},
         focus='Directed same-reader FINAL on your exact saved INITIAL defect and sole SOURCE-cycle1. Personally assess revised options/own notes and changed dependencies against complete retained primary contexts; verify unique key and actual absolute '+q['difficulty'].upper()+'. Preserve your own applicable judgments about unchanged literals by explicit exact pointer, no third full revision or inherited author verdict. Keep six/four exact whole-card bindings and current relevant bilateral MAIN peers. Unresolved defect is terminal HOLD; no new INITIAL/ordinarycycle2.',
         currentContext='CURRENT'+str(x['CURRENT'])+'/2000 remaining'+str(x['remaining'])+'. Exact solecycle1 applied '+label+' QA19PASS. All HOLD/attempt/cycle fences preserved. Catalog frozen until FINAL; no new INITIAL or ordinarycycle2.',
         contextPreflight='Verify own native session_meta and actual compacted events; never use coordinator env identity. Reviewer '+x['actors']['reviewer']['threadId']+'. First actual compaction finish this card only; second preservationSTOP. Compact task only, no whole checkpoint/history/catalog dump.',
         history='Your INITIAL FIX is immutable at previousIndependentInitial. This is its sole directed ordinary cycle1 FINAL, PASS or terminal HOLD; no reset. SOURCE READY/QA19 do not grant credit.')
t['returnSchema'] = t['returnSchema'].replace('stage INITIAL', 'stage FINAL').replace('status PASS/FIX/HOLD', 'status PASS/HOLD')
if 'actualPeerDependencyAddendum' in t:
 t['initialPeerDependencyHistory']={k:t.pop(k) for k in ['actualPeerDependencyAddendum','actualPeerDependencyBinding','peerCurrentRule'] if k in t}
 t['peerCurrentRule']='This exact cycle1 author packet has a fresh CURRENT peer snapshot. Initial peer delta is provenance only; verify actual CURRENT and preserve your applicable own INITIAL judgments.'
task_path = D/('reader-'+label+'-final-task.json')
m.write(task_path, t)
x['actors']['reviewer'].update(stage='START_FINAL_'+label.upper(), task=str(task_path),
                              expected='One directed FINAL '+label+' PASS/HOLD; no further ordinary cycle')
x['retainedIdleReviewer']=None
x['noRetainedIdleReviewer']=True
x['currentWork']={'id':q['id'], 'topicId':'fashion', 'sourceOrder':order,
                  'stage':'START_FINAL_'+label.upper(), 'sourceFreeze':qualified_freeze,
                  'rawAuthorFreeze':raw_freeze, 'catalogCommit':catalog_commit,
                  'qaReportCommit':qa_commit, 'qaPath':str(qa_path), 'cardHash':m.sha(q)}
x['next']='Directed FINAL '+label+' then deterministic PASS binding or terminal HOLD0'
m.write(D/'manifest.json', x)
print({'task':str(task_path), 'qaCommit':qa_commit,
       'taskCommit':m.savecode([task_path,D/'manifest.json',pathlib.Path(__file__)],
                              'Prepare directed FINAL '+label+' solecycle1 exact metadata')})
