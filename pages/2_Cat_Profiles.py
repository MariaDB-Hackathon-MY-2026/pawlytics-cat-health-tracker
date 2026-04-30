"""
Cat Profiles - CRUD Management
Register, view, edit, and delete cat profiles
"""

import streamlit as st
import sys
from pathlib import Path
import pandas as pd

# Add paths
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from backend.database import Database
from utils.session import init_session, set_current_cat, get_current_cat
from utils.helpers import *

# Check authentication
if 'authenticated' not in st.session_state or not st.session_state.get('authenticated'):
    st.warning("⚠️ Please log in first!")
    st.info("👉 Go back to welcome page to enter your name")
    st.stop()

# Get user info
user_id = st.session_state.get('user_id')
user_name = st.session_state.get('user_name', 'Guest')
is_guest = (user_name == "Guest")

# Page config
st.set_page_config(
    page_title="Cat Profiles - Pawlytics",
    page_icon="🐱",
    layout="wide"
)

# Initialize
init_session()
db = Database()

# ==========================================
# SIMPLE & CLEAN CSS - MAX VISIBILITY
# ==========================================

st.markdown("""
<style>
    /* Force white background for main content */
    .stApp {
        background: #f1f5f9 !important;
    }
    
    .main .block-container {
        background: white !important;
        border-radius: 20px !important;
        padding: 2rem !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05) !important;
    }
    
    /* Force ALL text to be dark */
    .main * {
        color: #1e293b !important;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #0f172a !important;
        font-weight: 700 !important;
    }
    
    /* Labels */
    label, .stMarkdown label {
        color: #0f172a !important;
        font-weight: 600 !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #1e293b !important;
    }
    
    [data-testid="stSidebar"] * {
        color: #e2e8f0 !important;
    }
    
    /* ========== FIX FOR NUMBER INPUT BOXES ========== */
    /* Number input container */
    .stNumberInput {
        background: white !important;
    }
    
    .stNumberInput > div {
        background: white !important;
    }
    
    /* Number input field */
    .stNumberInput input {
        background: white !important;
        color: #1e293b !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 10px !important;
        padding: 0.5rem !important;
        font-size: 1rem !important;
    }
    
    /* Number input buttons (+ and -) */
    .stNumberInput button {
        background: #f1f5f9 !important;
        color: #1e293b !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 8px !important;
        margin: 0 2px !important;
    }
    
    .stNumberInput button:hover {
        background: #e2e8f0 !important;
        color: #0f172a !important;
    }
    
    .stNumberInput button svg {
        color: #1e293b !important;
        fill: #1e293b !important;
    }
    
    /* Focus state */
    .stNumberInput input:focus {
        border-color: #4f46e5 !important;
        box-shadow: 0 0 0 2px rgba(79, 70, 229, 0.1) !important;
        outline: none !important;
    }
    
    /* ========== TEXT INPUT FIX ========== */
    .stTextInput > div > div > input {
        background: white !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 10px !important;
        color: #1e293b !important;
        padding: 0.5rem !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #4f46e5 !important;
        box-shadow: 0 0 0 2px rgba(79, 70, 229, 0.1) !important;
    }
    
    /* ========== SELECTBOX FIX ========== */
    .stSelectbox > div > div {
        background: white !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 10px !important;
        color: #1e293b !important;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #94a3b8 !important;
    }
    
    /* ========== TEXT AREA FIX ========== */
    .stTextArea > div > textarea {
        background: white !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 10px !important;
        color: #1e293b !important;
    }
    
    .stTextArea > div > textarea:focus {
        border-color: #4f46e5 !important;
        box-shadow: 0 0 0 2px rgba(79, 70, 229, 0.1) !important;
    }
    
    /* ✅ ADD THIS - Force text area to be white */
    .stTextArea textarea {
        background-color: white !important;
        background: white !important;
        color: #1e293b !important;
        border: 1px solid #cbd5e1 !important;
    }
    
    /* ✅ ADD THIS - Container background */
    .stTextArea > div {
        background: white !important;
    }
    
    .stTextArea {
        background: white !important;
    }
    
    /* ✅ ADD THIS - Placeholder text color */
    .stTextArea textarea::placeholder {
        color: #94a3b8 !important;
        opacity: 1 !important;
    }

    /* ========== SLIDER FIX ========== */
    .stSlider > div {
        color: #1e293b !important;
    }
    
    .stSlider div[data-baseweb="slider"] {
        background: #e2e8f0 !important;
    }
    
    /* ========== CHECKBOX FIX ========== */
    .stCheckbox > label {
        color: #1e293b !important;
    }
    
    /* ========== BUTTON FIX ========== */
    .stButton > button {
        background: #4f46e5 !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.5rem 1rem !important;
        font-weight: 600 !important;
        transition: all 0.2s !important;
    }
    
    .stButton > button:hover {
        background: #6366f1 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 2px 8px rgba(79, 70, 229, 0.3) !important;
    }
    
    /* ========== FORCE WHITE TEXT ON BUTTONS ========== */
    .stButton > button,
    .stButton > button *,
    .stButton > button p,
    .stButton > button span,
    button[type="submit"],
    button[type="submit"] *,
    div[data-testid="baseButton-primary"],
    div[data-testid="baseButton-primary"] * {
        color: white !important;
    }

    /* Form submit buttons specifically */
    form button[kind="primary"],
    form button[kind="primary"] *,
    form button[kind="primary"] p,
    form button[kind="primary"] span {
        color: white !important;
    }
    
    /* Delete button */
    .stButton button[kind="secondary"] {
        background: #ef4444 !important;
    }
    
    .stButton button[kind="secondary"]:hover {
        background: #dc2626 !important;
    }
            
    /* ========== SIDEBAR BUTTON FIX ========== */
    [data-testid="stSidebar"] .stButton > button {
        background: #4f46e5 !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.5rem 1rem !important;
        font-weight: 600 !important;
        transition: all 0.2s !important;
        width: 100% !important;
    }

    [data-testid="stSidebar"] .stButton > button:hover {
        background: #6366f1 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 2px 8px rgba(79, 70, 229, 0.3) !important;
    }

    /* Make sure logout button in sidebar is also purple, not red */
    [data-testid="stSidebar"] .stButton button[kind="secondary"] {
        background: #4f46e5 !important;  /* Override the red */
    }

    [data-testid="stSidebar"] .stButton button[kind="secondary"]:hover {
        background: #6366f1 !important;
    }
    
    /* ========== CAT CARDS ========== */
    .cat-card {
        background: white !important;
        border-radius: 16px !important;
        padding: 1.5rem !important;
        margin: 1rem 0 !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
        border: 1px solid #cbd5e1 !important;
        transition: all 0.2s !important;
    }
    
    .cat-card:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 4px 16px rgba(0,0,0,0.15) !important;
        border-color: #94a3b8 !important;
    }
    
    .cat-avatar {
        font-size: 3rem !important;
        text-align: center !important;
        margin-bottom: 0.75rem !important;
    }
    
    .cat-name {
        font-size: 1.5rem !important;
        font-weight: 800 !important;
        text-align: center !important;
        color: #0f172a !important;
        margin-bottom: 0.5rem !important;
    }
    
    .cat-info {
        text-align: center !important;
        color: #475569 !important;
        margin: 0.35rem 0 !important;
        font-size: 0.85rem !important;
    }
    
    .cat-info strong {
        color: #0f172a !important;
    }
    
    .calorie-badge {
        background: #4f46e5 !important;
        color: white !important;
        padding: 0.5rem 1rem !important;
        border-radius: 30px !important;
        display: inline-block !important;
        font-weight: 700 !important;
        margin: 1rem 0 0 0 !important;
        font-size: 0.85rem !important;
        text-align: center !important;
        width: 100% !important;
    }
    
    .calorie-badge * {
        color: white !important;
    }
    
    /* ========== TABS ========== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem !important;
        background: #f8fafc !important;
        padding: 0.5rem !important;
        border-radius: 12px !important;
        border: 1px solid #e2e8f0 !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        font-weight: 600 !important;
        background: transparent !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: #4f46e5 !important;
    }
    
    .stTabs [aria-selected="true"] * {
        color: white !important;
    }
    
    /* ========== ALERT BOXES ========== */
    .stAlert {
        border-radius: 10px !important;
    }
    
    .stAlert div, .stAlert p {
        color: #1e293b !important;
    }
    
    .stInfo {
        background: #e0f2fe !important;
        border-left: 4px solid #0284c7 !important;
    }
    
    .stSuccess {
        background: #dcfce7 !important;
        border-left: 4px solid #16a34a !important;
    }
    
    .stWarning {
        background: #fef9c3 !important;
        border-left: 4px solid #eab308 !important;
    }
    
    .stError {
        background: #fee2e2 !important;
        border-left: 4px solid #dc2626 !important;
    }
    
    /* ========== DIVIDER ========== */
    .custom-divider {
        margin: 1.5rem 0 !important;
        border: none !important;
        height: 1px !important;
        background: #e2e8f0 !important;
    }
    
    /* ========== SECTION HEADER ========== */
    .section-header {
        font-size: 1.3rem !important;
        font-weight: 700 !important;
        color: #0f172a !important;
        margin: 1rem 0 1rem 0 !important;
        padding-bottom: 0.5rem !important;
        border-bottom: 2px solid #e2e8f0 !important;
    }
    
    /* ========== EDIT FORM ========== */
    .edit-form-container {
        background: #f8fafc !important;
        padding: 1rem !important;
        border-radius: 12px !important;
        margin-top: 1rem !important;
        border: 1px solid #e2e8f0 !important;
    }
    
    /* ========== CALORIE RESULT ========== */
    .calorie-result {
        background: #4f46e5 !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        margin-top: 0.5rem !important;
        text-align: center !important;
    }
    
    .calorie-result * {
        color: white !important;
    }
    
    /* ========== FIX FOR STEP BUTTONS INSIDE NUMBER INPUT ========== */
    div[data-testid="stNumberInput"] button {
        background: #e2e8f0 !important;
        border: 1px solid #cbd5e1 !important;
        color: #1e293b !important;
    }
    
    div[data-testid="stNumberInput"] button svg {
        color: #1e293b !important;
        fill: #1e293b !important;
    }
    
    /* Make sure number input text is visible */
    input[type="number"] {
        color: #1e293b !important;
        background: white !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# HEADER
# ==========================================

st.markdown(f'<h1 style="font-size: 2rem; font-weight: 800; margin-bottom: 0;">🐱 {user_name}\'s Cats</h1>', unsafe_allow_html=True)
st.markdown('<p style="color: #64748b; margin-bottom: 1rem;">Manage your cats\' profiles and track their health journey</p>', unsafe_allow_html=True)

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# Sidebar user info
st.sidebar.markdown("---")
st.sidebar.markdown(f"### 👤 {user_name}")
st.sidebar.caption(f"User ID: {user_id[:8] if user_id else 'N/A'}")

# Edit name button
if not is_guest:
    if st.sidebar.button("✏️ Edit Name", use_container_width=True):
        st.session_state['show_name_editor'] = True

# Name editor popup
if st.session_state.get('show_name_editor'):
    with st.sidebar:
        new_name = st.text_input("New Name:", value=user_name, key="edit_name_input")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Save", use_container_width=True, key="save_name"):
                if new_name and new_name.strip():
                    import hashlib
                    st.session_state['user_name'] = new_name.strip()
                    st.session_state['user_id'] = hashlib.md5(new_name.strip().encode()).hexdigest()[:8]
                    st.session_state['show_name_editor'] = False
                    st.success(f"✅ Name changed to {new_name}!")
                    st.rerun()
        
        with col2:
            if st.button("Cancel", use_container_width=True, key="cancel_name"):
                st.session_state['show_name_editor'] = False
                st.rerun()

if st.sidebar.button("🚪 Logout", use_container_width=True):
    # Clear session
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.switch_page("Welcome.py")

# ==========================================
# TABS
# ==========================================

tab1, tab2 = st.tabs(["📋 All Cats", "➕ Add New Cat"])

# ==========================================
# TAB 1: ALL CATS
# ==========================================

with tab1:
    st.markdown('<p class="section-header">Furry Friends Gallery</p>', unsafe_allow_html=True)
    
    # Guest mode banner
    if is_guest:
        st.info("🎯 **Guest Mode** - Viewing all cats from community. Login to add & manage your own cats!")
    
    try:
        # Get cats based on user type
        if is_guest:
            cats = db.get_all_cats()  # Guest sees all cats
        else:
            cats = db.get_cats_by_user(user_id)  # User sees only theirs
        
        if cats:
            cols_per_row = 3
            for i in range(0, len(cats), cols_per_row):
                cols = st.columns(cols_per_row)
                
                for j, col in enumerate(cols):
                    if i + j < len(cats):
                        cat = cats[i + j]
                        
                        with col:
                            rer = calculate_rer(cat['weight_kg'])
                            der = calculate_der(rer, cat['activity_level'])
                            
                            avatar = "🐈" if cat['gender'] == 'Male' else "🐈‍⬛" if cat['gender'] == 'Female' else "🐱"
                            
                            st.markdown(f"""
                            <div class="cat-card">
                                <div class="cat-avatar">{avatar}</div>
                                <div class="cat-name">{cat['name']}</div>
                                <div class="cat-info">📅 {cat['age_months']} months old</div>
                                <div class="cat-info">⚖️ {cat['weight_kg']} kg • {cat['gender']}</div>
                                <div class="cat-info">💪 Condition: <strong>{cat['condition_score']}</strong></div>
                                <div class="cat-info">🏃 Activity: {cat['activity_level']}</div>
                                <div class="calorie-badge">🔥 {der} kcal/day</div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            col_a, col_b = st.columns(2)

                            with col_a:
                                if is_guest:
                                    st.button(f"✏️ Edit", key=f"edit_{cat['id']}", use_container_width=True, disabled=True, help="🔒 Login to edit")
                                else:
                                    if st.button(f"✏️ Edit", key=f"edit_{cat['id']}", use_container_width=True):
                                        st.session_state[f'editing_cat_{cat["id"]}'] = True

                            with col_b:
                                if is_guest:
                                    st.button(f"🗑️ Delete", key=f"delete_{cat['id']}", use_container_width=True, type="secondary", disabled=True, help="🔒 Login to delete")
                                else:
                                    if st.button(f"🗑️ Delete", key=f"delete_{cat['id']}", use_container_width=True, type="secondary"):
                                        if st.session_state.get(f'confirm_delete_{cat["id"]}'):
                                            db.execute_update("DELETE FROM cats WHERE id = %s", (cat['id'],))
                                            st.success(f"✅ {cat['name']} deleted successfully!")
                                            st.rerun()
                                        else:
                                            st.session_state[f'confirm_delete_{cat["id"]}'] = True
                                            st.warning("⚠️ Click again to confirm deletion")
                            
                            if st.session_state.get(f'editing_cat_{cat["id"]}'):
                                with st.container():
                                    st.markdown('<div class="edit-form-container">', unsafe_allow_html=True)
                                    st.markdown("**✏️ Edit Profile**")
                                    
                                    with st.form(f"edit_form_{cat['id']}"):
                                        new_name = st.text_input("Name", value=cat['name'], key=f"name_{cat['id']}")
                                        new_age = st.number_input("Age (months)", value=cat['age_months'], min_value=1, key=f"age_{cat['id']}")
                                        new_weight = st.number_input("Weight (kg)", value=float(cat['weight_kg']), min_value=0.5, step=0.1, key=f"weight_{cat['id']}")
                                        new_condition = st.selectbox("Condition", 
                                            options=['Underweight', 'Ideal', 'Overweight', 'Obese'],
                                            index=['Underweight', 'Ideal', 'Overweight', 'Obese'].index(cat['condition_score']),
                                            key=f"condition_{cat['id']}")
                                        new_activity = st.selectbox("Activity Level",
                                            options=['Sedentary', 'Moderate', 'Active', 'Very Active'],
                                            index=['Sedentary', 'Moderate', 'Active', 'Very Active'].index(cat['activity_level']),
                                            key=f"activity_{cat['id']}")
                                        
                                        col1, col2 = st.columns(2)
                                        
                                        with col1:
                                            if st.form_submit_button("💾 Save Changes", use_container_width=True):
                                                update_query = """
                                                    UPDATE cats 
                                                    SET name = %s, age_months = %s, weight_kg = %s, 
                                                        condition_score = %s, activity_level = %s
                                                    WHERE id = %s
                                                """
                                                db.execute_update(update_query, (new_name, new_age, new_weight, 
                                                                                 new_condition, new_activity, cat['id']))
                                                st.success("✅ Profile updated successfully!")
                                                del st.session_state[f'editing_cat_{cat["id"]}']
                                                st.rerun()
                                        
                                        with col2:
                                            if st.form_submit_button("❌ Cancel", use_container_width=True):
                                                del st.session_state[f'editing_cat_{cat["id"]}']
                                                st.rerun()
                                    
                                    st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("📭 No cats registered yet. Add your first cat in the 'Add New Cat' tab!")
            
    except Exception as e:
        st.error(f"⚠️ Error loading cats: {e}")

# ==========================================
# TAB 2: ADD NEW CAT
# ==========================================

with tab2:
    st.markdown('<p class="section-header">Tell Us About Your Cat</p>', unsafe_allow_html=True)
    
    # Block form for guests
    if is_guest:
        st.warning("Please login with your name to add your own cats!")
        st.info("**Try our AI features instead:**")
        st.markdown("""
        - 📸 **Scanner** - Analyze kibble labels with AI
        - 🐱 **Cat Photo Analyzer** - Check body condition
        - 💬 **AI Chat** - Ask nutrition questions
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📸 Try Scanner", use_container_width=True, type="primary"):
                st.switch_page("pages/3_Scanner.py")
        with col2:
            if st.button("🔐 Login to Add Cats", use_container_width=True):
                st.switch_page("Welcome.py")
        
        st.stop()  # Stop here, don't show form
    
    with st.form("add_cat_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("🐱 Cat Name *", placeholder="e.g., Luna, Simba, Oliver")
            age_months = st.number_input("📅 Age (months) *", min_value=1, max_value=300, value=12, step=1)
            weight_kg = st.number_input("⚖️ Weight (kg) *", min_value=0.5, max_value=30.0, value=4.0, step=0.1)
            gender = st.selectbox("🚻 Gender", options=['Male', 'Female', 'Unknown'])
        
        with col2:
            neutered = st.checkbox("✅ Neutered/Spayed")
            condition_score = st.selectbox("💪 Body Condition", 
                options=['Underweight', 'Ideal', 'Overweight', 'Obese'],
                index=1)
            bcs_numeric = st.slider("Body Condition Score (1-9)", min_value=1, max_value=9, value=5,
                help="1=Emaciated, 5=Ideal, 9=Severely Obese")
            activity_level = st.selectbox("🏃 Activity Level",
                options=['Sedentary', 'Moderate', 'Active', 'Very Active'],
                index=1)
        
        st.markdown("""
        <label style="font-weight: 600; margin-bottom: 0.5rem; display: block;">🏥 Health Conditions (optional)</label>
        """, unsafe_allow_html=True)

        # ✅ ACTUAL WORKING WIDGET (hidden styling)
        health_conditions = st.text_area(
            "",  # No label (we showed it above in HTML)
            placeholder="e.g., Diabetes, Kidney disease, Food allergies",
            height=100,
            key="health_conditions",
            label_visibility="collapsed"  # Hide the Streamlit label
        )
        
        owner_name = st.text_input("👤 Owner Name (optional)", placeholder="Your name")
        
        if weight_kg > 0:
            rer = calculate_rer(weight_kg)
            der = calculate_der(rer, activity_level)
            st.info(f"📊 **Estimated Daily Calorie Needs:** {der} kcal/day (RER: {rer} kcal)")
        
        col_left, col_btn, col_right = st.columns([1.5, 1, 1.5])

        with col_btn:
            submitted = st.form_submit_button("➕ Add Cat", use_container_width=True, type="primary")
        
        if submitted:
            if not name:
                st.error("❌ Cat name is required!")
            else:
                # Calculate age in years
                age_years = age_months // 12
                remaining_months = age_months % 12

                cat_id = db.add_cat(
                    name=name,
                    breed='Mixed',  # Default breed
                    age_years=age_years,
                    age_months=remaining_months,
                    weight_kg=weight_kg,
                    gender=gender,
                    activity_level=activity_level,
                    condition_score=condition_score,
                    health_conditions=health_conditions or None,
                    bcs_numeric=bcs_numeric,
                    user_id=user_id,  # ← ADD THIS
                    user_name=user_name  # ← ADD THIS
                )
                
                               
                if cat_id:
                    st.success(f"✅ {name} has been added successfully! 🎉")
                    st.balloons()
                    
                    if condition_score in ['Overweight', 'Obese']:
                        alert_data = {
                            'cat_id': cat_id,
                            'alert_type': 'overweight',
                            'severity': 'medium' if condition_score == 'Overweight' else 'high',
                            'message': f'{name} is {condition_score.lower()}. Consider adjusting diet and increasing activity.'
                        }
                        db.execute_update("""
                            INSERT INTO health_alerts (cat_id, alert_type, severity, message)
                            VALUES (%s, %s, %s, %s)
                        """, (alert_data['cat_id'], alert_data['alert_type'], 
                              alert_data['severity'], alert_data['message']))
                    
                    st.rerun()
                else:
                    st.error("❌ Failed to add cat. Please try again.")

# ==========================================
# CALORIE CALCULATOR TOOL
# ==========================================

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
st.markdown('<p class="section-header">🧮 Calorie Calculator Tool</p>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    calc_weight = st.number_input(
        "🐱 Cat Weight (kg)", 
        min_value=0.5, 
        max_value=30.0, 
        value=4.0, 
        step=0.1, 
        key="calc_weight"
    )

with col2:
    calc_activity = st.selectbox(
        "🏃 Activity Level", 
        options=['Sedentary', 'Moderate', 'Active', 'Very Active'],
        key="calc_activity"
    )

with col3:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("📊 Calculate Calories", use_container_width=True, key="calc_btn"):
        rer = calculate_rer(calc_weight)
        der = calculate_der(rer, calc_activity)
        
        st.markdown(f"""
        <div class="calorie-result">
            <strong>🔥 Caloric Needs</strong><br>
            RER: {rer} kcal/day<br>
            DER: {der} kcal/day<br>
            Per meal (2x/day): {der//2} kcal
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# FOOTER
# ==========================================

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.caption("""
    <div style="text-align: center; color: #64748b;">
        🐾 Pawlytics - Intelligent Cat Nutrition Platform<br>
        Track health, monitor nutrition, and optimize wellbeing
    </div>
    """, unsafe_allow_html=True)


