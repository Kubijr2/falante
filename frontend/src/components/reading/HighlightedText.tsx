import { useMemo } from "react";

import { useDebouncedValue } from "@/hooks/useDebouncedValue";
import { useVerbFormLookup } from "@/hooks/useVerbs";
import { isWordToken, tokenizeText } from "@/utils/tokenize";
import type { Vocabulary } from "@/types/vocabulary";
import type { VerbFormMatch } from "@/types/verb";

interface HighlightedTextProps {
  text: string;
  vocabulary: Vocabulary[];
  onWordClick: (word: string, match: Vocabulary | null, verbMatch: VerbFormMatch | null) => void;
}

export function HighlightedText({ text, vocabulary, onWordClick }: HighlightedTextProps) {
  // O(1) lookup per word instead of scanning the vocabulary list per token.
  const knownWords = useMemo(() => {
    const map = new Map<string, Vocabulary>();
    for (const word of vocabulary) {
      map.set(word.portuguese.toLowerCase(), word);
    }
    return map;
  }, [vocabulary]);

  const tokens = useMemo(() => tokenizeText(text), [text]);

  // Every word token that isn't a direct vocabulary match — these are the
  // ones worth checking against the verb-form lookup, since a word that's
  // already known by exact match doesn't need it.
  const uniqueUnknownForms = useMemo(() => {
    const set = new Set<string>();
    for (const token of tokens) {
      if (!isWordToken(token)) continue;
      if (knownWords.has(token.toLowerCase())) continue;
      set.add(token);
    }
    return Array.from(set);
  }, [tokens, knownWords]);

  // Debounced so pasting or typing a long passage doesn't fire a lookup
  // request on every keystroke — only once things settle for a moment.
  const debouncedUnknownForms = useDebouncedValue(uniqueUnknownForms, 400);
  const { data: verbMatches = {} } = useVerbFormLookup(debouncedUnknownForms);

  if (!text.trim()) {
    return (
      <div className="rounded-card border border-dashed border-border p-10 text-center text-ink/60 dark:border-border-dark dark:text-ink-dark/60">
        Paste some Portuguese text above to see it highlighted here.
      </div>
    );
  }

  return (
    <div className="whitespace-pre-wrap rounded-card border border-border bg-surface p-6 leading-relaxed dark:border-border-dark dark:bg-surface-dark">
      {tokens.map((token, i) => {
        if (!isWordToken(token)) {
          return <span key={i}>{token}</span>;
        }

        const directMatch = knownWords.get(token.toLowerCase()) ?? null;
        const verbMatch = verbMatches[token] ?? null;
        // A conjugated form (e.g. "falo") of a verb whose infinitive
        // ("falar") is already saved — treated as known, and clicking it
        // shows the saved infinitive's info, not a separate "falo" entry.
        const impliedMatch =
          !directMatch && verbMatch ? knownWords.get(verbMatch.infinitive.toLowerCase()) ?? null : null;

        const effectiveMatch = directMatch ?? impliedMatch;
        const isKnown = effectiveMatch !== null;

        return (
          <button
            key={i}
            type="button"
            onClick={() => onWordClick(token, effectiveMatch, isKnown ? null : verbMatch)}
            className={`rounded px-0.5 transition-colors ${
              isKnown
                ? "border-b-2 border-primary-400 hover:bg-primary-50 dark:hover:bg-primary-700/20"
                : "border-b-2 border-gold-500 bg-gold-400/10 hover:bg-gold-400/25"
            }`}
          >
            {token}
          </button>
        );
      })}
    </div>
  );
}
