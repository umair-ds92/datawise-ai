"""
DataWise AI - Monitoring Dashboard
Simple metrics and system health dashboard
"""

import streamlit as st
import json
from pathlib import Path
from datetime import datetime
from utils.metrics import metrics_tracker
from utils.logging import setup_logger

logger = setup_logger('monitoring')

st.set_page_config(
    page_title="DataWise AI - Monitoring",
    page_icon="📊",
    layout="wide"
)

st.title("📊 DataWise AI - Monitoring Dashboard")
st.caption(f"Last refreshed: {datetime.now().strftime('%H:%M:%S')}")
st.divider()

# ============================================
# CURRENT SESSION METRICS
# ============================================
st.subheader("🔄 Current Session")

summary = metrics_tracker.get_session_summary()
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Tasks Completed", summary['tasks_completed'])
with col2:
    st.metric("Total Tokens", f"{summary['total_tokens']:,}")
with col3:
    st.metric("Total Cost", f"${summary['total_cost_usd']:.4f}")
with col4:
    st.metric("Total Duration", f"{summary['total_duration_seconds']:.1f}s")

st.divider()

# ============================================
# HISTORICAL METRICS
# ============================================
st.subheader("📈 Historical Sessions")

metrics_dir = Path('./metrics')
if metrics_dir.exists():
    metric_files = sorted(metrics_dir.glob('*.json'), reverse=True)

    if metric_files:
        sessions_data = []
        for f in metric_files[:10]:  # Show last 10 sessions
            try:
                with open(f) as mf:
                    data = json.load(mf)
                    sessions_data.append({
                        'Session': data.get('session_id', f.stem),
                        'Tasks': len(data.get('tasks', [])),
                        'Tokens': data.get('total_input_tokens', 0) + data.get('total_output_tokens', 0),
                        'Cost ($)': round(data.get('total_cost_usd', 0), 4),
                        'Duration (s)': round(data.get('total_duration_seconds', 0), 1)
                    })
            except Exception:
                continue

        if sessions_data:
            st.dataframe(sessions_data, use_container_width=True)
    else:
        st.info("No historical sessions found yet.")
else:
    st.info("Metrics directory not found. Run some analyses first!")

st.divider()

# ============================================
# LOG VIEWER
# ============================================
st.subheader("📋 Recent Logs")

log_file = Path('./logs/datawise.log')
if log_file.exists():
    with open(log_file, 'r') as f:
        lines = f.readlines()

    # Show last 20 lines
    recent_logs = lines[-20:] if len(lines) > 20 else lines
    log_text = ''.join(recent_logs)

    st.code(log_text, language='text')

    if st.button("🗑️ Clear Logs"):
        with open(log_file, 'w') as f:
            f.write('')
        st.success("Logs cleared!")
        st.rerun()
else:
    st.info("No log file found yet.")

st.divider()

# ============================================
# SYSTEM INFO
# ============================================
st.subheader("⚙️ System Info")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Directories:**")
    dirs = ['temp', 'logs', 'cache', 'state', 'metrics', 'data/uploads', 'data/outputs']
    for d in dirs:
        path = Path(d)
        exists = "✅" if path.exists() else "❌"
        files = len(list(path.glob('*'))) if path.exists() else 0
        st.caption(f"{exists} `{d}` ({files} files)")

with col2:
    st.markdown("**Cache Stats:**")
    cache_dir = Path('./cache')
    if cache_dir.exists():
        cache_files = list(cache_dir.glob('*.json'))
        total_size = sum(f.stat().st_size for f in cache_files) / 1024
        st.caption(f"📦 Cached entries: {len(cache_files)}")
        st.caption(f"💾 Cache size: {total_size:.1f} KB")
    else:
        st.caption("Cache directory not found")

# Refresh button
if st.button("🔄 Refresh Dashboard"):
    st.rerun()