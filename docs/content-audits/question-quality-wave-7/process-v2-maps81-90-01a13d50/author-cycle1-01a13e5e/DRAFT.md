# Cycle 1 author draft

Baseline e25424066ba8c3e12f9ce7f0ea76ded0fd42fafa. The request JSON names a7e302d..., but all six supplied preimages and canonical hashes match e254 and current HEAD.

| Order | ID | Status | Change |
|---:|---|---|---|
| 84 | maps-cartography-read-coordinates | FIX | fixed coordinate duplicate/order and corrected hemispheres; added angular-coordinate context |
| 86 | maps-cartography-waldseemuller-america | FIX | historical inference from supplied map observations and prior model |
| 87 | maps-cartography-cadastral-parcels | FIX | applied FAO scale/line-width and source-data accuracy constraints |
| 88 | maps-cartography-area-distortion | FIX | projection-purpose choice, distinct from 90 arithmetic |
| 89 | maps-cartography-shape-distortion | FIX | relative-angle reasoning despite common rotation |
| 90 | maps-cartography-distance-distortion | FIX | retained valid linear-scale task; clarified ground-length distractor note |

Full before/proposed cards and hashes: candidate.json. Six literal groups and four slot reviews per ID: sourceproof.json. Full CURRENT and FINAL proposed 88/90 pair plus updated CURRENT peers 92/93/95 and nine pairwise comparisons with final 88/89/90: peer-pairs.json.

No catalog QA, runtime, build, or deploy run. Quality credit remains 0 pending independent CURRENT review.
