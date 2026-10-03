import { MenuAction, MenuDialog } from "./menuUi";
import { DesktopDisplaySettings } from "./DesktopControls";
import type { AccessibilityPreferences } from "../adapters/storage";

export function PresentationSettings({ preferences, setPreferences, back, session }: {
  readonly preferences: AccessibilityPreferences;
  readonly setPreferences: (preferences: AccessibilityPreferences) => void;
  readonly back?: () => void;
  readonly session?: { readonly collectQuestionFeedback: boolean; readonly setCollectQuestionFeedback: (value: boolean) => void; readonly resetHistory: () => void };
}) {
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
        <button className={`settings-toggle ${preferences.muted ? "" : "is-active"}`} type="button" aria-pressed={!preferences.muted} onClick={() => setPreferences({ ...preferences, muted: !preferences.muted })}>
          {preferences.muted ? "Звук выключен" : "Звук включён"}
        </button>
        <label className="settings-range">
          <span>Музыка <strong>{Math.round(preferences.musicVolume * 100)}%</strong></span>
          <input aria-label="Громкость музыки" type="range" min="0" max="1" step="0.1" value={preferences.musicVolume} onChange={(event) => setPreferences({ ...preferences, musicVolume: Number(event.target.value) })} />
        </label>
        <label className="settings-range">
          <span>Эффекты <strong>{Math.round(preferences.effectsVolume * 100)}%</strong></span>
          <input aria-label="Громкость эффектов" type="range" min="0" max="1" step="0.1" value={preferences.effectsVolume} onChange={(event) => setPreferences({ ...preferences, effectsVolume: Number(event.target.value) })} />
        </label>
      </section>
      <section className="settings-group" aria-labelledby="display-settings-title">
        <h3 id="display-settings-title">Отображение</h3>
        <label className="settings-check"><input type="checkbox" checked={preferences.textSize === "large"} onChange={(event) => setPreferences({ ...preferences, textSize: event.target.checked ? "large" : "normal" })} /><span>Крупный текст</span></label>
        <label className="settings-check"><input type="checkbox" checked={preferences.highContrast} onChange={(event) => setPreferences({ ...preferences, highContrast: event.target.checked })} /><span>Высокий контраст</span></label>
        <label className="settings-check"><input type="checkbox" checked={preferences.reducedMotion} onChange={(event) => setPreferences({ ...preferences, reducedMotion: event.target.checked })} /><span>Без анимации</span></label>
      </section>
      {session && <section className="settings-group settings-group--session" aria-labelledby="session-settings-title"><h3 id="session-settings-title">Партия и история</h3><label className="settings-check"><input type="checkbox" checked={session.collectQuestionFeedback} onChange={(event) => session.setCollectQuestionFeedback(event.target.checked)} /><span>Собирать обратную связь по вопросам</span></label><MenuAction onClick={session.resetHistory}>Сбросить историю вопросов</MenuAction></section>}
    </div>
  </section>;
}

export function SettingsDialog(props: Parameters<typeof PresentationSettings>[0] & { readonly back: () => void }) {
  return <MenuDialog wide title="Настройки" back={props.back}><PresentationSettings {...props} /></MenuDialog>;
}
