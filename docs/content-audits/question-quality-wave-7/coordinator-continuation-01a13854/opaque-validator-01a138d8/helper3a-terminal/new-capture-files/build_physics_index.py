import json,hashlib
from pathlib import Path
SRC=Path('/tmp/mindbattle-source-01a138ab-750c-7813-87b3-e06ea25d1e17/author-original-edition11.json')
ROOT=Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle')
base=ROOT/'docs/content-audits/question-quality-wave-7'
ids='''physics-ext-speed-distance-time
physics-ext-mass-matter
physics-ext-temperature-warmth
physics-ext-force-interaction
physics-ext-energy-work-capacity
physics-ext-density-mass-volume
physics-ext-momentum-mass-velocity
physics-ext-impulse-force-time
physics-ext-power-work-rate
physics-ext-torque-rotation
physics-ext-angular-velocity
physics-ext-capacitance-charge-voltage
physics-ext-resistance-current-opposition
physics-ext-induction-current-field
physics-ext-refraction-medium
physics-ext-diffraction-obstacle
physics-ext-interference-superposition
physics-ext-electric-flux
physics-ext-magnetic-flux
physics-ext-self-inductance
physics-ext-refractive-index
physics-ext-young-modulus
physics-ext-bernoulli-principle
physics-ext-coriolis-force
physics-ext-moment-inertia
physics-ext-pressure-force-area
physics-ext-electric-current-charge-flow
physics-ext-voltage-energy-charge
physics-ext-frequency-cycles-second
physics-ext-wavelength-neighbor-crests
physics-ext-acceleration-velocity-change
physics-ext-resonance-natural-frequency
physics-ext-buoyant-force
physics-ext-viscosity-fluid-friction
physics-ext-specific-heat
physics-ext-latent-heat
physics-ext-entropy-disorder
physics-ext-half-life
physics-ext-photoelectric-effect
physics-ext-doppler-effect
physics-ext-terminal-velocity
physics-ext-elasticity-return-shape
physics-ext-angular-momentum
physics-ext-binding-energy
physics-ext-debroglie-wavelength
physics-ext-work-function
physics-ext-critical-angle
physics-ext-quality-factor
physics-ext-thermal-conductivity
physics-ext-mean-free-path'''.split()
def sha(b): return hashlib.sha256(b).hexdigest()
d=json.loads(SRC.read_bytes()); rows={x['id']:x for x in d['all80ProtectedPreimage'] if x.get('id') in ids}
assert set(rows)==set(ids),(len(rows),set(ids)-set(rows))
url_rows={}
for id0 in ids:
 row=rows[id0]; u=row['card']['source']['url']; url_rows.setdefault(u,[]).append(id0)
found={}
# Existing full raw captures with exact requested source URL; only parse capture manifest files, never evidenceBindings.
for p in (base/'physics').rglob('*.json'):
 if 'manifest' not in p.name.lower(): continue
 try:m=json.loads(p.read_bytes())
 except:continue
 if isinstance(m,dict) and isinstance(m.get('captures'),list):
  for c in m['captures']:
   u=c.get('requestedUrl') or c.get('requestedURL') or c.get('url')
   if u not in url_rows:continue
   if c.get('returnCode')!=0 or '\t200\t' not in str(c.get('stdout','')):continue
   bp=(p.parent/c['bodyPath']).resolve(); hp=(p.parent/c['headerPath']).resolve()
   if bp.is_file() and hp.is_file():
    found.setdefault(u,[]).append({'kind':'single-response','manifestPath':str(p),'manifestSHA256':sha(p.read_bytes()),'bodyPath':str(bp),'bodyBytes':bp.stat().st_size,'bodySHA256':sha(bp.read_bytes()),'headersPath':str(hp),'headersBytes':hp.stat().st_size,'headersSHA256':sha(hp.read_bytes()),'httpStatus':'200','curlExitCode':0})
