import { useQuery } from "@tanstack/react-query";

import { apiClient } from "@/services/api/client";

interface DashboardSummary {
  streak: number;
  total_words: number;
  due_today: number;
  total_reviews: number;
  mastery_distribution: Record<number, number>;
  recently_learned: {
    id: number;
    portuguese: string;
    english: string;
    mastery_level: number;
  }[];
}

export function useDashboard() {
  return useQuery({
    queryKey: ["dashboard", "summary"],
    queryFn: async () => {
      const { data } = await apiClient.get<DashboardSummary>("/dashboard/summary");
      return data;
    },
  });
}
