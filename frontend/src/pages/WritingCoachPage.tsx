import { useState, type FormEvent } from "react";

import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { WritingResultPanel } from "@/components/writing/WritingResultPanel";
import { useReviewWriting, useWritingHistory } from "@/hooks/useWriting";
import { useTutorStatus } from "@/hooks/useTutor";
// Reuses the Tutor's status check on purpose — /tutor/status just reports
// whether AI is configured at all (bool(settings.ai_api_key)), which is
// exactly what every AI feature needs to know, not something tutor-specific.

export function WritingCoachPage() {
  const { data: status, isLoading: statusLoading } = useTutorStatus();
  const [text, setText] = useState("");
  const reviewMutation = useReviewWriting();
  const { data: history = [] } = useWritingHistory();

  function handleSubmit(e: FormEvent) {
    e.preventDefault();
    const trimmed = text.trim();
    if (!trimmed || reviewMutation.isPending) return;
    reviewMutation.mutate(trimmed);
  }

  if (statusLoading) {
    return (
      <div className="h-40 animate-pulse rounded-card border border-border bg-surface/60 dark:border-border-dark dark:bg-surface-dark/60" />
    );
  }

  if (!status?.enabled) {
    return (
      <div className="flex flex-col gap-6">
        <h1 className="font-display text-2xl">Writing Coach</h1>
        <Card className="text-sm text-ink/60 dark:text-ink-dark/60">
          AI features aren't configured for this app yet. Add an <code>AI_API_KEY</code> to{" "}
          <code>backend/.env</code> and restart the backend to enable the Writing Coach.
        </Card>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-6">
      <h1 className="font-display text-2xl">Writing Coach</h1>
      <p className="text-sm text-ink/60 dark:text-ink-dark/60">
        Paste something you wrote in Portuguese — get grammar corrections, natural wording
        suggestions, and vocabulary ideas, all with explanations.
      </p>

      <form onSubmit={handleSubmit} className="flex flex-col gap-3">
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          rows={6}
          placeholder="Cole aqui o que você escreveu em português…"
          className="rounded-lg border border-border bg-surface p-3 text-sm text-ink outline-none dark:border-border-dark dark:bg-surface-dark dark:text-ink-dark"
        />
        <div className="flex justify-end">
          <Button type="submit" disabled={!text.trim() || reviewMutation.isPending}>
            {reviewMutation.isPending ? "Reviewing…" : "Get feedback"}
          </Button>
        </div>
      </form>

      {reviewMutation.isError && (
        <p className="text-sm text-red-600">
          Something went wrong reviewing that — try again in a moment.
        </p>
      )}

      {reviewMutation.data && <WritingResultPanel submission={reviewMutation.data} />}

      {history.length > 0 && (
        <div className="flex flex-col gap-2 pt-4">
          <h2 className="font-display text-lg">Past submissions</h2>
          {history.map((submission) => (
            <Card key={submission.id} className="text-sm">
              <p className="line-clamp-2 text-ink/70 dark:text-ink-dark/70">
                {submission.original_text}
              </p>
              <p className="mt-1 text-xs text-ink/50 dark:text-ink-dark/50">
                {new Date(submission.created_at).toLocaleDateString()} ·{" "}
                {submission.corrections.length} correction
                {submission.corrections.length === 1 ? "" : "s"}
              </p>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
