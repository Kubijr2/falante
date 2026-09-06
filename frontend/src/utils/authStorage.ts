const STORAGE_KEY = "falante_auth_token";

export const authStorage = {
  getToken: (): string | null => localStorage.getItem(STORAGE_KEY),
  setToken: (token: string): void => localStorage.setItem(STORAGE_KEY, token),
  clearToken: (): void => localStorage.removeItem(STORAGE_KEY),
};

/**
 * Dispatched by the API client whenever a request comes back 401 (expired
 * or invalid token) — AuthContext listens for this to clear its state and
 * prompt a fresh login, without client.ts needing to import AuthContext
 * directly (which would create a circular import, since AuthContext's own
 * login/getMe calls go through apiClient).
 */
export const AUTH_UNAUTHORIZED_EVENT = "falante:auth-unauthorized";
