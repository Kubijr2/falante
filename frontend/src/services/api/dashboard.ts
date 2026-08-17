import { apiClient } from "@/services/api/client";
import type { DashboardSummary } from "@/types/vocabulary";

export const dashboardApi = {
  summary: async (): Promise<DashboardSummary> => {
    const { data } = await apiClient.get<DashboardSummary>("/dashboard/summary");
    return data;
  },
};
