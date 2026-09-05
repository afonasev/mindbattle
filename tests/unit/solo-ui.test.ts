import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import { SoloScreen } from "../../src/ui/soloUi";
import type { SoloRecord } from "../../src/adapters/storage";
import type { SoloState } from "../../src/domain/solo";

function record(index: number): SoloRecord {
  return { id: `top-${index}`, name: `Игрок ${index}`, score: 1_200 - index * 100, savedAt: `2026-09-05T${String(index).padStart(2, "0")}:00:00.000Z` };
}

describe("SoloScreen results", () => {
  it("keeps the current result visible with its full-table rank outside top-10", () => {
    const records = [...Array.from({ length: 11 }, (_, index) => record(index)), { id: "current", name: "Текущий", score: -100, savedAt: "2026-09-05T12:00:00.000Z" }];
    const html = renderToStaticMarkup(createElement(SoloScreen, {
      state: { phase: { kind: "finished" }, score: -100 } as SoloState,
      question: undefined,
      titleById: {},
      records,
      savedRecordId: "current",
      inputKind: "pointer" as const,
      command: () => undefined,
      finish: () => undefined,
      exit: () => undefined
    }));
    expect(html).toContain("Ваше место: 12");
    expect(html).toContain("-100 очков");
  });
});
