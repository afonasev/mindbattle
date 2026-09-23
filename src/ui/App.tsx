import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import {
  AnsweringAudioMonitor,
  createInputRouterState,
  disarmUntilNeutral,
  handleGamepadPoll,
  handleKeyboardInput,
  handleWindowBlur,
  phaseAudioActions,
  RevealAudioMonitor,
  soloGamepadCommand,
  soloKeyboardCommand,
  sharedAudioController,
  type GamepadSnapshot,
  type SoloInputKind,
  type SemanticInputAction
} from "../adapters";
import { GameController, SoloController } from "../application";
import { HttpDifficultyFeedbackSink } from "../feedback";
import { assertFullCatalog, catalog, TOPIC_TITLE_BY_ID } from "../content";
import {
  selectStandings,
  type AnswerPosition,
  type DomainCommand,
  type MatchState,
  type TeamId
} from "../domain";
import type { SoloCommand, SoloState } from "../domain/solo";
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
import { SoloFeedbackScreen, SoloRecordsScreen, SoloScreen } from "./soloUi";
import { FeedbackUnavailableDialog, type FeedbackRecoveryChoice } from "./FeedbackUnavailableDialog";
import { PresentationSettings } from "./PresentationSettings";
import { applyPwaUpdate, navigate, onPwaUpdate } from "../main";
import { QueuedDifficultyFeedbackSink } from "../feedback";
import { canApplyPwaUpdate } from "../pwaUpdate";

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
  if (typeof navigator.getGamepads !== "function") return [];
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
  const soloController = useMemo(() => new SoloController({
    catalog,
    storage: localStorage,
    clock: { now: () => performance.now(), wallTime: () => new Date().toISOString() },
    seeds: { nextSeed },
    feedback: new HttpDifficultyFeedbackSink()
  }), []);
  const [preferences, setPreferences] = useState(controller.preferences);
  const [match, setMatch] = useState<MatchState | null>(controller.state);
  const [solo, setSolo] = useState<SoloState | null>(soloController.state);
  const [soloRecordId, setSoloRecordId] = useState<string | null>(null);
  const [showSoloRecords, setShowSoloRecords] = useState(false);
  const [soloInput, setSoloInput] = useState<SoloInputKind>("pointer");
  const [feedbackRecoveryChoice, setFeedbackRecoveryChoice] = useState<FeedbackRecoveryChoice>("retry");
  const [menuError, setMenuError] = useState<string | null>(null);
  const [pwaUpdateReady, setPwaUpdateReady] = useState(false);
  const [pauseSettingsOpen, setPauseSettingsOpen] = useState(false);
  const [gamepads, setGamepads] = useState<readonly Gamepad[]>([]);
  const inputRef = useRef(createInputRouterState());
  const soloGamepadButtonsRef = useRef(new Map<number, readonly boolean[]>());
  const phaseRef = useRef<string | null>(null);
  const confirmationSecondRef = useRef<number | null>(null);
  const answeringAudioRef = useRef(new AnsweringAudioMonitor());
  const revealAudioRef = useRef(new RevealAudioMonitor());
  const soloPhaseRef = useRef<string | null>(null);
  const soloAnsweringAudioRef = useRef(new AnsweringAudioMonitor());
  const soloRevealAudioRef = useRef(new RevealAudioMonitor());
  const lobbyThemePlayedRef = useRef(false);
  const audioActivationRef = useRef(false);
  const audioRef = useRef(sharedAudioController(preferences));

  useEffect(() => onPwaUpdate(setPwaUpdateReady), []);
  useEffect(() => {
    const sink = new QueuedDifficultyFeedbackSink(new HttpDifficultyFeedbackSink(), localStorage);
    void sink.flush();
    const flush = () => void sink.flush();
    window.addEventListener("online", flush);
    return () => window.removeEventListener("online", flush);
  }, []);

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
        teams,
        collectQuestionFeedback: settings.collectQuestionFeedback
      });
      audioRef.current.setMusicDucked(false);
      audioRef.current.play("game-theme");
      inputRef.current = createInputRouterState(false);
      setMenuError(null);
      sync();
    } catch (error) {
      setMenuError(
        error instanceof Error ? error.message.split("\n")[0] : "Не удалось начать игру"
      );
    }
  }, [controller, settings, sync]);

  const startSolo = useCallback(() => {
    try {
      assertFullCatalog();
      setSoloRecordId(null);
      setSoloInput("pointer");
      soloGamepadButtonsRef.current = new Map(gamepadSnapshots().map((gamepad) => [gamepad.index, gamepad.buttons]));
      setSolo(soloController.start({ profile: "solo-endless-v1", collectQuestionFeedback: settings.collectQuestionFeedback }));
      soloPhaseRef.current = "topic";
      audioRef.current.setMusicDucked(false);
      audioRef.current.play("game-theme");
      setMenuError(null);
    } catch (error) {
      setMenuError(error instanceof Error ? error.message.split("\n")[0] : "Не удалось начать соло-забег");
    }
  }, [settings.collectQuestionFeedback, soloController]);

  const dispatchSolo = useCallback((command: SoloCommand) => setSolo(soloController.dispatch([command])), [soloController]);

  const submitSoloFeedback = useCallback(async () => {
    const submission = soloController.submitFeedback();
    setSolo(soloController.state ? { ...soloController.state } : null);
    await submission;
    setSolo(soloController.state ? { ...soloController.state } : null);
  }, [soloController]);

  const skipSoloFeedback = useCallback(() => {
    if (soloController.skipFeedback()) setSolo(soloController.state ? { ...soloController.state } : null);
    setFeedbackRecoveryChoice("retry");
  }, [soloController]);

  const retrySharedFeedback = useCallback(() => {
    setFeedbackRecoveryChoice("retry");
    void controller.handleFeedbackConfirmation().finally(sync);
    queueMicrotask(sync);
  }, [controller, sync]);

  const skipSharedFeedback = useCallback(() => {
    if (controller.skipCompletedFeedback()) sync();
    setFeedbackRecoveryChoice("retry");
  }, [controller, sync]);

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
      setGamepads(typeof navigator.getGamepads === "function"
        ? [...navigator.getGamepads()].filter((item): item is Gamepad => item !== null)
        : []);
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
      if (action.type === "feedback-direction") {
        if (controller.difficultyFeedbackStatus === "error") {
          if (action.direction === "west") setFeedbackRecoveryChoice("retry");
          if (action.direction === "east") setFeedbackRecoveryChoice("skip");
          return [];
        }
        void controller
          .handleFeedbackDirection(action.direction)
          .finally(sync);
        queueMicrotask(sync);
        return [];
      }
      if (action.type === "feedback-confirm") {
        if (controller.difficultyFeedbackStatus === "error") {
          if (feedbackRecoveryChoice === "retry") retrySharedFeedback();
          else skipSharedFeedback();
          return [];
        }
        void controller
          .handleFeedbackConfirmation()
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
  }, [controller, feedbackRecoveryChoice, retrySharedFeedback, skipSharedFeedback, sync]);

  useEffect(() => {
    if (!match) return;
    const mode =
      match.phase.kind === "answering"
        ? "answer"
        : match.phase.kind === "normal-topic"
          ? "normal-topic"
        : match.phase.kind === "bonus-veto"
          ? "bonus-veto"
          : match.phase.kind === "final-veto"
            ? "bonus-veto"
          : match.phase.kind === "difficulty-feedback"
            ? "difficulty-feedback"
          : "continue";
    const keyboard = (event: KeyboardEvent) => {
      if (event.target instanceof HTMLTextAreaElement || event.target instanceof HTMLInputElement) return;
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
            : current.phase.kind === "final-veto"
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
    if (!solo || solo.paused || solo.phase.kind !== "answering") return;
    const timer = window.setInterval(() => setSolo(soloController.tick()), 100);
    return () => window.clearInterval(timer);
  }, [solo, soloController]);

  useEffect(() => {
    if (!solo) return;
    const keyboard = (event: KeyboardEvent) => {
      if (event.type !== "keydown" || event.repeat || event.target instanceof HTMLTextAreaElement || event.target instanceof HTMLInputElement) return;
      const current = soloController.state;
      if (current?.paused && (event.code === "Escape" || event.code === "Enter" || event.code === "Space")) {
        event.preventDefault();
        setSoloInput(event.code.startsWith("Arrow") ? "arrows" : "wasd");
        dispatchSolo({ type: "resume" });
        return;
      }
      const phase = current?.phase;
      if (phase?.kind === "feedback" && soloController.difficultyFeedbackStatus === "error") {
        if (["KeyA", "ArrowLeft", "KeyD", "ArrowRight", "Enter", "Space"].includes(event.code)) event.preventDefault();
        if (event.code === "KeyA" || event.code === "ArrowLeft") setFeedbackRecoveryChoice("retry");
        else if (event.code === "KeyD" || event.code === "ArrowRight") setFeedbackRecoveryChoice("skip");
        else if (event.code === "Enter" || event.code === "Space") {
          if (feedbackRecoveryChoice === "retry") { setFeedbackRecoveryChoice("retry"); void submitSoloFeedback(); }
          else skipSoloFeedback();
        }
        return;
      }
      if (phase?.kind === "finished" && soloRecordId && (event.code === "Enter" || event.code === "Space")) {
        event.preventDefault();
        setSoloInput("wasd");
        setSolo(null);
        return;
      }
      if (phase && event.code === "Escape") {
        event.preventDefault();
        dispatchSolo({ type: "pause" });
        return;
      }
      if (phase?.kind === "feedback") {
        const source = event.code.startsWith("Arrow") ? "arrows" : "wasd";
        const feedbackCursor = phase.feedbackCursor ?? (phase.hasComplaint === true ? 0 : 1);
        if (phase.hasComplaint !== true && (event.code === "KeyA" || event.code === "ArrowLeft")) {
          event.preventDefault();
          setSoloInput(source);
          dispatchSolo({ type: "set-feedback-cursor", cursor: 0 });
          return;
        }
        if (phase.hasComplaint !== true && (event.code === "KeyD" || event.code === "ArrowRight")) {
          event.preventDefault();
          setSoloInput(source);
          dispatchSolo({ type: "set-feedback-cursor", cursor: 1 });
          return;
        }
        if (phase.hasComplaint === true && ["KeyW", "KeyA", "KeyS", "KeyD", "ArrowUp", "ArrowLeft", "ArrowDown", "ArrowRight"].includes(event.code)) {
          event.preventDefault();
          const delta = event.code === "KeyW" || event.code === "ArrowUp" ? -3 : event.code === "KeyS" || event.code === "ArrowDown" ? 3 : event.code === "KeyA" || event.code === "ArrowLeft" ? -1 : 1;
          const column = feedbackCursor % 3;
          const cursor = delta === -1 && column === 0 ? feedbackCursor : delta === 1 && column === 2 ? feedbackCursor : feedbackCursor + delta;
          setSoloInput(source);
          dispatchSolo({ type: "set-feedback-cursor", cursor });
          return;
        }
        if (event.code === "Enter" || event.code === "Space") {
          event.preventDefault();
          setSoloInput(source);
          if (phase.hasComplaint !== true) {
            const selected = feedbackCursor === 0;
            if (phase.hasComplaint !== selected) setSolo(soloController.setFeedbackChoice(selected));
            if (!selected) void submitSoloFeedback();
          } else if (feedbackCursor === 7) {
            if (phase.complaintReasons.length > 0 || phase.complaintNote.trim()) void submitSoloFeedback();
          }
          else {
            const reasons = ["too-easy", "too-hard", "weak-answer-options", "unclear-wording", "suspected-error", "ambiguous-answer", "uninteresting-for-quiz"] as const;
            dispatchSolo({ type: "toggle-feedback-reason", reason: reasons[feedbackCursor] });
          }
          return;
        }
      }
      const action = soloKeyboardCommand(event.code, phase);
      if (action) {
        event.preventDefault();
        setSoloInput(action.source);
        dispatchSolo(action.command);
      }
    };
    window.addEventListener("keydown", keyboard);
    return () => window.removeEventListener("keydown", keyboard);
  }, [dispatchSolo, feedbackRecoveryChoice, skipSoloFeedback, solo, soloController, soloRecordId, submitSoloFeedback]);

  useEffect(() => {
    if (!solo) return;
    let frame = 0;
    const poll = () => {
      const current = soloController.state;
      const phase = current?.phase;
      for (const gamepad of gamepadSnapshots()) {
        const previous = soloGamepadButtonsRef.current.get(gamepad.index) ?? [];
        const button = gamepad.buttons.findIndex((down, index) => down && !previous[index]);
        soloGamepadButtonsRef.current.set(gamepad.index, gamepad.buttons);
        if (button < 0) continue;
        if (phase?.kind === "feedback" && soloController.difficultyFeedbackStatus === "error") {
          if (button === 14) setFeedbackRecoveryChoice("retry");
          else if (button === 15) setFeedbackRecoveryChoice("skip");
          else if (button === 0) {
            if (feedbackRecoveryChoice === "retry") { setFeedbackRecoveryChoice("retry"); void submitSoloFeedback(); }
            else skipSoloFeedback();
          }
          break;
        }
        if (current?.paused && (button === 0 || button === 9)) {
          setSoloInput("gamepad");
          dispatchSolo({ type: "resume" });
          break;
        }
        if (phase && button === 9) {
          setSoloInput("gamepad");
          dispatchSolo({ type: "pause" });
          break;
        }
        if (phase?.kind === "finished" && soloRecordId && button === 0) {
          setSoloInput("gamepad");
          setSolo(null);
          break;
        }
        if (phase?.kind === "feedback") {
          const feedbackCursor = phase.feedbackCursor ?? (phase.hasComplaint === true ? 0 : 1);
          if (phase.hasComplaint !== true && button === 14) {
            setSoloInput("gamepad");
            dispatchSolo({ type: "set-feedback-cursor", cursor: 0 });
            break;
          }
          if (phase.hasComplaint !== true && button === 15) {
            setSoloInput("gamepad");
            dispatchSolo({ type: "set-feedback-cursor", cursor: 1 });
            break;
          }
          if (button === 0) {
            setSoloInput("gamepad");
            if (phase.hasComplaint !== true) {
              const selected = feedbackCursor === 0;
              if (phase.hasComplaint !== selected) setSolo(soloController.setFeedbackChoice(selected));
              if (!selected) void submitSoloFeedback();
            } else if (feedbackCursor === 7) {
              if (phase.complaintReasons.length > 0 || phase.complaintNote.trim()) void submitSoloFeedback();
            }
            else {
              const reasons = ["too-easy", "too-hard", "weak-answer-options", "unclear-wording", "suspected-error", "ambiguous-answer", "uninteresting-for-quiz"] as const;
              dispatchSolo({ type: "toggle-feedback-reason", reason: reasons[feedbackCursor] });
            }
            break;
          }
        }
        const command = soloGamepadCommand(button, phase);
        if (command) {
          setSoloInput("gamepad");
          dispatchSolo(command);
          break;
        }
      }
      frame = requestAnimationFrame(poll);
    };
    frame = requestAnimationFrame(poll);
    return () => cancelAnimationFrame(frame);
  }, [dispatchSolo, feedbackRecoveryChoice, skipSoloFeedback, solo, soloController, soloRecordId, submitSoloFeedback]);

  useEffect(() => {
    if (match || solo) {
      lobbyThemePlayedRef.current = false;
      return;
    }
    if (!lobbyThemePlayedRef.current) {
      audioRef.current.setMusicDucked(false);
      audioRef.current.play("menu-theme");
      lobbyThemePlayedRef.current = true;
    }
  }, [match, solo]);

  useEffect(() => {
    const activateMenuAudio = () => {
      if (audioActivationRef.current || match || solo) return;
      audioActivationRef.current = true;
      audioRef.current.setMusicDucked(false);
      audioRef.current.play("menu-theme");
      lobbyThemePlayedRef.current = true;
    };
    window.addEventListener("pointerdown", activateMenuAudio, { capture: true, once: true });
    window.addEventListener("keydown", activateMenuAudio, { capture: true, once: true });
    return () => {
      window.removeEventListener("pointerdown", activateMenuAudio, { capture: true });
      window.removeEventListener("keydown", activateMenuAudio, { capture: true });
    };
  }, [match, solo]);

  useEffect(() => {
    const phase = match?.phase.kind ?? null;
    if (phase !== phaseRef.current) {
      inputRef.current = disarmUntilNeutral(inputRef.current);
      for (const action of phaseAudioActions(phaseRef.current, phase)) {
        if (action.type === "stop-music") audioRef.current.stopMusic();
        else if (action.type === "set-music-ducked") audioRef.current.setMusicDucked(action.ducked);
        else audioRef.current.play(action.cue);
      }
    }
    phaseRef.current = phase;
  }, [match?.phase.kind]);

  useEffect(() => {
    if (!match || match.pause || match.phase.kind !== "reveal") {
      revealAudioRef.current.reset();
      return;
    }
    const signature = `${match.phase.round.questionId}:${match.phase.resolutions.map(({ teamId, result }) => `${teamId}:${result}`).join("|")}`;
    for (const cue of revealAudioRef.current.observe(signature, match.phase.resolutions)) audioRef.current.play(cue);
  }, [match]);

  useEffect(() => {
    const phase = solo?.phase.kind ?? null;
    if (phase === soloPhaseRef.current) return;
    const toMatchPhase: Readonly<Record<NonNullable<typeof phase>, string>> = {
      topic: "normal-topic",
      risk: "bonus-veto",
      answering: "answering",
      reveal: "reveal",
      feedback: "difficulty-feedback",
      finished: "finished"
    };
    const previous = soloPhaseRef.current ? toMatchPhase[soloPhaseRef.current as NonNullable<typeof phase>] : null;
    const current = phase ? toMatchPhase[phase] : null;
    for (const action of phaseAudioActions(previous, current)) {
      if (action.type === "stop-music") audioRef.current.stopMusic();
      else if (action.type === "set-music-ducked") audioRef.current.setMusicDucked(action.ducked);
      else audioRef.current.play(action.cue);
    }
    soloPhaseRef.current = phase;
  }, [solo?.phase.kind]);

  useEffect(() => {
    if (!solo || solo.paused || solo.phase.kind !== "answering") {
      soloAnsweringAudioRef.current.reset();
      return;
    }
    for (const cue of soloAnsweringAudioRef.current.observe(solo.phase.baseRemainingMs)) audioRef.current.play(cue);
  }, [solo]);

  useEffect(() => {
    if (!solo || solo.paused || solo.phase.kind !== "reveal") {
      soloRevealAudioRef.current.reset();
      return;
    }
    const signature = `${solo.runId}:${solo.slotIndex}:${solo.phase.result}`;
    const result = solo.phase.result === "correct" ? "correct" : "wrong";
    for (const cue of soloRevealAudioRef.current.observe(signature, [{ result }])) audioRef.current.play(cue);
  }, [solo]);

  useEffect(() => {
    if (!match || match.pause || match.phase.kind !== "answering") {
      answeringAudioRef.current.reset();
      return;
    }
    for (const cue of answeringAudioRef.current.observe(match.phase.baseRemainingMs)) {
      audioRef.current.play(cue);
    }
  }, [match]);

  useEffect(() => {
    if (!match || match.pause || match.phase.kind !== "topic-confirmation") {
      confirmationSecondRef.current = null;
      return;
    }
    const second = Math.ceil(match.phase.remainingMs / 1_000);
    if (second > 0 && second !== confirmationSecondRef.current) {
      audioRef.current.play("countdown");
      confirmationSecondRef.current = second;
    }
  }, [match]);

  const rootClass = [
    preferences.textSize === "large" ? "text-large" : "",
    preferences.highContrast ? "high-contrast" : "",
    preferences.reducedMotion ? "reduced-motion" : ""
  ].join(" ");

  if (solo) {
    const questionId = solo.phase.kind === "answering" || solo.phase.kind === "reveal" ? solo.phase.round.questionId : null;
    const question = questionId ? catalog.topics.flatMap((topic) => topic.questions).find((candidate) => candidate.id === questionId) : undefined;
    const savePreferences = (next: typeof preferences) => {
      const saved = controller.updatePreferences(next);
      audioRef.current.update(saved);
      if (saved.muted) audioRef.current.stopMusic();
      setPreferences(saved);
    };
    return <div className={rootClass}>{pwaUpdateReady && canApplyPwaUpdate(false, solo.phase.kind) && <PwaUpdateButton />}{pauseSettingsOpen ? <PresentationSettings preferences={preferences} setPreferences={savePreferences} back={() => setPauseSettingsOpen(false)} /> : solo.phase.kind === "feedback" ? <SoloFeedbackScreen value={solo.phase} choose={(hasComplaint) => { setSoloInput("pointer"); setSolo(soloController.setFeedbackChoice(hasComplaint)); if (!hasComplaint) void submitSoloFeedback(); }} toggleReason={(reason) => { setSoloInput("pointer"); setSolo(soloController.toggleFeedbackReason(reason)); }} setNote={(note) => { setSoloInput("pointer"); setSolo(soloController.setFeedbackNote(note)); }} submit={() => void submitSoloFeedback()} pending={soloController.difficultyFeedbackStatus === "pending"} error={soloController.difficultyFeedbackError} exit={() => setSolo(null)} /> : <SoloScreen state={solo} question={question} titleById={TOPIC_TITLE_BY_ID} records={soloController.records} savedRecordId={soloRecordId} inputKind={soloInput} settings={() => setPauseSettingsOpen(true)} command={(command) => { setSoloInput("pointer"); setSolo(soloController.dispatch([command])); }} finish={(name) => { const record = soloController.saveResult(name); if (record) setSoloRecordId(record.id); }} exit={() => setSolo(null)} />}{solo.phase.kind === "feedback" && soloController.difficultyFeedbackStatus === "error" && <FeedbackUnavailableDialog selected={feedbackRecoveryChoice} onSelect={setFeedbackRecoveryChoice} onRetry={() => { setFeedbackRecoveryChoice("retry"); void submitSoloFeedback(); }} onSkip={skipSoloFeedback} />}</div>;
  }

  if (!match || !controller.view) {
    return (
      <div className={rootClass}>
        {pwaUpdateReady && <PwaUpdateButton />}
        {showSoloRecords ? <SoloRecordsScreen records={soloController.records} exit={() => setShowSoloRecords(false)} /> : <MenuScreen
          settings={settings}
          setSettings={setSettings}
          preferences={preferences}
          setPreferences={(next) => {
            const saved = controller.updatePreferences(next);
            audioRef.current.update(saved);
            if (saved.muted) audioRef.current.stopMusic();
            else if (!match && !solo) {
              audioRef.current.setMusicDucked(false);
              audioRef.current.play("menu-theme");
            }
            setPreferences(saved);
          }}
          gamepads={gamepads}
          start={start}
          startSolo={startSolo}
          enterNetwork={() => navigate("/network")}
          restoreSolo={soloController.canRestore ? () => setSolo(soloController.restore()) : null}
          restoreLabel={
            controller.savedMatchStatus === "in-progress" ? "Продолжить игру на одном устройстве" : null
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
          viewRecords={() => setShowSoloRecords(true)}
          resetHistory={() => {
            if (window.confirm("Сбросить историю вопросов? Последняя партия сохранится.")) {
              controller.resetQuestionHistory();
            }
          }}
          error={menuError}
        />}
      </div>
    );
  }

  const view = controller.view;
  const titleById = TOPIC_TITLE_BY_ID as Readonly<Record<string, string>>;
  const pauseReason = match.pause?.reasons[0];

  if (pauseSettingsOpen) {
    return <div className={rootClass}><PresentationSettings preferences={preferences} setPreferences={(next) => {
      const saved = controller.updatePreferences(next);
      audioRef.current.update(saved);
      if (saved.muted) audioRef.current.stopMusic();
      setPreferences(saved);
    }} back={() => setPauseSettingsOpen(false)} /></div>;
  }

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
            assignments={settings.assignments}
          />
        )}
        {view.phase === "topic-confirmation" && (
          <TopicConfirmation view={view} titleById={titleById} />
        )}
        {(view.phase === "bonus-veto" || view.phase === "final-veto") && <BonusVeto state={match} titleById={titleById} assignments={settings.assignments} />}
        {view.phase === "difficulty-feedback" && (
          <DifficultyFeedbackScreen
            feedback={view.feedback!}
            status={controller.difficultyFeedbackStatus}
            error={controller.difficultyFeedbackError}
            assignments={settings.assignments}
            setNote={(note: string) => { controller.setFeedbackNote(note); sync(); }}
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
                : "Нажмите любую клавишу"
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
          <TeamCards state={match} view={view} activeTeamIds={match.config.teams} />
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
          settings={() => setPauseSettingsOpen(true)}
          restart={restart}
          exit={() => setMatch(null)}
        />
      )}
      {match.phase.kind === "difficulty-feedback" && controller.difficultyFeedbackStatus === "error" && (
        <FeedbackUnavailableDialog
          selected={feedbackRecoveryChoice}
          onSelect={setFeedbackRecoveryChoice}
          onRetry={retrySharedFeedback}
          onSkip={skipSharedFeedback}
        />
      )}
    </div>
  );
}

function PwaUpdateButton() { return <button className="pwa-update" type="button" onClick={() => void applyPwaUpdate()}>Доступно обновление · Обновить</button>; }
