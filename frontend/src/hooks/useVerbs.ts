import { useQuery } from "@tanstack/react-query";

import { verbApi } from "@/services/api/verb";
import type { VerbFormMatch } from "@/types/verb";

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

/**
 * Batch reverse-lookup for a set of raw word forms — "is this word a
 * conjugated form of a verb, and if so, what's its infinitive?" `forms`
 * should already be deduplicated and (ideally) debounced by the caller;
 * this hook just turns it into a cached query keyed on the exact set asked
 * for, so re-analyzing the same passage doesn't refetch.
 */
export function useVerbFormLookup(forms: string[]) {
  // Sorted + joined so the query key is stable regardless of the order
  // tokens were discovered in the text.
  const key = [...forms].sort().join("|");

  return useQuery<Record<string, VerbFormMatch>>({
    queryKey: ["verbs", "lookup-batch", key],
    queryFn: () => verbApi.lookupBatch(forms),
    enabled: forms.length > 0,
  });
}
