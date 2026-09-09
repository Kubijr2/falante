export interface StudyAssistantMessage {
  id: number;
  role: "user" | "assistant";
  content: string;
  created_at: string;
}

export interface StudyAssistantAskResponse {
  reply: string;
}
