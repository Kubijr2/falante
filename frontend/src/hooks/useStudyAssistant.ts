import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { studyAssistantApi } from "@/services/api/studyAssistant";

const QUERY_KEY = ["study-assistant", "history"];

export function useStudyAssistantHistory(enabled: boolean) {
  return useQuery({
    queryKey: QUERY_KEY,
    queryFn: studyAssistantApi.getHistory,
    enabled,
  });
}

export function useSendStudyAssistantMessage() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: studyAssistantApi.sendMessage,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: QUERY_KEY });
    },
  });
}

export function useClearStudyAssistant() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: studyAssistantApi.clearHistory,
    onSuccess: () => {
      queryClient.setQueryData(QUERY_KEY, []);
    },
  });
}
