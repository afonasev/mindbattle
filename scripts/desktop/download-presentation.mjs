const repository = 'https://github.com/afonasev/mindbattle';
export function installerReleases(version) {
  if (!/^\d+\.\d+\.\d+$/.test(version)) throw Error('Native installer version required');
  return `${repository}/releases?q=tag%3Av${version.split('.')[0]}%20prerelease%3Afalse`;
}

/** Human download entry point; content identities and update URLs remain untouched. */
export function installerDownloadSection(version) {
  if (!/^\d+\.\d+\.\d+$/.test(version)) throw Error('Native installer version required');
  const base = `${repository}/releases/download/v${version}/Mindbattle-${version}`;
  return `<!-- mindbattle-downloads:start -->
## Download / Скачать

| Windows | macOS |
| --- | --- |
| **[Download EXE](${base}-win-x64.exe)** | **[Download DMG](${base}-mac-universal.dmg)** |

[Installer releases / Только установщики](${installerReleases(version)}) · [Play in browser / Играть в браузере](https://mindbattle.afonasev.tech/)

Installer version: **${version}**. The installed game receives newer game content through its updater.

<!-- mindbattle-downloads:end -->`;
}

export function withInstallerDownloads(notes, version) {
  const remaining = notes.replace(/<!-- mindbattle-downloads:start -->[\s\S]*?<!-- mindbattle-downloads:end -->\s*/g, '').trimStart();
  return `${installerDownloadSection(version)}\n\n${remaining}`;
}
