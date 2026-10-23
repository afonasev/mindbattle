import copy, hashlib, json, pathlib
C = pathlib.Path('/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle')
ROOT = C / 'docs/content-audits/question-quality-wave-8/coordinator-01a16a43'
OUT = ROOT / 'source-human-medicine78-cycle1'
OLD = ROOT / 'source-human-medicine78'
INV = OUT / 'fresh-inventory.json'
NATIVE = '01a16a76-4a35-7b81-94e8-0204db5d83ca'
TOPIC = 'human-medicine'
QID = 'human-medicine-ext-digestion-stomach'
CYCLE = 1
STATUS = 'READY_FOR_SAME_READER_FINAL'

def canon(v): return json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')
def sha(v): return hashlib.sha256(canon(v)).hexdigest()
def file_sha(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def write(n, v): (OUT/n).write_text(json.dumps(v, ensure_ascii=False, indent=2)+'\n')
def groups(card):
    return {'prompt_ordered_answers_key': {'prompt':card['prompt'],'answers':[a['text'] for a in card['answers']],'correctIndex':card['correctIndex']},
            'explanation':card['explanation'], **{'note'+str(i):a['note'] for i,a in enumerate(card['answers'])}}

fresh = json.loads(INV.read_text())
old_candidate = json.loads((OLD/'candidate.json').read_text())
old_sourceproof = json.loads((OLD/'sourceproof.json').read_text())
old_peers = json.loads((OLD/'peer-snapshot.json').read_text())
current_questions = fresh['sameTopicMAIN']['questions']
source_order = next(i for i,q in enumerate(current_questions,1) if q['id']==QID)
before = copy.deepcopy(current_questions[source_order-1])
assert sha(before) == '6fbc3a06dc6291f227e521fbcb75237d5d4565717f47866f69d5f56e2d9f1edc'
assert before == old_candidate['entries'][0]['proposedCard']
assert source_order == 78 and before['difficulty']=='easy' and before['correctIndex']==2
proposed = copy.deepcopy(before)
proposed['prompt'] = proposed['prompt'].replace('пищеварительного тракта', 'пищеварительной системы')
assert proposed['prompt'] == 'В каком органе пищеварительной системы пища перемешивается с кислым соком и начинается переваривание белков?'
assert [k for k in before if before[k] != proposed[k]] == ['prompt']

before_groups, after_groups = groups(before), groups(proposed)
field_groups = {n:{'beforeCanonicalSHA256':sha(before_groups[n]),'afterCanonicalSHA256':sha(after_groups[n])} for n in before_groups}
candidate = {
 'sourceNativeId':NATIVE,'topicId':TOPIC,'cycle':CYCLE,
 'entries':[{'id':QID,'topicId':TOPIC,'sourceOrder':source_order,'status':STATUS,
             'beforeCard':before,'beforeHash':sha(before),'proposedCard':proposed,'afterHash':sha(proposed),'fieldGroups':field_groups}],
 'qualityCredit':0,
}
write('candidate.json',candidate)

proof = copy.deepcopy(old_sourceproof)
proof['sourceNativeId']=NATIVE; proof['topicId']=TOPIC; proof['cycle']=CYCLE; proof['id']=QID; proof['qualityCredit']=0
entry = proof['entries'][0]
entry['status']=STATUS
literal_values=after_groups
for item in entry['literalGroups']:
    name=item['group']; item['literal']=literal_values[name]; item['literalSHA256']=sha(literal_values[name])
    if name=='prompt_ordered_answers_key':
        item['primaryGround'] = 'Заданный класс «орган пищеварительной системы» охватывает все четыре органа: пищевод и желудок относятся к пищеварительному тракту (23.3 L31,L143-L159; 23.4 L31-L36), а печень и поджелудочная железа прямо названы вспомогательными органами пищеварения (23.6 L31-L35,L64-L75). Уникальный функциональный ключ остаётся желудком: пища смешивается с желудочными соками (23.4 L35,L102), а HCl и пепсин начинают расщепление белков (L50-L52,L110).'
for i,v in enumerate(entry['fourFullPromptAnswerNoteAssessments']):
    v['fullPrompt']=proposed['prompt']
    triple={'prompt':proposed['prompt'],'answer':v['answer'],'note':v['note']}
    v['tripleSHA256']=sha(triple)
    # Keep the existing plausibility, key, truth, usefulness and locator judgments verbatim;
    # update only the grammar/category statement for the corrected prompt.
    old_assessment=v['plausibilityUniqueKeyAndNoteTruthUsefulness']
    tail=old_assessment.split(' Правдоподобие:',1)[1]
    grammar='Грамматика: формулировка «В каком органе пищеварительной системы…?» задаёт категорию, включающую все четыре органа; все четыре ответа согласованно даны как краткие именительные подписи органов.'
    v['grammar']=grammar.replace('Грамматика: ','')
    v['plausibilityUniqueKeyAndNoteTruthUsefulness']=grammar+' Правдоподобие:'+tail
# These are unchanged from the authored INITIAL evidence; the prompt phrase alone was corrected.
assert entry['correctNoteNewFact']==old_sourceproof['entries'][0]['correctNoteNewFact']
assert entry['absoluteDifficulty']==old_sourceproof['entries'][0]['absoluteDifficulty']
write('sourceproof.json',proof)

# Refresh all machine snapshots from this cycle's newly generated inventory.
old_relevant={p['id']:p for p in old_peers['relevantSameTopicPeers']}
relevant_same=[]
for old_peer in old_peers['relevantSameTopicPeers']:
    q=next(q for q in current_questions if q['id']==old_peer['id'])
    order=next(i for i,x in enumerate(current_questions,1) if x['id']==q['id'])
    relevant_same.append({'id':q['id'],'topicId':TOPIC,'sourceOrder':order,'card':copy.deepcopy(q),'sha256':sha(q),
                          'existingToProposedMAIN':old_peer['existingToProposedMAIN'],
                          'proposedToExistingMAIN':old_peer['proposedToExistingMAIN']})
actual=[{'id':q['id'],'topicId':TOPIC,'sourceOrder':i,'card':copy.deepcopy(q),'sha256':sha(q)} for i,q in enumerate(current_questions,1)]
cross=[]
for old_peer in old_peers['relevantCrossTopicPeers']:
    topic=old_peer['topicId']; qid=old_peer['id']
    t=json.loads((C/f'src/content/topics/{topic}.json').read_text())
    q=next(q for q in t['questions'] if q['id']==qid)
    order=next(i for i,x in enumerate(t['questions'],1) if x['id']==qid)
    cross.append({'id':qid,'topicId':topic,'sourceOrder':order,'card':q,'sha256':sha(q),
                  'existingToProposedMAIN':old_peer['existingToProposedMAIN'],
                  'proposedToExistingMAIN':old_peer['proposedToExistingMAIN']})
peers=copy.deepcopy(old_peers)
peers['sourceNativeId']=NATIVE; peers['topicId']=TOPIC; peers['cycle']=CYCLE
peers['globalMAIN']=fresh['globalMAIN']; peers['sameTopicMAIN']=fresh['sameTopicMAIN']
peers['actualCurrentPeers']=actual; peers['relevantSameTopicPeers']=relevant_same; peers['relevantCrossTopicPeers']=cross
peers['inventoryBinding']={'path':str(INV),'fileSHA256':file_sha(INV),'globalMAINRowsCanonicalSHA256':fresh['globalMAIN']['rowsCanonicalSHA256'],'sameTopicFileSHA256':fresh['sameTopicMAIN']['fileSHA256']}
peers['qualityCredit']=0
write('peer-snapshot.json',peers)

# Author-packet binding and preservation assertions, not catalog QA.
assert candidate['sourceNativeId']==proof['sourceNativeId']==peers['sourceNativeId']==NATIVE
assert candidate['topicId']==proof['topicId']==peers['topicId']==TOPIC
assert candidate['cycle']==proof['cycle']==peers['cycle']==1
assert candidate['entries'][0]['beforeHash']=='6fbc3a06dc6291f227e521fbcb75237d5d4565717f47866f69d5f56e2d9f1edc'
assert candidate['entries'][0]['afterHash']==sha(proposed)
assert len(entry['literalGroups'])==6 and len(entry['fourFullPromptAnswerNoteAssessments'])==4
assert len(actual)==100 and len(fresh['globalMAIN']['rows'])==11000
assert actual[source_order-1]['sha256']==candidate['entries'][0]['beforeHash']
assert all(pathlib.Path(s['path']).is_file() and file_sha(s['path'])==s['sha256'] for s in proof['rawSources'])
print(json.dumps({'status':STATUS,'id':QID,'sourceOrder':source_order,'beforeHash':sha(before),'afterHash':sha(proposed),'onlyChangedCardField':'prompt','sameTopicPeers':len(relevant_same),'crossTopicPeers':len(cross),'MAINRows':len(fresh['globalMAIN']['rows']),'qualityCredit':0},ensure_ascii=False))
