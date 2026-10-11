import json,hashlib,subprocess,os
from pathlib import Path
OUT=Path(__file__).parent
REF='7ec5109'
AUTHOR='docs/content-audits/question-quality-wave-6/middle-ages/resume-2026-10-12-rework28/author-pilot4-repair-receipt.json'
TOPIC='src/content/topics/middle-ages.json'
def raw(p):return subprocess.check_output(['git','show',REF+':'+p])
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def dump(name,v):(OUT/name).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def witness(p):
 b=raw(p);return dict(path=p,commit=subprocess.check_output(['git','rev-parse',REF]).decode().strip(),gitBlob=subprocess.check_output(['git','rev-parse',REF+':'+p]).decode().strip(),rawSha256=sha(b),byteCount=len(b),workingBytesMatch=Path(p).read_bytes()==b)
# Values below are individual reader decisions; this code only binds literals and preserved byte provenance.
analysis={
 'precaria':[
  'TLFi HIST. DU DR. explicitly separates precaria (request) from precarium (fruit-bearing property granted to a protected dependent). The stem asks for the latter. Four bare Russian legal tenure terms are parallel; benefice is a plausible service grant, emphyteusis a plausible land-use right, allod a related ownership term. This exact Frankish terminology fits hard; no parenthesis singles out the key. Плодоносящее имущество is a literal but intelligible legal description of income-producing property.',
  'ALLEU defines inherited property free of obligations/redevances; Russian note accurately reports inheritance and feudal dues, specifically about allod, not a generic rejection.',
  'UC Davis full glossary fief (fee) calls benefice a grant of land or office in return for support and service. The note preserves both alternatives and obligation; useful fact about this distractor.',
  'EMPHYTEOSE TLFi defines cessible real right over land for annual payment; Academie9 expressly says jouissance sur la chose d’autrui. Thus alienability, use of another’s property and annual payment all have support; clear Russian note.',
  'PRECAIRE HIST. DU DR. describes modest or zero charges and no military obligations unlike benefice. These are extra legal facts beyond the granted-asset question/key; related precarial conveyance is named rather than conflated with the request.',
  'Two sentences explain the substantive source distinction between request and granted asset, and identify which the stem asks. Concise, clear, source-supported; overlaps note only where useful.'
 ],
 'dower':[
  'SOURCE PASS: DOUAIRE DR. ANC. explicitly defines usufruct on husband’s assets assigned at marriage with enjoyment if wife survives. EDITORIAL FIX at actual medium: prompt asks право пользования имуществом мужа; answer0 already defines itself as узуфрукт из имущества мужа, while other parenthetical definitions concern property brought into marriage or payment/gift for a bride. The gloss supplies the matching definition and excludes others without knowing douaire. Uniform parentheses do not remove this semantic cue. Keep medium/key slot; remove answer-defining cue and use plausible parallel marriage-property terms.',
  'DOUAIRE supports assignment at marriage and enjoyment only after survival of husband. Survival is an extra useful condition absent from prompt/key, so note passes even though explanatory overlap is allowed.',
  'DOT TLFi A says property a woman brings on marrying. This note is about the specified dot sense and the given distractor, supported and intelligible.',
  'Full UGR publisher page includes Spanish resumen and English abstract framing brideprice by purchase/exchange price. Note correctly attributes interpretation to Hughes and stays within abstract scope.',
  'UGR English abstract lists dowry given by groom in exchange for bride; Spanish resumen and keywords identify donacion propter nupcias. Note accurately describes that form. English label is a publisher rendering, not asserted to be original Latin.',
  'DOUAIRE contrasts usufruct assigned by husband with DOT brought into marriage; remaining options are bridal transfers per UGR. Two concise sentences give the key rationale. In-game answer cue is assigned to prompt-key, not counted again against explanation.'
 ],
 'dowry':[
  'UGR complete publisher abstract expressly describes medieval Mediterranean shift away from brideprice toward dowry. Key uniquely names the earlier system in Hughes’s scheme; parental dowry and groom donation are the two dowry forms the abstract discusses, douaire is a different use right. Although parental dowry is easily excluded, groom donation in exchange for bride is a plausible related misconception; distinguishing it from the named preceding system requires thematic knowledge. Therefore medium passes; not downgraded for allowing some narrowing.',
  'SOURCE PASS: purchase/exchange-price framing and movement toward dowry occur in the abstract. EDITORIAL FIX: correct note only restates brideprice as purchase/exchange (already supplied by Выкуп за невесту) and the transition already asked in prompt. It adds no useful extra fact about the correct option beyond prompt/key. This is the existing GAME_SPEC line143 rule, not a new requirement for every distractor to explain wrongness or a ban on note/explanation overlap. Add a supported extra fact about brideprice or reframe the question/note pair within the same fixed medium slot.',
  'UGR abstract says parents give one type of dowry; note correctly adds classification to this particular distractor. It does not claim full article was read.',
  'UGR abstract says groom gives another dowry type in exchange for bride; note states the useful classification, tied to this option. Specific source rendering in parentheses is identifiable though inelegant.',
  'DOUAIRE DR. ANC. supports wife’s usufruct and survival condition. Clear fact about this option, not generic negation.',
  'Two sentences correctly summarize shift and classify two dowry forms, then identify douaire as use of husband’s property. Sources cover all clauses; reading length and Russian constructions pass. Correct-note defect is not duplicated here.'
 ],
 'serf':[
  'TLFi HIST. DU MOY. AGE. defines a land-attached person whose goods/work belong to landowner. Russian stem preserves economic dependency and key correctly identifies familiar крепостной крестьянин. Easy allows familiar-definition reasoning; day worker, free tenant and freeholder are meaningful rural statuses, not absurd alternatives. Свободный is a useful narrowing clue but key itself does not echo dependency wording, and knowledge of крепостной is still used. No rare-date/term-trap requirement imposed.',
  'York university dictionary full entry defines labour hired for a day at a daily wage. Example is dated1600; that supports word meaning, not a first-attestation or all-medieval-labour claim. Current literal makes neither temporal claim. Useful option-specific wage fact passes.',
  'Lancaster full Rental entry lists tenants and rent due from each. Court baron expressly includes free and villein tenants, so note correctly avoids saying all tenants were free. A rental-list fact is useful to the free-tenant option; no universal freedom claim.',
  'SERF TLFi supports work/property belonging to owner and attachment to land. Attachment is additional useful fact beyond stem’s goods/work relationship; overlap with explanation is expressly allowed.',
  'Lancaster Freehold defines fee simple for ever by homage/service to manor lord. Note includes obligations and no longer falsely says freedom from manor custom. Useful precise tenure fact.',
  'Two clear Russian sentences identify serf and land attachment/dependency. Both factual clauses are supported by TLFi; attachment supplements the stem. No unsupported chevage survives in current literal.'
 ]}
