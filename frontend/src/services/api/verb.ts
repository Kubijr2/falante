import { apiClient } from "@/services/api/client";
import type { VerbDetail, VerbListItem } from "@/types/verb";

export const verbApi = {
  list: async (search?: string): Promise<VerbListItem[]> => {
    const { data } = await apiClient.get<VerbListItem[]>("/verbs", { params: { search } });
    return data;
  },

  getByInfinitive: async (infinitive: string): Promise<VerbDetail> => {
    const { data } = await apiClient.get<VerbDetail>(`/verbs/${infinitive}`);
    return data;
  },
};
