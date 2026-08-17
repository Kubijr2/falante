import axios from "axios";

// Falls back to localhost:8000 so `npm run dev` works with zero .env setup —
// but reads VITE_API_URL if you set one (e.g. for a deployed backend later).
const baseURL = import.meta.env.VITE_API_URL ?? "http://localhost:8000/api/v1";

export const apiClient = axios.create({
  baseURL,
  headers: { "Content-Type": "application/json" },
});
