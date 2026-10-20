"""Refresh existing active projections under a pre-write planning lease."""
import pathlib, importlib.util, datetime
D = pathlib.Path(__file__).parent
s = importlib.util.spec_from_file_location('owned', D / 'owned-tools.py')
m = importlib.util.module_from_spec(s)
s.loader.exec_module(m)
x = m.read(D / 'manifest.json')
assert x['owner'] == m.O
author = x['actors']['parks33Author']
reviewer = x['actors']['reviewer']
authors = [author] if author['stage'].startswith('START') else []
readers = [reviewer] if reviewer['stage'].startswith('START') else []
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
                  currentIndependentActors=readers, nativeActorsCurrent=[author, reviewer])
        m.write(cp_path, cp)
        sp = m.P / 'evidence/question-revision-process-v2/coordinator-state.json'
        st = m.read(sp)
        st.update(activeAuthors=authors, idleAuthors=[] if authors else [author],
                  activeIndependentReview=reviewer if readers else None,
                  currentNativeActors={'SOURCE': author, 'OTHER': reviewer},
                  nativeActorsCurrent=[author, reviewer], currentWork=x['currentWork'],
                  codeCommit=m.h.git(m.C, 'rev-parse', 'HEAD'), next=x['next'],
                  asOf=datetime.datetime.now(datetime.timezone.utc).isoformat())
        m.write(sp, st)
        files = [cp_path, sp]
        if x.get('remotePush'):
            rp = x['remotePush']
            record = {
                'branch': rp['branch'], 'commit': rp['sha'], 'remote': 'origin',
                'readbackVerified': rp['readbackVerified'], 'mainIntegrated': False}
            current = m.flow.get('question-quality-future-waves')[1]['evidence'].get('remote_push')
            if current != record:
                m.flow.evidence('question-quality-future-waves', 'remote_push', record)
                files.append(m.P / 'openspec/changes/question-quality-future-waves/delivery.json')
        print(m.h.save(m.P, 'refs/heads/codex/question-revision-resume-20261014',
                       [str(p.relative_to(m.P)) for p in files],
                       'Synchronize active exact2000 stage and existing evidence',
                       '468c6c6118c135884e32bdfbe9240235b72990dfc8c90b1b6e86def6cfc7f9d6'))
finally:
    with m.flow.locked():
        m.flow.lease('release', 'planning', m.O)
