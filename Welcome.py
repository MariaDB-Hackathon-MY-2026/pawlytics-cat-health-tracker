"""
Welcome Page - Name-based Entry
"""

import streamlit as st
import hashlib

# Page config - HIDE SIDEBAR!
st.set_page_config(
    page_title="Pawlytics - AI Pet Nutrition",
    page_icon="🐾",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Hide sidebar completely with CSS
st.markdown("""
<style>
    /* Hide sidebar */
    [data-testid="stSidebar"] {
        display: none !important;
    }
    
    /* Main container - white card */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Center the main container VERTICALLY & HORIZONTALLY */
    .main {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        min-height: 100vh !important;
    }
    
    .main .block-container {
        background: white !important;
        border-radius: 30px !important;
        padding: 3rem 2.5rem !important;
        box-shadow: 0 20px 40px rgba(0,0,0,0.15) !important;
        margin: 0 !important;
        max-width: 500px !important;
        width: 100% !important;
    }
    
    /* Force all text dark inside container */
    .main * {
        color: #1e293b !important;
    }
    
    /* Title container with paw icon */
    .title-wrapper {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 12px !important;
        margin-bottom: 0.25rem !important;
    }
    
    .paw-icon {
        font-size: 2.5rem !important;
    }
    
    .title-text {
        font-size: 2.2rem !important;
        font-weight: 800 !important;
        margin: 0 !important;
    }
    
    /* Caption */
    [data-testid="stCaptionContainer"], .stCaption, .st-emotion-cache-1v0mbdj p {
        color: #64748b !important;
        text-align: center !important;
        font-size: 0.95rem !important;
    }
    
    /* Divider */
    hr {
        margin: 1.5rem 0 !important;
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent, #cbd5e1, transparent) !important;
    }
    
    /* Input field */
    .stTextInput input {
        background: white !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 16px !important;
        padding: 0.8rem 1rem !important;
        font-size: 1rem !important;
        text-align: center !important;
        color: #0f172a !important;
        transition: all 0.2s ease !important;
    }
    
    .stTextInput input:focus {
        border-color: #4f46e5 !important;
        box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1) !important;
        outline: none !important;
    }
    
    .stTextInput input::placeholder {
        color: #94a3b8 !important;
    }
    
    /* Label */
    .stTextInput label {
        color: #0f172a !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        margin-bottom: 0.5rem !important;
        text-align: left !important;
    }
    
    /* Button */
.stButton > button {
    background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
    color: white !important;
    border: none !important;
    border-radius: 16px !important;
    padding: 0.8rem 1.5rem !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    transition: all 0.2s ease !important;
    width: 100% !important;
}

/* Force button text to be white */
.stButton > button p,
.stButton > button span,
.stButton > button div,
.stButton > button * {
    color: white !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 20px rgba(79, 70, 229, 0.3) !important;
}
    
    /* Success & Error messages */
    .stAlert {
        border-radius: 12px !important;
        border-left: 4px solid !important;
    }
    
    .stSuccess {
        background: #dcfce7 !important;
        border-left-color: #16a34a !important;
    }
    
    .stSuccess * {
        color: #14532d !important;
    }
    
    .stError {
        background: #fee2e2 !important;
        border-left-color: #dc2626 !important;
    }
    
    .stError * {
        color: #7f1d1d !important;
    }
    
    /* Features list */
    .feature-item {
        display: inline-flex !important;
        align-items: center !important;
        gap: 0.5rem !important;
        margin: 0.5rem 1rem !important;
        color: #475569 !important;
        font-size: 0.85rem !important;
    }
    
    /* Footer text */
    .footer-text {
        text-align: center !important;
        color: #94a3b8 !important;
        font-size: 0.75rem !important;
        margin-top: 2rem !important;
    }
</style>
""", unsafe_allow_html=True)

# Title with paw icon beside
st.markdown("""
<div class="title-wrapper">
    <span class="paw-icon">🐾</span>
    <span class="title-text">Pawlytics</span>
</div>
""", unsafe_allow_html=True)

# Subtitle
st.markdown('<p style="text-align: center; color: #64748b; font-size: 0.95rem; margin-bottom: 2rem;">AI-Powered Cat Nutrition Intelligence</p>', unsafe_allow_html=True)

# Divider
st.markdown("---")

# Name Input
name = st.text_input(
    "What's your name?",
    placeholder="e.g., John",
    key="user_name_input"
)

# Start Button
if st.button("Let's Start", type="primary", use_container_width=True):
    if name and name.strip():
        # Create user session
        st.session_state['user_name'] = name.strip()
        st.session_state['user_id'] = hashlib.md5(name.strip().encode()).hexdigest()[:8]
        st.session_state['authenticated'] = True
        
        st.success(f"✅ Welcome, {name}!")
        st.balloons()
        
        # Redirect to Home
        st.switch_page("pages/0_Home.py")
    else:
        st.error("❌ Please enter your name!")

# Guest link
st.markdown('<p style="text-align: center; margin-top: 1rem; font-size: 0.85rem; color: #64748b;">━━━━━━ or ━━━━━━</p>', unsafe_allow_html=True)

if st.button("Continue as Guest →", use_container_width=True, key="guest_btn"):
    import time
    guest_id = hashlib.md5(f"guest_{time.time()}".encode()).hexdigest()[:8]
    
    st.session_state['user_name'] = "Guest"
    st.session_state['user_id'] = guest_id
    st.session_state['authenticated'] = True
    
    st.success("✅ Welcome, Guest!")
    st.balloons()
    st.switch_page("pages/0_Home.py")

# Divider
st.markdown("---")

# Benefits
st.markdown("""
<div style="text-align: center;">
    <span class="feature-item">✓ No registration required</span>
    <span class="feature-item">✓ Privacy-first approach</span>
    <span class="feature-item">✓ Start in 5 seconds</span>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer-text">
    🔒 Your data stays with you. No emails, no passwords.
</div>
""", unsafe_allow_html=True)