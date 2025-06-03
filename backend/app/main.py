from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime

from app.routers import charts, grievances

# Create FastAPI instance
app = FastAPI(
    title="CPGrams Trends API",
    description="A modern API for dashboard data and chart analytics",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(charts.router)
app.include_router(grievances.router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to CPGrams Trends API",
        "version": "1.0.0",
        "docs": "/docs",
        "grievance_data": {
            "endpoint": "/api/grievances",
            "health": "/api/grievances/health",
            "schema": "/api/grievances/schema"
        },
        "timestamp": datetime.now().isoformat()
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "cpgrams-trends-api"
    }


@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Custom 404 handler"""
    return JSONResponse(
        status_code=404,
        content={
            "message": "Endpoint not found",
            "available_endpoints": [
                "/docs",
                "/api/health",
                "/api/charts/sales",
                "/api/charts/performance",
                "/api/charts/analytics",
                "/api/grievances",
                "/api/grievances/by-id",
                "/api/grievances/schema",
                "/api/grievances/health"
            ]
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    ) 