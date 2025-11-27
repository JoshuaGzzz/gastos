import streamlit as st
import time
import json
from datetime import datetime, timedelta
import os

st.set_page_config(layout="centered")

DATA_FILE = "data.json"

# ----------------------
# Load saved data
# ----------------------
def load_data():
    if not os.path.exists(DATA_FILE):
        return {}  # Return empty dict, not list
    
    try:
        with open(DATA_FILE, "r") as f:
            content = f.read().strip()
            if not content:
                return {} 
            return json.loads(content)
    except json.JSONDecodeError:
        return {}

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
    # Check if saved data exists and has the correct key
    if saved and "start_time" in saved:
        st.session_state.start_time = saved["start_time"]
    else:
        st.session_state.start_time = time.time()

if "last_reset" not in st.session_state:
    if saved and "last_reset" in saved:
        st.session_state.last_reset = saved["last_reset"]
    else:
        st.session_state.last_reset = "Never"

# ----------------------
# UI
# ----------------------
st.markdown("<h1 style='text-align:center;'>KELAN HULING GUMASTOS SI JOSEPH MEDINA</h1>", unsafe_allow_html=True)

# Current date/time (Adjusted for UTC+8)
now = (datetime.utcnow() + timedelta(hours=8)).strftime("%B %d, %Y — %I:%M:%S %p")
st.markdown(f"<h3 style='text-align:center;'>Current Date & Time:<br>{now}</h3>", unsafe_allow_html=True)

st.markdown("---")

# Stopwatch calculation
elapsed = time.time() - st.session_state.start_time

days = int(elapsed // 86400)
hours = int((elapsed % 86400) // 3600)
mins = int((elapsed % 3600) // 60)
secs = int(elapsed % 60)
millis = int((elapsed * 1000) % 1000)

time_text = f"{days:02d}:{hours:02d}:{mins:02d}:{secs:02d}:{millis:03d}"

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
        # UTC+8 logic for the reset timestamp
        st.session_state.last_reset = (datetime.utcnow() + timedelta(hours=8)).strftime("%B %d, %Y — %I:%M:%S %p")
        
        save_data()  # <--- ONLY SAVE HERE (When the data actually changes)
        st.rerun()

# Last reset timestamp
st.markdown(
    f"<h4 style='text-align:center;'>Last Reset: {st.session_state.last_reset}</h4>",
    unsafe_allow_html=True
)

# ----------------------
# Auto-refresh
# ----------------------
# REMOVED save_data() from here to prevent file corruption
time.sleep(0.1)
st.rerun()
