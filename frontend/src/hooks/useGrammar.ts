import { useQuery } from "@tanstack/react-query";

import { grammarApi, type GrammarFilters } from "@/services/api/grammar";

export function useGrammarTopics(filters: GrammarFilters = {}) {
  return useQuery({
    queryKey: ["grammar", "list", filters],
    queryFn: () => grammarApi.list(filters),
  });
}

export function useGrammarCategories() {
  return useQuery({
    queryKey: ["grammar", "categories"],
    queryFn: grammarApi.categories,
  });
}

export function useGrammarTopic(slug: string | undefined) {
  return useQuery({
    queryKey: ["grammar", "detail", slug],
    queryFn: () => grammarApi.getBySlug(slug!),
    enabled: Boolean(slug),
  });
}
