import { Badge } from "@/components/ui/Badge";
import { Card } from "@/components/ui/Card";
import type { Vocabulary } from "@/types/vocabulary";

interface RecentlyLearnedProps {
  words: Vocabulary[];
}

export function RecentlyLearned({ words }: RecentlyLearnedProps) {
  return (
    <Card>
      <p className="mb-3 font-display text-lg">Recently learned</p>
      {words.length === 0 ? (
        <p className="text-sm text-ink/60 dark:text-ink-dark/60">
          Nothing yet — review a flashcard and mark it "Medium" or "Easy" to see progress here.
        </p>
      ) : (
        <ul className="flex flex-col gap-2">
          {words.map((word) => (
            <li key={word.id} className="flex items-center justify-between text-sm">
              <span>
                <span className="font-medium">{word.portuguese}</span>
                <span className="text-ink/60 dark:text-ink-dark/60"> — {word.english}</span>
              </span>
              <Badge tone="gold">Level {word.mastery_level}</Badge>
            </li>
          ))}
        </ul>
      )}
    </Card>
  );
}
