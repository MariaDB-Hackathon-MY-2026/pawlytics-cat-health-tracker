"""
Dashboard - Main Overview Page
Shows stats, recent activity, health alerts, and quick actions
"""

import streamlit as st
import sys
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Add paths
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from backend.database import Database
from utils.session import init_session, get_session_id
from utils.helpers import *

# Check authentication
if 'authenticated' not in st.session_state or not st.session_state.get('authenticated'):
    st.warning("⚠️ Please log in first!")
    st.info("👉 Go back to welcome page to enter your name")
    st.stop()

# Get user info
user_id = st.session_state.get('user_id')
user_name = st.session_state.get('user_name', 'Guest')
is_guest = (user_name == "Guest")  # Check if guest mode

# Page config
st.set_page_config(
    page_title="Dashboard - Pawlytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize
init_session()
db = Database()

# ==========================================
# CSS STYLING - MAXIMUM VISIBILITY
# ==========================================

st.markdown("""
<style>
    /* Force all text to be dark */
    .stApp {
        background: #f1f5f9 !important;
    }
    
    .main, .block-container {
        background: transparent !important;
    }
    
    /* Force ALL text to be black/dark */
    * {
        color: #0f172a !important;
    }
    
    /* But keep sidebar text white */
    [data-testid="stSidebar"] * {
        color: #e2e8f0 !important;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6, .stMarkdown h1, .stMarkdown h2 {
        color: #0f172a !important;
        font-weight: 700 !important;
    }
    
    /* Metric cards - SOLID WHITE background */
    .metric-card {
        background: white !important;
        border-radius: 20px;
        padding: 1.5rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        border: 1px solid #cbd5e1;
        transition: all 0.3s;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #4f46e5, #7c3aed, #ec4899);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: #0f172a !important;
        margin-bottom: 0.25rem;
    }
    
    .metric-label {
        color: #475569 !important;
        font-size: 0.875rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Alert cards - SOLID backgrounds */
    .alert-card {
        background: white !important;
        border-radius: 16px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    }
    
    .alert-card:hover {
        transform: translateX(4px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
    }
    
    .alert-critical {
        border-left-color: #dc2626 !important;
        background: #fef2f2 !important;
    }
    
    .alert-high {
        border-left-color: #ea580c !important;
        background: #fff7ed !important;
    }
    
    .alert-medium {
        border-left-color: #eab308 !important;
        background: #fefce8 !important;
    }
    
    .alert-low {
        border-left-color: #16a34a !important;
        background: #f0fdf4 !important;
    }
    
    .alert-card strong, .alert-card p, .alert-card span {
        color: #1e293b !important;
    }
    
    /* Activity items - SOLID white */
    .activity-item {
        background: white !important;
        border-radius: 12px;
        padding: 0.875rem;
        margin: 0.5rem 0;
        border: 1px solid #cbd5e1;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }
    
    .activity-item:hover {
        background: #f8fafc !important;
        border-color: #94a3b8;
        transform: translateX(4px);
    }
    
    .activity-item strong, .activity-item div, .activity-item span {
        color: #1e293b !important;
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #0f172a !important;
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #cbd5e1;
    }
    
    /* Quick action buttons */
    .stButton > button {
        background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.6rem 1rem !important;
        font-weight: 600 !important;
        transition: all 0.3s !important;
        width: 100% !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(79, 70, 229, 0.3);
    }
    
    /* Sidebar - keep as is */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
    }
    
    /* Divider */
    .custom-divider {
        margin: 1.5rem 0;
        border: none;
        height: 1px;
        background: #cbd5e1;
    }
    
    /* Welcome text */
    .welcome-text {
        color: #475569 !important;
        margin-top: -0.25rem;
    }
    
    /* Fix for info/success/warning boxes */
    .stAlert, .stAlert div, .stAlert p {
        color: #1e293b !important;
    }
    
    .stAlert {
        background-color: #fefce8 !important;
        border-left-color: #eab308 !important;
    }
    
    /* Fix for metric component */
    [data-testid="stMetricValue"] {
        color: #0f172a !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #475569 !important;
    }
    
    /* Ensure plotly charts have dark text */
    .js-plotly-plot .plotly .main-svg {
        background: transparent !important;
    }
    
    /* Fix any transparent backgrounds */
    div[data-testid="stVerticalBlock"] > div {
        background: transparent !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# HEADER - MINIMAL & CLEAN
# ==========================================

st.title(f"📊 {user_name}'s Dashboard")
st.caption(f"Welcome back! Here's your cat nutrition analytics.")

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)


# ==========================================
# KEY STATISTICS
# ==========================================



try:
    # Check if guest mode
    if is_guest:
        # Guest sees ALL data from database
        my_cats = db.get_all_cats()
        my_kibbles = db.get_all_kibbles()
        
    else:
        # Normal user sees only their data
        my_cats = db.get_cats_by_user(user_id)
        my_kibbles = db.get_kibbles_by_user(user_id)
    
    # Calculate stats
    total_cats = len(my_cats)
    total_brands = len(my_kibbles)
    total_scans = total_brands
    
    # Calculate average quality
    if my_kibbles:
        rating_map = {'A': 5, 'B': 4, 'C': 3, 'D': 2, 'F': 1}
        ratings = [rating_map.get(k.get('rating', 'F'), 1) for k in my_kibbles]
        avg_quality = sum(ratings) / len(ratings) if ratings else 0
    else:
        avg_quality = 0
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">🐱</div>
            <div class="metric-value">{total_cats}</div>
            <div class="metric-label">My Cats</div>
            <div style="font-size: 0.75rem; color: #16a34a; margin-top: 0.5rem;">✓ Your felines</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">🏷️</div>
            <div class="metric-value">{total_brands}</div>
            <div class="metric-label">Brands Scanned</div>
            <div style="font-size: 0.75rem; color: #16a34a; margin-top: 0.5rem;">✓ Your scans</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">🤖</div>
            <div class="metric-value">{total_scans}</div>
            <div class="metric-label">AI Scans</div>
            <div style="font-size: 0.75rem; color: #16a34a; margin-top: 0.5rem;">✓ AI-powered</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">⭐</div>
            <div class="metric-value">{avg_quality:.1f} / 5.0</div>
            <div class="metric-label">Avg Quality</div>
            <div style="font-size: 0.75rem; color: #ea580c; margin-top: 0.5rem;">★ Your brands</div>
        </div>
        """, unsafe_allow_html=True)
    
except Exception as e:
    st.error(f"⚠️ Error loading statistics: {e}")

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# ANALYTICS CHARTS
# ==========================================

st.markdown('<h2 class="section-header">📊 Analytics Overview</h2>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    # Grade distribution pie chart (FIXED - removed weight='bold')
    try:
        if is_guest:
            kibbles = db.get_all_kibbles()
        else:
            kibbles = db.get_kibbles_by_user(user_id)
        if kibbles:
            df = pd.DataFrame(kibbles)
            grade_counts = df['rating'].value_counts().sort_index()
            
            color_map = {
                'A': '#22c55e', 'A+': '#22c55e',
                'B': '#eab308', 'B+': '#eab308',
                'C': '#f97316', 'C+': '#f97316',
                'D': '#ef4444', 'F': '#dc2626'
            }
            
            fig = go.Figure(data=[go.Pie(
                labels=grade_counts.index,
                values=grade_counts.values,
                hole=0.45,
                marker=dict(colors=[color_map.get(g, '#94a3b8') for g in grade_counts.index]),
                textinfo='label+percent',
                textposition='auto',
                textfont=dict(color='white', size=12),
                hovertemplate="<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>"
            )])
            
            fig.update_layout(
                title=dict(text="<b>Food Quality Distribution</b>", font=dict(size=16, color='#0f172a')),  # ✅ FIXED!
                height=400,
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5, font=dict(color='#1e293b')),
                paper_bgcolor='white',
                plot_bgcolor='white'
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("📭 No data available for quality distribution")
    except Exception as e:
        st.info("📭 Insufficient data for quality chart")

with col2:
    # ⭐ Top Brands by Value Chart (FULLY FIXED!)
    try:
        if is_guest:
            kibbles = db.get_all_kibbles()
        else:
            kibbles = db.get_kibbles_by_user(user_id)
        
        if kibbles and len(kibbles) > 0:
            df = pd.DataFrame(kibbles)
            
            # Force numeric conversion
            df['protein_pct'] = pd.to_numeric(df['protein_pct'], errors='coerce')
            df['price_per_kg'] = pd.to_numeric(df['price_per_kg'], errors='coerce')
            
            # Calculate value score (Protein % ÷ Price per KG)
            df['value_score'] = df['protein_pct'] / df['price_per_kg']
            
            # Ensure value_score is numeric
            df['value_score'] = pd.to_numeric(df['value_score'], errors='coerce')
            
            # Remove any rows with invalid data (NaN, zero, negative)
            df = df[df['value_score'].notna() & (df['value_score'] > 0)]
            
            if len(df) > 0:
                # Get top 10 brands by value (or less if fewer brands)
                top_n = min(10, len(df))
                df_top = df.nlargest(top_n, 'value_score')[['brand_name', 'value_score', 'rating', 'protein_pct', 'price_per_kg']].copy()
                
                # Assign colors based on grade
                color_map = {
                    'A': '#22c55e', 'A+': '#22c55e',
                    'B': '#eab308', 'B+': '#eab308', 
                    'C': '#f97316', 'C+': '#f97316',
                    'D': '#ef4444', 'F': '#dc2626'
                }
                df_top['color'] = df_top['rating'].apply(lambda x: color_map.get(str(x), '#94a3b8'))
                
                # Create horizontal bar chart
                fig = go.Figure(data=[go.Bar(
                    x=df_top['value_score'],
                    y=df_top['brand_name'],
                    orientation='h',
                    marker=dict(
                        color=df_top['color'],
                        line=dict(color='white', width=1.5)
                    ),
                    text=[f"{v:.2f}" for v in df_top['value_score']],
                    textposition='outside',
                    textfont=dict(color='#0f172a', size=11),
                    hovertemplate="<b>%{y}</b><br>" +
                                "Value Score: %{x:.2f}<br>" +
                                "Protein: %{customdata[0]:.1f}%<br>" +
                                "Price: RM %{customdata[1]:.2f}/kg<br>" +
                                "Grade: %{customdata[2]}" +
                                "<extra></extra>",
                    customdata=df_top[['protein_pct', 'price_per_kg', 'rating']].values
                )])
                
                fig.update_layout(
                    title=dict(
                        text=f"<b>Top {top_n} Brands by Value Score</b>",  # ✅ FIXED: HTML bold tag
                        font=dict(size=16, color='#0f172a')  # ✅ FIXED: Removed weight
                    ),
                    xaxis=dict(
                        title="Value Score (Protein % ÷ Price)", 
                        titlefont=dict(color='#475569', size=12),
                        tickfont=dict(color='#475569', size=11),
                        gridcolor='#e2e8f0',
                        showgrid=True
                    ),
                    yaxis=dict(
                        title="", 
                        tickfont=dict(color='#1e293b', size=11),
                        autorange="reversed"  # Top brand at top
                    ),
                    height=400,
                    showlegend=False,
                    paper_bgcolor='white',
                    plot_bgcolor='white',
                    margin=dict(l=10, r=10, t=40, b=40)
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Add helpful explanation
                st.caption("💡 **Value Score** = Protein % ÷ Price per KG. Higher score = Better protein content for your money!")
            else:
                st.info("📭 Need valid price and protein data to calculate value scores")
        else:
            st.info("📭 No brands analyzed yet. Start scanning!")
            
    except Exception as e:
        st.error(f"⚠️ Error: {e}")
        import traceback
        st.code(traceback.format_exc())

# ==========================================
# HEALTH ALERTS
# ==========================================

st.markdown('<h2 class="section-header">⚠️ Health Alerts</h2>', unsafe_allow_html=True)

try:
    if is_guest:
        # Guest sees all alerts
        alerts_query = """
            SELECT ha.*, c.name as cat_name
            FROM health_alerts ha
            JOIN cats c ON ha.cat_id = c.id
            WHERE ha.is_read = 0
            ORDER BY ha.created_at DESC
            LIMIT 5
        """
    else:
        # User sees only their cats' alerts
        alerts_query = """
            SELECT ha.*, c.name as cat_name
            FROM health_alerts ha
            JOIN cats c ON ha.cat_id = c.id
            WHERE c.user_id = %s AND ha.is_read = 0
            ORDER BY ha.created_at DESC
            LIMIT 5
        """

    alerts = db.execute_query(alerts_query) if is_guest else db.execute_query(alerts_query, (user_id,))
    
    if alerts:
        for alert in alerts:
            severity_class = 'alert-low'
            icon = '🟢'
            
            if alert['severity'] == 'high':
                severity_class = 'alert-high'
                icon = '🔴'
            elif alert['severity'] == 'critical':
                severity_class = 'alert-critical'
                icon = '💀'
            elif alert['severity'] == 'medium':
                severity_class = 'alert-medium'
                icon = '🟡'
            
            days_ago = calculate_days_ago(alert['created_at'])
            
            st.markdown(f"""
            <div class="alert-card {severity_class}">
                <div style="display: flex; justify-content: space-between; align-items: start;">
                    <div style="flex: 1;">
                        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                            <span style="font-size: 1.2rem;">{icon}</span>
                            <strong style="font-size: 1rem;">{alert['cat_name']}</strong>
                            <span style="background: rgba(0,0,0,0.08); padding: 2px 8px; border-radius: 12px; font-size: 0.7rem;">
                                {alert['alert_type'].replace('_', ' ').title()}
                            </span>
                        </div>
                        <p style="margin: 0; font-size: 0.875rem;">{alert['message']}</p>
                    </div>
                    <div style="font-size: 0.7rem; white-space: nowrap; margin-left: 12px;">
                        {days_ago} day{'s' if days_ago != 1 else ''} ago
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.success("✅ No active health alerts! All cats are doing well.")
        
except Exception as e:
    st.info("📭 No health alerts at the moment")

# ==========================================
# RECENT ACTIVITY
# ==========================================

col1, col2 = st.columns(2)

with col1:
    st.markdown('<h2 class="section-header">🕐 Recent Scans</h2>', unsafe_allow_html=True)
    
    try:
        if is_guest:
            recent_kibbles = db.execute_query("""
                SELECT brand_name, protein_pct, rating, created_at
                FROM kibbles
                ORDER BY created_at DESC
                LIMIT 5
            """)
        else:
            recent_kibbles = db.execute_query("""
                SELECT brand_name, protein_pct, rating, created_at
                FROM kibbles
                WHERE user_id = %s
                ORDER BY created_at DESC
                LIMIT 5
            """, (user_id,))
        
        if recent_kibbles:
            for kibble in recent_kibbles:
                emoji = get_grade_emoji(kibble['rating'])
                date_str = kibble['created_at'].strftime('%b %d') if kibble['created_at'] else 'Recent'
                
                st.markdown(f"""
                <div class="activity-item">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <span style="font-size: 1.1rem;">{emoji}</span>
                            <strong style="margin-left: 8px;">{kibble['brand_name']}</strong>
                        </div>
                        <span style="font-size: 0.7rem;">{date_str}</span>
                    </div>
                    <div style="margin-top: 6px; font-size: 0.8rem;">
                        Protein: {kibble['protein_pct']}% • Grade: {kibble['rating']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("📭 No scans yet. Start by scanning a label!")
    except Exception as e:
        st.info("📭 No recent scans")

with col2:
    st.markdown('<h2 class="section-header">🐱 Your Cats</h2>', unsafe_allow_html=True)
    
    try:
        if is_guest:
            cats = db.get_all_cats()
        else:
            cats = db.get_cats_by_user(user_id)
                
        if cats:
            for cat in cats[:5]:
                condition_color = "#16a34a" if cat['condition_score'] == 'Ideal' else "#ea580c"
                
                st.markdown(f"""
                <div class="activity-item">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <span style="font-size: 1.1rem;">🐾</span>
                            <strong style="margin-left: 8px;">{cat['name']}</strong>
                        </div>
                        <span style="background: {condition_color}; color: white; padding: 2px 8px; border-radius: 12px; font-size: 0.7rem;">
                            {cat['condition_score']}
                        </span>
                    </div>
                    <div style="margin-top: 6px; font-size: 0.8rem;">
                        {cat['age_months']} months • {cat['weight_kg']} kg
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("📭 No cats registered. Add your first cat!")
    except Exception as e:
        st.info("📭 No cats found")

# ==========================================
# QUICK ACTIONS
# ==========================================

st.markdown('<h2 class="section-header">⚡ Quick Actions</h2>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("📸 Scan New Food", use_container_width=True, type="primary"):
        st.switch_page("pages/3_Scanner.py")

with col2:
    if st.button("🐱 Add New Cat", use_container_width=True):
        st.switch_page("pages/2_Cat_Profiles.py")

with col3:
    if st.button("📈 View Analytics", use_container_width=True):
        st.switch_page("pages/4_Analytics.py")



# ==========================================
# FOOTER
# ==========================================

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.caption(f"""
    <div style="text-align: center;">
        🐾 Pawlytics - Intelligent Cat Nutrition Platform<br>
        
    </div>
    """, unsafe_allow_html=True)


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

