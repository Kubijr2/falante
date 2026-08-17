import { useState, type FormEvent } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { useTutorChat, useTutorStatus } from "@/hooks/useTutor";

interface TutorPanelProps {
  topicSlug: string;
}

export function TutorPanel({ topicSlug }: TutorPanelProps) {
  const { data: status, isLoading: statusLoading } = useTutorStatus();
  const { messages, sendQuestion, isSending, error } = useTutorChat(topicSlug);
  const [draft, setDraft] = useState("");

  function handleSubmit(e: FormEvent) {
    e.preventDefault();
    const question = draft.trim();
    if (!question || isSending) return;
    sendQuestion(question);
    setDraft("");
  }

  if (statusLoading) {
    return (
      <div className="h-32 animate-pulse rounded-card border border-border bg-surface/60 dark:border-border-dark dark:bg-surface-dark/60" />
    );
  }

  if (!status?.enabled) {
    return (
      <Card className="text-sm text-ink/60 dark:text-ink-dark/60">
        <p className="font-display text-lg text-ink dark:text-ink-dark">Ask the Tutor</p>
        <p className="mt-1">
          AI features aren't configured for this app yet. Add an <code>AI_API_KEY</code> to{" "}
          <code>backend/.env</code> and restart the backend to enable the tutor.
        </p>
      </Card>
    );
  }

  return (
    <Card className="flex flex-col gap-3">
      <p className="font-display text-lg">Ask the Tutor</p>
      <p className="text-sm text-ink/60 dark:text-ink-dark/60">
        Ask a question about this topic — it can explain the "why," not just translate.
      </p>

      {messages.length > 0 && (
        <div className="flex flex-col gap-3 max-h-96 overflow-y-auto py-2">
          {messages.map((message, i) => (
            <div
              key={i}
              className={`rounded-card px-4 py-2 text-sm ${
                message.role === "user"
                  ? "self-end bg-primary-500 text-white max-w-[85%]"
                  : "self-start bg-border/40 dark:bg-border-dark/40 max-w-[85%] [&_p]:mb-2 [&_p:last-child]:mb-0"
              }`}
            >
              {message.role === "assistant" ? (
                <ReactMarkdown remarkPlugins={[remarkGfm]}>{message.content}</ReactMarkdown>
              ) : (
                message.content
              )}
            </div>
          ))}
          {isSending && (
            <div className="self-start rounded-card bg-border/40 px-4 py-2 text-sm text-ink/50 dark:bg-border-dark/40 dark:text-ink-dark/50">
              Thinking…
            </div>
          )}
        </div>
      )}

      {error && (
        <p className="text-sm text-red-600">
          Something went wrong asking that — try again in a moment.
        </p>
      )}

      <form onSubmit={handleSubmit} className="flex gap-2">
        <input
          value={draft}
          onChange={(e) => setDraft(e.target.value)}
          placeholder="e.g. Why is estar used here instead of ser?"
          className="flex-1 rounded-lg border border-border bg-surface px-3 py-2 text-sm text-ink outline-none dark:border-border-dark dark:bg-surface-dark dark:text-ink-dark"
        />
        <Button type="submit" disabled={isSending || !draft.trim()}>
          Ask
        </Button>
      </form>
    </Card>
  );
}
