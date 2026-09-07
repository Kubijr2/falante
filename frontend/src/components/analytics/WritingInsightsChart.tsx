import { Bar, BarChart, CartesianGrid, Legend, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

import { Card } from "@/components/ui/Card";
import type { WritingInsightPoint } from "@/types/analytics";

interface WritingInsightsChartProps {
  data: WritingInsightPoint[];
}

export function WritingInsightsChart({ data }: WritingInsightsChartProps) {
  return (
    <Card>
      <p className="mb-3 font-display text-lg">Writing Insights</p>
      {data.length === 0 ? (
        <p className="text-sm text-ink/60 dark:text-ink-dark/60">
          Submit something to the Writing Coach to see your correction patterns here.
        </p>
      ) : (
        <ResponsiveContainer width="100%" height={220}>
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke="#DDE3DF" />
            <XAxis dataKey="date" tick={{ fontSize: 11 }} />
            <YAxis allowDecimals={false} tick={{ fontSize: 11 }} />
            <Tooltip />
            <Legend wrapperStyle={{ fontSize: 12 }} />
            <Bar dataKey="grammar" name="Grammar" fill="#1B6F5C" />
            <Bar dataKey="wording" name="Wording" fill="#E3A008" />
          </BarChart>
        </ResponsiveContainer>
      )}
    </Card>
  );
}
