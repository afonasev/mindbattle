"""Refresh existing active projections under a pre-write planning lease."""
import pathlib, importlib.util, datetime
D = pathlib.Path(__file__).parent
s = importlib.util.spec_from_file_location('owned', D / 'owned-tools.py')
m = importlib.util.module_from_spec(s)
s.loader.exec_module(m)
x = m.read(D / 'manifest.json')
assert x['owner'] == m.O
source_actors = [x['actors'][k] for k in x.get('sourceActorKeys', ['parks33Author'])]
reviewer = x['actors']['reviewer']
current_actors = [a for a in source_actors+[reviewer] if not a['stage'].startswith(('ARCHIVED', 'RETIRED'))]
authors = [a for a in source_actors if a['stage'].startswith('START')]
readers = [reviewer] if reviewer['stage'].startswith('START') else []
idle_authors = [a for a in source_actors if not a['stage'].startswith(('START', 'ARCHIVED', 'RETIRED'))]
assert len(authors) <= 2 and len(readers) <= 1
with m.flow.locked():
    m.flow.lease('acquire', 'planning', m.O)
try:
    with m.flow.locked():
        assert all(m.flow.get(cid)[1]['owner'] == m.O for cid in x['claims'])
        cp_path = m.P / 'openspec/changes/question-quality-future-waves/current-checkpoint.json'
        cp = m.read(cp_path)
        assert cp['owner'] == m.O
        assert len(cp['currentEligibleCompletedIds']) == x['CURRENT']
        assert len(cp['currentRemainingIds']) == x['remaining']
        cp.update(currentSourceActors=authors, currentSourceActiveCount=len(authors),
                  currentIndependentActors=readers, nativeActorsCurrent=current_actors)
        m.write(cp_path, cp)
        sp = m.P / 'evidence/question-revision-process-v2/coordinator-state.json'
        st = m.read(sp)
        st.update(activeAuthors=authors, idleAuthors=idle_authors,
                  activeIndependentReview=reviewer if readers else None,
                  currentNativeActors={a['threadId']: a for a in current_actors},
                  nativeActorsCurrent=current_actors, currentWork=x['currentWork'],
                  codeCommit=m.h.git(m.C, 'rev-parse', 'HEAD'), next=x['next'],
                  asOf=datetime.datetime.now(datetime.timezone.utc).isoformat())
        m.write(sp, st)
        files = [cp_path, sp]
        # remote_push is authoritative in delivery.json; stage sync never rewrites it.
        print(m.h.save(m.P, 'refs/heads/codex/question-revision-resume-20261014',
                       [str(p.relative_to(m.P)) for p in files],
                       'Synchronize active exact2000 stage and existing evidence',
                       '468c6c6118c135884e32bdfbe9240235b72990dfc8c90b1b6e86def6cfc7f9d6'))
finally:
    with m.flow.locked():
        m.flow.lease('release', 'planning', m.O)
