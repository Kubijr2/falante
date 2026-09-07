import { Bar, BarChart, CartesianGrid, Legend, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

import { Card } from "@/components/ui/Card";
import type { ReviewQualityPoint } from "@/types/analytics";

interface ReviewQualityChartProps {
  data: ReviewQualityPoint[];
}

export function ReviewQualityChart({ data }: ReviewQualityChartProps) {
  return (
    <Card>
      <p className="mb-3 font-display text-lg">Review Quality</p>
      {data.length === 0 ? (
        <p className="text-sm text-ink/60 dark:text-ink-dark/60">
          Review some flashcards to see how you're doing.
        </p>
      ) : (
        <ResponsiveContainer width="100%" height={220}>
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke="#DDE3DF" />
            <XAxis dataKey="date" tick={{ fontSize: 11 }} />
            <YAxis allowDecimals={false} tick={{ fontSize: 11 }} />
            <Tooltip />
            <Legend wrapperStyle={{ fontSize: 12 }} />
            <Bar dataKey="again" name="Again" stackId="a" fill="#DC2626" />
            <Bar dataKey="hard" name="Hard" stackId="a" fill="#E3A008" />
            <Bar dataKey="medium" name="Medium" stackId="a" fill="#2C8F76" />
            <Bar dataKey="easy" name="Easy" stackId="a" fill="#155A4A" />
          </BarChart>
        </ResponsiveContainer>
      )}
    </Card>
  );
}
