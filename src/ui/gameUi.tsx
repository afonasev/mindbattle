import type { TeamControlAssignment } from "../adapters";
import { GAMEPAD_GLYPHS, KEYBOARD_CONFIRM_GLYPHS, KEYBOARD_GLYPHS } from "../adapters";
import type {
  AnswerPosition,
  MatchState,
  PublicMatchView,
  StandingRow,
  TeamId
} from "../domain";

export const TEAM_META: Readonly<
  Record<TeamId, { readonly letter: string; readonly label: string }>
> = {
  green: { letter: "З", label: "Зелёная" },
  blue: { letter: "С", label: "Синяя" },
  yellow: { letter: "Ж", label: "Жёлтая" },
  red: { letter: "К", label: "Красная" }
};

const DIRECTIONS: readonly AnswerPosition[] = ["up", "right", "down", "left"];

export function TeamDiamond({ teamId }: { readonly teamId: TeamId }) {
  return (
    <span className={`team-diamond team-color--${teamId}`} aria-label={TEAM_META[teamId].label}>
      <span>{TEAM_META[teamId].letter}</span>
    </span>
  );
}

function controlGlyph(
  assignment: TeamControlAssignment | undefined,
  direction: AnswerPosition
): string {
  const cardinal = {
    up: "north",
    right: "east",
    down: "south",
    left: "west"
  } as const;
  if (!assignment) return "—";
  if (assignment.source.kind === "keyboard") {
    return KEYBOARD_GLYPHS[assignment.source.layout][cardinal[direction]];
  }
  return GAMEPAD_GLYPHS[assignment.source.profile].answer[cardinal[direction]];
}

export function DeviceGlyphs({
  assignments,
  direction
}: {
  readonly assignments: readonly TeamControlAssignment[];
  readonly direction: AnswerPosition;
}) {
  return (
    <span className="device-glyphs" aria-label="Клавиши ответа">
      {assignments.map((assignment) => (
        <kbd key={assignment.teamId}>
          <span className={`glyph-team-mini team-color--${assignment.teamId}`} aria-hidden="true">
            <span>{TEAM_META[assignment.teamId as TeamId].letter}</span>
          </span>
          {controlGlyph(assignment, direction)}
        </kbd>
      ))}
    </span>
  );
}

export function ConfirmGlyphs({ assignments }: { readonly assignments: readonly TeamControlAssignment[] }) {
  return (
    <span className="device-glyphs" aria-label="Кнопки подтверждения">
      {assignments.map((assignment) => (
        <kbd key={assignment.teamId}>
          <span className={`glyph-team-mini team-color--${assignment.teamId}`} aria-hidden="true"><span>{TEAM_META[assignment.teamId as TeamId].letter}</span></span>
          {assignment.source.kind === "keyboard"
            ? KEYBOARD_CONFIRM_GLYPHS[assignment.source.layout]
            : GAMEPAD_GLYPHS[assignment.source.profile].answer.south}
        </kbd>
      ))}
    </span>
  );
}

export function TeamCards({
  state,
  view,
  activeTeamIds
}: {
  readonly state: MatchState;
  readonly view: PublicMatchView;
  readonly activeTeamIds: readonly TeamId[];
}) {
  const answering = state.phase.kind === "answering";
  const baseRemainingMs = answering ? state.phase.baseRemainingMs : 0;
  const attemptsByTeam = answering
    ? new Map(state.phase.round.attempts.map((attempt) => [attempt.teamId, attempt]))
    : new Map();
  return (
    <ul className="game-team-strip" aria-label="Состояние команд">
      {view.teams
        .filter((team) => activeTeamIds.includes(team.id))
        .map((team) => {
          const awaitingAnswer = attemptsByTeam.get(team.id)?.status === "open";
          const timerMs = baseRemainingMs > 0 ? baseRemainingMs : team.reserveMs;
          const spendingReserve = baseRemainingMs === 0;
          return (
            <li
            key={team.id}
            className={[
              "game-team-card",
              `team-color--${team.id}`,
              team.result ? `game-team-card--${team.result}` : ""
            ].join(" ")}
          >
            <TeamDiamond teamId={team.id} />
            <span className="team-card-name">{TEAM_META[team.id].label}</span>
            <strong>{team.score}</strong>
            {answering && awaitingAnswer ? (
              <span
                className={spendingReserve ? "team-question-timer team-question-timer--reserve" : "team-question-timer"}
                aria-label={spendingReserve ? "Расходуется запас времени" : "Остаток базового времени"}
              >
                {Math.ceil(timerMs / 1000)}
              </span>
            ) : (
              <>
                <span className="team-reserve">Запас {Math.ceil(team.reserveMs / 1000)} c</span>
                <span className="answer-state" aria-label={team.hasAnswered ? "Ответ принят" : "Нет ответа"}>
                  {team.result === "correct"
                    ? "✓"
                    : team.result && team.result !== "spectator"
                      ? "×"
                      : team.hasAnswered
                        ? "✓"
                        : "·"}
                </span>
              </>
            )}
          </li>
          );
        })}
    </ul>
  );
}