# Exact pinned complete ranged entities in capture inventory.
for p in list((base/'coordinator-continuation-01a13772/capture-only').rglob('full-range-manifest.json'))+list((base/'coordinator-continuation-01a136e6/capture-only').rglob('full-range-manifest.json')):
 try:m=json.loads(p.read_bytes())
 except:continue
 u=m.get('url')
 if u not in url_rows or m.get('status')!='COMPLETE_PINNED_HTTP206_ENTITY':continue
 bp=ROOT/m['assembledPath']; records=m.get('records',[]); file_ok=bp.is_file() and bp.stat().st_size==m.get('assembledBytes') and sha(bp.read_bytes())==m.get('assembledSha256')
 record_ok=True
 for rec in records:
  for k,hk in [('bodyPath','bodySha256'),('headersPath','headersSha256')]:
   q=ROOT/rec[k]
   if not q.is_file() or q.stat().st_size!=rec.get('bodyBytes' if k=='bodyPath' else 'headersBytes') or sha(q.read_bytes())!=rec.get(hk):record_ok=False
 if file_ok and record_ok:
  initial=m.get('initial',{}); idir=p.parent
  # Find the saved initial body/header by the only exact page folder convention used in this inventory.
  candidates=[(idir/'initial.body',idir/'initial.headers'),(idir/'initial-0-8191.body',idir/'initial-0-8191.headers')]
  initial_body,initial_headers=next(((a,b) for a,b in candidates if a.exists() and b.exists()),(None,None))
  found.setdefault(u,[]).append({'kind':'pinned-range-entity','manifestPath':str(p),'manifestSHA256':sha(p.read_bytes()),'bodyPath':str(bp),'bodyBytes':m['assembledBytes'],'bodySHA256':m['assembledSha256'],'initialPartPath':str(initial_body) if initial_body else None,'initialHeadersPath':str(initial_headers) if initial_headers else None,'rangeRecordsPath':str(p.parent/'ranges'),'rangeRecordCount':len(records),'status':m['status'],'allRangeBodyHeaderHashesVerified':True})
# Prefer the coordinator's physics30-49 gap captures when available, otherwise the prior 20-29 range capture.
for u,ls in found.items():
 ls.sort(key=lambda x:(0 if 'coordinator-continuation-01a13772' in x['manifestPath'] else 1,0 if x['kind']=='pinned-range-entity' else 1))
entries=[]
for id0 in ids:
 u=rows[id0]['card']['source']['url']; refs=found.get(u,[])
 entries.append({'id':id0,'sourceUrl':u,'captureStatus':'EXACT_FULL_CAPTURE_FOUND' if refs else 'GAP_NO_EXACT_COMPLETE_CAPTURE_FOUND','capture':refs[0] if refs else None})
index={'schema':'mindbattle-physics-ext-capture-index-v1','scope':'Only the 50 supplied physics-ext IDs corresponding to selectedCards ordinals 50-99. No first-nine root-reserved IDs, no 782 binding recalculation, no network access, no source interpretation or quality decision.','scopeCheckpoint':'current-checkpoint.json was not present under searched /tmp or accessible Mindbattle worktree; scope ID set supplied verbatim by requester. Source URL mapping read only from author-original-edition11.json all80ProtectedPreimage ID+source.url fields.','sourcePacket':{'path':str(SRC),'bytes':SRC.stat().st_size,'sha256':sha(SRC.read_bytes())},'inventorySearch':{'manifestCount':1593,'roots':['/Users/eaafonasev/Projects/mindbattle/docs/content-audits','/Users/eaafonasev/.codex/worktrees','/tmp/mindbattle* and matching physics/question-quality capture directories'],'method':'Exact URL matches in capture manifests only; full capture required an existing body, raw response headers, manifest, and verifiable body/header hashes. Pinned range entities required complete manifest and verified every range body/header hash.','uniqueScopeURLs':len(url_rows),'matchedExactFullCaptureURLs':len(found),'entriesCovered':sum(x['captureStatus']=='EXACT_FULL_CAPTURE_FOUND' for x in entries),'entriesWithExactGaps':sum(x['captureStatus']!='EXACT_FULL_CAPTURE_FOUND' for x in entries)},'captureGroups':[{'sourceUrl':u,'coveredIds':url_rows[u],'capture':found[u][0]} for u in found],'entries':entries}
out=Path('/tmp/mindbattle-capture-01a1383a-d787-7fc0-921e-053e18541e25/physics-ext-50-99-existing-capture-index.json')
out.write_text(json.dumps(index,ensure_ascii=False,indent=2))
b=out.read_bytes();print('indexPath',out,'bytes',len(b),'sha256',sha(b),'ids',len(entries),'uniqueURLs',len(url_rows),'capturedURLs',len(found),'coveredIDs',index['inventorySearch']['entriesCovered'],'gaps',index['inventorySearch']['entriesWithExactGaps'])
for g in index['captureGroups']:print('CAPTURE',g['sourceUrl'],'IDs',','.join(g['coveredIds']),'body',g['capture']['bodyBytes'],g['capture']['bodySHA256'],'manifest',g['capture']['manifestPath'])
print('GAP_IDS',' '.join(x['id'] for x in entries if x['captureStatus']!='EXACT_FULL_CAPTURE_FOUND'))
