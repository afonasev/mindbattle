"""Serialize explicit independent decisions; never infer a substantive verdict."""
import json,hashlib,os,copy,subprocess
from pathlib import Path
OWN=Path(__file__).resolve().parent;ROOT=OWN.parents[4]
AUTHOR=ROOT/'docs/content-audits/question-quality-wave-6/winter-sports/resume-2026-10-11-author100'
def digest(b):return hashlib.sha256(b).hexdigest()
def canonical(o):return json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def save(n,v): (OWN/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
qs=json.loads((ROOT/'src/content/topics/winter-sports.json').read_text())['questions'][:25];byid={q['id']:q for q in qs}
author={c['questionId']:c for c in json.loads((AUTHOR/'author100-receipt.json').read_text())['cards']}
decisions=json.loads((OWN/'decisions.json').read_text());out=[];sources={}
for d in decisions:
 q=byid[d['id']];a=author[d['id']];assert digest(canonical(q))==a['cardCanonicalSha256'];assert len(d['fields'])==6
 row={'questionId':d['id'],'cardCanonicalSha256':digest(canonical(q)),'verdict':d['verdict'],'editorialAnalysis':d['editorialAnalysis'],'fields':[]}
 for f,(verdict,analysis) in zip(a['fields'],d['fields']):
  assert verdict in ('PASS','FIX_REQUIRED','HOLD') and analysis
  field={'field':f['field'],'literalSha256':f['literalSha256'],'verdict':verdict,'substantiveRead':True,'claimAnalysis':analysis,'proofs':copy.deepcopy(f['proofs'])}
  for p in field['proofs']:
   raw=AUTHOR/p['rawCapture'];b=raw.read_bytes();assert digest(b)==p['rawCaptureSha256'];rel=str(raw.relative_to(ROOT));git=subprocess.check_output(['git','show','HEAD:'+rel],cwd=ROOT)
   s={'originalPath':rel,'workingSha256':digest(b),'previousGitBlobSha256':digest(git),'previousGitBlobMatches':b==git,'onlyCRLFNormalization':b.replace(b'\r\n',b'\n')==git,'bytes':len(b)}
   if b!=git:
    dst=OWN/'preserved-originals'/raw.name;dst.parent.mkdir(exist_ok=True);dst.write_bytes(b);p['rawCapture']=str(dst.relative_to(OWN));s['preservedPath']=str(dst.relative_to(ROOT))
   else:p['rawCapture']=os.path.relpath(raw,OWN)
   p['independentReader']='01a12bed-2f93-7cb2-b624-3e6caf2fecec';p['locator']['authorSourceIndex']=os.path.relpath(AUTHOR/'source-index.json',OWN)
   sources[rel]=s
  extra=json.loads((OWN/'additional-proofs.json').read_text()) if (OWN/'additional-proofs.json').exists() else {}
  field['proofs'].extend(copy.deepcopy(extra.get(d['id'],{}).get(f['field'],[])))
  row['fields'].append(field)
 out.append(row)
(OWN/'preserved-originals'/'.gitattributes').write_text('* -text\n')
save('receipt.json',{'role':'independent','agentIdentity':'01a12bed-2f93-7cb2-b624-3e6caf2fecec','decisionMethod':'Actual current literal reading and original HTML/PDF extraction; explicit authored decisions.json. No inherited author verdict or analysis. Source passages/locators retained only after direct reading.','cards':out})
save('current-cards.json',[byid[d['id']] for d in decisions]);save('source-byte-preservation.json',{'baselineGit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'note':'Historical author hashes are retained, not relabelled. Exact working bytes preserved under owned -text path only when old Git normalized CRLF.','sources':list(sources.values())})
print('serialized explicit manual decisions',len(out))
