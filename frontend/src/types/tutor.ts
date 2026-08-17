export interface TutorMessage {
  role: "user" | "assistant";
  content: string;
}

export interface TutorRequest {
  question: string;
  topic_slug?: string | null;
  history: TutorMessage[];
}

export interface TutorResponse {
  answer: string;
}

export interface TutorStatus {
  enabled: boolean;
}
