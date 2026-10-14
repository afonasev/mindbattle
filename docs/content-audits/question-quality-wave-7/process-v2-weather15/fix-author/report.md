# Addressed fix cycle 11 — weather-climate

- Baseline: `48610ef5b078d9d202598bea21120b5055615053`; scope is the exact 11 IDs from `fix-requests11.json`.
- Proposed: 7 FIX, 4 HOLD. Автор не менял CURRENT catalog, index или claims и не создавал commit; commit exact-apply остаётся задачей координатора.
- FIX IDs: humidity-water-vapor, hurricane-eye, orographic-rain, pressure-air-weight, rain-shadow, tropical-depression, tropical-storm.
- HOLD IDs: cirrus-feathery, cumulonimbus-storm, climate-long-term, frontal-rain.
- Corrected relative-humidity comparison and non-tropical/subtropical conflation. Cyclone notes now use saved NOAA/AOML primary context. Pressure note adds units. Rain-shadow uses NOAA's independent Captain Cook/Hilo geographic example. Orographic options distinguish lake-effect, frontal, rain-shadow and relief-forced precipitation.
- Captured source bodies and headers once under `sources/`; NOAA weather/climate returned HTTP 202 WAF challenge with zero body, retained as evidence. Its card remains HOLD.
- Each FIX includes exact before/after hashes, all six literal field groups with group hashes, concrete rationale, source locators/evidence, and adjacent-card review. HOLD includes preserved preimage/groups and exact next action.
- Review boundary: author result only; exact CURRENT application, independent reviewer, full catalog QA and commit remain coordinator gates. No tests/build/runtime were run.

## Subagent proposal check (unqualified)

A subagent checked the proposals before exact-apply and reported PASS for all 7. This is unqualified proposal-check evidence only: it is not the separately assigned user-chat reader, not a CURRENT verdict, and earns zero CURRENT credit. The actual child report and thread provenance are retained in `subagent-proposal-check-unqualified.json`. Exact proposal `afterHash` values reported by the child:

| ID | Child-reported verdict | afterHash |
|---|---|---|
| weather-climate-humidity-water-vapor | PASS | `29f572d63b410899f627124b5e6a549ae065f880e88e981e9726367b720c7712` |
| weather-climate-hurricane-eye | PASS | `217b74539b5e1bf1e18e9276baa95bcfdfe02ce7cc279f61cfddb224a7cdd6ac` |
| weather-climate-orographic-rain | PASS | `e6fcf44b3ac9262cb16e07561f8bcbea68b3ea2e53286db2b8d81b64e5b9bb93` |
| weather-climate-pressure-air-weight | PASS | `f5b8c64ad595cfe27135546e716d423f060aba2f835724403a5e3c9b15435808` |
| weather-climate-rain-shadow | PASS | `a6f090150268fad150ac2826c279b506bfa9e84518dcdb178e3066473a5133cb` |
| weather-climate-tropical-depression | PASS | `4deef47b16c9e853b2b132a2018eb1aff90afd960543a541b95b65f973cb92bc` |
| weather-climate-tropical-storm | PASS | `de30b7aab3a183026f4133d1928b297b2dcc4b337ee80f0b76306f8bc09917c2` |

The child reported checking the humidity/pressure distinction, cyclone thresholds and terminology, orographic/rain-shadow evidence, neighbors, all 42 literal-group hashes, and captured source bytes/headers. These are proposal-check claims only. The four initial source-HOLD entries remain HOLD; no PASS or CURRENT credit is inferred. The designated reader must review the exact CURRENT cards after coordinator exact-apply.

- At final readback the shared branch was `codex/question-quality-wave-6` at `c931cf474ccafe23b001105adf23e5241be2f4f9`; this branch-head change was concurrent and not created by the author. The author files below remain untracked in the worktree.
