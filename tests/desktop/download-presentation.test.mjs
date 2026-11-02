import test from 'node:test';
import assert from 'node:assert/strict';
import {withInstallerDownloads} from '../../scripts/desktop/download-presentation.mjs';
test('installer links survive repeated rendering and exclude technical releases',()=>{
 const notes='## Русский\n- Исправлено\n\n## English\n- Fixed';
 const body=withInstallerDownloads(notes,'1.0.6');
 assert.equal(withInstallerDownloads(body,'1.0.6'),body);
 assert.ok(body.includes('/afonasev/mindbattle/releases/download/v1.0.6/Mindbattle-1.0.6-win-x64.exe'));
 assert.ok(body.includes('Mindbattle-1.0.6-mac-universal.dmg'));
 assert.ok(body.includes('tag%3Av1%20prerelease%3Afalse'));
 assert.ok(body.endsWith(notes));
 assert.throws(()=>withInstallerDownloads(notes,'content-42'));
});
