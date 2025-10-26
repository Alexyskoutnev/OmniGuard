#!/bin/bash


if [ -z "$GEMINI_API_KEY" ]; then
    echo "Warning: GEMINI_API_KEY not set"
    echo "   Set it with: export GEMINI_API_KEY='your-key'"
fi

if [ -z "$NVIDIA_API_KEY" ]; then
    echo "NVIDIA_API_KEY not set (will use default)"
fi

echo ""
echo "Backend will run at: http://localhost:8000"
echo ""

# Navigate to api directory and run server
cd "$(dirname "$0")/api"

# Install dependencies if needed
if [ ! -d "../.venv" ]; then
    echo "📦 Installing dependencies..."
    cd ..
    uv pip install -r api/requirements.txt
    cd api
fi

uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
