'use client';

import { Card, Title, AreaChart } from '@tremor/react';
import { SalesData } from '@/types/chart-types';

interface SalesChartProps {
  data: SalesData[];
  loading?: boolean;
}

export default function SalesChart({ data, loading = false }: SalesChartProps) {
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
      <Title>Sales Performance</Title>
      <AreaChart
        className="h-72 mt-4"
        data={data}
        index="month"
        categories={["sales", "profit"]}
        colors={["blue", "emerald"]}
        valueFormatter={(number: number) =>
          `$${Intl.NumberFormat("us").format(number).toString()}`
        }
        showLegend={true}
        showGridLines={true}
        curveType="natural"
      />
    </Card>
  );
} 