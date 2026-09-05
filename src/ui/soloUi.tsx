import type { Question } from "../content";
import type { SoloCommand, SoloState } from "../domain/solo";
import type { SoloRecord } from "../adapters/storage";
import type { AnswerPosition, ComplaintReason } from "../domain/types";

const labels = { up: "↑", right: "→", down: "↓", left: "←" } as const;
type SoloInputKind = "pointer" | "wasd" | "arrows" | "gamepad";

function inputHint(input: SoloInputKind, position?: AnswerPosition): string {
  if (input === "pointer") return position ? "Клик" : "Кликните карточку";
  if (input === "wasd") return position ? ({ up: "W", right: "D", down: "S", left: "A" } as const)[position] : "A/D · S";
  if (input === "arrows") return position ? labels[position] : "←/→ · Enter";
  return position ? labels[position] : "D-pad · A";
}

export function SoloScreen({ state, question, titleById, records, savedRecordId, inputKind, command, finish, exit }: {
  readonly state: SoloState;
  readonly question: Question | undefined;
  readonly titleById: Readonly<Record<string, string>>;
  readonly records: readonly SoloRecord[];
  readonly savedRecordId: string | null;
  readonly inputKind: SoloInputKind;
  readonly command: (command: SoloCommand) => void;
  readonly finish: (name: string) => void;
  readonly exit: () => void;
}) {
  const phase = state.phase;
  if (phase.kind === "finished") {
    if (savedRecordId) {
      const rank = records.findIndex((record) => record.id === savedRecordId) + 1;
      return <SoloFrame><section className="winner-stage solo-results"><div className="stage-label stage-label--bonus">Соло-рекорд</div><h2>Ваш результат: {state.score}</h2><ol>{records.slice(0, 10).map((record, index) => <li className={record.id === savedRecordId ? "solo-current" : ""} key={record.id}><span className="solo-record-rank">{index + 1}</span><strong>{record.name}</strong><b>{record.score}</b></li>)}</ol><p className="solo-rank">Ваше место: {rank} из {records.length} · {state.score} очков</p><button className="secondary-action" type="button" onClick={exit}>В меню</button><p className="control-help">Enter или Space · В меню</p></section></SoloFrame>;
    }
    return <NameEntry score={state.score} finish={finish} />;
  }
  const hearts = Array.from({ length: 3 }, (_, index) => <span key={index} className={index < state.lives ? "solo-heart" : "solo-heart solo-heart--empty"}>♥</span>);
  if (state.paused) return <SoloFrame><div className="pause-backdrop" role="dialog" aria-modal="true" aria-labelledby="solo-pause-title"><section className="pause-dialog"><div className="stage-label">Пауза</div><h2 id="solo-pause-title">Соло-забег восстановлен</h2><p>Таймеры остановлены.</p><button type="button" onClick={() => command({ type: "resume" })}>Продолжить</button><button type="button" onClick={exit}>Выйти в меню</button></section></div></SoloFrame>;
  const timerMs = phase.kind === "answering" ? (phase.baseRemainingMs > 0 ? phase.baseRemainingMs : state.reserveMs) : null;
  const reserve = phase.kind === "answering" && phase.baseRemainingMs === 0;
  const playerResultClass = phase.kind === "reveal" ? `game-team-card--${phase.result}` : "";
  return <SoloFrame>
    {phase.kind === "topic" && <section className="topic-stage solo-topic-stage"><div className="stage-label">Выбор темы</div><h2>Выберите тему</h2><div className="topic-cards topic-cards--three">{phase.candidates.map((topicId, index) => <button type="button" className={index === phase.cursor ? "topic-choice topic-choice--current" : "topic-choice"} onClick={() => command({ type: "select-topic", index: index as 0 | 1 | 2 })} key={topicId}>{titleById[topicId] ?? topicId}</button>)}</div><p className="control-help">{inputHint(inputKind)}</p></section>}
    {phase.kind === "risk" && <section className="topic-confirmation-stage solo-risk"><div className="stage-label stage-label--bonus">Бонусный вопрос · x3</div><h2>Рискнёте?</h2><p>Тема будет выбрана случайно. Верный ответ: <strong>+{({ easy: 300, medium: 600, hard: 900 })[phase.difficulty]}</strong>. Отказ: <strong>−{({ easy: 100, medium: 200, hard: 300 })[phase.difficulty]}</strong>.</p><div className="topic-cards topic-cards--two solo-risk-actions"><button type="button" className={(phase.cursor ?? 0) === 0 ? "topic-choice topic-choice--current" : "topic-choice"} onClick={() => command({ type: "accept-risk" })}>Принять риск</button><button type="button" className={(phase.cursor ?? 0) === 1 ? "topic-choice topic-choice--current" : "topic-choice"} onClick={() => command({ type: "decline-risk" })}>Отказаться</button></div><p className="control-help">A/D или ←/→ · Enter</p></section>}
    {(phase.kind === "answering" || phase.kind === "reveal") && question && <SoloQuestionBoard phase={phase} question={question} questionNumber={state.slotIndex + 1} titleById={titleById} inputKind={inputKind} command={command} />}
    <ul className="game-team-strip solo-team-strip" aria-label="Состояние игрока"><li className={["game-team-card", "team-color--green", playerResultClass].filter(Boolean).join(" ")}><span className="solo-player-mark" aria-hidden="true">И</span><span className="team-card-name">Игрок</span><strong>{state.score}</strong><span className="solo-lives" aria-label={`Жизни: ${state.lives} из 3`}>{hearts}</span>{timerMs !== null && <span className={reserve ? "team-question-timer team-question-timer--reserve" : "team-question-timer"} aria-label={reserve ? "Расходуется общий запас времени" : "Остаток базового времени"}>{Math.ceil(timerMs / 1000)}</span>}</li></ul>
  </SoloFrame>;
}

