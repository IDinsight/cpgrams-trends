'use client';

import { Card, Title, DonutChart, Legend } from '@tremor/react';
import { DonutChartData } from '@/types/chart-types';

interface AnalyticsDonutChartProps {
  data: DonutChartData[];
  loading?: boolean;
}

export default function AnalyticsDonutChart({ data, loading = false }: AnalyticsDonutChartProps) {
  if (loading) {
    return (
      <Card className="animate-pulse">
        <div className="h-8 bg-gray-200 rounded mb-4 w-1/3"></div>
        <div className="h-72 bg-gray-200 rounded"></div>
      </Card>
    );
  }

  const valueFormatter = (number: number) => `${number}`;

  return (
    <Card>
      <Title>Department Distribution</Title>
      <DonutChart
        className="h-72 mt-4"
        data={data}
        category="value"
        index="name"
        valueFormatter={valueFormatter}
        colors={["blue", "red", "emerald", "amber", "violet"]}
        showLabel={true}
        showAnimation={true}
      />
      <Legend
        className="mt-4"
        categories={data.map(item => item.name)}
        colors={["blue", "red", "emerald", "amber", "violet"]}
      />
    </Card>
  );
} 