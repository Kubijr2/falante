import { createContext, useContext, useEffect, useState, type ReactNode } from "react";

import { authApi } from "@/services/api/auth";
import type { AuthUser } from "@/types/auth";
import { AUTH_UNAUTHORIZED_EVENT, authStorage } from "@/utils/authStorage";

interface AuthContextValue {
  user: AuthUser | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  loginWithGoogleIdToken: (idToken: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(null);
  // Starts true — on first load we don't yet know if a stored token is
  // still valid, so every consumer (route guards especially) needs a way
  // to distinguish "still checking" from "confirmed logged out".
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const existingToken = authStorage.getToken();
    if (!existingToken) {
      setIsLoading(false);
      return;
    }
    // Re-hydrate: confirm the stored token is still valid and fetch the
    // user it belongs to, rather than trusting localStorage blindly.
    authApi
      .getMe()
      .then(setUser)
      .catch(() => authStorage.clearToken())
      .finally(() => setIsLoading(false));
  }, []);

  useEffect(() => {
    function handleUnauthorized() {
      setUser(null);
    }
    window.addEventListener(AUTH_UNAUTHORIZED_EVENT, handleUnauthorized);
    return () => window.removeEventListener(AUTH_UNAUTHORIZED_EVENT, handleUnauthorized);
  }, []);

  async function loginWithGoogleIdToken(idToken: string) {
    const response = await authApi.googleSignIn(idToken);
    authStorage.setToken(response.access_token);
    setUser(response.user);
  }

  function logout() {
    authStorage.clearToken();
    setUser(null);
  }

  return (
    <AuthContext.Provider
      value={{ user, isLoading, isAuthenticated: user !== null, loginWithGoogleIdToken, logout }}
    >
      {children}
    </AuthContext.Provider>
  );
}

// eslint-disable-next-line react-refresh/only-export-components -- provider + hook are kept together for cohesion, a standard React context pattern
export function useAuth(): AuthContextValue {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
