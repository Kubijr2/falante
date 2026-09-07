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
import { VerbsPage } from "@/pages/VerbsPage";
import { VocabularyPage } from "@/pages/VocabularyPage";
import { WritingCoachPage } from "@/pages/WritingCoachPage";

const AnalyticsPage = lazy(() =>
  import("@/pages/AnalyticsPage").then((m) => ({
    default: m.AnalyticsPage,
  }))
);

const googleClientId = import.meta.env.VITE_GOOGLE_CLIENT_ID ?? "";
const lazyFallback = <div>Loading...</div>;

export function App() {
  return (
    <GoogleOAuthProvider clientId={googleClientId}>
      <AuthProvider>
        <BrowserRouter>
          <Layout>
            <Routes>
              <Route path="/" element={<DashboardPage />} />
              
              <Route path="/vocabulary" element={<VocabularyPage />} />
              <Route path="/flashcards" element={<FlashcardsPage />} />
              <Route path="/grammar" element={<GrammarPage />} />
              <Route path="/verbs" element={<VerbsPage />} />
              <Route path="/writing" element={<WritingCoachPage />} />
              <Route path="/reading" element={<ReadingHelperPage />} />

              <Route
                path="/analytics"
                element={
                  <RequireAuth featureName="Analytics">
                    <Suspense fallback={lazyFallback}>
                      <AnalyticsPage />
                    </Suspense>
                  </RequireAuth>
                }
              />
            </Routes>
          </Layout>
        </BrowserRouter>
      </AuthProvider>
    </GoogleOAuthProvider>
  );
}