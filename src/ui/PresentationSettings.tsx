import { ControlsHelp } from "./ControlsHelp";
import { useState } from "react";
import { DEFAULT_PREFERENCES, decodePreferences, STORAGE_KEY } from "../adapters/storage";
import { useStatistics } from './useStatistics';
import { MenuAction, MenuDialog } from "./menuUi";
import { DesktopDisplaySettings } from "./DesktopControls";
import type { AccessibilityPreferences } from "../adapters/storage";

export function PresentationSettings({ preferences, setPreferences, back, session }: {
  readonly preferences: AccessibilityPreferences;
  readonly setPreferences: (preferences: AccessibilityPreferences) => void;
  readonly back?: () => void;
  readonly session?: { readonly resetHistory: () => void };
}) {
  const statistics = useStatistics();
  const [error, setError] = useState("");
  const [reset, setReset] = useState<"sound" | "display" | "all" | "history">();
  const [help, setHelp] = useState(false);
  const change = (next: AccessibilityPreferences) => {
    try {
      const latest = decodePreferences(JSON.parse(localStorage.getItem(STORAGE_KEY) || "null")?.preferences) ?? preferences;
      const changed = Object.fromEntries(Object.entries(next).filter(([key,value]) => value !== preferences[key as keyof AccessibilityPreferences]));
      setPreferences({ ...latest, ...changed }); window.dispatchEvent(new Event("preferences-changed")); setError(""); } catch (cause) { setError(cause instanceof Error ? cause.message : "Не удалось сохранить настройки."); }
  };
  const resetValues = () => {
    if (reset === "history") {
      try { session?.resetHistory(); setError(""); } catch { setError("Не удалось очистить историю. Попробуйте снова."); }
    } else if (reset === "sound") change({ ...preferences, masterVolume: 1, musicVolume: DEFAULT_PREFERENCES.musicVolume, effectsVolume: DEFAULT_PREFERENCES.effectsVolume, muted: false });
    else if (reset === "display") change({ ...preferences, textSize: DEFAULT_PREFERENCES.textSize, highContrast: false, reducedMotion: false, showFps: false });
    else { change({ ...DEFAULT_PREFERENCES }); window.dispatchEvent(new Event("reset-desktop-display")); }
    setReset(undefined);
  };
  return <section className="setup-stage menu-settings-stage" aria-labelledby="menu-settings-title">
    <div className="settings-stage-heading">
      <div>
        <span className="stage-label">Панель управления</span>
        <h2 id="menu-settings-title">Настройки</h2>
        <p>Сделайте партию комфортной, не меняя её правил.</p>
      </div>
      {back && <MenuAction className="settings-back navigation-action" onClick={back}>Назад</MenuAction>}
    </div>
    <div className="settings-grid">
            <DesktopDisplaySettings />
      <section className="settings-group" aria-labelledby="sound-settings-title">
        <h3 id="sound-settings-title">Звук</h3>
        <label className="settings-range"><span>Общая громкость <strong>{Math.round((preferences.masterVolume ?? 1) * 100)}%</strong></span><input aria-label="Общая громкость" type="range" min="0" max="1" step="0.1" value={preferences.masterVolume ?? 1} onChange={event => change({ ...preferences, masterVolume: Number(event.target.value), muted: false })} /></label>
        <label className="settings-range">
          <span>Музыка <strong>{Math.round(preferences.musicVolume * 100)}%</strong></span>
          <input aria-label="Громкость музыки" type="range" min="0" max="1" step="0.1" value={preferences.musicVolume} onChange={(event) => change({ ...preferences, musicVolume: Number(event.target.value) })} />
        </label>
        <label className="settings-range">
          <span>Эффекты <strong>{Math.round(preferences.effectsVolume * 100)}%</strong></span>
          <input aria-label="Громкость эффектов" type="range" min="0" max="1" step="0.1" value={preferences.effectsVolume} onChange={(event) => change({ ...preferences, effectsVolume: Number(event.target.value) })} />
        </label>
        <MenuAction onClick={() => setReset("sound")}>Сбросить звук</MenuAction>
      </section>
      <section className="settings-group" aria-labelledby="display-settings-title">
        <h3 id="display-settings-title">Отображение</h3>
        <label className="settings-check"><input type="checkbox" checked={preferences.textSize === "large"} onChange={(event) => change({ ...preferences, textSize: event.target.checked ? "large" : "normal" })} /><span>Крупный текст</span></label>
        <label className="settings-check"><input type="checkbox" checked={preferences.highContrast} onChange={(event) => change({ ...preferences, highContrast: event.target.checked })} /><span>Высокий контраст</span></label>
        <label className="settings-check"><input type="checkbox" checked={preferences.reducedMotion} onChange={(event) => change({ ...preferences, reducedMotion: event.target.checked })} /><span>Без анимации</span></label>
        <label className="settings-check"><input type="checkbox" checked={preferences.showFps === true} onChange={event => change({ ...preferences, showFps: event.target.checked })} /><span>Счётчик FPS</span></label>
        <MenuAction onClick={() => setReset("display")}>Сбросить отображение</MenuAction>
      </section>
      <section className="settings-group"><h3>Управление</h3><MenuAction onClick={() => setHelp(true)}>Справка по управлению</MenuAction></section>
      <section className="settings-group" aria-labelledby="statistics-settings-title"><h3 id="statistics-settings-title">Статистика</h3><label className="settings-check"><input type="checkbox" checked={statistics.enabled} disabled={statistics.pending} aria-describedby="statistics-description" onChange={event => void statistics.setEnabled(event.target.checked)} /><span>Отправлять анонимную статистику</span></label><p id="statistics-description">Помогает улучшать вопросы и баланс игры. Без имён и данных устройства.</p><p>После включения сбор начнётся с новых матчей. Жалобы и локальные рекорды доступны всегда.</p>{statistics.error && <p role="alert">{statistics.error}</p>}</section>
      {session && <section className="settings-group settings-group--session" aria-labelledby="session-settings-title"><h3 id="session-settings-title">Партия и история</h3><MenuAction onClick={() => setReset("history")}>Сбросить историю вопросов</MenuAction></section>}
    </div>
    <div className="settings-stage-footer">{error && <p role="alert">{error}</p>}<MenuAction onClick={() => setReset("all")}>Сбросить все настройки</MenuAction></div>
    {reset && <MenuDialog title={reset === "history" ? "Сбросить историю вопросов?" : reset === "sound" ? "Сбросить звук?" : reset === "display" ? "Сбросить отображение?" : "Сбросить все настройки?"} back={() => setReset(undefined)}><p>{reset === "history" ? "Очистится только локальная история вопросов. Текущая партия, рекорды и согласие на статистику сохранятся." : "Статистика, история вопросов, прогресс и рекорды сохранятся."}</p><MenuAction onClick={resetValues}>Сбросить</MenuAction><MenuAction onClick={() => setReset(undefined)}>Отменить</MenuAction></MenuDialog>}
    {help && <ControlsHelp back={() => setHelp(false)} />}
  </section>;
}

export function SettingsDialog(props: Parameters<typeof PresentationSettings>[0] & { readonly back: () => void }) {
  return <MenuDialog wide title="Настройки" back={props.back}><PresentationSettings {...props} /></MenuDialog>;
}
