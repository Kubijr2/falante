import { MasteryBreakdown } from "@/components/dashboard/MasteryBreakdown";
import { QuickActions } from "@/components/dashboard/QuickActions";
import { RecentlyLearned } from "@/components/dashboard/RecentlyLearned";
import { StatsGrid } from "@/components/dashboard/StatsGrid";
import { StreakCard } from "@/components/dashboard/StreakCard";
import { useDashboard } from "@/hooks/useDashboard";

export function DashboardPage() {
  const { data, isLoading, isError } = useDashboard();

  if (isLoading) {
    return (
      <div className="flex flex-col gap-4">
        {Array.from({ length: 3 }).map((_, i) => (
          <div
            key={i}
            className="h-24 animate-pulse rounded-card border border-border bg-surface/60 dark:border-border-dark dark:bg-surface-dark/60"
          />
        ))}
      </div>
    );
  }

  if (isError || !data) {
    return (
      <p className="text-center text-ink/60 dark:text-ink-dark/60">
        Couldn't load your dashboard. Is the backend running?
      </p>
    );
  }

  return (
    <div className="flex flex-col gap-6">
      <div className="flex items-center justify-between">
        <h1 className="font-display text-2xl">Dashboard</h1>
        <QuickActions dueToday={data.due_today} />
      </div>

      <StreakCard streak={data.streak} />
      <StatsGrid
        totalWords={data.total_words}
        dueToday={data.due_today}
        totalReviews={data.total_reviews}
      />

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        <MasteryBreakdown distribution={data.mastery_distribution} />
        <RecentlyLearned words={data.recently_learned} />
      </div>
    </div>
  );
}
