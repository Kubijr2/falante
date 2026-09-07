import {
  Area,
  AreaChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import { Card } from "@/components/ui/Card";
import type { VocabularyGrowthPoint } from "@/types/analytics";

interface VocabularyGrowthChartProps {
  data: VocabularyGrowthPoint[];
}

export function VocabularyGrowthChart({ data }: VocabularyGrowthChartProps) {
  return (
    <Card>
      <p className="mb-3 font-display text-lg">Vocabulary Growth</p>
      {data.length === 0 ? (
        <p className="text-sm text-ink/60 dark:text-ink-dark/60">
          Add some words to see your growth over time.
        </p>
      ) : data.length === 1 ? (
        // An area chart can't draw a visible trend line from a single
        // point — rather than show what looks like an empty, broken chart,
        // say plainly that there's not enough history yet.
        <p className="text-sm text-ink/60 dark:text-ink-dark/60">
          You've added {data[0].count} word{data[0].count === 1 ? "" : "s"} so far. Check back
          after a few more days to see your growth trend.
        </p>
      ) : (
        <ResponsiveContainer width="100%" height={220}>
          <AreaChart data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke="#DDE3DF" />
            <XAxis dataKey="date" tick={{ fontSize: 11 }} />
            <YAxis allowDecimals={false} tick={{ fontSize: 11 }} />
            <Tooltip />
            <Area
              type="monotone"
              dataKey="cumulative"
              name="Total words"
              stroke="#1B6F5C"
              fill="#1B6F5C"
              fillOpacity={0.15}
              strokeWidth={2}
            />
          </AreaChart>
        </ResponsiveContainer>
      )}
    </Card>
  );
}
