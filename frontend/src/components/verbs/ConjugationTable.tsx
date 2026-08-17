import { PERSON_LABELS } from "@/types/verb";

interface ConjugationTableProps {
  forms: string[];
}

export function ConjugationTable({ forms }: ConjugationTableProps) {
  return (
    <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
      {forms.map((form, i) => (
        <div
          key={PERSON_LABELS[i]}
          className="rounded-card border border-border bg-surface p-4 text-center dark:border-border-dark dark:bg-surface-dark"
        >
          <p className="text-xs uppercase tracking-wide text-ink/50 dark:text-ink-dark/50">
            {PERSON_LABELS[i]}
          </p>
          <p className="mt-1 font-display text-lg text-primary-700 dark:text-primary-100">
            {form}
          </p>
        </div>
      ))}
    </div>
  );
}
