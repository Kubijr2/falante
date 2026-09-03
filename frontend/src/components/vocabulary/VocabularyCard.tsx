import type { MouseEvent } from "react";
import { Link } from "react-router-dom";

import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { MasteryDots } from "@/components/vocabulary/MasteryDots";
import type { VerbListItem } from "@/types/verb";
import type { Vocabulary } from "@/types/vocabulary";

interface VocabularyCardProps {
  word: Vocabulary;
  onDelete: (id: number) => void;
  // Set when `word.portuguese` matches a known verb infinitive — turns the
  // card into a link through to that verb's conjugation page.
  matchedVerb?: VerbListItem;
}

export function VocabularyCard({ word, onDelete, matchedVerb }: VocabularyCardProps) {
  // The delete button lives inside what may become a <Link> — without
  // stopping propagation, clicking it would also trigger navigation.
  function handleDeleteClick(e: MouseEvent<HTMLButtonElement>) {
    e.preventDefault();
    e.stopPropagation();
    onDelete(word.id);
  }

  const cardBody = (
    <Card
      className={`flex flex-col gap-2 ${matchedVerb ? "transition-shadow hover:shadow-md" : ""}`}
    >
      <div className="flex items-start justify-between">
        <div>
          <h3 className="font-display text-lg">{word.portuguese}</h3>
          <p className="text-sm text-ink/70 dark:text-ink-dark/70">{word.english}</p>
        </div>
        <Button
          variant="ghost"
          onClick={handleDeleteClick}
          aria-label={`Delete ${word.portuguese}`}
        >
          ✕
        </Button>
      </div>

      {word.example_sentence && (
        <p className="text-sm italic text-ink/60 dark:text-ink-dark/60">
          "{word.example_sentence}"
        </p>
      )}

      <div className="flex flex-wrap items-center gap-2 pt-1">
        {matchedVerb && <Badge tone="primary">Verb</Badge>}
        {matchedVerb?.is_irregular && <Badge tone="gold">irregular</Badge>}
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

      {matchedVerb && (
        <p className="pt-1 text-xs text-primary-600 dark:text-primary-400">
          Tap to see conjugations →
        </p>
      )}
    </Card>
  );

  if (matchedVerb) {
    return (
      <Link to={`/verbs/${matchedVerb.infinitive}`} state={{ from: "vocabulary" }}>
        {cardBody}
      </Link>
    );
  }

  return cardBody;
}
