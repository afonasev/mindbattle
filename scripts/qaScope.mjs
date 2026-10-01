// Explicit coverage, chosen after reviewing contracts; never infer risk from filenames.
const uiUnits = ['tests/unit/solo-ui.test.ts', 'tests/unit/network-status.test.ts', 'tests/unit/content-answer-notes.test.ts'];
const inputUnits = ['src/adapters/input.test.ts', 'tests/unit/solo-input.test.ts', 'tests/unit/application-controller.test.ts'];
const networkUnits = ['tests/unit/network-domain.test.ts', 'tests/unit/network-room.test.ts', 'tests/unit/network-status.test.ts'];
export const scopes = {
  tooling: { units: [], browser: [] },
  ui: { units: uiUnits, browser: [
    ['menu.spec.ts', 'main menu uses one tagline'],
    ['menu.spec.ts', 'local mode uses the same secondary action'],
    ['menu.spec.ts', 'persists presentation volume'],
    ['qa-display.spec.ts', 'mobile menu and solo touch surface'],
    ['phone-reveal.spec.ts', 'phone reveal and states:', 4],
    ['solo.spec.ts', 'matches the team reveal for a wrong solo answer', 3],
    ['solo.spec.ts', 'uses the team pause dialog and resumes the solo run'],
    ['game.spec.ts', 'renders the main explanation and three horizontal wrong-answer cards without overflow'],
    ['qa-display.spec.ts', 'display reveal snapshot', 2]
  ] },
  network: { units: networkUnits, browser: [
    ['network.spec.ts', 'network feedback continues after a successful server write'],
    ['network.spec.ts', 'network: 12 phones, private answers, bonus, display restore and departure'],
    ['topic-diversity.spec.ts', 'network authoritative three and five topic lists agree on display and phones']
  ] },
  input: { units: inputUnits, projects: ['chromium-1280'], browser: [
    ['solo.spec.ts', 'accepts a neutral virtual gamepad before moving and confirming'],
    ['solo.spec.ts', 'uses D-pad left and right, not up and down, for solo feedback choices'],
    ['solo.spec.ts', 'boots when the browser does not implement the Gamepad API'],
    ['game.spec.ts', 'supports N\\+1 public bonus veto for three and four assigned teams']
  ] },
  full: { units: null, browser: null }
};
export function selectedSpec(scope, file, title) {
  return scope.browser.some(([name, pattern]) => file.endsWith(name) && new RegExp(pattern).test(title));
}
