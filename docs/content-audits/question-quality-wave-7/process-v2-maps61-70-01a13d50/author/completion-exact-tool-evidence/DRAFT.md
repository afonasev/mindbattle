# Exact-evidence completion: maps-cartography 61–70

Same ten frozen IDs and source orders, baseline `ea4b8d96c8edc94b01c918e002731a988bff3cd2`. No new IDs. This folder supersedes neither the earlier source-HOLD packet nor its history. Source contexts are exact slices from already-returned native web-reader text items, without rewriting; see provenance manifest for parent native call ID, rollout path, raw-output SHA, source URL, advertised Total lines/pages and extracted-context SHA. HTTP headers are not supplied or invented. Full parent tool outputs remain in sibling `exact-native-tool-responses/`.

Completeness checked against the returned line ranges and page counts: Esri PDF 10 pages L0–170; Esri spatial query L0–15; NOAA CORS L0–20; NOAA lidar L0–14; USGS publication page L0–68; UNESCO Tabula page L0–124; Hereford nomination PDF 5 pages L0–203. The Austrian National Library web response advertises 2,806 lines but is truncated in the saved native output and is not used.

**Author statuses:** FIX 8 (61–63, 65–66, 68–70); HOLD 2 (64, 67). Card 64 has a supported spatial-query key but weakly evidenced query-operation distractors; card 67 lacks a captured official definition distinguishing the broad ground-survey class from field submethods. Author FIX is not independent QA or quality credit.

Current and proposed medium9/hard5 peers were assessed through stems, options and notes. Full live-catalog cards and hashes for sourceOrders 69, 70, 85, 86 and 87 are in `peer-snapshot.json`. SourceOrders 86 (Waldseemuller) and 87 (cadastral parcels) each have distractor notes that spell out both historical targets. The two proposed historical candidates also use each other as a distractor and define each other in its note. This is direct cross-item leakage; independent review/coordinator adjudication must account for it before quality credit.

## Correct-note audit and edit history

Audited all eight correct notes. Six were rewritten to add exact saved-source facts absent from their stems: order 61, each Esri vector layer has its own attribute table opened with Show Table; order 65, NOAA postprocessed CORS coordinates can approach centimeter accuracy horizontally and vertically; order 66, USGS total-station and EDM uncertainty specifications; order 68, aircraft GPS and inertial-system roles; order 69, the Tabula’s parchment and 11 segments; order 70, the Hereford map’s one-sheet dimensions and circa 1290–1310 date. Orders 62 and 63 already had additional source-backed cell-value and table-field examples, so their notes were retained. Exact before/after literals and reasons are in `peer-snapshot.json` under `authorEditHistory`.

Canonical prompt group is `{prompt, answers: [ordered texts], correctIndex}`; all six literal groups, proposed-card hashes and four per-option assessment bindings were refreshed and checked. No new network calls, Git/index/catalog edits, runtime, tests, builds, audio or messages.
