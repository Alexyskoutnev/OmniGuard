# Quick Start Guide

Get the Safety Agent web application running in 2 minutes.

## Prerequisites

- Python 3.11+
- Node.js 18+
- Gemini API Key

## Setup

### 1. Set Your API Key

```bash
export GEMINI_API_KEY="your-gemini-api-key-here"
```

Optional:
```bash
export NVIDIA_API_KEY="your-nvidia-api-key"  # Has default if not set
```

### 2. Run the Application

**Option A: Run Everything (Recommended)**
```bash
./run_all.sh
```

This starts both backend and frontend. Press Ctrl+C to stop.

**Option B: Run Separately**

Terminal 1 (Backend):
```bash
./run_backend.sh
```

Terminal 2 (Frontend):
```bash
./run_frontend.sh
```

## Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## Usage

1. Open http://localhost:3000 in your browser
2. Upload a construction site video (MP4, MOV, or AVI)
3. Click "Analyze Video"
4. View results:
   - Safety metrics
   - Scene analysis
   - Agent recommendations
   - Execution trace
5. Download reports as needed

## Troubleshooting

### Backend won't start
- Check GEMINI_API_KEY is set: `echo $GEMINI_API_KEY`
- View backend logs: `tail -f backend.log`

### Frontend won't start
- Delete node_modules and reinstall: `cd frontend && rm -rf node_modules && npm install`
- View frontend logs: `tail -f frontend.log`

### CORS errors
- Ensure backend is running first
- Check backend shows "Application startup complete"

### API connection failed
- Verify backend is accessible: `curl http://localhost:8000`
- Check firewall/antivirus isn't blocking ports

## First-Time Setup

The scripts automatically:
- Install Python dependencies (via uv)
- Install Node dependencies (via npm)
- Start both services with auto-reload

## Stopping the Application

- **run_all.sh**: Press Ctrl+C once
- **Separate terminals**: Press Ctrl+C in each terminal

## Next Steps

- Read full documentation:
  - `api/README.md` - Backend API details
  - `frontend/README.md` - Frontend customization
- Deploy to production (see main README.md)
- Customize the UI theme (`frontend/src/theme.ts`)

## Support

If you encounter issues:
1. Check the logs (`backend.log` and `frontend.log`)
2. Verify API keys are set correctly
3. Ensure ports 3000 and 8000 are available
