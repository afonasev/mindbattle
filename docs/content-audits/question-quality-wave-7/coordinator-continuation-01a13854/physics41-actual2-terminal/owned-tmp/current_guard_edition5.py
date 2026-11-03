import json,pathlib,hashlib,copy
root=pathlib.Path('/tmp/mindbattle-source-01a13841-3085-7ba3-9570-46d16b85c036')
source=pathlib.Path('/Users/eaafonasev/Documents/Codex/2026-10-14/mindbattle-source-physics-next20/outputs/physics-source20-author-edition4.json')
rtpath=pathlib.Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle/src/content/topics/physics.json')
out=root/'author-original-edition5.json'
expected_e4='afb22bdbf0e92fae6f8b91294e7aca547f9510f4f55a91360a32a97529f08f14'
expected_runtime='0d139298a115b597d7b851361d9683dcfebea1a2b39047168ba1223d506ac22a'
e4bytes=source.read_bytes(); rtb=rtpath.read_bytes()
if hashlib.sha256(e4bytes).hexdigest()!=expected_e4: raise RuntimeError('edition 4 changed; stop and reconcile')
if hashlib.sha256(rtb).hexdigest()!=expected_runtime: raise RuntimeError('authoritative physics runtime changed; stop and reconcile')
d=json.loads(e4bytes); d['edition']=5
d['parentArtifact']={'path':str(source),'bytes':len(e4bytes),'sha256':expected_e4}
rt=json.loads(rtb)
ids=['physics-photoelectric-threshold-frequency','physics-meissner-effect','physics-de-broglie-wavelength']
current={q['id']:q for q in rt['questions'] if q.get('id') in ids}
if set(current)!=set(ids): raise RuntimeError('missing current protected IDs')
# Existing preimage keys are historical stable slots. Update by card ID, preserving each slot/index.
protected={x['id']:x for x in d['all80ProtectedPreimage'] if x.get('id') in ids}
if set(protected)!=set(ids): raise RuntimeError('protected preimage does not contain exactly the expected IDs')
updates=[]
for cid in ids:
 q=current[cid]
 digest=hashlib.sha256(json.dumps(q,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
 obj=protected[cid]
 obj['card']=copy.deepcopy(q)
 obj['currentCanonicalSha256']=digest
 obj['difficulty']=q['difficulty']
 obj['id']=cid
 updates.append({'protectedIndex':obj['index'],'id':cid,'currentCanonicalSha256':digest,'runtimeListPositionZeroBased':rt['questions'].index(q)})
# Explicitly log only semantic relationships affected by this refresh; no content/status changes to the 20 targets.
d['semanticNeighborhoodDelta']={
 'basis':{'runtimePath':str(rtpath),'runtimeBytes':len(rtb),'runtimeRawSha256':expected_runtime,'refreshedProtectedIndices':[26,27,28]},
 'comparisons':[
  {'protectedIndex':26,'protectedId':'physics-photoelectric-threshold-frequency','currentCanonicalSha256':updates[0]['currentCanonicalSha256'],'candidateIndex':36,'candidateId':'physics-frequency-unit','relationship':'Both mention frequency, but the protected prompt asks how two photon-frequency/intensity settings change photoelectron energy and emission rate; the candidate asks which phenomena use the SI hertz. Their predicates differ.'},
  {'protectedIndex':27,'protectedId':'physics-meissner-effect','currentCanonicalSha256':updates[1]['currentCanonicalSha256'],'candidateIndexes':[38,47],'candidateIds':['physics-magnet-like-poles','physics-metal-conductor'],'relationship':'The protected prompt distinguishes magnetic-flux expulsion on superconducting transition from flux preservation in a zero-resistance ideal conductor. Candidate #38 asks attraction/repulsion of like magnetic poles; #47 asks where collision energy in a normal conductor goes. They share broad magnetism/material context, not the tested behavior.'},
  {'protectedIndex':28,'protectedId':'physics-de-broglie-wavelength','currentCanonicalSha256':updates[2]['currentCanonicalSha256'],'candidateIndex':45,'candidateId':'physics-light-vacuum','relationship':'The protected prompt calculates the electron de Broglie wavelength and diffraction order. Candidate #45 classifies light as an electromagnetic wave, distinct from mechanical waves.'}
 ],
 'scope':'Only protected preimage objects #26–28 are refreshed. The 20 target cards, full 100-ID order, all other 77 protected objects, and prior editions are unchanged.'}
d['authorNotes']={**d.get('authorNotes',{}),'revision':'edition5 additive current-preimage delta: refreshed only protected IDs at stable slots #26–28 from the current authoritative physics topic JSON; added the focused semantic-neighborhood distinctions. Target proposals and prior editions are unchanged.'}
d['sourceQualificationAudit']['authorStatus']='edition 5 current-protected-preimage refresh; independent source/semantic/editorial qualification remains pending'
if d.get('readerAttestation'):
 d['readerAttestation']['editionRead']='5-current-guard-delta'
 d['readerAttestation']['currentDeltaReadMethod']='Personally read the complete current raw runtime JSON bytes (SHA-256 recorded in semanticNeighborhoodDelta) and the full current cards at protected stable slots #26–28, matching by stable IDs. Compared only the relevant current neighbor facts against candidate #36, #38, #45 and #47. Refreshed exactly those three protected preimage objects; did not alter the 20 target cards or recompute unchanged source bindings.'
 d['readerAttestation']['qualificationCaveat']='This is an author-side current-preimage and focused semantic-dedup read, not independent qualification. No SOURCE credit or PASS is claimed by this addendum.'
raw=json.dumps(d,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
out.write_bytes(raw)
print(json.dumps({'path':str(out),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'protectedUpdates':updates,'targetCount':len(d['entries'])},ensure_ascii=False))
