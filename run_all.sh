#!/bin/bash

# Safety Agent - Run Both Frontend and Backend

echo "🚀 Starting Safety Agent System"
echo "================================"
echo ""
echo "This will start both backend and frontend."
echo "Press Ctrl+C to stop both services."
echo ""

# Check if API keys are set
if [ -z "$GEMINI_API_KEY" ]; then
    echo "❌ Error: GEMINI_API_KEY not set"
    echo "   Set it with: export GEMINI_API_KEY='your-key'"
    exit 1
fi

# Get the directory of this script
DIR="$(cd "$(dirname "$0")" && pwd)"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping services..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

trap cleanup SIGINT SIGTERM

# Start backend in background
echo "📦 Starting backend..."
cd "$DIR"
./run_backend.sh > backend.log 2>&1 &
BACKEND_PID=$!

# Wait for backend to start
echo "⏳ Waiting for backend to initialize..."
sleep 3

# Check if backend is running
if ! kill -0 $BACKEND_PID 2>/dev/null; then
    echo "❌ Backend failed to start. Check backend.log for details."
    exit 1
fi

# Start frontend in background
echo "🎨 Starting frontend..."
cd "$DIR"
./run_frontend.sh > frontend.log 2>&1 &
FRONTEND_PID=$!

# Wait for frontend to start
echo "⏳ Waiting for frontend to initialize..."
sleep 5

echo ""
echo "✅ Services running!"
echo ""
echo "📍 Frontend: http://localhost:3000"
echo "📍 Backend:  http://localhost:8000"
echo "📖 API Docs: http://localhost:8000/docs"
echo ""
echo "📋 Logs:"
echo "   Backend:  tail -f backend.log"
echo "   Frontend: tail -f frontend.log"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Wait for processes
wait $BACKEND_PID $FRONTEND_PID
