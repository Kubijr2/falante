import { useState } from "react";

import { ConjugationTable } from "@/components/verbs/ConjugationTable";
import { TENSE_LABELS, TENSE_ORDER, type TenseKey, type VerbDetail } from "@/types/verb";

interface TenseTabsProps {
  conjugations: VerbDetail["conjugations"];
}

export function TenseTabs({ conjugations }: TenseTabsProps) {
  const [activeTense, setActiveTense] = useState<TenseKey>("present");

  return (
    <div className="flex flex-col gap-4">
      <div className="flex flex-wrap gap-2">
        {TENSE_ORDER.map((tense) => (
          <button
            key={tense}
            type="button"
            onClick={() => setActiveTense(tense)}
            className={`rounded-full px-3 py-1.5 text-sm font-medium transition-colors ${
              activeTense === tense
                ? "bg-primary-500 text-white"
                : "bg-border/50 text-ink/70 hover:bg-primary-50 dark:bg-border-dark/50 dark:text-ink-dark/70"
            }`}
          >
            {TENSE_LABELS[tense]}
          </button>
        ))}
      </div>
      <ConjugationTable forms={conjugations[activeTense]} />
    </div>
  );
}
