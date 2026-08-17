import { Card } from "@/components/ui/Card";

interface StreakCardProps {
  streak: number;
}

export function StreakCard({ streak }: StreakCardProps) {
  const message =
    streak === 0
      ? "Review a card today to start a streak"
      : `${streak} day${streak === 1 ? "" : "s"} in a row — keep it going`;

  return (
    <Card className="flex items-center gap-4 bg-gradient-to-br from-primary-50 to-surface dark:from-primary-700/20 dark:to-surface-dark">
      <div className="flex h-14 w-14 shrink-0 items-center justify-center rounded-full bg-gold-400/20 text-2xl font-display text-gold-500">
        {streak}
      </div>
      <div>
        <p className="font-display text-lg">Study streak</p>
        <p className="text-sm text-ink/60 dark:text-ink-dark/60">{message}</p>
      </div>
    </Card>
  );
}
