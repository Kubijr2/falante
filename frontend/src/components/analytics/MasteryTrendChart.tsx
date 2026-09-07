import {
  Area,
  AreaChart,
  CartesianGrid,
  Legend,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import { Card } from "@/components/ui/Card";
import type { MasteryTrendPoint } from "@/types/analytics";

interface MasteryTrendChartProps {
  data: MasteryTrendPoint[];
}

// Lightest (level 0, just added) to darkest (level 5, fully mastered) —
// same jade family used everywhere else, so a mastered word "deepening in
// color" reads intuitively without needing a legend to explain it.
const LEVEL_COLORS = ["#CEE5DD", "#A8D4C6", "#82C3AF", "#5CAF95", "#2C8F76", "#0F4438"];

export function MasteryTrendChart({ data }: MasteryTrendChartProps) {
  return (
    <Card>
      <p className="mb-3 font-display text-lg">Mastery Trend</p>
      {data.length === 0 ? (
        <p className="text-sm text-ink/60 dark:text-ink-dark/60">
          Add and review some words to see your mastery grow over time.
        </p>
      ) : data.length === 1 ? (
        // Same reasoning as VocabularyGrowthChart — an area chart needs at
        // least two points to draw a visible trend.
        <p className="text-sm text-ink/60 dark:text-ink-dark/60">
          Check back after a few more days of reviewing to see your mastery trend.
        </p>
      ) : (
        <ResponsiveContainer width="100%" height={240}>
          <AreaChart data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke="#DDE3DF" />
            <XAxis dataKey="date" tick={{ fontSize: 11 }} />
            <YAxis allowDecimals={false} tick={{ fontSize: 11 }} />
            <Tooltip />
            <Legend wrapperStyle={{ fontSize: 12 }} />
            {[0, 1, 2, 3, 4, 5].map((level) => (
              <Area
                key={level}
                type="monotone"
                dataKey={`level_${level}`}
                name={`Level ${level}`}
                stackId="mastery"
                stroke={LEVEL_COLORS[level]}
                fill={LEVEL_COLORS[level]}
              />
            ))}
          </AreaChart>
        </ResponsiveContainer>
      )}
    </Card>
  );
}
