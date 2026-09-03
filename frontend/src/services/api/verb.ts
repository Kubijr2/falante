import { apiClient } from "@/services/api/client";
import type { VerbDetail, VerbFormMatch, VerbListItem } from "@/types/verb";

export const verbApi = {
  list: async (search?: string): Promise<VerbListItem[]> => {
    const { data } = await apiClient.get<VerbListItem[]>("/verbs", { params: { search } });
    return data;
  },

  getByInfinitive: async (infinitive: string): Promise<VerbDetail> => {
    const { data } = await apiClient.get<VerbDetail>(`/verbs/${infinitive}`);
    return data;
  },

  lookupBatch: async (forms: string[]): Promise<Record<string, VerbFormMatch>> => {
    if (forms.length === 0) return {};
    const { data } = await apiClient.post<{ matches: Record<string, VerbFormMatch> }>(
      "/verbs/lookup-batch",
      { forms }
    );
    return data.matches;
  },
};
