# CPGrams Trends Backend

FastAPI backend service providing REST API endpoints for dashboard data and chart analytics.

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- pip or poetry

### Installation

1. Create and activate virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the server:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:

- Main API: `http://localhost:8000`
- Swagger docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 📚 API Documentation

### Health Check

- `GET /api/health` - Service health status

### Chart Data Endpoints

- `GET /api/charts/sales` - Monthly sales data
- `GET /api/charts/performance` - Performance metrics (KPIs)
- `GET /api/charts/analytics` - Analytics data for donut charts
- `GET /api/charts/kpi-cards` - KPI card data
- `GET /api/charts/time-series` - Time series data for line charts
- `GET /api/charts/donut-data` - Formatted donut chart data
- `GET /api/charts/revenue-by-month` - Monthly revenue data

### Example Response

```json
{
  "sales": [
    {
      "month": "Jan",
      "sales": 25000.5,
      "profit": 7500.25,
      "customers": 150
    }
  ]
}
```

## 🏗️ Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI application
│   │   ├── __init__.py
│   │   └── chart_models.py  # Pydantic models
│   ├── routers/
│   │   ├── __init__.py
│   │   └── charts.py        # Chart API endpoints
│   └── services/            # Business logic (future)
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🔧 Development

### Running in Development Mode

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Environment Variables

Create a `.env` file for environment-specific configurations:

```env
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

## 🛠️ Technology Stack

- **FastAPI** - Modern Python web framework
- **Pydantic** - Data validation and serialization
- **Uvicorn** - ASGI server implementation
- **Python-CORS** - Cross-Origin Resource Sharing

## 📝 Adding New Endpoints

1. Create models in `app/models/`
2. Add routers in `app/routers/`
3. Include router in `app/main.py`
4. Update API documentation

## 🧪 Testing

```bash
# Install test dependencies
pip install pytest httpx

# Run tests (when available)
pytest
```
