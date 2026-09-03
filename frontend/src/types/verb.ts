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
  conjugations: Record<TenseKey, string[]>;
}

export interface VerbFormMatch {
  infinitive: string;
  translation: string;
}

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
