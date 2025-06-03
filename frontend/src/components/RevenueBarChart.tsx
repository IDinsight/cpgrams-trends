'use client';

import { Card, Title, BarChart } from '@tremor/react';
import { RevenueData } from '@/types/chart-types';

interface RevenueBarChartProps {
  data: RevenueData[];
  loading?: boolean;
}

export default function RevenueBarChart({ data, loading = false }: RevenueBarChartProps) {
  if (loading) {
    return (
      <Card className="animate-pulse">
        <div className="h-8 bg-gray-200 rounded mb-4 w-1/3"></div>
        <div className="h-72 bg-gray-200 rounded"></div>
      </Card>
    );
  }

  return (
    <Card>
      <Title>Monthly Revenue vs Profit</Title>
      <BarChart
        className="h-72 mt-4"
        data={data}
        index="month"
        categories={["revenue", "profit"]}
        colors={["blue", "emerald"]}
        valueFormatter={(number: number) =>
          `$${Intl.NumberFormat("us").format(number).toString()}`
        }
        showLegend={true}
        showGridLines={true}
        layout="vertical"
      />
    </Card>
  );
} 