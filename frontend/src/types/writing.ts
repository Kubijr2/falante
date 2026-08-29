export type CorrectionType = "grammar" | "wording";

export interface Correction {
  type: CorrectionType;
  original: string;
  corrected: string;
  explanation: string;
}

export interface VocabularySuggestion {
  portuguese: string;
  english: string;
  reason: string;
}

export interface WritingSubmission {
  id: number;
  original_text: string;
  overall_feedback: string;
  corrections: Correction[];
  vocabulary_suggestions: VocabularySuggestion[];
  created_at: string;
}
