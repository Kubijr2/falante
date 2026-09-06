import type { ReactNode } from "react";

import { LoginButton } from "@/components/auth/LoginButton";
import { Card } from "@/components/ui/Card";
import { useAuth } from "@/context/AuthContext";

interface RequireAuthProps {
  children: ReactNode;
  // Shown alongside the login prompt — lets each page explain what
  // logging in unlocks, rather than a generic message everywhere.
  featureName?: string;
}

export function RequireAuth({ children, featureName = "this" }: RequireAuthProps) {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return (
      <div className="h-40 animate-pulse rounded-card border border-border bg-surface/60 dark:border-border-dark dark:bg-surface-dark/60" />
    );
  }

  if (!isAuthenticated) {
    return (
      <Card className="flex flex-col items-center gap-4 py-10 text-center">
        <p className="text-ink/70 dark:text-ink-dark/70">
          Log in to use {featureName} — your data is saved to your account and won't be there
          if you leave and come back without signing in.
        </p>
        <LoginButton />
      </Card>
    );
  }

  return <>{children}</>;
}
