import { useEffect, useState } from "react";
import { onPwaUpdate, onDesktopUpdateStatus, updateGame } from "../main";
import { desktop, type DesktopUpdateStatus } from "../desktop";
import { MenuAction, MenuDialog } from "./menuUi";

export function MainMenuUpdate() {
  const [ready, setReady] = useState(false);
  const [version, setVersion] = useState<string>();
  const [publishedAt, setPublishedAt] = useState<string>();
  const [status, setStatus] = useState<DesktopUpdateStatus>({ phase: 'idle' });
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  const [history, setHistory] = useState(false);
  useEffect(() => onPwaUpdate((available, nextVersion, publication) => { setReady(available); setVersion(nextVersion); setPublishedAt(publication); }), []);
  useEffect(() => onDesktopUpdateStatus(setStatus), []);
  async function run(action: () => Promise<unknown>) {
    if (busy) return;
    setBusy(true); setError('');
    try { await action(); } catch (cause) { setError(cause instanceof Error && /^[А-ЯЁ]/.test(cause.message) ? cause.message : 'Не удалось выполнить обновление. Попробуйте снова.'); }
    finally { setBusy(false); }
  }
  const downloading = status.phase === 'downloading';
  const candidate = ['available', 'paused', 'download-error'].includes(status.phase);
  const nextVersion = status.version ?? version;
  const publication = status.publishedAt ?? publishedAt;
  const date = publication && Number.isFinite(Date.parse(publication)) ? new Date(publication) : undefined;
  const dateLabel = date ? new Intl.DateTimeFormat('ru-RU', {year:'numeric',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit',timeZoneName:'short'}).format(date) : undefined;
  return <div className="menu-update">
    {status.phase === 'checking' && <p role="status">Проверяем обновления…</p>}
    {status.phase === 'error' && <p role="status">Не удалось проверить обновления. Следующая проверка — при запуске игры.</p>}
    {candidate && <MenuAction disabled={busy} caption={`${nextVersion ?? 'Новая версия'}${date ? ` · ${dateLabel}` : ''}`} onClick={() => void run(async () => { if (!desktop?.downloadUpdate || !await desktop.downloadUpdate()) throw Error('Обновление доступно только в безопасном меню.'); })}>{status.phase === 'download-error' ? 'Повторить скачивание' : status.phase === 'paused' ? 'Продолжить скачивание' : 'Обновить'}</MenuAction>}
    {downloading && <><p role="status">Скачиваем обновление · {status.total ? Math.min(100, Math.floor(100 * (status.completed ?? 0) / status.total)) : 0}%</p><MenuAction disabled={busy} onClick={() => void run(async () => desktop?.cancelDownload?.())}>Отменить скачивание</MenuAction></>}
    {status.phase === 'verifying' && <p role="status">Проверяем скачанные файлы…</p>}
    {ready && <MenuAction className="menu-update-ready" disabled={busy} caption={<><span>{nextVersion ? `Версия ${nextVersion.split('+')[0]}` : 'Новая версия'}</span>{date && <span>Опубликована <time dateTime={date.toISOString()}>{dateLabel}</time></span>}{desktop && <span>Применится при следующем запуске игры.</span>}</>} onClick={() => void run(async () => updateGame(() => true, () => {}))}>{desktop ? 'Перезапустить' : 'Обновить'}</MenuAction>}
    {status.phase === 'download-error' && <p role="alert">{status.message || 'Не удалось скачать обновление.'}</p>}
    {error && <p role="alert">{error}</p>}
    {desktop?.releaseHistory && <MenuAction onClick={() => setHistory(true)}>Что нового</MenuAction>}
    {history && <ReleaseHistory back={() => setHistory(false)} />}
  </div>;
}
function ReleaseHistory({ back }: { back: () => void }) {
  const [items, setItems] = useState<readonly { tag: string; version: string; date: string; notes: string }[]>([]);
  const [selected, setSelected] = useState('');
  const [error, setError] = useState('');
  useEffect(() => {
    let active = true;
    void desktop?.releaseHistory?.().then(values => { if (active) { setItems(values); setSelected(values[0]?.tag ?? ''); } }).catch(() => { if (active) setError('История версий сейчас недоступна. Проверьте соединение и откройте её снова.'); });
    return () => { active = false; };
  }, []);
  const release = items.find(item => item.tag === selected);
  return <MenuDialog wide title="Что нового" back={back} footer={<MenuAction onClick={back}>Назад</MenuAction>}>
    {error ? <p role="status">{error}</p> : !items.length ? <p role="status">Загружаем историю версий…</p> : <>
      <label>Версия<select value={selected} onChange={event => setSelected(event.target.value)}>{items.map(item => <option value={item.tag} key={item.tag}>{item.version} · {item.date ? new Date(item.date).toLocaleDateString('ru-RU') : 'Дата не указана'}</option>)}</select></label>
      {release && <article className="release-notes"><h3>{release.version}</h3><div>{release.notes.split('\n').filter(Boolean).map((line,index) => line.startsWith('### ') ? <h4 key={index}>{line.slice(4)}</h4> : <p key={index}>{line.startsWith('- ') ? `• ${line.slice(2)}` : line}</p>)}</div></article>}
    </>}
  </MenuDialog>;
}