export function TopicSelection({
  view,
  titleById,
  assignments
}: {
  readonly view: PublicMatchView;
  readonly titleById: Readonly<Record<string, string>>;
  readonly assignments: readonly TeamControlAssignment[];
}) {
  return (
    <section className="topic-stage" aria-labelledby="topic-title">
      <div className="stage-label">Выбор темы</div>
      <h2 id="topic-title">
        <TeamDiamond teamId={view.chooser!} /> {TEAM_META[view.chooser!].label} команда выбирает
      </h2>
      <div className="topic-cards topic-cards--three">
        {view.topicCandidates?.map((topicId, index) => (
          <div className={index === view.topicCursor ? "topic-choice topic-choice--current" : "topic-choice"} key={topicId}>
            {index === view.topicCursor && <span className="cursor-markers" aria-label="Курсор выбирающей команды"><TeamDiamond teamId={view.chooser!} /></span>}
            {titleById[topicId] ?? topicId}
          </div>
        ))}
      </div>
      <p className="control-help">←/→ курсор · подтвердить <ConfirmGlyphs assignments={assignments} /></p>
    </section>
  );
}

export function TopicConfirmation({
  view,
  titleById
}: {
  readonly view: PublicMatchView;
  readonly titleById: Readonly<Record<string, string>>;
}) {
  const presentation = view.confirmationPresentation ?? (view.confirmationBonus ? "bonus" : "normal");
  const bonus = presentation === "bonus";
  const final = presentation === "final";
  return (
    <section className="topic-confirmation-stage" aria-live="polite" aria-labelledby="confirmation-title">
      <div className={bonus ? "stage-label stage-label--bonus" : "stage-label"}>
        {bonus ? "Бонусный вопрос · x2" : final ? "Финальная тема" : "Тема выбрана"}
      </div>
      <h2 id="confirmation-title">{titleById[view.topicId ?? ""] ?? view.topicId}</h2>
      <strong className="topic-confirmation-countdown">
        {Math.ceil((view.confirmationRemainingMs ?? 0) / 1_000)}
      </strong>
      <span className="control-help">Нажмите любую клавишу</span>
    </section>
  );
}

export function BonusVeto({
  state,
  titleById,
  assignments
}: {
  readonly state: MatchState;
  readonly titleById: Readonly<Record<string, string>>;
  readonly assignments: readonly TeamControlAssignment[];
}) {
  const phase = state.phase;
  if (phase.kind !== "bonus-veto" && phase.kind !== "final-veto") return null;
  const final = phase.kind === "final-veto";
  const participants = final ? state.tieBreak?.contenders ?? [] : state.config.teams;
  return (
    <section className={final ? "topic-stage final-veto-stage" : "topic-stage bonus-stage"} aria-labelledby="bonus-title">
      <div className={final ? "stage-label" : "stage-label stage-label--bonus"}>{final ? "Финальная тема" : "Бонусный вопрос · x2"}</div>
      <h2 id="bonus-title">Запретите по одной разной теме</h2>
      <div className="topic-cards topic-cards--bonus">
        {phase.candidates.map((topicId, index) => {
          const vetoes = participants.filter((teamId) => phase.vetoes[teamId] === topicId);
          const cursors = participants.filter((teamId) => phase.cursors[teamId] === index);
          return (
            <div className={vetoes.length ? "topic-veto topic-veto--selected" : "topic-veto"} key={topicId}>
              <span>{titleById[topicId] ?? topicId}</span>
              <span className="veto-markers">
                {vetoes.map((teamId) => <TeamDiamond key={teamId} teamId={teamId} />)}
              </span>
              <span className="cursor-markers" aria-label="Курсоры команд">
                {cursors.map((teamId) => <TeamDiamond key={teamId} teamId={teamId} />)}
              </span>
            </div>
          );
        })}
      </div>
      <p className="control-help">←/→ курсор · подтвердить запрет <ConfirmGlyphs assignments={assignments} /> · ↑ снять запрет</p>
    </section>
  );
}

