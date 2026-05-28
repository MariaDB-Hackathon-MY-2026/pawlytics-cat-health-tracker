"""
AI Scanner - Core Feature
3 Tabs: Label Scanner | Cat Photo Analyzer | AI Chat
"""

import streamlit as st
import sys
from pathlib import Path
from datetime import datetime
import json

# Add paths
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from backend.database import Database
from backend.gemini_service import GeminiAnalyzer
from utils.session import init_session, get_session_id, add_scan_result
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
    page_title="AI Scanner - Pawlytics",
    page_icon="📸",
    layout="wide"
)

# Initialize
init_session()
db = Database()
gemini = GeminiAnalyzer()

# ==========================================
# CLEAN CSS - WHITE BACKGROUNDS, DARK TEXT
# ==========================================

st.markdown("""
<style>
    /* Main container */
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
    
    /* ========== UPLOAD ZONE - WHITE BACKGROUND ========== */
    .upload-zone {
        border: 2px dashed #cbd5e1 !important;
        border-radius: 16px !important;
        padding: 2rem !important;
        text-align: center !important;
        background: white !important;
        transition: all 0.2s ease !important;
        margin-bottom: 1rem !important;
    }
    
    .upload-zone:hover {
        background: #f8fafc !important;
        border-color: #94a3b8 !important;
    }
    
    .upload-icon {
        font-size: 3rem !important;
        margin-bottom: 1rem !important;
    }
    
    .upload-zone h3 {
        color: #0f172a !important;
        font-weight: 700 !important;
        margin: 0.5rem 0 !important;
    }
    
    .upload-zone p {
        color: #475569 !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
    }
    
    /* ========== FILE UPLOADER BUTTON ========== */
    .stFileUploader {
        margin-bottom: 1rem !important;
    }
    
    .stFileUploader > div:first-child {
        background: white !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
        padding: 0.5rem !important;
    }
    
    /* Browse files button */
    .stFileUploader button {
        background: #4f46e5 !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.4rem 1.2rem !important;
        font-weight: 600 !important;
    }
    
    .stFileUploader button:hover {
        background: #6366f1 !important;
    }
    
    /* File uploader text */
    .stFileUploader div[data-testid="stMarkdownContainer"] p {
        color: #1e293b !important;
        font-weight: 500 !important;
    }
    
    /* Result card */
    .result-card {
        background: #f8fafc !important;
        border-radius: 16px !important;
        padding: 1.5rem !important;
        margin: 1rem 0 !important;
        border: 1px solid #e2e8f0 !important;
    }
    
    /* Grade badges */
    .grade-badge {
        display: inline-block !important;
        padding: 0.5rem 1.5rem !important;
        border-radius: 30px !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
        margin: 1rem 0 !important;
        text-align: center !important;
        width: 100% !important;
    }
    
    .grade-A { background: #22c55e !important; color: white !important; }
    .grade-B { background: #eab308 !important; color: white !important; }
    .grade-C { background: #f97316 !important; color: white !important; }
    .grade-D { background: #ef4444 !important; color: white !important; }
    .grade-F { background: #991b1b !important; color: white !important; }
    
    .grade-badge * { color: white !important; }
    
    /* Chat messages */
    .chat-message {
        padding: 1rem !important;
        border-radius: 12px !important;
        margin: 0.5rem 0 !important;
        max-width: 85% !important;
    }
    
    .chat-message.user {
        background: #4f46e5 !important;
        margin-left: auto !important;
    }
    
    .chat-message.user * {
        color: white !important;
    }
    
    .chat-message.assistant {
        background: #f1f5f9 !important;
        border: 1px solid #e2e8f0 !important;
    }
    
    .chat-message.assistant * {
        color: #1e293b !important;
    }
    
    /* Nutrition grid */
    .nutrition-grid {
        display: grid !important;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)) !important;
        gap: 1rem !important;
        margin: 1rem 0 !important;
    }
    
    .nutrition-item {
        background: white !important;
        padding: 1rem !important;
        border-radius: 12px !important;
        text-align: center !important;
        border: 1px solid #e2e8f0 !important;
    }
    
    .nutrition-value {
        font-size: 1.8rem !important;
        font-weight: 800 !important;
        color: #4f46e5 !important;
    }
    
    .nutrition-label {
        font-size: 0.8rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        margin-top: 0.5rem !important;
        color: #64748b !important;
    }
    
    /* Tabs */
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
    
    /* Buttons */
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
    }
    
    /* Number inputs */
    .stNumberInput input {
        background: white !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 10px !important;
        color: #1e293b !important;
    }
    
    .stNumberInput button {
        background: #f1f5f9 !important;
        border: 1px solid #cbd5e1 !important;
        color: #1e293b !important;
    }
    
    /* Text inputs */
    .stTextInput input {
        background: white !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 10px !important;
        color: #1e293b !important;
    }
    
    .stTextInput input:focus {
        border-color: #4f46e5 !important;
        box-shadow: 0 0 0 2px rgba(79, 70, 229, 0.1) !important;
    }
    
    /* Text area */
    .stTextArea textarea {
        background: white !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 12px !important;
        color: #1e293b !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #4f46e5 !important;
        box-shadow: 0 0 0 2px rgba(79, 70, 229, 0.1) !important;
    }
    
    /* Selectbox */
    .stSelectbox > div > div {
        background: white !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 10px !important;
    }
    
    /* Info/Warning/Success boxes */
    .stAlert {
        border-radius: 10px !important;
    }
    
    .stInfo {
        background: #e0f2fe !important;
        border-left: 4px solid #0284c7 !important;
    }
    
    .stInfo * {
        color: #0c4a6e !important;
    }
    
    .stSuccess {
        background: #dcfce7 !important;
        border-left: 4px solid #16a34a !important;
    }
    
    .stSuccess * {
        color: #14532d !important;
    }
    
    .stWarning {
        background: #fef9c3 !important;
        border-left: 4px solid #eab308 !important;
    }
    
    .stWarning * {
        color: #713f12 !important;
    }
    
    .stError {
        background: #fee2e2 !important;
        border-left: 4px solid #dc2626 !important;
    }
    
    .stError * {
        color: #7f1d1d !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: #f8fafc !important;
        border-radius: 10px !important;
        border: 1px solid #e2e8f0 !important;
    }
    
    /* Divider */
    .custom-divider {
        margin: 1.5rem 0 !important;
        border: none !important;
        height: 1px !important;
        background: #e2e8f0 !important;
    }
    
    /* Metric */
    [data-testid="stMetricValue"] {
        color: #0f172a !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #475569 !important;
    }
    
    /* Footer - Centered */
    .footer-center {
        text-align: center !important;
        color: #64748b !important;
        font-size: 0.8rem !important;
        margin-top: 1rem !important;
    }
            
    /* NUCLEAR FIX - Override ALL button styles in file uploader */
    section[data-testid="stFileUploadDropzone"] button,
    div[data-testid="stFileUploader"] button,
    .uploadedFile button,
    button[kind="secondary"] {
        background: #4f46e5 !important;
        background-color: #4f46e5 !important;
        background-image: linear-gradient(135deg, #4f46e5, #6366f1) !important;
        color: white !important;
        border: 2px solid #4f46e5 !important;
    }
    
    section[data-testid="stFileUploadDropzone"] button:hover,
    div[data-testid="stFileUploader"] button:hover {
        background: #6366f1 !important;
        background-color: #6366f1 !important;
        background-image: linear-gradient(135deg, #6366f1, #818cf8) !important;
    }
    
    /* Text inside button */
    section[data-testid="stFileUploadDropzone"] button p,
    div[data-testid="stFileUploader"] button p,
    section[data-testid="stFileUploadDropzone"] button span,
    div[data-testid="stFileUploader"] button span {
        color: white !important;
        font-weight: 700 !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# HEADER
# ==========================================

st.markdown(f'<h1 style="font-size: 2rem; font-weight: 800; margin-bottom: 0;">📸 {user_name}\'s Scanner</h1>', unsafe_allow_html=True)
st.markdown('<p style="color: #64748b; margin-bottom: 1rem;">Upload images for AI-powered nutrition analysis</p>', unsafe_allow_html=True)

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# ==========================================
# TABS
# ==========================================

tab1, tab2, tab3 = st.tabs(["📋 Scan Label", "🐱 Analyze Cat Photo", "💬 Chat with AI"])

# ==========================================
# TAB 1: SCAN NUTRITION LABEL
# ==========================================

with tab1:
    st.markdown("### 📋 Nutrition Label Scanner")
    st.markdown("Upload a clear photo of the kibble nutrition label")
    
        
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Custom upload zone
        st.markdown("""
        <div class="upload-zone">
            <div class="upload-icon">📸</div>
            <h3>Drag and drop file here</h3>
            <p>Limit 200MB per file • JPG, JPEG, PNG, WEBP</p>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Choose an image",
            type=['jpg', 'jpeg', 'png', 'webp'],
            help="Best results: Clear, well-lit photos of the nutrition table",
            key="label_upload",
            label_visibility="collapsed"
        )
        
        if uploaded_file:
            st.image(uploaded_file, caption="Uploaded Label", use_column_width=True)
            
            col_a, col_b = st.columns(2)
            
            with col_a:
                if st.button("🔍 Analyze with AI", type="primary", use_container_width=True, key="analyze_label"):
                    with st.spinner("🤖 AI is analyzing the label..."):
                        temp_dir = Path("temp_uploads")
                        temp_dir.mkdir(exist_ok=True)
                        temp_path = temp_dir / uploaded_file.name
                        
                        with open(temp_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        
                        result = gemini.analyze_kibble_label(str(temp_path))
                        temp_path.unlink()
                        
                        if result:
                            st.session_state['label_scan_result'] = result
                            add_scan_result({
                                'type': 'label',
                                'timestamp': datetime.now().isoformat(),
                                'data': result
                            })
                            st.success("✅ Analysis complete!")
                            st.balloons()
                        else:
                            st.error("❌ Analysis failed. Please try a clearer image.")
            
            with col_b:
                if st.button("🔄 Clear", use_container_width=True, key="clear_label"):
                    if 'label_scan_result' in st.session_state:
                        del st.session_state['label_scan_result']
                    st.rerun()
        
        with st.expander("💡 Tips for Best Results"):
            st.markdown("""
            **For accurate scanning:**
            - ✅ Use clear, well-lit photos
            - ✅ Focus on the nutrition table
            - ✅ Avoid blurry or dark images
            - ✅ Include the entire nutrition panel
            
            **Supported formats:** JPG, PNG, WEBP
            """)
    
    with col2:
        if 'label_scan_result' in st.session_state:
            data = st.session_state['label_scan_result']
            
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.markdown("### 📋 Extracted Nutrition Data")
            st.info("Review and edit the data before saving")
            
            with st.form("kibble_save_form"):
                brand = st.text_input("Brand Name*", value=data.get('brand_name', ''))
                
                col_p, col_f, col_fb = st.columns(3)
                
                with col_p:
                    protein = st.number_input(
                        "Protein (%)*", 
                        value=float(data.get('protein_pct', 0)), 
                        min_value=0.0, 
                        max_value=100.0,
                        step=0.1
                    )
                
                with col_f:
                    fat = st.number_input(
                        "Fat (%)*", 
                        value=float(data.get('fat_pct', 0)), 
                        min_value=0.0, 
                        max_value=100.0,
                        step=0.1
                    )
                
                with col_fb:
                    fiber = st.number_input(
                        "Fiber (%)*", 
                        value=float(data.get('fiber_pct', 0)), 
                        min_value=0.0, 
                        max_value=100.0,
                        step=0.1
                    )
                
                col_m, col_a, col_pr = st.columns(3)
                
                with col_m:
                    moisture = st.number_input(
                        "Moisture (%)*", 
                        value=float(data.get('moisture_pct', 0)), 
                        min_value=0.0, 
                        max_value=100.0,
                        step=0.1
                    )
                
                with col_a:
                    ash = st.number_input(
                        "Ash (%)", 
                        value=float(data.get('ash_pct', 0)), 
                        min_value=0.0, 
                        max_value=100.0,
                        step=0.1
                    )
                
                with col_pr:
                    price = st.number_input(
                        "Price/kg (RM)", 
                        value=float(data.get('price_per_kg', 0)), 
                        min_value=0.0,
                        step=0.50
                    )
                
                nfe = 100 - (protein + fat + fiber + moisture + ash)
                
                st.markdown(f"""
                <div class="nutrition-item">
                    <div class="nutrition-value">{nfe:.1f}%</div>
                    <div class="nutrition-label">NFE (Carbs)</div>
                </div>
                """, unsafe_allow_html=True)
                
                rating = db.calculate_rating(protein, fat, fiber, moisture)
                
                st.markdown(f'<div class="grade-badge grade-{rating}">Grade: {rating}</div>', unsafe_allow_html=True)
                
                if rating == 'A':
                    st.success("🟢 Excellent nutrition! High protein, balanced macros.")
                elif rating == 'B':
                    st.info("🟡 Good quality food with decent nutrition.")
                elif rating == 'C':
                    st.warning("🟠 Average quality. Consider upgrading.")
                else:
                    st.error("🔴 Below recommended standards.")
                
                submitted = st.form_submit_button("💾 Save to Database", type="primary", use_container_width=True)
                
                if submitted:
                    if not brand:
                        st.error("❌ Brand name is required!")
                    else:
                        # Save with user tracking
                        kibble_id = db.add_kibble(
                            brand_name=brand,
                            product_name=brand,  # Use brand as product name
                            protein_pct=protein,
                            fat_pct=fat,
                            fiber_pct=fiber,
                            moisture_pct=moisture,
                            ash_pct=ash,
                            rating=rating,
                            price_per_kg=price if price > 0 else None,
                            user_id=user_id,  # ← ADD THIS
                            user_name=user_name  # ← ADD THIS
                        )

                        # Also add to scan history
                        if kibble_id:
                            db.add_scan(
                                user_id=user_id,
                                user_name=user_name,
                                kibble_data={
                                    'brand_name': brand,
                                    'product_name': brand,
                                    'protein_pct': protein,
                                    'fat_pct': fat,
                                    'fiber_pct': fiber,
                                    'rating': rating
                                }
                            )
                        
                        if kibble_id:
                            if is_guest:
                                st.success("✅ Analysis complete! Data saved to database.")
                                st.info("Please login with your name to save scans to your personal profile!")
                            else:
                                st.success(f"✅ Saved successfully!")
                            
                            db.execute_update("""
                                INSERT INTO scan_history (session_id, kibble_id, scan_type, result_data)
                                VALUES (%s, %s, 'label', %s)
                            """, (get_session_id(), kibble_id, json.dumps(data)))
                            
                            del st.session_state['label_scan_result']
                            st.rerun()
                        else:
                            st.error("❌ Failed to save.")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
       

# ==========================================
# TAB 2: ANALYZE CAT PHOTO
# ==========================================

with tab2:
    st.markdown("### 🐱 Cat Photo Analyzer")
    st.markdown("Upload a photo of your cat for body condition analysis")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Custom upload zone
        st.markdown("""
        <div class="upload-zone">
            <div class="upload-icon">🐱</div>
            <h3>Drag and drop file here</h3>
            <p>Limit 200MB per file • JPG, JPEG, PNG</p>
        </div>
        """, unsafe_allow_html=True)
        
        cat_photo = st.file_uploader(
            "Choose an image",
            type=['jpg', 'jpeg', 'png'],
            help="Clear side-view photos work best",
            key="cat_upload",
            label_visibility="collapsed"
        )
        
        if cat_photo:
            st.image(cat_photo, caption="Your Cat", use_column_width=True)
            
            if is_guest:
                cats = db.get_all_cats()
                st.info("**Guest Mode** - Viewing all cats. Login to see only yours!")
            else:
                cats = db.get_cats_by_user(user_id)
            if cats:
                cat_names = {cat['name']: cat['id'] for cat in cats}
                selected_cat = st.selectbox(
                    "Which cat is this? (Optional)",
                    options=["None - Just analyze"] + list(cat_names.keys()),
                    key="cat_select"
                )
            
            if st.button("🔍 Analyze Body Condition", type="primary", use_container_width=True, key="analyze_cat"):
                with st.spinner("🤖 AI is analyzing your cat..."):
                    temp_dir = Path("temp_uploads")
                    temp_dir.mkdir(exist_ok=True)
                    temp_path = temp_dir / cat_photo.name
                    
                    with open(temp_path, "wb") as f:
                        f.write(cat_photo.getbuffer())
                    
                    prompt = """
                    Analyze this cat photo and provide:
                    1. Body Condition Score (1-9, where 5 is ideal)
                    2. Weight assessment (Underweight/Ideal/Overweight/Obese)
                    3. Visible health indicators
                    4. Recommended food type (High protein/Low carb/Weight management)
                    5. Feeding suggestions
                    
                    Respond in JSON format:
                    {
                        "bcs": 5,
                        "weight_assessment": "Ideal",
                        "health_notes": "...",
                        "recommended_food": "...",
                        "feeding_suggestions": "..."
                    }
                    """
                    
                    result = gemini.analyze_image_with_prompt(str(temp_path), prompt)
                    temp_path.unlink()
                    
                    if result:
                        st.session_state['cat_analysis'] = result
                        st.success("✅ Analysis complete!")
                    else:
                        st.error("❌ Analysis failed. Please try again.")
    
    with col2:
        if 'cat_analysis' in st.session_state:
            analysis = st.session_state['cat_analysis']
            
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.markdown("### 📊 Analysis Results")
            
            bcs = analysis.get('bcs', 5)
            st.metric("Body Condition Score", f"{bcs}/9")
            
            weight_status = analysis.get('weight_assessment', 'Unknown')
            if weight_status == 'Ideal':
                st.success(f"✅ Weight Status: **{weight_status}**")
            elif weight_status in ['Overweight', 'Obese']:
                st.warning(f"⚠️ Weight Status: **{weight_status}**")
            else:
                st.info(f"ℹ️ Weight Status: **{weight_status}**")
            
            st.markdown("**Health Indicators:**")
            st.write(analysis.get('health_notes', 'No specific concerns detected'))
            
            st.markdown("**Recommended Food Type:**")
            st.info(analysis.get('recommended_food', 'Balanced nutrition'))
            
            st.markdown("**Feeding Suggestions:**")
            st.write(analysis.get('feeding_suggestions', 'Follow standard feeding guidelines'))
            
            st.markdown("---")
            st.markdown("**🎯 Matching Brands from Database:**")
            
            if weight_status in ['Overweight', 'Obese']:
                suitable = db.execute_query("""
                    SELECT brand_name, protein_pct, nfe_pct, rating, price_per_kg
                    FROM v_kibble_analytics
                    WHERE protein_pct >= 35 AND nfe_pct <= 25
                    ORDER BY rating DESC, price_per_kg ASC
                    LIMIT 5
                """)
            else:
                suitable = db.execute_query("""
                    SELECT brand_name, protein_pct, rating, price_per_kg
                    FROM v_kibble_analytics
                    WHERE rating IN ('A', 'B')
                    ORDER BY rating DESC
                    LIMIT 5
                """)
            
            if suitable:
                for brand in suitable:
                    emoji = get_grade_emoji(brand['rating'])
                    st.markdown(f"- {emoji} **{brand['brand_name']}** - Grade {brand['rating']} ({brand['protein_pct']}% protein)")
            
            st.markdown('</div>', unsafe_allow_html=True)
        

# ==========================================
# TAB 3: CHAT WITH AI
# ==========================================

with tab3:
    st.markdown("### 💬 Chat with AI Nutritionist")
    st.markdown("Ask anything about cat nutrition, food brands, or health concerns")
    
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = []
    
    for message in st.session_state.chat_messages:
        role = message['role']
        content = message['content']
        
        if role == 'user':
            st.markdown(f"""
            <div class="chat-message user">
                <strong>You:</strong><br>{content}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message assistant">
                <strong>AI Assistant:</strong><br>{content}
            </div>
            """, unsafe_allow_html=True)
    
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_area(
            "Your question:",
            placeholder="e.g., Is Whiskas good for kittens? What food is best for diabetic cats?",
            height=100,
            key="chat_input"
        )
        
        # Centered buttons
        col_left, col_send, col_clear, col_right = st.columns([1.5, 1, 1, 1.5])
        
        with col_send:
            submitted = st.form_submit_button("Send", use_container_width=True, type="primary")
        
        with col_clear:
            clear_clicked = st.form_submit_button("Clear", use_container_width=True)
    
    # Handle clear button
    if clear_clicked:
        st.session_state.chat_messages = []
        st.rerun()
    
    # Handle send button
    if submitted and user_input:
        st.session_state.chat_messages.append({'role': 'user', 'content': user_input})
        
        context = f"""
        You are an expert cat nutritionist. Answer based on AAFCO standards.
        
        Available brands: {len(db.get_all_kibbles())}
        Registered cats: {len(db.get_all_cats())}
        
        User question: {user_input}
        """
        
        with st.spinner("AI is thinking..."):
            try:
                response = gemini.chat(context)
                st.session_state.chat_messages.append({'role': 'assistant', 'content': response})
                db.execute_update("""
                    INSERT INTO chat_history (user_session, message, response)
                    VALUES (%s, %s, %s)
                """, (get_session_id(), user_input, response))
            except Exception as e:
                st.session_state.chat_messages.append({'role': 'assistant', 'content': "Error. Please try again."})
        
        st.rerun()
    
    st.markdown("### Quick Questions")
    st.markdown("""
    <style>
    /* Force white text on quick question buttons */
    div[data-testid="column"] button[kind="secondary"],
    div[data-testid="column"] button p,
    div[data-testid="column"] button span {
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    quick_questions = [
        "Best food for kittens?",
        "Low-carb food options?",
        "Is grain-free better?",
        "Overweight cat diet?",
        "Best protein sources?",
        "Whiskas vs Royal Canin?"
    ]
    
    cols = st.columns(3)
    for i, q in enumerate(quick_questions):
        with cols[i % 3]:
            if st.button(q, use_container_width=True, key=f"quick_{i}"):
                # Add user message
                st.session_state.chat_messages.append({'role': 'user', 'content': q})
                
                # Get AI response
                context = f"You are an expert cat nutritionist. Answer based on AAFCO standards and scientific evidence. Question: {q}"
                
                try:
                    with st.spinner("🤖 AI is thinking..."):
                        response = gemini.chat(context)
                        st.session_state.chat_messages.append({'role': 'assistant', 'content': response})
                        
                        # Save to database
                        db.execute_update("""
                            INSERT INTO chat_history (user_session, message, response)
                            VALUES (%s, %s, %s)
                        """, (get_session_id(), q, response))
                except Exception as e:
                    st.session_state.chat_messages.append({
                        'role': 'assistant', 
                        'content': "Sorry, I encountered an error. Please try again."
                    })
                
                st.rerun()

# ==========================================
# FOOTER - CENTERED
# ==========================================

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="footer-center">🐾 Pawlytics - AI-Powered Cat Nutrition Intelligence</div>', unsafe_allow_html=True)


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