from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime


class GrievanceRecord(BaseModel):
    """Base model for a grievance record"""
    _id: str
    state: Optional[str] = None
    org_code: Optional[str] = None
    sex: Optional[str] = None
    CategoryV7: Optional[int] = None
    DiaryDate: Optional[str] = None
    recvd_date: Optional[str] = None
    closing_date: Optional[str] = None
    resolution_date: Optional[str] = None
    dist_name: Optional[str] = None
    pincode: Optional[str] = None
    v7_target: Optional[str] = None


class StateWiseGrievances(BaseModel):
    """Model for state-wise grievance statistics"""
    state: str
    count: int
    percentage: float
    color: Optional[str] = None


class CategoryWiseGrievances(BaseModel):
    """Model for category-wise grievance statistics"""
    category: str
    count: int
    percentage: float
    color: Optional[str] = None


class MonthlyGrievanceStats(BaseModel):
    """Model for monthly grievance statistics"""
    month: str
    total_grievances: int
    resolved_grievances: int
    pending_grievances: int
    resolution_rate: float


class GrievanceKPI(BaseModel):
    """Model for grievance KPI metrics"""
    title: str
    value: str
    change: float
    trend: str
    color: str


class GenderWiseGrievances(BaseModel):
    """Model for gender-wise grievance distribution"""
    gender: str
    count: int
    percentage: float
    color: Optional[str] = None


class OrganizationWiseGrievances(BaseModel):
    """Model for organization-wise grievance statistics"""
    org_code: str
    org_name: Optional[str] = None
    count: int
    percentage: float
    avg_resolution_days: Optional[float] = None


class GrievanceTimeSeries(BaseModel):
    """Model for time series grievance data"""
    date: str
    received: int
    resolved: int
    pending: int


class GrievanceSummary(BaseModel):
    """Model for overall grievance summary"""
    total_grievances: int
    resolved_grievances: int
    pending_grievances: int
    avg_resolution_time: float
    resolution_rate: float
    top_states: List[StateWiseGrievances]
    top_categories: List[CategoryWiseGrievances] 