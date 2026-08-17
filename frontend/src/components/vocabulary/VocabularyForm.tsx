import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";

import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import type { VocabularyCreateInput } from "@/types/vocabulary";

const vocabularySchema = z.object({
  portuguese: z.string().min(1, "Required"),
  english: z.string().min(1, "Required"),
  example_sentence: z.string().optional(),
  category: z.string().optional(),
  tags: z.string().optional(), // comma-separated in the form, split on submit
  difficulty: z.enum(["easy", "medium", "hard"]),
});

type FormValues = z.infer<typeof vocabularySchema>;

interface VocabularyFormProps {
  onSubmit: (input: VocabularyCreateInput) => void;
  onCancel: () => void;
  isSubmitting?: boolean;
}

export function VocabularyForm({ onSubmit, onCancel, isSubmitting }: VocabularyFormProps) {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<FormValues>({
    resolver: zodResolver(vocabularySchema),
    defaultValues: { difficulty: "medium" },
  });

  function handleFormSubmit(values: FormValues) {
    onSubmit({
      portuguese: values.portuguese,
      english: values.english,
      example_sentence: values.example_sentence || undefined,
      category: values.category || undefined,
      tags: values.tags
        ? values.tags
            .split(",")
            .map((t) => t.trim())
            .filter(Boolean)
        : [],
      difficulty: values.difficulty,
    });
  }

  return (
    <form onSubmit={handleSubmit(handleFormSubmit)} className="flex flex-col gap-4">
      <div className="grid grid-cols-2 gap-4">
        <Input label="Portuguese" {...register("portuguese")} error={errors.portuguese?.message} />
        <Input label="English" {...register("english")} error={errors.english?.message} />
      </div>
      <Input label="Example sentence" {...register("example_sentence")} />
      <div className="grid grid-cols-2 gap-4">
        <Input label="Category" placeholder="e.g. food" {...register("category")} />
        <Input label="Tags (comma-separated)" placeholder="verbs, core" {...register("tags")} />
      </div>
      <div className="flex flex-col gap-1">
        <label htmlFor="difficulty" className="text-sm font-medium text-ink dark:text-ink-dark">
          Difficulty
        </label>
        <select
          id="difficulty"
          className="rounded-lg border border-border bg-surface px-3 py-2 text-sm text-ink dark:border-border-dark dark:bg-surface-dark dark:text-ink-dark"
          {...register("difficulty")}
        >
          <option value="easy">Easy</option>
          <option value="medium">Medium</option>
          <option value="hard">Hard</option>
        </select>
      </div>
      <div className="flex justify-end gap-2 pt-2">
        <Button type="button" variant="ghost" onClick={onCancel}>
          Cancel
        </Button>
        <Button type="submit" disabled={isSubmitting}>
          {isSubmitting ? "Saving…" : "Save word"}
        </Button>
      </div>
    </form>
  );
}
