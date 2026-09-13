import { useState } from "react";
import type {
  AccessibilityPreferences,
  ControlSource,
  TeamControlAssignment
} from "../adapters";
import { assignControlSource, assignmentsAreCompleteAndUnique } from "../adapters";
import { detectGamepadProfile } from "../adapters";
import { reserveFor, TEAM_IDS, type MatchConfig, type TeamId } from "../domain";
import { TEAM_META, TeamDiamond } from "./gameUi";

export interface MenuSettings {
  readonly questionCount: MatchConfig["questionCount"];
  readonly answerTimeMs: MatchConfig["answerTimeMs"];
  readonly teamCount: 2 | 3 | 4;
  readonly assignments: readonly TeamControlAssignment[];
  readonly collectQuestionFeedback: boolean;
}

export const DEFAULT_MENU_SETTINGS: MenuSettings = {
  questionCount: 15,
  answerTimeMs: 20_000,
  teamCount: 2,
  collectQuestionFeedback: true,
  assignments: [
    { teamId: "green", source: { kind: "keyboard", layout: "wasd" } },
    { teamId: "blue", source: { kind: "keyboard", layout: "arrows" } }
  ]
};

function sourceValue(source: ControlSource): string {
  return source.kind === "keyboard" ? source.layout : `gamepad:${source.index}`;
}

