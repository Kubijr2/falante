import type { Config } from "tailwindcss";

// Design tokens for Falante. Deliberately not the "cream + terracotta serif"
// AI-default palette — this leans into a muted jade/gold pairing that nods
// to Brazilian Portuguese without being a flag cliché, kept quiet enough to
// stay professional for a resume-facing project.
export default {
  darkMode: "class",
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        base: {
          DEFAULT: "#F6F7F5",
          dark: "#121715",
        },
        surface: {
          DEFAULT: "#FFFFFF",
          dark: "#1B231F",
        },
        ink: {
          DEFAULT: "#1C2321",
          dark: "#EDEFEC",
        },
        primary: {
          50: "#EAF4F1",
          100: "#CEE5DD",
          400: "#2C8F76",
          500: "#1B6F5C",
          600: "#155A4A",
          700: "#0F4438",
        },
        gold: {
          400: "#F2BA3E",
          500: "#E3A008",
        },
        border: {
          DEFAULT: "#DDE3DF",
          dark: "#2A342F",
        },
      },
      fontFamily: {
        display: ["Fraunces", "Georgia", "serif"],
        body: ["Inter", "system-ui", "sans-serif"],
        mono: ["JetBrains Mono", "monospace"],
      },
      borderRadius: {
        card: "1rem",
      },
    },
  },
  plugins: [],
} satisfies Config;
