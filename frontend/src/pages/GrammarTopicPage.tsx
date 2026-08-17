import { Link, useParams } from "react-router-dom";

import { GrammarArticle } from "@/components/grammar/GrammarArticle";
import { TutorPanel } from "@/components/grammar/TutorPanel";
import { Badge } from "@/components/ui/Badge";
import { useGrammarTopic } from "@/hooks/useGrammar";

export function GrammarTopicPage() {
  const { slug } = useParams<{ slug: string }>();
  const { data: topic, isLoading, isError } = useGrammarTopic(slug);

  if (isLoading) {
    return (
      <div className="h-64 animate-pulse rounded-card border border-border bg-surface/60 dark:border-border-dark dark:bg-surface-dark/60" />
    );
  }

  if (isError || !topic) {
    return (
      <div className="flex flex-col items-center gap-3 py-10 text-center">
        <p className="text-ink/60 dark:text-ink-dark/60">
          Couldn't find that grammar topic.
        </p>
        <Link to="/grammar" className="text-primary-600 underline dark:text-primary-400">
          Back to Grammar Reference
        </Link>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-4">
      <Link to="/grammar" className="text-sm text-primary-600 hover:underline dark:text-primary-400">
        ← Back to Grammar Reference
      </Link>
      <div className="flex flex-col gap-2">
        <Badge tone="primary" className="w-fit">
          {topic.category}
        </Badge>
        <h1 className="font-display text-2xl">{topic.title}</h1>
        <p className="text-ink/60 dark:text-ink-dark/60">{topic.summary}</p>
      </div>
      <GrammarArticle content={topic.content} />
      <TutorPanel topicSlug={topic.slug} />
    </div>
  );
}
