import { useQuery } from "@tanstack/react-query";

import { verbApi } from "@/services/api/verb";

export function useVerbs(search?: string) {
  return useQuery({
    queryKey: ["verbs", "list", search],
    queryFn: () => verbApi.list(search),
  });
}

export function useVerbDetail(infinitive: string | undefined) {
  return useQuery({
    queryKey: ["verbs", "detail", infinitive],
    queryFn: () => verbApi.getByInfinitive(infinitive!),
    enabled: Boolean(infinitive),
  });
}
