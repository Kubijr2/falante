import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { writingApi } from "@/services/api/writing";

export function useWritingHistory() {
  return useQuery({
    queryKey: ["writing", "history"],
    queryFn: writingApi.list,
  });
}

export function useWritingSubmission(id: number | undefined) {
  return useQuery({
    queryKey: ["writing", "detail", id],
    queryFn: () => writingApi.get(id!),
    enabled: id !== undefined,
  });
}

export function useReviewWriting() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (text: string) => writingApi.review(text),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["writing", "history"] });
    },
  });
}
