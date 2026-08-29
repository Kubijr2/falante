import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { CorrectionCard } from "@/components/writing/CorrectionCard";

describe("CorrectionCard", () => {
  it("shows the grammar badge for grammar corrections", () => {
    render(
      <CorrectionCard
        correction={{
          type: "grammar",
          original: "Eu gosta",
          corrected: "Eu gosto",
          explanation: "First person conjugation.",
        }}
      />
    );
    expect(screen.getByText("Grammar")).toBeInTheDocument();
    expect(screen.getByText("Eu gosta")).toBeInTheDocument();
    expect(screen.getByText("Eu gosto")).toBeInTheDocument();
  });

  it("shows the natural wording badge for wording suggestions", () => {
    render(
      <CorrectionCard
        correction={{
          type: "wording",
          original: "Eu fico muito feliz",
          corrected: "Fico super feliz",
          explanation: "More natural in casual speech.",
        }}
      />
    );
    expect(screen.getByText("Natural wording")).toBeInTheDocument();
  });
});
