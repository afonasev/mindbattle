# Mindbattle

[English](README.md) · [Русский](README.ru.md)

Mindbattle is a browser quiz game for playing together on one screen, on your own, or with phones connected to a shared display. It uses a local Node.js server for the game and feedback API. The interface is currently in Russian.

**[Play online](https://mindbattle.afonasev.tech/)**

## Play

| Mode | Players and devices | How it works |
| --- | --- | --- |
| Classic | 2–4 teams at one desktop screen | Teams answer the same questions simultaneously. Two teams can use separate keyboard layouts; additional teams need compatible gamepads. |
| Solo | One player on desktop or a portrait phone | An endless question run with lives, risk questions, and a local high score. The phone version can be installed as a PWA and used offline after its first online load. |
| Network | 2–12 players with phones and one desktop display | The display creates a room code. Each player joins on a phone; the server coordinates questions, answers, timers, and reconnects. The display is not a player. |

The network mode is implemented, but its real shared-display and multiple-physical-phone playtest is still open. Automated browser tests do not replace that check.

## Run locally

Requires **Node.js 20.19+** and npm. Desktop Chromium is the tested target for the shared-screen game.

```bash
npm ci
npm run dev
```

Open the address printed by the server, normally `http://127.0.0.1:4173`. For a production build on your machine:

```bash
npm run build
npm run preview
```

The server listens on `127.0.0.1:4173` by default. Set `MINDBATTLE_HOST` and `MINDBATTLE_PORT` to change that. To open the local network mode from phones, bind the server to a reachable interface and use your computer's LAN address; `127.0.0.1` only works on the computer itself.

Anonymous question feedback is saved to `data/difficulty-feedback.ndjson` by default. Set `MINDBATTLE_FEEDBACK_PATH` to use another location. Game progress and solo records are stored in the browser.

## Controls

- Classic supports `WASD`, arrow keys, and compatible Xbox, PlayStation, or Nintendo-style gamepads. Each team needs its own assigned input.
- Choose answers by position: up, right, down, or left. `Escape` opens the pause menu.
- Solo on a phone uses touch controls. In network mode, the shared display shows the room while each player answers on their phone.

## Checks

```bash
npm run check          # types, unit tests, and build
npm run content-check  # question catalog checks
npm run test:browser    # Playwright browser scenarios
```

Game rules live separately from the renderer and use serializable state and seeded randomness. See `src/domain/`, `src/application/`, `src/network/`, and `server/` for the main boundaries.

## Project workflow and deployment

[workflow/project.json](workflow/project.json) records the shared OpenSpec planning store, checks, and release policy. The canonical game specification and OpenSpec history are kept in that separate planning store; [docs/GAME_SPEC.md](docs/GAME_SPEC.md) explains the location. Feature branches are pushed to `origin` after verification, then integrated and pushed to `main` with evidence recorded in the change. Production deployment is a separate, explicitly authorized step and human acceptance remains separate from automated checks.

The maintainer deploys with `make deploy` to `mindbattle.afonasev.tech` using a configured VPS and SSH profile. This command builds the app, updates the server, restarts the service, and checks local health; it is not needed for local play. See [scripts/deploy.sh](scripts/deploy.sh) for the exact deployment procedure.

## License

[MIT](LICENSE).
