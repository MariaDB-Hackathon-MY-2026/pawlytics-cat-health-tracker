"""
Pawlytics - Main Application
Welcome Page & Navigation Router
"""

import streamlit as st
import sys
from pathlib import Path

# Add paths
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from backend.database import Database
from backend.gemini_service import GeminiAnalyzer
from utils.session import init_session, should_show_welcome, mark_welcome_shown

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Pawlytics - AI Pet Nutrition",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session
init_session()

# Initialize services
from backend.database import db_instance

def init_services():
    return db_instance, GeminiAnalyzer()

db, gemini = init_services()


# DEBUG: Check if method exists
print("🔍 Checking GeminiAnalyzer methods...")
print("Has analyze_image_with_prompt?", hasattr(gemini, 'analyze_image_with_prompt'))
print("Has analyze_kibble_label?", hasattr(gemini, 'analyze_kibble_label'))
print("Has chat?", hasattr(gemini, 'chat'))

# ==========================================
# MODERN CSS STYLING
# ==========================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&family=Inter:wght@400;500;600&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3 {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Fix button text to be WHITE */
.stButton > button {
    background: linear-gradient(135deg, #667eea, #764ba2) !important;
    color: white !important;
    font-weight: 700 !important;
    border: none !important;
    padding: 1rem 2rem !important;
    font-size: 1.1rem !important;
}

.stButton > button * {
    color: white !important;
}

/* Feature cards text fix */
.feature-card h3 {
    color: #1a1a1a !important;
}

.feature-card p {
    color: #555 !important;
}
    
    /* Background gradient */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        background-attachment: fixed;
    }
    
    /* Content container */
    .block-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border-radius: 30px;
        padding: 3rem;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
            
    /* Make main content text dark and readable */
    .main * {
        color: #1a1a1a !important;
    }

    .main label {
        color: #1a1a1a !important;
        font-weight: 600 !important;
    }
    
    /* Animated gradient text */
    .hero-title {
        font-size: 5rem;
        font-weight: 800;
        background: linear-gradient(120deg, #667eea, #764ba2, #f093fb, #667eea);
        background-size: 300% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        animation: gradient-flow 4s ease infinite;
        letter-spacing: -3px;
        line-height: 1.2;
    }
    
    @keyframes gradient-flow {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    .hero-subtitle {
        text-align: center;
        font-size: 1.5rem;
        color: #666;
        font-weight: 500;
        margin: 1rem 0 3rem 0;
    }
    
    /* Feature cards with glassmorphism */
    .feature-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.8), rgba(255,255,255,0.5));
        backdrop-filter: blur(10px);
        border-radius: 25px;
        padding: 2.5rem;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.3);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        height: 100%;
        position: relative;
        overflow: hidden;
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        transform: scaleX(0);
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-15px) scale(1.02);
        box-shadow: 0 25px 50px rgba(102, 126, 234, 0.4);
    }
    
    .feature-card:hover::before {
        transform: scaleX(1);
    }
    
    .feature-icon {
        font-size: 4rem;
        margin-bottom: 1.5rem;
        display: block;
        filter: drop-shadow(0 4px 10px rgba(102, 126, 234, 0.3));
    }
    
    .feature-title {
        background: linear-gradient(120deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 1rem 0;
    }
    
    .feature-desc {
        color: #555;
        line-height: 1.8;
        font-size: 1.05rem;
    }
    
    /* CTA Button */
    .cta-button {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 1.5rem 4rem;
        border-radius: 50px;
        font-size: 1.3rem;
        font-weight: 700;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
        border: none;
        cursor: pointer;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    .cta-button:hover {
        transform: translateY(-5px) scale(1.05);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.6);
    }
    
    /* Stats section */
    .stats-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 2rem;
        margin: 3rem 0;
    }
    
    .stat-card {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        border: 2px solid rgba(102, 126, 234, 0.2);
    }
    
    .stat-number {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(120deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .stat-label {
        color: #666;
        font-size: 1rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 0.5rem;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #1e293b !important;
    }
    
    [data-testid="stSidebar"] * {
        color: #e2e8f0 !important;
    }
    
    /* Smooth animations */
    .fade-in {
        animation: fadeIn 1s ease-in;
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .slide-up {
        animation: slideUp 0.8s ease-out;
    }
    
    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(50px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# WELCOME PAGE CONTENT
# ==========================================

if should_show_welcome():
    # Hero Section
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    st.markdown('<h1 style="font-size: 4rem; font-weight: 800; color: #1a1a1a; text-align: center; font-family: Poppins, sans-serif; margin-bottom: 0.5rem;">🐾 Pawlytics</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #333; font-size: 1.3rem; font-weight: 500; margin-bottom: 3rem;">AI-Powered Pet Nutrition Intelligence System</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Introduction
    st.markdown("""
    <div class="slide-up" style="text-align: center; max-width: 800px; margin: 0 auto 4rem auto; padding: 2rem;">
        <p style="font-size: 1.3rem; line-height: 1.8; color: #555;">
            Welcome to <strong style="background: linear-gradient(120deg, #667eea, #764ba2); 
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Pawlytics</strong> 
            — your intelligent companion for making informed decisions about your cat's nutrition. 
            Our AI-powered system helps you understand pet food labels, compare products, and ensure 
            your feline friend gets the <strong>best nutrition possible</strong>.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key Features
    st.markdown('<h2 style="text-align: center; margin: 4rem 0 2rem 0; font-size: 2.5rem;">✨ What Makes Pawlytics Special?</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3, gap="large")
    
    with col1:
        st.markdown("""
    <div style="background: rgba(255,255,255,0.95); backdrop-filter: blur(10px); border-radius: 20px; 
                padding: 2.5rem; box-shadow: 0 10px 30px rgba(0,0,0,0.1); border: 1px solid rgba(102,126,234,0.3); 
                transition: all 0.3s ease; height: 100%;">
        <div style="font-size: 3rem; margin-bottom: 1rem; text-align: center;">📸</div>
        <h3 style="color: #1a1a1a; font-weight: 700; font-size: 1.5rem; margin-bottom: 1rem; text-align: center;">
            AI Vision Scanner
        </h3>
        <p style="color: #555; line-height: 1.6; font-size: 1rem; text-align: center;">
            Upload kibble labels and let our advanced AI extract nutrition data instantly with 95%+ accuracy.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
    <div style="background: rgba(255,255,255,0.95); backdrop-filter: blur(10px); border-radius: 20px; 
                padding: 2.5rem; box-shadow: 0 10px 30px rgba(0,0,0,0.1); border: 1px solid rgba(102,126,234,0.3); 
                transition: all 0.3s ease; height: 100%;">
        <div style="font-size: 3rem; margin-bottom: 1rem; text-align: center;">📊</div>
        <h3 style="color: #1a1a1a; font-weight: 700; font-size: 1.5rem; margin-bottom: 1rem; text-align: center;">
            Smart Analytics
        </h3>
        <p style="color: #555; line-height: 1.6; font-size: 1rem; text-align: center;">
            Compare brands, analyze cost-to-nutrient ratios, and discover the best value options for your budget.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
    <div style="background: rgba(255,255,255,0.95); backdrop-filter: blur(10px); border-radius: 20px; 
                padding: 2.5rem; box-shadow: 0 10px 30px rgba(0,0,0,0.1); border: 1px solid rgba(102,126,234,0.3); 
                transition: all 0.3s ease; height: 100%;">
        <div style="font-size: 3rem; margin-bottom: 1rem; text-align: center;">🐱</div>
        <h3 style="color: #1a1a1a; font-weight: 700; font-size: 1.5rem; margin-bottom: 1rem; text-align: center;">
            Health Tracking
        </h3>
        <p style="color: #555; line-height: 1.6; font-size: 1rem; text-align: center;">
            Monitor your cat's body condition, and receive personalized recommendations.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats Section
    st.markdown('<div style="margin: 5rem 0 3rem 0;">', unsafe_allow_html=True)
    
    try:
        stats = db.get_table_stats()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{stats.get('kibbles', 0)}</div>
                <div class="stat-label">Brands Analyzed</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{stats.get('cats', 0)}</div>
                <div class="stat-label">Cats Tracked</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{stats.get('kibbles', 0)}</div>
                <div class="stat-label">AI Scans Performed</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class="stat-card">
                <div class="stat-number">95%</div>
                <div class="stat-label">AI Accuracy</div>
            </div>
            """, unsafe_allow_html=True)
    except:
        pass
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # CTA Button
    st.markdown('<div style="text-align: center; margin: 5rem 0 3rem 0;">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 ENTER DASHBOARD", key="enter_dashboard", use_container_width=True, type="primary"):
            mark_welcome_shown()
            st.switch_page("pages/1_Dashboard.py")  
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div style="text-align: center; color: #888; padding: 3rem 0 1rem 0; border-top: 1px solid rgba(0,0,0,0.1); margin-top: 5rem;">
        <p style="font-size: 1.1rem; margin: 0.5rem 0;">🐾 Built with ❤️ for Cats and Their Humans</p>
        <p style="margin: 0.5rem 0;">Hackathon 2026 | Powered by Gemini AI & MariaDB</p>
    </div>
    """, unsafe_allow_html=True)

else:
    # Show message to navigate to pages
    st.markdown('<h1 class="hero-title">🐾 Pawlytics</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">Select a page from the sidebar to begin</p>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; margin-top: 3rem;">
        <p style="font-size: 1.2rem; color: #666;">
            👈 Use the <strong>sidebar navigation</strong> to access:
        </p>
        <ul style="list-style: none; padding: 0; font-size: 1.1rem; color: #555; margin-top: 2rem;">
            <li style="margin: 1rem 0;">📊 <strong>Dashboard</strong> - View overview and stats</li>
            <li style="margin: 1rem 0;">🐱 <strong>Cat Profiles</strong> - Manage your cats</li>
            <li style="margin: 1rem 0;">📸 <strong>AI Scanner</strong> - Scan labels & photos</li>
            <li style="margin: 1rem 0;">📈 <strong>Analytics</strong> - Insights & comparisons</li>
            
        </ul>
    </div>
    """, unsafe_allow_html=True)