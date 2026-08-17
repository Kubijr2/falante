import type { ButtonHTMLAttributes, ReactNode } from "react";

type Variant = "primary" | "secondary" | "ghost" | "danger";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: Variant;
  children: ReactNode;
}

const variantClasses: Record<Variant, string> = {
  primary: "bg-primary-500 text-white hover:bg-primary-600",
  secondary:
    "bg-surface dark:bg-surface-dark border border-border dark:border-border-dark text-ink dark:text-ink-dark hover:bg-primary-50 dark:hover:bg-primary-700/20",
  ghost: "text-ink dark:text-ink-dark hover:bg-primary-50 dark:hover:bg-primary-700/20",
  danger: "bg-white text-red-600 border border-red-200 hover:bg-red-50",
};

export function Button({ variant = "primary", className = "", children, ...rest }: ButtonProps) {
  return (
    <button
      className={`inline-flex items-center justify-center gap-2 rounded-full px-4 py-2 text-sm font-medium transition-colors disabled:cursor-not-allowed disabled:opacity-50 ${variantClasses[variant]} ${className}`}
      {...rest}
    >
      {children}
    </button>
  );
}
