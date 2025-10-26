import json
import sys
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from agent.safety_agents import create_runner, run_agent_system
from pipeline.pipeline import run_video_model

app = FastAPI(
    title="Construction Safety Agent API",
    description="AI-powered real-time safety monitoring",
    version="1.0.0",
)

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "Construction Safety Agent API",
        "version": "1.0.0",
    }


@app.post("/api/analyze")
async def analyze_video(file: UploadFile):
    """
    Analyze construction site video for safety hazards

    Args:
        file: Video file (mp4, mov, avi)

    Returns:
        JSON with event data, agent analysis, and execution trace
    """
    # Validate file type
    if not file.content_type or not file.content_type.startswith("video/"):
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Please upload a video file.",
        )

    # Read video bytes
    video_bytes = await file.read()
    video_id = f"api_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    try:
        # Run video analysis with Gemini
        event_json = run_video_model(video_bytes, video_id)
        event_data = json.loads(event_json)

        # Run agent system
        runner = create_runner(verbose=False)
        agent_output = run_agent_system(event_json, runner)

        # Get structured trace data
        traces = runner.logger.traces
        trace_data = [
            {
                "agent_name": t.agent_name,
                "start_time": t.start_time,
                "end_time": t.end_time,
                "duration_ms": t.duration_ms,
                "iterations": t.iterations,
                "handoff_to": t.handoff_to,
                "final_output": t.final_output,
                "tool_calls": [
                    {
                        "tool_name": tc.tool_name,
                        "arguments": tc.arguments,
                        "result": tc.result,
                        "duration_ms": tc.duration_ms,
                        "timestamp": tc.timestamp,
                        "success": tc.success,
                        "error": tc.error,
                    }
                    for tc in t.tool_calls
                ],
            }
            for t in traces
        ]

        return {
            "status": "success",
            "video_id": video_id,
            "event": event_data,
            "agent_output": agent_output,
            "trace": trace_data,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {e!s}",
        ) from e


@app.get("/api/health")
def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "gemini": "configured" if "GEMINI_API_KEY" in str(Path.cwd()) else "check env",
        "nvidia": "configured" if "NVIDIA_API_KEY" in str(Path.cwd()) else "check env",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
