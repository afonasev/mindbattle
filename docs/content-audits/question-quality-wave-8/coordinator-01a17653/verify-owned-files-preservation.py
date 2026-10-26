"""Verify owned files against private HEAD and only the configured canonical checkpoint."""
from pathlib import Path
import importlib.util,json,subprocess,sys,datetime
D=Path(__file__).parent
s=importlib.util.spec_from_file_location('m',D/'owned-tools.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
x=m.read(D/'manifest.json');C=m.C;P=m.P;head=m.h.git(C,'rev-parse','HEAD')
assert D==Path(m.read(Path(x['canonicalCheckpoint']))['currentManifest']).parent and D.parent==C/'docs/content-audits/question-quality-wave-8'
assert all(m.flow.get(cid)[1]['owner']==m.O for cid in x['claims']) and m.read(P/'.flow-leases.json')=={}
base=m.read(D/'takeover.json')['predecessorRemotePush']['commit']
topic='src/content/topics/'+x['activeRoute']['topicId']+'.json'
canonical=C/f"docs/content-audits/question-quality-wave-{x['activeRoute']['wave']}/root-certified-source-checkpoint.json"
assert Path(x['activeRoute']['sourceCheckpoint'])==canonical
allowed={topic,str(canonical.relative_to(C))}
recovery_metadata={}
binding=D/'recovery-release-binding.json'
if binding.is_file():
 recovery=m.read(binding);auth=m.read(Path(recovery['authorization']))
 assert recovery['owner']==auth['owner']==m.O
 assert recovery['predecessor']==auth['predecessor']==m.read(Path(x['predecessorHandoff']))['rootNativeAudit']['threadId']
 prior=Path(x['predecessorHandoff']).parent
 exact={str((prior/n).relative_to(C)) for n in ['manifest.json','handoff-next.json']}
 assert set(recovery['exactPredecessorMetadata'])==exact
 for rel,digest in recovery['exactPredecessorMetadata'].items():
  p=C/rel;assert m.raw(p)==digest
  assert p.read_bytes()==subprocess.check_output(['git','-C',str(C),'show',recovery['supportedReleaseCode']+':'+rel])
  assert p.read_bytes()==subprocess.check_output(['git','-C',str(C),'show',head+':'+rel])
  recovery_metadata[rel]=digest
 allowed.update(exact)
changed=m.h.git(C,'diff','--name-only',base,head).splitlines()
prefix=str(D.relative_to(C))+'/'
assert all(p.startswith(prefix) or p in allowed for p in changed),[p for p in changed if not p.startswith(prefix) and p not in allowed]
bindings={}
for p in sorted(D.rglob('*')):
 assert not p.is_symlink(),str(p)
 if not p.is_file():continue
 rel=str(p.relative_to(C))
 assert p.read_bytes()==subprocess.check_output(['git','-C',str(C),'show',head+':'+rel]),rel
 bindings[rel]=m.raw(p)
tracked=set(m.h.git(C,'ls-tree','-r','--name-only',head,'--',str(D.relative_to(C))).splitlines())
assert tracked==set(bindings),'Missing or untracked owned file'
cp=m.read(Path(x['canonicalCheckpoint']));reg=m.read(canonical)
accepted={v['questionId']:v['cardCanonicalSha256'] for v in cp['completedCardHashes']}
wave=next(w for w in cp['waves'] if w['changeId']==x['activeRoute']['waveChangeId'])
ids=[v['questionId'] for v in reg['cards']]
assert len(ids)==len(set(ids))==reg['sourceEditorialCompletedCards']==wave['currentSourceEditorialCards']
assert reg['sourceEditorialCompletedFields']==6*len(ids) and reg[f"wave{x['activeRoute']['wave']}Remaining"]==500-len(ids)
assert all(v['questionId'] in wave['selectedIds'] and accepted[v['questionId']]==v['cardCanonicalSha256'] for v in reg['cards'])
assert reg['latestBatch']['CURRENT']==x['CURRENT'] and reg['latestBatch']['remaining']==x['remaining']
assert reg['ownerNativeId']==m.O
for root,key in [(C,'code'),(P,'planning')]:
 assert m.raw(Path(m.h.git(root,'rev-parse','--path-format=absolute','--git-path','index')))==x['foreignIndexes'][key]
assert m.h.git(C,'rev-parse','HEAD')==head
out=D/'owned-files-preservation.json';assert not out.exists()
m.write(out,{'owner':m.O,'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'privateHeadBeforeReport':head,'comparisonUsesForeignIndex':False,'ownedFileCount':len(bindings),'ownedFileSHA256':bindings,'changedPathsSinceTakeover':changed,'scope':'Only ownedD, exact active topic, and exact configured root-certified source checkpoint','canonicalCheckpoint':{'path':str(canonical),'rawSHA256':m.raw(canonical),'uniqueCurrentCards':len(ids),'fields':6*len(ids),'allExactAcceptedHashes':True,'ownerNativeIdMeaning':'Historical last certificate writer, not a live claim; preserve through release/takeover'},'CURRENT':x['CURRENT'],'remaining':x['remaining'],'foreignIndexesUnchanged':x['foreignIndexes'],'ownTemporaryResources':x['owncleanupCurrentOwner']['temporaryResources'],'allOwnedAuthorsArchived':all(a.get('archived',False) for k,a in x['actors'].items() if k.startswith('author')),'worktreeRetainedForAuthorizedContinuation':str(C),'noForeignCleanup':True})
if recovery_metadata:
 result=m.read(out);result.update(authorizedPredecessorReleaseMetadata=recovery_metadata,recoveryBinding=str(binding),scope='Only ownedD, exact active topic/checkpoint and two exact human-authorized predecessor release metadata files frozen at recorded release commit');m.write(out,result)
print(m.savecode([out,Path(__file__)],'Preserve private-HEAD owned files and exact configured source checkpoint'))
print({'ownedFileCount':len(bindings),'canonicalUniqueCurrentCards':len(ids),'canonicalFields':6*len(ids),'foreignIndexUsedForSnapshot':False})
