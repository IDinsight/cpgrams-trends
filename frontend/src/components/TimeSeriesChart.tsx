'use client';

import { Card, Title, LineChart } from '@tremor/react';
import { TimeSeriesData } from '@/types/chart-types';

interface TimeSeriesChartProps {
  data: TimeSeriesData[];
  loading?: boolean;
}

export default function TimeSeriesChart({ data, loading = false }: TimeSeriesChartProps) {
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
      <Title>Website Traffic Over Time</Title>
      <LineChart
        className="h-72 mt-4"
        data={data}
        index="date"
        categories={["value"]}
        colors={["blue"]}
        valueFormatter={(number: number) =>
          `${Intl.NumberFormat("us").format(number).toString()} visits`
        }
        showLegend={false}
        showGridLines={true}
        curveType="natural"
        connectNulls={true}
      />
    </Card>
  );
} 