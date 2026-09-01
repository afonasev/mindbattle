export type Difficulty = "easy" | "medium" | "hard";

export interface QuestionSource {
  readonly title: string;
  readonly url: string;
  readonly verifiedAt: string;
}

export interface Question {
  readonly id: string;
  readonly difficulty: Difficulty;
  readonly prompt: string;
  readonly answers: readonly [string, string, string, string];
  readonly correctIndex: 0 | 1 | 2 | 3;
  readonly explanation: string;
  readonly source: QuestionSource;
}

export interface TopicPack {
  readonly id: string;
  readonly title: string;
  readonly questions: readonly Question[];
}

export interface ContentCatalog {
  readonly revision: string;
  readonly topics: readonly TopicPack[];
}

export interface ReviewEntry {
  readonly topicId: string;
  readonly author: string;
  readonly reviewer: string;
  readonly status: "approved";
  readonly contentSha256: string;
  readonly reviewedAt: string;
  readonly checkedQuestions: 30;
  readonly criticalFindingsOpen: 0;
}
