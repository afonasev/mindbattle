import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import {
  AudioController,
  createInputRouterState,
  createWebAudioSink,
  disarmUntilNeutral,
  handleGamepadPoll,
  handleKeyboardInput,
  handleWindowBlur,
  type GamepadSnapshot,
  type SemanticInputAction
} from "../adapters";
import { GameController } from "../application";
import { HttpDifficultyFeedbackSink } from "../feedback";
import { assertFullCatalog, catalog, TOPIC_TITLE_BY_ID } from "../content";
import {
  selectStandings,
  type AnswerPosition,
  type DomainCommand,
  type MatchState,
  type TeamId
} from "../domain";
import { DEFAULT_MENU_SETTINGS, MenuScreen, type MenuSettings } from "./MenuScreen";
import {
  BonusVeto,
  DifficultyFeedbackScreen,
  PauseOverlay,
  QuestionBoard,
  Standings,
  TEAM_META,
  TeamCards,
  TopicConfirmation,
  TopicSelection
} from "./gameUi";

const toPosition = {
  north: "up",
  east: "right",
  south: "down",
  west: "left"
} as const;

function nextSeed(): string {
  const value = crypto.getRandomValues(new Uint32Array(2));
  return `${value[0].toString(16)}-${value[1].toString(16)}`;
}

function gamepadSnapshots(): readonly GamepadSnapshot[] {
  return [...navigator.getGamepads()]
    .filter((item): item is Gamepad => item !== null)
    .map((gamepad) => ({
      index: gamepad.index,
      id: gamepad.id,
      mapping: gamepad.mapping,
      connected: gamepad.connected,
      buttons: gamepad.buttons.map(({ pressed }) => pressed)
    }));
}

