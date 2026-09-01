import { readFileSync, readdirSync } from "node:fs";
import { extname, join } from "node:path";
import ts from "typescript";
import { describe, expect, it } from "vitest";

const forbiddenBrowserGlobals = [
  "window",
  "document",
  "navigator",
  "localStorage",
  "sessionStorage",
  "indexedDB",
  "fetch",
  "WebSocket",
  "AudioContext",
  "Gamepad"
];

function sourceFiles(root: string): string[] {
  return readdirSync(root, { withFileTypes: true }).flatMap((entry) => {
    const path = join(root, entry.name);
    if (entry.isDirectory()) return sourceFiles(path);
    return [".ts", ".tsx"].includes(extname(entry.name)) ? [path] : [];
  });
}

describe("domain architecture boundary", () => {
  it("does not import UI or browser APIs", () => {
    const files = sourceFiles("src/domain");
    expect(files.length).toBeGreaterThan(0);

    for (const file of files) {
      const source = readFileSync(file, "utf8");
      const sourceFile = ts.createSourceFile(file, source, ts.ScriptTarget.Latest, true);

      function verify(node: ts.Node) {
        if (ts.isImportDeclaration(node) && ts.isStringLiteral(node.moduleSpecifier)) {
          const specifier = node.moduleSpecifier.text;
          expect(specifier, `${file} imports UI/runtime dependency ${specifier}`).not.toMatch(
            /^(react|react-dom)(\/|$)|(^|\/)(ui|adapters)(\/|$)/
          );
        }

        if (ts.isIdentifier(node)) {
          expect(
            forbiddenBrowserGlobals,
            `${file} references forbidden browser global ${node.text}`
          ).not.toContain(node.text);
        }

        ts.forEachChild(node, verify);
      }

      verify(sourceFile);
    }
  });
});