a=json.loads(raw(AUTHOR));topic=json.loads(raw(TOPIC));byid={c['id']:c for c in topic['questions']}
manifest=json.loads(raw('docs/content-audits/question-quality-wave-6/middle-ages/resume-2026-10-12-rework28/source-manifest.json'))
sm={Path(s['rawCapture']).name:s for s in manifest['sources']}
cards=[];sources={}
for ac in a['cards']:
 c=byid[ac['questionId']];cid=c['id'];short=cid.removeprefix('middle-ages-');assert sha(canon(c))==ac['cardCanonicalSha256']
 fields=[]
 for i,af in enumerate(ac['fields']):
  name=af['field'];literal=([c['prompt'],c['correctIndex'],c['answers'][c['correctIndex']]['text']] if name=='prompt-key' else c['explanation'] if name=='explanation' else c['answers'][int(name[-1])]['note'])
  lb=json.dumps(literal,ensure_ascii=False,separators=(',',':')).encode() if name=='prompt-key' else literal.encode()
  fix=(short=='dower' and name=='prompt-key') or (short=='dowry' and name=='note0')
  proofs=[]
  for s in af['proofs']:
   p=s['rawCapture'];w=witness(p);assert w['rawSha256']==s['rawCaptureSha256'];m=sm[Path(p).name]
   sources[p]=dict(**w,sourceClass=s['sourceClass'],url=s['url'],captureUrl=m.get('captureUrl',s['url']),readMethod='Reader read substantive complete dictionary bodies or complete HTML page text from committed full original, not snippet/author passage alone. Nonclaim frequency/graph/concordance metadata not treated as proof.',scopeLimitation='Publisher abstract only; no full article claim.' if p.endswith('ugr-dowry.html') else 'Complete native response capture.')
   proofs.append(dict(sourceClass=s['sourceClass'],url=s['url'],rawCapture=p,rawCaptureSha256=w['rawSha256'],gitBlob=w['gitBlob'],frozenCommit=w['commit'],locator=s['locator']))
  fields.append(dict(field=name,literalText=literal,literalSha256=sha(lb),sourceVerdict='PASS',editorialVerdict='FIX' if fix else 'PASS',verdict='FIX' if fix else 'PASS',substantiveRead=True,individualReaderAnalysis=analysis[short][i],proofs=proofs))
 cards.append(dict(questionId=cid,difficulty=c['difficulty'],correctIndex=c['correctIndex'],currentCard=c,cardCanonicalSha256=sha(canon(c)),sourceVerdict='PASS',editorialVerdict='FIX' if any(f['verdict']=='FIX' for f in fields) else 'PASS',verdict='FIX' if any(f['verdict']=='FIX' for f in fields) else 'PASS',fields=fields))
