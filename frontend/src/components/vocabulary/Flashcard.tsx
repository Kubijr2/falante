import type { Vocabulary } from "@/types/vocabulary";

interface FlashcardProps {
  word: Vocabulary;
  isFlipped: boolean;
  onFlip: () => void;
}

export function Flashcard({ word, isFlipped, onFlip }: FlashcardProps) {
  return (
    <div className="[perspective:1200px]">
      <button
        type="button"
        onClick={onFlip}
        aria-label={isFlipped ? "Show Portuguese" : "Show English translation"}
        className="relative h-64 w-full max-w-sm mx-auto rounded-card text-left transition-transform duration-500 [transform-style:preserve-3d]"
        style={{ transform: isFlipped ? "rotateY(180deg)" : "rotateY(0deg)" }}
      >
        {/* Front: Portuguese */}
        <div className="absolute inset-0 flex flex-col items-center justify-center gap-2 rounded-card border border-border bg-surface p-6 shadow-sm [backface-visibility:hidden] dark:border-border-dark dark:bg-surface-dark">
          <span className="text-xs uppercase tracking-wide text-ink/50 dark:text-ink-dark/50">
            Portuguese
          </span>
          <span className="font-display text-3xl">{word.portuguese}</span>
          <span className="text-xs text-ink/40 dark:text-ink-dark/40">Tap to flip</span>
        </div>

        {/* Back: English */}
        <div
          className="absolute inset-0 flex flex-col items-center justify-center gap-2 rounded-card border border-primary-500 bg-primary-50 p-6 shadow-sm [backface-visibility:hidden] dark:bg-primary-700/20"
          style={{ transform: "rotateY(180deg)" }}
        >
          <span className="text-xs uppercase tracking-wide text-primary-700 dark:text-primary-100">
            English
          </span>
          <span className="font-display text-3xl text-primary-700 dark:text-primary-100">
            {word.english}
          </span>
          {word.example_sentence && (
            <span className="text-center text-sm italic text-primary-700/80 dark:text-primary-100/80">
              “{word.example_sentence}”
            </span>
          )}
        </div>
      </button>
    </div>
  );
}
