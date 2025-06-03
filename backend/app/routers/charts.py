from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime, timedelta
import random

from app.models.chart_models import (
    SalesData, 
    PerformanceMetric, 
    AnalyticsData, 
    KPICard, 
    TimeSeriesData, 
    DonutChartData
)

router = APIRouter(prefix="/api/charts", tags=["charts"])


@router.get("/sales", response_model=List[SalesData])
async def get_sales_data():
    """Get sales data for area/bar charts"""
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    
    sales_data = []
    for month in months:
        sales_data.append(SalesData(
            month=month,
            sales=random.uniform(10000, 50000),
            profit=random.uniform(2000, 15000),
            customers=random.randint(100, 500)
        ))
    
    return sales_data


@router.get("/performance", response_model=List[PerformanceMetric])
async def get_performance_metrics():
    """Get performance metrics for KPI cards"""
    metrics = [
        {
            "metric": "Revenue",
            "value": 45000.00,
            "change": 12.5,
            "trend": "up"
        },
        {
            "metric": "Users",
            "value": 1250.0,
            "change": -3.2,
            "trend": "down"
        },
        {
            "metric": "Conversion Rate",
            "value": 3.45,
            "change": 0.8,
            "trend": "up"
        },
        {
            "metric": "Avg. Order Value",
            "value": 89.50,
            "change": 5.1,
            "trend": "up"
        }
    ]
    
    return [PerformanceMetric(**metric) for metric in metrics]


@router.get("/analytics", response_model=List[AnalyticsData])
async def get_analytics_data():
    """Get analytics data for donut charts"""
    categories = [
        {"category": "Desktop", "value": 45.2, "percentage": 45.2, "color": "#3b82f6"},
        {"category": "Mobile", "value": 32.8, "percentage": 32.8, "color": "#ef4444"},
        {"category": "Tablet", "value": 15.1, "percentage": 15.1, "color": "#10b981"},
        {"category": "Other", "value": 6.9, "percentage": 6.9, "color": "#f59e0b"}
    ]
    
    return [AnalyticsData(**category) for category in categories]


@router.get("/kpi-cards", response_model=List[KPICard])
async def get_kpi_cards():
    """Get KPI card data"""
    kpis = [
        {
            "title": "Total Revenue",
            "value": "$45,231",
            "change": 20.1,
            "trend": "up",
            "color": "emerald"
        },
        {
            "title": "Active Users",
            "value": "2,350",
            "change": -10.1,
            "trend": "down",
            "color": "red"
        },
        {
            "title": "Conversion Rate",
            "value": "3.45%",
            "change": 5.4,
            "trend": "up",
            "color": "blue"
        },
        {
            "title": "Avg Session",
            "value": "4:35",
            "change": 2.1,
            "trend": "up",
            "color": "emerald"
        }
    ]
    
    return [KPICard(**kpi) for kpi in kpis]


@router.get("/time-series", response_model=List[TimeSeriesData])
async def get_time_series_data():
    """Get time series data for line charts"""
    base_date = datetime.now() - timedelta(days=30)
    time_series = []
    
    for i in range(30):
        current_date = base_date + timedelta(days=i)
        time_series.append(TimeSeriesData(
            date=current_date.strftime("%Y-%m-%d"),
            value=random.uniform(100, 1000),
            category="Website Traffic"
        ))
    
    return time_series


@router.get("/donut-data", response_model=List[DonutChartData])
async def get_donut_chart_data():
    """Get data specifically formatted for donut charts"""
    donut_data = [
        {"name": "Sales", "value": 890, "color": "#3b82f6"},
        {"name": "Marketing", "value": 338, "color": "#ef4444"},
        {"name": "Development", "value": 538, "color": "#10b981"},
        {"name": "Support", "value": 396, "color": "#f59e0b"},
        {"name": "Other", "value": 135, "color": "#8b5cf6"}
    ]
    
    return [DonutChartData(**item) for item in donut_data]


@router.get("/revenue-by-month", response_model=List[dict])
async def get_revenue_by_month():
    """Get monthly revenue data for area charts"""
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    revenue_data = []
    
    for month in months:
        revenue_data.append({
            "month": month,
            "revenue": random.randint(15000, 50000),
            "profit": random.randint(5000, 20000)
        })
    
    return revenue_data 