import json
import logging
import sys
from datetime import datetime
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent))

from pipeline.pipeline import run_video_model

# Configure page
st.set_page_config(
    page_title="Safety Agent System",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for professional styling
st.markdown(
    """
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #6b7280;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f9fafb;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #3b82f6;
    }
    .severity-critical {
        color: #dc2626;
        font-weight: 700;
    }
    .severity-high {
        color: #ea580c;
        font-weight: 700;
    }
    .severity-medium {
        color: #d97706;
        font-weight: 700;
    }
    .severity-low {
        color: #65a30d;
        font-weight: 700;
    }
    .agent-trace {
        background: #f9fafb;
        padding: 1rem;
        border-radius: 0.5rem;
        font-family: 'Monaco', 'Menlo', monospace;
        font-size: 0.875rem;
        white-space: pre-wrap;
        border: 1px solid #e5e7eb;
    }
    .stButton>button {
        background-color: #3b82f6;
        color: white;
        font-weight: 600;
        padding: 0.5rem 2rem;
        border-radius: 0.5rem;
        border: none;
    }
    .stButton>button:hover {
        background-color: #2563eb;
    }
</style>
""",
    unsafe_allow_html=True,
)


# Initialize session state
if "analysis_complete" not in st.session_state:
    st.session_state.analysis_complete = False
if "event_data" not in st.session_state:
    st.session_state.event_data = None
if "agent_output" not in st.session_state:
    st.session_state.agent_output = None
if "trace_log" not in st.session_state:
    st.session_state.trace_log = []


def capture_trace_logs():
    """Capture agent trace logs"""

    class TraceCapture(logging.Handler):
        def __init__(self):
            super().__init__()
            self.logs = []

        def emit(self, record):
            self.logs.append(self.format(record))

    handler = TraceCapture()
    handler.setFormatter(logging.Formatter("%(message)s"))

    logger = logging.getLogger()
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    return handler


def process_video(video_bytes, video_id):
    """Process video through the safety agent system"""
    from agent.safety_agents import create_runner, run_agent_system

    # Capture traces
    trace_handler = capture_trace_logs()

    # Run video analysis with Gemini
    with st.spinner("🎥 Analyzing video with Gemini 2.5 Pro..."):
        event_json = run_video_model(video_bytes, video_id)
        event_data = json.loads(event_json)
        st.session_state.event_data = event_data

    # Run agent system
    with st.spinner("🤖 Processing through safety agent system..."):
        runner = create_runner(verbose=True)
        result = run_agent_system(event_json, runner)
        st.session_state.agent_output = result

    # Get trace logs
    st.session_state.trace_log = trace_handler.logs

    st.session_state.analysis_complete = True


# Sidebar
with st.sidebar:
    st.markdown("### 🏗️ Safety Agent System")
    st.markdown("---")

    st.markdown("**AI-Powered Safety Monitoring**")
    st.markdown(
        """
    - 🎥 Real-time video analysis
    - 🤖 Multi-agent system
    - 🚨 Automatic emergency dispatch
    - 📊 Risk assessment
    """
    )

    st.markdown("---")
    st.markdown("**Powered by:**")
    st.markdown("- Gemini 2.5 Pro Vision")
    st.markdown("- NVIDIA Nemotron")
    st.markdown("- Custom Agent Framework")

    if st.button("Reset Demo", use_container_width=True):
        st.session_state.analysis_complete = False
        st.session_state.event_data = None
        st.session_state.agent_output = None
        st.session_state.trace_log = []
        st.rerun()

# Main content
st.markdown(
    '<div class="main-header">Construction Safety Agent System</div>', unsafe_allow_html=True
)
st.markdown(
    '<div class="sub-header">AI-powered real-time safety monitoring with multi-agent analysis</div>',
    unsafe_allow_html=True,
)

# Video Upload Section
if not st.session_state.analysis_complete:
    st.markdown("### 📹 Upload Construction Site Video")

    col1, col2 = st.columns([2, 1])

    with col1:
        uploaded_file = st.file_uploader(
            "Choose a video file (MP4 format recommended)",
            type=["mp4", "mov", "avi"],
            help="Upload a construction site video for safety analysis",
        )

        if uploaded_file is not None:
            # Display video
            st.video(uploaded_file)

            # Process button
            if st.button("🚀 Analyze Video", use_container_width=True, type="primary"):
                video_bytes = uploaded_file.read()
                video_id = f"demo_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

                # Process
                process_video(video_bytes, video_id)
                st.rerun()

    with col2:
        st.markdown("#### 📊 What We Analyze")
        st.markdown(
            """
        **Safety Hazards:**
        - Medical emergencies
        - Fire hazards
        - PPE violations
        - Equipment risks
        - Environmental hazards

        **Actions Taken:**
        - 911 dispatch
        - Site-wide alerts
        - Incident logging
        - Compliance tracking
        """
        )

# Results Section
else:
    event_data = st.session_state.event_data

    # Key Metrics Row
    st.markdown("### 📊 Analysis Results")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        severity = event_data["safety_status"]
        severity_class = f"severity-{severity.lower()}"
        st.markdown(
            f"""
        <div class="metric-card">
            <div style="font-size: 0.875rem; color: #6b7280; margin-bottom: 0.5rem;">Safety Status</div>
            <div class="{severity_class}" style="font-size: 1.5rem;">{severity}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        probability = event_data["predictions"]["probability"]
        st.markdown(
            f"""
        <div class="metric-card">
            <div style="font-size: 0.875rem; color: #6b7280; margin-bottom: 0.5rem;">Risk Probability</div>
            <div style="font-size: 1.5rem; font-weight: 700; color: #dc2626;">{probability * 100:.0f}%</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col3:
        incident_type = event_data["predictions"]["incident_type"]
        st.markdown(
            f"""
        <div class="metric-card">
            <div style="font-size: 0.875rem; color: #6b7280; margin-bottom: 0.5rem;">Incident Type</div>
            <div style="font-size: 1rem; font-weight: 600; color: #1f2937;">{incident_type}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col4:
        video_id = event_data["video_id"]
        st.markdown(
            f"""
        <div class="metric-card">
            <div style="font-size: 0.875rem; color: #6b7280; margin-bottom: 0.5rem;">Video ID</div>
            <div style="font-size: 0.75rem; font-weight: 600; color: #1f2937;">{video_id}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # Two-column layout for details
    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.markdown("### 🎥 Scene Analysis")
        st.markdown(f"**Description:** {event_data['scene_description']}")

        st.markdown("### 🚨 Safety Response")
        st.info(event_data["safety_response"])

    with col_right:
        st.markdown("### 🤖 Agent System Output")
        st.success(st.session_state.agent_output)

    # Agent Trace Section
    st.markdown("---")
    st.markdown("### 🔍 Agent Execution Trace")

    with st.expander("View Detailed Agent Trace", expanded=True):
        if st.session_state.trace_log:
            trace_text = "\n".join(st.session_state.trace_log)
            st.markdown(f'<div class="agent-trace">{trace_text}</div>', unsafe_allow_html=True)
        else:
            st.info("No trace logs captured")

    # Download Section
    st.markdown("---")
    col1, col2, col3 = st.columns(3)

    with col1:
        # Download event data
        event_json = json.dumps(event_data, indent=2)
        st.download_button(
            label="📥 Download Event Data (JSON)",
            data=event_json,
            file_name=f"event_{event_data['video_id']}.json",
            mime="application/json",
            use_container_width=True,
        )

    with col2:
        # Download agent output
        st.download_button(
            label="📥 Download Agent Report",
            data=st.session_state.agent_output,
            file_name=f"report_{event_data['video_id']}.txt",
            mime="text/plain",
            use_container_width=True,
        )

    with col3:
        # Download trace
        trace_text = "\n".join(st.session_state.trace_log)
        st.download_button(
            label="📥 Download Trace Log",
            data=trace_text,
            file_name=f"trace_{event_data['video_id']}.log",
            mime="text/plain",
            use_container_width=True,
        )


# Footer
st.markdown("---")
st.markdown(
    """
<div style="text-align: center; color: #6b7280; font-size: 0.875rem;">
    <p><strong>Construction Safety Agent System</strong> | Powered by AI | Real-time Safety Monitoring</p>
    <p>Demo for Investor Presentation</p>
</div>
""",
    unsafe_allow_html=True,
)