export function QuestionBoard({
  state,
  view,
  assignments,
  titleById
}: {
  readonly state: MatchState;
  readonly view: PublicMatchView;
  readonly assignments: readonly TeamControlAssignment[];
  readonly titleById: Readonly<Record<string, string>>;
}) {
  const question = view.question;
  if (!question || (state.phase.kind !== "answering" && state.phase.kind !== "reveal")) return null;
  const reveal = state.phase.kind === "reveal";
  const selectedWrong = new Set(
    view.teams
      .map((team) => team.answerPosition)
      .filter((position): position is AnswerPosition => Boolean(position) && position !== question.correctPosition)
  );
  const positionsByTeam = new Map(
    view.teams
      .filter((team) => team.answerPosition)
      .map((team) => [team.id, team.answerPosition] as const)
  );
  return (
    <section className={reveal ? "question-stage question-stage--reveal" : "question-stage"}>
      <header className="question-header">
        <span>{titleById[question.topicId] ?? question.topicId}</span>
        <strong>
          {state.phase.round.mode === "tie-break"
            ? `Финал ${state.tieBreak?.questionNumber ?? 1}`
            : `Вопрос ${state.mainQuestionIndex + 1} / ${state.config.questionCount}`}
        </strong>
      </header>
      <h2>{question.prompt}</h2>
      <div className="answer-cross">
        {DIRECTIONS.map((direction) => {
          const chosenTeams = view.teams.filter((team) => positionsByTeam.get(team.id) === direction);
          const className = [
            "answer-option",
            `answer-option--${direction}`,
            reveal && direction === question.correctPosition ? "answer-option--correct" : "",
            reveal && selectedWrong.has(direction) ? "answer-option--wrong" : ""
          ].join(" ");
          return (
            <article className={className} key={direction} data-position={direction}>
              <span className="answer-text">{question.options[direction]}</span>
              {!reveal && <DeviceGlyphs assignments={assignments} direction={direction} />}
              {reveal && (
                <span className="answer-team-markers">
                  {chosenTeams.map((team) => <TeamDiamond key={team.id} teamId={team.id} />)}
                </span>
              )}
            </article>
          );
        })}
      </div>
      {reveal && (
        <aside className="explanation">
          <strong>Почему так?</strong>
          <p>{question.explanation?.join(" ")}</p>
          {question.source && (
            <a href={question.source.url} target="_blank" rel="noopener noreferrer">
              Источник: {question.source.title} ↗
            </a>
          )}
          {question.wrongAnswerNotes && question.wrongAnswerNotes.length > 0 && (
            <section
              className="wrong-answer-notes"
              aria-label="Справки о выбранных неправильных ответах"
              style={{
                gridTemplateColumns: `repeat(${question.wrongAnswerNotes.length}, minmax(0, 1fr))`
              }}
            >
              <strong>А что означали другие выбранные варианты?</strong>
              {question.wrongAnswerNotes.map((item) => (
                <article key={item.position}>
                  <b>{item.answer}</b>
                  <p>{item.note}</p>
                </article>
              ))}
            </section>
          )}
          <span>Отпустите кнопки, затем нажмите любую назначенную клавишу</span>
        </aside>
      )}
    </section>
  );
}

