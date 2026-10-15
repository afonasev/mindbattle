import { MenuAction, MenuDialog } from "./menuUi";
import { useEffect, useState } from "react";
import { desktop, type DisplaySettings } from "../desktop";
export function DesktopQuit() {
  return desktop ? <MenuAction onClick={() => void desktop?.quit()}>Выход из игры</MenuAction> : null;
}
export function DesktopDisplaySettings() {
  const [value, setValue] = useState<DisplaySettings>();
  const [options, setOptions] = useState<readonly {width:number;height:number}[]>([]);
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);
  const [trial, setTrial] = useState(false);
  const [remaining, setRemaining] = useState(15);
  useEffect(() => {
    void desktop?.display().then(setValue).catch(() => setError('Не удалось загрузить настройки экрана.'));
    void desktop?.displayOptions?.().then(setOptions).catch(() => setError('Не удалось получить доступные размеры окна.'));
  }, []);
  useEffect(() => {
    if (!trial) return;
    const timer = setInterval(() => setRemaining(left => Math.max(0, left - 1)), 1000);
    return () => clearInterval(timer);
  }, [trial]);
  useEffect(() => { if (trial && remaining === 0) void finish(false); }, [remaining, trial]);
  useEffect(() => { const reset = () => { void preview({ width:1280,height:720,fullscreen:false,auto:true }); }; window.addEventListener('reset-desktop-display', reset); return () => window.removeEventListener('reset-desktop-display', reset); }, []);
  if (!desktop) return null;
  async function preview(next: DisplaySettings) {
    if (busy) return;
    setBusy(true); setError('');
    try { setValue(await desktop!.setDisplay(next)); setRemaining(15); setTrial(true); }
    catch { setError('Не удалось изменить настройки экрана.'); }
    finally { setBusy(false); }
  }
  async function finish(confirm: boolean) {
    if (busy) return;
    setBusy(true);
    try { const saved = confirm ? await desktop?.confirmDisplay?.() : await desktop?.cancelDisplay?.(); if (saved) setValue(saved); }
    catch { setError('Не удалось сохранить режим экрана. Восстановлен прежний режим.'); const saved = await desktop?.display(); if (saved) setValue(saved); }
    finally { setBusy(false); setTrial(false); }
  }
  return <section className="settings-group" aria-labelledby="desktop-display-title"><h3 id="desktop-display-title">Экран</h3>
    {value && <>
      <label className="desktop-setting">Режим экрана<select aria-label="Режим экрана" disabled={busy} value={value.fullscreen ? 'full' : 'window'} onChange={event => void preview({...value,fullscreen:event.target.value==='full'})}><option value="window">Оконный</option><option value="full">Полный экран</option></select></label>
      <label className="desktop-setting">Разрешение окна<select aria-label="Разрешение окна" disabled={busy || value.fullscreen} value={value.auto ? 'auto' : `${value.width}x${value.height}`} onChange={event => { if(event.target.value==='auto') void preview({...value,auto:true}); else { const [width,height]=event.target.value.split('x').map(Number); void preview({...value,width,height,auto:false}); } }}><option value="auto">Auto</option>{options.map(size => <option key={`${size.width}x${size.height}`} value={`${size.width}x${size.height}`}>{size.width} × {size.height}</option>)}</select></label>
      {value.fullscreen && <p>Полный экран использует разрешение монитора.</p>}
      <MenuAction onClick={() => void preview({width:1280,height:720,fullscreen:false,auto:true})}>Сбросить экран</MenuAction>
    </>}
    {busy && <p role="status">Применяем режим экрана…</p>}
    {error && <p role="alert">{error}</p>}
    {trial && <MenuDialog title="Сохранить режим экрана?" back={() => void finish(false)}><p>Без подтверждения прежний режим восстановится через {remaining} с.</p><MenuAction disabled={busy} onClick={() => void finish(true)}>Сохранить режим</MenuAction><MenuAction disabled={busy} onClick={() => void finish(false)}>Отменить</MenuAction></MenuDialog>}
  </section>;
}
