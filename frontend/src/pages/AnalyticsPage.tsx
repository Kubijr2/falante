import { useState } from "react";

import { AnalyticsWidget } from "@/components/analytics/AnalyticsWidget";
import { RangeSelector } from "@/components/analytics/RangeSelector";
import { useAnalytics } from "@/hooks/useAnalytics";
import { ALL_WIDGET_IDS, type AnalyticsRange } from "@/types/analytics";

export function AnalyticsPage() {
  const [range, setRange] = useState<AnalyticsRange>("30d");
  const { data, isLoading, isError } = useAnalytics(range);

  return (
    <div className="flex flex-col gap-6">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <h1 className="font-display text-2xl">Analytics</h1>
        <RangeSelector value={range} onChange={setRange} />
      </div>

      {isLoading && (
        <div className="flex flex-col gap-4">
          {Array.from({ length: 3 }).map((_, i) => (
            <div
              key={i}
              className="h-48 animate-pulse rounded-card border border-border bg-surface/60 dark:border-border-dark dark:bg-surface-dark/60"
            />
          ))}
        </div>
      )}

      {isError && (
        <p className="text-center text-ink/60 dark:text-ink-dark/60">
          Couldn't load your analytics. Is the backend running?
        </p>
      )}

      {data && (
        <div className="flex flex-col gap-4">
          {ALL_WIDGET_IDS.map((widgetId) => (
            <AnalyticsWidget key={widgetId} widgetId={widgetId} data={data} />
          ))}
        </div>
      )}
    </div>
  );
}
