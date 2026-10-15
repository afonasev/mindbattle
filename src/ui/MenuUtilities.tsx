import { useEffect, useState } from 'react';
import { MenuAction, MenuDialog } from './menuUi';
import { DEFAULT_PREFERENCES, decodePreferences, STORAGE_KEY } from '../adapters/storage';

export function FpsCounter() {
  const read = () => { try { return (decodePreferences(JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}')?.preferences) ?? DEFAULT_PREFERENCES).showFps === true; } catch { return false; } };
  const [enabled, setEnabled] = useState(read);
  const [fps, setFps] = useState(0);
  useEffect(() => { const sync = () => setEnabled(read()); window.addEventListener('preferences-changed', sync); window.addEventListener('storage', sync); return () => { window.removeEventListener('preferences-changed', sync); window.removeEventListener('storage', sync); }; }, []);
  useEffect(() => {
    if (!enabled) return;
    let frame = 0, count = 0, then = performance.now();
    const tick = (now: number) => { count++; if (now - then >= 500) { setFps(Math.round(count * 1000 / (now - then))); then = now; count = 0; } frame = requestAnimationFrame(tick); };
    frame = requestAnimationFrame(tick); return () => cancelAnimationFrame(frame);
  }, [enabled]);
  return enabled ? <output className="fps-counter">{fps} FPS</output> : null;
}

export function GamepadKeyboard() {
  const [target, setTarget] = useState<HTMLInputElement | HTMLTextAreaElement>();
  const [draft, setDraft] = useState('');
  const [layout, setLayout] = useState<'ru' | 'en' | 'symbols'>('ru');
  const [upper, setUpper] = useState(false);
  useEffect(() => {
    const open = (event: Event) => { const input = (event as CustomEvent<HTMLInputElement | HTMLTextAreaElement>).detail; setTarget(input); setDraft(input.value); };
    window.addEventListener('menu-edit-text', open); return () => window.removeEventListener('menu-edit-text', open);
  }, []);
  if (!target) return null;
  const close = () => { setTarget(undefined); target.focus(); };
  const chars = layout === 'ru' ? 'йцукенгшщзхъфывапролджэячсмитьбюё' : layout === 'en' ? 'qwertyuiopasdfghjklzxcvbnm' : '0123456789!@#$%^&*()_+-=[]{};:,.?/\\|<>~`\'"';
  const write = (value: string) => setDraft(value.slice(0, target.maxLength > 0 ? target.maxLength : 1000));
  const commit = () => {
    const proto = target instanceof HTMLTextAreaElement ? HTMLTextAreaElement.prototype : HTMLInputElement.prototype;
    Object.getOwnPropertyDescriptor(proto, 'value')?.set?.call(target, draft);
    target.dispatchEvent(new Event('input', { bubbles: true }));
    target.dispatchEvent(new Event('change', { bubbles: true }));
    close();
  };
  return <MenuDialog wide title="Ввод текста" back={close} footer={<div className="help-tabs"><MenuAction onClick={() => write(draft + ' ')}>Пробел</MenuAction><MenuAction onClick={() => write(draft.slice(0,-1))}>Стереть</MenuAction><MenuAction onClick={commit}>Готово</MenuAction><MenuAction onClick={close}>Отменить</MenuAction></div>}>
    <output className="keyboard-preview">{target.type === 'password' ? '•'.repeat(draft.length) : draft || ' '}</output>
    <div className="help-tabs"><MenuAction onClick={() => setLayout('ru')}>АБВ</MenuAction><MenuAction onClick={() => setLayout('en')}>ABC</MenuAction><MenuAction onClick={() => setLayout('symbols')}>123</MenuAction><MenuAction onClick={() => setUpper(!upper)}>Регистр</MenuAction></div>
    <div className="gamepad-keyboard">{[...chars].map(char => <MenuAction key={char} onClick={() => write(draft + (upper ? char.toUpperCase() : char))}>{upper ? char.toUpperCase() : char}</MenuAction>)}</div>
  </MenuDialog>;
}
