import { useMutation, useQuery } from "@tanstack/react-query";
import { useState } from "react";

import { tutorApi } from "@/services/api/tutor";
import type { TutorMessage } from "@/types/tutor";

export function useTutorStatus() {
  return useQuery({
    queryKey: ["tutor", "status"],
    queryFn: tutorApi.status,
    staleTime: 5 * 60_000, // rarely changes mid-session, no need to refetch often
  });
}

/**
 * Owns the running conversation for one Grammar topic page. Deliberately
 * plain React state, not TanStack Query — this is client-only session state
 * with no server-side counterpart to sync against (the backend never
 * persists the transcript; see TutorRequest.history in the backend schema).
 */
export function useTutorChat(topicSlug: string | undefined) {
  const [messages, setMessages] = useState<TutorMessage[]>([]);

  const mutation = useMutation({
    mutationFn: (question: string) => tutorApi.ask(question, messages, topicSlug),
  });

  function sendQuestion(question: string) {
    const userMessage: TutorMessage = { role: "user", content: question };
    setMessages((prev) => [...prev, userMessage]);

    mutation.mutate(question, {
      onSuccess: (response) => {
        setMessages((prev) => [...prev, { role: "assistant", content: response.answer }]);
      },
      onError: () => {
        // Roll the optimistic user message back out rather than leaving an
        // unanswered question sitting in the transcript.
        setMessages((prev) => prev.slice(0, -1));
      },
    });
  }

  return {
    messages,
    sendQuestion,
    isSending: mutation.isPending,
    error: mutation.error,
  };
}
