import { describe, expect, it } from "vitest";
import { CatalogDomainContext } from "../../src/application/contentContext";
import { chooseTopicCandidates, EMPTY_QUESTION_HISTORY, seedRandom, TOPIC_DOMAIN_BY_ID, topicGroupLimit, type TopicPack } from "../../src/content";
import { catalog } from "../../src/content/catalog";
import { createMatch, reduceFrame } from "../../src/domain/match";
import { createSoloRun } from "../../src/domain/solo";
import { deserializeMatch, serializeMatch } from "../../src/domain/serialization";
import type { DomainCommand, MatchState, TopicSelectionRequest } from "../../src/domain/types";

function topic(id: string): TopicPack {
  return { id, title: id, questions: (["easy", "medium", "hard"] as const).flatMap(difficulty =>
    Array.from({ length: 8 }, (_, index) => ({ id: `${id}-${difficulty}-${index}`, difficulty, prompt: "Вопрос",
      answers: ["A", "B", "C", "D"] as const, correctIndex: 0 as const, explanation: "Справка.",
      source: { title: "Источник", url: "https://example.com", verifiedAt: "2026-09-28" } }))) };
}
const packs = ["history-russia", "world-geography", "classical-music"].map(topic);
function context() { return new CatalogDomainContext({ revision: "groups-fixture", topics: packs }, EMPTY_QUESTION_HISTORY); }
function request(overrides: Partial<TopicSelectionRequest> = {}): TopicSelectionRequest {
  return { kind: "normal", count: 3, difficulty: "easy", excludedTopicIds: [], excludedQuestionIds: [], shownTopicCounts: {}, random: seedRandom("groups"), ...overrides };
}
function frame(state: MatchState, ctx: CatalogDomainContext, commands: readonly DomainCommand[]) {
  return reduceFrame(state, { atMs: state.lastFrameAtMs, sequence: 1, commands }, ctx);
}

