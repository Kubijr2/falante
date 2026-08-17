import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { vocabularyApi, type VocabularyFilters } from "@/services/api/vocabulary";
import type { VocabularyCreateInput, VocabularyUpdateInput } from "@/types/vocabulary";

const vocabularyKey = (filters: VocabularyFilters) => ["vocabulary", filters] as const;

export function useVocabulary(filters: VocabularyFilters = {}) {
  return useQuery({
    queryKey: vocabularyKey(filters),
    queryFn: () => vocabularyApi.list(filters),
  });
}

export function useCreateVocabulary() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (input: VocabularyCreateInput) => vocabularyApi.create(input),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["vocabulary"] });
    },
  });
}

export function useUpdateVocabulary() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, input }: { id: number; input: VocabularyUpdateInput }) =>
      vocabularyApi.update(id, input),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["vocabulary"] });
    },
  });
}

export function useDeleteVocabulary() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => vocabularyApi.remove(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["vocabulary"] });
    },
  });
}
