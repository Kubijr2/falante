import { FlashcardDeck } from "@/components/vocabulary/FlashcardDeck";

export function FlashcardsPage() {
  return (
    <div className="flex flex-col gap-6">
      <h1 className="font-display text-2xl">Flashcards</h1>
      <FlashcardDeck />
    </div>
  );
}
