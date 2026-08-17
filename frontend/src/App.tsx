import { Suspense, lazy } from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";

import { Layout } from "@/components/Layout";
import { DashboardPage } from "@/pages/DashboardPage";
import { FlashcardsPage } from "@/pages/FlashcardsPage";
import { GrammarPage } from "@/pages/GrammarPage";
import { VocabularyPage } from "@/pages/VocabularyPage";
import { VerbsPage } from "@/pages/VerbsPage";

// react-markdown + remark-gfm are only needed on this one page — lazy-load
// it so that dependency doesn't bloat the main bundle for everyone else.
const GrammarTopicPage = lazy(() =>
  import("@/pages/GrammarTopicPage").then((m) => ({ default: m.GrammarTopicPage }))
);
const VerbDetailPage = lazy(() =>
  import("@/pages/VerbDetailPage").then((m) => ({ default: m.VerbDetailPage }))
);

export function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/vocabulary" element={<VocabularyPage />} />
          <Route path="/flashcards" element={<FlashcardsPage />} />
          <Route path="/grammar" element={<GrammarPage />} />
          <Route
            path="/grammar/:slug"
            element={
              <Suspense fallback={<div className="h-64 animate-pulse rounded-card border border-border dark:border-border-dark" />}>
                <GrammarTopicPage />
              </Suspense>
            }
          />
          <Route path="/verbs" element={<VerbsPage />} />
          <Route
            path="/verbs/:infinitive"
            element={
              <Suspense fallback={<div className="h-64 animate-pulse rounded-card border border-border dark:border-border-dark" />}>
                <VerbDetailPage />
              </Suspense>
            }
          />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}
