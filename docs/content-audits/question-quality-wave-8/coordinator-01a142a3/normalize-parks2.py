"""Mechanical normalization of exact SOURCE packet and literal grammar ACK; no credit."""
import pathlib,importlib.util,json,copy
D=pathlib.Path(__file__).parent;C=D.parents[3]
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('owned',D/'owned-tools.py');S=D.parent/'process-v2-parks-repair-002-01a141dd/author';B=D/'qualified-parks2-source62';B.mkdir(exist_ok=True);assert {p.name for p in B.iterdir()} <= {'candidate.json','sourceproof.json','peer-snapshot.json'}
a=m.read(S/'candidate.json');sp=m.read(S/'sourceproof.json');ps=m.read(S/'peer-snapshot.json');ack=m.read(S/'note1-grammar-ack.json');e=a['entries'][0];p=sp['entries'][0];c=e['proposedCard'];old=c['answers'][1]['note'];c['answers'][1]['note']=ack['triple']['note'];assert ack['triple']=={'prompt':c['prompt'],'answer':c['answers'][1]['text'],'note':c['answers'][1]['note']};assert m.sha(ack['triple'])==ack['canonicalSHA256'];e['afterHash']=m.sha(c)
raw=D.parent/'coordinator-01a141dd/source-captures/source62-parks2-original-opened-nps-contexts.json';rp=str(raw.relative_to(C));assert m.raw(raw)=='f27f891c685f5e0cef3071c19700e74a00aed7425b077612c4c912a83daaef03';rawText=raw.read_text()
originalRaw=copy.deepcopy(sp['rawSources'])
assert all(s['url'] in rawText for s in originalRaw)
sp['rawSources']=[{'path':rp,'sha256':m.raw(raw),'url':originalRaw[0]['url'],'additionalURLs':[s['url'] for s in originalRaw[1:]],'locator':'Original complete rendered SOURCE NPS outputs; preserve per-group and per-variant precise locators.','readProvenance':'Original full opened web outputs personally read by SOURCE01a14262-8bca; exact journal capture preserved by predecessor. No paraphrase raw used.','originalSourceRecords':originalRaw}]
before=e['beforeCard'];bg={'prompt_ordered_answers_key':{'prompt':before['prompt'],'answers':[v['text'] for v in before['answers']],'correctIndex':before['correctIndex']},'explanation':before['explanation'],**{'note'+str(k):v['note'] for k,v in enumerate(before['answers'])}}
for g in p['literalGroups']:
 g['sourcePaths']=[rp]
 if g['group']=='note1':
  assert g['literal']==old;g['literal']=c['answers'][1]['note'];g['literalSHA256']=m.sha(g['literal'])
 g['literalSHA256']=m.sha(g['literal']);e['fieldGroups'][g['group']]={'beforeCanonicalSHA256':m.sha(bg[g['group']]),'afterCanonicalSHA256':g['literalSHA256']}
for v in p['fourFullPromptAnswerNoteAssessments']:
 v['sourcePaths']=[rp]
 if 'plausibilityUniqueKeyAndNoteTruthfulness' in v:v['plausibilityUniqueKeyAndNoteTruthUsefulness']=v.pop('plausibilityUniqueKeyAndNoteTruthfulness')
 if v['slot']==1:
  assert v['note']==old;v['note']=c['answers'][1]['note'];v['grammar']=ack['grammarAssessment'];v['tripleSHA256']=ack['canonicalSHA256']
for v in p['fourFullPromptAnswerNoteAssessments']:
 assert v['fullPrompt']==c['prompt'] and v['answer']==c['answers'][v['slot']]['text'] and v['note']==c['answers'][v['slot']]['note'];v['tripleSHA256']=m.sha({'prompt':v['fullPrompt'],'answer':v['answer'],'note':v['note']})
if p['correctNoteNewFact'].get('fact')==old:p['correctNoteNewFact']['fact']=c['answers'][1]['note']
# Preserve exact full peers and bilateral SOURCE judgments; resolve real topic by ID and card.
for peers in [ps['actualCurrentPeers'],p.get('actualCurrentPeers',[])]:
 for peer in peers:
  matches=[]
  for f in (C/'src/content/topics').glob('*.json'):
   for q in m.read(f)['questions']:
    if q['id']==peer['id']:matches.append((f.stem,q))
  assert len(matches)==1 and matches[0][1]==peer['card'];peer['topicId']=matches[0][0]
  peer['sha256']=peer.get('sha256',peer.get('canonicalSHA256'));assert peer['sha256']==m.sha(peer['card'])
for obj in [a,sp,ps]:obj['rootNormalization']={'coordinator':m.O,'originalPacket':str(S.relative_to(C)),'originalFreeze':'f6eecc30db3d852faa662ee6e15a5bb4db147fe1','grammarAck':str((S/'note1-grammar-ack.json').relative_to(C)),'grammarAckFreeze':'280fa64f293995924c01025b5008708fa44565b7','transformations':['Exact SOURCE acknowledged note1 literal and dependent hashes; canonical JSON string quoting repaired for all group hashes with unchanged literals','Absent per-page raw paths replaced by original full SOURCE capture composite; exact URLs and locators retained','Assessment field alias normalized without changing judgments','Full actual peer topic and sha256 normalized by ID/fullcard'],'semanticRootEdits':False,'qualityCredit':0}
for n,x in [('candidate.json',a),('sourceproof.json',sp),('peer-snapshot.json',ps)]:m.write(B/n,x)
app=load('standard',C/'docs/content-audits/question-quality-wave-7/coordinator-01a13e5e/apply-standard.py');app.P=m.P
r=app.apply(B,'01a14262-8bca-7a42-9ef8-31c73fb38274',[2],D/'apply-parks2.json',D/'qa-book69-parks2.json',pathlib.Path(__file__),qualifyOnly=True);m.write(D/'qualification-parks2.json',{'qualified':True,'groups':len(r['finalGroupBindings']),'variants':len(r['finalVariantBindings']),'qualityCredit':0})
print('sourceFreeze',m.savecode([pathlib.Path(__file__),D/'qualification-parks2.json']+list(B.iterdir()),'Freeze mechanically normalized SOURCE park2 exact grammar ACK and full primary capture'))
