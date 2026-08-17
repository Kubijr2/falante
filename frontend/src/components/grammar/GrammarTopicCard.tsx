import { Link } from "react-router-dom";

import { Badge } from "@/components/ui/Badge";
import { Card } from "@/components/ui/Card";
import type { GrammarTopicListItem } from "@/types/grammar";

interface GrammarTopicCardProps {
  topic: GrammarTopicListItem;
}

export function GrammarTopicCard({ topic }: GrammarTopicCardProps) {
  return (
    <Link to={`/grammar/${topic.slug}`}>
      <Card className="flex h-full flex-col gap-2 transition-shadow hover:shadow-md">
        <Badge tone="primary" className="w-fit">
          {topic.category}
        </Badge>
        <h3 className="font-display text-lg">{topic.title}</h3>
        <p className="text-sm text-ink/60 dark:text-ink-dark/60">{topic.summary}</p>
      </Card>
    </Link>
  );
}
