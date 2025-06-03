# CPGrams Grievance Data API Usage Guide

## Overview

This API provides flexible access to CPGrams grievance data (175,784 records) with powerful filtering capabilities using jq for efficient processing of large JSON files.

## Base URL

```
http://localhost:8000
```

## Available Endpoints

### 1. Health Check

```bash
GET /api/grievances/health
```

**Response:**

```json
{
  "status": "healthy",
  "total_records": 175784,
  "service": "grievance-data",
  "timestamp": "2025-06-03T18:14:02.572137"
}
```

### 2. Schema Information

```bash
GET /api/grievances/schema
```

Returns available fields and their types, plus filtering documentation.

### 3. Get Grievances (Simple Filtering)

```bash
GET /api/grievances/?[query_parameters]
```

**Query Parameters:**

- `state` - Filter by state code (e.g., WB, UP, TN)
- `org_code` - Filter by organization code
- `sex` - Filter by gender (M/F)
- `CategoryV7` - Filter by category V7 number
- `dist_name` - Filter by district name
- `pincode` - Filter by pincode
- `v7_target` - Filter by V7 target (Yes/No)
- `diary_date_from` - Filter DiaryDate from (YYYY-MM-DD)
- `diary_date_to` - Filter DiaryDate to (YYYY-MM-DD)
- `recvd_date_from` - Filter received date from (YYYY-MM-DD)
- `recvd_date_to` - Filter received date to (YYYY-MM-DD)
- `closing_date_from` - Filter closing date from (YYYY-MM-DD)
- `closing_date_to` - Filter closing date to (YYYY-MM-DD)
- `limit` - Number of records to return (max 1000, default 100)
- `offset` - Number of records to skip (default 0)

**Examples:**

```bash
# Get 5 records
curl "http://localhost:8000/api/grievances/?limit=5"

# Filter by state
curl "http://localhost:8000/api/grievances/?state=WB&limit=3"

# Date range filtering
curl "http://localhost:8000/api/grievances/?diary_date_from=2023-01-01&diary_date_to=2023-01-31&limit=5"

# Multiple filters
curl "http://localhost:8000/api/grievances/?state=UP&sex=M&limit=10"
```

### 4. Advanced Filtering (POST)

```bash
POST /api/grievances/filter?limit=100&offset=0
Content-Type: application/json
```

**Request Body Examples:**

Simple filtering:

```json
{
  "state": "WB",
  "sex": "M"
}
```

Array filtering (multiple values):

```json
{
  "state": ["WB", "UP", "TN"],
  "sex": "M",
  "CategoryV7": [11578, 2369]
}
```

Date range filtering:

```json
{
  "state": "WB",
  "DiaryDate": {
    "from": "2023-01-01",
    "to": "2023-01-31"
  }
}
```

Complex combination:

```json
{
  "state": ["WB", "UP"],
  "sex": "M",
  "v7_target": "Yes",
  "recvd_date": {
    "from": "2023-01-01",
    "to": "2023-12-31"
  }
}
```

### 5. Get Unique Values

```bash
GET /api/grievances/unique-values/{field}
```

**Allowed fields:**

- `_id`, `state`, `org_code`, `sex`, `CategoryV7`
- `DiaryDate`, `recvd_date`, `closing_date`, `resolution_date`
- `dist_name`, `pincode`, `v7_target`, `UserCode`, `registration_no`

**Example:**

```bash
curl "http://localhost:8000/api/grievances/unique-values/state"
```

**Response:**

```json
{
  "field": "state",
  "unique_values": ["WB", "UP", "TN", "MH", ...],
  "count": 41,
  "timestamp": "2025-06-03T18:14:02.572137"
}
```

### 6. Field Statistics

```bash
GET /api/grievances/statistics/{field}
```

**Allowed fields:**

- `state`, `org_code`, `sex`, `CategoryV7`
- `DiaryDate`, `recvd_date`, `closing_date`, `resolution_date`
- `dist_name`, `v7_target`

**Example:**

```bash
curl "http://localhost:8000/api/grievances/statistics/state"
```

**Response:**

```json
{
  "field": "state",
  "unique_values": 41,
  "distribution": [
    { "value": "UP", "count": 39334 },
    { "value": "BH", "count": 16295 },
    { "value": "MH", "count": 15206 }
  ],
  "timestamp": "2025-06-03T18:14:02.572137"
}
```

## Response Format

All responses include:

- `data` - Array of matching records
- `total_count` - Total number of matching records
- `returned_count` - Number of records in this response
- `filters_applied` - Echo of applied filters
- `limit` - Applied limit
- `offset` - Applied offset
- `timestamp` - Response timestamp

## Data Structure

Each grievance record contains:

- `_id` - Unique grievance ID
- `state` - State code (WB, UP, TN, etc.)
- `org_code` - Organization code
- `sex` - Gender (M/F)
- `CategoryV7` - Category V7 number (MongoDB NumberLong format)
- `DiaryDate` - Diary date (MongoDB ISODate format)
- `recvd_date` - Received date
- `closing_date` - Closing date
- `resolution_date` - Resolution date
- `dist_name` - District name
- `pincode` - Pincode
- `v7_target` - V7 target (Yes/No)
- `UserCode` - User code
- `registration_no` - Registration number
- `remarks_text` - Remarks text
- `subject_content_text` - Subject content text

## Date Handling

Dates are stored in MongoDB extended JSON format:

```json
{
  "$date": "2023-01-01T00:00:19.977+0000"
}
```

For filtering, use ISO date strings (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS).

## Performance Notes

- The API uses `jq` for efficient processing of large JSON files
- Pagination is recommended for large result sets
- Use specific filters to reduce response times
- Maximum limit is 1000 records per request

## Error Handling

The API returns appropriate HTTP status codes:

- `200` - Success
- `400` - Bad request (invalid field names, etc.)
- `500` - Server error (jq processing error, etc.)

Error responses include a `detail` field with error description.

## Top States by Grievance Count

1. **UP** - 39,334 grievances
2. **BH** - 16,295 grievances
3. **MH** - 15,206 grievances
4. **DH** - 12,380 grievances
5. **GJ** - 9,891 grievances

## Integration Examples

### Python

```python
import requests

# Simple filtering
response = requests.get("http://localhost:8000/api/grievances/",
                       params={"state": "WB", "limit": 10})
data = response.json()

# Advanced filtering
filters = {
    "state": ["WB", "UP"],
    "sex": "M",
    "DiaryDate": {"from": "2023-01-01", "to": "2023-12-31"}
}
response = requests.post("http://localhost:8000/api/grievances/filter",
                        json=filters, params={"limit": 100})
data = response.json()
```

### JavaScript

```javascript
// Simple filtering
const response = await fetch(
  "http://localhost:8000/api/grievances/?state=WB&limit=10"
);
const data = await response.json();

// Advanced filtering
const filters = {
  state: ["WB", "UP"],
  sex: "M",
  DiaryDate: { from: "2023-01-01", to: "2023-12-31" },
};
const response = await fetch(
  "http://localhost:8000/api/grievances/filter?limit=100",
  {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(filters),
  }
);
const data = await response.json();
```
