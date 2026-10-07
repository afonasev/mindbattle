import { MatchSetupFields } from "./MatchSetupFields";
import { MenuAction, ScreenHeader, ScreenSurface } from "./menuUi";
import { PresentationSettings } from "./PresentationSettings";
import { DesktopQuit } from "./DesktopControls";
import { MainMenuUpdate } from "./MainMenuUpdate";
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
  const home = !settingsOpen && !classicSetupOpen;
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
    <ScreenSurface className={`menu-shell ${home ? "menu-home" : "menu-subpage"}`}>
      {home && <div className="menu-scenery" aria-hidden="true"><div className="arena-orbit"><div className="arena-core" /></div><div className="arena-horizon" /></div>}
      <ScreenHeader hero={home} subtitle={home ? "Главное меню" : settingsOpen ? "Настройки" : "На одном устройстве"} back={settingsOpen ? () => setSettingsOpen(false) : classicSetupOpen ? () => setClassicSetupOpen(false) : undefined} />

      {home && (
      <section className="menu-mode-stage" aria-label="Выбор режима">
        <div className="menu-intro"><span className="eyebrow">Интеллектуальная битва</span><p>Все решит эрудиция</p></div>
        <div className="menu-actions main-menu-actions">
          <MenuAction variant="primary" arrow caption="Свой темп. Личный рекорд." onClick={startSolo}>Одиночная игра</MenuAction>
          <MenuAction className="mobile-classic-action" aria-label="На одном устройстве (2–4)" arrow caption="2–4 команды · один общий экран" onClick={() => setClassicSetupOpen(true)}>На одном устройстве</MenuAction>
          <MenuAction className="desktop-network-action" aria-label="Сетевая игра (2–12)" arrow caption="Создать комнату для 2–12 игроков" onClick={enterNetwork}>Сетевая игра</MenuAction>
          <MenuAction className="mobile-network-action" arrow caption="Выбрать игру в сетевом лобби" onClick={enterNetwork}>Подключиться к игре</MenuAction>
          {restoreSolo && <MenuAction arrow caption="Вернуться к сохранённому забегу" onClick={restoreSolo}>Продолжить одиночную игру</MenuAction>}
          {restoreLabel && <MenuAction className="mobile-classic-action" arrow onClick={restore}>{restoreLabel}</MenuAction>}
        </div>
        {error && <p className="menu-error" role="alert">{error}</p>}
      </section>
      )}
      {home && <div className="menu-utilities">
        <MenuAction className="menu-records-action" arrow caption="Лучшие результаты одиночной игры" onClick={viewRecords}>Рекорды</MenuAction>
        <MenuAction arrow onClick={() => setSettingsOpen(true)}>Настройки</MenuAction>
        <MainMenuUpdate />
        <DesktopQuit />
      </div>}

      {classicSetupOpen && (
      <section className="setup-stage mobile-classic-setup" aria-labelledby="setup-title">
        <div className="stage-label">Настройка партии</div>
        <h2 id="setup-title">Классическая игра</h2>
        <MatchSetupFields questionCount={settings.questionCount} answerTimeMs={settings.answerTimeMs} teamCount={settings.teamCount} setQuestionCount={(questionCount) => setSettings({ ...settings, questionCount })} setAnswerTimeMs={(answerTimeMs) => setSettings({ ...settings, answerTimeMs })} setTeamCount={updateTeamCount}>
          <div className="reserve-readout">
            <span>Запас времени</span>
            <strong>{reserveFor(settings.questionCount) / 1000} c</strong>
            <small>для каждой команды</small>
          </div>
        </MatchSetupFields>

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
          <MenuAction variant="primary" className="" disabled={!valid} onClick={start}>Начать игру</MenuAction>

        </div>
        {error && <p className="menu-error" role="alert">{error}</p>}
      </section>
      )}

      {settingsOpen && <PresentationSettings preferences={preferences} setPreferences={setPreferences} session={{ collectQuestionFeedback: settings.collectQuestionFeedback, setCollectQuestionFeedback: (value) => setSettings({ ...settings, collectQuestionFeedback: value }), resetHistory }} />}
    </ScreenSurface>
  );
}