export function App() {
  const controller = useMemo(
    () =>
      new GameController({
        catalog,
        storage: localStorage,
        clock: {
          now: () => performance.now(),
          wallTime: () => new Date().toISOString()
        },
        seeds: { nextSeed },
        feedback: new HttpDifficultyFeedbackSink()
      }),
    []
  );
  const [settings, setSettings] = useState<MenuSettings>(DEFAULT_MENU_SETTINGS);
  const [preferences, setPreferences] = useState(controller.preferences);
  const [match, setMatch] = useState<MatchState | null>(controller.state);
  const [menuError, setMenuError] = useState<string | null>(null);
  const [gamepads, setGamepads] = useState<readonly Gamepad[]>([]);
  const inputRef = useRef(createInputRouterState());
  const phaseRef = useRef<string | null>(null);
  const audioRef = useRef(new AudioController(createWebAudioSink(), preferences));

  const sync = useCallback(
    () => setMatch(controller.state ? { ...controller.state } : null),
    [controller]
  );
  const dispatch = useCallback(
    (commands: readonly DomainCommand[]) => {
      controller.dispatch(commands);
      sync();
    },
    [controller, sync]
  );

  const start = useCallback(() => {
    try {
      assertFullCatalog();
      const teams = ["green", "blue", "yellow", "red"].slice(0, settings.teamCount) as TeamId[];
      controller.updateControlAssignments(settings.assignments);
      controller.start({
        profile: "classic-v1",
        questionCount: settings.questionCount,
        answerTimeMs: settings.answerTimeMs,
        teams
      });
      inputRef.current = createInputRouterState(false);
      setMenuError(null);
      sync();
    } catch (error) {
      setMenuError(
        error instanceof Error ? error.message.split("\n")[0] : "Не удалось начать игру"
      );
    }
  }, [controller, settings, sync]);

  const restart = useCallback(() => {
    try {
      controller.restart();
      inputRef.current = createInputRouterState(false);
      sync();
    } catch (error) {
      setMenuError(error instanceof Error ? error.message : "Не удалось начать заново");
      setMatch(null);
    }
  }, [controller, sync]);

  useEffect(() => {
    const update = () =>
      setGamepads([...navigator.getGamepads()].filter((item): item is Gamepad => item !== null));
    update();
    window.addEventListener("gamepadconnected", update);
    window.addEventListener("gamepaddisconnected", update);
    return () => {
      window.removeEventListener("gamepadconnected", update);
      window.removeEventListener("gamepaddisconnected", update);
    };
  }, []);

  const semanticToDomain = useCallback((actions: readonly SemanticInputAction[]): DomainCommand[] => {
    return actions.flatMap((action): DomainCommand[] => {
      if (action.type === "answer") {
        return [{
          type: "answer",
          teamId: action.teamId as TeamId,
          position: toPosition[action.direction] as AnswerPosition
        }];
      }
      if (action.type === "topic-move") {
        return [{ type: "move-topic", teamId: action.teamId as TeamId, delta: action.delta }];
      }
      if (action.type === "topic-confirm") {
        return [{ type: "confirm-topic", teamId: action.teamId as TeamId }];
      }
      if (action.type === "bonus-move") {
        return [{ type: "move-veto", teamId: action.teamId as TeamId, delta: action.delta }];
      }
      if (action.type === "bonus-confirm") {
        return [{ type: "set-veto", teamId: action.teamId as TeamId }];
      }
      if (action.type === "bonus-cancel") {
        return [{ type: "clear-veto", teamId: action.teamId as TeamId }];
      }
      if (action.type === "continue") {
        return [{ type: "continue", teamId: action.teamId as TeamId }];
      }
      if (action.type === "difficulty-rating") {
        void controller
          .rateDifficulty(action.teamId as TeamId, action.difficulty)
          .finally(sync);
        queueMicrotask(sync);
        return [];
      }
      if (action.type === "pause") {
        return [{
          type: "pause",
          reason:
            action.reason === "gamepad-disconnected"
              ? { kind: "controller-disconnected", teamId: action.teamId as TeamId }
              : action.reason === "blur"
                ? { kind: "focus-lost" }
                : { kind: "manual" }
        }];
      }
      if (action.type === "gamepad-reconnected") {
        setSettings((current) => ({
          ...current,
          assignments: (() => {
            const assignments = [
              ...current.assignments.filter(({ teamId }) => teamId !== action.teamId),
              { teamId: action.teamId, source: action.source }
            ];
            controller.updateControlAssignments(assignments);
            return assignments;
          })()
        }));
      }
      return [];
    });
  }, [controller, sync]);

  useEffect(() => {
    if (!match) return;
    const mode =
      match.phase.kind === "answering"
        ? "answer"
        : match.phase.kind === "normal-topic"
          ? "normal-topic"
        : match.phase.kind === "bonus-veto"
          ? "bonus-veto"
          : match.phase.kind === "difficulty-feedback"
            ? "difficulty-feedback"
          : "continue";
    const keyboard = (event: KeyboardEvent) => {
      const result = handleKeyboardInput(
        inputRef.current,
        {
          type: event.type as "keydown" | "keyup",
          code: event.code,
          repeat: event.repeat
        },
        settings.assignments,
        mode
      );
      inputRef.current = result.state;
      if (result.actions.length > 0) event.preventDefault();
      const commands = semanticToDomain(result.actions);
      if (commands.length > 0) {
        dispatch(commands);
      }
    };
    const blur = () => {
      const result = handleWindowBlur(inputRef.current);
      inputRef.current = result.state;
      dispatch(semanticToDomain(result.actions));
    };
    window.addEventListener("keydown", keyboard);
    window.addEventListener("keyup", keyboard);
    window.addEventListener("blur", blur);
    return () => {
      window.removeEventListener("keydown", keyboard);
      window.removeEventListener("keyup", keyboard);
      window.removeEventListener("blur", blur);
    };
  }, [dispatch, match, semanticToDomain, settings.assignments]);

  useEffect(() => {
    if (!match) return;
    let frame = 0;
    const poll = () => {
      const current = controller.state;
      if (!current) return;
      const mode =
        current.phase.kind === "answering"
          ? "answer"
          : current.phase.kind === "normal-topic"
            ? "normal-topic"
          : current.phase.kind === "bonus-veto"
            ? "bonus-veto"
            : current.phase.kind === "difficulty-feedback"
              ? "difficulty-feedback"
            : "continue";
      const disconnected = current.pause?.reasons.find(
        (reason) => reason.kind === "controller-disconnected"
      );
      const result = handleGamepadPoll(
        inputRef.current,
        gamepadSnapshots(),
        settings.assignments,
        mode,
        disconnected?.kind === "controller-disconnected" ? disconnected.teamId : undefined
      );
      inputRef.current = result.state;
      const commands = semanticToDomain(result.actions);
      if (commands.length > 0) dispatch(commands);
      frame = requestAnimationFrame(poll);
    };
    frame = requestAnimationFrame(poll);
    return () => cancelAnimationFrame(frame);
  }, [controller, dispatch, match, semanticToDomain, settings.assignments]);

  useEffect(() => {
    if (
      !match ||
      match.pause ||
      (match.phase.kind !== "answering" && match.phase.kind !== "topic-confirmation")
    ) return;
    const timer = window.setInterval(() => {
      controller.tick();
      sync();
    }, 100);
    return () => window.clearInterval(timer);
  }, [controller, match, sync]);

  useEffect(() => {
    const phase = match?.phase.kind ?? null;
    if (phase && phase !== phaseRef.current) {
      inputRef.current = disarmUntilNeutral(inputRef.current);
      if (phase === "answering") audioRef.current.play("question-start");
      if (phase === "bonus-veto") audioRef.current.play("bonus");
      if (phase === "reveal") audioRef.current.play("reveal");
      if (phase === "finished") audioRef.current.play("winner");
    }
    phaseRef.current = phase;
  }, [match?.phase.kind]);

  const rootClass = [
    preferences.textSize === "large" ? "text-large" : "",
    preferences.highContrast ? "high-contrast" : "",
    preferences.reducedMotion ? "reduced-motion" : ""
  ].join(" ");

  if (!match || !controller.view) {
    return (
      <div className={rootClass}>
        <MenuScreen
          settings={settings}
          setSettings={setSettings}
          preferences={preferences}
          setPreferences={(next) => {
            const saved = controller.updatePreferences(next);
            audioRef.current.update(saved);
            setPreferences(saved);
          }}
          gamepads={gamepads}
          start={start}
          restoreLabel={
            controller.savedMatchStatus === "completed"
              ? "Последние результаты"
              : controller.savedMatchStatus === "in-progress"
                ? "Продолжить партию"
                : null
          }
          restore={() => {
            const restored = controller.restoreLastMatch();
            if (restored) {
              setSettings((current) => ({
                ...current,
                questionCount: restored.config.questionCount,
                answerTimeMs: restored.config.answerTimeMs,
                teamCount: restored.config.teams.length as 2 | 3 | 4,
                assignments: controller.controlAssignments
              }));
              sync();
            }
          }}
          resetHistory={() => {
            if (window.confirm("Сбросить историю вопросов? Последняя партия сохранится.")) {
              controller.resetQuestionHistory();
            }
          }}
          error={menuError}
        />
      </div>
    );
  }

  const view = controller.view;
  const titleById = TOPIC_TITLE_BY_ID as Readonly<Record<string, string>>;
  const pauseReason = match.pause?.reasons[0];

  return (
    <div className={rootClass}>
      <main className="game-shell">
        <div className="arena-glow" aria-hidden="true" />
        <header className="game-brand">
          <strong>Mindbattle</strong>
          <span>
            {match.tieBreak
              ? "Финальная битва"
              : `Этап ${
                  Math.floor(
                    match.mainQuestionIndex / (match.config.questionCount / 3)
                  ) + 1
                }`}
          </span>
        </header>

        {view.phase === "normal-topic" && (
          <TopicSelection
            view={view}
            titleById={titleById}
          />
        )}
        {view.phase === "topic-confirmation" && (
          <TopicConfirmation view={view} titleById={titleById} />
        )}
        {view.phase === "bonus-veto" && <BonusVeto state={match} titleById={titleById} />}
        {view.phase === "difficulty-feedback" && (
          <DifficultyFeedbackScreen
            selected={match.phase.kind === "difficulty-feedback" ? match.phase.selectedDifficulty : null}
            status={controller.difficultyFeedbackStatus}
            error={controller.difficultyFeedbackError}
            assignments={settings.assignments}
          />
        )}
        {(view.phase === "answering" || view.phase === "reveal") && (
          <QuestionBoard
            state={match}
            view={view}
            assignments={settings.assignments}
            titleById={titleById}
          />
        )}
        {view.phase === "standings" && (
          <Standings
            rows={view.standings ?? selectStandings(match)}
            title={
              match.phase.kind === "standings" && match.phase.completedStage === 3
                ? "Ничья за первое место"
                : `Этап ${match.phase.kind === "standings" ? match.phase.completedStage : ""} завершён`
            }
            footer={
              match.phase.kind === "standings" && match.phase.completedStage === 3
                ? "Новое нажатие начнёт финальную битву"
                : "Отпустите кнопки, затем нажмите любую назначенную клавишу"
            }
          />
        )}
        {view.phase === "finished" && (
          <section className="winner-stage">
            <div className="stage-label stage-label--bonus">Победитель</div>
            <h2>{TEAM_META[view.winnerId!].label} команда</h2>
            <Standings rows={view.standings ?? []} title="Итоговая таблица" footer="" />
            <div className="winner-actions">
              <button type="button" className="primary-action" onClick={restart}>
                Начать заново
              </button>
              <button type="button" className="secondary-action" onClick={() => setMatch(null)}>
                Выйти в меню
              </button>
            </div>
          </section>
        )}

        {view.phase !== "standings" && view.phase !== "finished" && view.phase !== "difficulty-feedback" && (
          <TeamCards view={view} activeTeamIds={match.config.teams} />
        )}
        <footer>ESC · пауза</footer>
      </main>

      {match.pause && (
        <PauseOverlay
          reason={
            pauseReason?.kind === "controller-disconnected"
              ? `Переподключите контроллер: ${TEAM_META[pauseReason.teamId].label}`
              : pauseReason?.kind === "focus-lost"
                ? "Окно игры потеряло фокус"
                : pauseReason?.kind === "restored-snapshot"
                  ? "Партия восстановлена"
                  : "Игра остановлена"
          }
          resume={() => dispatch([{ type: "resume" }])}
          restart={restart}
          exit={() => setMatch(null)}
        />
      )}
    </div>
  );
}
