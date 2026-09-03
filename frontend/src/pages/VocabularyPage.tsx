import { useMemo, useState } from "react";

import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { VocabularyForm } from "@/components/vocabulary/VocabularyForm";
import { VocabularyList } from "@/components/vocabulary/VocabularyList";
import { useCreateVocabulary, useDeleteVocabulary, useVocabulary } from "@/hooks/useVocabulary";
import { useVerbs } from "@/hooks/useVerbs";

export function VocabularyPage() {
  const [search, setSearch] = useState("");
  const [isFormOpen, setIsFormOpen] = useState(false);

  const { data: words = [], isLoading } = useVocabulary({ search: search || undefined });
  // No search filter — this is for cross-referencing every vocabulary word
  // against the full verb list, not for a verb search UI.
  const { data: verbs = [] } = useVerbs();
  const createMutation = useCreateVocabulary();
  const deleteMutation = useDeleteVocabulary();

  const verbsByInfinitive = useMemo(() => {
    const map = new Map();
    for (const verb of verbs) {
      map.set(verb.infinitive.toLowerCase(), verb);
    }
    return map;
  }, [verbs]);

  return (
    <div className="flex flex-col gap-6">
      <div className="flex items-center justify-between gap-4">
        <h1 className="font-display text-2xl">Vocabulary</h1>
        <Button onClick={() => setIsFormOpen((prev) => !prev)}>
          {isFormOpen ? "Close" : "+ Add word"}
        </Button>
      </div>

      {isFormOpen && (
        <div className="rounded-card border border-border bg-surface p-5 dark:border-border-dark dark:bg-surface-dark">
          <VocabularyForm
            isSubmitting={createMutation.isPending}
            onCancel={() => setIsFormOpen(false)}
            onSubmit={(input) => {
              createMutation.mutate(input, {
                onSuccess: () => setIsFormOpen(false),
              });
            }}
          />
        </div>
      )}

      <Input
        label="Search"
        placeholder="Search Portuguese or English…"
        value={search}
        onChange={(e) => setSearch(e.target.value)}
      />

      <VocabularyList
        words={words}
        isLoading={isLoading}
        onDelete={(id) => deleteMutation.mutate(id)}
        verbsByInfinitive={verbsByInfinitive}
      />
    </div>
  );
}
