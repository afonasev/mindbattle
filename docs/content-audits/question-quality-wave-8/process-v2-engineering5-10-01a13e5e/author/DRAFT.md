# Engineering machines sourceOrder 5–10

Baseline `e581e5a505177afa60eceee1c4a5a0bf192f23f7`; exact scope is the six IDs bolt-fastener through universal-joint. All six preimages were SHA-checked against both the recovered HOLD manifest and baseline topic catalog.

## Outcome

- `engineering-machines-bolt-fastener` — FIX proposal ready for independent review. Prompt scopes the external-wrench cue to one nonuniversal bolt/screw convention.
- `engineering-machines-screw-fastener` — FIX proposal ready for independent review. Prompt scopes the internal-driver cue the same way.
- `engineering-machines-nut-fastener` — FIX proposal ready for independent review; prompt asks for the internal-thread component receiving a bolt.
- `engineering-machines-rivet-fastener` — FIX proposal ready for independent review; prompt asks about forming the closure head.
- `engineering-machines-counterweight-balance` — HOLD: Otis supports the traction-lift case only, not the crane clause or the flywheel/coupling/bearing note claims.
- `engineering-machines-universal-joint` — HOLD: Spicer supports operating-angle terminology, not the original kinematics or gear-coupling/plain-bearing/ratchet note claims.

Every FIX preserves ID, topic, sourceOrder, easy difficulty, answer text/order and correctIndex. It has six literal groups with before/after hashes, four individually assessed prompt-answer-note rows, full-source locators, and a complete candidate card. All remain proposals for independent review, not current PASS; quality credit is zero.

## Source read

Reused the existing complete NASA RP-1228 100-page PDF and extracted text. Read and visually rendered full relevant pages: PDF 5 (printed 1, bolt materials); PDF 11 (printed 7, locknut thread engagement); PDFs 30–31 (printed 26–27, rivets, head forming and removal).

One new official NASA source was captured for the actual bolt/screw ambiguity gap: full 384-page PDF and extracted text in `sources/`. PDF p.383 (printed 21-7) was read and rendered. Q10 gives several competing definitions, states none is universally acceptable and the definitions overlap, and recommends specifying geometry or part number. Both prompts therefore ask only within a named convention.

Read the saved complete Otis L0–L497 and Spicer L0–L223 texts at the relevant passages. Their embedded/interactive media were not used as evidence.

## Packet files

- `candidate.json`: exact six preimages, four FIX proposals, two HOLDs.
- `sourceproof.json`: source-file byte hashes, six literal groups and detailed four-slot grounds for every FIX.
- `peer-snapshot.json`: all 100 current cards and hashes, full relevant neighbors, four proposals and all 15 comparisons among the final six cards.
- `needed-evidence.json`: exact remaining support needed for both HOLDs.
- `sources/nasa-fastener-faq.*`: official full capture addressing the genuine classification ambiguity.

No catalog, planning, index, claim, Git/index, test, runtime, build or deploy files were changed.
