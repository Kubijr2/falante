import { GoogleOAuthProvider } from "@react-oauth/google";
import { Suspense, lazy } from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";

import { RequireAuth } from "@/components/auth/RequireAuth";
import { Layout } from "@/components/Layout";
import { AuthProvider } from "@/context/AuthContext";
import { DashboardPage } from "@/pages/DashboardPage";
import { FlashcardsPage } from "@/pages/FlashcardsPage";
import { GrammarPage } from "@/pages/GrammarPage";
import { ReadingHelperPage } from "@/pages/ReadingHelperPage";
import { VocabularyPage } from "@/pages/VocabularyPage";
import { VerbsPage } from "@/pages/VerbsPage";
import { WritingCoachPage } from "@/pages/WritingCoachPage";

// react-markdown + remark-gfm are only needed on these pages — lazy-load
// them so that dependency doesn't bloat the main bundle for everyone else.
const GrammarTopicPage = lazy(() =>
  import("@/pages/GrammarTopicPage").then((m) => ({ default: m.GrammarTopicPage }))
);
const VerbDetailPage = lazy(() =>
  import("@/pages/VerbDetailPage").then((m) => ({ default: m.VerbDetailPage }))
);

const lazyFallback = (
  <div className="h-64 animate-pulse rounded-card border border-border dark:border-border-dark" />
);

const googleClientId = import.meta.env.VITE_GOOGLE_CLIENT_ID ?? "";

export function App() {
  return (
    <GoogleOAuthProvider clientId={googleClientId}>
      <AuthProvider>
        <BrowserRouter>
          <Layout>
            <Routes>
              {/* Home / Dashboard — public landing view when logged out,
                  real personalized stats when logged in. DashboardPage
                  handles that branching itself, so it's intentionally NOT
                  wrapped in RequireAuth here. */}
              <Route path="/" element={<DashboardPage />} />

              {/* Personal data — require login. Grammar Reference and the
                  Verb Explorer stay public/browsable below, unwrapped. */}
              <Route
                path="/vocabulary"
                element={
                  <RequireAuth featureName="the Vocabulary Manager">
                    <VocabularyPage />
                  </RequireAuth>
                }
              />
              <Route
                path="/flashcards"
                element={
                  <RequireAuth featureName="Flashcards">
                    <FlashcardsPage />
                  </RequireAuth>
                }
              />
              <Route
                path="/writing"
                element={
                  <RequireAuth featureName="the Writing Coach">
                    <WritingCoachPage />
                  </RequireAuth>
                }
              />
              <Route
                path="/reading"
                element={
                  <RequireAuth featureName="the Reading Helper">
                    <ReadingHelperPage />
                  </RequireAuth>
                }
              />

              {/* Public — no login required to browse */}
              <Route path="/grammar" element={<GrammarPage />} />
              <Route
                path="/grammar/:slug"
                element={
                  <Suspense fallback={lazyFallback}>
                    <GrammarTopicPage />
                  </Suspense>
                }
              />
              <Route path="/verbs" element={<VerbsPage />} />
              <Route
                path="/verbs/:infinitive"
                element={
                  <Suspense fallback={lazyFallback}>
                    <VerbDetailPage />
                  </Suspense>
                }
              />
            </Routes>
          </Layout>
        </BrowserRouter>
      </AuthProvider>
    </GoogleOAuthProvider>
  );
}
