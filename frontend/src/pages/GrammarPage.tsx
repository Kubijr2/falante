import { useState } from "react";

import { CategoryFilter } from "@/components/grammar/CategoryFilter";
import { GrammarTopicList } from "@/components/grammar/GrammarTopicList";
import { Input } from "@/components/ui/Input";
import { useGrammarCategories, useGrammarTopics } from "@/hooks/useGrammar";

export function GrammarPage() {
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState<string | null>(null);

  const { data: categories = [] } = useGrammarCategories();
  const { data: topics = [], isLoading } = useGrammarTopics({
    search: search || undefined,
    category: category ?? undefined,
  });

  return (
    <div className="flex flex-col gap-6">
      <h1 className="font-display text-2xl">Grammar Reference</h1>

      <Input
        label="Search"
        placeholder="Search grammar topics…"
        value={search}
        onChange={(e) => setSearch(e.target.value)}
      />

      <CategoryFilter categories={categories} selected={category} onSelect={setCategory} />

      <GrammarTopicList topics={topics} isLoading={isLoading} />
    </div>
  );
}
