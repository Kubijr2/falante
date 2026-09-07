import { apiClient } from "@/services/api/client";
import type { AnalyticsRange, AnalyticsSummary } from "@/types/analytics";

export const analyticsApi = {
  getSummary: async (range: AnalyticsRange): Promise<AnalyticsSummary> => {
    const { data } = await apiClient.get<AnalyticsSummary>("/analytics/summary", {
      params: { range },
    });
    return data;
  },
};
