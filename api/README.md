# Safety Agent API

FastAPI backend for the Construction Safety Agent System.

## Quick Start

### 1. Install Dependencies

```bash
cd api
uv pip install -r requirements.txt
```

### 2. Set Environment Variables

```bash
export GEMINI_API_KEY="your-gemini-api-key"
export NVIDIA_API_KEY="your-nvidia-api-key"  # Optional
```

### 3. Run the Server

```bash
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Or with Python directly:

```bash
uv run python main.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

### `GET /`
Health check endpoint

**Response:**
```json
{
  "status": "online",
  "service": "Construction Safety Agent API",
  "version": "1.0.0"
}
```

### `POST /api/analyze`
Analyze construction site video

**Request:**
- Content-Type: `multipart/form-data`
- Body: `file` (video file)

**Response:**
```json
{
  "status": "success",
  "video_id": "api_20231120_143022",
  "event": {
    "video_id": "...",
    "safety_status": "HIGH",
    "scene_description": "...",
    "predictions": {...},
    "safety_response": "..."
  },
  "agent_output": "Agent analysis result...",
  "trace": [
    {
      "agent_name": "Safety Router Agent",
      "start_time": "2023-11-20T14:30:22.123",
      "end_time": "2023-11-20T14:30:23.456",
      "duration_ms": 1333,
      "iterations": 2,
      "handoff_to": "EMS Safety Agent",
      "final_output": "...",
      "tool_calls": [
        {
          "tool_name": "detect_ems_hazard",
          "arguments": {...},
          "result": "...",
          "duration_ms": 250,
          "timestamp": "...",
          "success": true,
          "error": null
        }
      ]
    }
  ]
}
```

### `GET /api/health`
Detailed health check

**Response:**
```json
{
  "status": "healthy",
  "gemini": "configured",
  "nvidia": "configured"
}
```

## Development

### Auto-reload
```bash
uv run uvicorn main:app --reload
```

### API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## CORS

The API allows requests from:
- `http://localhost:3000` (React dev server)
- `http://localhost:5173` (Vite dev server)

## Deployment

### Docker

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install uv
RUN uv pip install -r requirements.txt

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t safety-agent-api .
docker run -p 8000:8000 \
  -e GEMINI_API_KEY=your-key \
  -e NVIDIA_API_KEY=your-key \
  safety-agent-api
```
