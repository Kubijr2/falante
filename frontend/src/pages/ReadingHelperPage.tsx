import { useState } from "react";

import { HighlightedText } from "@/components/reading/HighlightedText";
import { WordDetailModal } from "@/components/reading/WordDetailModal";
import { useVocabulary } from "@/hooks/useVocabulary";
import type { VerbFormMatch } from "@/types/verb";
import type { Vocabulary } from "@/types/vocabulary";

interface Selected {
  word: string;
  match: Vocabulary | null;
  verbMatch: VerbFormMatch | null;
}

export function ReadingHelperPage() {
  const [text, setText] = useState("");
  const [selected, setSelected] = useState<Selected | null>(null);

  // No filters — we need the full list to check every word in the pasted
  // text against it, not a search-scoped subset.
  const { data: vocabulary = [] } = useVocabulary();

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="font-display text-2xl">Reading Helper</h1>
        <p className="mt-1 text-sm text-ink/60 dark:text-ink-dark/60">
          Paste Portuguese text below. Words already in your Vocabulary — including conjugated
          forms of verbs you've saved — are underlined in green. New words are highlighted in
          gold; tap one to add it.
        </p>
      </div>

      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        rows={6}
        placeholder="Cole um texto em português aqui…"
        className="rounded-lg border border-border bg-surface p-3 text-sm text-ink outline-none dark:border-border-dark dark:bg-surface-dark dark:text-ink-dark"
      />

      <HighlightedText
        text={text}
        vocabulary={vocabulary}
        onWordClick={(word, match, verbMatch) => setSelected({ word, match, verbMatch })}
      />

      <WordDetailModal
        word={selected?.word ?? null}
        match={selected?.match ?? null}
        verbMatch={selected?.verbMatch ?? null}
        onClose={() => setSelected(null)}
      />
    </div>
  );
}
