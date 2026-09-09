import { apiClient } from "@/services/api/client";
import type { StudyAssistantAskResponse, StudyAssistantMessage } from "@/types/studyAssistant";

export const studyAssistantApi = {
  getHistory: async (): Promise<StudyAssistantMessage[]> => {
    const { data } = await apiClient.get<StudyAssistantMessage[]>("/study-assistant");
    return data;
  },

  sendMessage: async (message: string): Promise<StudyAssistantAskResponse> => {
    const { data } = await apiClient.post<StudyAssistantAskResponse>("/study-assistant/message", {
      message,
    });
    return data;
  },

  clearHistory: async (): Promise<void> => {
    await apiClient.delete("/study-assistant");
  },
};
