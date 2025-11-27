import streamlit as st
import time
from datetime import datetime

st.set_page_config(layout="centered")

# ---- Initialize session state ----
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

if "last_reset" not in st.session_state:
    st.session_state.last_reset = "Never"

# ---- Title ----
st.markdown(
    "<h1 style='text-align: center;'>Joseph Medina Spending Check</h1>",
    unsafe_allow_html=True
)

# ---- Current Date & Time ----
current_dt = datetime.now().strftime("%B %d, %Y — %I:%M:%S %p")
st.markdown(
    f"<h3 style='text-align: center;'>Current Date & Time:<br>{current_dt}</h3>",
    unsafe_allow_html=True
)

st.markdown("---")

# ---- Stopwatch Calculation ----
elapsed = time.time() - st.session_state.start_time
mins = int(elapsed // 60)
secs = int(elapsed % 60)
millis = int((elapsed * 1000) % 1000)

stopwatch_text = f"{mins:02d}:{secs:02d}:{millis:03d}"

# ---- Stopwatch Display ----
st.markdown(
    f"""
    <h2 style='text-align:center;'>⏱️ How many hours since his last spend</h2>
    <h1 style='text-align:center; font-size:60px;'>{stopwatch_text}</h1>
    """,
    unsafe_allow_html=True
)

# ---- Reset Button ----
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    if st.button("Reset", use_container_width=True):
        st.session_state.start_time = time.time()
        st.session_state.last_reset = datetime.now().strftime("%B %d, %Y — %I:%M:%S %p")
        st.rerun()

# ---- Last Reset Timestamp ----
st.markdown(
    f"<h4 style='text-align:center;'>Last Reset: {st.session_state.last_reset}</h4>",
    unsafe_allow_html=True
)

# ---- Auto-refresh every 100 ms ----
st.session_state._ = st.empty()
time.sleep(0.1)
st.rerun()
