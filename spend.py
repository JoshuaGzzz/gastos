import streamlit as st
import time
import json
from datetime import datetime
import os

st.set_page_config(layout="centered")

DATA_FILE = "data.json"

# ----------------------
# Load saved data
# ----------------------
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return None

# ----------------------
# Save data
# ----------------------
def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump({
            "start_time": st.session_state.start_time,
            "last_reset": st.session_state.last_reset
        }, f)

# ----------------------
# Initialize State
# ----------------------
saved = load_data()

if "start_time" not in st.session_state:
    if saved:
        st.session_state.start_time = saved["start_time"]
    else:
        st.session_state.start_time = time.time()

if "last_reset" not in st.session_state:
    if saved:
        st.session_state.last_reset = saved["last_reset"]
    else:
        st.session_state.last_reset = "Never"

# ----------------------
# UI
# ----------------------
st.markdown("<h1 style='text-align:center;'>KELAN HULING GUMASTOS SI JOSEPH MEDINA</h1>", unsafe_allow_html=True)

# Current date/time
now = datetime.now().strftime("%B %d, %Y — %I:%M:%S %p")
st.markdown(f"<h3 style='text-align:center;'>Current Date & Time:<br>{now}</h3>", unsafe_allow_html=True)

st.markdown("---")

# Stopwatch calculation
elapsed = time.time() - st.session_state.start_time
mins = int(elapsed // 60)
secs = int(elapsed % 60)
millis = int((elapsed * 1000) % 1000)
time_text = f"{mins:02d}:{secs:02d}:{millis:03d}"

st.markdown(
    f"<h2 style='text-align:center;'>HOURS SINCE LAST SPEND</h2>"
    f"<h1 style='text-align:center; font-size:60px;'>{time_text}</h1>",
    unsafe_allow_html=True
)

# ----------------------
# Reset button centered
# ----------------------
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    if st.button("🔄 Reset Stopwatch", use_container_width=True):
        st.session_state.start_time = time.time()
        st.session_state.last_reset = datetime.now().strftime("%B %d, %Y — %I:%M:%S %p")
        save_data()    # SAVE PERSISTENT DATA
        st.rerun()

# Last reset timestamp
st.markdown(
    f"<h4 style='text-align:center;'>Last Reset: {st.session_state.last_reset}</h4>",
    unsafe_allow_html=True
)

# ----------------------
# Auto-refresh every 100 ms
# ----------------------
save_data()   # update persistent file continuously
time.sleep(0.1)
st.rerun()
