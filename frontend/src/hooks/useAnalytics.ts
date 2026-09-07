import { useQuery } from "@tanstack/react-query";

import { analyticsApi } from "@/services/api/analytics";
import type { AnalyticsRange } from "@/types/analytics";

export function useAnalytics(range: AnalyticsRange, enabled: boolean = true) {
  return useQuery({
    queryKey: ["analytics", "summary", range],
    queryFn: () => analyticsApi.getSummary(range),
    enabled,
  });
}
