"""Full source fetches; explicit transport/completeness metadata, no verdicts."""
import urllib.request,ssl,certifi,json,hashlib,pathlib,concurrent.futures
r=pathlib.Path(__file__).parent;s=r/'sources'
urls={
'met-tarot-ja.html':'https://www.metmuseum.org/ja/perspectives/tarot-2',
'canasta-slash.html':'https://bicyclecards.com/how-to-play/canasta/',
'pokemon-assets.pdf':'https://assets.pokemon.com/assets/cms2/pdf/trading-card-game/rulebook/par_rulebook_en.pdf',
'yugioh-eu.pdf':'https://img.yugioh-card.com/uk/rulebook/Rulebook_v9_en.pdf',
'lorcana-retry.pdf':'https://files.disneylorcana.com/Comprehensive-Rules_2.2.0-EN.pdf?download=1',
'durak-retry.pdf':'https://c.tabletopia.com/games/pdurak/rules/durakrules/en',
}
def fetch(x):
 name,url=x
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
  with urllib.request.urlopen(req,context=ssl.create_default_context(cafile=certifi.where()),timeout=25) as f:
   b=f.read();ctype=f.headers.get('Content-Type');length=f.headers.get('Content-Length');status=f.status;final=f.url
  (s/name).write_bytes(b);return {'file':name,'url':url,'finalUrl':final,'status':status,'contentType':ctype,'contentLength':length,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
 except Exception as e:return {'file':name,'url':url,'error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool: rows=list(pool.map(fetch,urls.items()))
(r/'retry-downloads.json').write_text(json.dumps(rows,indent=2)+'\n')
for row in rows: print(json.dumps(row))
