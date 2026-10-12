import json,hashlib,subprocess,os,re
from pathlib import Path
from html.parser import HTMLParser
ROOT='/Users/eaafonasev/.codex/worktrees/question-quality-wave6-01a12b0f/mindbattle'
assert subprocess.check_output(['git','rev-parse','--show-toplevel'],text=True).strip()==ROOT
OUT=Path(__file__).parent
AUTHOR='docs/content-audits/question-quality-wave-6/winter-sports/resume-2026-10-12-last15-fresh-first5/repair059067/author-source-editorial-review-corrected.json'
TOPIC='src/content/topics/winter-sports.json';FREEZE='6b60a7b';RUNTIME='3b33ae4'
sha=lambda b:hashlib.sha256(b).hexdigest()
can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
nat=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=False,separators=(',',':')).encode()
git=lambda ref,p:subprocess.check_output(['git','show',ref+':'+p])
a=json.loads(Path(AUTHOR).read_bytes());assert Path(AUTHOR).read_bytes()==git(FREEZE,AUTHOR)
scope=['winter-sports-059','winter-sports-067']
loadcards=lambda b:{c['id']:c for c in json.loads(b)['questions']}
frozen=loadcards(git(RUNTIME,TOPIC));working=loadcards(Path(TOPIC).read_bytes());head=loadcards(git('HEAD',TOPIC));baseline=loadcards(git(a['runtimeBaselineCommit'],TOPIC))
assert all(frozen[k]==working[k]==head[k]==a['cards'][k]['nativeCardLiteral'] for k in scope)
protected=[k for k in baseline if k not in scope];assert len(protected)==98
assert all(baseline[k]==frozen[k] for k in protected)
class H(HTMLParser):
 def __init__(self):super().__init__();self.nodes=[];self.skip=0
 def handle_starttag(self,t,a):
  if t in ('script','style'):self.skip+=1
 def handle_endtag(self,t):
  if t in ('script','style'):self.skip-=1
 def handle_data(self,s):
  if not self.skip and s.strip():self.nodes.append(s.strip())
raws={};sources=[];contexts=[]
for name,m in a['originalSourceCaptures'].items():
 b=Path(m['path']).read_bytes();assert b==git(FREEZE,m['path'])==git('HEAD',m['path']);assert sha(b)==m['sha256'];blob=subprocess.check_output(['git','hash-object',m['path']],text=True).strip();assert blob==m['gitBlobSha1'];raws[name]=b
 rec={'path':m['path'],'originalURL':m['url'],'captureURL':m['url'],'URLBasis':'Preserved direct-resource capture register; no substituted live fetch or inferred redirect URL.','SHA256':sha(b),'GitBlobSHA1':blob,'bytes':len(b),'durableAt':FREEZE,'diskFreezeHEADEqual':True,'readExtent':'Integrity only; no new PDF reading or PDF-derived quote' if name.endswith('.pdf') else 'Full relevant HTML entries and surrounding contexts personally read'};sources.append(rec)
 if name.endswith('.html'):
  h=H();h.feed(b.decode());ranges=[(60,98)] if name=='long-track.html' else [(78,95),(114,130),(165,174),(192,205),(215,228)]
  contexts.append({'source':rec,'parserRecipe':'HTMLParser convert_charrefs=True, omit script/style data, strip each nonempty data node; node indices zero-based. Separate from raw byte locators.','nodes':[{'index0':i,'text':h.nodes[i],'UTF8SHA256':sha(h.nodes[i].encode())} for l,r in ranges for i in range(l,r)]})
(OUT/'html-independent-context.json').write_text(json.dumps(contexts,ensure_ascii=False,indent=2)+'\n')
def quote(name,start,stop):
 b=raws[name];p=start.encode();assert b.count(p)==1;s=b.index(p);e=b.index(stop.encode(),s);q=b[s:e];m=next(x for x in sources if x['path'].endswith('/'+name))
 return {'source':m,'rawByteOffset0':s,'rawByteLength':e-s,'HTMLLine1':b[:s].count(b'\n')+1,'exactRawHTMLQuote':q.decode(),'quoteSHA256':sha(q),'recipe':'Exact UTF8 raw HTML byte slice; tags/entities retained. No collapsed PDF text or Unicode-codepoint offset.'}
Q={
 'long':quote('long-track.html','In the individual distance events,','</p>'),
 'plus':quote('iihf-terminology.html','Individual player statistic accounting','<br />'),
 'empty':quote('iihf-terminology.html','Goal scored against a team that has pulled','<br />'),
 'pull':quote('iihf-terminology.html','Tactic that may be employed by the trailing','<br />'),
 'game':quote('iihf-terminology.html','A game is a competition between','<br />'),
 'short':quote('iihf-terminology.html','When a team is short of one or more','<br />')}
