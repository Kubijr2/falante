import { AnalyticsWidget } from "@/components/analytics/AnalyticsWidget";
import type { AnalyticsSummary, WidgetId } from "@/types/analytics";

interface PinnedWidgetsProps {
  widgetIds: WidgetId[];
  data: AnalyticsSummary;
}

// Split into its own file specifically so it can be lazy-loaded from
// DashboardPage — DashboardPage is the homepage and loads eagerly for every
// visitor, but recharts (pulled in transitively via AnalyticsWidget) is
// only actually needed by someone who's pinned a chart to their dashboard.
export function PinnedWidgets({ widgetIds, data }: PinnedWidgetsProps) {
  return (
    <div className="flex flex-col gap-4 pt-2">
      {widgetIds.map((widgetId) => (
        <AnalyticsWidget key={widgetId} widgetId={widgetId} data={data} />
      ))}
    </div>
  );
}
