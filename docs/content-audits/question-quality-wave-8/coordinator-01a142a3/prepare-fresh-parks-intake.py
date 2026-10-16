"""Pin current live before images for fresh SOURCE; no catalog mutation."""
import pathlib
import importlib.util
D = pathlib.Path(__file__).parent.resolve()
s = importlib.util.spec_from_file_location('own', D / 'owned-tools.py')
m = importlib.util.module_from_spec(s)
s.loader.exec_module(m)
topic = m.read(m.C / 'src/content/topics/national-parks-nature.json')
cards = [
 {'sourceOrder': i + 1, 'id': q['id'], 'card': q, 'sha256': m.sha(q)}
 for i, q in enumerate(topic['questions'])
 if 6 <= i + 1 <= 15
]
assert len(cards) == 10
intake = D / 'parks6-15-fresh-actual-intake.json'
m.write(intake, {
 'topicId': 'national-parks-nature', 'CURRENT': 832, 'cards': cards,
 'catalogCommit': '4db6a0f4cf9f1048dfce8b6344e1913173bc6cf2',
 'stageByOrder': {str(n): ('FINAL after one SOURCE fix-cycle1' if n <= 8 else 'INITIAL') for n in range(6, 16)},
 'canonicalINITIALAudit': str((D / 'parks6-15-canonical-intake.json').relative_to(m.C)),
 'sourceBeforeImages': 'Use actual intake/live C; old initial6-8 border park questions are historical.'
})
task = D / 'source-parks6-15-fresh-task.json'
t = m.read(task)
t['intake'] = str(intake)
t['actor'] = '01a142d8-32ad-7621-83d1-4865c76c51f5'
m.write(task, t)
print(m.savecode([intake, task, pathlib.Path(__file__)], 'Pin fresh SOURCE parks6-15 actual country before images and native ID'))
