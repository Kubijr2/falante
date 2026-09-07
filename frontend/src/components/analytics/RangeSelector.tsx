import type { AnalyticsRange } from "@/types/analytics";

interface RangeSelectorProps {
  value: AnalyticsRange;
  onChange: (range: AnalyticsRange) => void;
}

const OPTIONS: { value: AnalyticsRange; label: string }[] = [
  { value: "7d", label: "7 days" },
  { value: "30d", label: "30 days" },
  { value: "90d", label: "90 days" },
  { value: "all", label: "All time" },
];

export function RangeSelector({ value, onChange }: RangeSelectorProps) {
  return (
    <div className="flex gap-2">
      {OPTIONS.map((option) => (
        <button
          key={option.value}
          type="button"
          onClick={() => onChange(option.value)}
          className={`rounded-full px-3 py-1.5 text-sm font-medium transition-colors ${
            value === option.value
              ? "bg-primary-500 text-white"
              : "bg-border/50 text-ink/70 hover:bg-primary-50 dark:bg-border-dark/50 dark:text-ink-dark/70"
          }`}
        >
          {option.label}
        </button>
      ))}
    </div>
  );
}
