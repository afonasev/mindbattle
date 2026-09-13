import {
  activeTeams,
  bonusParticipants,
  createMatch,
  excludeNetworkPlayer,
  reduceFrame,
} from "../domain/match";
import { selectPublicView, selectStandings } from "../domain/selectors";
import type {
  DomainCommand,
  DomainContext,
  MatchState,
  TeamId,
} from "../domain/types";
import type { DifficultyFeedbackEventV3 } from "../feedback/types";
import type {
  CommandEnvelope,
  NetworkPlayer,
  NetworkSnapshot,
} from "./protocol";
export class RoomError extends Error {
  constructor(
    message: string,
    public status = 400,
  ) {
    super(message);
  }
}
interface Seat extends NetworkPlayer {
  token: string;
  generation: number;
  lastSeen: number;
}
export class NetworkRoom {
  readonly players: Seat[] = [];
  leaderId: TeamId | undefined;
  state: MatchState | null = null;
  epoch = 0;
  phaseRevision = 0;
  settings = {
    questionCount: 15 as 9 | 15 | 21,
    answerTimeMs: 20000 as 10000 | 20000 | 30000,
  };
  display = { connected: false, generation: 0, lastSeen: 0 };
  closed = false;
  feedbackError = "";
  private sequence = 0;
  private processed = new Map<string, Set<string>>();
  private feedbackPending = false;
  constructor(
    readonly code: string,
    readonly organizerToken: string,
    readonly context: DomainContext,
    readonly titles: Record<string, string>,
    private readonly secret: () => string,
    private readonly submitFeedback: (
      event: DifficultyFeedbackEventV3,
    ) => Promise<void>,
    private readonly changed: () => void = () => {},
  ) {}
  private actor(token: string) {
    if (this.closed) throw new RoomError("Комната закрыта", 410);
    if (token === this.organizerToken) return null;
    const seat = this.players.find((p) => p.token === token && !p.departed);
    if (!seat)
      throw new RoomError(
        "Нет доступа к комнате. Возможно, вы были исключены.",
        403,
      );
    return seat;
  }
  join(name: string, at: number): { id: TeamId; token: string } {
    if (this.closed) throw new RoomError("Комната закрыта", 410);
    if (this.state)
      throw new RoomError("Игра уже началась. Дождитесь новой партии.", 409);
    name = name.trim();
    if (!name || [...name].length > 24 || /[\p{Cc}\p{Cf}]/u.test(name))
      throw new RoomError("Имя должно содержать от 1 до 24 символов");
    if (
      this.players.some(
        (p) =>
          !p.departed &&
          p.name.toLocaleLowerCase() === name.toLocaleLowerCase(),
      )
    )
      throw new RoomError("Это имя уже занято");
    const id = Array.from(
      { length: 12 },
      (_, i) => `player-${i + 1}` as TeamId,
    ).find((id) => !this.players.some((p) => p.id === id));
    if (!id) throw new RoomError("В комнате уже 12 игроков", 409);
    const seat: Seat = {
      id,
      name,
      token: this.secret(),
      connected: false,
      departed: false,
      generation: 0,
      lastSeen: at,
    };
    this.players.push(seat);
    this.leaderId ??= id;
    this.changed();
    return { id, token: seat.token };
  }
  connect(token: string, at: number): number {
    const actor = this.actor(token);
    const target = actor ?? this.display;
    target.connected = true;
    target.lastSeen = at;
    target.generation++;
    this.changed();
    return target.generation;
  }
  heartbeat(token: string, generation: number, at: number) {
    const target = this.actor(token) ?? this.display;
    if (target.generation === generation) target.lastSeen = at;
  }
  disconnect(token: string, generation: number, at: number) {
    let actor: Seat | null;
    try {
      actor = this.actor(token);
    } catch {
      return;
    }
    const target = actor ?? this.display;
    if (target.generation !== generation) return;
    target.connected = false;
    this.freeze(at);
    this.changed();
  }
  tick(at: number) {
    for (const seat of this.players)
      if (!seat.departed && seat.connected && at - seat.lastSeen > 8000)
        this.disconnect(seat.token, seat.generation, at);
    if (this.display.connected && at - this.display.lastSeen > 8000)
      this.disconnect(this.organizerToken, this.display.generation, at);
    if (this.state) this.reduce([], at);
  }
  private freeze(at: number) {
    if (!this.state || this.state.phase.kind === "finished") return;
    this.reduce([], at);
    if (!this.state.pause) {
      this.state = { ...this.state, pause: { reasons: [{ kind: "manual" }] } };
      this.phaseRevision++;
    }
  }
  private reduce(commands: DomainCommand[], at: number) {
    if (!this.state) return;
    const before = this.state.phase.kind;
    const feedbackStage =
      this.state.phase.kind === "difficulty-feedback"
        ? this.state.phase.stage
        : null;
    const q = this.state.mainQuestionIndex;
    const paused = !!this.state.pause;
    this.state = reduceFrame(
      this.state,
      { atMs: at, sequence: ++this.sequence, commands },
      this.context,
    );
    if (
      this.state.phase.kind !== before ||
      (this.state.phase.kind === "difficulty-feedback" &&
        this.state.phase.stage !== feedbackStage) ||
      this.state.mainQuestionIndex !== q ||
      !!this.state.pause !== paused
    )
      this.phaseRevision++;
  }
  command(token: string, envelope: CommandEnvelope, at: number) {
    const actor = this.actor(token);
    if (
      !envelope ||
      typeof envelope.commandId !== "string" ||
      envelope.commandId.length > 100 ||
      !envelope.commandId ||
      !envelope.action
    )
      throw new RoomError("Некорректная команда");
    const seen = this.processed.get(token) ?? new Set<string>();
    if (seen.has(envelope.commandId)) return;
    this.tick(at);
    if (
      envelope.epoch !== this.epoch ||
      envelope.phaseRevision !== this.phaseRevision
    )
      throw new RoomError("Экран уже изменился. Повторите действие.", 409);
    const action = envelope.action;
    const leader = actor?.id === this.leaderId;
    const requireLeader = () => {
      if (!actor || !leader)
        throw new RoomError("Это действие доступно ведущему", 403);
    };
    const requireDisplay = () => {
      if (actor)
        throw new RoomError("Это действие доступно общему экрану", 403);
    };
    const requireLobby = () => {
      if (this.state) throw new RoomError("Доступно только в лобби", 409);
    };
    if (action.type === "settings") {
      requireDisplay();
      requireLobby();
      if (
        ![9, 15, 21].includes(action.questionCount) ||
        ![10000, 20000, 30000].includes(action.answerTimeMs)
      )
        throw new RoomError("Неверные настройки");
      this.settings = {
        questionCount: action.questionCount as 9 | 15 | 21,
        answerTimeMs: action.answerTimeMs as 10000 | 20000 | 30000,
      };
    } else if (action.type === "leader") {
      requireDisplay();
      requireLobby();
      const seat = this.players.find(
        (p) => p.id === action.playerId && !p.departed,
      );
      if (!seat) throw new RoomError("Игрок не найден");
      this.leaderId = seat.id;
    } else if (action.type === "remove" || action.type === "exclude") {
      requireDisplay();
      if (action.type === "remove") requireLobby();
      const seat = this.players.find(
        (p) => p.id === action.playerId && !p.departed,
      );
      if (!seat) throw new RoomError("Игрок не найден");
      if (this.state && seat.connected)
        throw new RoomError("Игрок уже подключился", 409);
      if (this.state) {
        this.state = excludeNetworkPlayer(this.state, seat.id, this.context);
        seat.departed = true;
        this.phaseRevision++;
      } else this.players.splice(this.players.indexOf(seat), 1);
      if (this.leaderId === seat.id)
        this.leaderId = this.players.find((p) => !p.departed)?.id;
      if (
        this.state &&
        !this.players.some((p) => !p.departed && !p.connected) &&
        this.display.connected &&
        this.state.phase.kind !== "finished"
      )
        this.reduce([{ type: "resume" }], at);
    } else if (action.type === "start") {
      requireDisplay();
      requireLobby();
      if (
        !this.display.connected ||
        this.players.length < 2 ||
        this.players.some((p) => !p.connected)
      )
        throw new RoomError(
          "Для старта нужны общий экран и минимум два подключённых игрока",
          409,
        );
      const seed = this.secret();
      this.epoch++;
      this.phaseRevision++;
      this.state = createMatch(
        {
          profile: "network-v1",
          ...this.settings,
          teams: this.players.map((p) => p.id),
        },
        seed,
        at,
        this.context,
        `network:${this.code}:${seed}`,
      );
    } else if (action.type === "replay") {
      requireLeader();
      if (!this.state) throw new RoomError("Партия ещё не началась");
      for (let i = this.players.length - 1; i >= 0; i--)
        if (this.players[i].departed) this.players.splice(i, 1);
      this.state = null;
      this.epoch++;
      this.phaseRevision++;
      this.feedbackError = "";
    } else if (action.type === "close") {
      if (this.state) requireLeader();
      else requireDisplay();
      this.closed = true;
    } else if (action.type === "pause") {
      requireLeader();
      this.freeze(at);
    } else if (action.type === "resume") {
      requireLeader();
      if (
        !this.display.connected ||
        this.players.some((p) => !p.departed && !p.connected)
      )
        throw new RoomError(
          "Сначала дождитесь подключения или исключите отсутствующих",
          409,
        );
      this.reduce([{ type: "resume" }], at);
    } else {
      if (!this.state || this.state.pause)
        throw new RoomError("Игра на паузе или ещё не началась", 409);
      if (!actor)
        throw new RoomError("Управление игрой доступно с телефона", 403);
      let commands: DomainCommand[] = [];
      const phase = this.state.phase;
      if (action.type === "answer") {
        if (!["up", "right", "down", "left"].includes(action.position))
          throw new RoomError("Неверный ответ");
        if (
          phase.kind !== "answering" ||
          !phase.round.attempts.some(
            (a) =>
              a.teamId === actor.id &&
              (a.status === "open" || a.status === "answered"),
          )
        )
          throw new RoomError("Ответ сейчас недоступен", 409);
        commands = [
          { type: "answer", teamId: actor.id, position: action.position },
        ];
      } else if (action.type === "topic") {
        if (phase.kind !== "normal-topic" || phase.chooser !== actor.id)
          throw new RoomError("Сейчас выбирает другой игрок", 403);
        const index = phase.candidates.indexOf(action.topicId);
        if (index < 0) throw new RoomError("Тема недоступна");
        while (
          this.state.phase.kind === "normal-topic" &&
          this.state.phase.cursor !== index
        )
          this.reduce([{ type: "move-topic", teamId: actor.id, delta: 1 }], at);
        commands = [{ type: "confirm-topic", teamId: actor.id }];
      } else if (action.type === "veto" || action.type === "clear-veto") {
        if (
          phase.kind !== "bonus-veto" ||
          !bonusParticipants(this.state).includes(actor.id)
        )
          throw new RoomError("Вы не участвуете в этих запретах", 403);
        if (
          action.type === "veto" &&
          !phase.candidates.includes(action.topicId)
        )
          throw new RoomError("Тема недоступна");
        if (
          action.type === "veto" &&
          Object.entries(phase.vetoes).some(
            ([playerId, topicId]) =>
              playerId !== actor.id && topicId === action.topicId,
          )
        )
          throw new RoomError("Эту тему уже исключил другой игрок", 409);
        commands = [
          action.type === "veto"
            ? { type: "set-veto", teamId: actor.id, topicId: action.topicId }
            : { type: "clear-veto", teamId: actor.id },
        ];
      } else {
        requireLeader();
        if (action.type === "continue")
          commands = [{ type: "continue", teamId: actor.id }];
        else if (action.type === "retry-feedback") {
          this.feedbackError = "";
        } else {
          if (phase.kind !== "difficulty-feedback")
            throw new RoomError("Оценка вопроса сейчас недоступна", 409);
          if (
            (action.type === "feedback-choice" &&
              (phase.stage !== "choice" ||
                typeof action.complaint !== "boolean")) ||
            (["feedback-note", "feedback-reason", "feedback-submit"].includes(
              action.type,
            ) &&
              phase.stage !== "reasons")
          ) {
            throw new RoomError("Экран жалобы уже изменился", 409);
          }
          if (action.type === "feedback-note") {
            if (typeof action.note !== "string")
              throw new RoomError("Неверная заметка");
            commands = [{ type: "set-feedback-note", note: action.note }];
          } else {
            const index =
              action.type === "feedback-choice"
                ? action.complaint
                  ? 0
                  : 1
                : action.type === "feedback-reason"
                  ? action.index
                  : action.type === "feedback-submit"
                    ? 7
                    : -1;
            if (
              !Number.isInteger(index) ||
              index < 0 ||
              index > (phase.stage === "choice" ? 1 : 7) ||
              phase.stage === "done"
            )
              throw new RoomError("Неверное действие жалобы");
            while (
              this.state.phase.kind === "difficulty-feedback" &&
              this.state.phase.cursor !== index
            )
              this.reduce(
                [{ type: "feedback-direction", direction: "east" }],
                at,
              );
            if (
              action.type === "feedback-submit" &&
              action.note !== undefined
            ) {
              if (typeof action.note !== "string")
                throw new RoomError("Неверная заметка");
              commands = [
                { type: "set-feedback-note", note: action.note },
                { type: "feedback-confirm" },
              ];
            } else commands = [{ type: "feedback-confirm" }];
          }
        }
      }
      this.reduce(commands, at);
    }
    seen.add(envelope.commandId);
    if (seen.size > 512) seen.delete(seen.values().next().value!);
    this.processed.set(token, seen);
    this.changed();
    void this.flushFeedback();
  }
  async flushFeedback() {
    const state = this.state;
    if (
      !state ||
      state.phase.kind !== "difficulty-feedback" ||
      state.phase.stage !== "done" ||
      this.feedbackPending ||
      this.feedbackError
    )
      return;
    const phase = state.phase;
    const epoch = this.epoch;
    this.feedbackPending = true;
    try {
      await this.submitFeedback({
        schemaVersion: 3,
        eventId: phase.eventId,
        matchId: state.matchId,
        catalogRevision: state.catalogRevision,
        questionId: phase.round.questionId,
        assignedDifficulty: phase.round.difficulty,
        hasComplaint: phase.hasComplaint === true,
        complaintReasons: phase.complaintReasons,
        ...(phase.complaintNote.trim()
          ? { complaintNote: phase.complaintNote.trim() }
          : {}),
      });
      if (
        this.epoch === epoch &&
        this.state?.phase.kind === "difficulty-feedback" &&
        this.state.phase.eventId === phase.eventId
      )
        this.reduce(
          [{ type: "confirm-difficulty-feedback", eventId: phase.eventId }],
          this.state.lastFrameAtMs,
        );
    } catch {
      if (this.epoch === epoch)
        this.feedbackError = "Не удалось сохранить отзыв. Повторите отправку.";
    } finally {
      this.feedbackPending = false;
      this.changed();
    }
  }
  snapshot(token: string, at: number): NetworkSnapshot {
    const actor = this.actor(token);
    const publicSeat = (p: Seat): NetworkPlayer => ({
      id: p.id,
      name: p.name,
      connected: p.connected,
      departed: p.departed,
    });
    const base: NetworkSnapshot = {
      code: this.code,
      epoch: this.epoch,
      phaseRevision: this.phaseRevision,
      serverTime: at,
      role: actor ? "player" : "display",
      selfId: actor?.id,
      isLeader: actor?.id === this.leaderId,
      leaderName: this.players.find((p) => p.id === this.leaderId)?.name ?? "",
      settings: this.settings,
      players: actor
        ? this.state
          ? [publicSeat(actor)]
          : this.players.filter((p) => !p.departed).map(publicSeat)
        : this.players.map(publicSeat),
      displayConnected: this.display.connected,
      disconnected: actor
        ? []
        : this.players
            .filter((p) => !p.departed && !p.connected)
            .map(publicSeat),
      phase: this.state?.phase.kind ?? "lobby",
      paused: !!this.state?.pause,
      titles: {},
      canChoose: false,
      canVeto: false,
      canAnswer: false,
    };
    if (!this.state) return base;
    const state = this.state;
    const view = selectPublicView(state, this.context);
    const phase = state.phase;
    const cards = view.teams
      .filter((card) => !actor || card.id === actor.id)
      .map((card) => {
        const seat = this.players.find((p) => p.id === card.id)!;
        const attempt =
          phase.kind === "answering"
            ? phase.round.attempts.find((a) => a.teamId === card.id)
            : null;
        const remainingMs =
          phase.kind === "answering" && attempt?.status === "open"
            ? phase.baseRemainingMs > 0
              ? phase.baseRemainingMs
              : card.reserveMs
            : undefined;
        return {
          ...card,
          name: seat.name,
          departed: seat.departed,
          remainingMs,
        };
      });
    const visibleStandings = [
      ...selectStandings({
        ...state,
        teams: state.teams.filter(
          (t) => !state.departedTeamIds?.includes(t.id),
        ),
      }),
      ...selectStandings(state)
        .filter((row) => state.departedTeamIds?.includes(row.teamId))
        .map((row) => ({ ...row, rank: 0 })),
    ];
    const scoreboard = visibleStandings.map((row) => ({
      teamId: row.teamId,
      name: this.players.find((player) => player.id === row.teamId)?.name ?? "",
      rank: row.rank,
      score: row.score,
      departed: !!this.players.find((player) => player.id === row.teamId)?.departed,
    }));
    const standings = view.standings ? visibleStandings : undefined;
    const personalView = {
      ...view,
      standings,
      teams: cards,
      ...(actor
        ? {
            standings: undefined,
            winnerId: undefined,
            vetoes: undefined,
            chooser: undefined,
            feedback: base.isLeader ? view.feedback : undefined,
          }
        : {}),
    };
    if (actor && personalView.question?.wrongAnswerNotes) {
      const own = cards[0]?.answerPosition;
      personalView.question = {
        ...personalView.question,
        wrongAnswerNotes: personalView.question.wrongAnswerNotes.filter(
          (n) => n.position === own,
        ),
      };
    }
    const topicIds = [
      ...(view.topicCandidates ?? []),
      ...(view.topicId ? [view.topicId] : []),
      ...(view.question ? [view.question.topicId] : []),
    ];
    return {
      ...base,
      scoreboard: actor ? scoreboard : undefined,
      view: personalView,
      titles: Object.fromEntries(
        topicIds.map((id) => [id, this.titles[id] ?? id]),
      ),
      canChoose: phase.kind === "normal-topic" && phase.chooser === actor?.id,
      canVeto:
        phase.kind === "bonus-veto" &&
        !!actor &&
        bonusParticipants(state).includes(actor.id),
      canAnswer:
        phase.kind === "answering" &&
        phase.round.attempts.some(
          (a) =>
            a.teamId === actor?.id &&
            (a.status === "open" || a.status === "answered"),
        ),
      ownAnswer:
        actor && phase.kind === "answering"
          ? phase.round.attempts.find((a) => a.teamId === actor.id)?.answer
          : undefined,
      ownVeto:
        actor && phase.kind === "bonus-veto"
          ? phase.vetoes[actor.id]
          : undefined,
      vetoes:
        actor && phase.kind === "bonus-veto"
          ? Object.entries(phase.vetoes).flatMap(([playerId, topicId]) =>
              topicId
                ? [{
                    playerId: playerId as TeamId,
                    name:
                      this.players.find((player) => player.id === playerId)
                        ?.name ?? "Игрок",
                    topicId,
                  }]
                : [],
            )
          : undefined,
      vetoParticipants:
        !actor && phase.kind === "bonus-veto"
          ? bonusParticipants(state).map(
              (id) => this.players.find((p) => p.id === id)!.name,
            )
          : undefined,
      questionNumber: state.mainQuestionIndex + 1,
      tieBreakNumber: state.tieBreak?.questionNumber,
      spectating: !!actor && !!state.tieBreak && !state.tieBreak.contenders.includes(actor.id),
      difficulty: "round" in phase ? phase.round.difficulty : undefined,
      endReason: state.endReason,
      feedbackError: base.isLeader ? this.feedbackError : undefined,
    };
  }
}
