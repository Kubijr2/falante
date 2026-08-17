import { apiClient } from "@/services/api/client";
import type {
  ReviewResult,
  Vocabulary,
  VocabularyCreateInput,
  VocabularyUpdateInput,
} from "@/types/vocabulary";

export interface VocabularyFilters {
  category?: string;
  search?: string;
}

export const vocabularyApi = {
  list: async (filters: VocabularyFilters = {}): Promise<Vocabulary[]> => {
    const { data } = await apiClient.get<Vocabulary[]>("/vocabulary", { params: filters });
    return data;
  },

  create: async (input: VocabularyCreateInput): Promise<Vocabulary> => {
    const { data } = await apiClient.post<Vocabulary>("/vocabulary", input);
    return data;
  },

  update: async (id: number, input: VocabularyUpdateInput): Promise<Vocabulary> => {
    const { data } = await apiClient.patch<Vocabulary>(`/vocabulary/${id}`, input);
    return data;
  },

  remove: async (id: number): Promise<void> => {
    await apiClient.delete(`/vocabulary/${id}`);
  },

  dueFlashcards: async (): Promise<Vocabulary[]> => {
    const { data } = await apiClient.get<Vocabulary[]>("/flashcards/due");
    return data;
  },

  submitReview: async (id: number, result: ReviewResult): Promise<Vocabulary> => {
    const { data } = await apiClient.post<Vocabulary>(`/flashcards/${id}/review`, { result });
    return data;
  },
};
