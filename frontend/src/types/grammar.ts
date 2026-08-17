export interface GrammarTopicListItem {
  id: number;
  slug: string;
  title: string;
  category: string;
  summary: string;
}

export interface GrammarTopicDetail extends GrammarTopicListItem {
  content: string;
  created_at: string;
  updated_at: string;
}
