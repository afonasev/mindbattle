import type { TeamControlAssignment } from "../adapters";
import { GAMEPAD_GLYPHS, KEYBOARD_GLYPHS } from "../adapters";
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

export function TeamCards({
  view,
  activeTeamIds
}: {
  readonly view: PublicMatchView;
  readonly activeTeamIds: readonly TeamId[];
}) {
  return (
    <ul className="game-team-strip" aria-label="Состояние команд">
      {view.teams
        .filter((team) => activeTeamIds.includes(team.id))
        .map((team) => (
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
          </li>
        ))}
    </ul>
  );
}

export function TopicSelection({
  view,
  titleById,
  assignment,
  choose
}: {
  readonly view: PublicMatchView;
  readonly titleById: Readonly<Record<string, string>>;
  readonly assignment: TeamControlAssignment | undefined;
  readonly choose: (topicId: string) => void;
}) {
  return (
    <section className="topic-stage" aria-labelledby="topic-title">
      <div className="stage-label">Выбор темы</div>
      <h2 id="topic-title">
        <TeamDiamond teamId={view.chooser!} /> {TEAM_META[view.chooser!].label} команда выбирает
      </h2>
      <div className="topic-cards topic-cards--three">
        {view.topicCandidates?.map((topicId, index) => (
          <button key={topicId} type="button" onClick={() => choose(topicId)}>
            <span className="topic-key">
              {controlGlyph(assignment, (["left", "up", "right"] as const)[index])}
            </span>
            {titleById[topicId] ?? topicId}
          </button>
        ))}
      </div>
      <p className="control-help">A / W / D · ← / ↑ / → · левая / верхняя / правая кнопка</p>
    </section>
  );
}

export function BonusVeto({
  state,
  titleById
}: {
  readonly state: MatchState;
  readonly titleById: Readonly<Record<string, string>>;
}) {
  if (state.phase.kind !== "bonus-veto") return null;
  return (
    <section className="topic-stage bonus-stage" aria-labelledby="bonus-title">
      <div className="stage-label stage-label--bonus">Бонусный вопрос · x2</div>
      <h2 id="bonus-title">Запретите по одной разной теме</h2>
      <div className="topic-cards topic-cards--bonus">
        {state.phase.candidates.map((topicId, index) => {
          const vetoes = state.config.teams.filter(
            (teamId) => state.phase.kind === "bonus-veto" && state.phase.vetoes[teamId] === topicId
          );
          const cursors = state.config.teams.filter(
            (teamId) => state.phase.kind === "bonus-veto" && state.phase.cursors[teamId] === index
          );
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
      <p className="control-help">←/→ курсор · ↓ запретить или заменить · ↑ снять запрет · D-pad / WASD / стрелки</p>
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
  const baseRemainingMs = state.phase.kind === "answering" ? state.phase.baseRemainingMs : 0;
  return (
    <section className={reveal ? "question-stage question-stage--reveal" : "question-stage"}>
      <header className="question-header">
        <span>{titleById[question.topicId] ?? question.topicId}</span>
        <strong>
          {state.phase.round.mode === "tie-break"
            ? `Финал ${state.tieBreak?.questionNumber ?? 1}`
            : `Вопрос ${state.mainQuestionIndex + 1} / ${state.config.questionCount}`}
        </strong>
        <span className={baseRemainingMs <= 5_000 && !reveal ? "timer timer--danger" : "timer"}>
          {reveal ? "Ответ" : Math.ceil(baseRemainingMs / 1000)}
        </span>
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
          <span>Отпустите кнопки, затем нажмите любую назначенную клавишу</span>
        </aside>
      )}
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
