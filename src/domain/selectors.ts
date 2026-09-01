import type {
  AnswerPosition,
  DomainContext,
  MatchState,
  TeamId,
  TeamResolution
} from "./types";

export interface PublicTeamCard {
  readonly id: TeamId;
  readonly score: number;
  readonly reserveMs: number;
  readonly correct: number;
  readonly incorrect: number;
  readonly noAnswer: number;
  readonly hasAnswered: boolean;
  readonly result?: TeamResolution["result"];
  readonly answerPosition?: AnswerPosition | null;
}

export interface StandingRow {
  readonly rank: number;
  readonly teamId: TeamId;
  readonly score: number;
  readonly correct: number;
  readonly incorrect: number;
  readonly noAnswer: number;
}

export interface PublicQuestion {
  readonly id: string;
  readonly topicId: string;
  readonly prompt: string;
  readonly options: Readonly<Record<AnswerPosition, string>>;
  readonly explanation?: readonly string[];
  readonly source?: {
    readonly title: string;
    readonly url: string;
  };
  readonly correctPosition?: AnswerPosition;
}

export interface PublicMatchView {
  readonly phase: MatchState["phase"]["kind"];
  readonly paused: boolean;
  readonly teams: readonly PublicTeamCard[];
  readonly question?: PublicQuestion;
  readonly chooser?: TeamId;
  readonly topicCandidates?: readonly string[];
  readonly topicId?: string;
  readonly confirmationRemainingMs?: number;
  readonly vetoes?: Readonly<Partial<Record<TeamId, string>>>;
  readonly standings?: readonly StandingRow[];
  readonly winnerId?: TeamId;
  readonly feedback?: {
    readonly eventId: string;
    readonly questionId: string;
    readonly assignedDifficulty: "easy" | "medium" | "hard";
    readonly selectedDifficulty: "easy" | "medium" | "hard" | null;
  };
}

function attemptFlags(state: MatchState): Readonly<Record<TeamId, boolean>> {
  if (state.phase.kind !== "answering") return {} as Readonly<Record<TeamId, boolean>>;
  return Object.fromEntries(
    state.phase.round.attempts.map(({ teamId, status }) => [teamId, status === "answered"])
  ) as Readonly<Record<TeamId, boolean>>;
}

export function selectStandings(state: MatchState): readonly StandingRow[] {
  const winnerId = state.phase.kind === "finished" ? state.phase.winnerId : undefined;
  const sorted = [...state.teams].sort(
    (left, right) =>
      right.score - left.score ||
      (left.id === winnerId ? -1 : right.id === winnerId ? 1 : 0) ||
      state.config.teams.indexOf(left.id) - state.config.teams.indexOf(right.id)
  );
  const winningScore = winnerId
    ? state.teams.find(({ id }) => id === winnerId)?.score
    : undefined;
  return sorted.map((team) => {
    const previousWithSameScore = sorted.findIndex(({ score }) => score === team.score);
    return {
      rank:
        winnerId && team.id === winnerId
          ? 1
          : previousWithSameScore + 1 +
            (winnerId && team.score === winningScore ? 1 : 0),
      teamId: team.id,
      score: team.score,
      correct: team.correct,
      incorrect: team.incorrect,
      noAnswer: team.noAnswer
    };
  });
}

function selectQuestion(state: MatchState, context: DomainContext): PublicQuestion | undefined {
  if (
    state.phase.kind !== "answering" &&
    state.phase.kind !== "reveal" &&
    state.phase.kind !== "difficulty-feedback"
  ) return undefined;
  const round = state.phase.round;
  const question = context.getQuestion(round.questionId);
  if (!question) throw new Error(`Question ${round.questionId} is absent from catalog revision`);
  const textById = new Map(question.answers.map(({ id, text }) => [id, text]));
  const options = Object.fromEntries(
    (["up", "right", "down", "left"] as const).map((position, index) => {
      const answerId = round.answerOrder[index];
      const text = textById.get(answerId);
      if (text === undefined) throw new Error(`Answer ${answerId} is absent from question ${question.id}`);
      return [position, text];
    })
  ) as Readonly<Record<AnswerPosition, string>>;
  if (state.phase.kind === "reveal" || state.phase.kind === "difficulty-feedback") {
    return {
      id: question.id,
      topicId: question.topicId,
      prompt: question.prompt,
      options,
      explanation: question.explanation,
      source: question.source,
      correctPosition: round.correctPosition
    };
  }
  return { id: question.id, topicId: question.topicId, prompt: question.prompt, options };
}

export function selectPublicView(state: MatchState, context: DomainContext): PublicMatchView {
  const flags = attemptFlags(state);
  const resolutionByTeam =
    state.phase.kind === "reveal" || state.phase.kind === "difficulty-feedback"
      ? new Map(state.phase.resolutions.map((resolution) => [resolution.teamId, resolution]))
      : new Map<TeamId, TeamResolution>();
  const teams = state.teams.map((team): PublicTeamCard => {
    const resolution = resolutionByTeam.get(team.id);
    if (resolution) {
      return {
        ...team,
        hasAnswered: resolution.answer !== null,
        result: resolution.result,
        answerPosition: resolution.answer
      };
    }
    return { ...team, hasAnswered: flags[team.id] ?? false };
  });
  const base: PublicMatchView = {
    phase: state.phase.kind,
    paused: state.pause !== null,
    teams
  };

  if (state.phase.kind === "normal-topic") {
    return {
      ...base,
      chooser: state.phase.chooser,
      topicCandidates: state.phase.candidates
    };
  }
  if (state.phase.kind === "topic-confirmation") {
    return {
      ...base,
      topicId: state.phase.topicId,
      confirmationRemainingMs: state.phase.remainingMs
    };
  }
  if (state.phase.kind === "bonus-veto") {
    return {
      ...base,
      topicCandidates: state.phase.candidates,
      vetoes: state.phase.vetoes
    };
  }
  if (state.phase.kind === "answering" || state.phase.kind === "reveal") {
    return { ...base, question: selectQuestion(state, context) };
  }
  if (state.phase.kind === "difficulty-feedback") {
    return {
      ...base,
      feedback: {
        eventId: state.phase.eventId,
        questionId: state.phase.round.questionId,
        assignedDifficulty: state.phase.round.difficulty,
        selectedDifficulty: state.phase.selectedDifficulty
      }
    };
  }
  if (state.phase.kind === "standings") {
    return { ...base, standings: selectStandings(state) };
  }
  return {
    ...base,
    standings: selectStandings(state),
    winnerId: state.phase.winnerId
  };
}
