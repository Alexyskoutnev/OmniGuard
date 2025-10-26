# Safety Agent System - Streamlit Demo

Professional investor-ready demo application for the Construction Safety Agent System.

## Features

- **Video Upload**: Upload construction site videos for analysis
- **Real-time Analysis**: Watch as Gemini 2.5 Pro analyzes the video
- **Multi-Agent Processing**: See agents in action with live trace
- **Professional UI**: Clean, investor-friendly interface
- **Detailed Results**: Safety status, risk probability, incident classification
- **Agent Trace Viewer**: See every step of the agent decision-making process
- **Export Reports**: Download event data, reports, and trace logs

## Quick Start

### 1. Install Dependencies

```bash
uv pip install streamlit google-genai
```

### 2. Set API Keys

```bash
export GEMINI_API_KEY="your-gemini-api-key"
export NVIDIA_API_KEY="your-nvidia-api-key"  # Optional, has default
```

### 3. Run the App

```bash
uv run streamlit run streamlit_app.py
```

The app will open in your browser at `http://localhost:8501`

## Usage

1. **Upload Video**: Click "Choose a video file" and select a construction site video
2. **Analyze**: Click "🚀 Analyze Video" to start processing
3. **View Results**: See real-time analysis results including:
   - Safety status (SAFE, LOW, MEDIUM, HIGH, EXTREME)
   - Risk probability
   - Incident type classification
   - Scene description
   - Recommended safety response
4. **Agent Trace**: Expand the trace viewer to see agent execution details
5. **Export**: Download JSON event data, text reports, or trace logs

## Demo Video Suggestions

For best investor demo results, use videos showing:
- ✅ Medical emergencies (worker distress, heat exhaustion)
- ✅ Fire hazards (welding near combustibles, smoke)
- ✅ PPE violations (missing hard hats, no high-vis vests)
- ✅ Clear safety concerns with visible workers

## Interface Layout

### Main Dashboard
- **Header**: System branding and description
- **Metrics Row**: 4-card summary (Safety Status, Risk %, Incident Type, Video ID)
- **Scene Analysis**: Gemini's video interpretation
- **Safety Response**: Recommended immediate actions
- **Agent Output**: Multi-agent system response
- **Agent Trace**: Expandable execution trace viewer
- **Export Section**: Download buttons for all data

### Sidebar
- System overview
- Technology stack
- Reset button

## Customization

### Styling

Edit the CSS in `streamlit_app.py` to customize colors and layout:

```python
st.markdown("""
<style>
    .main-header { color: #your-color; }
    .metric-card { background: #your-bg; }
</style>
""", unsafe_allow_html=True)
```

### Adding Features

The app is modular - you can easily add:
- Real-time video streaming
- Multiple video comparison
- Historical analysis dashboard
- Custom reporting templates

## Deployment

### Streamlit Cloud

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Add secrets for API keys in Settings → Secrets:
```toml
GEMINI_API_KEY = "your-key"
NVIDIA_API_KEY = "your-key"
```
5. Deploy!

### Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

# Install uv
RUN pip install uv
RUN uv pip install streamlit google-genai

EXPOSE 8501

CMD ["uv", "run", "streamlit", "run", "streamlit_app.py", "--server.address", "0.0.0.0"]
```

```bash
docker build -t safety-agent-demo .
docker run -p 8501:8501 \
  -e GEMINI_API_KEY=your-key \
  -e NVIDIA_API_KEY=your-key \
  safety-agent-demo
```

## Troubleshooting

### Video not processing
- Check API keys are set correctly
- Ensure video is MP4 format and < 20MB
- Check internet connection for API calls

### Trace not showing
- Ensure `verbose=True` in runner creation
- Check logging configuration
- Verify handler is capturing stdout

### Slow analysis
- Gemini 2.5 Pro can take 10-30s for video analysis
- Use shorter videos for demos (< 30 seconds)
- Consider caching results for repeat demos

## Tips for Investor Demos

1. **Pre-load Videos**: Have 2-3 demo videos ready
2. **Highlight Metrics**: Emphasize the risk probability and instant detection
3. **Show Trace**: Expand the agent trace to show multi-agent collaboration
4. **Explain Value**: Focus on reducing workplace accidents and compliance costs
5. **Speed**: Use short videos (10-20s) for quick demos
6. **Reset Between Demos**: Use sidebar reset button for clean slate

## Performance

- Video upload: < 1s
- Gemini analysis: 5-30s (depends on video length)
- Agent processing: 2-10s
- Total time: ~15-45s per video

## Support

For issues or questions, check:
- Main README.md in project root
- Pipeline README at `pipeline/README.md`
- Agent framework docs at `agent/src/README.md`
