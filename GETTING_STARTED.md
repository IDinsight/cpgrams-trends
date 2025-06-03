# 🚀 Getting Started with CPGrams Trends

Welcome to CPGrams Trends - a modern full-stack dashboard application with FastAPI backend and Next.js frontend using [Tremor](https://github.com/tremorlabs/tremor) components for beautiful charts.

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.9+** - For the FastAPI backend
- **Node.js 18+** - For the Next.js frontend
- **Git** - For version control
- **pnpm** (recommended) or **npm** - For frontend package management

## 🔧 Quick Setup

### Option 1: Automated Setup (Recommended)

Run the setup script to automatically configure both backend and frontend:

```bash
# Make the script executable and run
chmod +x setup.sh
./setup.sh
```

This script will:

- Check system dependencies
- Set up Python virtual environment
- Install backend dependencies
- Install frontend dependencies
- Create environment configuration

### Option 2: Manual Setup

#### Backend Setup

1. Navigate to backend directory:

   ```bash
   cd backend
   ```

2. Create and activate virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

#### Frontend Setup

1. Navigate to frontend directory:

   ```bash
   cd frontend
   ```

2. Install dependencies:

   ```bash
   pnpm install  # or npm install --legacy-peer-deps
   ```

3. Create environment file:
   ```bash
   echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
   ```

## 🏃‍♂️ Running the Application

### Option 1: Using Scripts (Recommended)

Start both services with the provided scripts:

**Terminal 1 - Backend:**

```bash
./start-backend.sh
```

**Terminal 2 - Frontend:**

```bash
./start-frontend.sh
```

### Option 2: Manual Start

**Backend:**

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend:**

```bash
cd frontend
pnpm dev  # or npm run dev
```

### Option 3: Docker Compose

Run both services with Docker:

```bash
docker-compose up --build
```

## 🌐 Accessing the Application

Once both services are running:

- **Frontend Dashboard**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Alternative API Docs**: http://localhost:8000/redoc

## 📊 Features Overview

### Dashboard Components

The frontend includes these interactive Tremor components:

1. **KPI Cards** - Key performance indicators with trend arrows
2. **Sales Area Chart** - Monthly sales and profit visualization
3. **Department Donut Chart** - Distribution by department
4. **Time Series Line Chart** - Website traffic over time
5. **Revenue Bar Chart** - Monthly revenue vs profit comparison

### API Endpoints

The backend provides these RESTful endpoints:

- `GET /api/health` - Health check
- `GET /api/charts/kpi-cards` - KPI metrics
- `GET /api/charts/sales` - Sales data
- `GET /api/charts/donut-data` - Donut chart data
- `GET /api/charts/time-series` - Time series data
- `GET /api/charts/revenue-by-month` - Revenue data

## 🛠️ Technology Stack

### Backend

- **FastAPI** - Modern Python web framework
- **Pydantic** - Data validation and serialization
- **Uvicorn** - ASGI server

### Frontend

- **Next.js 14** - React framework with App Router
- **TypeScript** - Type safety
- **Tremor** - Beautiful chart components
- **Tailwind CSS** - Utility-first styling
- **Lucide React** - Icons

## 🔧 Development

### Project Structure

```
cpgrams-trends/
├── backend/                 # FastAPI server
│   ├── app/
│   │   ├── main.py         # FastAPI application
│   │   ├── models/         # Pydantic models
│   │   └── routers/        # API endpoints
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile         # Backend container
├── frontend/               # Next.js application
│   ├── src/
│   │   ├── app/           # App router pages
│   │   ├── components/    # Chart components
│   │   ├── lib/          # API utilities
│   │   └── types/        # TypeScript types
│   ├── package.json      # Node dependencies
│   └── Dockerfile        # Frontend container
├── docker-compose.yml     # Container orchestration
├── setup.sh              # Automated setup
└── README.md             # Project overview
```

### Adding New Charts

1. **Backend**: Add new endpoint in `backend/app/routers/charts.py`
2. **Frontend**: Create component in `frontend/src/components/`
3. **Types**: Define TypeScript interfaces in `frontend/src/types/`
4. **API**: Add API function in `frontend/src/lib/api.ts`

### Environment Variables

#### Frontend (.env.local)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

#### Backend (optional .env)

```env
API_HOST=0.0.0.0
API_PORT=8000
```

## 🐳 Docker Deployment

### Build and Run

```bash
# Build and start services
docker-compose up --build

# Run in background
docker-compose up -d --build

# Stop services
docker-compose down
```

### Individual Services

```bash
# Backend only
docker build -t cpgrams-backend ./backend
docker run -p 8000:8000 cpgrams-backend

# Frontend only
docker build -t cpgrams-frontend ./frontend
docker run -p 3000:3000 cpgrams-frontend
```

## 🚨 Troubleshooting

### Common Issues

1. **Port Already in Use**

   ```bash
   # Kill processes on ports 3000 or 8000
   lsof -ti:3000 | xargs kill -9
   lsof -ti:8000 | xargs kill -9
   ```

2. **Python Virtual Environment Issues**

   ```bash
   # Recreate virtual environment
   rm -rf backend/venv
   cd backend && python -m venv venv
   ```

3. **Node Modules Issues**

   ```bash
   # Clear and reinstall
   cd frontend
   rm -rf node_modules package-lock.json
   npm install --legacy-peer-deps
   ```

4. **API Connection Errors**
   - Ensure backend is running on port 8000
   - Check `NEXT_PUBLIC_API_URL` in frontend/.env.local
   - Verify CORS settings in backend/app/main.py

## 📚 Next Steps

1. **Customize Data**: Modify the sample data in `backend/app/routers/charts.py`
2. **Add Charts**: Create new Tremor components for additional visualizations
3. **Styling**: Customize the Tailwind CSS styling in components
4. **Deploy**: Use Vercel (frontend) and Railway/Heroku (backend) for hosting

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test both services
5. Submit a pull request

---

**Need Help?** Check the individual READMEs in `/backend` and `/frontend` directories for more detailed information.
