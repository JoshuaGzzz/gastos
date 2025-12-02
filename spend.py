import streamlit as st
import time
import json
import pandas as pd
from datetime import datetime, timedelta, timezone
import os

st.set_page_config(layout="centered", page_title="Spend Tracker")

DATA_FILE = "data.json"

# ----------------------
# Config: Timezone (GMT+8)
# ----------------------
# This creates a timezone object for GMT+8
TZ_MANILA = timezone(timedelta(hours=8))

# ----------------------
# Load saved data
# ----------------------
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return None
    return None

# ----------------------
# Save data
# ----------------------
def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump({
            "start_time": st.session_state.start_time,
            "last_reset": st.session_state.last_reset,
            "history": st.session_state.history
        }, f)

# ----------------------
# Initialize State
# ----------------------
saved = load_data()

if "start_time" not in st.session_state:
    st.session_state.start_time = saved["start_time"] if saved and "start_time" in saved else time.time()

if "last_reset" not in st.session_state:
    st.session_state.last_reset = saved["last_reset"] if saved and "last_reset" in saved else "Never"

if "history" not in st.session_state:
    st.session_state.history = saved["history"] if saved and "history" in saved else []

# ----------------------
# Helper: Format Duration (For Table)
# ----------------------
def format_duration_text(seconds):
    seconds = int(seconds)
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    
    # Returns friendly text for the table: 1d 02h 15m 30s
    return f"{days}d {hours:02d}h {minutes:02d}m {seconds:02d}s"

# ----------------------
# UI
# ----------------------
st.markdown("<h1 style='text-align:center;'>KELAN HULING GUMASTOS SI JOSEPH MEDINA</h1>", unsafe_allow_html=True)

# Current date/time (ADJUSTED TO GMT+8)
now = datetime.now(TZ_MANILA).strftime("%B %d, %Y — %I:%M:%S %p")
st.markdown(f"<h3 style='text-align:center;'>Current Date & Time (PH):<br>{now}</h3>", unsafe_allow_html=True)

st.markdown("---")

# ----------------------
# Stopwatch Calculation (DD:HH:MM:SS)
# ----------------------
elapsed = time.time() - st.session_state.start_time

# Calculate components
days = int(elapsed // 86400)
hours = int((elapsed % 86400) // 3600)
mins = int((elapsed % 3600) // 60)
secs = int(elapsed % 60)

# Format: 00:00:00:00
time_text = f"{days:02d}:{hours:02d}:{mins:02d}:{secs:02d}"

st.markdown(
    f"<h2 style='text-align:center;'>TIME SINCE LAST SPEND</h2>"
    f"<h1 style='text-align:center; font-size:60px;'>{time_text}</h1>"
    f"<h4 style='text-align:center; color:gray;'>(Days : Hours : Minutes : Seconds)</h4>",
    unsafe_allow_html=True
)

# ----------------------
# RESET FORM
# ----------------------
st.write("### 💸 Reset Timer")

# clear_on_submit=True wipes the input field after clicking the button
with st.form("reset_form", clear_on_submit=True):
    reason = st.text_input("Reason for spending", placeholder="e.g., fucking photocards")
    submitted = st.form_submit_button("Reset at gumastos si Joseph", use_container_width=True)

    if submitted:
        # 1. Capture Data (ADJUSTED TO GMT+8)
        current_time = datetime.now(TZ_MANILA).strftime("%Y-%m-%d %I:%M:%S %p")
        duration_string = format_duration_text(elapsed) # Use the friendly format for history
        clean_reason = reason if reason else "No reason provided"

        # 2. Add to history (Newest first)
        st.session_state.history.insert(0, {
            "Date Reset": current_time,
            "Duration Lasted": duration_string,
            "Reason": clean_reason
        })

        # 3. Reset Timer
        st.session_state.start_time = time.time()
        st.session_state.last_reset = current_time
        
        # 4. Save & Reload
        save_data()
        st.rerun()

# Last reset timestamp text
st.markdown(
    f"<div style='text-align:center; margin-top:10px; color:gray;'>Last Reset: {st.session_state.last_reset}</div>",
    unsafe_allow_html=True
)

st.markdown("---")

# ----------------------
# History Table
# ----------------------
st.write("## 📜 Spending History")

if st.session_state.history:
    df = pd.DataFrame(st.session_state.history)
    st.dataframe(
        df, 
        use_container_width=True,
        hide_index=True,
        column_order=["Date Reset", "Reason", "Duration Lasted"]
    )
else:
    st.info("No spending recorded yet. Keep saving!")

# ----------------------
# Auto-refresh
# ----------------------
time.sleep(0.1)
st.rerun()
