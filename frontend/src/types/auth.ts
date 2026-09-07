export interface AuthUser {
  id: number;
  email: string;
  name: string;
  picture_url: string | null;
  dashboard_widgets: string[];
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: AuthUser;
}
