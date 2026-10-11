#!/usr/bin/env python3
"""Focused evidence contract and optional committed-byte roundtrip."""
import hashlib,json,subprocess,sys
from pathlib import Path
root=Path(__file__).resolve().parent; rel=root.relative_to(Path.cwd()).as_posix()
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def git(*args):return subprocess.check_output(['git',*args])
r=json.loads((root/'reader-receipt.json').read_bytes());c=r['cards'][0];f=r['frozenEvidenceCommit']
assert r['readerIdentity']==r['actualCODEX_THREAD_ID']!=r['authorIdentity']
assert r['scope']==['middle-ages-dower']
assert sha(canon(c['currentCard']))==c['cardCanonicalSha256']
assert json.loads((root/'frozen-card.json').read_bytes())==c['currentCard']
q=json.loads(git('show','HEAD:'+r['topicWitness']['path']))['questions']
current=next(v for v in q if v['id']==c['questionId'])
assert current==c['currentCard']
assert len(q)==100
protected={p['questionId']:p['canonicalSha256'] for p in r['protected']['cards']}
assert len(protected)==99
assert all(sha(canon(v))==protected[v['id']] for v in q if v['id']!=c['questionId'])
assert [x['field'] for x in c['fields']]==['prompt-key','note0','note1','note2','note3','explanation']
for x in c['fields']:
 b=canon(x['literalText']) if isinstance(x['literalText'],list) else x['literalText'].encode()
 assert sha(b)==x['literalSha256'] and x['substantiveRead'] and x['individualReaderAnalysis']
 for p in x['proofs']:
  b=Path(p['rawCapture']).read_bytes()
  assert sha(b)==p['rawCaptureSha256']
  assert sha(p['passage'].encode())==p['passageSha256']
  assert git('show',f+':'+p['originalPath'])==b
  text=(root/(Path(p['rawCapture']).name+'.reader-text.txt')).read_text()
  assert p['passage'] in text
for p in r['inputReceipts']:
 assert sha(git('show',p['commit']+':'+p['path']))==p['sha256']
 assert Path(p['path']).read_bytes()==git('show',p['commit']+':'+p['path'])
assert sum(x['sourceVerdict']=='PASS' for x in c['fields'])==6
assert sum(x['editorialVerdict']=='PASS' for x in c['fields'])==4
assert sum(x['editorialVerdict']=='FIX' for x in c['fields'])==2
report={'readerIdentity':r['readerIdentity'],'scope':r['scope'],'cardCanonicalSha256':c['cardCanonicalSha256'],'counts':r['counts'],'protected99Unchanged':True,'inputReceiptsAndOriginalsByteIdentical':True,'focusedContracts':'PASS'}
if len(sys.argv)>1:
 rev=sys.argv[1];rows=[]
 paths=git('ls-tree','-r','--name-only',rev,'--',rel).decode().splitlines()
 assert paths
 for p in paths:
  b=Path(p).read_bytes();committed=git('show',rev+':'+p);assert b==committed,p
  rows.append({'path':p,'byteCount':len(b),'workingSha256':sha(b),'committedSha256':sha(committed),'gitBlob':git('rev-parse',rev+':'+p).decode().strip(),'byteIdentical':True})
 report.update({'evidenceCommit':git('rev-parse',rev).decode().strip(),'verifiedFiles':rows,'method':'Exact git show committed blob bytes compared with working bytes for each owned evidence file. No text-normalized comparisons.'})
print(json.dumps(report,ensure_ascii=False,indent=2))
