import json,hashlib
from pathlib import Path
from html.parser import HTMLParser
ROOT=Path('/tmp/mindbattle-source-01a137d4-70e3-74f0-bbe4-0d13e5dca25f')
cand=ROOT/'author-correction-3.json'; pairs=ROOT/'weather-good7-source-editorial-pairs-correction-1.json'; prevpairs=ROOT/'weather-good7-source-editorial-pairs.json'; sourcefix=ROOT/'source-correction-1-manifest.json'
cb=cand.read_bytes();pb=pairs.read_bytes();opb=prevpairs.read_bytes();smb=sourcefix.read_bytes()
assert hashlib.sha256(cb).hexdigest()=='117da3c02e37834d8e34eaad87430e3499f74246dfc43d88d9da071c439615a6'
assert hashlib.sha256(pb).hexdigest()=='3197471c517b7927fd1445e25fbe5642be18210bdd92c01fb142a2e63b619675'
assert hashlib.sha256(opb).hexdigest()=='6a3edb93249018505d41bfb99c155be1aa96afdae0e5e9a2fa6f16acefa4fc02'
cd=json.loads(cb)
ctx=next(x for x in cd['sourceCaptureBindings'] if x['sourceKey']=='CAP-thunder-jetstream')['typedCompleteContexts'][0]
rawpath=Path(ctx['bodyRef']); raw=rawpath.read_bytes();assert len(raw)==4630 and hashlib.sha256(raw).hexdigest()=='9297fea339337785038942bd301410a46a5529ba8e23d2714ce26b8b39f8a76e'
class P(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.parts=[];self.alt=[]
 def handle_data(self,data):self.parts.append(data)
 def handle_starttag(self,tag,attrs):
  if tag.lower()=='img':self.alt.extend(v or '' for k,v in attrs if k.lower()=='alt')
p=P();p.feed(raw.decode('utf-8','strict'));p.close();literal=' '.join(' '.join(p.parts).split());literal_hash=hashlib.sha256(literal.encode('utf-8')).hexdigest()
old=ctx['completeVisibleLiteral'];oldhash=ctx['normalizedBareUTF8SHA256']
assert oldhash=='b62aaa38cf1b2efbd7291580513c2d222c31bfc520be3f82a4b3df46ac55a772'
assert '54,000 °F (30,000 °C )' in literal
corr={
 'schema':'mindbattle-hash-policy-and-thunder-normalization-corrigendum-v1',
 'authorNativeThreadId':'01a137d4-70e3-74f0-bbe4-0d13e5dca25f',
 'boundArtifacts':[
  {'path':str(cand),'bytes':len(cb),'sha256':hashlib.sha256(cb).hexdigest(),'role':'effective author packet; immutable binding'},
  {'path':str(pairs),'bytes':len(pb),'sha256':hashlib.sha256(pb).hexdigest(),'role':'effective paired SOURCE/EDITORIAL addendum; immutable binding'},
  {'path':str(prevpairs),'bytes':len(opb),'sha256':hashlib.sha256(opb).hexdigest(),'role':'historical paired addendum; preserved'},
  {'path':str(sourcefix),'bytes':len(smb),'sha256':hashlib.sha256(smb).hexdigest(),'role':'bounded source corrections lineage; preserved'}],
 'hashPolicyClarification':{
  'authority':'This author declares these as distinct input recipes for each field; a digest from one recipe must not be presented as the digest of a different recipe. Existing artifacts and stored hash values are not rewritten by this corrigendum.',
  'authorPacketRecipes':{
   'promptAnswersKey':'SHA256 of compact insertion-ordered UTF-8 JSON object with exact keys prompt, orderedAnswerTexts, correctIndex, correctAnswerText.',
   'explanationAndAnswerNotes':'SHA256 of exact UTF-8 JSON scalar value bytes as declared by author packet canonicalization.scalarHashes; preserve the packet-declared recipe when interpreting packet fields.',
   'difficultyClass':'SHA256 of compact UTF-8 JSON scalar string (quoted JSON string; see classSHA256 field recipe).',
   'metadataSource':'SHA256 of sorted-key compact UTF-8 JSON object.',
   'fullCard':'SHA256 of sorted-key compact UTF-8 JSON object, no trailing LF.'},
  'pairedReasonAddendumRecipes':{
   'promptAnswersKey':'SHA256 of the same compact insertion-ordered UTF-8 JSON object recipe.',
   'explanationAndAnswerNotes':'SHA256 of bare literal UTF-8 content bytes; no JSON quotation marks, escaping, or trailing LF.',
   'difficultyClass':'SHA256 of compact UTF-8 JSON scalar string, matching the paired group exactGroupSHA256 policy for difficulty.',
   'metadataSource':'SHA256 of sorted-key compact UTF-8 JSON object.',
   'scope':'56 paired literal groups across seven cards; recipe is per group type, not one uniform scalar rule.'},
  'comparisonRule':'Do not claim hash equality between JSON-serialized scalar bytes and bare literal UTF-8 bytes. Compare only hashes whose recipe-specific preimages are byte-identical. Composite, difficulty and metadata use the explicitly stated JSON recipes; explanation/answer-note pair literals use the bare-text recipe.'},
 'thunderWholeDocumentNormalization':{
  'sourceRef':'CAP-thunder-jetstream','sourceURL':'https://www.weather.gov/source/zhu/ZHU_Training_Page/lightning_stuff/lightning2/thunder.html',
  'rawPath':str(rawpath),'rawBoundsHalfOpen':[0,4630],'rawBytes':len(raw),'rawSHA256':hashlib.sha256(raw).hexdigest(),'rawCaptureUnchanged':True,
  'correctedExtractionRecipe':'Strict UTF-8 decode; Python HTMLParser(convert_charrefs=True); collect character-data callbacks in order; retain image alt text in separate collection; join character data with spaces; collapse Unicode whitespace with split/join; no Unicode normalization; hash bare normalized literal as UTF-8.',
  'correctedCompleteVisibleLiteral':literal,'correctedLiteralCharacters':len(literal),'correctedNormalizedBareUTF8SHA256':literal_hash,'imageAltTextSeparate':p.alt,
  'knownInlineMarkupResult':'At the first inline superscript/unit sequence the parsed text is exactly 54,000 °F (30,000 °C ); this spacing comes from adjacent HTML character-data nodes and is preserved by the declared join rule.',
  'historicalIncorrectExtractionPreserved':{'completeVisibleLiteral':old,'normalizedBareUTF8SHA256':oldhash,'status':'superseded historical value; do not use as effective complete-visible-literal receipt'},
  'preservedExactSubcontexts':[
   {'locator':'nearby thunder exact table cell','rawBoundsHalfOpen':[2337,2538],'rawContextSHA256':'8aa1978790d73fecaf508e3ab21e2dbed0e4fb963568b4a612b7f23e0201be17'},
   {'locator':'distant wave propagation exact table cell','rawBoundsHalfOpen':[2540,2802],'rawContextSHA256':'81fa7aa8300c2d58ea52ea6479802524f6f57a066f5c6a14040d98d1dfdb8300'},
   {'locator':'distant continuous rumble exact table cell','rawBoundsHalfOpen':[2804,3063],'rawContextSHA256':'95ddfc24be1516b7f648f307169a782606d828876f484e69b4460699e657cf01'},
   {'locator':'temperature inversion refraction paragraph','rawBoundsHalfOpen':[3419,3779],'rawContextSHA256':'51c6ee84f6a50c65ba9640251592b1327282a4a5ebc9fe88115831ff5526f536'}],
  'scope':'Correct the effective whole-document extraction receipt only. Raw body, raw headers, four exact subcontexts, #28 product wording, and prior artifact are unchanged.'},
 'qualification':'Not a product edit, qualification, or credit claim. Coordinator remains owner of qualification; current aggregate supplied by coordinator is 558/1442, source credit remains 0.',
 'actionsNotTaken':['overwrite of bound packet or paired addendum','new network/capture request','runtime/QA/test/build','Git write/commit/push/merge/deploy']}
# Include old and corrected visible literals as a separate audit trail; no mutation of source capture or bound artifacts.
out=ROOT/'hash-policy-thunder-normalization-corrigendum.json';blob=json.dumps(corr,ensure_ascii=False,separators=(',',':')).encode()+b'\n';out.write_bytes(blob)
man={'schema':'mindbattle-hash-policy-thunder-normalization-corrigendum-manifest-v1','corrigendumPath':str(out),'corrigendumBytes':len(blob),'corrigendumSHA256':hashlib.sha256(blob).hexdigest(),'boundCandidateSHA256':hashlib.sha256(cb).hexdigest(),'boundPairedAddendumSHA256':hashlib.sha256(pb).hexdigest(),'historicalPairedAddendumSHA256':hashlib.sha256(opb).hexdigest(),'rawThunderPath':str(rawpath),'rawThunderBytes':len(raw),'rawThunderSHA256':hashlib.sha256(raw).hexdigest(),'correctedNormalizedLiteralSHA256':literal_hash,'historicalNormalizedLiteralSHA256':oldhash,'sourceCredit':0,'qualificationPending':True}
mp=ROOT/'hash-policy-thunder-normalization-corrigendum-manifest.json';mb=json.dumps(man,ensure_ascii=False,indent=2).encode()+b'\n';mp.write_bytes(mb)
print('corrigendum',len(blob),hashlib.sha256(blob).hexdigest());print('manifest',len(mb),hashlib.sha256(mb).hexdigest());print('corrected literal',len(literal),literal_hash);print('historical literal',len(old),oldhash)
