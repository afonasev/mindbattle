import type { PublicMatchView, PublicTeamCard } from "../domain/selectors";
import type { AnswerPosition, MatchConfig, TeamId } from "../domain/types";
export interface Credential {
  code: string;
  token: string;
  role: "display" | "player";
}
export interface NetworkPlayer {
  id: TeamId;
  name: string;
  connected: boolean;
  departed: boolean;
}
export type NetworkCard = PublicTeamCard & {
  name: string;
  departed: boolean;
  remainingMs?: number;
};
export interface NetworkScoreRow {
  teamId: TeamId;
  name: string;
  rank: number;
  score: number;
  departed: boolean;
}
export interface NetworkVeto {
  playerId: TeamId;
  name: string;
  topicId: string;
}
export interface NetworkSnapshot {
  code: string;
  epoch: number;
  phaseRevision: number;
  serverTime: number;
  role: "display" | "player";
  selfId?: TeamId;
  isLeader: boolean;
  leaderName: string;
  settings: Pick<MatchConfig, "questionCount" | "answerTimeMs">;
  players: NetworkPlayer[];
  displayConnected: boolean;
  disconnected: NetworkPlayer[];
  phase: "lobby" | PublicMatchView["phase"];
  paused: boolean;
  view?: Omit<PublicMatchView, "teams"> & { teams: NetworkCard[] };
  titles: Record<string, string>;
  canChoose: boolean;
  chooserName?: string;
  canVeto: boolean;
  canAnswer: boolean;
  ownAnswer?: AnswerPosition | null;
  ownVeto?: string;
  vetoParticipants?: string[];
  questionNumber?: number;
  tieBreakNumber?: number;
  spectating?: boolean;
  difficulty?: string;
  endReason?: string;
  feedbackError?: string;
  scoreboard?: readonly NetworkScoreRow[];
  vetoes?: readonly NetworkVeto[];
}
export type NetworkAction =
  | { type: "settings"; questionCount: number; answerTimeMs: number }
  | { type: "leader" | "remove" | "exclude"; playerId: string }
  | {
      type:
        | "start"
        | "replay"
        | "close"
        | "pause"
        | "resume"
        | "continue"
        | "clear-veto"
        | "retry-feedback"
        | "skip-feedback";
    }
  | { type: "topic" | "veto"; topicId: string }
  | { type: "answer"; position: AnswerPosition }
  | { type: "feedback-choice"; complaint: boolean }
  | { type: "feedback-reason"; index: number }
  | { type: "feedback-note"; note: string }
  | { type: "feedback-submit"; note?: string };
export interface CommandEnvelope {
  commandId: string;
  epoch: number;
  phaseRevision: number;
  action: NetworkAction;
}
