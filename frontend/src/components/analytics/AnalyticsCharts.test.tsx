import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { RangeSelector } from "@/components/analytics/RangeSelector";
import { ReviewActivityHeatmap } from "@/components/analytics/ReviewActivityHeatmap";
import { VocabularyGrowthChart } from "@/components/analytics/VocabularyGrowthChart";

describe("VocabularyGrowthChart", () => {
  it("shows an empty-state message with no data", () => {
    render(<VocabularyGrowthChart data={[]} />);
    expect(screen.getByText(/add some words/i)).toBeInTheDocument();
  });

  it("renders without crashing when given real data", () => {
    render(
      <VocabularyGrowthChart
        data={[
          { date: "2026-01-01", count: 2, cumulative: 2 },
          { date: "2026-01-02", count: 1, cumulative: 3 },
        ]}
      />
    );
    expect(screen.getByText("Vocabulary Growth")).toBeInTheDocument();
  });

  it("shows a friendly message instead of a blank chart for a single day of data", () => {
    render(<VocabularyGrowthChart data={[{ date: "2026-01-01", count: 3, cumulative: 3 }]} />);
    expect(screen.getByText(/check back after a few more days/i)).toBeInTheDocument();
  });
});

describe("ReviewActivityHeatmap", () => {
  it("shows an empty-state message with no data", () => {
    render(<ReviewActivityHeatmap data={[]} />);
    expect(screen.getByText(/review a flashcard/i)).toBeInTheDocument();
  });

  it("renders one cell per day of data", () => {
    const { container } = render(
      <ReviewActivityHeatmap
        data={[
          { date: "2026-01-01", count: 3 },
          { date: "2026-01-02", count: 0 },
          { date: "2026-01-03", count: 7 },
        ]}
      />
    );
    // Each day renders as one colored div cell — 3 days in, 3 cells out.
    expect(container.querySelectorAll("[title]").length).toBe(3);
  });

  it("gives the busiest day the strongest color intensity", () => {
    const { container } = render(
      <ReviewActivityHeatmap
        data={[
          { date: "2026-01-01", count: 1 },
          { date: "2026-01-02", count: 10 },
        ]}
      />
    );
    const cells = container.querySelectorAll("[title]");
    // The max-count cell should get the darkest class, not the lightest.
    expect(cells[1].className).toContain("bg-primary-600");
  });
});

describe("RangeSelector", () => {
  it("highlights the currently selected range", () => {
    render(<RangeSelector value="30d" onChange={() => {}} />);
    const activeButton = screen.getByText("30 days");
    expect(activeButton.className).toContain("bg-primary-500");
  });

  it("calls onChange with the clicked range", () => {
    let selected: string | null = null;
    render(<RangeSelector value="30d" onChange={(r) => (selected = r)} />);
    screen.getByText("7 days").click();
    expect(selected).toBe("7d");
  });
});
