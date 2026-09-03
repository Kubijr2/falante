import { Link, useLocation, useParams } from "react-router-dom";

import { Badge } from "@/components/ui/Badge";
import { TenseTabs } from "@/components/verbs/TenseTabs";
import { useVerbDetail } from "@/hooks/useVerbs";

interface VerbNavState {
  from?: "vocabulary" | "verbs";
}

export function VerbDetailPage() {
  const { infinitive } = useParams<{ infinitive: string }>();
  const location = useLocation();
  const { data: verb, isLoading, isError } = useVerbDetail(infinitive);

  // Whoever links here decides what "back" means by passing this via the
  // <Link state={{ from: ... }}> prop — VerbSearchList (the Verb Explorer)
  // passes nothing, which defaults to "verbs" below; VocabularyCard passes
  // { from: "vocabulary" } when a saved word is recognized as a verb. This
  // is what lets the same page correctly say "Back to Vocabulary" or
  // "Back to Verb Explorer" depending on how you actually got here.
  const navState = location.state as VerbNavState | null;
  const cameFromVocabulary = navState?.from === "vocabulary";
  const backTo = cameFromVocabulary ? "/vocabulary" : "/verbs";
  const backLabel = cameFromVocabulary ? "Back to Vocabulary" : "Back to Verb Explorer";

  if (isLoading) {
    return (
      <div className="h-64 animate-pulse rounded-card border border-border bg-surface/60 dark:border-border-dark dark:bg-surface-dark/60" />
    );
  }

  if (isError || !verb) {
    return (
      <div className="flex flex-col items-center gap-3 py-10 text-center">
        <p className="text-ink/60 dark:text-ink-dark/60">Couldn't find that verb.</p>
        <Link to={backTo} className="text-primary-600 underline dark:text-primary-400">
          {backLabel}
        </Link>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-4">
      <Link to={backTo} className="text-sm text-primary-600 hover:underline dark:text-primary-400">
        ← {backLabel}
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
