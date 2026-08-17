import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { MasteryDots } from "@/components/vocabulary/MasteryDots";
import type { Vocabulary } from "@/types/vocabulary";

interface VocabularyCardProps {
  word: Vocabulary;
  onDelete: (id: number) => void;
}

export function VocabularyCard({ word, onDelete }: VocabularyCardProps) {
  return (
    <Card className="flex flex-col gap-2">
      <div className="flex items-start justify-between">
        <div>
          <h3 className="font-display text-lg">{word.portuguese}</h3>
          <p className="text-sm text-ink/70 dark:text-ink-dark/70">{word.english}</p>
        </div>
        <Button variant="ghost" onClick={() => onDelete(word.id)} aria-label={`Delete ${word.portuguese}`}>
          ✕
        </Button>
      </div>

      {word.example_sentence && (
        <p className="text-sm italic text-ink/60 dark:text-ink-dark/60">
          “{word.example_sentence}”
        </p>
      )}

      <div className="flex flex-wrap items-center gap-2 pt-1">
        {word.category && <Badge tone="primary">{word.category}</Badge>}
        {word.tags.map((tag) => (
          <Badge key={tag} tone="neutral">
            {tag}
          </Badge>
        ))}
      </div>

      <div className="flex items-center justify-between pt-2">
        <MasteryDots level={word.mastery_level} />
        <Badge tone="gold">{word.difficulty}</Badge>
      </div>
    </Card>
  );
}
