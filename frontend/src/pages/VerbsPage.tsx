import { useState } from "react";

import { VerbSearchList } from "@/components/verbs/VerbSearchList";
import { Input } from "@/components/ui/Input";
import { useVerbs } from "@/hooks/useVerbs";

export function VerbsPage() {
  const [search, setSearch] = useState("");
  const { data: verbs = [], isLoading } = useVerbs(search || undefined);

  return (
    <div className="flex flex-col gap-6">
      <h1 className="font-display text-2xl">Verb Conjugation Explorer</h1>

      <Input
        label="Search"
        placeholder="Search by infinitive or English meaning…"
        value={search}
        onChange={(e) => setSearch(e.target.value)}
      />

      <VerbSearchList verbs={verbs} isLoading={isLoading} />
    </div>
  );
}