function SoloFrame({ children }: { readonly children: React.ReactNode }) {
  return <main className="game-shell solo-shell"><div className="arena-glow" aria-hidden="true" /><header className="game-brand"><strong>Mindbattle</strong><span>Соло-забег</span></header>{children}<footer>ESC · пауза</footer></main>;
}

function SoloQuestionBoard({ phase, question, questionNumber, titleById, inputKind, command }: { readonly phase: Extract<SoloState["phase"], { kind: "answering" | "reveal" }>; readonly question: Question; readonly questionNumber: number; readonly titleById: Readonly<Record<string, string>>; readonly inputKind: SoloInputKind; readonly command: (command: SoloCommand) => void }) {
  const reveal = phase.kind === "reveal";
  const continueWithPointer = () => command({ type: "continue" });
  const wrongAnswer = reveal && phase.result === "wrong" && phase.answer
    ? question.answers[Number(phase.round.answerOrder[( ["up", "right", "down", "left"] as const).indexOf(phase.answer)].replace("answer-", ""))]
    : null;
  const wrongAnswerNote = wrongAnswer && typeof wrongAnswer !== "string" ? wrongAnswer : null;
  return <section className={reveal ? "question-stage question-stage--reveal solo-question" : "question-stage solo-question"}><header className="question-header"><span>{titleById[phase.round.topicId] ?? phase.round.topicId}</span><strong>{phase.round.risk ? "Бонус · x3" : `Вопрос ${questionNumber}`}</strong></header><h2>{question.prompt}</h2><div className="answer-cross">{phase.round.answerOrder.map((answerId, index) => { const answer = question.answers[Number(answerId.replace("answer-", ""))]; const position = (["up", "right", "down", "left"] as const)[index] as AnswerPosition; const text = typeof answer === "string" ? answer : answer.text; const selectedWrong = reveal && phase.result === "wrong" && phase.answer === position ? "answer-option--wrong" : ""; const className = ["answer-option", `answer-option--${position}`, reveal && position === phase.round.correctPosition ? "answer-option--correct" : "", selectedWrong].filter(Boolean).join(" "); return <button type="button" className={`${className} solo-answer-button`} disabled={reveal} onClick={() => command({ type: "answer", position })} key={answerId}><span className="answer-text"><kbd>{inputHint(inputKind, position)}</kbd>{text}</span></button>; })}</div>{reveal && <aside className="explanation" onClick={continueWithPointer}><strong>{phase.result === "correct" ? "Верно!" : "Правильный ответ"}</strong><p>{question.explanation}</p>{wrongAnswerNote && <section className="wrong-answer-notes" aria-label="Справки о выбранных неправильных ответах"><strong>А что означал выбранный вариант?</strong><article><b>{wrongAnswerNote.text}</b><p>{wrongAnswerNote.note}</p></article></section>}</aside>}</section>;
}

