interface CategoryFilterProps {
  categories: string[];
  selected: string | null;
  onSelect: (category: string | null) => void;
}

export function CategoryFilter({ categories, selected, onSelect }: CategoryFilterProps) {
  return (
    <div className="flex flex-wrap gap-2">
      <button
        type="button"
        onClick={() => onSelect(null)}
        className={`rounded-full px-3 py-1 text-sm font-medium transition-colors ${
          selected === null
            ? "bg-primary-500 text-white"
            : "bg-border/50 text-ink/70 hover:bg-primary-50 dark:bg-border-dark/50 dark:text-ink-dark/70"
        }`}
      >
        All
      </button>
      {categories.map((category) => (
        <button
          key={category}
          type="button"
          onClick={() => onSelect(category)}
          className={`rounded-full px-3 py-1 text-sm font-medium transition-colors ${
            selected === category
              ? "bg-primary-500 text-white"
              : "bg-border/50 text-ink/70 hover:bg-primary-50 dark:bg-border-dark/50 dark:text-ink-dark/70"
          }`}
        >
          {category}
        </button>
      ))}
    </div>
  );
}