spec=Path('/Users/eaafonasev/Projects/mindbattle-planning/docs/GAME_SPEC.md').read_bytes();lines=spec.decode().splitlines();(OUT/'approved-rules.txt').write_text('\n'.join(f'{i+1}: {lines[i]}' for i in range(136,155))+'\n')
dump('reader-receipt.json',dict(schemaVersion=1,role='independent-source-and-editorial-reader',readerIdentity=os.environ['CODEX_THREAD_ID'],actualCODEX_THREAD_ID=os.environ['CODEX_THREAD_ID'],authorIdentity=a['agentIdentity'],independentIdentities=os.environ['CODEX_THREAD_ID']!=a['agentIdentity'],frozenContentCommit=subprocess.check_output(['git','rev-parse','9800700']).decode().strip(),frozenEvidenceCommit=subprocess.check_output(['git','rev-parse',REF]).decode().strip(),topicWitness=witness(TOPIC),authorReceipt=witness(AUTHOR),authorRoundtrip=witness('docs/content-audits/question-quality-wave-6/middle-ages/resume-2026-10-12-rework28/pilot-four-git-roundtrip.json'),scopeRule=witness('docs/content-audits/question-quality-wave-6/coordinator-continuation-01a12c24/middle28-current-rework-scope-2026-10-12.json'),approvedRules=dict(sourcePath='/Users/eaafonasev/Projects/mindbattle-planning/docs/GAME_SPEC.md',sourceRawSha256=sha(spec),lines='137-155',localSnapshot='approved-rules.txt',medium='line139',easy='line138',hard='line140',correctNoteAdditionalFact='line143',overlapAllowed=True),scope=[c['questionId'] for c in cards],protected='Palimpsest certified result preserved without reread; other96 no substantive review or edits. Prior failed/FIX/HOLD history and originals untouched.',decisionOrigin='Individual manual independent reading; serializer only hashes and binds manually supplied decisions.',cards=cards,sourceOriginals=list(sources.values()),counts=dict(cards=4,fields=24,sourcePASS=24,editorialPASS=22,editorialFIX=2,HOLD=0),duplicates=dict(method='Narrow external-topic textual search for brideprice/douaire/precarium/personal-dependency/land-attachment phrases, excluding middle-ages; no result. No claim of exhaustive semantic catalog clearance.',externalPartners=[]),qaScope='Evidence JSON/literal/hash/Git blob byte checks only. No runtime/content mutation, no full suite, build or deploy.'))
