export interface SalesData {
  month: string;
  sales: number;
  profit: number;
  customers: number;
}

export interface PerformanceMetric {
  metric: string;
  value: number;
  change: number;
  trend: "up" | "down" | "stable";
}

export interface AnalyticsData {
  category: string;
  value: number;
  percentage: number;
  color?: string;
}

export interface KPICard {
  title: string;
  value: string;
  change: number;
  trend: "up" | "down" | "stable";
  color: string;
}

export interface TimeSeriesData {
  date: string;
  value: number;
  category?: string;
}

export interface DonutChartData {
  name: string;
  value: number;
  color: string;
}

export interface RevenueData {
  month: string;
  revenue: number;
  profit: number;
}
