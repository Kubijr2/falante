import { apiClient } from "@/services/api/client";
import type { AuthResponse, AuthUser } from "@/types/auth";

export const authApi = {
  googleSignIn: async (idToken: string): Promise<AuthResponse> => {
    const { data } = await apiClient.post<AuthResponse>("/auth/google", { id_token: idToken });
    return data;
  },

  getMe: async (): Promise<AuthUser> => {
    const { data } = await apiClient.get<AuthUser>("/auth/me");
    return data;
  },
};
