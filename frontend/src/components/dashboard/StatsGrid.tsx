import { Card } from "@/components/ui/Card";

interface StatsGridProps {
  totalWords: number;
  dueToday: number;
  totalReviews: number;
}

function Stat({ label, value }: { label: string; value: number }) {
  return (
    <Card className="text-center">
      <p className="font-display text-3xl text-primary-600 dark:text-primary-400">{value}</p>
      <p className="mt-1 text-sm text-ink/60 dark:text-ink-dark/60">{label}</p>
    </Card>
  );
}

export function StatsGrid({ totalWords, dueToday, totalReviews }: StatsGridProps) {
  return (
    <div className="grid grid-cols-3 gap-4">
      <Stat label="Words saved" value={totalWords} />
      <Stat label="Due today" value={dueToday} />
      <Stat label="Total reviews" value={totalReviews} />
    </div>
  );
}
