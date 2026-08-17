interface MasteryDotsProps {
  level: number; // 0-5
}

export function MasteryDots({ level }: MasteryDotsProps) {
  return (
    <div className="flex items-center gap-1" aria-label={`Mastery level ${level} of 5`}>
      {Array.from({ length: 5 }).map((_, i) => (
        <span
          key={i}
          className={`h-1.5 w-1.5 rounded-full ${
            i < level ? "bg-gold-500" : "bg-border dark:bg-border-dark"
          }`}
        />
      ))}
    </div>
  );
}
