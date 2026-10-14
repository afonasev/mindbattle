import test from 'node:test';
import assert from 'node:assert/strict';
import { gameLaunchUrl, isMutedLaunch } from '../../desktop/launch.mjs';

test('muted desktop launch adds the startup query to the game URL', () => {
  assert.equal(gameLaunchUrl('mindbattle://game', true), 'mindbattle://game/?muted=1');
  assert.equal(gameLaunchUrl('mindbattle://game', false), 'mindbattle://game/');
});

test('desktop wrapper recognizes only the explicit muted switch', () => {
  assert.equal(isMutedLaunch(['electron', 'desktop/main.mjs', '--muted']), true);
  assert.equal(isMutedLaunch(['electron', 'desktop/main.mjs']), false);
});
