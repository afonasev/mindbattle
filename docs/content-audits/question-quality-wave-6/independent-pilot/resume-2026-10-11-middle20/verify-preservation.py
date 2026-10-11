"""Mechanical preservation and source provenance inventory, not editorial judging."""
import hashlib
import json
import subprocess
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
def digest(data): return hashlib.sha256(data).hexdigest()
def canonical(value): return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()
freeze = json.loads((HERE / 'freeze.json').read_text())
receipt = json.loads((HERE / 'independent-current.json').read_text())
topic_path = 'src/content/topics/middle-ages.json'
current_topic = json.loads((REPO / topic_path).read_text())
author_topic = json.loads(subprocess.check_output(['git', 'show', '73d7174:' + topic_path], cwd=REPO))
current = {c['id']: c for c in current_topic['questions']}
author = {c['id']: c for c in author_topic['questions']}
errors = []; card_results = []; sources = {}
for frozen in freeze['snapshot']:
    qid = frozen['id']; now = current[qid]
    hashes = {label: digest(canonical(value)) for label, value in [('freeze', frozen), ('current', now), ('author73d7174', author[qid])]}
    if len(set(hashes.values())) != 1: errors.append(qid + ': frozen target changed')
    card_results.append({'questionId': qid, 'currentCardCanonicalSha256': hashes['current'], 'allThreeHashesMatch': len(set(hashes.values())) == 1})
for row in receipt['cards']:
    for field in row['fields']:
        for p in field['proofs']:
            raw = (HERE / p['rawCapture']).resolve(); relative = str(raw.relative_to(REPO))
            if relative not in sources:
                tracked = subprocess.run(['git', 'ls-files', '--error-unmatch', relative], cwd=REPO, capture_output=True).returncode == 0
                sources[relative] = {'sha256': digest(raw.read_bytes()), 'trackedInGit': tracked, 'url': p['url'], 'captureFormat': p['captureFormat'], 'captureMethod': p['captureMethod'], 'readLocators': []}
                if not tracked: errors.append('untracked source ' + relative)
            if sources[relative]['sha256'] != p['rawCaptureSha256']: errors.append('source hash changed ' + relative)
            if p['locator'] not in sources[relative]['readLocators']: sources[relative]['readLocators'].append(p['locator'])
quotas = Counter(c['difficulty'] for c in current_topic['questions'])
positions = {level: [sum(c['difficulty'] == level and c['correctIndex'] == i for c in current_topic['questions']) for i in range(4)] for level in ('easy', 'medium', 'hard')}
expected_positions = {'easy': [10]*4, 'medium': [10]*4, 'hard': [5]*4}
if dict(quotas) != {'easy': 40, 'medium': 40, 'hard': 20}: errors.append('topic quota mismatch')
if positions != expected_positions: errors.append('topic position mismatch')
if [c['id'] for c in current_topic['questions']] != [c['id'] for c in author_topic['questions']]: errors.append('topic ID/order mismatch')
for c in current_topic['questions']:
    if (c['difficulty'], c['correctIndex']) != (author[c['id']]['difficulty'], author[c['id']]['correctIndex']): errors.append(c['id'] + ': immutable difficulty/index changed')
result = {'role': 'independent', 'agentIdentity': freeze['agentIdentity'], 'baseline': '73d7174',
          'targetCardCount': len(card_results), 'cardHashes': card_results,
          'topicQuotas': dict(quotas), 'topicCorrectPositions': positions,
          'sourceInventory': sources, 'sourcesReadAs': 'Full original captures with substantive article passages and context read; source inventory locators identify the actual claim-bearing sections. Original raw Stanford responses separately audited. No Oxford malformed PDF, challenge, search snippet or author summary used as factual proof.',
          'cardVerdicts': dict(Counter(c['verdict'] for c in receipt['cards'])),
          'fieldVerdicts': dict(Counter(f['verdict'] for c in receipt['cards'] for f in c['fields'])),
          'proofCount': sum(len(f['proofs']) for c in receipt['cards'] for f in c['fields']),
          'mechanicalErrors': errors, 'newCertifiedCards': 0,
          'limits': 'Reports existing manually assigned verdicts; creates no PASS. Coordinator alone decides dual-role credit. Other IDs are not substantively re-audited.'}
(HERE / 'preservation-and-source-inventory.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('sourceInventory', 'cardHashes', 'sourcesReadAs')}, ensure_ascii=False))
raise SystemExit(bool(errors))
