import type { AccessibilityPreferences } from "../adapters/storage";

export function PresentationSettings({ preferences, setPreferences, back }: {
  readonly preferences: AccessibilityPreferences;
  readonly setPreferences: (preferences: AccessibilityPreferences) => void;
  readonly back: () => void;
}) {
  return <section className="setup-stage menu-settings-stage" aria-labelledby="menu-settings-title">
    <div className="settings-stage-heading">
      <div>
        <span className="stage-label">Панель управления</span>
        <h2 id="menu-settings-title">Настройки</h2>
        <p>Сделайте партию комфортной, не меняя её правил.</p>
      </div>
      <button className="secondary-action settings-back" type="button" onClick={back}>Назад</button>
    </div>
    <div className="settings-grid">
      <section className="settings-group" aria-labelledby="sound-settings-title">
        <h3 id="sound-settings-title">Звук</h3>
        <button className={`settings-toggle ${preferences.muted ? "" : "is-active"}`} type="button" aria-pressed={!preferences.muted} onClick={() => setPreferences({ ...preferences, muted: !preferences.muted })}>
          {preferences.muted ? "Звук выключен" : "Звук включён"}
        </button>
        <label className="settings-range">
          <span>Громкость <strong>{Math.round(preferences.volume * 100)}%</strong></span>
          <input aria-label="Громкость" type="range" min="0" max="1" step="0.1" value={preferences.volume} onChange={(event) => setPreferences({ ...preferences, volume: Number(event.target.value) })} />
        </label>
      </section>
      <section className="settings-group" aria-labelledby="display-settings-title">
        <h3 id="display-settings-title">Отображение</h3>
        <label className="settings-check"><input type="checkbox" checked={preferences.textSize === "large"} onChange={(event) => setPreferences({ ...preferences, textSize: event.target.checked ? "large" : "normal" })} /><span>Крупный текст</span></label>
        <label className="settings-check"><input type="checkbox" checked={preferences.highContrast} onChange={(event) => setPreferences({ ...preferences, highContrast: event.target.checked })} /><span>Высокий контраст</span></label>
        <label className="settings-check"><input type="checkbox" checked={preferences.reducedMotion} onChange={(event) => setPreferences({ ...preferences, reducedMotion: event.target.checked })} /><span>Без анимации</span></label>
      </section>
    </div>
  </section>;
}
