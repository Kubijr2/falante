import { Link } from "react-router-dom";

import { Button } from "@/components/ui/Button";

interface QuickActionsProps {
  dueToday: number;
}

export function QuickActions({ dueToday }: QuickActionsProps) {
  return (
    <div className="flex gap-3">
      <Link to="/flashcards">
        <Button>{dueToday > 0 ? `Review ${dueToday} due` : "Practice flashcards"}</Button>
      </Link>
      <Link to="/vocabulary">
        <Button variant="secondary">+ Add word</Button>
      </Link>
    </div>
  );
}
