import { MasteryTrendChart } from "@/components/analytics/MasteryTrendChart";
import { ReviewActivityHeatmap } from "@/components/analytics/ReviewActivityHeatmap";
import { ReviewQualityChart } from "@/components/analytics/ReviewQualityChart";
import { VocabularyGrowthChart } from "@/components/analytics/VocabularyGrowthChart";
import { WritingInsightsChart } from "@/components/analytics/WritingInsightsChart";
import type { AnalyticsSummary, WidgetId } from "@/types/analytics";

interface AnalyticsWidgetProps {
  widgetId: WidgetId;
  data: AnalyticsSummary;
}

export function AnalyticsWidget({ widgetId, data }: AnalyticsWidgetProps) {
  switch (widgetId) {
    case "vocabulary_growth":
      return <VocabularyGrowthChart data={data.vocabulary_growth} />;
    case "review_activity":
      return <ReviewActivityHeatmap data={data.review_activity} />;
    case "review_quality":
      return <ReviewQualityChart data={data.review_quality} />;
    case "mastery_trend":
      return <MasteryTrendChart data={data.mastery_trend} />;
    case "writing_insights":
      return <WritingInsightsChart data={data.writing_insights} />;
    default:
      return null;
  }
}
