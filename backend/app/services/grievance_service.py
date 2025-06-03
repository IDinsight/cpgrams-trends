import subprocess
import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime


class GrievanceService:
    """Service for querying grievance data using jq"""
    
    def __init__(self):
        self.data_file = os.path.join(os.path.dirname(__file__), "../../../data/no_pii_grievance_v2.json")
    
    def _execute_jq(self, query: str) -> Any:
        """Execute a jq query on the grievance data file"""
        try:
            cmd = ["jq", "-c", query, self.data_file]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return json.loads(result.stdout)
        except subprocess.CalledProcessError as e:
            raise Exception(f"jq query failed: {e.stderr}")
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse jq output: {str(e)}")
    
    def _normalize_date_value(self, date_obj: Any) -> Optional[str]:
        """Extract date string from MongoDB date object"""
        if isinstance(date_obj, dict) and "$date" in date_obj:
            return date_obj["$date"]
        return date_obj
    
    def _normalize_number_value(self, num_obj: Any) -> Optional[int]:
        """Extract number from MongoDB NumberLong object"""
        if isinstance(num_obj, dict) and "$numberLong" in num_obj:
            return int(num_obj["$numberLong"])
        return num_obj
    
    def _build_jq_filter(self, filters: Dict[str, Any]) -> str:
        """Build jq filter expression from provided filters"""
        filter_conditions = []
        
        for field, value in filters.items():
            if value is None:
                continue
                
            if field in ["CategoryV7"]:
                # Handle NumberLong fields
                if isinstance(value, list):
                    conditions = [f'(.{field}."$numberLong" | tonumber) == {v}' for v in value]
                    filter_conditions.append(f'({" or ".join(conditions)})')
                else:
                    filter_conditions.append(f'(.{field}."$numberLong" | tonumber) == {value}')
            
            elif field in ["DiaryDate", "recvd_date", "closing_date", "resolution_date"]:
                # Handle date fields
                if isinstance(value, dict):
                    if "from" in value and "to" in value:
                        filter_conditions.append(f'(.{field}."$date" >= "{value["from"]}") and (.{field}."$date" <= "{value["to"]}")')
                    elif "from" in value:
                        filter_conditions.append(f'.{field}."$date" >= "{value["from"]}"')
                    elif "to" in value:
                        filter_conditions.append(f'.{field}."$date" <= "{value["to"]}"')
                else:
                    filter_conditions.append(f'.{field}."$date" | startswith("{value}")')
            
            else:
                # Handle regular string fields
                if isinstance(value, list):
                    # For array values, use OR conditions
                    conditions = [f'.{field} == "{v}"' for v in value]
                    filter_conditions.append(f'({" or ".join(conditions)})')
                else:
                    filter_conditions.append(f'.{field} == "{value}"')
        
        if not filter_conditions:
            return "."
        
        return f'[.[] | select({" and ".join(filter_conditions)})]'
    
    def get_grievances(self, 
                      filters: Optional[Dict[str, Any]] = None,
                      limit: Optional[int] = None,
                      offset: Optional[int] = None) -> Dict[str, Any]:
        """
        Get grievances with optional filtering, pagination
        
        Args:
            filters: Dictionary of field filters
            limit: Number of records to return
            offset: Number of records to skip
            
        Returns:
            Dictionary with results and metadata
        """
        
        # Build the jq query
        if filters:
            jq_filter = self._build_jq_filter(filters)
        else:
            jq_filter = "."
        
        # Add pagination if specified
        if offset is not None and limit is not None:
            jq_query = f'{jq_filter} | .[{offset}:{offset + limit}]'
        elif limit is not None:
            jq_query = f'{jq_filter} | .[:{limit}]'
        elif offset is not None:
            jq_query = f'{jq_filter} | .[{offset}:]'
        else:
            jq_query = jq_filter
        
        # Execute the query
        results = self._execute_jq(jq_query)
        
        # Get total count for metadata
        count_query = f'{jq_filter} | length' if filters else '. | length'
        total_count = self._execute_jq(count_query)
        
        return {
            "data": results,
            "total_count": total_count,
            "returned_count": len(results),
            "filters_applied": filters or {},
            "limit": limit,
            "offset": offset,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_grievance_by_id(self, grievance_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific grievance by its ID
        
        Args:
            grievance_id: The unique grievance ID
            
        Returns:
            Single grievance record or None if not found
        """
        try:
            # Use jq to find the specific grievance by ID
            query = f'[.[] | select(._id == "{grievance_id}")] | .[0] // null'
            result = self._execute_jq(query)
            
            return result if result else None
            
        except Exception as e:
            raise Exception(f"Error retrieving grievance by ID: {str(e)}")
    
    def get_unique_values(self, field: str) -> List[Any]:
        """Get unique values for a specific field"""
        if field in ["CategoryV7"]:
            query = f'[.[] | .{field}."$numberLong" | tonumber] | unique | sort'
        elif field in ["DiaryDate", "recvd_date", "closing_date", "resolution_date"]:
            query = f'[.[] | .{field}."$date"] | unique | sort'
        else:
            query = f'[.[] | .{field}] | unique | sort'
        
        return self._execute_jq(query)
    
    def get_field_statistics(self, field: str) -> Dict[str, Any]:
        """Get basic statistics for a field"""
        if field in ["CategoryV7"]:
            # Count by CategoryV7, handling null values
            query = f'group_by(.{field}."$numberLong" // "null") | map({{value: (.[0].{field}."$numberLong" | if . == null then "null" else (. | tonumber) end), count: length}}) | sort_by(-.count)'
        elif field in ["DiaryDate", "recvd_date", "closing_date", "resolution_date"]:
            # Count by date (year-month)
            query = f'group_by(.{field}."$date" | split("T")[0] | split("-") | .[0:2] | join("-")) | map({{value: .[0].{field}."$date" | split("T")[0] | split("-") | .[0:2] | join("-"), count: length}}) | sort_by(-.count)'
        else:
            # Count by field value
            query = f'group_by(.{field}) | map({{value: .[0].{field}, count: length}}) | sort_by(-.count)'
        
        stats = self._execute_jq(query)
        
        return {
            "field": field,
            "unique_values": len(stats),
            "distribution": stats,
            "timestamp": datetime.now().isoformat()
        } 