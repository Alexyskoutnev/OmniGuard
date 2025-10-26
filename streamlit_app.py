import json
import sys
from datetime import datetime
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent))

from pipeline.pipeline import run_video_model

# Configure page
st.set_page_config(
    page_title="Safety Agent",
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
        font-weight: 600;
        color: #1d1d1f;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }
    .sub-header {
        font-size: 1.2rem;
        font-weight: 400;
        color: #86868b;
        margin-bottom: 3rem;
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
        background-color: #0071e3;
        color: white;
        font-weight: 500;
        padding: 0.75rem 2rem;
        border-radius: 0.75rem;
        border: none;
        font-size: 1rem;
    }
    .stButton>button:hover {
        background-color: #0077ed;
    }
    [data-testid="stSidebar"] {
        background-color: #f5f5f7;
    }

    /* Tree trace styling */
    .stExpander {
        border: 1px solid #e5e7eb;
        border-radius: 0.5rem;
        margin-bottom: 0.5rem;
        background: #ffffff;
    }

    .stExpander > summary {
        font-weight: 500;
        color: #1d1d1f;
    }

    /* Tool execution containers */
    .element-container {
        margin-bottom: 0.75rem;
    }

    /* Code blocks in tree */
    code {
        font-size: 0.875rem;
        background: #f5f5f7;
        padding: 0.125rem 0.375rem;
        border-radius: 0.25rem;
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
if "trace_data" not in st.session_state:
    st.session_state.trace_data = None


def render_tree_trace(traces):
    """Render agent traces as an interactive tree UI"""
    if not traces:
        st.info("No trace data available")
        return

    for trace in traces:
        # Agent node
        duration_str = f"{trace.duration_ms:.0f}ms" if trace.duration_ms else "..."
        with st.expander(f"🤖 {trace.agent_name} ({duration_str})", expanded=True):
            # Agent metadata
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"**Start:** `{trace.start_time.split('T')[1][:8]}`")
            with col2:
                st.markdown(f"**Iterations:** `{trace.iterations}`")
            with col3:
                st.markdown(f"**Duration:** `{duration_str}`")

            st.markdown("")

            # Tool calls
            if trace.tool_calls:
                st.markdown("**Tool Executions:**")
                for tc in trace.tool_calls:
                    status_icon = "✅" if tc.success else "❌"
                    tool_duration = f"{tc.duration_ms:.1f}ms"

                    with st.container():
                        st.markdown(f"{status_icon} **{tc.tool_name}** `{tool_duration}`")

                        # Input (arguments)
                        with st.expander("📥 Input", expanded=False):
                            st.json(tc.arguments)

                        # Output (result)
                        with st.expander("📤 Output", expanded=False):
                            if tc.error:
                                st.error(tc.error)
                            else:
                                result_display = tc.result
                                if len(result_display) > 500:
                                    result_display = result_display[:500] + "..."
                                st.code(result_display, language="text")

                        st.markdown("")
            else:
                st.markdown("*No tool calls*")

            # Handoff information
            if trace.handoff_to:
                st.markdown("")
                st.info(f"🔄 Handed off to: **{trace.handoff_to}**")

            # Final output
            if trace.final_output:
                st.markdown("")
                with st.expander("📋 Final Output", expanded=False):
                    st.markdown(trace.final_output)


def process_video(video_bytes, video_id):
    """Process video through the safety agent system"""
    from agent.safety_agents import create_runner, run_agent_system

    # Run video analysis with Gemini
    with st.spinner("Analyzing video with Gemini 2.5 Pro..."):
        event_json = run_video_model(video_bytes, video_id)
        event_data = json.loads(event_json)
        st.session_state.event_data = event_data

    # Run agent system
    with st.spinner("Processing through safety agent system..."):
        runner = create_runner(verbose=False)  # Disable verbose for clean UI
        result = run_agent_system(event_json, runner)
        st.session_state.agent_output = result

        # Capture structured trace data from runner's logger
        st.session_state.trace_data = runner.logger.traces

    st.session_state.analysis_complete = True


# Sidebar
with st.sidebar:
    st.markdown("### Safety Agent System")
    st.markdown("AI-powered safety monitoring")

    st.markdown("")
    st.markdown("")

    if st.button("Reset", use_container_width=True):
        st.session_state.analysis_complete = False
        st.session_state.event_data = None
        st.session_state.agent_output = None
        st.session_state.trace_data = None
        st.rerun()

# Main content
st.markdown(
    '<div class="main-header">Construction Safety Agent System</div>', unsafe_allow_html=True
)
st.markdown(
    '<div class="sub-header">AI-powered real-time safety monitoring</div>',
    unsafe_allow_html=True,
)

st.markdown("")
st.markdown("")

# Video Upload Section
if not st.session_state.analysis_complete:
    uploaded_file = st.file_uploader(
        "Upload Construction Site Video",
        type=["mp4", "mov", "avi"],
        label_visibility="collapsed",
    )

    if uploaded_file is not None:
        st.video(uploaded_file)

        st.markdown("")

        # Process button
        if st.button("Analyze Video", use_container_width=True, type="primary"):
            video_bytes = uploaded_file.read()
            video_id = f"demo_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

            # Process
            process_video(video_bytes, video_id)
            st.rerun()

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

    st.markdown("")
    st.markdown("")

    # Two-column layout for details
    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.markdown("### Scene Analysis")
        st.markdown(event_data["scene_description"])

        st.markdown("")

        st.markdown("### Safety Response")
        st.info(event_data["safety_response"])

    with col_right:
        st.markdown("### Agent Analysis")
        st.success(st.session_state.agent_output)

    # Agent Trace Section
    st.markdown("")
    st.markdown("")

    st.markdown("### Agent Execution Trace")
    render_tree_trace(st.session_state.trace_data)

    # Download Section
    st.markdown("")
    st.markdown("")

    col1, col2, col3 = st.columns(3)

    with col1:
        event_json = json.dumps(event_data, indent=2)
        st.download_button(
            label="Download Event Data",
            data=event_json,
            file_name=f"event_{event_data['video_id']}.json",
            mime="application/json",
            use_container_width=True,
        )

    with col2:
        st.download_button(
            label="Download Report",
            data=st.session_state.agent_output,
            file_name=f"report_{event_data['video_id']}.txt",
            mime="text/plain",
            use_container_width=True,
        )

    with col3:
        # Convert structured traces to JSON
        trace_data_json = json.dumps(
            [
                {
                    "agent_name": t.agent_name,
                    "start_time": t.start_time,
                    "end_time": t.end_time,
                    "duration_ms": t.duration_ms,
                    "iterations": t.iterations,
                    "handoff_to": t.handoff_to,
                    "tool_calls": [
                        {
                            "tool_name": tc.tool_name,
                            "arguments": tc.arguments,
                            "result": tc.result,
                            "duration_ms": tc.duration_ms,
                            "success": tc.success,
                            "error": tc.error,
                        }
                        for tc in t.tool_calls
                    ],
                }
                for t in (st.session_state.trace_data or [])
            ],
            indent=2,
        )
        st.download_button(
            label="Download Trace",
            data=trace_data_json,
            file_name=f"trace_{event_data['video_id']}.json",
            mime="application/json",
            use_container_width=True,
        )
