import { LoginButton } from "@/components/auth/LoginButton";
import { Badge } from "@/components/ui/Badge";
import { MasteryBreakdown } from "@/components/dashboard/MasteryBreakdown";
import { QuickActions } from "@/components/dashboard/QuickActions";
import { RecentlyLearned } from "@/components/dashboard/RecentlyLearned";
import { StatsGrid } from "@/components/dashboard/StatsGrid";
import { StreakCard } from "@/components/dashboard/StreakCard";
import { useAuth } from "@/context/AuthContext";
import { useDashboard } from "@/hooks/useDashboard";

// Deliberately flavorful example words (not "word1, word2") — this doubles
// as a small, honest preview of what saving real vocabulary looks like.
const EXAMPLE_DATA = {
  streak: 12,
  total_words: 87,
  due_today: 5,
  total_reviews: 243,
  mastery_distribution: { 0: 10, 1: 15, 2: 20, 3: 18, 4: 14, 5: 10 },
  recently_learned: [
    { id: 1, portuguese: "saudade", english: "a deep, wistful longing", mastery_level: 3 },
    { id: 2, portuguese: "cafezinho", english: "a little coffee — a daily ritual", mastery_level: 2 },
    { id: 3, portuguese: "jeitinho", english: "a clever, informal workaround", mastery_level: 4 },
  ],
};

function PublicHome() {
  return (
    <div className="flex flex-col gap-10">
      <div className="flex flex-col items-center gap-4 py-6 text-center">
        <h1 className="font-display text-3xl">Learn Brazilian Portuguese with Falante</h1>
        <p className="max-w-xl text-ink/70 dark:text-ink-dark/70">
          Vocabulary with real spaced repetition, a conjugation engine covering 85 verbs,
          grammar articles that explain the "why" instead of just the rule, an AI tutor and
          writing coach, and a reading helper that recognizes verb forms — not just exact word
          matches.
        </p>
        <LoginButton />
      </div>

      <div>
        <div className="mb-3 flex flex-wrap items-center gap-2">
          <h2 className="font-display text-xl">Example dashboard</h2>
          <Badge tone="gold">Sample data — sign in to see your own</Badge>
        </div>
        <div className="flex flex-col gap-6 opacity-90">
          <StreakCard streak={EXAMPLE_DATA.streak} />
          <StatsGrid
            totalWords={EXAMPLE_DATA.total_words}
            dueToday={EXAMPLE_DATA.due_today}
            totalReviews={EXAMPLE_DATA.total_reviews}
          />
          <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
            <MasteryBreakdown distribution={EXAMPLE_DATA.mastery_distribution} />
            <RecentlyLearned words={EXAMPLE_DATA.recently_learned} />
          </div>
        </div>
      </div>
    </div>
  );
}

function PersonalDashboard() {
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

export function DashboardPage() {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return (
      <div className="h-40 animate-pulse rounded-card border border-border bg-surface/60 dark:border-border-dark dark:bg-surface-dark/60" />
    );
  }

  return isAuthenticated ? <PersonalDashboard /> : <PublicHome />;
}
