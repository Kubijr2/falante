import { Badge } from "@/components/ui/Badge";
import { Card } from "@/components/ui/Card";
import type { Correction } from "@/types/writing";

interface CorrectionCardProps {
  correction: Correction;
}

export function CorrectionCard({ correction }: CorrectionCardProps) {
  return (
    <Card className="flex flex-col gap-2">
      <Badge tone={correction.type === "grammar" ? "primary" : "gold"} className="w-fit">
        {correction.type === "grammar" ? "Grammar" : "Natural wording"}
      </Badge>
      <div className="flex flex-col gap-1 text-sm">
        <p className="text-red-600 line-through decoration-red-400">{correction.original}</p>
        <p className="font-medium text-primary-700 dark:text-primary-100">{correction.corrected}</p>
      </div>
      <p className="text-sm text-ink/70 dark:text-ink-dark/70">{correction.explanation}</p>
    </Card>
  );
}
