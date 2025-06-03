#!/bin/bash

echo "🔧 CPGrams Trends - Initial Setup"
echo "=================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check dependencies
print_status "Checking system dependencies..."

# Check Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d ' ' -f 2)
    print_success "Python $PYTHON_VERSION found"
else
    print_error "Python 3.9+ is required but not installed"
    exit 1
fi

# Check Node.js
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    print_success "Node.js $NODE_VERSION found"
else
    print_error "Node.js 18+ is required but not installed"
    exit 1
fi

# Check package manager preference
PACKAGE_MANAGER="npm"
if command -v pnpm &> /dev/null; then
    PACKAGE_MANAGER="pnpm"
    print_success "Using pnpm as package manager"
elif command -v yarn &> /dev/null; then
    PACKAGE_MANAGER="yarn"
    print_success "Using yarn as package manager"
else
    print_success "Using npm as package manager"
fi

# Setup Backend
print_status "Setting up FastAPI backend..."
cd backend

if [ ! -d "venv" ]; then
    print_status "Creating Python virtual environment..."
    python3 -m venv venv
    print_success "Virtual environment created"
fi

print_status "Activating virtual environment and installing dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
print_success "Backend dependencies installed"

cd ..

# Setup Frontend
print_status "Setting up Next.js frontend..."
cd frontend

print_status "Installing frontend dependencies..."
if [ "$PACKAGE_MANAGER" = "pnpm" ]; then
    pnpm install
elif [ "$PACKAGE_MANAGER" = "yarn" ]; then
    yarn install
else
    npm install --legacy-peer-deps
fi
print_success "Frontend dependencies installed"

cd ..

# Create environment file
print_status "Creating environment configuration..."
if [ ! -f "frontend/.env.local" ]; then
    echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > frontend/.env.local
    print_success "Environment file created"
fi

print_success "Setup completed successfully!"
echo ""
echo "=================================="
echo "🎉 CPGrams Trends is ready to use!"
echo "=================================="
echo ""
echo "To start the application:"
echo "1. Start backend:  ./start-backend.sh"
echo "2. Start frontend: ./start-frontend.sh"
echo ""
echo "Or run both with:"
echo "Backend:  cd backend && source venv/bin/activate && uvicorn app.main:app --reload"
echo "Frontend: cd frontend && $PACKAGE_MANAGER dev"
echo ""
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend:  http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs" 