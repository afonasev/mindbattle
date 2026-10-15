import { execFileSync } from 'node:child_process';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
const labels = {ru:{added:'Новое',improved:'Улучшения',fixed:'Исправления'},en:{added:'Added',improved:'Improved',fixed:'Fixed'}};
// Versioned, reviewed bilingual fragments are tied to the commits that introduce them.
// Never guess a release's behavior from technical commit subjects.
export function releaseNotes({ cwd = process.cwd(), channel = 'installer', revision = 'HEAD', run = (args) => execFileSync('git',args,{cwd,encoding:'utf8'}).trim() } = {}) {
  const tags = run(['tag','--merged',revision,'--sort=-creatordate']).split('\n').filter(Boolean).filter(tag => channel === 'installer' ? /^v\d+\.\d+\.\d+$/.test(tag) : new RegExp(`^${channel}-[0-9]+$`).test(tag));
  const previous = tags.find(tag => run(['rev-parse',`${tag}^{commit}`]) !== run(['rev-parse',revision]));
  const range = previous ? `${previous}..${revision}` : revision;
  const commits = run(['log','--format=%H',range]).split('\n').filter(Boolean);
  const entries = [], seen = new Set();
  for (const commit of commits) {
    const files = run(['diff-tree','--root','--no-commit-id','--name-only','--diff-filter=A','-r',commit,'--','docs/desktop/release-changes']).split('\n').filter(file => file.endsWith('.json'));
    for (const file of files) {
      const fragment = JSON.parse(run(['show',`${commit}:${file}`]));
      if (seen.has(fragment.id)) continue;
      seen.add(fragment.id);
      for (const entry of fragment.changes ?? []) {
        if (!labels.ru[entry.category] || typeof entry.ru !== 'string' || typeof entry.en !== 'string' || !entry.ru.trim() || !entry.en.trim()) throw Error('Release notes require matching RU/EN changes.');
        entries.push(entry);
      }
    }
  }
  if (!entries.length) throw Error('No reviewed bilingual release notes in the selected Git history. Add a release-changes fragment before publishing.');
  return ['ru','en'].map(lang => `## ${lang === 'ru' ? 'Русский' : 'English'}\n\n` + Object.entries(labels[lang]).map(([category,label]) => {
    const changes = entries.filter(entry => entry.category === category);
    return changes.length ? `### ${label}\n${changes.map(entry=>`- ${entry[lang]}`).join('\n')}\n` : '';
  }).filter(Boolean).join('\n') + (lang === 'ru' ? '\nТестовая поставка без платформенной подписи. Реальная приёмка macOS/Windows записывается отдельно. Не отключайте системную защиту. Если доверяете этому GitHub-релизу: Windows — «Подробнее → Выполнить в любом случае»; macOS — скопируйте игру в Applications и используйте штатное «Всё равно открыть» в настройках безопасности.\n' : '\nUnsigned test distribution. macOS/Windows acceptance is recorded separately. Keep system protection enabled. If you trust this GitHub release: Windows — More info → Run anyway; macOS — copy to Applications and use the standard Open Anyway security action.\n')).join('\n');
}
if (process.argv[1] === fileURLToPath(import.meta.url)) process.stdout.write(releaseNotes({channel:process.argv[2] ?? 'installer'})+'\n');
