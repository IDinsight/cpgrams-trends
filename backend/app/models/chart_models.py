from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime


class ChartDataPoint(BaseModel):
    """Base model for chart data points"""
    name: str
    value: float
    date: Optional[datetime] = None


class SalesData(BaseModel):
    """Model for sales chart data"""
    month: str
    sales: float
    profit: float
    customers: int


class PerformanceMetric(BaseModel):
    """Model for performance metrics"""
    metric: str
    value: float
    change: float
    trend: str  # "up", "down", "stable"


class AnalyticsData(BaseModel):
    """Model for analytics dashboard data"""
    category: str
    value: float
    percentage: float
    color: Optional[str] = None


class ChartResponse(BaseModel):
    """Generic response model for chart data"""
    data: List[Dict[str, Any]]
    total_count: int
    last_updated: datetime


class KPICard(BaseModel):
    """Model for KPI cards"""
    title: str
    value: str
    change: float
    trend: str
    color: str


class TimeSeriesData(BaseModel):
    """Model for time series data"""
    date: str
    value: float
    category: Optional[str] = None


class DonutChartData(BaseModel):
    """Model for donut chart data"""
    name: str
    value: float
    color: str 