export function DifficultyFeedbackScreen({
  feedback,
  status,
  error,
  assignments
}: {
  readonly feedback: NonNullable<PublicMatchView["feedback"]>;
  readonly status: "idle" | "pending" | "error";
  readonly error: string | null;
  readonly assignments: readonly TeamControlAssignment[];
}) {
  const feedbackItems = [
    ["like", "Да"], ["abstain", "Не уверен"], ["dislike", "Нет"],
    ["unfamiliar-topic", "Тема нам почти не знакома"],
    ["unclear-wording", "Непонятная формулировка"],
    ["suspected-error", "Вопрос содержит ошибку"],
    ["ambiguous-answer", "Неоднозначный ответ"],
    ["too-niche-or-uninteresting", "Слишком узко или неинтересно"],
    ["weak-answer-options", "Неправильные ответы слишком очевидные"], ["done", "Готово"]
  ] as const;
  const responses = Object.entries(feedback.responses) as readonly [TeamId, NonNullable<PublicMatchView["feedback"]>["responses"][TeamId]][];
  const renderItem = ([tag, label]: readonly [string, string], index: number) => {
    const markers = responses.filter(([, response]) => response.similarityPreference === tag || response.diagnosticFlags.includes(tag as never));
    const cursors = responses.filter(([, response]) => !response.completed && response.tagCursor === index);
    return <article key={tag} className={cursors.length > 0 ? "feedback-tag feedback-tag--cursor" : "feedback-tag"} role="listitem">
      <strong>{label}</strong>
      <span className="feedback-tag-state">
        {markers.length > 0 && <span className="feedback-tag-markers" aria-label="Команды, выбравшие этот пункт">{markers.map(([teamId]) => <TeamDiamond key={teamId} teamId={teamId} />)}</span>}
        {cursors.length > 0 && <span className="feedback-cursors" aria-label="Команды, чей курсор находится на этом пункте">{cursors.map(([teamId]) => <TeamDiamond key={teamId} teamId={teamId} />)}</span>}
      </span>
    </article>;
  };
  return (
    <section className="difficulty-feedback-stage" aria-labelledby="difficulty-feedback-title">
      <div className="stage-label">Фидбэк о вопросе</div>
      <h2 id="difficulty-feedback-title">{feedback.stage === "difficulty" ? "Насколько вопрос был сложен для вашей команды?" : "Отметьте впечатление от вопроса"}</h2>
      {feedback.stage === "difficulty" ? <>
        <p className="feedback-instruction">Выберите скрытую оценку. Ваша оценка останется скрытой.</p>
        <div className="difficulty-feedback-options" aria-label="Варианты сложности">
          <article className="difficulty-feedback-option"><kbd>←</kbd><strong>Тривиальный</strong></article>
          <article className="difficulty-feedback-option"><kbd>↑</kbd><strong>Лёгкий</strong></article>
          <article className="difficulty-feedback-option"><kbd>→</kbd><strong>Средний</strong></article>
          <article className="difficulty-feedback-option"><kbd>↓</kbd><strong>Сложный</strong></article>
        </div>
        <div className="feedback-readiness" aria-label="Готовность выбора сложности">
          {responses.map(([teamId, response]) => <article key={teamId} className="feedback-team-status"><TeamDiamond teamId={teamId} /><strong>{TEAM_META[teamId].label}</strong><span>{response.difficultySelected ? "Сложность выбрана" : "Выбирает…"}</span></article>)}
        </div>
      </> : <>
        <p className="feedback-instruction">Стрелки — курсор <span>·</span> подтвердить <ConfirmGlyphs assignments={assignments} /></p>
        <div className="feedback-groups">
          <section className="feedback-group feedback-group--reaction" aria-labelledby="feedback-reaction-title"><h3 id="feedback-reaction-title">Такой вопрос подходит для игры?</h3><p>Выберите один вариант кнопкой подтверждения</p><div className="feedback-reactions" role="list">{feedbackItems.slice(0, 3).map(renderItem)}</div></section>
          <section className="feedback-group" aria-labelledby="feedback-tags-title"><h3 id="feedback-tags-title">Что можно улучшить?</h3><p>Можно отметить несколько пунктов кнопкой подтверждения</p><div className="feedback-tag-board" role="list">{feedbackItems.slice(3, 9).map((item, index) => renderItem(item, index + 3))}</div></section>
          <div className="feedback-complete" role="list">{renderItem(feedbackItems[9], 9)}</div>
        </div>
      </>}
      <p
        className={status === "error" ? "feedback-status feedback-status--error" : "feedback-status"}
        aria-live="polite"
      >
        {status === "pending"
          ? "Сохраняем фидбэк на сервере…"
          : status === "error"
            ? `${error ?? "Не удалось сохранить фидбэк"}. Нажмите направление ещё раз.`
            : feedback.stage === "difficulty" ? "Все команды выбирают сложность одновременно" : "Каждая команда завершает анкету на пункте «Готово»"}
      </p>
    </section>
  );
}

export function Standings({
  rows,
  title,
  footer
}: {
  readonly rows: readonly StandingRow[];
  readonly title: string;
  readonly footer: string;
}) {
  return (
    <section className="standings-stage">
      <div className="stage-label">Результаты</div>
      <h2>{title}</h2>
      <ol className="standings-table">
        {rows.map((row) => (
          <li key={row.teamId}>
            <span className="standing-rank">{row.rank}</span>
            <TeamDiamond teamId={row.teamId} />
            <strong>{TEAM_META[row.teamId].label}</strong>
            <span>✓ {row.correct}</span>
            <span>× {row.incorrect}</span>
            <span>Без ответа {row.noAnswer}</span>
            <b>{row.score}</b>
          </li>
        ))}
      </ol>
      <p className="control-help">{footer}</p>
    </section>
  );
}

export function PauseOverlay({
  reason,
  resume,
  restart,
  exit
}: {
  readonly reason: string;
  readonly resume: () => void;
  readonly restart: () => void;
  readonly exit: () => void;
}) {
  return (
    <div className="pause-backdrop" role="dialog" aria-modal="true" aria-labelledby="pause-title">
      <section className="pause-dialog">
        <div className="stage-label">Пауза</div>
        <h2 id="pause-title">{reason}</h2>
        <button type="button" onClick={resume}>Продолжить</button>
        <button type="button" onClick={restart}>Начать заново</button>
        <button type="button" onClick={exit}>Выйти в меню</button>
      </section>
    </div>
  );
}
