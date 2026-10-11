import urllib.request,ssl,certifi,concurrent.futures,json,hashlib
from pathlib import Path
R=Path(__file__).parent
urls={
'lorcana-resources.html':'https://www.disneylorcana.com/en-US/resources',
'lorcana-current.pdf':'https://files.disneylorcana.com/CRUpdate_EN_Oct-2026.pdf',
'lorcana-quick-current.pdf':'https://files.disneylorcana.com/Whispers-in-the-Well_StarterDeckA_RULES_A.pdf',
'pokemon-current.pdf':'https://www.pokemon.com/static-assets/content-assets/cms2/pdf/trading-card-game/rulebook/meg_rulebook_en.pdf',
'pokemon-rules.html':'https://www.pokemon.com/us/pokemon-tcg/rules',
'magic-rules.html':'https://magic.wizards.com/en/rules',
'yugioh-faq.html':'https://www.yugioh-card.com/en/about/faq-for-parents/'
}
def fetch(item):
 n,u=item
 try:
  with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),context=ssl.create_default_context(cafile=certifi.where()),timeout=40) as r:
   b=r.read(); p=R/'sources'/n
   if n.endswith('.pdf') and not b.startswith(b'%PDF'):p=p.with_suffix('.html')
   p.write_bytes(b); return dict(url=u,path=str(p),status=r.status,headers=dict(r.headers),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
 except Exception as e:return dict(url=u,error=str(e))
rows=list(concurrent.futures.ThreadPoolExecutor(7).map(fetch,urls.items()));(R/'fetch-receipts.json').write_text(json.dumps(rows,indent=2));print(json.dumps(rows,indent=2))
