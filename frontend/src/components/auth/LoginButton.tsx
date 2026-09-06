import { GoogleLogin } from "@react-oauth/google";
import axios from "axios";
import { useState } from "react";

import { useAuth } from "@/context/AuthContext";

function extractErrorMessage(err: unknown): string {
  if (axios.isAxiosError(err)) {
    if (err.response) {
      // The backend responded but rejected the request — show its actual
      // reason (e.g. a Client ID mismatch, or "Couldn't verify with
      // Google: ...") rather than a generic message that hides it.
      const detail = err.response.data?.detail;
      if (typeof detail === "string") return detail;
      return `Sign-in failed (server responded ${err.response.status}).`;
    }
    // No response at all usually means the request never reached the
    // backend — a CORS rejection or the API being unreachable.
    return "Couldn't reach the server — check that the backend is running and CORS_ORIGINS includes this site's URL.";
  }
  return "Couldn't sign you in — try again in a moment.";
}

export function LoginButton() {
  const { loginWithGoogleIdToken } = useAuth();
  const [error, setError] = useState<string | null>(null);

  return (
    <div className="flex flex-col items-center gap-2">
      <GoogleLogin
        onSuccess={(credentialResponse) => {
          setError(null);
          if (!credentialResponse.credential) {
            setError("Google didn't return a credential — try again.");
            return;
          }
          loginWithGoogleIdToken(credentialResponse.credential).catch((err) => {
            setError(extractErrorMessage(err));
          });
        }}
        onError={() => setError("Google sign-in failed — try again.")}
      />
      {error && <p className="max-w-xs text-center text-sm text-red-600">{error}</p>}
    </div>
  );
}
