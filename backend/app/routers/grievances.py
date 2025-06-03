from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel

from app.services.grievance_service import GrievanceService

router = APIRouter(prefix="/api/grievances", tags=["grievances"])
grievance_service = GrievanceService()


class GrievanceIdRequest(BaseModel):
    grievance_id: str


@router.post("/by-id")
async def get_grievance_by_id(request: GrievanceIdRequest) -> Dict[str, Any]:
    """
    Get a specific grievance by its ID.
    
    Request body:
    {
        "grievance_id": "MORLY/E/2023/0000001"
    }
    
    Returns:
        Single grievance record or 404 if not found
    """
    try:
        result = grievance_service.get_grievance_by_id(request.grievance_id)
        
        if not result:
            raise HTTPException(status_code=404, detail=f"Grievance with ID '{request.grievance_id}' not found")
        
        return {
            "data": result,
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving grievance: {str(e)}")


@router.get("/")
async def get_grievances(
    # Filtering parameters
    state: Optional[str] = Query(None, description="Filter by state"),
    org_code: Optional[str] = Query(None, description="Filter by organization code"),
    sex: Optional[str] = Query(None, description="Filter by gender (M/F)"),
    CategoryV7: Optional[int] = Query(None, description="Filter by category V7"),
    dist_name: Optional[str] = Query(None, description="Filter by district name"),
    pincode: Optional[str] = Query(None, description="Filter by pincode"),
    v7_target: Optional[str] = Query(None, description="Filter by V7 target (Yes/No)"),
    
    # Date filtering
    diary_date_from: Optional[str] = Query(None, description="Filter DiaryDate from (YYYY-MM-DD)"),
    diary_date_to: Optional[str] = Query(None, description="Filter DiaryDate to (YYYY-MM-DD)"),
    recvd_date_from: Optional[str] = Query(None, description="Filter received date from (YYYY-MM-DD)"),
    recvd_date_to: Optional[str] = Query(None, description="Filter received date to (YYYY-MM-DD)"),
    closing_date_from: Optional[str] = Query(None, description="Filter closing date from (YYYY-MM-DD)"),
    closing_date_to: Optional[str] = Query(None, description="Filter closing date to (YYYY-MM-DD)"),
    
    # Pagination
    limit: Optional[int] = Query(100, description="Number of records to return (max 1000)", le=1000),
    offset: Optional[int] = Query(0, description="Number of records to skip", ge=0),
) -> Dict[str, Any]:
    """
    Get grievances with flexible filtering options.
    Returns raw JSON data without pre-analysis.
    """
    try:
        # Build filters dictionary
        filters = {}
        
        # Simple field filters
        if state:
            filters["state"] = state
        if org_code:
            filters["org_code"] = org_code
        if sex:
            filters["sex"] = sex
        if CategoryV7:
            filters["CategoryV7"] = CategoryV7
        if dist_name:
            filters["dist_name"] = dist_name
        if pincode:
            filters["pincode"] = pincode
        if v7_target:
            filters["v7_target"] = v7_target
        
        # Date range filters
        if diary_date_from or diary_date_to:
            date_filter = {}
            if diary_date_from:
                date_filter["from"] = diary_date_from
            if diary_date_to:
                date_filter["to"] = diary_date_to
            filters["DiaryDate"] = date_filter
        
        if recvd_date_from or recvd_date_to:
            date_filter = {}
            if recvd_date_from:
                date_filter["from"] = recvd_date_from
            if recvd_date_to:
                date_filter["to"] = recvd_date_to
            filters["recvd_date"] = date_filter
        
        if closing_date_from or closing_date_to:
            date_filter = {}
            if closing_date_from:
                date_filter["from"] = closing_date_from
            if closing_date_to:
                date_filter["to"] = closing_date_to
            filters["closing_date"] = date_filter
        
        # Get filtered results
        results = grievance_service.get_grievances(
            filters=filters if filters else None,
            limit=limit,
            offset=offset
        )
        
        return results
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")


@router.post("/filter")
async def filter_grievances(
    filters: Dict[str, Any],
    limit: Optional[int] = Query(100, le=1000),
    offset: Optional[int] = Query(0, ge=0)
) -> Dict[str, Any]:
    """
    Advanced filtering with POST request body.
    Allows complex filter combinations.
    
    Example body:
    {
        "state": ["WB", "UP", "TN"],
        "sex": "M",
        "CategoryV7": [11578, 2369],
        "DiaryDate": {"from": "2023-01-01", "to": "2023-12-31"}
    }
    """
    try:
        results = grievance_service.get_grievances(
            filters=filters,
            limit=limit,
            offset=offset
        )
        return results
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")


@router.get("/unique-values/{field}")
async def get_unique_values(field: str) -> Dict[str, Any]:
    """
    Get unique values for a specific field.
    Useful for building filter dropdowns.
    """
    try:
        # List of allowed fields
        allowed_fields = [
            "_id", "state", "org_code", "sex", "CategoryV7", 
            "DiaryDate", "recvd_date", "closing_date", "resolution_date",
            "dist_name", "pincode", "v7_target", "UserCode", "registration_no"
        ]
        
        if field not in allowed_fields:
            raise HTTPException(
                status_code=400, 
                detail=f"Field '{field}' not allowed. Allowed fields: {allowed_fields}"
            )
        
        unique_values = grievance_service.get_unique_values(field)
        
        return {
            "field": field,
            "unique_values": unique_values,
            "count": len(unique_values),
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting unique values: {str(e)}")


@router.get("/statistics/{field}")
async def get_field_statistics(field: str) -> Dict[str, Any]:
    """
    Get distribution statistics for a specific field.
    Returns count of each unique value.
    """
    try:
        # List of allowed fields
        allowed_fields = [
            "state", "org_code", "sex", "CategoryV7", 
            "DiaryDate", "recvd_date", "closing_date", "resolution_date",
            "dist_name", "v7_target"
        ]
        
        if field not in allowed_fields:
            raise HTTPException(
                status_code=400, 
                detail=f"Field '{field}' not allowed for statistics. Allowed fields: {allowed_fields}"
            )
        
        stats = grievance_service.get_field_statistics(field)
        return stats
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting field statistics: {str(e)}")


@router.get("/schema")
async def get_schema() -> Dict[str, Any]:
    """
    Get the schema/structure of grievance data.
    Shows available fields and their types.
    """
    return {
        "fields": {
            "_id": {"type": "string", "description": "Unique grievance ID"},
            "state": {"type": "string", "description": "State code (e.g., WB, UP, TN)"},
            "org_code": {"type": "string", "description": "Organization code"},
            "sex": {"type": "string", "description": "Gender (M/F)"},
            "CategoryV7": {"type": "integer", "description": "Category V7 number"},
            "DiaryDate": {"type": "date", "description": "Diary date"},
            "recvd_date": {"type": "date", "description": "Received date"},
            "closing_date": {"type": "date", "description": "Closing date"},
            "resolution_date": {"type": "date", "description": "Resolution date"},
            "dist_name": {"type": "string", "description": "District name"},
            "pincode": {"type": "string", "description": "Pincode"},
            "v7_target": {"type": "string", "description": "V7 target (Yes/No)"},
            "UserCode": {"type": "string", "description": "User code"},
            "registration_no": {"type": "string", "description": "Registration number"},
            "remarks_text": {"type": "text", "description": "Remarks text"},
            "subject_content_text": {"type": "text", "description": "Subject content text"}
        },
        "filtering": {
            "simple_filters": "Use query parameters for simple filtering",
            "date_ranges": "Use _from and _to suffixes for date ranges",
            "complex_filters": "Use POST /filter for complex combinations",
            "pagination": "Use limit and offset parameters"
        },
        "timestamp": datetime.now().isoformat()
    }


@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """Health check for grievance service"""
    try:
        # Test a simple query
        test_result = grievance_service.get_grievances(limit=1)
        return {
            "status": "healthy",
            "total_records": test_result["total_count"],
            "service": "grievance-data",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Service unhealthy: {str(e)}") 