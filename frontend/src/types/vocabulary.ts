export type Difficulty = "easy" | "medium" | "hard";

export interface Vocabulary {
  id: number;
  portuguese: string;
  english: string;
  example_sentence: string | null;
  notes: string | null;
  category: string | null;
  tags: string[];
  difficulty: Difficulty;
  mastery_level: number;
  next_review_at: string;
  created_at: string;
  updated_at: string;
}

export interface VocabularyCreateInput {
  portuguese: string;
  english: string;
  example_sentence?: string;
  notes?: string;
  category?: string;
  tags: string[];
  difficulty: Difficulty;
}

export type VocabularyUpdateInput = Partial<VocabularyCreateInput>;

export type ReviewResult = "again" | "hard" | "medium" | "easy";

export interface DashboardSummary {
  streak: number;
  total_words: number;
  due_today: number;
  total_reviews: number;
  mastery_distribution: Record<number, number>;
  recently_learned: Vocabulary[];
}

