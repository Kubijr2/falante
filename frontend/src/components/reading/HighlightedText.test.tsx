import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import type { ReactElement } from "react";
import { beforeEach, describe, expect, it, vi } from "vitest";

vi.mock("@/services/api/verb", () => ({
  verbApi: {
    lookupBatch: vi.fn(),
  },
}));

import { HighlightedText } from "@/components/reading/HighlightedText";
import { verbApi } from "@/services/api/verb";
import type { Vocabulary } from "@/types/vocabulary";

const knownWord: Vocabulary = {
  id: 1,
  portuguese: "falar",
  english: "to speak",
  example_sentence: null,
  notes: null,
  category: null,
  tags: [],
  difficulty: "medium",
  mastery_level: 2,
  next_review_at: "",
  created_at: "",
  updated_at: "",
};

function renderWithClient(ui: ReactElement) {
  const client = new QueryClient();
  return render(<QueryClientProvider client={client}>{ui}</QueryClientProvider>);
}

beforeEach(() => {
  vi.mocked(verbApi.lookupBatch).mockReset();
  vi.mocked(verbApi.lookupBatch).mockResolvedValue({});
});

describe("HighlightedText", () => {
  it("shows a placeholder when text is empty", () => {
    renderWithClient(<HighlightedText text="" vocabulary={[]} onWordClick={vi.fn()} />);
    expect(screen.getByText(/paste some portuguese text/i)).toBeInTheDocument();
  });

  it("reconstructs the original text exactly across all tokens", () => {
    const { container } = renderWithClient(
      <HighlightedText text="Eu quero falar." vocabulary={[]} onWordClick={vi.fn()} />
    );
    expect(container.textContent).toBe("Eu quero falar.");
  });

  it("calls onWordClick with the matched vocabulary entry for a known word", () => {
    const onWordClick = vi.fn();
    renderWithClient(
      <HighlightedText text="Eu quero falar." vocabulary={[knownWord]} onWordClick={onWordClick} />
    );
    fireEvent.click(screen.getByText("falar"));
    expect(onWordClick).toHaveBeenCalledWith("falar", knownWord, null);
  });

  it("calls onWordClick with null match and null verbMatch for a plain unknown word", () => {
    const onWordClick = vi.fn();
    renderWithClient(
      <HighlightedText text="Eu quero xilofone." vocabulary={[knownWord]} onWordClick={onWordClick} />
    );
    fireEvent.click(screen.getByText("xilofone"));
    expect(onWordClick).toHaveBeenCalledWith("xilofone", null, null);
  });

  it("matches known words case-insensitively", () => {
    const onWordClick = vi.fn();
    renderWithClient(
      <HighlightedText text="Falar é bom." vocabulary={[knownWord]} onWordClick={onWordClick} />
    );
    fireEvent.click(screen.getByText("Falar"));
    expect(onWordClick).toHaveBeenCalledWith("Falar", knownWord, null);
  });

  it("does not render punctuation or whitespace as clickable buttons", () => {
    renderWithClient(<HighlightedText text="Oi, tudo bem?" vocabulary={[]} onWordClick={vi.fn()} />);
    expect(screen.getAllByRole("button")).toHaveLength(3);
  });

  it("treats a conjugated form of a known verb as known once the lookup resolves", async () => {
    vi.mocked(verbApi.lookupBatch).mockResolvedValue({
      falo: { infinitive: "falar", translation: "to speak" },
    });
    const onWordClick = vi.fn();
    renderWithClient(
      <HighlightedText text="Eu falo português." vocabulary={[knownWord]} onWordClick={onWordClick} />
    );

    // Wait for the debounced lookup to resolve and the word to re-render
    // with "known" styling before clicking it.
    await waitFor(
      () => {
        expect(screen.getByText("falo").className).toContain("border-primary-400");
      },
      { timeout: 2000 }
    );

    fireEvent.click(screen.getByText("falo"));
    expect(onWordClick).toHaveBeenCalledWith("falo", knownWord, null);
  });

  it("keeps an unrecognized-but-verb-shaped word unknown, passing the verb match through", async () => {
    vi.mocked(verbApi.lookupBatch).mockResolvedValue({
      comi: { infinitive: "comer", translation: "to eat" },
    });
    const onWordClick = vi.fn();
    renderWithClient(
      <HighlightedText text="Eu comi pizza." vocabulary={[knownWord]} onWordClick={onWordClick} />
    );

    await waitFor(
      () => {
        expect(vi.mocked(verbApi.lookupBatch)).toHaveBeenCalled();
      },
      { timeout: 2000 }
    );

    // "comer" isn't in the vocabulary, so even though it's a recognized
    // verb form, it stays visually "unknown" — the smart suggestion lives
    // in the modal (via verbMatch), not in the highlight color.
    await waitFor(() => {
      expect(screen.getByText("comi").className).toContain("border-gold-500");
    });

    fireEvent.click(screen.getByText("comi"));
    expect(onWordClick).toHaveBeenCalledWith("comi", null, {
      infinitive: "comer",
      translation: "to eat",
    });
  });
});
