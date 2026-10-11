"""Only validate explicit receipts against saved cards and Git originals. Never assign verdicts."""
import json,hashlib,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent;REPO=ROOT.parents[4]
def sha(b):return hashlib.sha256(b).hexdigest()
def canonical(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def gitblob(p):return subprocess.check_output(['git','show','HEAD:'+str(p.relative_to(REPO))],cwd=REPO)
labels=['winter25','winter25/repeat3','architecture50/batch01','architecture50/batch02','middle-serf-repeat1'];scope=json.loads((REPO/'docs/content-audits/question-quality-wave-6/coordinator-continuation-01a12c24/architecture-unread50-scope.json').read_text());scopehash={x['questionId']:x['cardCanonicalSha256'] for x in scope['cards']};raws={};rows=[];errors=[]
for label in labels:
 base=ROOT/label;receipt=json.loads((base/'receipt.json').read_text());snap={q['id']:q for q in json.loads((base/'current-cards.json').read_text())}
 assert receipt['role']=='independent' and receipt['agentIdentity']=='01a12c3f-d480-76f2-89bd-c49dcc5becfe'
 for c in receipt['cards']:
  q=snap[c['questionId']];assert sha(canonical(q))==c['cardCanonicalSha256'];assert len(c['fields'])==6
  if c['questionId'] in scopehash:assert scopehash[c['questionId']]==c['cardCanonicalSha256']
  author=json.loads((REPO/c['authorReceipt']).read_text());assert author['role']=='author' and author['agentIdentity']==c['authorIdentity']!=receipt['agentIdentity'];assert sha((REPO/c['authorReceipt']).read_bytes())==c['authorReceiptSha256'];assert (REPO/c['authorReceipt']).read_bytes()==gitblob(REPO/c['authorReceipt'])
  a=next(x for x in author['cards'] if x['questionId']==q['id']);assert a['cardCanonicalSha256']==c['cardCanonicalSha256']
  for f in c['fields']:
   assert f['substantiveRead'] and f['claimAnalysis'] and f['proofs'];n=f['field'];lit=canonical([q['prompt'],q['correctIndex'],q['answers'][q['correctIndex']]['text']]) if n=='prompt-key' else (q['explanation'] if n=='explanation' else q['answers'][int(n[-1])]['note']).encode();assert sha(lit)==f['literalSha256']
   for p in f['proofs']:
    raw=(base/p['rawCapture']).resolve();b=raw.read_bytes();assert sha(b)==p['rawCaptureSha256'] and b==gitblob(raw);assert sha(p['passage'].encode())==p['passageSha256'];raws[str(raw.relative_to(REPO))]=sha(b)
  topic=q['id'].split('-')[0] if q['id'].startswith('architecture-') else ('middle-ages' if q['id'].startswith('middle-ages-') else 'winter-sports');path=REPO/'src/content/topics'/f'{topic}.json';live=next(x for x in json.loads(path.read_text())['questions'] if x['id']==q['id']);committed=next(x for x in json.loads(gitblob(path))['questions'] if x['id']==q['id']);match=sha(canonical(live))==c['cardCanonicalSha256'];gitmatch=sha(canonical(committed))==c['cardCanonicalSha256']
  assert q['id']=='middle-ages-serf' or (match and gitmatch)
  rows.append({'questionId':q['id'],'reviewedHash':c['cardCanonicalSha256'],'currentDiskMatch':match,'currentGitMatch':gitmatch,'liveHash':sha(canonical(live)),'verdict':c['verdict']})
report={'rows':rows,'cards':len(rows),'fields':len(rows)*6,'rawOriginals':len(raws),'rawHashes':raws,'currentDiskMatches':sum(x['currentDiskMatch'] for x in rows),'currentGitMatches':sum(x['currentGitMatch'] for x in rows),'archScopeHashMatches':len(scopehash),'errors':errors,'newSubstantiveVerdicts':0,'note':'Old serf revision may be concurrently superseded; no certification of unseen new revision is inferred.'};(ROOT/'frozen-check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print({k:v for k,v in report.items() if k not in ['rows','rawHashes']})
