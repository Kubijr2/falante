import { apiClient } from "@/services/api/client";
import type { WritingSubmission } from "@/types/writing";

export const writingApi = {
  review: async (text: string): Promise<WritingSubmission> => {
    const { data } = await apiClient.post<WritingSubmission>("/writing/review", { text });
    return data;
  },

  list: async (): Promise<WritingSubmission[]> => {
    const { data } = await apiClient.get<WritingSubmission[]>("/writing");
    return data;
  },

  get: async (id: number): Promise<WritingSubmission> => {
    const { data } = await apiClient.get<WritingSubmission>(`/writing/${id}`);
    return data;
  },
};
