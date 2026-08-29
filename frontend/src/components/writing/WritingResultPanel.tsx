import { CorrectionCard } from "@/components/writing/CorrectionCard";
import { VocabularySuggestionCard } from "@/components/writing/VocabularySuggestionCard";
import { Card } from "@/components/ui/Card";
import type { WritingSubmission } from "@/types/writing";

interface WritingResultPanelProps {
  submission: WritingSubmission;
}

export function WritingResultPanel({ submission }: WritingResultPanelProps) {
  return (
    <div className="flex flex-col gap-4">
      <Card className="bg-primary-50 dark:bg-primary-700/20">
        <p className="text-sm text-primary-700 dark:text-primary-100">{submission.overall_feedback}</p>
      </Card>

      {submission.corrections.length > 0 && (
        <div className="flex flex-col gap-3">
          <h3 className="font-display text-lg">Corrections</h3>
          {submission.corrections.map((correction, i) => (
            <CorrectionCard key={i} correction={correction} />
          ))}
        </div>
      )}

      {submission.vocabulary_suggestions.length > 0 && (
        <div className="flex flex-col gap-3">
          <h3 className="font-display text-lg">Vocabulary you might find useful</h3>
          {submission.vocabulary_suggestions.map((suggestion, i) => (
            <VocabularySuggestionCard key={i} suggestion={suggestion} />
          ))}
        </div>
      )}
    </div>
  );
}
