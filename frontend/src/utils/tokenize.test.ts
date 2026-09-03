import { describe, expect, it } from "vitest";

import { isWordToken, tokenizeText } from "@/utils/tokenize";

describe("tokenizeText", () => {
  it("splits a simple sentence into word and non-word tokens", () => {
    const tokens = tokenizeText("Eu falo português.");
    expect(tokens.join("")).toBe("Eu falo português."); // reconstructs exactly
    expect(tokens).toContain("Eu");
    expect(tokens).toContain("falo");
    expect(tokens).toContain("português");
  });

  it("preserves whitespace and newlines exactly", () => {
    const text = "Linha um.\nLinha dois.";
    const tokens = tokenizeText(text);
    expect(tokens.join("")).toBe(text);
  });

  it("handles accented Portuguese characters as part of words", () => {
    const tokens = tokenizeText("saudade não é ação");
    expect(tokens).toContain("saudade");
    expect(tokens).toContain("não");
    expect(tokens).toContain("é");
    expect(tokens).toContain("ação");
  });

  it("returns an empty array for empty input", () => {
    expect(tokenizeText("")).toEqual([]);
  });
});

describe("isWordToken", () => {
  it("identifies word tokens", () => {
    expect(isWordToken("falar")).toBe(true);
    expect(isWordToken("não")).toBe(true);
  });

  it("identifies non-word tokens", () => {
    expect(isWordToken(" ")).toBe(false);
    expect(isWordToken(".")).toBe(false);
    expect(isWordToken(", ")).toBe(false);
  });
});
