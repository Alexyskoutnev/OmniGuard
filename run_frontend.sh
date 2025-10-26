#!/bin/bash

cd "$(dirname "$0")/frontend"

if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
    echo ""
fi

echo "Frontend will run at: http://localhost:3000"

npm run dev
