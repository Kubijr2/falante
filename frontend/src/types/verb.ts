export interface VerbListItem {
  id: number;
  infinitive: string;
  translation: string;
  is_irregular: boolean;
}

export type TenseKey =
  | "present"
  | "preterito_perfeito"
  | "preterito_imperfeito"
  | "future"
  | "conditional"
  | "subjunctive_present";

export interface VerbDetail extends VerbListItem {
  // tense key -> [eu, ele/ela/você, nós, eles/elas/vocês]
  conjugations: Record<TenseKey, string[]>;
}

// Single source of truth for display order + labels on the frontend,
// mirroring app/services/conjugation_engine.py's TENSE_LABELS.
export const TENSE_ORDER: TenseKey[] = [
  "present",
  "preterito_perfeito",
  "preterito_imperfeito",
  "future",
  "conditional",
  "subjunctive_present",
];

export const TENSE_LABELS: Record<TenseKey, string> = {
  present: "Present",
  preterito_perfeito: "Pretérito Perfeito",
  preterito_imperfeito: "Pretérito Imperfeito",
  future: "Future",
  conditional: "Conditional",
  subjunctive_present: "Subjunctive (Present)",
};

export const PERSON_LABELS = ["eu", "ele/ela/você", "nós", "eles/elas/vocês"];
