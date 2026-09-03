/**
 * Splits text into alternating word and non-word tokens, preserving every
 * character (whitespace, punctuation, newlines) so the original text can be
 * reconstructed exactly by re-joining the tokens — this is what lets the
 * reading pane render highlighted words inline without disturbing the
 * original formatting.
 *
 * \p{L} (Unicode "Letter" category) is used instead of \w so accented
 * Portuguese characters (á, ã, ç, é, í, õ, ú, etc.) are correctly treated as
 * word characters rather than splitting a word apart.
 *
 * Known limitation (acceptable for a no-AI MVP): this matches whole words
 * only. "falo" (I speak) won't be recognized as related to a saved "falar"
 * (to speak) entry — there's no stemming/lemmatization here, matching the
 * original brief's "no AI required" scope for this feature.
 */
export function tokenizeText(text: string): string[] {
  return text.match(/[\p{L}]+|[^\p{L}]+/gu) ?? [];
}

export function isWordToken(token: string): boolean {
  return /[\p{L}]/u.test(token);
}