S=[
 'COC describes counterclockwise travel and lane exchange together, without a direction dependent on lane, race distance or crossing.',
 'Full individual-distance paragraph supports direction, exchange per lap for equal distance and conditional outside-lane priority.',
 'COC says pairs exchange lanes per lap to equalize distance while travelling counterclockwise. Lane assignment changes, route direction does not.',
 'The complete paragraph explicitly lists 500/1000/1500 metres with the same direction and per-lap exchange; not just the short direction quote.',
 'The outside-lane right-of-way is expressly conditional on simultaneous arrival at crossover.',
 'Exchange lanes and equalize distance are expressly stated together with counterclockwise travel. No reversal claimed.',
 'The full IIHF plus/minus entry expressly excludes power-play team goals. Even-strength and even-strength overtime meet its stated condition. Empty-net is defined by goalkeeper withdrawal, which alone is not the power-play exclusion.',
 'Full Plus/Minus entry contains the on-ice and equal-strength wording, power-play exclusion and goalkeeper exclusion. The explanation faithfully attributes this terminology description.',
 'Full entry defines goals for/against at equal strength and assigns plus one/minus one. The author short exclusion quote alone would not prove this, so the whole entry is bound here.',
 'Empty-Net Goal and full Pulling entry support withdrawal, extra skater and tactic. Shorthanded defines penalty-created power play; goalkeeper withdrawal is not itself a penalty. Delayed-penalty use is also present and does not invalidate this distinction.',
 'Full entry directly excludes power-play goals and goalkeepers. The short-handed entry identifies power play for the opposing team.',
 'Game entry supplies optional overtime after regulation; Plus/Minus conditions are playing strength and on-ice participation, not period. The note retains the equal-strength condition and does not claim all overtime goals qualify.'
]
E=[
 'PASS easy: familiar direction fact; the three wrong choices offer lane-, distance- and crossing-dependent route hypotheses. Distinct misconceptions, no arithmetic or terminology shortcut. Not a reverse of 057, whose tested fact is event format.',
 'Clear explanation of course direction and relevant mechanics; retains simultaneous-arrival condition.',
 'Repair resolves the prior own-option FIX: the note gives why inside/outside assignment changes and distinguishes that from course direction, directly linked to the lane-dependent variant.',
 'Useful own-variant fact: actual distances vary while direction does not. More than a bare negation.',
 'Correct note adds conditional crossover priority beyond direction asked in prompt/key. Its presence also in explanation is permitted.',
 'Useful crossing-specific fact: the change is lane assignment for equal distance, not travel direction.',
 'PASS medium: knowledge of a hockey statistic is required to identify its exclusion. All alternatives are real goal situations; equal-strength versus empty-net versus power-play versus overtime are plausible competing bases for a statistic. No ratios or ordinary majority cue. Categories may overlap, but only power-play is the expressly excluded characteristic; an empty-net label alone implies no exclusion.',
 'Clear attributed definition and boundaries. It does not present the terminology entry as an exhaustive treatment of shorthanded goals or all statistical exceptions.',
 'Own-option useful fact: equal-strength goals count and their sign depends on which team scores. Does not merely state the keyed exclusion.',
 'Own-option useful fact: goalkeeper withdrawal supplies an extra skater and describes goal state. This is independent of penalty advantage and relates directly to empty-net variant.',
 'Correct note adds the separate goalkeeper exclusion beyond the asked type of team goal. Additional fact remains valid even though it also appears in explanation.',
 'Own-option useful fact: overtime follows regulation when needed; the timing category does not itself remove equal-strength goals from the metric. Conditional option is preserved.'
]
P=[['long']]*6+[['plus','empty','pull','short','game'],['plus'],['plus'],['empty','pull','short'],['plus','short'],['game','plus']]
rows=[]
for ci,k in enumerate(scope):
 c=frozen[k];ar=a['cards'][k];assert sha(can(c))==ar['nativeCardSha256'];fields=[]
 for fi,g in enumerate(['prompt-key','explanation','note0','note1','note2','note3']):
  lit={'prompt':c['prompt'],'ordered4OptionTexts':[z['text'] for z in c['answers']],'correctIndex':c['correctIndex'],'key':c['answers'][c['correctIndex']]['text']} if fi==0 else c['explanation'] if fi==1 else c['answers'][fi-2]['note']
  ag=next(z for z in ar['groups'] if z['group']==g);assert lit==ag['currentNativeLiteral'];assert sha(can(lit))==ag['literalSha256'];ix=ci*6+fi
  for b in ag['sourceQuoteBindings']:
   raw=Path(b['rawPath']).read_bytes();sl=raw[b['rawByteOffsetZeroBased']:b['rawByteOffsetZeroBased']+b['rawByteLength']];assert sl==b['quote'].encode();assert sha(sl)==b['quoteSha256Unchanged']
  fields.append({'field':g,'currentLiteral':lit,'canonicalJSONSHA256':sha(can(lit)),'insertionJSONSHA256':sha(nat(lit)),'sourceVerdict':'PASS','editorialVerdict':'PASS','manualSourceReason':S[ix],'manualEditorialReason':E[ix],'independentSourceProofs':[Q[t] for t in P[ix]]})
 rows.append({'id':k,'difficulty':c['difficulty'],'wholeSourceVerdict':'PASS','wholeEditorialVerdict':'PASS','wholeVerdict':'PASS','canonicalCardSHA256':sha(can(c)),'insertionCardSHA256':sha(nat(c)),'fields':fields})
