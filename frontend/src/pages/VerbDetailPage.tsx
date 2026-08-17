import { Link, useParams } from "react-router-dom";

import { Badge } from "@/components/ui/Badge";
import { TenseTabs } from "@/components/verbs/TenseTabs";
import { useVerbDetail } from "@/hooks/useVerbs";

export function VerbDetailPage() {
  const { infinitive } = useParams<{ infinitive: string }>();
  const { data: verb, isLoading, isError } = useVerbDetail(infinitive);

  if (isLoading) {
    return (
      <div className="h-64 animate-pulse rounded-card border border-border bg-surface/60 dark:border-border-dark dark:bg-surface-dark/60" />
    );
  }

  if (isError || !verb) {
    return (
      <div className="flex flex-col items-center gap-3 py-10 text-center">
        <p className="text-ink/60 dark:text-ink-dark/60">Couldn't find that verb.</p>
        <Link to="/verbs" className="text-primary-600 underline dark:text-primary-400">
          Back to Verb Explorer
        </Link>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-4">
      <Link to="/verbs" className="text-sm text-primary-600 hover:underline dark:text-primary-400">
        ← Back to Verb Explorer
      </Link>
      <div className="flex flex-col gap-2">
        <div className="flex items-center gap-2">
          <h1 className="font-display text-2xl">{verb.infinitive}</h1>
          {verb.is_irregular && <Badge tone="gold">irregular</Badge>}
        </div>
        <p className="text-ink/60 dark:text-ink-dark/60">{verb.translation}</p>
      </div>
      <TenseTabs conjugations={verb.conjugations} />
    </div>
  );
}
