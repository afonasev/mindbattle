import subprocess,sys,json
from pathlib import Path
ROOT=Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle')
assert Path(subprocess.check_output(['git','rev-parse','--show-toplevel'],cwd=ROOT).decode().strip())==ROOT
OUT=ROOT/'docs/content-audits/question-quality-wave-6/independent-pilot/resume-2026-10-12-winter30-current'
mode=sys.argv[1];assert mode in ('staged','committed');files=[p for p in OUT.rglob('*') if p.is_file()];assert all('__pycache__' not in p.parts for p in files)
for p in files:
 rel=str(p.relative_to(ROOT));ref=':'+rel if mode=='staged' else 'HEAD:'+rel
 assert subprocess.check_output(['git','show',ref],cwd=ROOT)==p.read_bytes(),rel
assert (ROOT/'src/content/topics/winter-sports.json').read_bytes()==subprocess.check_output(['git','show','b31dc20:src/content/topics/winter-sports.json'],cwd=ROOT)
print(json.dumps({'mode':mode,'ownedFilesExactBytes':len(files),'topicEqualsFrozen':True,'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip(),'result':'PASS'}))
