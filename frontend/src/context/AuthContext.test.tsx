import { act, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";

vi.mock("@/services/api/auth", () => ({
  authApi: {
    googleSignIn: vi.fn(),
    getMe: vi.fn(),
  },
}));

import { AuthProvider, useAuth } from "@/context/AuthContext";
import { authApi } from "@/services/api/auth";
import { AUTH_UNAUTHORIZED_EVENT, authStorage } from "@/utils/authStorage";

const fakeUser = { id: 1, email: "cole@example.com", name: "Cole", picture_url: null, dashboard_widgets: [] };

function Probe() {
  const { user, isAuthenticated, isLoading, loginWithGoogleIdToken, logout } = useAuth();
  return (
    <div>
      <span data-testid="loading">{String(isLoading)}</span>
      <span data-testid="authed">{String(isAuthenticated)}</span>
      <span data-testid="email">{user?.email ?? "none"}</span>
      <button onClick={() => loginWithGoogleIdToken("fake-id-token")}>Login</button>
      <button onClick={logout}>Logout</button>
    </div>
  );
}

beforeEach(() => {
  localStorage.clear();
  vi.mocked(authApi.googleSignIn).mockReset();
  vi.mocked(authApi.getMe).mockReset();
});

describe("AuthContext", () => {
  it("starts logged out with no stored token", async () => {
    render(
      <AuthProvider>
        <Probe />
      </AuthProvider>
    );
    await waitFor(() => expect(screen.getByTestId("loading").textContent).toBe("false"));
    expect(screen.getByTestId("authed").textContent).toBe("false");
  });

  it("re-hydrates from a stored token on load", async () => {
    authStorage.setToken("existing-token");
    vi.mocked(authApi.getMe).mockResolvedValue(fakeUser);

    render(
      <AuthProvider>
        <Probe />
      </AuthProvider>
    );

    await waitFor(() => expect(screen.getByTestId("authed").textContent).toBe("true"));
    expect(screen.getByTestId("email").textContent).toBe("cole@example.com");
  });

  it("clears a stored token that turns out to be invalid", async () => {
    authStorage.setToken("stale-token");
    vi.mocked(authApi.getMe).mockRejectedValue(new Error("401"));

    render(
      <AuthProvider>
        <Probe />
      </AuthProvider>
    );

    await waitFor(() => expect(screen.getByTestId("loading").textContent).toBe("false"));
    expect(screen.getByTestId("authed").textContent).toBe("false");
    expect(authStorage.getToken()).toBeNull();
  });

  it("logs in and stores the returned token", async () => {
    vi.mocked(authApi.googleSignIn).mockResolvedValue({
      access_token: "new-token",
      token_type: "bearer",
      user: fakeUser,
    });

    render(
      <AuthProvider>
        <Probe />
      </AuthProvider>
    );
    await waitFor(() => expect(screen.getByTestId("loading").textContent).toBe("false"));

    fireEvent.click(screen.getByText("Login"));

    await waitFor(() => expect(screen.getByTestId("authed").textContent).toBe("true"));
    expect(authStorage.getToken()).toBe("new-token");
  });

  it("logs out and clears the stored token", async () => {
    authStorage.setToken("existing-token");
    vi.mocked(authApi.getMe).mockResolvedValue(fakeUser);

    render(
      <AuthProvider>
        <Probe />
      </AuthProvider>
    );
    await waitFor(() => expect(screen.getByTestId("authed").textContent).toBe("true"));

    fireEvent.click(screen.getByText("Logout"));

    await waitFor(() => expect(screen.getByTestId("authed").textContent).toBe("false"));
    expect(authStorage.getToken()).toBeNull();
  });

  it("logs the user out when the API client reports a 401", async () => {
    authStorage.setToken("existing-token");
    vi.mocked(authApi.getMe).mockResolvedValue(fakeUser);

    render(
      <AuthProvider>
        <Probe />
      </AuthProvider>
    );
    await waitFor(() => expect(screen.getByTestId("authed").textContent).toBe("true"));

    act(() => {
      window.dispatchEvent(new Event(AUTH_UNAUTHORIZED_EVENT));
    });

    await waitFor(() => expect(screen.getByTestId("authed").textContent).toBe("false"));
  });
});
