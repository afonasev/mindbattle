"""Lossless mechanical intake of the two preserved SOURCE packets; no quality credit."""
import pathlib, json, hashlib, importlib.util, subprocess, sys
D = pathlib.Path(__file__).parent
spec = importlib.util.spec_from_file_location('owned', D/'owned-tools.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
C, P = m.C, m.P
OLD = D.parent/'coordinator-01a152aa'
spec = importlib.util.spec_from_file_location('apply_standard', C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py')
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a); a.P = P

def groups(q):
    return {'prompt_ordered_answers_key': {'prompt':q['prompt'], 'answers':[v['text'] for v in q['answers']], 'correctIndex':q['correctIndex']}, 'explanation':q['explanation'], **{'note'+str(k):v['note'] for k,v in enumerate(q['answers'])}}

reports = []
packet_paths = [pathlib.Path(p).resolve() for p in sys.argv[1:]] if len(sys.argv)>1 else [OLD/n for n in ['source-polar41-cycle1-fresh', 'source-parks31-complete']]
for R in packet_paths:
    name = R.name; B = D/('qualified-'+name)
    candidate, sp, ps = [m.read(R/n) for n in ['candidate.json','sourceproof.json','peer-snapshot.json']]
    e = candidate['entries'][0]; topic = m.read(C/f"src/content/topics/{e['topicId']}.json")
    assert topic['questions'][e['sourceOrder']-1] == e['beforeCard']
    assert m.sha(e['beforeCard']) == e['beforeHash'] and m.sha(e['proposedCard']) == e['afterHash']
    before, after = groups(e['beforeCard']), groups(e['proposedCard'])
    for g in sp['entries'][0]['literalGroups']:
        assert g['literal'] == after[g['group']] and m.sha(g['literal']) == g['literalSHA256']
    if isinstance(e['fieldGroups'],dict):
        for k, fg in e['fieldGroups'].items():
            assert fg['beforeCanonicalSHA256'] == m.sha(before[k]) and fg['afterCanonicalSHA256'] == m.sha(after[k])
    else:
        assert isinstance(e['fieldGroups'],list)
        if all(isinstance(g,str) for g in e['fieldGroups']):
            assert set(e['fieldGroups']) == {k for k in after if before[k] != after[k]}
        else:
            assert len(e['fieldGroups']) == 6 and {g['group'] for g in e['fieldGroups']} == set(after)
            if all('before' in g and 'after' in g for g in e['fieldGroups']):
                for g in e['fieldGroups']:
                    k=g['group']
                    assert g['before'] == before[k] and g['after'] == after[k]
                    assert g['beforeCanonicalSHA256'] == m.sha(before[k]) and g['afterCanonicalSHA256'] == m.sha(after[k])
                e['originalFieldGroups'] = e['fieldGroups']
                e['fieldGroups'] = {g['group']:{k:g[k] for k in ['beforeCanonicalSHA256','afterCanonicalSHA256']} for g in e['originalFieldGroups']}
            else:
                for g in e['fieldGroups']:
                    assert g['literal'] == after[g['group']] and g['literalSHA256'] == m.sha(g['literal'])
    global_audit = ps.get('globalMAIN', ps.get('global11000MainAudit'))
    inventory = global_audit.get('allCurrentFileByteBindings', global_audit.get('fileManifest',global_audit.get('files')))
    assert len(inventory) == 110
    rows, catalog = [], {}
    for f in inventory:
        path = C/f['path']; digest = next(f[k] for k in ['fileSha256','fileSHA256','rawSHA256','sha256'] if k in f)
        assert m.raw(path) == digest
        t = m.read(path)
        for q in t['questions']:
            catalog[q['id']] = (t['id'], q)
            rows.append({'topicId':t['id'],'id':q['id'],'prompt':q['prompt'],'answers':[v['text'] for v in q['answers']],'correctIndex':q['correctIndex']})
    assert len(rows) == 11000 and m.sha(rows) == global_audit.get('rowsCanonicalSHA256',global_audit.get('projectionCanonicalSHA256'))
    actual = {}
    if 'actualCurrentPeers' in ps:
        snapshots = ps['actualCurrentPeers'] + ps.get('sameTopicClosestFullBodies',[]) + ps.get('crossCatalogClosestFullBodies',[])
    else:
        saved = ps['sameTopicMAIN']['questions']
        assert [p.get('card',p) for p in saved] == topic['questions']
        snapshots = [{'id':p.get('card',p)['id'],'topicId':topic['id'],'card':p.get('card',p),'sha256':m.sha(p.get('card',p))} for p in saved] + ps['fullClosestCurrentPeers']
    for peer in snapshots:
        q = peer['card']; digest = peer.get('sha256',peer.get('canonicalSHA256'))
        pid = peer.get('id',q['id'])
        assert catalog[pid] == (peer['topicId'], q) and m.sha(q) == digest
        actual[pid] = {**peer, 'id':pid, 'sha256':digest}
    paths = {}
    for source in sp['rawSources']:
        original = dict(source); p = C/source['path']; digest = source.get('sha256',source.get('fileSHA256',m.raw(p)))
        assert m.raw(p) == digest
        if source.get('completeOutputPointer'):
            body = m.read(p)
            for key in source['completeOutputPointer'].split('/')[1:]:
                body = body[int(key)] if isinstance(body,list) else body[key]
            assert hashlib.sha256(body.encode()).hexdigest() == source['completeOutputSHA256']
        rel = str(p.relative_to(C)); paths[source['path']] = rel
        source.update(path=rel, sha256=digest, originalSourceBinding=original)
    def source_aliases(v):
        if isinstance(v,dict):
            for k, x in v.items():
                if k == 'sourcePaths': v[k] = [paths.get(p,p) for p in x]
                else: source_aliases(x)
        elif isinstance(v,list):
            for x in v: source_aliases(x)
    source_aliases(sp)
    if 'fullOriginalToolOutputs' in sp:
        sp['immutableFullOriginalToolOutputs'] = {'path':str((R/'sourceproof.json').relative_to(C)), 'sha256':m.raw(R/'sourceproof.json'), 'jsonPointer':'/fullOriginalToolOutputs'}
        del sp['fullOriginalToolOutputs']
    ps['actualCurrentPeers'] = list(actual.values())
    sp['mechanicalIntake'] = {'rawPacket':str(R.relative_to(C)), 'rawSHA256':m.raw(R/'sourceproof.json'), 'operation':'Path/hash aliases and immutable raw pointers only; no literal or editorial judgment changed.'}
    B.mkdir(exist_ok=True)
    for n, value in [('candidate.json',candidate),('sourceproof.json',sp),('peer-snapshot.json',ps)]: m.write(B/n,value)
    report = a.apply(B,candidate['sourceNativeId'],[e['sourceOrder']],D/(name+'-apply.json'),D/'qa-content.json',pathlib.Path(__file__),qualifyOnly=True,peerSnapshot={'actualCurrentPeers':[p for p in actual.values() if p['topicId']==topic['id']]})
    report.update(rawPacket=str(R.relative_to(C)),cycle=candidate['cycle'],globalMAIN=m.sha(rows),status='MECHANICAL_INTAKE_PASS_PENDING_INDEPENDENT_REVIEW',qualityCredit=0)
    m.write(D/(name+'-intake.json'),report); reports.append({'id':e['id'],'afterHash':e['afterHash'],'status':report['status']})
files = [pathlib.Path(__file__),D/'method-pilot.md'] + list(D.glob('*-intake.json')) + [p for p in D.glob('qualified-*/*.json')]
print(json.dumps({'commit':m.savecode(files,'Mechanically qualify SOURCE packet without new editorial review'),'packets':reports},ensure_ascii=False))
