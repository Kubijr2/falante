import { apiClient } from "@/services/api/client";
import type { TutorMessage, TutorResponse, TutorStatus } from "@/types/tutor";

export const tutorApi = {
  status: async (): Promise<TutorStatus> => {
    const { data } = await apiClient.get<TutorStatus>("/tutor/status");
    return data;
  },

  ask: async (
    question: string,
    history: TutorMessage[],
    topicSlug?: string | null
  ): Promise<TutorResponse> => {
    const { data } = await apiClient.post<TutorResponse>("/tutor/ask", {
      question,
      topic_slug: topicSlug ?? null,
      history,
    });
    return data;
  },
};
