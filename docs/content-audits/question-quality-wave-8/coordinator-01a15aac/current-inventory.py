"""Machine facts only; no semantic peer choice, judgment, or quality credit."""
import pathlib, json, hashlib, sys
C = pathlib.Path(__file__).resolve().parents[4]
topic_id, output = sys.argv[1:3]
out = pathlib.Path(output).resolve()
assert out.is_relative_to(C / 'docs/content-audits/question-quality-wave-8')
assert not out.exists(), 'Preserve original inventory; choose a new owned filename'
sha = lambda v: hashlib.sha256(json.dumps(v, ensure_ascii=False, sort_keys=True,
                                         separators=(',', ':')).encode()).hexdigest()
rows, files, topics = [], [], {}
for p in sorted((C / 'src/content/topics').glob('*.json')):
    t = json.loads(p.read_text())
    topics[t['id']] = t
    files.append({'path': str(p.relative_to(C)),
                  'sha256': hashlib.sha256(p.read_bytes()).hexdigest()})
    rows.extend({'topicId': t['id'], 'id': q['id'], 'prompt': q['prompt'],
                 'answers': [v['text'] for v in q['answers']],
                 'correctIndex': q['correctIndex']} for q in t['questions'])
assert len(files) == 110 and len(rows) == 11000
t = topics[topic_id]
assert len(t['questions']) == 100
tp = C / f'src/content/topics/{topic_id}.json'
value = {
    'purpose': 'Fresh deterministic facts; author must personally assess relevant whole peers',
    'globalMAIN': {'topicFileCount': len(files), 'questionCount': len(rows),
                   'rowsCanonicalSHA256': sha(rows),
                   'allCurrentFileByteBindings': files, 'rows': rows},
    'sameTopicMAIN': {'path': str(tp.relative_to(C)), 'topicId': topic_id,
                      'fileSHA256': hashlib.sha256(tp.read_bytes()).hexdigest(),
                      'questionCount': 100, 'questions': t['questions']},
    'actualCurrentPeers': [
        {'id': q['id'], 'topicId': topic_id, 'sourceOrder': k,
         'card': q, 'sha256': sha(q)} for k, q in enumerate(t['questions'], 1)]}
out.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'output': str(out), 'topicFiles': 110, 'MAINRows': 11000,
                  'topicCards': 100, 'qualityCredit': 0}))
