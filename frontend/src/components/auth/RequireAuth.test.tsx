import { render, screen, waitFor, fireEvent } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

vi.mock("@react-oauth/google", () => ({
  GoogleLogin: ({ onSuccess }: { onSuccess: (r: { credential?: string }) => void }) => (
    <button onClick={() => onSuccess({ credential: "fake-credential" })}>
      Sign in with Google
    </button>
  ),
  GoogleOAuthProvider: ({ children }: { children: React.ReactNode }) => <>{children}</>,
}));

vi.mock("@/services/api/auth", () => ({
  authApi: {
    googleSignIn: vi.fn(),
    getMe: vi.fn(),
  },
}));

import { RequireAuth } from "@/components/auth/RequireAuth";
import { AuthProvider } from "@/context/AuthContext";
import { authApi } from "@/services/api/auth";
import { authStorage } from "@/utils/authStorage";

const fakeUser = { id: 1, email: "cole@example.com", name: "Cole", picture_url: null };

describe("RequireAuth", () => {
  it("shows a login prompt naming the feature when logged out", async () => {
    localStorage.clear();
    render(
      <AuthProvider>
        <RequireAuth featureName="the Writing Coach">
          <p>Secret content</p>
        </RequireAuth>
      </AuthProvider>
    );

    await waitFor(() => {
      expect(screen.getByText(/the writing coach/i)).toBeInTheDocument();
    });
    expect(screen.queryByText("Secret content")).not.toBeInTheDocument();
  });

  it("renders children once logged in", async () => {
    localStorage.clear();
    vi.mocked(authApi.getMe).mockResolvedValue(fakeUser);
    authStorage.setToken("existing-token");

    render(
      <AuthProvider>
        <RequireAuth featureName="the Writing Coach">
          <p>Secret content</p>
        </RequireAuth>
      </AuthProvider>
    );

    await waitFor(() => {
      expect(screen.getByText("Secret content")).toBeInTheDocument();
    });
  });

  it("logging in through the prompt reveals the protected content", async () => {
    localStorage.clear();
    vi.mocked(authApi.googleSignIn).mockResolvedValue({
      access_token: "new-token",
      token_type: "bearer",
      user: fakeUser,
    });

    render(
      <AuthProvider>
        <RequireAuth featureName="the Writing Coach">
          <p>Secret content</p>
        </RequireAuth>
      </AuthProvider>
    );

    await waitFor(() => screen.getByText("Sign in with Google"));
    fireEvent.click(screen.getByText("Sign in with Google"));

    await waitFor(() => {
      expect(screen.getByText("Secret content")).toBeInTheDocument();
    });
  });
});
