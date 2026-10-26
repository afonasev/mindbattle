"""Prepare exact metadata for one already-applied SOURCE; no content judgments."""
import pathlib, importlib.util, sys
D = pathlib.Path(__file__).parent
s = importlib.util.spec_from_file_location('owned', D/'owned-tools.py')
m = importlib.util.module_from_spec(s)
s.loader.exec_module(m)
order, catalog_commit, raw_freeze, qualified_freeze = sys.argv[1:5]
order = int(order)
assert m.h.git(m.C, 'rev-parse', '--verify', catalog_commit+'^{commit}') == catalog_commit, 'Exact full tested catalog commit required'
label = 'cars-road-transport' + str(order)
packet_name = sys.argv[5] if len(sys.argv)>5 else 'source-'+label
assert packet_name.startswith('source-'+label) and pathlib.Path(packet_name).name == packet_name
B = pathlib.Path(sys.argv[6]).resolve() if len(sys.argv)>6 else D/('qualified-' + packet_name)
assert B.is_relative_to(D)  # own route; immutable schema references remain wave8
raw_packet = B.with_name(B.name.removeprefix('qualified-'))
e = m.read(B/'candidate.json')['entries'][0]
q = m.read(m.C/'src/content/topics/cars-road-transport.json')['questions'][order-1]
assert q == e['proposedCard'] and m.sha(q) == e['afterHash']
qa_path = pathlib.Path(sys.argv[7]).resolve() if len(sys.argv)>7 else D/('qa-qualified-' + packet_name + '.json')
assert qa_path.is_relative_to(D)
qa = m.read(qa_path)
assert qa['success'] and qa['numPassedTests'] == 19
assert qa['numFailedTests'] == qa['numPendingTests'] == 0
qa_commit = m.savecode([qa_path], 'Preserve exact '+label+' affected content QA19 PASS')
x = m.read(D/'manifest.json')
cp = m.read(m.P/'openspec/changes/question-quality-future-waves/current-checkpoint.json')
assert cp['owner'] == m.O and len(cp['currentEligibleCompletedIds']) == x['CURRENT']
t = m.read(x['readerInitialTaskTemplate'])
t.update(topicId='cars-road-transport', owner=m.O, manifest=str(D/'manifest.json'),
         binderSchemaReference=str(D/'bind-current-receipt.py'), role='independent reviewer one exact INITIAL '+label,
         phase='START_INITIAL_'+label.upper(), id=q['id'], sourceOrder=order,
         catalogCommit=catalog_commit, cardHash=m.sha(q),
         sourceFreeze=qualified_freeze, rawAuthorFreeze=raw_freeze,
         authorNativeId=m.read(B/'candidate.json')['sourceNativeId'],
         authorPacket=str(B), immutableRawAuthorPacket=str(raw_packet),
         applyReport=str(D/('qualified-'+packet_name+'-apply.json')),
         qa=str(qa_path), qaSHA256=m.raw(qa_path), qaReportCommit=qa_commit,
         outputDirectory=str(D/('independent-'+label+'-initial')),
         frozen={'id':q['id'], 'topicId':'cars-road-transport', 'sourceOrder':order,
                 'difficulty':q['difficulty'], 'correctIndex':q['correctIndex']},
         focus='Personally assess whole exact CURRENT: six literal canonical groups, four full prompt/answer/note variants; every claim/option/note grounded in personally read complete immutable primary contexts. Unique key, grammar, absolute adult '+q['difficulty'].upper()+', correct-note extra own fact. Read actual relevant full peers and bilateral entity/relation/value/context/direct reverse. No inherited author judgment or lexical-only duplicate verdict.',
         currentContext='CURRENT'+str(x['CURRENT'])+'/2000 remaining'+str(x['remaining'])+'. Exact applied '+label+' QA19PASS. All prior HOLDs and exhausted attempts preserved. Catalog frozen until verdict; no third full revision.',
         contextPreflight='Verify own native session_meta and actual compacted events; never use coordinator env identity. Reviewer '+x['actors']['reviewer']['threadId']+'. First actual compaction finish this card only; second preservationSTOP. Compact task only, no whole checkpoint/history/catalog dump.',
         history='No independent INITIAL for this ID exists. SOURCE READY/QA19 do not grant credit. Only this exact applied CURRENT is assigned.')
task_path = D/('reader-'+label+'-initial-task.json')
m.write(task_path, t)
x['actors']['reviewer'].update(stage='START_INITIAL_'+label.upper(), task=str(task_path),
                              expected='One exact INITIAL '+label+'; assess specific blocker at30min')
x['retainedIdleReviewer']=None
x['noRetainedIdleReviewer']=True
x['currentWork']={'id':q['id'], 'topicId':'cars-road-transport', 'sourceOrder':order,
                  'stage':'START_INITIAL_'+label.upper(), 'sourceFreeze':qualified_freeze,
                  'rawAuthorFreeze':raw_freeze, 'catalogCommit':catalog_commit,
                  'qaReportCommit':qa_commit, 'qaPath':str(qa_path), 'cardHash':m.sha(q)}
x['next']='Independent INITIAL '+label+' then deterministic binding or sole directed cycle1'
m.write(D/'manifest.json', x)
print({'task':str(task_path), 'qaCommit':qa_commit,
       'taskCommit':m.savecode([task_path,D/'manifest.json',pathlib.Path(__file__)],
                              'Prepare independent INITIAL '+label+' exact metadata')})
