import { Button } from "@/components/ui/Button";
import { Flashcard } from "@/components/vocabulary/Flashcard";
import { useFlashcardSession } from "@/hooks/useFlashcardSession";

export function FlashcardDeck() {
  const {
    currentCard,
    isFlipped,
    flip,
    submitReview,
    isSessionComplete,
    totalDue,
    remaining,
    isLoading,
    isSubmitting,
  } = useFlashcardSession();

  if (isLoading) {
    return <p className="text-center text-ink/60 dark:text-ink-dark/60">Loading today’s cards…</p>;
  }

  if (totalDue === 0) {
    return (
      <div className="rounded-card border border-dashed border-border p-10 text-center text-ink/60 dark:border-border-dark dark:text-ink-dark/60">
        Nothing due right now — add some vocabulary or check back later.
      </div>
    );
  }

  if (isSessionComplete) {
    return (
      <div className="rounded-card border border-primary-500 bg-primary-50 p-10 text-center text-primary-700 dark:bg-primary-700/20 dark:text-primary-100">
        Session complete! You reviewed {totalDue} {totalDue === 1 ? "card" : "cards"}.
      </div>
    );
  }

  if (!currentCard) return null;

  return (
    <div className="flex flex-col items-center gap-6">
      <p className="text-sm text-ink/60 dark:text-ink-dark/60">
        {remaining} of {totalDue} cards remaining
      </p>

      <Flashcard word={currentCard} isFlipped={isFlipped} onFlip={flip} />

      {isFlipped && (
        <div className="flex gap-2">
          <Button variant="danger" disabled={isSubmitting} onClick={() => submitReview("again")}>
            Again
          </Button>
          <Button variant="secondary" disabled={isSubmitting} onClick={() => submitReview("hard")}>
            Hard
          </Button>
          <Button variant="secondary" disabled={isSubmitting} onClick={() => submitReview("medium")}>
            Medium
          </Button>
          <Button disabled={isSubmitting} onClick={() => submitReview("easy")}>
            Easy
          </Button>
        </div>
      )}
    </div>
  );
}
