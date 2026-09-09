import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";

vi.mock("@/services/api/studyAssistant", () => ({
  studyAssistantApi: {
    getHistory: vi.fn(),
    sendMessage: vi.fn(),
    clearHistory: vi.fn(),
  },
}));

vi.mock("@/context/AuthContext", () => ({
  useAuth: vi.fn(),
}));

import { FloatingChatBubble } from "@/components/study-assistant/FloatingChatBubble";
import { useAuth } from "@/context/AuthContext";
import { studyAssistantApi } from "@/services/api/studyAssistant";

function renderWithClient() {
  const client = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  return render(
    <QueryClientProvider client={client}>
      <FloatingChatBubble />
    </QueryClientProvider>
  );
}

beforeEach(() => {
  vi.mocked(studyAssistantApi.getHistory).mockReset().mockResolvedValue([]);
  vi.mocked(studyAssistantApi.sendMessage).mockReset();
  vi.mocked(studyAssistantApi.clearHistory).mockReset().mockResolvedValue(undefined);
});

describe("FloatingChatBubble", () => {
  it("renders nothing at all for a logged-out visitor", () => {
    vi.mocked(useAuth).mockReturnValue({ isAuthenticated: false } as ReturnType<typeof useAuth>);
    const { container } = renderWithClient();
    expect(container).toBeEmptyDOMElement();
  });

  it("shows the bubble button for a logged-in user, closed by default", () => {
    vi.mocked(useAuth).mockReturnValue({ isAuthenticated: true } as ReturnType<typeof useAuth>);
    renderWithClient();
    expect(screen.getByLabelText("Open Study Assistant")).toBeInTheDocument();
    expect(screen.queryByText("Study Assistant")).not.toBeInTheDocument();
  });

  it("opens the panel and shows the empty-state prompt when there's no history", async () => {
    vi.mocked(useAuth).mockReturnValue({ isAuthenticated: true } as ReturnType<typeof useAuth>);
    renderWithClient();

    fireEvent.click(screen.getByLabelText("Open Study Assistant"));

    await waitFor(() => {
      expect(screen.getByText(/ask me anything about your portuguese studies/i)).toBeInTheDocument();
    });
  });

  it("loads and displays existing conversation history when opened", async () => {
    vi.mocked(useAuth).mockReturnValue({ isAuthenticated: true } as ReturnType<typeof useAuth>);
    vi.mocked(studyAssistantApi.getHistory).mockResolvedValue([
      { id: 1, role: "user", content: "Why is ser different from estar?", created_at: "2026-01-01" },
      { id: 2, role: "assistant", content: "Great question — what do you think?", created_at: "2026-01-01" },
    ]);
    renderWithClient();

    fireEvent.click(screen.getByLabelText("Open Study Assistant"));

    await waitFor(() => {
      expect(screen.getByText("Why is ser different from estar?")).toBeInTheDocument();
      expect(screen.getByText("Great question — what do you think?")).toBeInTheDocument();
    });
  });

  it("sends a message and shows the updated history", async () => {
    vi.mocked(useAuth).mockReturnValue({ isAuthenticated: true } as ReturnType<typeof useAuth>);
    vi.mocked(studyAssistantApi.getHistory)
      .mockResolvedValueOnce([])
      .mockResolvedValueOnce([
        { id: 1, role: "user", content: "Help me practice", created_at: "2026-01-01" },
        { id: 2, role: "assistant", content: "Sure — try this word first", created_at: "2026-01-01" },
      ]);
    vi.mocked(studyAssistantApi.sendMessage).mockResolvedValue({ reply: "Sure — try this word first" });

    renderWithClient();
    fireEvent.click(screen.getByLabelText("Open Study Assistant"));
    await waitFor(() => screen.getByPlaceholderText("Ask a question…"));

    fireEvent.change(screen.getByPlaceholderText("Ask a question…"), {
      target: { value: "Help me practice" },
    });
    fireEvent.click(screen.getByText("Send"));

    await waitFor(() => {
      expect(screen.getByText("Sure — try this word first")).toBeInTheDocument();
    });
    expect(studyAssistantApi.sendMessage).toHaveBeenCalledWith(
      "Help me practice",
      expect.anything()
    );
  });

  it("shows a friendly error message when sending fails", async () => {
    const axiosError = {
      isAxiosError: true,
      response: { data: { detail: "You've reached today's limit." } },
    };
    vi.mocked(useAuth).mockReturnValue({ isAuthenticated: true } as ReturnType<typeof useAuth>);
    vi.mocked(studyAssistantApi.getHistory).mockResolvedValue([]);
    vi.mocked(studyAssistantApi.sendMessage).mockRejectedValue(axiosError);

    renderWithClient();
    fireEvent.click(screen.getByLabelText("Open Study Assistant"));
    await waitFor(() => screen.getByPlaceholderText("Ask a question…"));

    fireEvent.change(screen.getByPlaceholderText("Ask a question…"), {
      target: { value: "test" },
    });
    fireEvent.click(screen.getByText("Send"));

    await waitFor(() => {
      expect(screen.getByText("You've reached today's limit.")).toBeInTheDocument();
    });
  });

  it("requires a Yes/No confirmation before clearing", async () => {
    vi.mocked(useAuth).mockReturnValue({ isAuthenticated: true } as ReturnType<typeof useAuth>);
    vi.mocked(studyAssistantApi.getHistory).mockResolvedValue([
      { id: 1, role: "user", content: "hi", created_at: "2026-01-01" },
    ]);

    renderWithClient();
    fireEvent.click(screen.getByLabelText("Open Study Assistant"));
    await waitFor(() => screen.getByText("Clear"));

    fireEvent.click(screen.getByText("Clear"));
    expect(screen.getByText("Clear all?")).toBeInTheDocument();

    fireEvent.click(screen.getByText("Yes"));

    await waitFor(() => {
      expect(studyAssistantApi.clearHistory).toHaveBeenCalled();
    });
  });
});
