import type { ReactNode } from "react";
import { NavLink } from "react-router-dom";

const navLinkClass = ({ isActive }: { isActive: boolean }) =>
  `rounded-full px-4 py-1.5 text-sm font-medium transition-colors ${
    isActive
      ? "bg-primary-500 text-white"
      : "text-ink/70 hover:bg-primary-50 dark:text-ink-dark/70 dark:hover:bg-primary-700/20"
  }`;

export function Layout({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-screen bg-base dark:bg-base-dark">
      <header className="border-b border-border dark:border-border-dark">
        <div className="mx-auto flex max-w-5xl items-center justify-between px-6 py-4">
          <span className="font-display text-xl text-primary-600 dark:text-primary-400">
            Falante
          </span>
          <nav className="flex gap-2">
            <NavLink to="/" end className={navLinkClass}>
              Dashboard
            </NavLink>
            <NavLink to="/vocabulary" className={navLinkClass}>
              Vocabulary
            </NavLink>
            <NavLink to="/flashcards" className={navLinkClass}>
              Flashcards
            </NavLink>
            <NavLink to="/grammar" className={navLinkClass}>
              Grammar
            </NavLink>
            <NavLink to="/verbs" className={navLinkClass}>
              Verbs
            </NavLink>
          </nav>
        </div>
      </header>
      <main className="mx-auto max-w-5xl px-6 py-8">{children}</main>
    </div>
  );
}
