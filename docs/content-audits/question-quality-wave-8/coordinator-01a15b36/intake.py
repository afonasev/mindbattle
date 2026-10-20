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
        if g['group'] == 'prompt_ordered_answers_key' and isinstance(g['literal'], str):
            # Lossless shape alias only: candidate already binds the entire
            # ordered group, and all four personal assessments bind its strings.
            assert g['literal'] == e['proposedCard']['prompt']
            assert m.sha(g['literal']) == g['literalSHA256']
            variants = sp['entries'][0]['fourFullPromptAnswerNoteAssessments']
            assert len(variants) == 4 and {v['slot'] for v in variants} == set(range(4))
            for v in variants:
                answer = e['proposedCard']['answers'][v['slot']]
                assert v['fullPrompt'] == g['literal'] and v['answer'] == answer['text']
                assert v['note'] == answer['note']
            assert e['fieldGroups']['prompt_ordered_answers_key']['afterCanonicalSHA256'] == m.sha(after[g['group']])
            g['originalPromptOnlyLiteral'] = g['literal']
            g['originalPromptOnlyLiteralSHA256'] = g['literalSHA256']
            g['literal'] = after[g['group']]
            g['literalSHA256'] = m.sha(g['literal'])
            g['technicalShapeAlias'] = 'Same author candidate group and four bound full triples; no text or primaryGround changed.'
        assert g['literal'] == after[g['group']]
        if m.sha(g['literal']) != g['literalSHA256']:
            assert isinstance(g['literal'],str)
            assert g['literalSHA256'] == hashlib.sha256(g['literal'].encode('utf-8')).hexdigest()
            g['originalLiteralRawUTF8SHA256'] = g['literalSHA256']
            g['literalSHA256'] = m.sha(g['literal'])
            g['technicalLiteralHashAlias'] = 'Identical author literal, raw UTF8 hash normalized to canonical JSON string hash.'
        assert m.sha(g['literal']) == g['literalSHA256']
    if isinstance(e['fieldGroups'],dict):
        for k, fg in e['fieldGroups'].items():
            for phase, literal in [('before', before[k]), ('after', after[k])]:
                key = phase+'CanonicalSHA256'
                if fg[key] != m.sha(literal):
                    assert isinstance(literal, str)
                    assert fg[key] == hashlib.sha256(literal.encode('utf-8')).hexdigest()
                    fg['original'+phase.title()+'RawUTF8SHA256'] = fg[key]
                    fg[key] = m.sha(literal)
                    fg['technicalHashRepresentationAlias'] = 'Exact identical author string; raw UTF8 and canonical JSON string hashes distinguished.'
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
    if global_audit is None and isinstance(ps.get('retrieval'), dict):
        retained = ps['retrieval']
        assert retained['topicFileCount'] == 110 and retained['questionCount'] == 11000
        assert len(retained['globalRows']) == 11000
        assert m.sha(retained['globalRows']) == retained.get('globalRowsCanonicalSHA256', retained.get('rowsCanonicalSHA256'))
        global_audit = ps['globalMAIN'] = {
            'topicFileCount': retained['topicFileCount'],
            'questionCount': retained['questionCount'],
            'rows': retained['globalRows'],
            'rowsCanonicalSHA256': retained.get('globalRowsCanonicalSHA256', retained.get('rowsCanonicalSHA256')),
            'allCurrentFileByteBindings': retained['allCurrentFileByteBindings']}
        ps['sameTopicMAIN'] = retained['sameTopicMAIN']
        ps['technicalRetrievalShapeAlias'] = 'Exact original retrieval rows/file bindings/topic bodies; no new facts or peer judgments.'
    if global_audit is None and 'inventoryPath' in ps:
        inv_path = C / ps['inventoryPath']
        assert m.raw(inv_path) == ps['inventoryFileSHA256']
        retained = m.read(inv_path)
        assert ps.get('currentMainRows', retained['globalMAIN']['questionCount']) == retained['globalMAIN']['questionCount'] == 11000
        assert ps.get('sameTopicCurrentCards', retained['sameTopicMAIN']['questionCount']) == retained['sameTopicMAIN']['questionCount'] == 100
        ps['globalMAIN'] = global_audit = retained['globalMAIN']
        ps['sameTopicMAIN'] = retained['sameTopicMAIN']
        ps['technicalInventoryReferenceHydration'] = {'path':ps['inventoryPath'], 'sha256':ps['inventoryFileSHA256'], 'operation':'Exact author-retained inventory only; no new peer judgment.'}
    # Lossless hydration from the author's immutable, SHA-bound fresh inventory.
    if 'sourceInventoryPath' in global_audit:
        inventory_path = pathlib.Path(global_audit['sourceInventoryPath'])
        assert m.raw(inventory_path) == global_audit['sourceInventorySHA256']
        saved_inventory = m.read(inventory_path)
        full_global = saved_inventory['globalMAIN']
        assert full_global['rowsCanonicalSHA256'] == global_audit['rowsCanonicalSHA256']
        assert full_global['topicFileCount'] == global_audit['topicFileCount'] == 110
        assert full_global['questionCount'] == global_audit['questionCount'] == 11000
        global_audit['originalInventoryReference'] = dict(global_audit)
        global_audit['allCurrentFileByteBindings'] = full_global['allCurrentFileByteBindings']
        same_topic = ps['sameTopicMAIN']
        assert same_topic['sourceInventoryPath'] == str(inventory_path)
        assert same_topic['sourceInventorySHA256'] == m.raw(inventory_path)
        assert saved_inventory['sameTopicMAIN']['questions'] == topic['questions']
        same_topic['questions'] = saved_inventory['sameTopicMAIN']['questions']
        same_topic['technicalHydration'] = 'Exact original saved100 bodies from SHA-bound author inventory; no new assessment.'
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
    if isinstance(ps.get('actualCurrentPeers'), int):
        # This raw field is an inventory count, not a list of assessed peers.
        # Preserve the count and use only the author's explicit full relevant
        # peer bodies. Do not invent 100 peer assessments or hydrate an unbound path.
        assert ps['actualCurrentPeers'] == len(topic['questions']) == 100
        assert isinstance(ps.get('fullRelevantSameTopicPeers'), list) and ps['fullRelevantSameTopicPeers']
        ps['originalActualCurrentPeerInventoryCount'] = ps['actualCurrentPeers']
        ps['actualCurrentPeers'] = ps['fullRelevantSameTopicPeers']
        ps['technicalPeerContainerAlias'] = 'Explicit fullRelevantSameTopicPeers retained verbatim; inventory count is not substantive peer credit. Original full100 topic inventory remains at immutable raw inventoryPath.'
    if 'actualCurrentPeers' in ps:
        snapshots = ps['actualCurrentPeers'] + ps.get('sameTopicClosestFullBodies',[]) + ps.get('crossCatalogClosestFullBodies',[])
    else:
        saved = ps['sameTopicMAIN']['questions']
        assert [p.get('card',p) for p in saved] == topic['questions']
        snapshots = [{'id':p.get('card',p)['id'],'topicId':topic['id'],'card':p.get('card',p),'sha256':m.sha(p.get('card',p))} for p in saved] + ps['fullClosestCurrentPeers']
    for peer in snapshots:
        q = peer['card']; digest = peer.get('sha256',peer.get('canonicalSHA256'))
        pid = peer.get('id',q['id'])
        if pid == e['id'] and q == e['proposedCard'] and digest == e['beforeHash'] and q != e['beforeCard']:
            # Proven self-reference alias: immutable candidate supplies both exact
            # bodies, while the peer hash and live catalog bind the before body.
            # Do not alter any distinct peer or the original author packet.
            assert peer['topicId'] == e['topicId'] and catalog[pid] == (e['topicId'], e['beforeCard'])
            peer['originalSelfProposedBody'] = q
            peer['technicalSelfPreimageAlias'] = 'Original own proposal body paired with exact beforeHash; normalize self to candidate beforeCard and live CURRENT. Self is not a distinct peer.'
            peer['card'] = q = e['beforeCard']
        assert catalog[pid] == (peer['topicId'], q) and m.sha(q) == digest
        actual[pid] = {**peer, 'id':pid, 'sha256':digest}
    paths = {}; verified_pointer_bodies = set()
    for source in sp['rawSources']:
        original = dict(source); p = C/source['path']; digest = source.get('sha256',source.get('fileSHA256',m.raw(p)))
        assert m.raw(p) == digest
        if p.suffix == '.json' and 'completeOutputPointer' not in source:
            capture = m.read(p)
            hits = []
            def find_body(value, pointer=''):
                if isinstance(value,dict):
                    for key, child in value.items():
                        find_body(child,pointer+'/'+key.replace('~','~0').replace('/','~1'))
                elif isinstance(value,list):
                    for key, child in enumerate(value):find_body(child,pointer+'/'+str(key))
                elif isinstance(value,str) and 'Source: open(' in value and source['url'] in value:
                    hits.append((pointer,value))
            find_body(capture)
            assert len(hits) == 1, ('AMBIGUOUS_FULL_SOURCE_BODY', str(p), len(hits))
            pointer, body = hits[0]
            source['completeOutputPointer'] = pointer
            source['completeOutputSHA256'] = hashlib.sha256(body.encode('utf-8')).hexdigest()
            source['technicalCompleteOutputBinding'] = 'Unique already-retained full original tool body; empty JSON Pointer means the root JSON string.'
        if p.suffix != '.json' and source.get('completeOutputPointer') == '/file/full captured page text':
            assert source['completeOutputSHA256'] == m.raw(p)
            source['originalTextFileLocator'] = source.pop('completeOutputPointer')
            source['technicalTextFileBinding'] = 'Exact whole UTF8 file; descriptive file locator is not a JSON Pointer. Original declaration retained.'
        if 'completeOutputPointer' in source:
            capture = m.read(p)
            if isinstance(capture,dict) and 'originalRecord' in capture and source['completeOutputPointer'].startswith('/payload/'):
                # Capture helper pointer is relative to retained native record.
                # Verify exact native lineage before adding its wrapper prefix.
                native_path = pathlib.Path(capture['nativeJournal'])
                if not native_path.exists():
                    matches = list(pathlib.Path('/Users/eaafonasev/.codex/archived_sessions').glob('*'+capture['sourceNativeId']+'.jsonl'))
                    assert len(matches) == 1
                    native_path = matches[0]
                native_record = json.loads(native_path.read_text().splitlines()[capture['nativeRecordLine']-1])
                assert native_record == capture['originalRecord']
                assert capture['sourceNativeId'] == candidate['sourceNativeId']
                source['originalNativeRecordRelativePointer'] = source['completeOutputPointer']
                source['completeOutputPointer'] = '/originalRecord'+source['completeOutputPointer']
                source['technicalCaptureWrapperPointerAlias'] = 'Exact retained originalRecord verified against actual native journal line; prefix only, raw unchanged.'
            body = m.read(p)
            for key in source['completeOutputPointer'].split('/')[1:]:
                body = body[int(key)] if isinstance(body,list) else body[key]
            actual_body = hashlib.sha256(body.encode()).hexdigest()
            declared = source['completeOutputSHA256']; canonical_string = m.sha(body)
            pointer_key = (str(p),source['completeOutputPointer'])
            if declared not in (actual_body, canonical_string) and isinstance(capture,dict) and 'originalRecord' in capture:
                # Reused SOURCE71 captures carry authoritative body hashes in
                # their immutable wrappers. Prove native equality before a
                # lossless alias of a separately mistyped packet declaration.
                assert capture['completeOutputPointer'] == source['completeOutputPointer']
                assert capture['completeOutputSHA256'] == actual_body and source['url'] in body
                native_path = pathlib.Path(capture['nativeJournal'])
                if not native_path.exists():
                    matches = list(pathlib.Path('/Users/eaafonasev/.codex/archived_sessions').glob('*'+capture['sourceNativeId']+'.jsonl'))
                    assert len(matches) == 1
                    native_path = matches[0]
                native_record = json.loads(native_path.read_text().splitlines()[capture['nativeRecordLine']-1])
                assert native_record == capture['originalRecord']
                source['originalDeclaredCompleteOutputSHA256'] = declared
                source['technicalNativeVerifiedCaptureHashAlias'] = {'nativeId':capture['sourceNativeId'], 'nativeRecordLine':capture['nativeRecordLine'], 'originalRecordByteEqual':True, 'captureBodySHA256':actual_body}
                source['completeOutputSHA256'] = actual_body
                declared = actual_body
            if declared != actual_body:
                if declared != canonical_string:
                    # Only a proven one-character omission of the already verified
                    # identical capture/pointer is repairable as a copied hash typo.
                    assert pointer_key in verified_pointer_bodies and source['url'] in body
                    assert len(declared)+1 == len(canonical_string)
                    assert any(canonical_string[:i]+canonical_string[i+1:] == declared for i in range(len(canonical_string)))
                    source['copiedHashOmissionProvenAgainstIdenticalVerifiedCapture'] = True
                source['originalDeclaredCompleteOutputSHA256'] = declared
                source['canonicalJSONStringSHA256'] = canonical_string
                source['completeOutputSHA256'] = actual_body
                source['captureHashRepresentationNormalization'] = 'Original unchanged body verified at immutable file/pointer. Raw UTF8 payload and canonical JSON string hashes are distinct; original declaration retained.'
            verified_pointer_bodies.add(pointer_key)
        rel = str(p.relative_to(C)); paths[source['path']] = rel
        paths[str(p)] = paths[rel] = rel
        if source.get('completeOutputPointer'):
            for base in [source['path'],str(p),rel]:
                paths[base+'#'+source['completeOutputPointer']] = rel
        source.update(path=rel, sha256=digest, originalSourceBinding=original)
    def source_aliases(v):
        if isinstance(v,dict):
            for k, x in list(v.items()):
                if k == 'sourcePaths':
                    normalized = [paths.get(p,p) for p in x]
                    if normalized != x: v['sourcePathsBeforeTechnicalNormalization'] = x
                    v[k] = normalized
                else: source_aliases(x)
        elif isinstance(v,list):
            for x in v: source_aliases(x)
    source_aliases(sp)
    for v in sp['entries'][0]['fourFullPromptAnswerNoteAssessments']:
        triple = {'prompt':v['fullPrompt'],'answer':v['answer'],'note':v['note']}
        if 'tripleSHA256' in v and v['tripleSHA256'] != m.sha(triple):
            assert v['tripleSHA256'] == m.sha({'slot':v['slot'],**triple})
            v['originalSlotIncludedTripleSHA256'] = v['tripleSHA256']
            v['tripleSHA256'] = m.sha(triple)
            v['technicalTripleShapeAlias'] = 'Same author full prompt/answer/note, redundant numeric slot excluded from canonical triple hash only.'
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
files = [pathlib.Path(__file__)] + list(D.glob('*-intake.json')) + [p for p in D.glob('qualified-*/*.json')]
print(json.dumps({'commit':m.savecode(files,'Mechanically qualify SOURCE packet without new editorial review'),'packets':reports},ensure_ascii=False))
