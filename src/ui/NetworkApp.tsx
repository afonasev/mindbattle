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
  phaseAudioActions,
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
import { PresentationSettings } from "./PresentationSettings";
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
  const [feedbackNote, setFeedbackNote] = useState("");
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
  const muted =
    new URLSearchParams(location.search).get("muted") === "1" ||
    preferences.muted;
  const connection = useRef<NetworkConnection | null>(null);
  const audio = useRef<AudioController | null>(null);
  const lastPhase = useRef("");
  const revealAudio = useRef(new RevealAudioMonitor());
  const confirmationAudio = useRef(new TopicCountdownAudioMonitor());
  const enableAudio = () => {
    if (!mobile && !audio.current)
      audio.current = sharedAudioController({
        volume: preferences.volume,
        muted,
      });
  };
  useEffect(() => {
    audio.current?.update({ volume: preferences.volume, muted });
    if (muted) audio.current?.stopMusic();
  }, [muted, preferences.volume]);
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
    const signature = `${snapshot.epoch}:${snapshot.phase}`;
    if (lastPhase.current === signature) return;
    const previousPhase = lastPhase.current.split(":")[1] || null;
    lastPhase.current = signature;
    if (snapshot.paused) return;
    for (const action of phaseAudioActions(previousPhase, snapshot.phase)) {
      if (action.type === "stop-music") audio.current?.stopMusic();
      else if (action.type === "set-music-ducked") audio.current?.setMusicDucked(action.ducked);
      else audio.current?.play(action.cue);
    }
    if (snapshot.phase === "lobby") audio.current?.play("menu-theme");
  }, [snapshot?.phase, snapshot?.epoch, mobile]);
  useEffect(() => {
    if (!snapshot || !shouldPlayNetworkAudio(snapshot.role, mobile) || snapshot.paused || snapshot.phase !== "reveal" || !snapshot.view) {
      if (snapshot?.phase !== "reveal") revealAudio.current.reset();
      return;
    }
    const signature = `${snapshot.epoch}:${snapshot.phaseRevision}`;
    for (const cue of revealAudio.current.observe(signature, snapshot.view.teams.map(({ result }) => ({ result: result ?? "no-answer" })))) {
      audio.current?.play(cue);
    }
  }, [snapshot?.epoch, snapshot?.phase, snapshot?.phaseRevision, snapshot?.paused, snapshot?.view, mobile]);
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
    if (snapshot?.paused) audio.current?.stopMusic();
  }, [snapshot?.paused]);
  useEffect(() => () => audio.current?.stopMusic(), []);
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
    if (!snapshot || !connection.current || busy) return;
    setBusy(true);
    setError("");
    enableAudio();
    try {
      await connection.current.command(snapshot, action);
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setBusy(false);
    }
  }
  function reset() {
    if (credential) forgetCredential(credential);
    setCredential(null);
    setSnapshot(null);
    setTerminal(false);
    setStatus("");
    setError("");
  }
  const locked = busy || !!status || !!snapshot?.paused;
  const view = snapshot?.view;
  const own = view?.teams[0];
  const phase = snapshot?.phase;
  const display = snapshot?.role === "display";
  const canSkipConfirmation =
    mobile &&
    !!snapshot?.isLeader &&
    phase === "topic-confirmation" &&
    !locked;
  return (
    <main
      className={`game-shell network-app ${mobile ? "network-mobile" : "network-display"} ${preferences.textSize === "large" ? "network-text-large" : ""} ${preferences.highContrast ? "network-high-contrast" : ""} ${preferences.reducedMotion ? "reduced-motion" : ""}`}
      onClick={
        canSkipConfirmation
          ? (event) => {
              event.preventDefault();
              void act({ type: "continue" });
            }
          : undefined
      }
    >
      <header className="game-brand network-header">
        <a href="/">MINDBATTLE</a>
        <span>Сетевая игра{snapshot ? ` · ${snapshot.code}` : ""}</span>
      </header>
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
          <button onClick={reset}>Вернуться к подключению</button>
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
              <button
                className="network-primary"
                disabled={busy || code.length !== 4}
              >
                Подключиться
              </button>
            </form>
          ) : (
            <button
              className="network-primary"
              disabled={busy}
              onClick={() => void enter(true)}
            >
              Создать сетевую игру
            </button>
          )}
        </section>
      ) : !snapshot ? (
        <section className="network-entry">
          <p>Ожидаем состояние комнаты…</p>
          <button onClick={reset}>Другая комната</button>
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
                          <button
                            disabled={busy}
                            onClick={() =>
                              void act({ type: "leader", playerId: p.id })
                            }
                          >
                            Ведущий
                          </button>
                          <button
                            aria-label={`Удалить ${p.name}`}
                            disabled={busy}
                            onClick={() =>
                              void act({ type: "remove", playerId: p.id })
                            }
                          >
                            Удалить
                          </button>
                        </span>
                      )}
                    </li>
                  ))}
                </ul>
                {display && (
                  <>
                    <div className="network-settings">
                      <label>
                        Вопросов
                        <select
                          aria-label="Вопросов"
                          value={snapshot.settings.questionCount}
                          onChange={(e) =>
                            void act({
                              type: "settings",
                              ...snapshot.settings,
                              questionCount: Number(e.target.value),
                            })
                          }
                        >
                          {[9, 15, 21].map((n) => (
                            <option key={n}>{n}</option>
                          ))}
                        </select>
                      </label>
                      <label>
                        Время на ответ
                        <select
                          aria-label="Время на ответ"
                          value={snapshot.settings.answerTimeMs}
                          onChange={(e) =>
                            void act({
                              type: "settings",
                              ...snapshot.settings,
                              answerTimeMs: Number(e.target.value),
                            })
                          }
                        >
                          {[10000, 20000, 30000].map((n) => (
                            <option key={n} value={n}>
                              {n / 1000} секунд
                            </option>
                          ))}
                        </select>
                      </label>
                    </div>
                    <button
                      className="network-primary"
                      disabled={
                        busy ||
                        snapshot.players.length < 2 ||
                        snapshot.players.some((p) => !p.connected)
                      }
                      onClick={() => void act({ type: "start" })}
                    >
                      Начать игру
                    </button>
                    <button onClick={() => void act({ type: "close" })}>
                      Закрыть комнату
                    </button>
                  </>
                )}
              </div>
            </section>
          ) : (
            <section className="network-match">
              <div className="network-round-heading">
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
                      <button
                        className="network-primary"
                        disabled={locked}
                        onClick={() => void act({ type: "continue" })}
                      >
                        Дальше
                      </button>
                    )}
                    <button
                      disabled={busy || !!status}
                      onClick={() => void act({ type: "pause" })}
                    >
                      Пауза
                    </button>
                  </div>
                )}
              </div>
              {view && (!display || (phase !== "standings" && phase !== "finished")) && (
                <div className="network-cards">
                  {view.teams.map((card, i) => (
                    <article
                      className={`network-player-card ${card.departed ? "departed" : ""}`}
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
                      <b>{card.score}</b>
                      <small>
                        {card.departed
                          ? "Выбыл"
                          : card.remainingMs !== undefined
                            ? `Время: ${seconds(card.remainingMs)} с`
                            : card.hasAnswered && phase === "answering"
                              ? "✓ Ответ принят"
                              : `Запас: ${seconds(card.reserveMs)} с`}
                      </small>
                      {card.result && (
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
              )}
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
                  <h1>
                    {snapshot.canChoose
                      ? "Выберите тему"
                      : display
                        ? `Выбирает ${snapshot.players.find((p) => p.id === view?.chooser)?.name ?? "игрок"}`
                        : `Выбирает ${snapshot.chooserName ?? "игрок"}`}
                  </h1>
                  <div className="network-topics">
                    {view?.topicCandidates?.map((id) => (
                      <button
                        disabled={locked || !snapshot.canChoose}
                        key={id}
                        onClick={() => void act({ type: "topic", topicId: id })}
                      >
                        {snapshot.titles[id]}
                      </button>
                    ))}
                  </div>
                </section>
              )}
              {phase === "bonus-veto" && (
                <section className="topic-stage network-topic-stage">
                  <h1>Бонусный вопрос · ×2</h1>
                  <p>
                    {snapshot.canVeto
                      ? "Запретите одну свободную тему. Свой запрет можно изменить."
                      : display
                        ? `Запрещают темы: ${snapshot.vetoParticipants?.join(", ")}`
                        : "Тему выбирают участники очереди"}
                  </p>
                  <div className="network-topics">
                    {view?.topicCandidates?.map((id) => {
                      const veto = snapshot.vetoes?.find(
                        (entry) => entry.topicId === id,
                      );
                      const vetoedByOther =
                        !!veto && veto.playerId !== snapshot.selfId;
                      return (
                        <button
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
                        </button>
                      );
                    })}
                  </div>
                  {snapshot.canVeto && snapshot.ownVeto && (
                    <button
                      disabled={locked}
                      onClick={() => void act({ type: "clear-veto" })}
                    >
                      Снять запрет
                    </button>
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
                    className={`question-stage network-question-area ${phase === "reveal" ? "revealed" : ""}`}
                  >
                    <h1 className="network-question">{view.question.prompt}</h1>
                    <div className="network-answers">
                      {positions.map((position) => {
                        const question = view.question!;
                        const chosen = snapshot.ownAnswer === position;
                        const correct = question.correctPosition === position;
                        const wrong =
                          phase === "reveal" &&
                          view.teams.some(
                            (c) =>
                              c.answerPosition === position &&
                              c.result === "wrong",
                          );
                        return (
                          <button
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
                                {correct ? "✓ Правильный ответ " : ""}
                                {view.teams
                                  .filter((c) => c.answerPosition === position)
                                  .map((c) => c.name)
                                  .join(", ")}
                              </small>
                            )}
                          </button>
                        );
                      })}
                    </div>
                    {phase === "answering" && snapshot.ownAnswer && (
                      <p role="status">
                        Ответ принят. Его можно изменить до раскрытия.
                      </p>
                    )}
                    {phase === "reveal" && (
                      <div className="network-explanation">
                        {view.question.explanation?.map((line, i) => (
                          <p key={i}>{line}</p>
                        ))}
                        {view.question.wrongAnswerNotes?.map((note) => (
                          <p key={note.position}>
                            <strong>{note.answer}:</strong> {note.note}
                          </p>
                        ))}
                        {view.question.source && (
                          <a
                            href={view.question.source.url}
                            target="_blank"
                            rel="noreferrer"
                          >
                            {view.question.source.title}
                          </a>
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
                          <button
                            disabled={locked}
                            onClick={() =>
                              void act({
                                type: "feedback-choice",
                                complaint: true,
                              })
                            }
                          >
                            Да
                          </button>
                          <button
                            className="network-primary"
                            disabled={locked}
                            onClick={() =>
                              void act({
                                type: "feedback-choice",
                                complaint: false,
                              })
                            }
                          >
                            Нет, дальше
                          </button>
                        </>
                      ) : view.feedback.stage === "reasons" ? (
                        <>
                          <div className="network-topics">
                            {reasons.map((label, index) => (
                              <button
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
                              </button>
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
                          <button
                            disabled={locked}
                            onClick={() =>
                              void act({
                                type: "feedback-submit",
                                note: feedbackNote,
                              })
                            }
                          >
                            Отправить
                          </button>
                        </>
                      ) : (
                        <p>Сохраняем отзыв…</p>
                      )}
                      {snapshot.feedbackError && (
                        <>
                          <p role="alert">{snapshot.feedbackError}</p>
                          <button
                            disabled={locked}
                            onClick={() => void act({ type: "retry-feedback" })}
                          >
                            Повторить отправку
                          </button>
                        </>
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
                        : display && view?.winnerId ? `Победитель — ${snapshot.players.find(p => p.id === view.winnerId)?.name}` : "Игра завершена"
                      : "Результаты этапа"}
                  </h1>
                  {display ? (
                    <div className="network-standings">
                      {view?.standings?.map((row) => {
                        const player = snapshot.players.find(
                          (p) => p.id === row.teamId,
                        );
                        return (
                          <div key={row.teamId}>
                            <span>{player?.departed ? "—" : row.rank}</span>
                            <strong>
                              {player?.name}
                              {player?.departed ? " · Выбыл" : ""}
                            </strong>
                            <span>
                              {row.correct} верно · {row.incorrect} неверно ·{" "}
                              {row.noAnswer} без ответа
                            </span>
                            <b>{row.score}</b>
                          </div>
                        );
                      })}
                    </div>
                  ) : (
                    <p>
                      Ваш результат: <strong>{own?.score ?? 0} очков</strong>.
                      Общие итоги — на большом экране.
                    </p>
                  )}
                </section>
              )}
              {phase === "finished" && snapshot.isLeader && (
                <div className="network-actions">
                  <button
                    className="network-primary"
                    disabled={busy || !!status}
                    onClick={() => void act({ type: "replay" })}
                  >
                    Сыграть ещё
                  </button>
                  <button
                    disabled={busy}
                    onClick={() => void act({ type: "close" })}
                  >
                    Выйти в меню
                  </button>
                </div>
              )}
            </section>
          )}
          {snapshot.paused && phase !== "finished" && (
            <div
              className="network-pause"
              role="dialog"
              aria-modal="true"
              aria-labelledby="network-pause-title"
            >
              <section>
                <h2 id="network-pause-title">Игра на паузе</h2>
                {!snapshot.displayConnected && (
                  <p>Ждём возвращения общего экрана</p>
                )}
                {display &&
                  snapshot.disconnected.map((p) => (
                    <div key={p.id}>
                      <p>{p.name} отключился</p>
                      <button
                        disabled={busy}
                        onClick={() =>
                          void act({ type: "exclude", playerId: p.id })
                        }
                      >
                        Продолжить без {p.name}
                      </button>
                    </div>
                  ))}
                {(snapshot.isLeader || display) && (
                  <button disabled={busy} onClick={() => setPauseSettingsOpen(true)}>Настройки</button>
                )}
                {snapshot.isLeader ? (
                  <>
                    <p>Когда все вернутся, продолжите игру.</p>
                    <button
                      className="network-primary"
                      disabled={busy || !!status}
                      onClick={() => void act({ type: "resume" })}
                    >
                      Продолжить
                    </button>
                    <button
                      disabled={busy}
                      onClick={() => void act({ type: "replay" })}
                    >
                      Вернуться в лобби
                    </button>
                    <button
                      disabled={busy}
                      onClick={() => void act({ type: "close" })}
                    >
                      Завершить игру
                    </button>
                  </>
                ) : (
                  <p>Ждём подключения игроков и команды ведущего.</p>
                )}
              </section>
            </div>
          )}
        </>
      )}
      {pauseSettingsOpen && (
        <div className="pause-backdrop" role="dialog" aria-modal="true" aria-labelledby="menu-settings-title">
          <PresentationSettings preferences={preferences} setPreferences={savePreferences} back={() => setPauseSettingsOpen(false)} />
        </div>
      )}
    </main>
  );
}
