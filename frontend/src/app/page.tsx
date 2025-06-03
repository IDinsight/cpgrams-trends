"use client";

import { useEffect, useState } from "react";
import { Title, Text } from "@tremor/react";
import { AlertCircle } from "lucide-react";

import KPICards from "@/components/KPICards";
import SalesChart from "@/components/SalesChart";
import AnalyticsDonutChart from "@/components/AnalyticsDonutChart";
import TimeSeriesChart from "@/components/TimeSeriesChart";
import RevenueBarChart from "@/components/RevenueBarChart";

import {
  KPICard,
  SalesData,
  DonutChartData,
  TimeSeriesData,
  RevenueData,
} from "@/types/chart-types";

export default function Dashboard() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [dashboardData, setDashboardData] = useState<{
    kpiCards: KPICard[];
    salesData: SalesData[];
    donutData: DonutChartData[];
    timeSeriesData: TimeSeriesData[];
    revenueData: RevenueData[];
  }>({
    kpiCards: [],
    salesData: [],
    donutData: [],
    timeSeriesData: [],
    revenueData: [],
  });

  useEffect(() => {}, []);

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 p-8">
        <div className="max-w-7xl mx-auto">
          <div className="bg-red-50 border border-red-200 rounded-lg p-6 flex items-center space-x-3">
            <AlertCircle className="h-6 w-6 text-red-600" />
            <div>
              <h3 className="text-red-800 font-medium">
                Error Loading Dashboard
              </h3>
              <p className="text-red-600 text-sm mt-1">{error}</p>
              <p className="text-red-600 text-sm mt-1">
                Make sure the FastAPI backend is running on
                http://localhost:8000
              </p>
              <button
                onClick={() => window.location.reload()}
                className="mt-3 bg-red-600 text-white px-4 py-2 rounded text-sm hover:bg-red-700"
              >
                Retry
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <Title className="text-3xl font-bold text-gray-900">
            CPGrams Trends Dashboard
          </Title>
          <Text className="text-gray-600 mt-2">
            Real-time analytics and performance insights
          </Text>
        </div>

        {/* KPI Cards */}
        <KPICards data={dashboardData.kpiCards} loading={loading} />

        {/* Charts Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          <SalesChart data={dashboardData.salesData} loading={loading} />
          <AnalyticsDonutChart
            data={dashboardData.donutData}
            loading={loading}
          />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <TimeSeriesChart
            data={dashboardData.timeSeriesData}
            loading={loading}
          />
          <RevenueBarChart data={dashboardData.revenueData} loading={loading} />
        </div>

        {/* Footer */}
        <div className="mt-12 text-center text-gray-500 text-sm">
          <Text>Powered by FastAPI + Next.js + Tremor</Text>
        </div>
      </div>
    </div>
  );
}
