import { ComplaintDialog } from './ComplaintDialog';
import type { ComplaintContext } from '../feedback/types';
import { MatchSetupFields } from "./MatchSetupFields";
import { MenuAction, ScreenHeader, ScreenSurface, SessionMenu } from "./menuUi";
import { navigate } from "../main";
import { ReleaseAction } from "./ReleaseAction";
import { useEffect, useRef, useState } from "react";
import {
  NetworkConnection,
  networkRequest,
  savedCredential,
  saveCredential,
  forgetCredential,
} from "../network/client";
import type {
  Credential,
  NetworkAction,
  NetworkSnapshot,
} from "../network/protocol";
import {
  AudioController,
  AnswerCommitAudioMonitor,
  AnsweringAudioMonitor,
  phaseAudioActions,
  classicMusicStage,
  presentationMusicCue,
  RevealAudioMonitor,
  shouldPlayNetworkAudio,
  sharedAudioController,
  TopicCountdownAudioMonitor,
} from "../adapters/audio";
import {
  DEFAULT_PREFERENCES,
  decodePreferences,
  STORAGE_KEY,
} from "../adapters/storage";
import "./network.css";
import { phoneStatus } from "./networkStatus";
import { SettingsDialog } from "./PresentationSettings";
import { FeedbackUnavailableDialog, type FeedbackRecoveryChoice } from "./FeedbackUnavailableDialog";
function initialPreferences() {
  try {
    return (
      decodePreferences(
        JSON.parse(localStorage.getItem(STORAGE_KEY) ?? "null")?.preferences,
      ) ??
      decodePreferences(
        JSON.parse(localStorage.getItem("mindbattle-network-preferences-v1") ?? "null"),
      ) ??
      DEFAULT_PREFERENCES
    );
  } catch {
    return DEFAULT_PREFERENCES;
  }
}
const positions = ["up", "right", "down", "left"] as const;
const letters = { up: "А", right: "Б", down: "В", left: "Г" };
const reasons = [
  "Слишком лёгкий",
  "Слишком сложный",
  "Слабые неверные варианты",
  "Непонятная формулировка",
  "Фактическая ошибка",
  "Неоднозначный ответ",
  "Неинтересный вопрос",
];
const reasonKeys = [
  "too-easy",
  "too-hard",
  "weak-answer-options",
  "unclear-wording",
  "suspected-error",
  "ambiguous-answer",
  "uninteresting-for-quiz",
];
const seconds = (ms: number) => Math.ceil(ms / 1000);
export function NetworkApp() {
  const mobile = useRef(
    matchMedia("(max-width: 760px)").matches ||
      matchMedia("(pointer: coarse)").matches,
  ).current;
  const [credential, setCredential] = useState<Credential | null>(() =>
    savedCredential(undefined, mobile ? "player" : "display"),
  );
  const [snapshot, setSnapshot] = useState<NetworkSnapshot | null>(null);
  const [code, setCode] = useState("");
  const [name, setName] = useState("");
  const [complaint, setComplaint] = useState<ComplaintContext | null>(null);
  const [feedbackNote, setFeedbackNote] = useState("");
  const [feedbackRecoveryChoice, setFeedbackRecoveryChoice] = useState<FeedbackRecoveryChoice>("retry");
  const [scoreboardOpen, setScoreboardOpen] = useState(false);
  useEffect(
    () => setFeedbackNote(snapshot?.view?.feedback?.complaintNote ?? ""),
    [snapshot?.view?.feedback?.eventId],
  );
  useEffect(() => setScoreboardOpen(false), [snapshot?.epoch, snapshot?.phase]);
  const [error, setError] = useState("");
  const [status, setStatus] = useState("");
  const [terminal, setTerminal] = useState(false);
  const [busy, setBusy] = useState(false);
  const [preferences, setPreferences] = useState(initialPreferences);
  const [pauseSettingsOpen, setPauseSettingsOpen] = useState(false);
  const [localMenuOpen, setLocalMenuOpen] = useState(false);
  const muted =
    new URLSearchParams(location.search).get("muted") === "1" ||
    preferences.muted;
  const connection = useRef<NetworkConnection | null>(null);
  const audio = useRef<AudioController | null>(null);
  const lastPhase = useRef("");
  const revealAudio = useRef(new RevealAudioMonitor());
  const answerCommitAudio = useRef(new AnswerCommitAudioMonitor());
  const answeringAudio = useRef(new AnsweringAudioMonitor());
  const confirmationAudio = useRef(new TopicCountdownAudioMonitor());
  const enableAudio = () => {
    if (!mobile && !audio.current)
      audio.current = sharedAudioController({
        musicVolume: preferences.musicVolume,
        effectsVolume: preferences.effectsVolume,
        muted,
      });
  };
  useEffect(() => {
    audio.current?.update({ musicVolume: preferences.musicVolume, effectsVolume: preferences.effectsVolume, muted });
    if (muted) audio.current?.stopMusic();
  }, [muted, preferences.musicVolume, preferences.effectsVolume]);
  const savePreferences = (next: typeof preferences) => {
    setPreferences(next);
    try {
      localStorage.setItem("mindbattle-network-preferences-v1", JSON.stringify(next));
      const persisted = JSON.parse(localStorage.getItem(STORAGE_KEY) ?? "null");
      if (persisted && typeof persisted === "object" && !Array.isArray(persisted)) {
        localStorage.setItem(STORAGE_KEY, JSON.stringify({ ...persisted, preferences: next }));
      }
    } catch {
      // Storage is optional presentation state.
    }
  };
  useEffect(() => {
    if (!credential) return;
    setTerminal(false);
    setStatus("Подключаемся…");
    setSnapshot(null);
    const client = new NetworkConnection(
      credential,
      setSnapshot,
      (message, ended) => {
        setStatus(message);
        if (ended) setTerminal(true);
      },
    );
    connection.current = client;
    return () => {
      client.close();
      connection.current = null;
    };
  }, [credential]);
  useEffect(() => {
    if (!snapshot || !shouldPlayNetworkAudio(snapshot.role, mobile)) return;
    if (snapshot.paused) return;
    const signature = `${snapshot.epoch}:${snapshot.phase}`;
    if (lastPhase.current === signature) return;
    const previousPhase = lastPhase.current.split(":")[1] || null;
    lastPhase.current = signature;
    if (snapshot.phase !== "reveal") audio.current?.stopEvents();
    for (const action of phaseAudioActions(previousPhase, snapshot.phase)) {
      if (action.type === "stop-music") audio.current?.stopMusic();
      else if (action.type === "set-music-ducked") audio.current?.setMusicDucked(action.ducked);
      else audio.current?.play(action.cue);
    }
  }, [snapshot?.phase, snapshot?.epoch, snapshot?.paused, mobile]);
  const musicCue = presentationMusicCue(snapshot?.phase ?? "lobby", snapshot
    ? classicMusicStage((snapshot.questionNumber ?? 1) - 1, snapshot.settings.questionCount, !!snapshot.tieBreakNumber)
    : 0);
  useEffect(() => {
    if (mobile || (snapshot && !shouldPlayNetworkAudio(snapshot.role, mobile))) return;
    if (snapshot?.paused || muted) {
      audio.current?.stopMusic();
      audio.current?.stopEvents();
      return;
    }
    if (!musicCue) { audio.current?.stopMusic(); return; }
    audio.current?.setMusicDucked(snapshot?.phase === "answering");
    audio.current?.play(musicCue);
  }, [musicCue, snapshot?.phase, snapshot?.paused, snapshot?.epoch, snapshot?.role, credential, mobile, muted, preferences.musicVolume, preferences.effectsVolume]);
  useEffect(() => {
    if (!snapshot || !shouldPlayNetworkAudio(snapshot.role, mobile) || !snapshot.view ||
        !["answering", "reveal"].includes(snapshot.phase)) return;
    const signature = `${snapshot.epoch}:${snapshot.questionNumber}:${snapshot.tieBreakNumber ?? 0}`;
    const cues = answerCommitAudio.current.observe(signature, snapshot.view.teams.filter(team => team.hasAnswered).map(team => team.id));
    for (const cue of cues) if (!snapshot.paused) audio.current?.play(cue);
  }, [snapshot, mobile]);
  useEffect(() => {
    if (!snapshot || !shouldPlayNetworkAudio(snapshot.role, mobile) || snapshot.phase !== "reveal" || !snapshot.view) {
      if (snapshot?.phase !== "reveal") revealAudio.current.reset();
      return;
    }
    const signature = `${snapshot.epoch}:${snapshot.phaseRevision}`;
    for (const cue of revealAudio.current.observe(signature, snapshot.view.teams.map(({ result }) => ({ result: result ?? "no-answer" })))) {
      if (!snapshot.paused) audio.current?.play(cue);
    }
  }, [snapshot?.epoch, snapshot?.phase, snapshot?.phaseRevision, snapshot?.paused, snapshot?.view, mobile]);
  useEffect(() => {
    if (!snapshot || !shouldPlayNetworkAudio(snapshot.role, mobile)) return;
    if (snapshot.phase !== "answering") { answeringAudio.current.reset(); return; }
    if (snapshot.paused || snapshot.view?.baseRemainingMs === undefined) return;
    for (const cue of answeringAudio.current.observe(snapshot.view.baseRemainingMs)) audio.current?.play(cue);
  }, [snapshot, mobile]);
  useEffect(() => {
    if (mobile || snapshot?.phase !== "topic-confirmation") {
      confirmationAudio.current.reset();
      return;
    }
    if (snapshot.paused) return;
    const remainingMs = snapshot.view?.confirmationRemainingMs;
    if (remainingMs === undefined) return;
    for (const cue of confirmationAudio.current.observe(remainingMs))
      audio.current?.play(cue);
  }, [snapshot?.phase, snapshot?.paused, snapshot?.view?.confirmationRemainingMs, mobile]);
  useEffect(() => {
    if (snapshot?.paused) { audio.current?.stopMusic(); audio.current?.stopEvents(); }
  }, [snapshot?.paused]);
  useEffect(() => () => { audio.current?.stopMusic(); audio.current?.stopEvents(); }, []);
  async function enter(create = false) {
    setBusy(true);
    setError("");
    enableAudio();
    try {
      let next: Credential | null = create
        ? null
        : savedCredential(code, "player");
      if (!next)
        next = await networkRequest<Credential>(
          create ? "create" : "join",
          create ? {} : { code, name },
        );
      saveCredential(next);
      setCredential(next);
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setBusy(false);
    }
  }
  async function act(action: NetworkAction) {
    if (!snapshot || !connection.current || busy) return false;
    setBusy(true);
    setError("");
    enableAudio();
    try {
      await connection.current.command(snapshot, action);
      return true;
    } catch (e) {
      setError((e as Error).message);
      return false;
    } finally {
      setBusy(false);
    }
  }
  async function exitRoom() {
    if (await act({ type: "close" })) { reset(); navigate("/"); }
  }
  function reset() {
    if (credential) forgetCredential(credential);
    setCredential(null);
    setSnapshot(null);
    setTerminal(false);
    setStatus("");
    setError("");
    setLocalMenuOpen(false);
    setPauseSettingsOpen(false);
  }
  const locked = busy || !!status || !!snapshot?.paused;
  const view = snapshot?.view;
  const phase = snapshot?.phase;
  const display = snapshot?.role === "display";
  const personalCard = view?.teams.find((card) => card.id === snapshot?.selfId);
  const personalAnswerTime = !display && phase === "answering" && personalCard?.remainingMs !== undefined && (view?.baseRemainingMs ?? 0) > 0;
  const turnStatus = snapshot ? phoneStatus(snapshot) : null;
  useEffect(() => {
    if (complaint && (!snapshot?.isLeader || phase !== 'reveal' || snapshot.complaintContext?.eventId !== complaint.eventId)) setComplaint(null);
  }, [snapshot?.isLeader, phase, snapshot?.complaintContext?.eventId, complaint]);
  const canSkipConfirmation =
    mobile &&
    !!snapshot?.isLeader &&
    phase === "topic-confirmation" &&
    !locked;
  function openMenu() {
    if (snapshot?.isLeader && phase !== "lobby" && phase !== "finished" && !snapshot.paused) void act({ type: "pause" });
    else setLocalMenuOpen(true);
  }
  useEffect(() => {
    const keyboard = (event: KeyboardEvent) => {
      if (event.code !== "Escape" || event.repeat || event.target instanceof HTMLInputElement || event.target instanceof HTMLTextAreaElement) return;
      event.preventDefault();
      if (credential && !terminal) openMenu();
    };
    window.addEventListener("keydown", keyboard);
    return () => window.removeEventListener("keydown", keyboard);
  });
  const playerCards = view && phase !== "standings" && phase !== "finished" ? (
    <div className={`network-cards ${view.teams.length > 4 ? "network-cards--many" : ""}`}>
      {view.teams.map((card) => (
        <article
          className={`network-player-card ${card.departed ? "departed" : ""} ${card.name.length > 18 ? "network-player-card-long-name" : ""} ${(phase === "reveal" || phase === "difficulty-feedback") && card.result ? `network-player-card--${card.result}` : ""}`}
          key={card.id}
          role={mobile ? "button" : undefined}
          tabIndex={mobile ? 0 : undefined}
          aria-label={mobile ? "Показать текущий счёт" : undefined}
          onClick={mobile ? () => setScoreboardOpen(true) : undefined}
          onKeyDown={
            mobile
              ? (event) => {
                  if (event.key === "Enter" || event.key === " ") {
                    event.preventDefault();
                    setScoreboardOpen(true);
                  }
                }
              : undefined
          }
        >
          <span className="network-player-number">
            {display ? card.id.replace("player-", "") : "Я"}
          </span>
          <strong>{card.name}</strong>
          {!display && !terminal && (
            <span className="network-reserve" aria-label={personalAnswerTime ? "Время ответа и запас" : "Запас времени"}>
              <span>{personalAnswerTime ? "Ответ" : "Запас"}</span>
              <strong>{seconds(personalAnswerTime ? card.remainingMs! : card.reserveMs)} <small>с</small></strong>
              {personalAnswerTime && <small className="network-reserve-balance">Запас {seconds(card.reserveMs)} с</small>}
            </span>
          )}
          <b>{card.score}</b>
          <small>
            {card.departed
              ? "Выбыл"
              : display && card.remainingMs !== undefined
                ? `Время: ${seconds(card.remainingMs)} с`
                : card.hasAnswered && phase === "answering"
                  ? "✓ Ответ принят"
                  : ""}
          </small>
          {(phase === "reveal" || phase === "difficulty-feedback") && card.result && (
            <small>
              {card.result === "correct"
                ? "✓ Верно"
                : card.result === "spectator"
                  ? "Наблюдает"
                  : card.result === "no-answer"
                    ? "Нет ответа"
                    : "Неверно"}
            </small>
          )}
        </article>
      ))}
    </div>
  ) : null;
  return (
    <ScreenSurface
      className={`game-shell network-app ${mobile ? "network-mobile" : "network-display"} ${preferences.textSize === "large" ? "network-text-large" : ""} ${preferences.highContrast ? "network-high-contrast" : ""} ${preferences.reducedMotion ? "reduced-motion" : ""}`}
      onClick={
        canSkipConfirmation && !localMenuOpen && !pauseSettingsOpen
          ? (event) => {
              event.preventDefault();
              void act({ type: "continue" });
            }
          : undefined
      }
    >
      <ReleaseAction safe={!credential || terminal} />
      <ScreenHeader className="network-header" subtitle={mobile && personalCard ? snapshot?.code : <>Сетевая игра{snapshot ? ` · ${snapshot.code}` : ""}</>}
        back={!credential || terminal ? () => navigate("/") : undefined} menu={credential && !terminal ? openMenu : undefined} disabled={busy} />
      {error && (
        <p className="network-error" role="alert">
          {error}
        </p>
      )}
      {status && (
        <p className="network-status" role="status">
          {status}
        </p>
      )}
      {terminal ? (
        <section className="network-entry">
          <h1>Подключение завершено</h1>
          <MenuAction onClick={reset}>Вернуться к подключению</MenuAction>
        </section>
      ) : !credential ? (
        <section className="network-entry">
          <span className="network-eyebrow">Один экран. Вся компания.</span>
          <h1>{mobile ? "Вступить в игру" : "Соберите свою компанию"}</h1>
          <p>
            {mobile
              ? "Введите код с общего экрана и своё имя."
              : "До 12 игроков отвечают со своих телефонов. Вопросы и результаты — здесь."}
          </p>
          {mobile ? (
            <form
              onSubmit={(e) => {
                e.preventDefault();
                void enter();
              }}
            >
              <label>
                Код комнаты
                <input
                  aria-label="Код комнаты"
                  value={code}
                  inputMode="numeric"
                  pattern="[0-9]{4}"
                  maxLength={4}
                  required
                  onChange={(e) => setCode(e.target.value.replace(/\D/g, ""))}
                />
              </label>
              <label>
                Ваше имя
                <input
                  aria-label="Ваше имя"
                  value={name}
                  maxLength={24}
                  required={!savedCredential(code, "player")}
                  onChange={(e) => setName(e.target.value)}
                />
              </label>
              <MenuAction
                type="submit"
                variant="primary"
                disabled={busy || code.length !== 4}
              >
                Подключиться
              </MenuAction>
            </form>
          ) : (
            <MenuAction
              variant="primary"
              disabled={busy}
              onClick={() => void enter(true)}
            >
              Создать сетевую игру
            </MenuAction>
          )}
        </section>
      ) : !snapshot ? (
        <section className="network-entry">
          <p>Ожидаем состояние комнаты…</p>
          <MenuAction onClick={reset}>Другая комната</MenuAction>
          {localMenuOpen && <SessionMenu title="Подключение" settings={() => setPauseSettingsOpen(true)} exit={() => navigate("/")} back={() => setLocalMenuOpen(false)} />}
        </section>
      ) : (
        <>
          {phase === "lobby" ? (
            <section className="setup-stage network-lobby">
              <div className="network-lobby-intro">
                <span className="network-eyebrow">Код комнаты</span>
                <h1 className="network-code">{snapshot.code}</h1>
                <p>
                  {display
                    ? "Откройте Mindbattle на телефоне и нажмите «Подключиться к игре»."
                    : "Вы в комнате. Ждём начала игры."}
                </p>
                <p>
                  Ведущий:{" "}
                  <strong>{snapshot.leaderName || "пока не выбран"}</strong>
                </p>
              </div>
              <div className="network-lobby-content">
                <h2>Игроки · {snapshot.players.length}/12</h2>
                <ul className="network-roster">
                  {snapshot.players.map((p) => (
                    <li key={p.id}>
                      <span>
                        <strong>{p.name}</strong>
                        <small>
                          {p.connected ? "Подключён" : "Ожидаем соединения"}
                        </small>
                      </span>
                      {display && (
                        <span className="network-roster-actions">
                          <MenuAction
                            disabled={busy}
                            onClick={() =>
                              void act({ type: "leader", playerId: p.id })
                            }
                          >
                            Ведущий
                          </MenuAction>
                          <MenuAction
                            aria-label={`Удалить ${p.name}`}
                            disabled={busy}
                            onClick={() =>
                              void act({ type: "remove", playerId: p.id })
                            }
                          >
                            Удалить
                          </MenuAction>
                        </span>
                      )}
                    </li>
                  ))}
                </ul>
                {display && (
                  <>
                    <MatchSetupFields compact disabled={busy} questionCount={snapshot.settings.questionCount} answerTimeMs={snapshot.settings.answerTimeMs} setQuestionCount={(questionCount) => void act({ type: "settings", ...snapshot.settings, questionCount })} setAnswerTimeMs={(answerTimeMs) => void act({ type: "settings", ...snapshot.settings, answerTimeMs })} />
                    <MenuAction
                      variant="primary"
                      disabled={
                        busy ||
                        snapshot.players.length < 2 ||
                        snapshot.players.some((p) => !p.connected)
                      }
                      onClick={() => void act({ type: "start" })}
                    >
                      Начать игру
                    </MenuAction>
                    <MenuAction onClick={() => void exitRoom()}>
                      Закрыть комнату
                    </MenuAction>
                  </>
                )}
              </div>
            </section>
          ) : (
            <section className="network-match">
              <div className="network-round-heading">
                {display && view?.question && <span className="network-topic-label">{snapshot.titles[view.question.topicId]}</span>}
                <span>
                  {snapshot.tieBreakNumber
                    ? `Финальная битва · вопрос ${snapshot.tieBreakNumber}`
                    : `Вопрос ${snapshot.questionNumber}/${snapshot.settings.questionCount}`}
                  {snapshot.difficulty
                    ? ` · ${{ easy: "Лёгкий", medium: "Средний", hard: "Сложный" }[snapshot.difficulty] ?? snapshot.difficulty}`
                    : ""}
                </span>
                {snapshot.isLeader && (
                  <div className="network-round-actions">
                    {(phase === "reveal" || phase === "standings") && (
                      <MenuAction
                        variant="primary"
                        disabled={locked}
                        onClick={() => void act({ type: "continue" })}
                      >
                        Дальше
                      </MenuAction>
                    )}

                  </div>
                )}
              </div>
              {!display && turnStatus && phase !== "normal-topic" && (
                <p role="status" className={`network-turn-status network-turn-status--${turnStatus!.required ? "required" : "waiting"}`}>
                  {turnStatus!.text}
                </p>
              )}
              {!display && playerCards}
              {snapshot.spectating && <p>Вы наблюдаете финальную битву за первое место.</p>}
              {mobile && scoreboardOpen && (
                <div
                  className="network-scoreboard-overlay"
                  role="dialog"
                  aria-modal="true"
                  aria-label="Текущий счёт"
                  onClick={() => setScoreboardOpen(false)}
                >
                  <section>
                    <p>Текущий счёт</p>
                    <div className="network-scoreboard-list">
                      {snapshot.scoreboard?.map((row) => (
                        <div key={row.teamId}>
                          <span>{row.departed ? "—" : row.rank}</span>
                          <strong>{row.name}{row.departed ? " · Выбыл" : ""}</strong>
                          <b>{row.score}</b>
                        </div>
                      ))}
                    </div>
                  </section>
                </div>
              )}
              {phase === "normal-topic" && (
                <section className="topic-stage network-topic-stage">
                  <h1 className={!display ? `network-turn-status network-turn-status--${turnStatus?.required ? "required" : "waiting"}` : undefined}>
                    {snapshot.canChoose
                      ? "Выберите тему"
                      : display
                        ? `Выбирает ${snapshot.players.find((p) => p.id === view?.chooser)?.name ?? "игрок"}`
                        : turnStatus?.text}
                  </h1>
                  <div className={`network-topics ${!display && turnStatus?.required ? "network-action-required" : ""}`}>
                    {view?.topicCandidates?.map((id) => (
                      <MenuAction
                        disabled={locked || !snapshot.canChoose}
                        key={id}
                        onClick={() => void act({ type: "topic", topicId: id })}
                      >
                        {snapshot.titles[id]}
                      </MenuAction>
                    ))}
                  </div>
                </section>
              )}
              {(phase === "bonus-veto" || phase === "final-veto") && (
                <section className="topic-stage network-topic-stage">
                  <h1>{phase === "final-veto" ? "Финальная битва" : "Бонусный вопрос · ×2"}</h1>
                  {display && <p>
                    {snapshot.canVeto
                      ? snapshot.ownVeto ? "Для замены выберите свободную тему или снимите свой запрет." : "Исключите одну свободную тему."
                      : display
                        ? `Запрещают темы: ${snapshot.vetoParticipants?.join(", ")}`
                        : "Другие игроки исключают темы"}
                  </p>}
                  <div className={`network-topics ${!display && turnStatus?.required ? "network-action-required" : ""}`}>
                    {view?.topicCandidates?.map((id) => {
                      const veto = snapshot.vetoes?.find(
                        (entry) => entry.topicId === id,
                      );
                      const vetoedByOther =
                        !!veto && veto.playerId !== snapshot.selfId;
                      return (
                        <MenuAction
                          className={snapshot.ownVeto === id ? "selected" : ""}
                          disabled={locked || !snapshot.canVeto || vetoedByOther}
                          key={id}
                          onClick={() => void act({ type: "veto", topicId: id })}
                        >
                          {snapshot.titles[id]}
                          {display ? (
                            <small>
                              {Object.entries(view.vetoes ?? {})
                                .filter(([, topic]) => topic === id)
                                .map(
                                  ([player]) =>
                                    snapshot.players.find((p) => p.id === player)
                                      ?.name,
                                )
                                .join(", ")}
                            </small>
                          ) : veto ? (
                            <small>
                              {vetoedByOther
                                ? `Исключил: ${veto.name}`
                                : "Ваш запрет"}
                            </small>
                          ) : null}
                        </MenuAction>
                      );
                    })}
                  </div>
                  {snapshot.canVeto && snapshot.ownVeto && (
                    <MenuAction
                      disabled={locked}
                      onClick={() => void act({ type: "clear-veto" })}
                    >
                      Снять запрет
                    </MenuAction>
                  )}
                </section>
              )}
              {phase === "topic-confirmation" && (
                <section className="topic-confirmation-stage network-confirmation">
                  <p>
                    {view?.confirmationBonus ? "Бонусная тема" : "Тема вопроса"}
                  </p>
                  <h1>{snapshot.titles[view?.topicId ?? ""]}</h1>
                  <strong>{seconds(view?.confirmationRemainingMs ?? 0)}</strong>
                </section>
              )}
              {(phase === "answering" || phase === "reveal") &&
                view?.question && (
                  <div
                    className={`question-stage network-question-area ${phase === "reveal" ? "revealed question-stage--reveal" : ""}`}
                  >
                    <h1 className="network-question">{view.question.prompt}</h1>
                    <div className={`network-answers ${turnStatus?.required ? "network-action-required" : ""}`}>
                      {positions.map((position) => {
                        const question = view.question!;
                        const chosen = snapshot.ownAnswer === position;
                        const correct = phase === "reveal" && question.correctPosition === position;
                        const wrong =
                          phase === "reveal" &&
                          (snapshot.revealedChoices ?? []).some(
                            (c) =>
                              c.answerPosition === position &&
                              c.result === "wrong",
                          );
                        return (
                          <MenuAction
                            key={position}
                            className={`${chosen ? "selected" : ""} ${correct ? "correct" : ""} ${wrong ? "wrong" : ""}`}
                            disabled={
                              locked ||
                              !snapshot.canAnswer ||
                              phase !== "answering"
                            }
                            onClick={() =>
                              void act({ type: "answer", position })
                            }
                          >
                            <span className="network-answer-letter">
                              {letters[position]}
                            </span>
                            <span>{question.options[position]}</span>
                            {phase === "reveal" && (
                              <small>
                                {display ? (
                                  <span className="network-answer-players" aria-label={correct ? "Правильный ответ" : "Неверный ответ"}>
                                    {(snapshot.revealedChoices ?? []).filter(c => c.answerPosition === position).map(c => (
                                      <span key={c.id} className="network-answer-player" title={c.name} aria-label={c.name}>{c.id.replace("player-", "")}</span>
                                    ))}
                                  </span>
                                ) : <>
                                  {correct ? "✓ Правильный ответ · " : wrong ? "✕ Неверный ответ · " : ""}
                                  {(snapshot.revealedChoices ?? []).filter(c => c.answerPosition === position).map(c => c.name).join(", ")}
                                </>}
                              </small>
                            )}
                          </MenuAction>
                        );
                      })}
                    </div>
                    {phase === "reveal" && (
                      <div className="network-explanation explanation">
                        <strong>Почему так?</strong>
                        {view.question.explanation?.map((line, i) => (
                          <p key={i}>{line}</p>
                        ))}
                        {view.question.source && (
                          <a
                            href={view.question.source.url}
                            target="_blank"
                            rel="noreferrer"
                          >
                            Источник: {view.question.source.title} ↗
                          </a>
                        )}
                        {view.question.answerNotes?.some((note) => note.position !== view.question?.correctPosition) && (
                          <section className="wrong-answer-notes" aria-label="Справки к неправильным вариантам">
                            {view.question.answerNotes.filter((note) => note.position !== view.question?.correctPosition).map((note) => (
                              <article key={note.position}>
                                <b>{note.answer}</b>
                                <p>{note.note}</p>
                              </article>
                            ))}
                          </section>
                        )}
                      </div>
                    )}
                  </div>
                )}
              {phase === "difficulty-feedback" && (
                <>
                  <h1>Хотите пожаловаться на вопрос?</h1>
                  {snapshot.isLeader && view?.feedback ? (
                    <div className="network-feedback">
                      {view.feedback.stage === "choice" ? (
                        <>
                          <MenuAction
                            disabled={locked}
                            onClick={() =>
                              void act({
                                type: "feedback-choice",
                                complaint: true,
                              })
                            }
                          >
                            Да
                          </MenuAction>
                          <MenuAction
                            variant="primary"
                            disabled={locked}
                            onClick={() =>
                              void act({
                                type: "feedback-choice",
                                complaint: false,
                              })
                            }
                          >
                            Нет, дальше
                          </MenuAction>
                        </>
                      ) : view.feedback.stage === "reasons" ? (
                        <>
                          <div className={`network-topics ${!display && turnStatus?.required ? "network-action-required" : ""}`}>
                            {reasons.map((label, index) => (
                              <MenuAction
                                key={label}
                                className={
                                  view.feedback!.complaintReasons.includes(
                                    reasonKeys[index] as never,
                                  )
                                    ? "selected"
                                    : ""
                                }
                                disabled={locked}
                                onClick={() =>
                                  void act({ type: "feedback-reason", index })
                                }
                              >
                                {label}
                              </MenuAction>
                            ))}
                          </div>
                          <label>
                            Комментарий
                            <textarea
                              maxLength={500}
                              value={feedbackNote}
                              onChange={(e) => setFeedbackNote(e.target.value)}
                            />
                          </label>
                          <MenuAction
                            disabled={locked}
                            onClick={() =>
                              void act({
                                type: "feedback-submit",
                                note: feedbackNote,
                              })
                            }
                          >
                            Отправить
                          </MenuAction>
                        </>
                      ) : (
                        <p>Сохраняем отзыв…</p>
                      )}
                      {snapshot.feedbackError && !snapshot.paused && !localMenuOpen && !pauseSettingsOpen && (
                        <FeedbackUnavailableDialog
                          selected={feedbackRecoveryChoice}
                          onSelect={setFeedbackRecoveryChoice}
                          onRetry={() => { setFeedbackRecoveryChoice("retry"); void act({ type: "retry-feedback" }); }}
                          onSkip={() => { setFeedbackRecoveryChoice("retry"); void act({ type: "skip-feedback" }); }}
                        />
                      )}
                    </div>
                  ) : (
                    <p>Ведущий собирает общий отзыв о вопросе.</p>
                  )}
                </>
              )}
              {(phase === "standings" || phase === "finished") && (
                <section className="standings-stage network-results">
                  <h1>
                    {phase === "finished"
                      ? snapshot.endReason
                        ? "Партия завершена: остался один игрок"
                        : view?.winnerId ? `Победитель — ${snapshot.players.find(p => p.id === view.winnerId)?.name}` : "Игра завершена"
                      : snapshot.tieBreakNumber ? "Результаты основной игры · впереди финальная битва" : "Результаты этапа"}
                  </h1>
                  <table className="network-standings" aria-label="Результаты всех игроков">
                    <thead>
                      <tr>
                        <th scope="col" className="network-standing-rank" aria-label="Место">#</th>
                        <th scope="col">Игрок</th>
                        <th scope="col" className="network-standing-score">Очки</th>
                        <th scope="col" className="network-standing-stat" aria-label="Правильные ответы"><abbr title="Правильные ответы">✓</abbr></th>
                        <th scope="col" className="network-standing-stat" aria-label="Неверно, включая отсутствие ответа"><abbr title="Неверно, включая отсутствие ответа">✕</abbr></th>
                      </tr>
                    </thead>
                    <tbody>
                      {view?.standings?.map((row) => {
                        const player = snapshot.players.find((p) => p.id === row.teamId);
                        const self = row.teamId === snapshot.selfId;
                        return (
                          <tr key={row.teamId} className={self ? "network-standing--self" : ""} aria-current={self ? "true" : undefined}>
                            <td>{player?.departed ? "—" : row.rank}</td>
                            <th scope="row" className="network-standing-name">{player?.name}{self ? " · Вы" : ""}{player?.departed && <small>Выбыл</small>}</th>
                            <td className="network-standing-score">{row.score}</td>
                            <td>{row.correct}</td>
                            <td>{row.incorrect + row.noAnswer}</td>
                          </tr>
                        );
                      })}
                    </tbody>
                  </table>
                  <p className="network-standings-key">✓ верно · ✕ неверно, включая пропуски</p>
                </section>
              )}
              {phase === "finished" && snapshot.isLeader && (
                <div className="network-actions">
                  <MenuAction
                    variant="primary"
                    disabled={busy || !!status}
                    onClick={() => void act({ type: "replay" })}
                  >
                    Сыграть ещё
                  </MenuAction>
                  <MenuAction
                    disabled={busy}
                    onClick={() => void exitRoom()}
                  >
                    Выйти в меню
                  </MenuAction>
                </div>
              )}
              {display && playerCards}
            </section>
          )}
          {(snapshot.paused || localMenuOpen) && !pauseSettingsOpen && !complaint && (
            <SessionMenu
              title={snapshot.paused ? "Игра на паузе" : "Сетевая игра"}
              disabled={busy}
              resumeDisabled={!!status}
              resume={snapshot.paused && snapshot.isLeader ? () => void act({ type: "resume" }) : undefined}
              complaint={snapshot.complaintContext ? () => setComplaint(snapshot.complaintContext!) : undefined}
              settings={() => setPauseSettingsOpen(true)}
              restart={snapshot.isLeader && phase !== "lobby" ? () => void act({ type: "replay" }) : undefined}
              restartLabel="Вернуться в лобби"
              exit={(phase === "lobby" ? display : snapshot.isLeader) ? () => void exitRoom() : () => navigate("/")}
              exitLabel={(phase === "lobby" ? display : snapshot.isLeader) ? "Завершить игру" : "Выйти в меню"}
              back={!snapshot.paused ? () => setLocalMenuOpen(false) : undefined}
            >
              {snapshot.paused && <>
                {!snapshot.displayConnected && <p>Ждём возвращения общего экрана</p>}
                {display && snapshot.disconnected.map((player) => <div key={player.id}><p>{player.name} отключился</p><MenuAction disabled={busy} onClick={() => void act({ type: "exclude", playerId: player.id })}>Продолжить без {player.name}</MenuAction></div>)}
                <p>{snapshot.isLeader ? "Когда все вернутся, продолжите игру." : "Ждём подключения игроков и команды ведущего."}</p>
              </>}
              {!snapshot.paused && phase !== "lobby" && phase !== "finished" && <p>Сетевая партия продолжается. Общей паузой управляет ведущий.</p>}
            </SessionMenu>
          )}
        </>
      )}
      {complaint && snapshot?.complaintContext?.eventId === complaint.eventId && snapshot.isLeader && <ComplaintDialog context={complaint} close={() => { setComplaint(null); if (snapshot.paused) void act({ type: 'resume' }); else setLocalMenuOpen(false); }} />}
      {pauseSettingsOpen && (
        <SettingsDialog preferences={preferences} setPreferences={savePreferences} back={() => setPauseSettingsOpen(false)} />
      )}
    </ScreenSurface>
  );
}
