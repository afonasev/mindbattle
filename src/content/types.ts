export type Difficulty = "easy" | "medium" | "hard";

export interface QuestionSource {
  readonly title: string;
  readonly url: string;
  readonly verifiedAt: string;
}

export interface QuestionAnswer {
  readonly text: string;
  readonly note: string;
}

export type QuestionAnswerInput = string | QuestionAnswer;

export interface Question {
  readonly id: string;
  readonly difficulty: Difficulty;
  readonly prompt: string;
  readonly answers: readonly [
    QuestionAnswerInput,
    QuestionAnswerInput,
    QuestionAnswerInput,
    QuestionAnswerInput
  ];
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
  readonly checkedQuestions: number;
  readonly criticalFindingsOpen: 0;
  readonly evidence: {
    readonly questionIdsSha256: string;
    readonly checks: {
      readonly factualCorrectness: number;
      readonly correctIndex: number;
      readonly difficulty: number;
      readonly distractors: number;
      readonly answerNotes: number;
      readonly grammar: number;
      readonly explanation: number;
      readonly sourceRelevance: number;
      readonly duplicates: number;
    };
    readonly reviewedPackageIds: readonly string[];
    readonly resolvedFindings: readonly {
      readonly questionId: string;
      readonly issue: string;
      readonly resolution: string;
    }[];
  };
}
