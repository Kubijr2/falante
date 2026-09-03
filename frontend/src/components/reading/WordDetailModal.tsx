import { useState } from "react";

import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Modal } from "@/components/ui/Modal";
import { useCreateVocabulary } from "@/hooks/useVocabulary";
import type { VerbFormMatch } from "@/types/verb";
import type { Vocabulary } from "@/types/vocabulary";

interface WordDetailModalProps {
  word: string | null;
  match: Vocabulary | null;
  verbMatch: VerbFormMatch | null;
  onClose: () => void;
}

export function WordDetailModal({ word, match, verbMatch, onClose }: WordDetailModalProps) {
  const [english, setEnglish] = useState("");
  const createMutation = useCreateVocabulary();

  const isOpen = word !== null;

  function handleClose() {
    setEnglish("");
    createMutation.reset();
    onClose();
  }

  // Used for the plain "not a recognized verb" manual-entry case — saves
  // exactly the word as typed.
  function handleSaveAsIs() {
    if (!word || !english.trim()) return;
    createMutation.mutate(
      { portuguese: word, english: english.trim(), tags: ["from reading"], difficulty: "medium" },
      { onSuccess: handleClose }
    );
  }

  // Used when the word is a recognized conjugated form of a verb — saves
  // the infinitive, not the literal form encountered, so it groups with
  // any other conjugated form of the same verb instead of creating a
  // separate vocabulary entry per form.
  function handleSaveInfinitive() {
    if (!verbMatch) return;
    const translation = english.trim() || verbMatch.translation;
    createMutation.mutate(
      {
        portuguese: verbMatch.infinitive,
        english: translation,
        tags: ["from reading", "verb"],
        difficulty: "medium",
      },
      { onSuccess: handleClose }
    );
  }

  if (!word) return null;

  return (
    <Modal isOpen={isOpen} onClose={handleClose}>
      {match ? (
        // Known word — read-only view of what's already saved. If the
        // clicked word differs from what's saved (e.g. clicked "falo",
        // saved word is "falar"), say so, since otherwise it'd look like a
        // mismatch rather than the intended grouping behavior.
        <div className="flex flex-col gap-3">
          <div className="flex items-center justify-between">
            <h3 className="font-display text-xl">{match.portuguese}</h3>
            <Badge tone="primary">Level {match.mastery_level}</Badge>
          </div>
          {word.toLowerCase() !== match.portuguese.toLowerCase() && (
            <p className="text-xs text-ink/50 dark:text-ink-dark/50">
              "{word}" is a conjugated form of "{match.portuguese}", which you've already saved.
            </p>
          )}
          <p className="text-ink/80 dark:text-ink-dark/80">{match.english}</p>
          {match.example_sentence && (
            <p className="text-sm italic text-ink/60 dark:text-ink-dark/60">
              "{match.example_sentence}"
            </p>
          )}
          {match.notes && (
            <p className="text-sm text-ink/60 dark:text-ink-dark/60">{match.notes}</p>
          )}
          <div className="flex justify-end pt-2">
            <Button variant="secondary" onClick={handleClose}>
              Close
            </Button>
          </div>
        </div>
      ) : verbMatch ? (
        // Unknown, but recognized as a conjugated form of a verb — offer to
        // save the infinitive (pre-filled translation, still editable)
        // rather than the literal form encountered.
        <div className="flex flex-col gap-4">
          <div>
            <h3 className="font-display text-xl">{word}</h3>
            <p className="mt-1 text-sm text-ink/60 dark:text-ink-dark/60">
              This looks like a form of <span className="font-medium">{verbMatch.infinitive}</span> (
              {verbMatch.translation}).
            </p>
          </div>
          <Input
            label={`English translation for "${verbMatch.infinitive}"`}
            placeholder={verbMatch.translation}
            value={english}
            onChange={(e) => setEnglish(e.target.value)}
            autoFocus
          />
          {createMutation.isError && (
            <p className="text-sm text-red-600">Couldn't save that — try again.</p>
          )}
          <div className="flex justify-end gap-2 pt-2">
            <Button variant="ghost" onClick={handleClose}>
              Cancel
            </Button>
            <Button onClick={handleSaveInfinitive} disabled={createMutation.isPending}>
              {createMutation.isPending
                ? "Saving…"
                : `Save "${verbMatch.infinitive}" to vocabulary`}
            </Button>
          </div>
        </div>
      ) : (
        // Plain unknown word — quick manual-translation save form.
        <div className="flex flex-col gap-4">
          <h3 className="font-display text-xl">{word}</h3>
          <Input
            label="English translation"
            placeholder="What does this mean?"
            value={english}
            onChange={(e) => setEnglish(e.target.value)}
            autoFocus
          />
          {createMutation.isError && (
            <p className="text-sm text-red-600">Couldn't save that — try again.</p>
          )}
          <div className="flex justify-end gap-2 pt-2">
            <Button variant="ghost" onClick={handleClose}>
              Cancel
            </Button>
            <Button
              onClick={handleSaveAsIs}
              disabled={!english.trim() || createMutation.isPending}
            >
              {createMutation.isPending ? "Saving…" : "Save to vocabulary"}
            </Button>
          </div>
        </div>
      )}
    </Modal>
  );
}
