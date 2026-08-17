import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useMemo, useState } from "react";

import { vocabularyApi } from "@/services/api/vocabulary";
import type { ReviewResult } from "@/types/vocabulary";

export function useFlashcardSession() {
  const queryClient = useQueryClient();
  const [index, setIndex] = useState(0);
  const [isFlipped, setIsFlipped] = useState(false);

  const dueQuery = useQuery({
    queryKey: ["flashcards", "due"],
    queryFn: vocabularyApi.dueFlashcards,
  });

  const reviewMutation = useMutation({
    mutationFn: ({ id, result }: { id: number; result: ReviewResult }) =>
      vocabularyApi.submitReview(id, result),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["flashcards", "due"] });
      queryClient.invalidateQueries({ queryKey: ["vocabulary"] });
    },
  });

  const cards = useMemo(() => dueQuery.data ?? [], [dueQuery.data]);
  const currentCard = useMemo(() => cards[index] ?? null, [cards, index]);
  const isSessionComplete = dueQuery.isSuccess && cards.length > 0 && index >= cards.length;

  function flip() {
    setIsFlipped((prev) => !prev);
  }

  function submitReview(result: ReviewResult) {
    if (!currentCard) return;
    reviewMutation.mutate({ id: currentCard.id, result });
    setIsFlipped(false);
    setIndex((prev) => prev + 1);
  }

  return {
    currentCard,
    isFlipped,
    flip,
    submitReview,
    isSessionComplete,
    totalDue: cards.length,
    remaining: Math.max(cards.length - index, 0),
    isLoading: dueQuery.isLoading,
    isSubmitting: reviewMutation.isPending,
  };
}
