import { apiClient } from "@/services/api/client";
import type { GrammarTopicDetail, GrammarTopicListItem } from "@/types/grammar";

export interface GrammarFilters {
  category?: string;
  search?: string;
}

export const grammarApi = {
  list: async (filters: GrammarFilters = {}): Promise<GrammarTopicListItem[]> => {
    const { data } = await apiClient.get<GrammarTopicListItem[]>("/grammar", { params: filters });
    return data;
  },

  categories: async (): Promise<string[]> => {
    const { data } = await apiClient.get<string[]>("/grammar/categories");
    return data;
  },

  getBySlug: async (slug: string): Promise<GrammarTopicDetail> => {
    const { data } = await apiClient.get<GrammarTopicDetail>(`/grammar/${slug}`);
    return data;
  },
};