partners=[]
for p in Path('src/content/topics').glob('*.json'):
 for c in json.loads(p.read_bytes())['questions']:
  if re.search(r'плюс.?минус|power.?play|гол в большинств|пуст\w* ворот|против часовой|по часовой',c['prompt']+' '+c['answers'][c['correctIndex']]['text'],re.I) or c['id']=='winter-sports-057':partners.append({'topic':str(p),'id':c['id'],'prompt':c['prompt'],'key':c['answers'][c['correctIndex']]['text'],'canonicalCardSHA256':sha(can(c))})
spec=Path('/Users/eaafonasev/Projects/mindbattle-planning/docs/GAME_SPEC.md').read_text().splitlines()
reader=os.environ['CODEX_THREAD_ID'];assert reader=='01a12f3d-8ec1-78b3-b153-5f2a62967421';assert a['authorIdentity']=='01a12fdb-8151-7890-9f51-8232f5f56bc2';assert reader!=a['authorIdentity']
r={'recordType':'Independent personal source and editorial reread of current repaired whole12','readerIdentity':reader,'identityBasis':'Actual CODEX_THREAD_ID matched coordinator trusted native reader ID; no model override, chat creation or delegation.','authorIdentity':a['authorIdentity'],'authorReceipt':AUTHOR,'authorFreeze':FREEZE,'authorReceiptSHA256':sha(Path(AUTHOR).read_bytes()),'runtimeFreeze':RUNTIME,'scope':scope,'cards':rows,'sources':sources,'htmlContextFile':'html-independent-context.json','sourceReadExtent':'All current12 groups and all8 option texts/key personally read; full relevant original HTML event/glossary entries including nearby caveats. Four original source files byte/SHA/blob verified. Two PDFs integrity-only in this repair, no new PDF content or PDF quote claim.','approvedRules':[{'path':'/Users/eaafonasev/Projects/mindbattle-planning/docs/GAME_SPEC.md','line1':n,'quote':spec[n-1]} for n in (138,139,143,144)],'duplicateEvidence':{'partners':partners,'analysis':'067 tests which goals count toward individual statistics; 068 tests the name of a goal following goalkeeper withdrawal. Reuse of an option or source is not a direct/reverse association duplicate. 059 tests course direction, 057 tests event format. Other matching clockwise/card pairs test unrelated facts. No sourcecount credit or neighbouring edits.'},'hashRecipes':{'canonical':'SHA256 UTF8 json.dumps ensure_ascii=False sort_keys=True separators comma/colon; scalar strings include JSONquotes.','insertion':'Same sort_keys=False.','HTML':'Exact raw captured HTML bytes, not PDF-collapsed Unicode text.'},'sourceLimitAnnotation':'IIHF terminology description is simplified, especially equal-strength wording. This card expressly asks what this entry excludes, not exhaustive all-goal statistical eligibility. Do not infer that all shorthanded or empty-net goals are excluded; categories can overlap with a power play.','guards':{'whole12CurrentDiskRuntimeHEADAuthorEquality':True,'protected98RuntimeBaselineEquality':True,'protected98CurrentChangedIds':[k for k in protected if working[k]!=baseline[k]],'all4OriginalSHAandBlobDiskFreezeHEADEquality':True,'allAuthorQuoteByteSlicesAndSHAVerified':True,'scopeDefinitionCommit':a['scopeGitCommit'],'scopeProvenanceCorrectionRetained':a['scopeProvenanceCorrection'],'runtimeSourceAuthorPlanningReviewhashCounterMutations':0,'counterIncrement':0},'summary':{'groups':12,'source':{'PASS':12,'FIX':0,'HOLD':0},'editorial':{'PASS':12,'FIX':0,'HOLD':0},'whole':{'PASS':2,'FIX':0,'HOLD':0}},'checks':'Scoped JSON/current-card literals and all12 canonical hashes; raw-source disk/freeze/HEAD bytes SHA/blob; author quote offsets plus own full-context byte proofs; preserved98/runtime baseline; duplicate candidate comparison. No tests/fullQA/build/browsergame/deploy/acceptance.','cleanup':{'ownedTemporaryProcesses':0,'ownedTemporaryFiles':0,'ownedUntrackedIgnoredAfterCommitExpected':0,'foreignChangesAndIndexPreserved':True,'retainedEvidence':'This helper, current2 native snapshots, original-byte source proof and personally read HTML contexts, all Git durable.'},'nextStep':'Coordinator evaluates paired first5 receipts. Reader stops after own commit and cleanup. Remaining10 held pending coordinator authorization; no reader counter increment.'}
(OUT/'reader-receipt.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');(OUT/'current2-canonical.json').write_bytes(can([frozen[k] for k in scope])+b'\n');(OUT/'current2-insertion.json').write_bytes(nat([frozen[k] for k in scope])+b'\n')
print(r['summary']);print([(x['id'],x['canonicalCardSHA256']) for x in rows])
