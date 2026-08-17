import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { MasteryDots } from "@/components/vocabulary/MasteryDots";

describe("MasteryDots", () => {
  it("labels the mastery level for screen readers", () => {
    render(<MasteryDots level={3} />);
    expect(screen.getByLabelText("Mastery level 3 of 5")).toBeInTheDocument();
  });

  it("renders exactly 5 dots regardless of level", () => {
    render(<MasteryDots level={0} />);
    const wrapper = screen.getByLabelText("Mastery level 0 of 5");
    expect(wrapper.children.length).toBe(5);
  });
});
