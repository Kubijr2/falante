import type { HTMLAttributes, ReactNode } from "react";

interface CardProps extends HTMLAttributes<HTMLDivElement> {
  children: ReactNode;
}

export function Card({ className = "", children, ...rest }: CardProps) {
  return (
    <div
      className={`rounded-card border border-border bg-surface p-5 shadow-sm dark:border-border-dark dark:bg-surface-dark ${className}`}
      {...rest}
    >
      {children}
    </div>
  );
}
