# Controls art, simplified direction

User approved the simplified solo mockup on 2026-10-16, then authorized implementation.
The exact original is versioned as `public/images/controls-simplified-v2.png`:
SHA256 `5a4821bc3b89e60a26f3e8a50016a0e839621997aadad3dff253a23f70bddbd1`.
Concept approval is separate from runtime visual acceptance.

`public/images/controls-keycaps-v2.png` is a transparent generated sprite atlas derived
from that approved reference with the built-in imagegen tool (1536×1024 RGBA).
It preserves the graphite keycaps, subtle texture, soft silver edges and ivory printed
legends. It removes the poster background, UI text, callout lines and dots.
No post-generation bitmap edits were used. SVG viewBox selects complete key illustrations;
text and layout remain responsive and use the actual selected game mode/layout.
`ControlsHelp.tsx` contains the exact sprite rectangles.

Generation prompt: recompose the reference key artwork on genuine transparent alpha,
1536×1024, four columns and two rows, without grid or labels. Top row: WASD T group,
arrow T group, A/D pair, left/right arrow pair. Bottom row: Enter, Space, right Shift,
Esc. Keep each asset inside its cell with transparent margins, preserve the reference
materials and printed legends, remove all background, blue rings, leaders and external
text. No background rectangles or checkerboard pattern.

Pad keeps the existing device source and runtime `GAMEPAD_GLYPHS`; family and game
mode are selected separately. Keyboard bindings are checked against input.ts/soloInput.ts,
pause handling against App.tsx. No physical input adapter is changed.

## F3: render the approved original intact

The solo/WASD page now renders `controls-simplified-v2.png` as one full `<img>`,
without sprite extraction, new key legends or reconstructed captions. Exact SHA256
is verified against the approved asset by browser QA. Transparent mode hotspots
follow the tabs already printed in the picture; external device/layout controls and
Back remain functional. Fit/zoom and pan controls make the complete original
accessible on narrow screens. Other modes/layouts retain their corresponding
existing illustrations and bindings, rather than showing an inaccurate solo PNG.
