import axios from "axios";
import { useEffect, useRef, useState, type FormEvent } from "react";

import { Button } from "@/components/ui/Button";
import { useAuth } from "@/context/AuthContext";
import {
  useClearStudyAssistant,
  useSendStudyAssistantMessage,
  useStudyAssistantHistory,
} from "@/hooks/useStudyAssistant";

function extractErrorMessage(err: unknown): string {
  if (axios.isAxiosError(err) && err.response) {
    const detail = err.response.data?.detail;
    if (typeof detail === "string") return detail;
  }
  return "Something went wrong sending that — try again in a moment.";
}

export function FloatingChatBubble() {
  const { isAuthenticated } = useAuth();
  const [isOpen, setIsOpen] = useState(false);
  const [draft, setDraft] = useState("");
  const [confirmingClear, setConfirmingClear] = useState(false);
  const [sendError, setSendError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const { data: history = [], isLoading } = useStudyAssistantHistory(isOpen && isAuthenticated);
  const sendMessage = useSendStudyAssistantMessage();
  const clearHistory = useClearStudyAssistant();

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [history, sendMessage.isPending]);

  // Not rendered at all for logged-out visitors — this assistant is built
  // entirely around the user's own vocabulary/progress data, so there's
  // nothing useful to show without an account.
  if (!isAuthenticated) return null;

  function handleSubmit(e: FormEvent) {
    e.preventDefault();
    const message = draft.trim();
    if (!message || sendMessage.isPending) return;
    setSendError(null);
    setDraft("");
    sendMessage.mutate(message, {
      onError: (err) => setSendError(extractErrorMessage(err)),
    });
  }

  function handleClearConfirmed() {
    clearHistory.mutate(undefined, {
      onSettled: () => setConfirmingClear(false),
    });
  }

  return (
    <div className="fixed bottom-5 right-5 z-50 flex flex-col items-end gap-3">
      {isOpen && (
        <div className="flex h-[28rem] w-80 flex-col overflow-hidden rounded-card border border-border bg-surface shadow-lg dark:border-border-dark dark:bg-surface-dark">
          <div className="flex items-center justify-between border-b border-border px-4 py-3 dark:border-border-dark">
            <p className="font-display text-base">Study Assistant</p>
            <div className="flex items-center gap-2">
              {confirmingClear ? (
                <div className="flex items-center gap-1 text-xs">
                  <span className="text-ink/60 dark:text-ink-dark/60">Clear all?</span>
                  <button
                    onClick={handleClearConfirmed}
                    className="font-medium text-red-600 hover:underline"
                  >
                    Yes
                  </button>
                  <button
                    onClick={() => setConfirmingClear(false)}
                    className="text-ink/60 hover:underline dark:text-ink-dark/60"
                  >
                    No
                  </button>
                </div>
              ) : (
                history.length > 0 && (
                  <button
                    onClick={() => setConfirmingClear(true)}
                    className="text-xs text-ink/50 hover:underline dark:text-ink-dark/50"
                  >
                    Clear
                  </button>
                )
              )}
              <button
                onClick={() => setIsOpen(false)}
                aria-label="Close Study Assistant"
                className="text-ink/50 hover:text-ink dark:text-ink-dark/50 dark:hover:text-ink-dark"
              >
                ✕
              </button>
            </div>
          </div>

          <div className="flex-1 overflow-y-auto px-4 py-3">
            {isLoading ? (
              <p className="text-sm text-ink/50 dark:text-ink-dark/50">Loading…</p>
            ) : history.length === 0 ? (
              <p className="text-sm text-ink/60 dark:text-ink-dark/60">
                Ask me anything about your Portuguese studies — I know what you've been
                practicing and can help you work through it, hints first.
              </p>
            ) : (
              <div className="flex flex-col gap-2">
                {history.map((message) => (
                  <div
                    key={message.id}
                    className={`rounded-card px-3 py-2 text-sm ${
                      message.role === "user"
                        ? "self-end max-w-[85%] bg-primary-500 text-white"
                        : "self-start max-w-[85%] bg-border/40 dark:bg-border-dark/40"
                    }`}
                  >
                    {message.content}
                  </div>
                ))}
                {sendMessage.isPending && (
                  <div className="self-start rounded-card bg-border/40 px-3 py-2 text-sm text-ink/50 dark:bg-border-dark/40 dark:text-ink-dark/50">
                    Thinking…
                  </div>
                )}
                <div ref={messagesEndRef} />
              </div>
            )}
            {sendError && <p className="mt-2 text-xs text-red-600">{sendError}</p>}
          </div>

          <form onSubmit={handleSubmit} className="flex gap-2 border-t border-border p-3 dark:border-border-dark">
            <input
              value={draft}
              onChange={(e) => setDraft(e.target.value)}
              placeholder="Ask a question…"
              className="flex-1 rounded-lg border border-border bg-base px-3 py-1.5 text-sm outline-none dark:border-border-dark dark:bg-base-dark"
            />
            <Button type="submit" disabled={sendMessage.isPending || !draft.trim()}>
              Send
            </Button>
          </form>
        </div>
      )}

      <button
        onClick={() => setIsOpen((prev) => !prev)}
        aria-label={isOpen ? "Close Study Assistant" : "Open Study Assistant"}
        className="flex h-14 w-14 items-center justify-center rounded-full bg-primary-500 text-white shadow-lg transition-transform hover:scale-105"
      >
        {isOpen ? "✕" : "💬"}
      </button>
    </div>
  );
}
