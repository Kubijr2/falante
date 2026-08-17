import { useQuery } from "@tanstack/react-query";

import { dashboardApi } from "@/services/api/dashboard";

export function useDashboard() {
  return useQuery({
    queryKey: ["dashboard", "summary"],
    queryFn: dashboardApi.summary,
  });
}
