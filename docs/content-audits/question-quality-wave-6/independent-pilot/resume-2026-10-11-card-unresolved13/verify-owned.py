"""Bounded preservation/provenance checks. Does not generate editorial verdicts."""
import hashlib,json,re,subprocess
from collections import Counter
from pathlib import Path
P=Path(__file__).resolve().parent
R=P.parents[4]
A=R/'docs/content-audits/question-quality-wave-6/card-games/resume-2026-10-11-unresolved13'
def sha(x):return hashlib.sha256(x).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def git(*args):return subprocess.check_output(['git',*args],cwd=R)
checks={}
raw=(R/'src/content/topics/card-games.json').read_bytes()
frozen=git('show','e2ac59d:src/content/topics/card-games.json')
checks['entire100CardTopicByteIdenticalToFrozenAuthor']=raw==frozen
checks['topicSha256']=sha(raw)
t=json.loads(raw);r=json.loads((P/'independent13.json').read_text());author=json.loads((A/'author13.json').read_text())
checks['distinctReaders']=r['agentIdentity']!=author['agentIdentity']
checks['actualThreadMatchesReceipt']=r['agentIdentity']==__import__('os').environ['CODEX_THREAD_ID']
checks['manifestExact']=set(c['questionId'] for c in r['cards'])==set(json.loads((A/'manifest.json').read_text())['ids'])
checks['all13AuthorHashesMatch']=all(c['cardCanonicalSha256']==next(x['cardCanonicalSha256'] for x in author['cards'] if x['questionId']==c['questionId']) for c in r['cards'])
checks['pilotPreservedInFull']=json.loads((P/'pilot5.json').read_text())['cards']==r['cards'][:5]
checks['fieldCount']=sum(len(c['fields']) for c in r['cards'])
checks['cardVerdicts']=dict(Counter(c['verdict'] for c in r['cards']))
checks['fieldVerdicts']=dict(Counter(f['verdict'] for c in r['cards'] for f in c['fields']))
checks['quota']=dict(Counter(c['difficulty'] for c in t['questions']))
checks['keyPositions']={level:[sum(c['difficulty']==level and c['correctIndex']==i for c in t['questions']) for i in range(4)] for level in ('easy','medium','hard')}
originals={}
for c in r['cards']:
 for f in c['fields']:
  for pr in f['proofs']:
   path=(P/pr['rawCapture']).resolve();rel=str(path.relative_to(R));b=path.read_bytes()
   tracked=bool(git('ls-files','--',rel).strip())
   originals[rel]={'sha256':sha(b),'bytes':len(b),'trackedInGit':tracked,'matchesBoundHash':sha(b)==pr['rawCaptureSha256'],'captureFormat':pr['captureFormat']}
checks['originals']=originals
checks['proofCount']=sum(len(f['proofs']) for c in r['cards'] for f in c['fields'])
checks['fullExtractions']={}
for stem in ('pokemon-asia','lorcana-it'):
 d=json.loads((A/'sources'/(stem+'-provenance.json')).read_text());responses=d.get('rawResponses',d.get('responses'));lines={};conflicts=[];hashes=[]
 for response in responses:
  b=(A/'sources'/response['path']).read_bytes();hashes.append(sha(b)==response['sha256'])
  for n,txt in re.findall(r'^L(\d+)(?:@P[\d-]+)?: ?([^\n]*)',b.decode(),re.M):
   n=int(n)
   if n in lines and lines[n]!=txt:conflicts.append(n)
   lines[n]=txt
 total=d.get('lines',d.get('originalLines'));missing=sorted(set(range(total))-set(lines))
 rebuilt='\n'.join(lines[n] for n in sorted(lines))+'\n'
 checks['fullExtractions'][stem]={'allResponseHashesMatch':all(hashes),'originalLineCount':total,'capturedLineCount':len(lines),'missing':missing,'conflicts':conflicts,'exactReconstruction':rebuilt==(A/'sources'/(stem+'-full-extracted.txt')).read_text()}
checks['newRootCertification']=0
checks['assertionsAllPass']=all(checks[k] for k in ('entire100CardTopicByteIdenticalToFrozenAuthor','distinctReaders','actualThreadMatchesReceipt','manifestExact','all13AuthorHashesMatch','pilotPreservedInFull')) and checks['fieldCount']==78 and all(v['trackedInGit'] and v['matchesBoundHash'] for v in originals.values()) and all(v['exactReconstruction'] and v['allResponseHashesMatch'] and not v['missing'] and not v['conflicts'] for v in checks['fullExtractions'].values())
(P/'preservation-provenance.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in checks.items() if k not in ('originals','fullExtractions')},ensure_ascii=False,indent=2))
assert checks['assertionsAllPass']
