import { LoginButton } from "@/components/auth/LoginButton";
import { Button } from "@/components/ui/Button";
import { useAuth } from "@/context/AuthContext";

export function UserMenu() {
  const { user, isAuthenticated, isLoading, logout } = useAuth();

  if (isLoading) {
    return <div className="h-8 w-20 animate-pulse rounded-full bg-border/50" />;
  }

  if (!isAuthenticated || !user) {
    return <LoginButton />;
  }

  return (
    <div className="flex items-center gap-2">
      {user.picture_url && (
        <img src={user.picture_url} alt={user.name} className="h-7 w-7 rounded-full" />
      )}
      <span className="text-sm text-ink/70 dark:text-ink-dark/70">{user.name}</span>
      <Button variant="ghost" onClick={logout}>
        Log out
      </Button>
    </div>
  );
}
