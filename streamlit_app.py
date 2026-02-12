"""
DataWise AI - Enhanced Streamlit Web Interface
Interactive data analysis powered by multi-agent AI
"""

import streamlit as st
import asyncio
import os
from pathlib import Path

from team.analyzer_gpt import create_basic_team
from config.openai_model_client import get_model_client
from config.docker_utils import (
    getDockerCommandLineExecutor,
    start_docker_container,
    stop_docker_container
)
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.base import TaskResult
from utils.validators import validate_file, validate_task
from utils.state_manager import state_manager
from utils.metrics import metrics_tracker
from utils.logging import agent_logger
from utils.error_handlers import format_error_for_user

# ============================================
# PAGE CONFIGURATION
# ============================================
st.set_page_config(
    page_title="DataWise AI",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# SESSION STATE INITIALIZATION
# ============================================
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'autogen_team_state' not in st.session_state:
    st.session_state.autogen_team_state = None
if 'session_id' not in st.session_state:
    from datetime import datetime
    st.session_state.session_id = datetime.now().strftime('%Y%m%d_%H%M%S')
if 'task_count' not in st.session_state:
    st.session_state.task_count = 0

# ============================================
# SIDEBAR
# ============================================
with st.sidebar:
    st.title("⚙️ Settings")
    st.divider()

    # Session info
    st.subheader("📊 Session Info")
    st.caption(f"Session: `{st.session_state.session_id}`")
    st.caption(f"Tasks completed: {st.session_state.task_count}")

    st.divider()

    # Metrics display
    st.subheader("💰 Usage Metrics")
    summary = metrics_tracker.get_session_summary()
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Tasks", summary['tasks_completed'])
        st.metric("Tokens", f"{summary['total_tokens']:,}")
    with col2:
        st.metric("Cost", f"${summary['total_cost_usd']:.4f}")
        st.metric("Time", f"{summary['total_duration_seconds']:.1f}s")

    st.divider()

    # Controls
    st.subheader("🎛️ Controls")

    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.session_state.autogen_team_state = None
        st.rerun()

    if st.button("💾 Save Session", use_container_width=True):
        if st.session_state.autogen_team_state:
            state_manager.save_state(
                st.session_state.session_id,
                st.session_state.autogen_team_state
            )
            st.success("Session saved!")

    st.divider()

    # Help section
    with st.expander("💡 Example Tasks"):
        st.markdown("""
        - *How many rows and columns are in my data?*
        - *Show me the distribution of [column name]*
        - *Plot a bar chart of the top 10 values*
        - *What are the correlations between columns?*
        - *Find missing values in my dataset*
        - *Show summary statistics*
        """)

# ============================================
# MAIN INTERFACE
# ============================================
st.title("DataWise AI")
st.caption("Multi-agent data analysis powered by AutoGen + GPT-4o")
st.divider()

# File upload section
col1, col2 = st.columns([2, 1])

with col1:
    uploaded_file = st.file_uploader(
        "📂 Upload your data file",
        type=['csv', 'xlsx', 'json'],
        help="Supported formats: CSV, Excel, JSON (Max 100MB)"
    )

with col2:
    if uploaded_file:
        # Validate file
        is_valid, error_msg = validate_file(
            uploaded_file.name,
            uploaded_file.size
        )

        if is_valid:
            st.success(f"✅ {uploaded_file.name}")
            st.caption(f"Size: {uploaded_file.size / 1024:.1f} KB")

            # Save file to temp directory
            os.makedirs('temp', exist_ok=True)
            with open('temp/data.csv', 'wb') as f:
                f.write(uploaded_file.getbuffer())
        else:
            st.error(f"❌ {error_msg}")
            uploaded_file = None
    else:
        st.info("👆 Upload a file to begin")

st.divider()

# Chat history display
if st.session_state.messages:
    st.subheader("💬 Conversation")
    for msg in st.session_state.messages:
        if msg['role'] == 'user':
            with st.chat_message('user', avatar='👨'):
                st.markdown(msg['content'])
        elif msg['role'] == 'analyzer':
            with st.chat_message('assistant', avatar='🤖'):
                st.markdown(msg['content'])
        elif msg['role'] == 'executor':
            with st.chat_message('assistant', avatar='🧑🏻‍💻'):
                st.markdown(msg['content'])
        elif msg['role'] == 'system':
            st.caption(msg['content'])

# ============================================
# TASK INPUT
# ============================================
task = st.chat_input(
    "Ask something about your data... (e.g. 'Show me the top 10 rows')",
    disabled=uploaded_file is None
)

if not uploaded_file:
    st.warning("⚠️ Please upload a data file before asking questions.")


# ============================================
# ANALYSIS RUNNER
# ============================================
async def run_analysis(docker, model_client, task: str):
    """Run the multi-agent analysis pipeline"""
    try:
        await start_docker_container(docker)
        team = create_basic_team(docker, model_client)

        # Restore previous session state if available
        if st.session_state.autogen_team_state is not None:
            await team.load_state(st.session_state.autogen_team_state)

        agent_logger.log_task_start(task)
        metrics_tracker.start_task(task)

        async for message in team.run_stream(task=task):
            if isinstance(message, TextMessage):
                content = f"**{message.source}**: {message.content}"

                if message.source == 'user':
                    role = 'user'
                elif 'analyzer' in message.source.lower() or 'data' in message.source.lower():
                    role = 'analyzer'
                else:
                    role = 'executor'

                st.session_state.messages.append({
                    'role': role,
                    'content': content
                })

                # Display message in real-time
                avatar = '🤖' if role == 'analyzer' else '🧑🏻‍💻'
                with st.chat_message(role, avatar=avatar if role != 'user' else '👨'):
                    st.markdown(content)

            elif isinstance(message, TaskResult):
                stop_msg = f"*Analysis complete — {message.stop_reason}*"
                st.session_state.messages.append({
                    'role': 'system',
                    'content': stop_msg
                })
                st.caption(stop_msg)

        # Save team state for conversation continuity
        st.session_state.autogen_team_state = await team.save_state()
        metrics_tracker.end_task(status='success')
        agent_logger.log_task_complete(task, 0)

        return None

    except Exception as e:
        metrics_tracker.end_task(status='error')
        agent_logger.log_error(e, context='run_analysis')
        return e

    finally:
        await stop_docker_container(docker)


# ============================================
# HANDLE TASK SUBMISSION
# ============================================
if task:
    # Validate task
    is_valid, error_msg = validate_task(task)
    if not is_valid:
        st.error(f"❌ {error_msg}")
    else:
        # Show user message immediately
        with st.chat_message('user', avatar='👨'):
            st.markdown(task)
        st.session_state.messages.append({'role': 'user', 'content': task})

        # Run analysis
        with st.spinner("🤖 Agents are working..."):
            model_client = get_model_client()
            docker = getDockerCommandLineExecutor()
            error = asyncio.run(run_analysis(docker, model_client, task))

        if error:
            user_friendly = format_error_for_user(error)
            st.error(f"❌ {user_friendly}")
        else:
            st.session_state.task_count += 1

        # Display output image if generated
        for img_name in ['output.png', 'chart.png', 'plot.png']:
            img_path = f'temp/{img_name}'
            if os.path.exists(img_path):
                st.image(img_path, caption='Generated Visualization')
                break