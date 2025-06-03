#!/bin/bash

echo "🚀 Starting CPGrams Trends Frontend..."
echo "--------------------------------"

# Navigate to frontend directory
cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install --legacy-peer-deps
fi

# Start the development server
echo "🌟 Starting Next.js server on http://localhost:3000"
echo "🎨 Dashboard will open automatically"
echo "--------------------------------"
npm run dev 