describe("topic-diversity-v1", () => {
  it("validates the named caps and counts", () => {
    expect(topicGroupLimit("normal", 3)).toBe(1);
    expect(topicGroupLimit("final", 5)).toBe(1);
    expect(topicGroupLimit("bonus", 3)).toBe(1);
    expect(topicGroupLimit("bonus", 4)).toBe(2);
    expect(topicGroupLimit("bonus", 5)).toBe(2);
    expect(() => topicGroupLimit("normal", 4)).toThrow();
    expect(() => topicGroupLimit("toString" as never, 3)).toThrow();
    expect(() => topicGroupLimit("bonus", 6)).toThrow();
    expect(() => topicGroupLimit("final", 3.5)).toThrow();
  });

  it("never offers multiple country histories or music topics in a normal set", () => {
    for (let seed = 0; seed < 40; seed += 1) {
      const ctx = new CatalogDomainContext(catalog, EMPTY_QUESTION_HISTORY);
      for (const kind of ["normal", "bonus", "final"] as const) {
        for (const count of kind === "normal" ? [3] : [3, 4, 5]) {
          const selection = ctx.selectTopics(request({ kind, count, random: seedRandom(String(seed)) }));
          expect(new Set(selection.topicIds.map(id => TOPIC_DOMAIN_BY_ID[id])).size).toBe(count);
        }
      }
    }
  });

  it("allows exactly two per group in a large bonus and never three", () => {
    const fixture = ["h0", "h1", "h2", "m0", "m1", "s0"].map(topic);
    const domain = (id: string) => id[0];
    const history = { selected: [], shownCounts: {} };
    const four = chooseTopicCandidates(fixture.slice(0, 5), 4, history, seedRandom("bonus"), domain, "bonus");
    expect(four.topicIds.filter(id => id[0] === "h")).toHaveLength(2);
    expect(four.topicIds.filter(id => id[0] === "m")).toHaveLength(2);
    const five = chooseTopicCandidates(fixture, 5, history, seedRandom("bonus"), domain, "bonus");
    expect(new Set(five.topicIds.map(domain)).size).toBe(3);
    expect(five.topicIds.filter(id => id[0] === "h")).toHaveLength(2);
    expect(() => chooseTopicCandidates(fixture.slice(0, 5), 5, history, seedRandom("bonus"), domain, "bonus")).toThrow(/Недостаточно/);
    expect(() => chooseTopicCandidates(fixture, 4, history, seedRandom("bonus"), domain, "final")).toThrow(/Недостаточно/);
  });

  it("matches an independent exhaustive oracle for caps, minimum reuse and maximum diversity", () => {
    const fixture = ["h0", "h1", "h2", "m0", "m1", "s0", "g0", "g1", "f0"].map(topic);
    const domain = (id: string) => id[0];
    for (let seed = 0; seed < 24; seed += 1) {
      const selected = fixture.filter((_, index) => (seed + index) % 3 !== 0).map(t => t.id);
      for (const kind of ["bonus", "final"] as const) for (const count of [3, 4, 5]) {
        const cap = kind === "bonus" && count > 3 ? 2 : 1;
        let best = [Infinity, Infinity];
        for (let mask = 0; mask < 1 << fixture.length; mask += 1) {
          const ids = fixture.filter((_, index) => mask & 1 << index).map(t => t.id);
          if (ids.length !== count || ids.some(id => ids.filter(other => domain(other) === domain(id)).length > cap)) continue;
          const score = [ids.filter(id => selected.includes(id)).length, -new Set(ids.map(domain)).size];
          if (score[0] < best[0] || score[0] === best[0] && score[1] < best[1]) best = score;
        }
        const input = { selected, shownCounts: { h0: 15, m1: 10 } };
        const result = chooseTopicCandidates(fixture, count, input, seedRandom(String(seed)), domain, kind);
        expect([result.reusedTopicIds.length, -new Set(result.topicIds.map(domain)).size]).toEqual(best);
        expect(chooseTopicCandidates(fixture, count, input, seedRandom(String(seed)), domain, kind)).toEqual(result);
      }
    }
  });

  it("returns selected topics only when needed and uses a new question", () => {
    const ctx = context();
    const excluded = packs.map(t => `${t.id}-easy-0`);
    const selection = ctx.selectTopics(request({ excludedTopicIds: packs.slice(1).map(t => t.id), excludedQuestionIds: excluded }));
    expect(selection.reusedTopicIds).toHaveLength(2);
    const question = ctx.selectQuestion({ topicId: selection.reusedTopicIds![0], difficulty: "easy", excludedQuestionIds: excluded, random: selection.random });
    expect(excluded).not.toContain(question.question.id);
    const exhausted = [...excluded, ...packs[1].questions.filter(q => q.difficulty === "easy").map(q => q.id)];
    expect(() => ctx.selectTopics(request({ excludedQuestionIds: exhausted }))).toThrow(/Недостаточно/);
  });

  it("avoids reuse even if a previously selected topic has a lower show penalty", () => {
    const fixture = ["h0", "h1", "m0", "s0"].map(topic);
    const result = chooseTopicCandidates(fixture, 3, { selected: ["h0"], shownCounts: { h1: 100 } }, seedRandom("7"), id => id[0]);
    expect(result.topicIds).toContain("h1");
    expect(result.reusedTopicIds).toEqual([]);
  });

  it.each(["classic-v1", "network-v1"] as const)("keeps question history and snapshots across returned topics in %s", profile => {
    const ctx = context();
    let state = createMatch({ profile, teams: profile === "classic-v1" ? ["green", "blue"] : ["player-1", "player-2"], questionCount: 9, answerTimeMs: 10000, collectQuestionFeedback: false }, "reuse-match", 0, ctx);
    const observed = new Set<string>();
    let finals = 0;
    for (let step = 0; step < 100; step += 1) {
      expect(deserializeMatch(serializeMatch(state), ctx.catalogRevision)).toEqual(state);
      const phase = state.phase;
      if (phase.kind === "normal-topic") {
        expect(new Set(phase.candidates.map(id => TOPIC_DOMAIN_BY_ID[id])).size).toBe(3);
        state = frame(state, ctx, [{ type: "confirm-topic", teamId: phase.chooser }]);
      } else if (phase.kind === "bonus-veto" || phase.kind === "final-veto") {
        expect(new Set(phase.candidates.map(id => TOPIC_DOMAIN_BY_ID[id])).size).toBe(3);
        if (phase.kind === "final-veto") { finals += 1; break; }
        state = frame(state, ctx, state.config.teams.map((teamId, index) => ({ type: "set-veto", teamId, topicId: phase.candidates[index] })));
      } else if (phase.kind === "topic-confirmation") {
        state = frame(state, ctx, [{ type: "continue", teamId: state.config.teams[0] }]);
      } else if (phase.kind === "answering") {
        expect(observed.has(phase.round.questionId)).toBe(false); observed.add(phase.round.questionId);
        const question = ctx.getQuestion(phase.round.questionId)!;
        const position = (["up", "right", "down", "left"] as const)[phase.round.answerOrder.indexOf(question.correctAnswerId)];
        state = frame(state, ctx, state.config.teams.map(teamId => ({ type: "answer", teamId, position })));
      } else if (phase.kind === "reveal" || phase.kind === "standings") {
        if (observed.size === 9 && profile === "network-v1") break;
        state = frame(state, ctx, [{ type: "continue", teamId: state.config.teams[0] }]);
      } else throw new Error(`Unexpected phase ${phase.kind}`);
    }
    expect(observed.size).toBe(9);
    expect(new Set(state.selectedTopicIds).size).toBe(state.selectedTopicIds.length);
    if (profile === "classic-v1") expect(finals).toBe(1);
  });

  it("rejects an invalid returned-topic declaration at the game boundary", () => {
    class InvalidContext extends CatalogDomainContext {
      override selectTopics(input: TopicSelectionRequest) {
        return { ...super.selectTopics(input), reusedTopicIds: ["history-russia"] };
      }
    }
    const ctx = new InvalidContext({ revision: "groups-fixture", topics: packs }, EMPTY_QUESTION_HISTORY);
    expect(() => createMatch({ profile: "classic-v1", teams: ["green", "blue"], questionCount: 9, answerTimeMs: 10000 }, "invalid-reuse", 0, ctx))
      .toThrow(/Invalid reused topic declaration/);
  });

  it("uses the same distinct groups in a seeded solo choice", () => {
    const first = createSoloRun({ profile: "solo-endless-v1", collectQuestionFeedback: false }, "solo-groups", 0, context());
    const second = createSoloRun({ profile: "solo-endless-v1", collectQuestionFeedback: false }, "solo-groups", 0, context());
    expect(first).toEqual(second);
    expect(first.phase.kind).toBe("topic");
    if (first.phase.kind === "topic") expect(new Set(first.phase.candidates.map(id => TOPIC_DOMAIN_BY_ID[id])).size).toBe(3);
  });
});
