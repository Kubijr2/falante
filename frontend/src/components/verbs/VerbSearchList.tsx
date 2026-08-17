import { Link } from "react-router-dom";

import { Badge } from "@/components/ui/Badge";
import { Card } from "@/components/ui/Card";
import type { VerbListItem } from "@/types/verb";

interface VerbSearchListProps {
  verbs: VerbListItem[];
  isLoading: boolean;
}

export function VerbSearchList({ verbs, isLoading }: VerbSearchListProps) {
  if (isLoading) {
    return (
      <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
        {Array.from({ length: 6 }).map((_, i) => (
          <div
            key={i}
            className="h-16 animate-pulse rounded-card border border-border bg-surface/60 dark:border-border-dark dark:bg-surface-dark/60"
          />
        ))}
      </div>
    );
  }

  if (verbs.length === 0) {
    return (
      <div className="rounded-card border border-dashed border-border p-10 text-center text-ink/60 dark:border-border-dark dark:text-ink-dark/60">
        No verbs match that search.
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
      {verbs.map((verb) => (
        <Link key={verb.id} to={`/verbs/${verb.infinitive}`}>
          <Card className="flex items-center justify-between gap-2 transition-shadow hover:shadow-md">
            <div>
              <p className="font-display text-base">{verb.infinitive}</p>
              <p className="text-sm text-ink/60 dark:text-ink-dark/60">{verb.translation}</p>
            </div>
            {verb.is_irregular && <Badge tone="gold">irregular</Badge>}
          </Card>
        </Link>
      ))}
    </div>
  );
}
