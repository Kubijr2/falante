import type { HTMLAttributes, ReactNode } from "react";

type Tone = "primary" | "gold" | "neutral";

interface BadgeProps extends HTMLAttributes<HTMLSpanElement> {
  tone?: Tone;
  children: ReactNode;
}

const toneClasses: Record<Tone, string> = {
  primary: "bg-primary-50 text-primary-700 dark:bg-primary-700/20 dark:text-primary-100",
  gold: "bg-gold-400/20 text-gold-500",
  neutral: "bg-border/60 text-ink/70 dark:bg-border-dark/60 dark:text-ink-dark/70",
};

export function Badge({ tone = "neutral", className = "", children, ...rest }: BadgeProps) {
  return (
    <span
      className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${toneClasses[tone]} ${className}`}
      {...rest}
    >
      {children}
    </span>
  );
}
