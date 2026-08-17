import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";
import path from "node:path";

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    port: 5173,
    // Listen on all interfaces so the dev server is reachable from the host
    // machine when running inside Docker (see frontend/Dockerfile.dev).
    // Harmless outside Docker too.
    host: true,
    watch: {
      // Bind-mounted filesystems in Docker (especially on macOS/Windows)
      // don't always propagate native file-change events reliably, so hot
      // reload can silently stop working. Polling fixes it at a small CPU
      // cost — only enabled when DOCKER=true, set in docker-compose.yml, so
      // plain local `npm run dev` still uses the cheaper native watcher.
      usePolling: process.env.DOCKER === "true",
    },
  },
  test: {
    environment: "jsdom",
    globals: true,
    setupFiles: "./src/setupTests.ts",
  },
});