export function SoloFeedbackScreen({ value, choose, toggleReason, setNote, submit, pending, error }: {
  readonly value: Extract<SoloState["phase"], { kind: "feedback" }>;
  readonly choose: (hasComplaint: boolean) => void;
  readonly toggleReason: (reason: ComplaintReason) => void;
  readonly setNote: (note: string) => void;
  readonly submit: () => void;
  readonly pending: boolean;
  readonly error: string | null;
}) {
  const reasons: readonly [ComplaintReason, string][] = [["too-easy", "Слишком лёгкий"], ["too-hard", "Слишком сложный"], ["weak-answer-options", "Неправильные ответы очевидны"], ["unclear-wording", "Непонятная формулировка"], ["suspected-error", "Фактическая ошибка"], ["ambiguous-answer", "Неоднозначный ответ"], ["uninteresting-for-quiz", "Неинтересный для викторины"]];
  const choice = value.hasComplaint !== true;
  const canSubmitComplaint = value.complaintReasons.length > 0 || Boolean(value.complaintNote.trim());
  return <SoloFrame><section className="difficulty-feedback-stage solo-feedback" aria-labelledby="solo-feedback-title"><div className="stage-label">Фидбэк о вопросе</div><h2 id="solo-feedback-title">{choice ? "Хотите пожаловаться на вопрос?" : "Что не так с вопросом?"}</h2><p className="feedback-instruction">{choice ? "A/D или ←/→ — выбор" : "WASD или стрелки — курсор"} · Enter — подтвердить</p><div className="feedback-tag-board" role="list">{choice ? <><button type="button" className={value.feedbackCursor === 0 ? "feedback-tag feedback-tag--cursor" : "feedback-tag"} onClick={() => choose(true)}><strong>Да</strong></button><button type="button" className={value.feedbackCursor === 1 ? "feedback-tag feedback-tag--cursor" : "feedback-tag"} onClick={() => choose(false)}><strong>Нет</strong></button></> : <>{reasons.map(([reason, label], index) => <button type="button" className={value.feedbackCursor === index ? "feedback-tag feedback-tag--cursor" : "feedback-tag"} onClick={() => toggleReason(reason)} key={reason}><strong>{label}</strong>{value.complaintReasons.includes(reason) && <span className="feedback-tag-state">✓</span>}</button>)}<button type="button" className={value.feedbackCursor === 7 ? "feedback-tag feedback-tag--cursor" : "feedback-tag"} disabled={pending || !canSubmitComplaint} onClick={submit}><strong>{pending ? "Сохраняем…" : "Готово"}</strong></button></>}</div>{!choice && <label className="feedback-note">Заметка (необязательно, до 500 символов)<textarea value={value.complaintNote} maxLength={500} onChange={(event) => setNote(event.target.value)} /></label>}<p className={error ? "feedback-status feedback-status--error" : "feedback-status"} aria-live="polite">{error ? error : choice ? "«Нет» выбрано по умолчанию и тоже сохраняется" : "Выберите хотя бы одну причину или добавьте заметку, затем подтвердите «Готово»"}</p></section></SoloFrame>;
}

function NameEntry({ score, finish }: { readonly score: number; readonly finish: (name: string) => void }) {
  let input: HTMLInputElement | null = null;
  return <SoloFrame><section className="winner-stage solo-results"><div className="stage-label">Забег завершён</div><h2>Результат: {score}</h2><form className="solo-name-form" onSubmit={(event) => { event.preventDefault(); finish(input?.value ?? ""); }}><label>Ваше имя<input autoFocus maxLength={32} ref={(element) => { input = element; }} /></label><button className="primary-action" type="submit">Сохранить результат</button></form><p className="control-help">Enter · Сохранить результат</p></section></SoloFrame>;
}
