import { useState } from "react";

import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { useCreateVocabulary } from "@/hooks/useVocabulary";
import type { VocabularySuggestion } from "@/types/writing";

interface VocabularySuggestionCardProps {
  suggestion: VocabularySuggestion;
}

export function VocabularySuggestionCard({ suggestion }: VocabularySuggestionCardProps) {
  const createMutation = useCreateVocabulary();
  const [added, setAdded] = useState(false);

  function handleAdd() {
    createMutation.mutate(
      {
        portuguese: suggestion.portuguese,
        english: suggestion.english,
        notes: suggestion.reason,
        tags: ["from writing coach"],
        difficulty: "medium",
      },
      { onSuccess: () => setAdded(true) }
    );
  }

  return (
    <Card className="flex items-center justify-between gap-3">
      <div>
        <p className="font-medium">{suggestion.portuguese}</p>
        <p className="text-sm text-ink/60 dark:text-ink-dark/60">{suggestion.english}</p>
        <p className="mt-1 text-xs text-ink/50 dark:text-ink-dark/50">{suggestion.reason}</p>
      </div>
      <Button
        variant={added ? "secondary" : "primary"}
        disabled={added || createMutation.isPending}
        onClick={handleAdd}
      >
        {added ? "Added ✓" : "+ Add to vocabulary"}
      </Button>
    </Card>
  );
}
