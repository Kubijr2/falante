import { VocabularyCard } from "@/components/vocabulary/VocabularyCard";
import type { Vocabulary } from "@/types/vocabulary";

interface VocabularyListProps {
  words: Vocabulary[];
  isLoading: boolean;
  onDelete: (id: number) => void;
}

export function VocabularyList({ words, isLoading, onDelete }: VocabularyListProps) {
  if (isLoading) {
    return (
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {Array.from({ length: 6 }).map((_, i) => (
          <div
            key={i}
            className="h-32 animate-pulse rounded-card border border-border bg-surface/60 dark:border-border-dark dark:bg-surface-dark/60"
          />
        ))}
      </div>
    );
  }

  if (words.length === 0) {
    return (
      <div className="rounded-card border border-dashed border-border p-10 text-center text-ink/60 dark:border-border-dark dark:text-ink-dark/60">
        No words yet. Add your first word to start building your vocabulary.
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
      {words.map((word) => (
        <VocabularyCard key={word.id} word={word} onDelete={onDelete} />
      ))}
    </div>
  );
}
