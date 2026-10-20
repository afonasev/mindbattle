"""Preserve an author HOLD verbatim; no application, independent verdict or credit."""
import pathlib, importlib.util, sys
D = pathlib.Path(__file__).parent
s = importlib.util.spec_from_file_location('owned', D / 'owned-tools.py')
m = importlib.util.module_from_spec(s)
s.loader.exec_module(m)
order = int(sys.argv[1])
packet = D / f'source-parks{order}'
e = m.read(packet / 'candidate.json')['entries'][0]
q = m.read(m.C / 'src/content/topics/national-parks-nature.json')['questions'][order - 1]
assert e['status'] == 'HOLD' and e['beforeCard'] == q
assert e['beforeHash'] == m.sha(q) and e['afterHash'] == m.sha(e['proposedCard'])
cp = m.read(m.P / 'openspec/changes/question-quality-future-waves/current-checkpoint.json')
assert q['id'] not in cp['currentEligibleCompletedIds']
out = D / f'terminal-parks{order}-source-hold.json'
report = {'owner': m.O, 'id': q['id'], 'hash': m.sha(q),
          'status': 'SOURCE_HOLD_UNQUALIFIED_UNAPPLIED_NO_INITIAL', 'qualityCredit': 0,
          'sourcePacket': str(packet), 'proposedHash': e['afterHash'],
          'authorReason': e.get('holdReason', e.get('reason')),
          'catalogUnchanged': True, 'independentINITIAL': False,
          'attempts': 'Preserve exact original sourceproof and captures; no reset via ID or session',
          'QA': 'NotRun: no application'}
m.write(out, report)
x = m.read(D / 'manifest.json')
x['held'][f'parks{order}'] = report
x['actors']['parks33Author']['stage'] = f'IDLE_SOURCE{order}_HOLD_PRESERVED'
x['currentWork'] = report
x['next'] = 'Next untouched SOURCE after context preflight; held evidence and attempts retained'
m.write(D / 'manifest.json', x)
files = [D / 'manifest.json', out, pathlib.Path(__file__)]
files += [p for p in packet.rglob('*') if p.is_file()]
print(m.savecode(files, f'Preserve SOURCE{order} HOLD unapplied without independent credit'))