export function MenuScreen({
  settings,
  setSettings,
  preferences,
  setPreferences,
  gamepads,
  start,
  startSolo,
  enterNetwork,
  restoreSolo,
  restoreLabel,
  restore,
  viewRecords,
  resetHistory,
  error
}: {
  readonly settings: MenuSettings;
  readonly setSettings: (settings: MenuSettings) => void;
  readonly preferences: AccessibilityPreferences;
  readonly setPreferences: (preferences: AccessibilityPreferences) => void;
  readonly gamepads: readonly Gamepad[];
  readonly start: () => void;
  readonly startSolo: () => void;
  readonly enterNetwork: () => void;
  readonly restoreSolo: (() => void) | null;
  readonly restoreLabel: string | null;
  readonly restore: () => void;
  readonly viewRecords: () => void;
  readonly resetHistory: () => void;
  readonly error: string | null;
}) {
  const [settingsOpen, setSettingsOpen] = useState(false);
  const [classicSetupOpen, setClassicSetupOpen] = useState(false);
  const activeTeams = TEAM_IDS.slice(0, settings.teamCount);
  const valid = assignmentsAreCompleteAndUnique(activeTeams, settings.assignments);
  const updateTeamCount = (teamCount: 2 | 3 | 4) => {
    const teams = TEAM_IDS.slice(0, teamCount);
    setSettings({
      ...settings,
      teamCount,
      assignments: settings.assignments.filter(({ teamId }) => (teams as readonly string[]).includes(teamId))
    });
  };
  const updateAssignment = (teamId: TeamId, value: string) => {
    let source: ControlSource | null = null;
    if (value === "wasd" || value === "arrows") {
      source = { kind: "keyboard", layout: value };
    } else if (value.startsWith("gamepad:")) {
      const index = Number(value.slice("gamepad:".length));
      const gamepad = gamepads.find((candidate) => candidate.index === index);
      if (gamepad) {
        source = {
          kind: "gamepad",
          index,
          id: gamepad.id,
          profile: detectGamepadProfile(gamepad.id, gamepad.mapping)
        };
      }
    }
    if (!source) {
      setSettings({
        ...settings,
        assignments: settings.assignments.filter((assignment) => assignment.teamId !== teamId)
      });
      return;
    }
    const result = assignControlSource(settings.assignments, teamId, source);
    if (result.ok) setSettings({ ...settings, assignments: result.assignments });
  };

  return (
    <main className="menu-shell">
      <div className="arena-glow" aria-hidden="true" />
      <header className="brand-lockup brand-lockup--menu">
        <span className="eyebrow">Интеллектуальная битва</span>
        <h1>Mindbattle</h1>
        <p>Все решит эрудиция</p>
      </header>

      {!settingsOpen && !classicSetupOpen && (
      <section className="setup-stage menu-mode-stage" aria-label="Выбор режима">
        <div className="menu-actions">
          <button className="secondary-action" type="button" onClick={startSolo}>Одиночная игра</button>
          <button className="secondary-action mobile-classic-action" type="button" onClick={() => setClassicSetupOpen(true)}>На одном устройстве (2–4)</button>
          <a className="secondary-action network-menu-desktop" href="/network" onClick={(event) => { event.preventDefault(); enterNetwork(); }}>Сетевая игра (2–12)</a>
          <a className="secondary-action network-menu-mobile" href="/network" onClick={(event) => { event.preventDefault(); enterNetwork(); }}>Сетевая игра (2–12)</a>
          {restoreSolo && <button className="secondary-action" type="button" onClick={restoreSolo}>Продолжить одиночную игру</button>}
          {restoreLabel && <button className="secondary-action mobile-classic-action" type="button" onClick={restore}>{restoreLabel}</button>}
          <button className="secondary-action" type="button" onClick={() => setSettingsOpen(true)}>Настройки</button>
          <button className="secondary-action" type="button" onClick={viewRecords}>Рекорды</button>
        </div>
        {error && <p className="menu-error" role="alert">{error}</p>}
      </section>
      )}

      {classicSetupOpen && (
      <section className="setup-stage mobile-classic-setup" aria-labelledby="setup-title">
        <div className="stage-label">Настройка партии</div>
        <h2 id="setup-title">Классическая игра</h2>
        <div className="segmented-settings">
          <fieldset>
            <legend>Вопросов</legend>
            {[9, 15, 21].map((value) => (
              <button
                className={settings.questionCount === value ? "is-selected" : ""}
                key={value}
                type="button"
                onClick={() => setSettings({ ...settings, questionCount: value as 9 | 15 | 21 })}
              >
                {value}
              </button>
            ))}
          </fieldset>
          <fieldset>
            <legend>Команд</legend>
            {[2, 3, 4].map((value) => (
              <button
                className={settings.teamCount === value ? "is-selected" : ""}
                key={value}
                type="button"
                onClick={() => updateTeamCount(value as 2 | 3 | 4)}
              >
                {value}
              </button>
            ))}
          </fieldset>
          <fieldset>
            <legend>На ответ</legend>
            {[10, 20, 30].map((value) => (
              <button
                className={settings.answerTimeMs === value * 1000 ? "is-selected" : ""}
                key={value}
                type="button"
                onClick={() =>
                  setSettings({
                    ...settings,
                    answerTimeMs: (value * 1000) as 10_000 | 20_000 | 30_000
                  })
                }
              >
                {value} c
              </button>
            ))}
          </fieldset>
          <div className="reserve-readout">
            <span>Запас времени</span>
            <strong>{reserveFor(settings.questionCount) / 1000} c</strong>
            <small>для каждой команды</small>
          </div>
        </div>

        <div className="controller-grid">
          {activeTeams.map((teamId) => {
            const assignment = settings.assignments.find((item) => item.teamId === teamId);
            return (
              <label className={`controller-card team-color--${teamId}`} key={teamId}>
                <TeamDiamond teamId={teamId} />
                <span>{TEAM_META[teamId].label}</span>
                <select
                  aria-label={`Контроллер команды ${TEAM_META[teamId].label}`}
                  value={assignment ? sourceValue(assignment.source) : ""}
                  onChange={(event) => updateAssignment(teamId, event.target.value)}
                >
                  <option value="">Выберите управление</option>
                  <option value="wasd">WASD</option>
                  <option value="arrows">Стрелки</option>
                  {gamepads.map((gamepad) => (
                    <option key={gamepad.index} value={`gamepad:${gamepad.index}`}>
                      Геймпад {gamepad.index + 1}
                    </option>
                  ))}
                </select>
              </label>
            );
          })}
        </div>

        <div className="menu-actions">
          <button className="primary-action" type="button" disabled={!valid} onClick={start}>Начать игру</button>
          <button className="secondary-action" type="button" onClick={() => setClassicSetupOpen(false)}>Назад к режимам</button>
        </div>
        {error && <p className="menu-error" role="alert">{error}</p>}
      </section>
      )}

      {settingsOpen && (
        <section className="setup-stage menu-settings-stage" aria-labelledby="menu-settings-title">
          <div className="settings-stage-heading">
            <div>
              <span className="stage-label">Панель управления</span>
              <h2 id="menu-settings-title">Настройки</h2>
              <p>Сделайте партию комфортной, не меняя её правил.</p>
            </div>
            <button className="secondary-action settings-back" type="button" onClick={() => setSettingsOpen(false)}>Назад</button>
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
            <section className="settings-group settings-group--session" aria-labelledby="session-settings-title">
              <h3 id="session-settings-title">Партия и история</h3>
              <label className="settings-check"><input type="checkbox" checked={settings.collectQuestionFeedback} onChange={(event) => setSettings({ ...settings, collectQuestionFeedback: event.target.checked })} /><span>Собирать обратную связь по вопросам</span></label>
              <button className="settings-reset" type="button" onClick={resetHistory}>Сбросить историю вопросов</button>
            </section>
          </div>
        </section>
      )}
      <footer>Локально · Offline-first · один общий экран</footer>
    </main>
  );
}
