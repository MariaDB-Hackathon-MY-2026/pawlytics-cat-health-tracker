"""
Session Management Utility
Handles user sessions without login
"""

import streamlit as st
import uuid
from datetime import datetime

def init_session():
    """Initialize session state variables"""
    
    # Generate unique session ID if not exists
    if 'session_id' not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    
    # Initialize other session variables
    if 'current_cat' not in st.session_state:
        st.session_state.current_cat = None
    
    if 'scan_results' not in st.session_state:
        st.session_state.scan_results = []
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    if 'welcome_shown' not in st.session_state:
        st.session_state.welcome_shown = False
    
    if 'theme' not in st.session_state:
        st.session_state.theme = 'light'

def get_session_id():
    """Get current session ID"""
    return st.session_state.get('session_id', 'unknown')

def set_current_cat(cat_id):
    """Set currently selected cat"""
    st.session_state.current_cat = cat_id

def get_current_cat():
    """Get currently selected cat"""
    return st.session_state.get('current_cat')

def add_scan_result(result):
    """Add scan result to session history"""
    if 'scan_results' not in st.session_state:
        st.session_state.scan_results = []
    st.session_state.scan_results.append(result)

def mark_welcome_shown():
    """Mark welcome page as shown"""
    st.session_state.welcome_shown = True

def should_show_welcome():
    """Check if welcome page should be shown"""
    return not st.session_state.get('welcome_shown', False)