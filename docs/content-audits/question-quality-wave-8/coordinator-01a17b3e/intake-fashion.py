"""Lossless mechanical intake of the two preserved SOURCE packets; no quality credit."""
import pathlib, json, hashlib, importlib.util, subprocess, sys, re
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
assert len(sys.argv)>1, "Explicit new route packet required; no inherited fallback"
for R in packet_paths:
    assert R.parent==D and R.name.startswith("source-fashion"), "Only owned fashion packet"
    name = R.name; B = D/('qualified-'+name)
    candidate, sp, ps = [m.read(R/n) for n in ['candidate.json','sourceproof.json','peer-snapshot.json']]
    m.alias_source80_cycle1_single_peer_entry(candidate,sp,ps,R)
    m.alias_source26_cycle1_canonical_readiness(candidate,sp,ps,R)
    m.alias_source23_cycle1_self_preimage(candidate,sp,ps,R)
    m.alias_source22_peer_header(candidate,sp,ps,R)
    m.alias_source9_global_field_names(candidate,sp,ps,R)
    m.alias_source86_single_peer_entry(candidate,sp,ps,R)
    m.alias_source83_cycle1_copied_same_topic(candidate,sp,ps,R)
    m.alias_source78_concurrent74_snapshot(candidate,sp,ps,R)
    m.alias_source74_cycle1_own_global_metadata(candidate,sp,ps,R)
    if R.name=='source-video-game-history70' and (R/'concurrent66-addendum.json').exists():
        clar=m.read(R/'concurrent66-addendum.json');cor=m.read(R/'concurrent66-identity-correction.json')
        uid=candidate['sourceNativeId'];assert uid==sp['sourceNativeId']==ps['sourceNativeId']==m.read(D/'manifest.json')['actors']['author68']['threadId']
        assert cor['actualSourceNativeId']==cor['correctedId']==uid and cor['wrongDeclaredId']==clar['sourceNativeId']
        original_ref=cor['originalAddendum'];assert original_ref['path']==str(R/'concurrent66-addendum.json') and original_ref['rawSHA256']==m.raw(R/'concurrent66-addendum.json')
        assert clar['cycle']==candidate['cycle']==sp['cycle']==ps['cycle']==0 and clar['targetOrder']==70 and clar['changedOrder']==66
        proof=m.read(D/'video-game-history70-native-proof.json');baseline=proof['preservedCatalogBaseline'];tp=C/'src/content/topics/video-game-history.json'
        old_bytes=subprocess.check_output(['git','-C',str(C),'show',baseline+':'+str(tp.relative_to(C))]);old=json.loads(old_bytes);live=m.read(tp)
        assert [i for i,(a,b) in enumerate(zip(old['questions'],live['questions']),1) if a!=b]==[66]
        assert [v['card'] for v in ps['actualCurrentPeers']]==old['questions'] and all(m.sha(v['card'])==v['sha256'] for v in ps['actualCurrentPeers'])
        for fn,digest in clar['originalCriticalSHA256'].items():
            assert m.raw(R/fn)==digest==clar['originalCriticalSHA256After'][fn]==proof['rawFileSHA256'][fn]
        report=pathlib.Path(clar['knownApplyReport']['path']);assert report==D/'qualified-source-video-game-history66-apply.json' and m.raw(report)==clar['knownApplyReport']['sha256']
        applied=m.read(report)['applied'][0];assert applied['beforeCard']==old['questions'][65] and applied['proposedCard']==live['questions'][65]
        assert clar['exactCurrent66']['body']==live['questions'][65] and clar['exactCurrent66']['hash']==m.sha(live['questions'][65])
        e=candidate['entries'][0];assert clar['unchangedProposed70']['body']==e['proposedCard'] and clar['unchangedProposed70']['hash']==e['afterHash']==m.sha(e['proposedCard'])
        assert len(clar['bilateralMAINComparison'])==2 and all(all(v[k] for k in ['direction','entity','relation','value','context','finding']) for v in clar['bilateralMAINComparison'])
        assert clar['directReverseCheck']['compared'] and clar['directReverseCheck']['result'] and clar['dependencyConclusion']
        ip=pathlib.Path(clar['freshCurrentInventory']['path']);assert ip.parent==R and m.raw(ip)==clar['freshCurrentInventory']['sha256'];inv=m.read(ip)
        assert inv['sameTopicMAIN']['questions']==live['questions'] and inv['sameTopicMAIN']['fileSHA256']==m.raw(tp)
        bindings=ps['globalMAIN']['allCurrentFileByteBindings'];fresh=inv['globalMAIN']['allCurrentFileByteBindings'];assert len(bindings)==len(fresh)==110
        for b,f in zip(bindings,fresh):
            assert b['path']==f['path'] and m.raw(C/f['path'])==f['sha256']
            assert b['sha256']==(hashlib.sha256(old_bytes).hexdigest() if b['path']==str(tp.relative_to(C)) else f['sha256'])
        rows=[]
        for b in bindings:
            t=old if b['path']==str(tp.relative_to(C)) else m.read(C/b['path'])
            rows.extend({'topicId':t['id'],'id':q['id'],'prompt':q['prompt'],'answers':[v['text'] for v in q['answers']],'correctIndex':q['correctIndex']} for q in t['questions'])
        assert len(rows)==11000 and ps['globalMAIN']['rows']==rows and ps['globalMAIN']['rowsCanonicalSHA256']==m.sha(rows)
        ps['historicalGlobalMAINBinding']={'rawPath':str(R/'peer-snapshot.json'),'rawSHA256':m.raw(R/'peer-snapshot.json'),'baseline':baseline}
        ps['globalMAIN']=inv['globalMAIN'];ps['actualCurrentPeers']=inv['actualCurrentPeers'];ps['sameTopicMAIN']=inv['sameTopicMAIN']
        sp['sourceInventoryPath']=str(ip);sp['sourceInventorySHA256']=m.raw(ip)
        binding={'rawPacket':str(R),'rawFreeze':proof['preservedCatalogBaseline'],'originalPacketProof':str(D/'video-game-history70-native-proof.json'),'sameAuthorDependencyAddendum':str(R/'concurrent66-addendum.json'),'addendumSHA256':m.raw(R/'concurrent66-addendum.json'),'identityCorrection':str(R/'concurrent66-identity-correction.json'),'identityCorrectionSHA256':m.raw(R/'concurrent66-identity-correction.json'),'knownAppliedDeltaOnly':66,'originalsUnchanged':True,'noRootSemanticDecision':True,'qualityCredit':0}
        ps['technicalConcurrentDependencyAlias']=binding;sp['technicalConcurrentDependencyAlias']=binding
    if 'allCurrentFileByteBindings' not in ps.get('globalMAIN',{}) and 'currentFileByteBindings' in ps.get('globalMAIN',{}):
        bindings=ps['globalMAIN']['currentFileByteBindings'];assert len(bindings)==110 and all(m.raw(C/v['path'])==v['sha256'] for v in bindings)
        ps['globalMAIN']['allCurrentFileByteBindings']=bindings
        ps['technicalCurrentFileByteBindingNameAlias']={'rawPeer':str(R/'peer-snapshot.json'),'rawSHA256':m.raw(R/'peer-snapshot.json'),'originalPointer':'/globalMAIN/currentFileByteBindings','operation':'Exact110 live file path/hash bindings; redundant container name only, raw and judgments unchanged.'}
    m.assert_retained_source_admissibility(sp)
    m.alias_explicit_global_inventory_file(candidate,sp,ps,R)
    m.alias_explicit_owned_packet_source_paths(candidate,sp,R)
    m.alias_source96_distinct99_preimage(candidate,sp,ps,R)
    m.alias_explicit_fresh_inventory_context(candidate,sp,ps,R)
    m.alias_explicit_inventory_file_digest(candidate,sp,ps,R)
    m.alias_exact_videogame2_distinct_peers(candidate,sp,ps,R)
    m.alias_explicit_inventory_binding(candidate,sp,ps,R)
    m.alias_explicit_complete_inventory_paths(candidate,sp,ps,R)
    m.alias_explicit_cross_topic_peers(candidate,sp,ps,R)
    m.alias_same_topic_current_peer_container(candidate,sp,ps,R)
    m.alias_explicit_root_candidate(candidate,sp,ps,R)
    m.alias_source77_own_prior_application(candidate,sp,ps,R)
    m.alias_source31_root_entry_identity(candidate,sp,R)
    m.alias_source83_clarified_literals(candidate,sp,ps,R)
    m.alias_source83_cycle1_redundant_snapshot(candidate,sp,ps,R)
    m.alias_source84_cycle1_variant_names(candidate,sp,ps,R)
    m.alias_explicit_peer_inventory_projection(candidate,sp,ps,R)
    m.alias_serialized_prompt_group(candidate,sp)
    m.alias_full_prompt_answer_concatenation(candidate,sp)
    m.alias_full_body_wrapper_digests(ps,R)
    m.alias_explicit_nested_inventory(candidate,sp,ps,R)
    e = candidate['entries'][0]; topic = m.read(C/f"src/content/topics/{e['topicId']}.json")
    assert topic['questions'][e['sourceOrder']-1] == e['beforeCard']
    assert m.sha(e['beforeCard']) == e['beforeHash'] and m.sha(e['proposedCard']) == e['afterHash']
    if 'entries' not in sp:
        assert sp['id'] == e['id'] and sp['status'] == e['status']
        assert sp['beforeHash'] == e['beforeHash'] and sp['afterHash'] == e['afterHash']
        keys=['id','status','beforeHash','afterHash','literalGroups','fourFullPromptAnswerNoteAssessments','correctNoteNewFact','absoluteDifficulty','changeRationale']
        assert len(sp['literalGroups']) == 6 and len(sp['fourFullPromptAnswerNoteAssessments']) == 4
        sp['entries']=[{k:sp[k] for k in keys}]
        sp['technicalSingleEntryContainerAlias']='Exact original top-level single-card fields retained and aliased into entries[0]; no literal or assessment changed.'
    if 'literalGroups' not in sp['entries'][0] and 'sixLiteralGroups' in sp['entries'][0]:
        entry=sp['entries'][0]
        assert len(entry['sixLiteralGroups'])==6
        entry['literalGroups']=entry['sixLiteralGroups']
        entry['technicalLiteralGroupContainerAlias']='Same original sixLiteralGroups exact list aliased into literalGroups; original container retained, no literal or ground changed.'
    before, after = groups(e['beforeCard']), groups(e['proposedCard'])
    if e['status'] == 'READY_FOR_SAME_READER_FINAL':
        assert candidate['cycle'] == 1 and R.name.endswith('-cycle1')
        initial = m.read(D/('independent-fashion'+str(e['sourceOrder'])+'-initial/receipt.json'))
        assert initial['entries'][0]['id'] == e['id'] and initial['entries'][0]['status'] == 'FIX'
        e['originalDirectedFinalStatus'] = e['status']
        e['status'] = 'READY_FOR_INDEPENDENT_REVIEW'
    if R.name=='source-history-russia91' and candidate['sourceNativeId']=='01a164f2-bdf7-78b1-a2b1-803a3d34a4f0':
        assert m.raw(R/'sourceproof.json')=='a6000e69e02a40001f14145016e71b1e1867aafc2e19b09101a35b2b2dd7848a'
        g=next(v for v in sp['entries'][0]['literalGroups'] if v['group']=='explanation')
        assert g['sourcePaths']==[] and g['locator']=='' and m.sha(g['literal'])=='4cd6070668cb8c22d3252e88815a5bf97e9b2f68b734a2c573713f90c27e5de6'
        refs=[v for v in sp['rawSources'] if v.get('claimRole')=='MAIN, correct answer and explanation'];assert len(refs)==1
        ref=refs[0];assert ref['url']=='https://www.prlib.ru/node/619247' and ref['sourceOutputLocator']=='turn4view0 L63-L64'
        assert ref['captureReadProvenance']['readThisNativeId']==candidate['sourceNativeId'] and ref['captureReadProvenance']['personallyReadRelevantContext'] is True
        assert ref['captureReadProvenance']['relevantLocator']==ref['sourceOutputLocator'] and 'L64 says it was soon suppressed.' in ref['captureReadProvenance']['claimCoverage']
        assert 'and suppression.' in sp['sourceIndex']['main'] and ref['sourceOutputLocator'] in sp['sourceIndex']['main']
        g['technicalAlreadyDeclaredExplanationSourceAlias']={'rawSHA256':m.raw(R/'sourceproof.json'),'originalSourcePaths':[],'originalLocator':'','bindingPointer':'/rawSources/0/claimRole','locatorPointer':'/rawSources/0/sourceOutputLocator','operation':'Exact already-declared explanation role, personally-read provenance and sourceIndex.main coverage relocated into redundant literal-group reference fields only. Raw/literal/ground/digests unchanged; no new source or judgment.'}
        g['sourcePaths']=[ref['path']];g['locator']=ref['sourceOutputLocator']
    for g in sp['entries'][0]['literalGroups']:
        if g['group'] == 'prompt_ordered_answers_key' and isinstance(g['literal'], str):
            # Lossless shape alias only: candidate already binds the entire
            # ordered group, and all four personal assessments bind its strings.
            assert g['literal'] == e['proposedCard']['prompt']
            assert g['literalSHA256'] in [m.sha(g['literal']),hashlib.sha256(g['literal'].encode()).hexdigest()]
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
    if global_audit is not None and 'freshInventoryPath' in global_audit and 'freshInventoryPath' not in sp and 'sourceInventoryPath' not in sp:
        # Exact explicit peer path+SHA and sourceproof prose locator refer to
        # the same author-retained inventory; no arbitrary path hydration.
        declared=global_audit['freshInventoryPath']
        inv_path=pathlib.Path(declared); inv_path=inv_path if inv_path.is_absolute() else C/inv_path
        explicit_initial_peer_binding = declared not in json.dumps(sp.get('sourceIndex',{}),ensure_ascii=False) and candidate['cycle']==0
        if explicit_initial_peer_binding:
            assert candidate['sourceNativeId']==sp['sourceNativeId']==ps['sourceNativeId']
            assert candidate['cycle']==sp['cycle']==ps['cycle']==0
            assert sp['entries'][0]['id']==e['id']
            assert inv_path.is_relative_to(R) and inv_path.is_file()
            assert m.raw(inv_path)==global_audit['freshInventorySHA256']
            initial_inv=m.read(inv_path)
            assert initial_inv['sameTopicMAIN']['questions']==ps['sameTopicMAIN']['questions']==topic['questions']
            assert initial_inv['sameTopicMAIN']['fileSHA256']==ps['sameTopicMAIN']['fileSHA256']==m.raw(C/ps['sameTopicMAIN']['path'])
            if 'freshInventoryPath' not in ps['sameTopicMAIN']:
                ps['sameTopicMAIN']['freshInventoryPath']=declared
                ps['technicalSameTopicFullBodyInventoryLocatorAlias']={'explicitGlobalPath':declared,'fileSHA256':m.raw(inv_path),'operation':'Same raw author peer already contains all100 exact ordered topic bodies and matching topic file SHA; global explicit inventory has identical100 bodies. Locator alias only, original raw untouched.'}
            assert ps['sameTopicMAIN']['freshInventoryPath']==declared
            assert ps['sameTopicMAIN']['questions']==topic['questions'] and len(topic['questions'])==100
            assert len(global_audit['allCurrentFileByteBindings'])==110
            sp['technicalExplicitInitialPeerInventoryBinding']={'rawPeerSnapshot':str(R/'peer-snapshot.json'),'rawPeerSnapshotSHA256':m.raw(R/'peer-snapshot.json'),'path':declared,'fileSHA256':m.raw(inv_path),'operation':'Exact explicit same-author initial peer inventory path/SHA; all existing live110/11000/100 checks below retained. Acquisition prose unchanged; no unbound hydration or new judgment.'}
        elif declared not in json.dumps(sp.get('sourceIndex',{}),ensure_ascii=False):
            assert candidate['cycle']==1 and R.name.endswith('-cycle1')
            initial_raw=R.with_name(R.name.removesuffix('-cycle1'))
            initial_sp=m.read(initial_raw/'sourceproof.json');initial_candidate=m.read(initial_raw/'candidate.json')
            assert candidate['sourceNativeId']==initial_candidate['sourceNativeId']==initial_sp['sourceNativeId']
            assert e['beforeCard']==initial_candidate['entries'][0]['proposedCard']
            assert sp['sourceIndex']==initial_sp['sourceIndex']
            full=[p for p in ps['actualCurrentPeers'] if p['topicId']==e['topicId']]
            assert len(full)==100 and [p['sourceOrder'] for p in full]==list(range(1,101))
            assert [p['card'] for p in full]==topic['questions']
            assert all(m.sha(p['card'])==p.get('sha256',p.get('canonicalSHA256')) for p in full)
            sp['technicalHistoricalSourceIndexProsePreserved']={'initialRawSourceproof':str((initial_raw/'sourceproof.json').relative_to(C)),'rawSHA256':m.raw(initial_raw/'sourceproof.json'),'meaning':'Original identical acquisition-history prose retained; CURRENT inventory comes from exact explicit cycle1 peer path/SHA, all100 full current author bodies, all110 live file bindings. No unbound hydration or new peer judgment.'}

        if 'freshInventoryPath' not in ps['sameTopicMAIN']:
            # An explicit sourceIndex inventory is already bound by path and SHA.
            # Prove identical full topic bodies before aliasing its redundant name.
            explicit=sp.get('sourceIndex',{}).get('cycle1FreshInventory' if candidate['cycle']==1 else 'freshInventory',{})
            assert inv_path.is_relative_to(R) and inv_path.is_file()
            assert candidate['sourceNativeId']==sp['sourceNativeId']==ps['sourceNativeId']
            assert candidate['cycle']==sp['cycle']==ps['cycle'] and candidate['cycle'] in (0,1)
            if candidate['cycle']==1:
                assert R.name.endswith('-cycle1')
                original_candidate=m.read(R.with_name(R.name.removesuffix('-cycle1'))/'candidate.json')
                assert candidate['sourceNativeId']==original_candidate['sourceNativeId']
                assert e['beforeCard']==original_candidate['entries'][0]['proposedCard']
                assert m.read(D/('independent-fashion'+str(e['sourceOrder'])+'-initial/receipt.json'))['entries'][0]['status']=='FIX'
            assert explicit['path']==declared and explicit['sha256']==global_audit['freshInventorySHA256']==m.raw(inv_path)
            bound_inventory=m.read(inv_path)
            assert explicit['globalRowsCanonicalSHA256']==global_audit['rowsCanonicalSHA256']==bound_inventory['globalMAIN']['rowsCanonicalSHA256']
            assert bound_inventory['sameTopicMAIN']['questions']==ps['sameTopicMAIN']['questions']==topic['questions']
            assert bound_inventory['sameTopicMAIN']['fileSHA256']==ps['sameTopicMAIN']['fileSHA256']==m.raw(C/ps['sameTopicMAIN']['path'])
            assert len(topic['questions'])==100 and len(global_audit['allCurrentFileByteBindings'])==110
            ps['sameTopicMAIN']['freshInventoryPath']=declared
            sp['technicalExplicitSourceIndexInventoryAlias']={'path':declared,'fileSHA256':m.raw(inv_path),'rawPeerSHA256':m.raw(R/'peer-snapshot.json'),'operation':'Exact explicit sourceIndex freshInventory path/SHA and identical full100 topic bodies; redundant peer locator name only. Raw and all assessments unchanged.'}
        assert ps['sameTopicMAIN']['freshInventoryPath']==declared
        assert m.raw(inv_path)==global_audit['freshInventorySHA256']
        inv=m.read(inv_path)
        assert inv['globalMAIN']['topicFileCount']==110 and inv['globalMAIN']['questionCount']==11000
        assert inv['globalMAIN']['rowsCanonicalSHA256']==global_audit['rowsCanonicalSHA256']
        assert inv['sameTopicMAIN']['questions']==topic['questions']
        assert len(inv['globalMAIN']['allCurrentFileByteBindings'])==110
        for binding in inv['globalMAIN']['allCurrentFileByteBindings']:
            assert m.raw(C/binding['path'])==binding['sha256']
        sp['freshInventoryPath']=str(inv_path)
        sp['freshInventorySHA256']=m.raw(inv_path)
        global_audit['originalFreshInventoryPath']=declared
        global_audit['freshInventoryPath']=str(inv_path)
        ps['technicalSourceproofProseInventoryLocatorAlias']={'originalSourceIndex':sp['sourceIndex'],'explicitRawPeerPath':declared,'explicitRawPeerSHA256':m.raw(inv_path),'operation':'Exact already-bound author inventory and all100/110 live checks; path/container alias only, no new semantic assessment.'}
    if global_audit is not None and 'freshInventoryPath' in global_audit and 'sourceInventoryPath' not in global_audit:
        inv_path=pathlib.Path(global_audit['freshInventoryPath'])
        if 'sourceInventoryPath' not in sp:
            assert str(inv_path) == sp['freshInventoryPath']
            assert m.raw(inv_path) == sp['freshInventorySHA256'] == global_audit['freshInventorySHA256']
            sp['sourceInventoryPath']=sp['freshInventoryPath']
            sp['sourceInventorySHA256']=sp['freshInventorySHA256']
            sp['technicalExplicitFreshSourceInventoryAlias']='Identical explicit author path and verified file SHA; names only, no unbound hydration or assessment.'
        assert str(inv_path) == sp['sourceInventoryPath']
        assert m.raw(inv_path) == global_audit['freshInventorySHA256'] == sp['sourceInventorySHA256']
        inv=m.read(inv_path)
        assert inv['globalMAIN']['rowsCanonicalSHA256'] == global_audit['rowsCanonicalSHA256']
        assert inv['globalMAIN']['questionCount'] == global_audit['questionCount'] == 11000
        original=dict(global_audit)
        global_audit.update(sourceInventoryPath=str(inv_path),sourceInventorySHA256=m.raw(inv_path),topicFileCount=inv['globalMAIN']['topicFileCount'])
        global_audit['originalFreshInventoryReference']=original
        same=ps['sameTopicMAIN']
        assert same['questionCount'] == inv['sameTopicMAIN']['questionCount'] == 100
        assert (C/same['path']).resolve() == (C/inv['sameTopicMAIN']['path']).resolve()
        assert same['fileSHA256'] == inv['sameTopicMAIN']['fileSHA256'] == m.raw(C/same['path'])
        same.update(sourceInventoryPath=str(inv_path),sourceInventorySHA256=m.raw(inv_path))
        ps['technicalFreshInventoryReferenceAlias']='Exact explicit path+SHA bound independently in sourceproof and globalMAIN; alias names only, no unbound hydration or peer assessment.'
    if 'inventoryPath' in global_audit and 'inventoryFileSHA256' in global_audit and 'sourceInventoryPath' not in sp:
        # Explicit immutable peer inventory binding within the exact author bundle.
        # Require the full existing rows/files/topic snapshots before naming aliases.
        assert candidate['sourceNativeId']==sp['sourceNativeId']==ps['sourceNativeId']
        assert candidate['cycle']==sp['cycle']==ps['cycle']
        assert sp['entries'][0]['id']==e['id']
        declared=global_audit['inventoryPath']
        inv_path=pathlib.Path(declared);inv_path=inv_path if inv_path.is_absolute() else C/inv_path
        assert inv_path.is_relative_to(R) and inv_path.is_file()
        assert m.raw(inv_path)==global_audit['inventoryFileSHA256']
        inv=m.read(inv_path)
        assert inv['globalMAIN']['topicFileCount']==global_audit['topicFileCount']==110
        assert inv['globalMAIN']['questionCount']==global_audit['questionCount']==11000
        inventory_current_rows=[]
        for current_path in sorted((C/'src/content/topics').glob('*.json')):
            current_topic=m.read(current_path)
            inventory_current_rows.extend({'topicId':current_topic['id'],'id':q['id'],'prompt':q['prompt'],'answers':[v['text'] for v in q['answers']],'correctIndex':q['correctIndex']} for q in current_topic['questions'])
        assert len(inventory_current_rows)==11000
        assert inv['globalMAIN']['rowsCanonicalSHA256']==global_audit['rowsCanonicalSHA256']==m.sha(inventory_current_rows)
        original_file_bindings=global_audit['allCurrentFileByteBindings']
        assert len(original_file_bindings)==110
        normalized_file_bindings=[]
        for binding in original_file_bindings:
            digest=next(binding[k] for k in ['sha256','fileSHA256','fileSha256'] if k in binding)
            current_topic=m.read(C/binding['path'])
            assert m.raw(C/binding['path'])==digest
            assert binding.get('topicId',current_topic['id'])==current_topic['id']
            assert binding.get('questionCount',len(current_topic['questions']))==len(current_topic['questions'])==100
            normalized_file_bindings.append({'path':binding['path'],'sha256':digest})
        assert inv['globalMAIN']['allCurrentFileByteBindings']==normalized_file_bindings
        original_questions=ps['sameTopicMAIN']['questions']
        assert len(original_questions)==100
        if all(isinstance(v,dict) and 'card' in v for v in original_questions):
            assert [v['sourceOrder'] for v in original_questions]==list(range(1,101))
            assert all(v['topicId']==e['topicId'] and v['id']==v['card']['id'] and m.sha(v['card'])==v['sha256'] for v in original_questions)
            inventory_topic_bodies=[v['card'] for v in original_questions]
        else:
            inventory_topic_bodies=original_questions
        assert inv['sameTopicMAIN']['questions']==inventory_topic_bodies==topic['questions']
        assert len(topic['questions'])==100
        global_audit['originalAugmentedFileByteBindings']=original_file_bindings
        global_audit['allCurrentFileByteBindings']=normalized_file_bindings
        assert inv['sameTopicMAIN']['fileSHA256']==ps['sameTopicMAIN']['fileSHA256']==m.raw(C/ps['sameTopicMAIN']['path'])
        sp['sourceInventoryPath']=str(inv_path);sp['sourceInventorySHA256']=m.raw(inv_path)
        global_audit.update(inventoryPath=str(inv_path),inventorySHA256=m.raw(inv_path))
        ps['sameTopicMAIN'].update(inventoryPath=str(inv_path),inventorySHA256=m.raw(inv_path))
        ps['technicalExplicitPeerInventoryBindingAlias']={'originalPeerPath':declared,'fileSHA256':m.raw(inv_path),'rawPeerSnapshot':str(R/'peer-snapshot.json'),'rawPeerSnapshotSHA256':m.raw(R/'peer-snapshot.json'),'operation':'Only names/path representation for exact author peer-bound inventory after all110/11000/100 current checks; raw and semantic judgments unchanged.'}
    if 'inventoryPath' in global_audit and 'sourceInventoryPath' not in sp and 'sourceInventoryPath' not in global_audit:
        # Optional unbound locator is not proof and must never hydrate bodies.
        # The original raw packet already binds all110 files/11000 rows and
        # all100 ordered full bodies, independently of that optional file.
        assert 'inventorySHA256' not in global_audit and 'inventorySHA256' not in ps['sameTopicMAIN']
        assert candidate['sourceNativeId']==sp['sourceNativeId']==ps['sourceNativeId']
        assert candidate['cycle']==sp['cycle']==ps['cycle']
        # A locator with no digest is optional metadata. Missing corresponding
        # topic locator cannot supply proof and must not hydrate an inventory.
        original_topic_locator=ps['sameTopicMAIN'].get('inventoryPath')
        assert original_topic_locator is None or global_audit['inventoryPath']==original_topic_locator
        assert len(global_audit['allCurrentFileByteBindings'])==110
        full=ps['actualCurrentPeers']
        if len(full)==100:
            assert [v['sourceOrder'] for v in full]==list(range(1,101))
            assert [v['card'] for v in full]==topic['questions']
        else:
            # Explicit full topic remains100; a distinct-peer list may omit
            # the candidate itself. Do not invent a self peer or read the
            # optional undigested inventory file to fill that list.
            assert len(full)==99
            assert {v['id'] for v in full}=={q['id'] for q in topic['questions']}-{e['id']}
            assert ps['sameTopicMAIN']['questions']==topic['questions'] and len(topic['questions'])==100
            assert ps['sameTopicMAIN']['fileSHA256']==m.raw(C/ps['sameTopicMAIN']['path'])
            checkpoint=m.read(P/'openspec/changes/question-quality-future-waves/current-checkpoint.json')
            frozen_topic=json.loads(subprocess.check_output(['git','-C',str(C),'show',checkpoint['baselineSHA']+':'+ps['sameTopicMAIN']['path']]))
            assert [q['id'] for q in frozen_topic['questions']]==[q['id'] for q in topic['questions']]
            positions={q['id']:(i,q) for i,q in enumerate(topic['questions'],1)}
            absent_orders=[]
            for v in full:
                position,body=positions[v['id']]
                assert v['card']==body
                if 'sourceOrder' in v:assert v['sourceOrder']==position
                else:
                    absent_orders.append(v['id']);v['sourceOrder']=position
            if absent_orders:
                ps['technicalExplicitPeerOrderAlias']={'rawPeerSnapshot':str(R/'peer-snapshot.json'),'rawPeerSHA256':m.raw(R/'peer-snapshot.json'),'originalSourceOrderAbsentFor':absent_orders,'originalFullTopicPointer':'/sameTopicMAIN/questions','frozenOrderCommit':checkpoint['baselineSHA'],'operation':'Exact peer ID/full body maps to existing explicit100-topic position, additionally identical to frozen baseline ID order. Original field absence and raw retained; no peer body or semantic judgment changed.'}
        assert all(v['topicId']==e['topicId'] and v['id']==v['card']['id'] and m.sha(v['card'])==v.get('sha256',v.get('canonicalSHA256')) for v in full)
        ps['technicalCompleteInlineSnapshotNoInventoryHydration']={'originalOptionalInventoryLocator':global_audit['inventoryPath'],'originalOptionalTopicInventoryLocator':original_topic_locator,'actualPeerCount':len(full),'candidateExcludedFromDistinctPeers':len(full)==99,'rawPeerSnapshot':str(R/'peer-snapshot.json'),'rawPeerSHA256':m.raw(R/'peer-snapshot.json'),'operation':'No inventory file read or SHA invented. Use already explicit full100 topic bodies, all110 raw file bindings and original11000 row digest, validated by unchanged downstream checks. Optional locator remains untrusted metadata; author raw and semantic grounds unchanged. A99peer list excludes self and remains unchanged.'}
    if 'inventoryPath' in global_audit and 'sourceInventoryPath' in sp and 'inventoryPath' not in ps.get('sameTopicMAIN',{}):
        # Redundant names only: both original files already bind one immutable
        # author inventory and all100 full peer bodies, not an unbound hydration.
        ip=pathlib.Path(global_audit['inventoryPath'])
        assert ip.is_relative_to(R) and str(ip)==sp['sourceInventoryPath']
        digest=global_audit['inventoryFileSHA256']
        assert m.raw(ip)==digest==sp['sourceInventorySHA256']
        inv=m.read(ip);same=ps['sameTopicMAIN'];full=ps['actualCurrentPeers']
        assert inv['globalMAIN']['rowsCanonicalSHA256']==global_audit['rowsCanonicalSHA256']
        assert inv['globalMAIN']['topicFileCount']==global_audit['topicFileCount']==110
        assert inv['globalMAIN']['questionCount']==global_audit['questionCount']==11000
        assert len(full)==same['questionCount']==100
        assert [v['sourceOrder'] for v in full]==list(range(1,101))
        assert [v['card'] for v in full]==inv['sameTopicMAIN']['questions']==topic['questions']
        assert all(v['topicId']==topic['id'] and v['id']==v['card']['id'] and m.sha(v['card'])==v['sha256'] for v in full)
        assert same['path']==inv['sameTopicMAIN']['path'] and same['topicId']==topic['id']
        assert same['fileSHA256']==inv['sameTopicMAIN']['fileSHA256']==m.raw(C/same['path'])
        global_audit['inventorySHA256']=digest
        same.update(inventoryPath=str(ip),inventorySHA256=digest)
        ps['technicalExactInventoryRedundantNamesAlias']={'rawPeerPath':str(R/'peer-snapshot.json'),'rawPeerSHA256':m.raw(R/'peer-snapshot.json'),'inventoryPath':str(ip),'inventoryFileSHA256':digest,'verifiedFullOrderedPeers':100,'operation':'Existing sourceproof/global path+SHA, exact full100 bodies and topic/file SHA verified; redundant names only. Raw, sources, judgments unchanged; original missing-field failure uncured.'}
    if 'inventoryPath' in global_audit and 'sourceInventoryPath' not in global_audit and 'sourceInventoryPath' in sp:
        inv_path=pathlib.Path(global_audit['inventoryPath'])
        inv_path=inv_path if inv_path.is_absolute() else C/inv_path
        assert str(inv_path)==sp['sourceInventoryPath']==ps['sameTopicMAIN']['inventoryPath']
        assert m.raw(inv_path)==sp['sourceInventorySHA256']==global_audit['inventorySHA256']==ps['sameTopicMAIN']['inventorySHA256']
        inv=m.read(inv_path)
        assert inv['globalMAIN']['topicFileCount']==global_audit['topicFileCount']==110
        assert inv['globalMAIN']['questionCount']==global_audit['questionCount']==11000
        assert inv['globalMAIN']['rowsCanonicalSHA256']==global_audit['rowsCanonicalSHA256']
        assert len(inv['globalMAIN']['allCurrentFileByteBindings'])==110
        assert inv['sameTopicMAIN']['questions']==topic['questions'] and len(topic['questions'])==100
        global_audit.update(sourceInventoryPath=str(inv_path),sourceInventorySHA256=m.raw(inv_path))
        global_audit['technicalInventoryPathNameAlias']='Exact sourceproof and both peer containers declare identical immutable inventory path and SHA; names only.'
    same_questions=ps.get('sameTopicMAIN',{}).get('questions',[])
    if len(same_questions)==100 and all(isinstance(p,dict) and 'card' in p for p in same_questions):
        assert [p['sourceOrder'] for p in same_questions]==list(range(1,101))
        assert all(p['topicId']==e['topicId'] and p['id']==p['card']['id'] and m.sha(p['card'])==p['sha256'] for p in same_questions)
        assert [p['card'] for p in same_questions]==topic['questions']
        ps['originalSameTopicQuestionWrappers']=same_questions
        ps['sameTopicMAIN']['questions']=[p['card'] for p in same_questions]
        ps['technicalSameTopicQuestionWrapperAlias']='Exact100 original ordered full card bodies and hashes, wrapper only; raw unchanged.'
    # Explicit full100 ordered author peers are a retained topic snapshot,
    # even when the original names its container actualCurrentPeers only.
    if 'questions' not in ps.get('sameTopicMAIN',{}) and len(ps.get('actualCurrentPeers',[])) == 100:
        full_peers=ps['actualCurrentPeers']
        assert all(p['topicId']==e['topicId'] for p in full_peers)
        assert [p['sourceOrder'] for p in full_peers]==list(range(1,101))
        assert [p['card'] for p in full_peers]==topic['questions']
        assert all(m.sha(p['card'])==p.get('sha256',p.get('canonicalSHA256')) for p in full_peers)
        topic_path=f"src/content/topics/{e['topicId']}.json"
        binding=next(f for f in global_audit['allCurrentFileByteBindings'] if f['path']==topic_path)
        bound_sha=binding.get('sha256',binding.get('fileSHA256',binding.get('fileSha256')))
        assert m.raw(C/topic_path)==bound_sha
        if 'sameTopicMAIN' in ps:
            original_same=ps['sameTopicMAIN']
            if 'topicId' not in original_same:
                assert original_same['path']==topic_path and original_same['questionCount']==100 and original_same['fileSHA256']==bound_sha
                assert topic['id']==e['topicId'] and all(peer['topicId']==e['topicId'] for peer in full_peers)
                assert [peer['card'] for peer in full_peers]==topic['questions']
                ps['technicalMissingRedundantTopicIdAlias']={'rawPeerPath':str(R/'peer-snapshot.json'),'rawPeerSHA256':m.raw(R/'peer-snapshot.json'),'originalTopicIdAbsent':True,'candidateTopicId':e['topicId'],'operation':'Exact candidate/topic id plus all100 original ordered peer topicIds and full bodies, path/file SHA/count already verified; redundant identity name only. Raw and semantic judgments unchanged; original format gap uncured.'}
                original_same={**original_same,'topicId':e['topicId']}
            assert original_same['path']==topic_path and original_same['topicId']==e['topicId'] and original_same['questionCount']==100 and original_same['fileSHA256']==bound_sha
            ps['originalSameTopicMAINMetadata']=ps['sameTopicMAIN']
        ps['sameTopicMAIN']={'topicId':e['topicId'],'path':topic_path,'fileSHA256':bound_sha,'questionCount':100,'questions':[p['card'] for p in full_peers]}
        ps['technicalExplicitFullPeerSnapshotContainerAlias']='All100 original ordered full peer bodies and explicit global file binding verified; names only, no unbound hydration or new assessment.'
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
        if 'sourceInventoryPath' not in same_topic:
            assert sp['sourceInventoryPath'] == str(inventory_path)
            assert sp['sourceInventorySHA256'] == m.raw(inventory_path) == global_audit['sourceInventorySHA256']
            assert (C/same_topic['path']).resolve() == (C/saved_inventory['sameTopicMAIN']['path']).resolve()
            assert same_topic['questionCount'] == saved_inventory['sameTopicMAIN']['questionCount'] == 100
            assert same_topic['fileSHA256'] == saved_inventory['sameTopicMAIN']['fileSHA256'] == m.raw(C/same_topic['path'])
            same_topic.update(sourceInventoryPath=str(inventory_path),sourceInventorySHA256=m.raw(inventory_path))
            same_topic['technicalExplicitInventoryContainerAlias']='Exact sourceproof/globalMAIN explicit path and SHA plus topic path/fileSHA/count equality; no invented snapshot or assessment.'
        assert same_topic['sourceInventoryPath'] == str(inventory_path)
        assert same_topic['sourceInventorySHA256'] == m.raw(inventory_path)
        assert saved_inventory['sameTopicMAIN']['questions'] == topic['questions']
        same_topic['questions'] = saved_inventory['sameTopicMAIN']['questions']
        same_topic['technicalHydration'] = 'Exact original saved100 bodies from SHA-bound author inventory; no new assessment.'
    if 'sameTopicMAIN' not in ps and 'currentTopicSnapshot' in ps:
        retained_topic = ps['currentTopicSnapshot']
        assert retained_topic['topicId'] == topic['id']
        assert retained_topic['questionCount'] == len(retained_topic['questions']) == 100
        assert retained_topic['questions'] == topic['questions']
        assert retained_topic['fileSHA256'] == m.raw(C / retained_topic['path'])
        ps['sameTopicMAIN'] = retained_topic
        ps['technicalSameTopicContainerAlias'] = 'Exact author-retained currentTopicSnapshot full100 bodies and current file hash; no hydration or peer judgment.'
    # A directed naming-only repair retained the original INITIAL inventory.
    # Rebind only its own historical preimage after proving the full initial
    # application chain and that every other catalog body is unchanged.
    if candidate['cycle'] == 1 and R.name.endswith('-cycle1') and 'rows' in global_audit:
        old_questions = ps['sameTopicMAIN'].get('questions', [])
        changes = [(a,b) for a,b in zip(old_questions,topic['questions']) if a != b]
        if changes:
            assert len(old_questions) == len(topic['questions']) == 100 and len(changes) == 1
            old_self, live_self = changes[0]
            prior_path = R.with_name(R.name.removesuffix('-cycle1'))/'candidate.json'
            prior = m.read(prior_path)['entries'][0]
            assert old_self == prior['beforeCard'] and live_self == prior['proposedCard'] == e['beforeCard']
            assert e['proposedCard'] == {**live_self, 'prompt':live_self['prompt'].replace('Амри','Эймери'), 'explanation':live_self['explanation'].replace('Амри','Эймери')}
            original_global = json.loads(json.dumps(global_audit))
            old_rows, live_rows = [], []
            bindings = global_audit['allCurrentFileByteBindings']
            assert len(bindings) == 110
            for f in bindings:
                p = C/f['path']; t = m.read(p)
                if t['id'] == e['topicId']:
                    old_topic = {**t,'questions':old_questions}
                    assert hashlib.sha256((json.dumps(old_topic,ensure_ascii=False,indent=2)+'\n').encode()).hexdigest() == f['sha256']
                    f['sha256'] = m.raw(p)
                else:
                    assert m.raw(p) == f['sha256']
                    old_topic = t
                for source, dest in [(old_topic,old_rows),(t,live_rows)]:
                    dest.extend({'topicId':source['id'],'id':q['id'],'prompt':q['prompt'],'answers':[v['text'] for v in q['answers']],'correctIndex':q['correctIndex']} for q in source['questions'])
            assert old_rows == global_audit['rows'] and m.sha(old_rows) == global_audit['rowsCanonicalSHA256']
            ps['originalHistoricalSelfInventory'] = original_global
            global_audit.update(rows=live_rows,rowsCanonicalSHA256=m.sha(live_rows))
            ps['sameTopicMAIN']['questions'] = topic['questions']
            if 'fileSHA256' in ps['sameTopicMAIN']:
                ps['sameTopicMAIN']['fileSHA256'] = m.raw(C/f"src/content/topics/{e['topicId']}.json")
            for peer in ps['actualCurrentPeers']:
                if peer['id'] == e['id']:
                    assert peer['card'] == old_self and peer['sha256'] == m.sha(old_self)
                    peer.update(originalHistoricalSelfPreimage=peer['card'],card=live_self,sha256=m.sha(live_self))
            ps['technicalSelfOnlyCatalogDelta'] = {'priorCandidate':str(prior_path.relative_to(C)), 'priorCandidateRawSHA256':m.raw(prior_path), 'oldSelfSHA256':m.sha(old_self), 'currentSelfSHA256':m.sha(live_self), 'otherCardsUnchanged':True, 'selfIsDistinctPeer':False, 'operation':'Machine freshness only; exact naming repair; no peer assessment created or changed.'}
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
        original_path=source['path']
        recovery_path=R/'raw/recovery.json'
        if not recovery_path.exists() and candidate['cycle']==1 and R.name.endswith('-cycle1') and (R.with_name(R.name.removesuffix('-cycle1'))/'raw/recovery.json').exists():
            initial_raw=R.with_name(R.name.removesuffix('-cycle1'))
            initial_candidate=m.read(initial_raw/'candidate.json')
            assert e['beforeCard']==initial_candidate['entries'][0]['proposedCard']
            assert candidate['sourceNativeId']==initial_candidate['sourceNativeId']
            recovery_path=initial_raw/'raw/recovery.json'
        if recovery_path.exists() and p.suffix=='.json':
            oldcap=m.read(p)
            if isinstance(oldcap,dict) and 'originalRecord' in oldcap:
                oldbody=oldcap['originalRecord']['payload']['output'][1]['text']
                if oldbody.startswith('Warning: truncated output'):
                    recovery=m.read(recovery_path);rp=pathlib.Path(recovery['capture']['path']);recap=m.read(rp)
                    assert m.raw(rp)==recovery['capture']['fileSHA256']
                    assert recovery['networkCalls']==0 and recovery['reEmission']['retainedStoreLoaded'] is True
                    assert recap['sourceNativeId']==oldcap['sourceNativeId']==candidate['sourceNativeId']
                    journal=[json.loads(l) for l in pathlib.Path(recap['nativeJournal']).open()]
                    assert journal[oldcap['nativeRecordLine']-1]==oldcap['originalRecord']
                    assert journal[recap['nativeRecordLine']-1]==recap['originalRecord']
                    oldcall=journal[recovery['originalRetainedResult']['functionsExecCallOrdinal']-1]['payload']
                    assert oldcall['call_id']==oldcap['originalRecord']['payload']['call_id']
                    key=recovery['originalRetainedResult']['storeKey'];assert key in oldcall['input'] and 'store(' in oldcall['input']
                    newcall=next(r['payload'] for r in journal if r.get('payload',{}).get('call_id')==recap['originalRecord']['payload']['call_id'] and r.get('payload',{}).get('type')=='custom_tool_call')
                    assert key in newcall['input'] and 'text(load(' in newcall['input']
                    assert not re.search(r'(?m)^\s*(?:(?:const|let|var)\s+\w+\s*=\s*|text\(\s*)?await\s+tools\.web__run\s*\(',newcall['input'])
                    full=recap['originalRecord']['payload']['output'][1]['text']
                    assert not re.search(r'Warning: truncated output|…\d+ tokens truncated…',full)
                    parts=re.split(r'…\d+ tokens truncated…',oldbody.split('\n\n',1)[1]);assert len(parts)==2
                    assert all(part in full for part in parts) and full.index(parts[0])<full.index(parts[1])
                    assert source['url'] in full
                    source.update(path=str(rp.relative_to(C)),sha256=m.raw(rp),completeOutputPointer=recap['completeOutputPointer'],completeOutputSHA256=recap['completeOutputSHA256'],originalTruncatedSourceBinding=original,technicalRetainedStoreFullOutputRecovery={'recovery':str(recovery_path.relative_to(C)),'recoverySHA256':m.raw(recovery_path),'oldNativeLine':oldcap['nativeRecordLine'],'newNativeLine':recap['nativeRecordLine'],'visibleOriginalPrefixSuffixExact':True,'networkCalls':0,'operation':'Existing original store result re-emitted in full, not a source retry; raw packet and old captures immutable.'})
                    p=rp;digest=m.raw(p)

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
                native_path = pathlib.Path(capture.get('nativeJournal') or capture['nativeJournalActual'])
                if not native_path.exists():
                    matches = list(pathlib.Path('/Users/eaafonasev/.codex/archived_sessions').glob('*'+capture['sourceNativeId']+'.jsonl'))
                    assert len(matches) == 1
                    native_path = matches[0]
                native_record = json.loads(native_path.read_text().split('\n')[capture['nativeRecordLine']-1])
                assert native_record == capture['originalRecord']
                assert capture['sourceNativeId'] == candidate['sourceNativeId']
                source['originalNativeRecordRelativePointer'] = source['completeOutputPointer']
                source['completeOutputPointer'] = '/originalRecord'+source['completeOutputPointer']
                source['technicalCaptureWrapperPointerAlias'] = 'Exact retained originalRecord verified against actual native journal line; prefix only, raw unchanged.'
            # A reused capture may retain the old sourceproof's container pointer.
            # Alias only when the unchanged native wrapper, URL and exact declared
            # body digest independently identify the same full original output.
            if isinstance(capture,dict) and 'originalRecord' in capture:
                try:
                    probe = m.read(p)
                    for key in source['completeOutputPointer'].split('/')[1:]:
                        probe = probe[int(key)] if isinstance(probe,list) else probe[key]
                except (KeyError,IndexError,TypeError,ValueError):
                    native_path = pathlib.Path(capture.get('nativeJournal') or capture['nativeJournalActual'])
                    if not native_path.exists():
                        matches = list(pathlib.Path('/Users/eaafonasev/.codex/archived_sessions').glob('*'+capture['sourceNativeId']+'.jsonl'))
                        assert len(matches) == 1
                        native_path = matches[0]
                    assert json.loads(native_path.read_text().split('\n')[capture['nativeRecordLine']-1]) == capture['originalRecord']
                    bound = m.read(p)
                    pointer = capture['completeOutputPointer']
                    if pointer.startswith('/payload/'):
                        pointer = '/originalRecord'+pointer
                    for key in pointer.split('/')[1:]:
                        bound = bound[int(key)] if isinstance(bound,list) else bound[key]
                    assert isinstance(bound,str) and source['url'] in bound
                    body_sha = hashlib.sha256(bound.encode()).hexdigest()
                    assert capture['completeOutputSHA256'] == body_sha
                    assert source['completeOutputSHA256'] in (body_sha,m.sha(bound))
                    source['originalInvalidContainerPointer'] = source['completeOutputPointer']
                    source['completeOutputPointer'] = pointer
                    source['technicalNativeBoundContainerPointerAlias'] = {'nativeId':capture['sourceNativeId'],'nativeRecordLine':capture['nativeRecordLine'],'originalRecordExact':True,'sameDeclaredBodySHA256':body_sha,'operation':'Pointer only; author raw, source body, locator and judgments unchanged.'}
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
                native_path = pathlib.Path(capture.get('nativeJournal') or capture['nativeJournalActual'])
                if not native_path.exists():
                    matches = list(pathlib.Path('/Users/eaafonasev/.codex/archived_sessions').glob('*'+capture['sourceNativeId']+'.jsonl'))
                    assert len(matches) == 1
                    native_path = matches[0]
                native_record = json.loads(native_path.read_text().split('\n')[capture['nativeRecordLine']-1])
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
        rel = str(p.relative_to(C)); paths[original_path] = rel; paths[str(C/original_path)] = rel; paths[source['path']] = rel
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
    if R.name=='source-human-medicine28':
        binding=m.read(D/'source28-intake-variant-container-alias.json')
        original_sp=m.read(R/'sourceproof.json')
        assert candidate['sourceNativeId']==binding['sourceNativeId']
        assert m.raw(R/'sourceproof.json')==binding['rawSourceproofSHA256'] and m.raw(R/'candidate.json')==binding['rawCandidateSHA256'] and m.raw(R/'peer-snapshot.json')==binding['rawPeerSHA256']
        for i,v in enumerate(sp['entries'][0]['fourFullPromptAnswerNoteAssessments']):
            original=original_sp['entries'][0]['fourFullPromptAnswerNoteAssessments'][i];b=binding['originalCombinedAssessmentBindings'][i]
            assert v['slot']==original['slot']==b['slot'] and v['grammar']==original['grammar'] and m.sha(v['grammar'])==b['literalCanonicalSHA256']
            assert v['tripleSHA256']==original['tripleSHA256']==b['tripleSHA256'] and 'plausibilityUniqueKeyAndNoteTruthUsefulness' not in v
            v['plausibilityUniqueKeyAndNoteTruthUsefulness']=v['grammar']
            v['technicalOriginalCombinedAssessmentFieldAlias']={'binding':str(D/'source28-intake-variant-container-alias.json'),'originalPointer':b['originalPointer'],'operation':'Identical full existing combined author assessment string; standard container name only. Original grammar and raw retained.'}
    for v in sp['entries'][0]['fourFullPromptAnswerNoteAssessments']:
        triple = {'prompt':v['fullPrompt'],'answer':v['answer'],'note':v['note']}
        if 'tripleSHA256' in v and v['tripleSHA256'] != m.sha(triple):
            if v['tripleSHA256'] == m.sha({'fullPrompt':v['fullPrompt'],'answer':v['answer'],'note':v['note']}):
                v['originalFullPromptKeyTripleSHA256'] = v['tripleSHA256']
                v['technicalTripleShapeAlias'] = 'Same exact author fullPrompt/answer/note literals; fullPrompt key named prompt in canonical triple only.'
            elif v['tripleSHA256']==m.sha([v['fullPrompt'],v['answer'],v['note']]):
                v['originalOrderedListTripleSHA256']=v['tripleSHA256']
                v['technicalTripleShapeAlias']='Exact ordered three literal list [prompt,answer,note] mapped to canonical named object; candidate/six-group/whole literal identity already verified, no ground or raw change.'
            else:
                assert v['tripleSHA256'] == m.sha({'slot':v['slot'],**triple})
                v['originalSlotIncludedTripleSHA256'] = v['tripleSHA256']
                v['technicalTripleShapeAlias'] = 'Same author full prompt/answer/note, redundant numeric slot excluded from canonical triple hash only.'
            v['tripleSHA256'] = m.sha(triple)
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
