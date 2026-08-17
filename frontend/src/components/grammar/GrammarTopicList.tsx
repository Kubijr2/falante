import { GrammarTopicCard } from "@/components/grammar/GrammarTopicCard";
import type { GrammarTopicListItem } from "@/types/grammar";

interface GrammarTopicListProps {
  topics: GrammarTopicListItem[];
  isLoading: boolean;
}

export function GrammarTopicList({ topics, isLoading }: GrammarTopicListProps) {
  if (isLoading) {
    return (
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {Array.from({ length: 5 }).map((_, i) => (
          <div
            key={i}
            className="h-32 animate-pulse rounded-card border border-border bg-surface/60 dark:border-border-dark dark:bg-surface-dark/60"
          />
        ))}
      </div>
    );
  }

  if (topics.length === 0) {
    return (
      <div className="rounded-card border border-dashed border-border p-10 text-center text-ink/60 dark:border-border-dark dark:text-ink-dark/60">
        No topics match that search or filter.
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
      {topics.map((topic) => (
        <GrammarTopicCard key={topic.slug} topic={topic} />
      ))}
    </div>
  );
}
