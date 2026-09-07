import { Card } from "@/components/ui/Card";
import type { ReviewActivityPoint } from "@/types/analytics";

interface ReviewActivityHeatmapProps {
  data: ReviewActivityPoint[];
}

// Not a stock recharts chart type — GitHub-style contribution grids are
// simple enough to hand-roll as a grid of colored cells rather than pull in
// a dedicated heatmap library for one component.
function intensityClass(count: number, max: number): string {
  if (count === 0) return "bg-border/40 dark:bg-border-dark/40";
  const ratio = count / max;
  if (ratio > 0.75) return "bg-primary-600";
  if (ratio > 0.5) return "bg-primary-500";
  if (ratio > 0.25) return "bg-primary-400";
  return "bg-primary-100 dark:bg-primary-700/40";
}

export function ReviewActivityHeatmap({ data }: ReviewActivityHeatmapProps) {
  const max = Math.max(1, ...data.map((d) => d.count));

  return (
    <Card>
      <p className="mb-3 font-display text-lg">Review Activity</p>
      {data.length === 0 ? (
        <p className="text-sm text-ink/60 dark:text-ink-dark/60">
          Review a flashcard to start building your activity history.
        </p>
      ) : (
        <div className="flex flex-wrap gap-1">
          {data.map((point) => (
            <div
              key={point.date}
              title={`${point.date}: ${point.count} review${point.count === 1 ? "" : "s"}`}
              className={`h-4 w-4 rounded-sm ${intensityClass(point.count, max)}`}
            />
          ))}
        </div>
      )}
    </Card>
  );
}
