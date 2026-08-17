import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

interface GrammarArticleProps {
  content: string;
}

// Styled via arbitrary-variant selectors on the wrapper instead of pulling
// in @tailwindcss/typography — keeps the dependency list smaller for what's
// ultimately five articles' worth of markdown.
export function GrammarArticle({ content }: GrammarArticleProps) {
  return (
    <div
      className="
        [&_h2]:font-display [&_h2]:text-xl [&_h2]:mt-6 [&_h2]:mb-2
        [&_h3]:font-display [&_h3]:text-lg [&_h3]:mt-4 [&_h3]:mb-1
        [&_p]:text-ink/90 dark:[&_p]:text-ink-dark/90 [&_p]:leading-relaxed [&_p]:mb-3
        [&_ul]:list-disc [&_ul]:pl-5 [&_ul]:mb-3 [&_li]:mb-1
        [&_strong]:font-semibold [&_strong]:text-primary-700 dark:[&_strong]:text-primary-100
        [&_em]:italic
        [&_table]:w-full [&_table]:border-collapse [&_table]:mb-4 [&_table]:text-sm
        [&_th]:border [&_th]:border-border dark:[&_th]:border-border-dark [&_th]:bg-primary-50 dark:[&_th]:bg-primary-700/20 [&_th]:p-2 [&_th]:text-left
        [&_td]:border [&_td]:border-border dark:[&_td]:border-border-dark [&_td]:p-2
        [&_code]:font-mono [&_code]:text-sm [&_code]:bg-border/40 dark:[&_code]:bg-border-dark/40 [&_code]:px-1 [&_code]:rounded
      "
    >
      <ReactMarkdown remarkPlugins={[remarkGfm]}>{content}</ReactMarkdown>
    </div>
  );
}
