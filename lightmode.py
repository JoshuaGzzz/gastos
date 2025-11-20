import streamlit as st

# Initialize theme
if "theme" not in st.session_state:
    st.session_state["theme"] = "light"

def get_css(theme):
    floating_css = """
        div[data-testid="stButton"] {
            position: fixed;
            top: 0.5rem; /* Vertical alignment */
            right: 10rem; /* Move to right side. Increase this number if it overlaps with Deploy/Menu */
            z-index: 9999999; 
            width: auto !important; /* Make button compact */
        }
        
        /* Ensure the inner button element also respects size */
        div[data-testid="stButton"] > button {
            width: auto !important;
            display: inline-block !important;
        }
    """
    
    if theme == "dark":
        return f"""
        <style>
        {floating_css}
        .stApp {{ background: #0b1220; color: #ffffff; }}
        .block-container {{ padding-top: 5rem; }}
        button {{
            background-color: #374151 !important;
            color: #ffffff !important;
            border: 1px solid #6b7280 !important;
        }}
        </style>
        """
    else:
        return f"""
        <style>
        {floating_css}
        .stApp {{ background: #ffffff; color: #000000; }}
        .block-container {{ padding-top: 5rem; }}
        button {{
            background-color: #e5e7eb !important;
            color: #111827 !important;
            border: 1px solid #d1d5db !important;
        }}
        </style>
        """


if st.button("Click to study better!"):
    st.session_state["theme"] = "dark" if st.session_state["theme"] == "light" else "light"
    st.rerun()

st.markdown(get_css(st.session_state["theme"]), unsafe_allow_html=True)

st.write("The button should now be compact and floating on the right side!")