"""Prepare one untouched assigned ID; never launch or assess content automatically."""
import pathlib, importlib.util, sys
D = pathlib.Path(__file__).parent
s = importlib.util.spec_from_file_location('owned', D / 'owned-tools.py')
m = importlib.util.module_from_spec(s)
s.loader.exec_module(m)
order = int(sys.argv[1])
q = m.read(m.C / 'src/content/topics/national-parks-nature.json')['questions'][order - 1]
x = m.read(D / 'manifest.json')
cp = m.read(m.P / 'openspec/changes/question-quality-future-waves/current-checkpoint.json')
assert q['id'] not in cp['currentEligibleCompletedIds']
assert f'parks{order}' not in x['held']
out = D / f'source-parks{order}-task.json'
assert not out.exists(), 'Never overwrite a previous assignment/reset its attempt history'
t = m.read(D / 'source-parks37-task.json')
t.update(phase=f'START_SOURCE{order}', id=q['id'], sourceOrder=order,
         difficulty=q['difficulty'], correctIndex=q['correctIndex'], beforeHash=m.sha(q),
         baselineCode=m.h.git(m.C, 'rev-parse', 'HEAD'),
         outputDirectory=str(D / f'source-parks{order}'),
         scope=f'One untouched SOURCE{order}; preserve exact frozen ID/topic/order/level/key. '
               'Preserve good text; repair only genuine source/language/absolutelevel/MAIN defects. '
               'Necessary fulltext solution within protected-territories topic is authorized. '
               'No invented bans: common name roots in prompt/key are not automatically defects.',
         limits=f'Only new owned SOURCE output/raw. No catalog/planning/Git/index/tests/runtime/'
                f'messages/newchats/claims. After{order} END; no adjacent work. '
                'First actualcompaction finish begun card only; second preservationSTOP.',
         currentContext=f"CURRENT{x['CURRENT']}/2000 remaining{x['remaining']}; "
                        'prior HOLD/status/attempt records remain authoritative in manifest. '
                        'Do not reset failed requests or consumed cycles by moving IDs/sessions. '
                        'Read only the relevant compact record when a prior failure is implicated.',
         frozen={'id': q['id'], 'topicId': 'national-parks-nature', 'sourceOrder': order,
                 'difficulty': q['difficulty'], 'correctIndex': q['correctIndex']},
         deliver=f'One READY/HOLD{order}, threeJSON and necessary fullprimary captures; credit0. '
                 'Whole6/four/absolutelevel/actualfreshpeers/source own grounds. '
                 'Use current-inventory.py for machinefacts; personally assess relevant wholepeers. '
                 'No copied stale snapshot, snippetproof or automatic PASS. <=10lines final.')
m.write(out, t)
x['actors']['parks33Author'].update(stage=f'START_SOURCE{order}', task=str(out))
x['currentWork'] = {'id': q['id'], 'stage': f'START_SOURCE{order}'}
x['next'] = f'One SOURCE{order}, then only applicable next stage; no held retries'
m.write(D / 'manifest.json', x)
print(m.savecode([out, D / 'manifest.json', pathlib.Path(__file__)],
                 f'Prepare one untouched SOURCE{order} preserving scope and prior attempts'))
