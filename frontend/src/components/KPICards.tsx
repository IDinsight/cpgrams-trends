'use client';

import { Card, Metric, Text, Flex, BadgeDelta, DeltaType } from '@tremor/react';
import { KPICard } from '@/types/chart-types';

interface KPICardsProps {
  data: KPICard[];
  loading?: boolean;
}

const getDeltaType = (trend: string): DeltaType => {
  switch (trend) {
    case 'up': return 'increase';
    case 'down': return 'decrease';
    case 'stable': return 'unchanged';
    default: return 'unchanged';
  }
};

type TremorColor = 
  | 'blue' | 'emerald' | 'red' | 'amber' | 'gray' | 'green' | 'yellow' 
  | 'orange' | 'violet' | 'purple' | 'pink' | 'rose' | 'indigo' | 'cyan' | 'teal';

const getDecorationColor = (color: string): TremorColor => {
  const validColors: TremorColor[] = [
    'blue', 'emerald', 'red', 'amber', 'gray', 'green', 'yellow',
    'orange', 'violet', 'purple', 'pink', 'rose', 'indigo', 'cyan', 'teal'
  ];
  return validColors.includes(color as TremorColor) ? color as TremorColor : 'blue';
};

export default function KPICards({ data, loading = false }: KPICardsProps) {
  if (loading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        {[...Array(4)].map((_, i) => (
          <Card key={i} className="animate-pulse">
            <div className="h-16 bg-gray-200 rounded"></div>
          </Card>
        ))}
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
      {data.map((kpi, index) => (
        <Card key={index} decoration="top" decorationColor={getDecorationColor(kpi.color)}>
          <Flex justifyContent="between" alignItems="start">
            <div className="truncate">
              <Text>{kpi.title}</Text>
              <Metric className="truncate">{kpi.value}</Metric>
            </div>
            <BadgeDelta 
              deltaType={getDeltaType(kpi.trend)}
              size="xs"
            >
              {Math.abs(kpi.change)}%
            </BadgeDelta>
          </Flex>
        </Card>
      ))}
    </div>
  );
} 