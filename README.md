# CPGrams Trends Monorepo

A modern full-stack application for displaying data through interactive charts and dashboards.

## 🏗️ Architecture

This monorepo contains:

- **Backend**: FastAPI server (`/backend`) - Provides REST API endpoints for data
- **Frontend**: Next.js application (`/frontend`) - Interactive dashboard with Tremor charts

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+
- pnpm (recommended) or npm

### Backend Setup (FastAPI)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

- API docs: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

### Frontend Setup (Next.js + Tremor)

```bash
cd frontend
pnpm install
pnpm dev
```

The frontend will be available at `http://localhost:3000`

## 📊 Features

### Backend Features

- RESTful API with FastAPI
- CORS enabled for frontend integration
- Swagger/OpenAPI documentation
- Sample data endpoints for charts
- Structured data models with Pydantic

### Frontend Features

- Modern Next.js 14 with TypeScript
- Tremor UI components for charts and dashboards
- Responsive design with Tailwind CSS
- Real-time data fetching from API
- Interactive chart components

## 🛠️ Technology Stack

### Backend

- **FastAPI** - Modern Python web framework
- **Pydantic** - Data validation and serialization
- **Uvicorn** - ASGI server

### Frontend

- **Next.js 14** - React framework
- **TypeScript** - Type safety
- **Tremor** - Chart and dashboard components
- **Tailwind CSS** - Styling
- **Radix UI** - Accessible primitives

## 📁 Project Structure

```
cpgrams-trends/
├── backend/                 # FastAPI server
│   ├── app/
│   │   ├── main.py         # FastAPI application
│   │   ├── models/         # Pydantic models
│   │   ├── routers/        # API route handlers
│   │   └── services/       # Business logic
│   ├── requirements.txt    # Python dependencies
│   └── README.md          # Backend documentation
├── frontend/               # Next.js application
│   ├── src/
│   │   ├── app/           # App router pages
│   │   ├── components/    # React components
│   │   ├── lib/          # Utilities and configurations
│   │   └── types/        # TypeScript definitions
│   ├── package.json      # Node.js dependencies
│   └── README.md         # Frontend documentation
└── README.md             # This file
```

## 🔧 Development

### Running Both Services

For development, you'll need to run both services:

1. **Terminal 1** - Backend:

   ```bash
   cd backend && source venv/bin/activate && uvicorn app.main:app --reload
   ```

2. **Terminal 2** - Frontend:
   ```bash
   cd frontend && pnpm dev
   ```

### API Endpoints

The backend provides the following endpoints:

- `GET /api/health` - Health check
- `GET /api/charts/sales` - Sales data for charts
- `GET /api/charts/performance` - Performance metrics
- `GET /api/charts/analytics` - Analytics dashboard data

## 📈 Chart Types Available

Using Tremor components, the frontend supports:

- Area Charts
- Bar Charts
- Line Charts
- Donut Charts
- KPI Cards
- Data Tables
- Sparklines

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test both backend and frontend
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
