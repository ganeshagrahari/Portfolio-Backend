#!/bin/bash

echo "🚀 Starting Ganesh's AI Assistant Backend"
echo "=========================================="
echo ""

# Activate virtual environment
source venv/bin/activate

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found!"
    echo "💡 Run: bash setup_env.sh"
    exit 1
fi

# Start the server
echo "🌐 Starting FastAPI server..."
echo "📍 Local: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
