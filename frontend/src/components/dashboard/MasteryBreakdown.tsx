import { Card } from "@/components/ui/Card";

interface MasteryBreakdownProps {
  distribution: Record<number, number>;
}

export function MasteryBreakdown({ distribution }: MasteryBreakdownProps) {
  const levels = [0, 1, 2, 3, 4, 5];
  const max = Math.max(1, ...levels.map((l) => distribution[l] ?? 0));

  return (
    <Card>
      <p className="mb-3 font-display text-lg">Mastery breakdown</p>
      <div className="flex items-end gap-3">
        {levels.map((level) => {
          const count = distribution[level] ?? 0;
          const heightPct = (count / max) * 100;
          return (
            <div key={level} className="flex flex-1 flex-col items-center gap-1">
              <div className="flex h-24 w-full items-end">
                <div
                  className="w-full rounded-t bg-primary-400/80 transition-all dark:bg-primary-500/70"
                  style={{ height: `${count === 0 ? 2 : heightPct}%` }}
                  aria-label={`${count} words at mastery level ${level}`}
                />
              </div>
              <span className="text-xs text-ink/50 dark:text-ink-dark/50">{level}</span>
            </div>
          );
        })}
      </div>
    </Card>
  );
}
