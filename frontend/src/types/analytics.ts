export type AnalyticsRange = "7d" | "30d" | "90d" | "all";

export interface VocabularyGrowthPoint {
  date: string;
  count: number;
  cumulative: number;
}

export interface ReviewActivityPoint {
  date: string;
  count: number;
}

export interface ReviewQualityPoint {
  date: string;
  again: number;
  hard: number;
  medium: number;
  easy: number;
}

export interface MasteryTrendPoint {
  date: string;
  level_0: number;
  level_1: number;
  level_2: number;
  level_3: number;
  level_4: number;
  level_5: number;
}

export interface WritingInsightPoint {
  date: string;
  grammar: number;
  wording: number;
}

export interface AnalyticsSummary {
  vocabulary_growth: VocabularyGrowthPoint[];
  review_activity: ReviewActivityPoint[];
  review_quality: ReviewQualityPoint[];
  mastery_trend: MasteryTrendPoint[];
  writing_insights: WritingInsightPoint[];
}

export type WidgetId =
  | "vocabulary_growth"
  | "review_activity"
  | "review_quality"
  | "mastery_trend"
  | "writing_insights";

export const WIDGET_LABELS: Record<WidgetId, string> = {
  vocabulary_growth: "Vocabulary Growth",
  review_activity: "Review Activity",
  review_quality: "Review Quality",
  mastery_trend: "Mastery Trend",
  writing_insights: "Writing Insights",
};

export const ALL_WIDGET_IDS: WidgetId[] = [
  "vocabulary_growth",
  "review_activity",
  "review_quality",
  "mastery_trend",
  "writing_insights",
];
