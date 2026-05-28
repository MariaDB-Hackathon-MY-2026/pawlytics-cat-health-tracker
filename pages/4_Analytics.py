"""
Analytics & Insights Page
Advanced data visualization and comparisons
"""

import streamlit as st
import sys
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Add paths
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from backend.database import Database
from utils.session import init_session
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
    page_title="Analytics - Pawlytics",
    page_icon="📈",
    layout="wide"
)

# Initialize
init_session()
db = Database()

# ==========================================
# CLEAN CSS - WHITE BACKGROUND, DARK TEXT
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
    
    /* Metric cards */
    .metric-card {
        background: white !important;
        border-radius: 16px !important;
        padding: 1.5rem !important;
        text-align: center !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08) !important;
        border: 1px solid #e2e8f0 !important;
        transition: all 0.2s ease !important;
    }
    
    .metric-card:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 4px 16px rgba(0,0,0,0.12) !important;
        border-color: #cbd5e1 !important;
    }
    
    .metric-value {
        font-size: 2.2rem !important;
        font-weight: 800 !important;
        color: #4f46e5 !important;
        margin: 0 !important;
    }
    
    .metric-label {
        font-size: 0.85rem !important;
        color: #64748b !important;
        margin-top: 0.5rem !important;
        font-weight: 500 !important;
    }
    
    /* Chart title */
    .chart-title {
        font-size: 1.3rem !important;
        font-weight: 700 !important;
        color: #0f172a !important;
        margin: 1rem 0 1rem 0 !important;
        padding-bottom: 0.5rem !important;
        border-bottom: 2px solid #e2e8f0 !important;
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
    
    /* Selectbox */
    .stSelectbox > div > div {
        background: white !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 10px !important;
    }
    
    /* Radio buttons */
    .stRadio > div {
        gap: 1rem !important;
    }
    
    .stRadio label {
        background: #f8fafc !important;
        padding: 0.3rem 1rem !important;
        border-radius: 20px !important;
        border: 1px solid #e2e8f0 !important;
    }
    
    .stRadio label[data-baseweb="radio"]:checked {
        background: #4f46e5 !important;
        color: white !important;
    }
    
    /* Dataframe */
    .dataframe {
        border-radius: 12px !important;
        overflow: hidden !important;
    }
    
    .dataframe th {
        background: #f8fafc !important;
        color: #0f172a !important;
        font-weight: 700 !important;
        padding: 0.75rem !important;
    }
    
    .dataframe td {
        padding: 0.5rem !important;
        color: #1e293b !important;
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
    
    /* Medal cards */
    .medal-card {
        padding: 1.5rem !important;
        border-radius: 16px !important;
        text-align: center !important;
        background: white !important;
        border: 1px solid #e2e8f0 !important;
    }
    
    .medal-emoji {
        font-size: 3rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    .medal-brand {
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        color: #0f172a !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# HEADER
# ==========================================

st.markdown('<h1 style="font-size: 2rem; font-weight: 800; margin-bottom: 0;">📈 Insights & Analytics</h1>', unsafe_allow_html=True)
st.markdown('<p style="color: #64748b; margin-bottom: 1rem;">Deep dive into nutrition data and brand comparisons</p>', unsafe_allow_html=True)

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# ==========================================
# FETCH DATA
# ==========================================

try:
    analytics = db.get_analytics()
    
    if not analytics:
        st.info("📭 No data available. Start by scanning some kibble labels!")
        st.stop()
    
    df = pd.DataFrame(analytics)
    
    # Data cleaning
    numeric_cols = ['protein_pct', 'fat_pct', 'fiber_pct', 'nfe_pct', 
                   'protein_dmb', 'price_per_kg', 'protein_value_ratio']
    
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    df = df.dropna(subset=['protein_pct', 'price_per_kg'])
    
    # ==========================================
    # TOP METRICS
    # ==========================================
    
      
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">📦 {len(df)}</div>
            <div class="metric-label">Total Brands</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        avg_protein = df['protein_pct'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">🥩 {avg_protein:.1f}%</div>
            <div class="metric-label">Avg Protein</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        avg_price = df['price_per_kg'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">💰 RM {avg_price:.2f}</div>
            <div class="metric-label">Avg Price/kg</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        a_grade = len(df[df['rating'] == 'A'])
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">🏆 {a_grade}</div>
            <div class="metric-label">A-Grade Brands</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    # ==========================================
    # TABS
    # ==========================================
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Cost vs Nutrient", 
        "🏆 Brand Rankings", 
        "📉 Carbs (NFE) Analysis",
        "📋 Data Export"
    ])
    
    # ==========================================
    # TAB 1: SCATTER PLOT - FIXED TEXT
    # ==========================================
    
    with tab1:
        st.markdown('<p class="chart-title">💰 Find the Sweet Spot: High Protein, Low Price</p>', unsafe_allow_html=True)
        
        df_scatter = df[df['protein_value_ratio'].notna() & (df['protein_value_ratio'] > 0)].copy()
        
        if len(df_scatter) > 0:
            color_map = {
                'A': '#22c55e',
                'B': '#eab308',
                'C': '#f97316',
                'D': '#ef4444',
                'F': '#991b1b'
            }
            
            fig = px.scatter(
                df_scatter,
                x='price_per_kg',
                y='protein_pct',
                size='protein_value_ratio',
                color='rating',
                hover_data=['brand_name', 'fat_pct', 'nfe_pct'],
                title='Protein Content vs Price Analysis',
                labels={
                    'price_per_kg': 'Price per KG (RM)',
                    'protein_pct': 'Protein Content (%)',
                    'rating': 'Grade'
                },
                color_discrete_map=color_map
            )
            
            # FIXED LAYOUT - DARK TEXT
            fig.update_layout(
                height=500,
                hovermode='closest',
                plot_bgcolor='white',
                paper_bgcolor='white',
                title_font=dict(size=16, color='#0f172a', family='Arial, sans-serif'),
                font=dict(color='#0f172a', size=12, family='Arial, sans-serif'),
                xaxis=dict(
                    title_font=dict(size=14, color='#0f172a'),
                    tickfont=dict(size=12, color='#0f172a'),
                    gridcolor='#e2e8f0',
                    showgrid=True
                ),
                yaxis=dict(
                    title_font=dict(size=14, color='#0f172a'),
                    tickfont=dict(size=12, color='#0f172a'),
                    gridcolor='#e2e8f0',
                    showgrid=True
                ),
                legend=dict(
                    font=dict(size=12, color='#0f172a'),
                    bgcolor='rgba(255,255,255,0.9)',
                    bordercolor='#cbd5e1',
                    borderwidth=1
                )
            )
            
            # FIXED HOVER - DARK TEXT
            fig.update_traces(
                marker=dict(line=dict(width=1, color='white')),
                hoverlabel=dict(
                    bgcolor='white',
                    font_size=13,
                    font_color='#0f172a',
                    bordercolor='#cbd5e1'
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.info("💡 **Tip:** Best value brands are in the **top-left corner** (high protein, low price)")
            
            best_value = df_scatter.nlargest(3, 'protein_value_ratio')
            
            st.markdown("### 🎯 Top 3 Best Value Brands")
            
            for i, row in best_value.iterrows():
                emoji = get_grade_emoji(row['rating'])
                st.success(f"""
                **{emoji} {row['brand_name']}**
                - Protein: {row['protein_pct']}%
                - Price: RM {row['price_per_kg']:.2f}/kg
                - Value Score: {row['protein_value_ratio']:.2f}
                - Grade: {row['rating']}
                """)
        else:
            st.info("Not enough data for scatter plot")
    
    # ==========================================
    # TAB 2: RANKINGS
    # ==========================================
    
    with tab2:
        st.markdown('<p class="chart-title">🏆 Brand Rankings</p>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            sort_by = st.selectbox(
                "Sort by:",
                options=['Value Score', 'Protein %', 'Price', 'Grade'],
                index=0
            )
        
        with col2:
            order = st.radio("Order:", ["Descending", "Ascending"], horizontal=True)
        
        ranking_df = df[['brand_name', 'protein_pct', 'price_per_kg', 'rating', 'protein_value_ratio']].copy()
        
        sort_col_map = {
            'Value Score': 'protein_value_ratio',
            'Protein %': 'protein_pct',
            'Price': 'price_per_kg',
            'Grade': 'rating'
        }
        
        sort_col = sort_col_map[sort_by]
        ascending = (order == "Ascending")
        
        ranking_df = ranking_df.sort_values(sort_col, ascending=ascending).reset_index(drop=True)
        ranking_df.insert(0, 'Rank', range(1, len(ranking_df) + 1))
        
        ranking_df.columns = ['Rank', 'Brand', 'Protein %', 'Price/kg (RM)', 'Grade', 'Value Score']
        
        st.dataframe(
            ranking_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Rank": st.column_config.NumberColumn("🏅", width="small"),
                "Grade": st.column_config.TextColumn("Grade", width="small"),
                "Value Score": st.column_config.NumberColumn(
                    "Value Score",
                    help="Protein % ÷ Price per KG",
                    format="%.2f"
                )
            }
        )
        
        if len(ranking_df) >= 3:
            st.markdown("### 🏅 Top 3 Rankings")
            
            col1, col2, col3 = st.columns(3)
            
            medals = ['🥇', '🥈', '🥉']
            
            for i, col in enumerate([col1, col2, col3]):
                if i < len(ranking_df):
                    brand = ranking_df.iloc[i]
                    with col:
                        st.markdown(f"""
                        <div class="medal-card">
                            <div class="medal-emoji">{medals[i]}</div>
                            <div class="medal-brand">{brand['Brand']}</div>
                            <p style="margin: 0.5rem 0 0 0;">Grade: <strong>{brand['Grade']}</strong></p>
                            <p style="margin: 0;">{brand['Protein %']:.1f}% Protein</p>
                            <p style="margin: 0;">RM {brand['Price/kg (RM)']:.2f}/kg</p>
                        </div>
                        """, unsafe_allow_html=True)
    
    # ==========================================
    # TAB 3: NFE ANALYSIS - FIXED TEXT
    # ==========================================
    
    with tab3:
        st.markdown('<p class="chart-title">🍞 Carbohydrate (NFE) Analysis</p>', unsafe_allow_html=True)
        
        st.info("💡 **Why NFE matters:** Cats are obligate carnivores and need minimal carbohydrates. High NFE (>30%) can lead to obesity and diabetes.")
        
        df_nfe = df.sort_values('nfe_pct', ascending=True).copy()
        
        fig = px.bar(
            df_nfe,
            x='brand_name',
            y='nfe_pct',
            color='nfe_pct',
            title='Carbohydrate Content by Brand',
            labels={'brand_name': 'Brand', 'nfe_pct': 'NFE (Carbs) %'},
            color_continuous_scale=['#22c55e', '#eab308', '#f97316', '#ef4444']
        )
        
        fig.add_hline(y=25, line_dash="dash", line_color="#22c55e", 
                     annotation_text="Ideal (<25%)", 
                     annotation_font_color="#22c55e",
                     annotation_font_size=12)
        fig.add_hline(y=35, line_dash="dash", line_color="#ef4444",
                     annotation_text="High Risk (>35%)", 
                     annotation_font_color="#ef4444",
                     annotation_font_size=12)
        
        # FIXED LAYOUT - DARK TEXT
        fig.update_layout(
            height=500,
            showlegend=False,
            plot_bgcolor='white',
            paper_bgcolor='white',
            title_font=dict(size=16, color='#0f172a', family='Arial, sans-serif'),
            font=dict(color='#0f172a', size=12, family='Arial, sans-serif'),
            xaxis=dict(
                title_font=dict(size=14, color='#0f172a'),
                tickfont=dict(size=11, color='#0f172a'),
                tickangle=-45,
                gridcolor='#e2e8f0'
            ),
            yaxis=dict(
                title_font=dict(size=14, color='#0f172a'),
                tickfont=dict(size=12, color='#0f172a'),
                gridcolor='#e2e8f0',
                showgrid=True
            )
        )
        
        # FIXED HOVER - DARK TEXT
        fig.update_traces(
            hoverlabel=dict(
                bgcolor='white',
                font_size=13,
                font_color='#0f172a',
                bordercolor='#cbd5e1'
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        low_nfe = df[df['nfe_pct'] < 25]
        medium_nfe = df[(df['nfe_pct'] >= 25) & (df['nfe_pct'] < 35)]
        high_nfe = df[df['nfe_pct'] >= 35]
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.success(f"""
            **🟢 Low NFE (<25%)**
            
            {len(low_nfe)} brands
            
            Best for weight management
            """)
        
        with col2:
            st.warning(f"""
            **🟡 Medium NFE (25-35%)**
            
            {len(medium_nfe)} brands
            
            Acceptable for active cats
            """)
        
        with col3:
            st.error(f"""
            **🔴 High NFE (>35%)**
            
            {len(high_nfe)} brands
            
            Avoid for overweight cats
            """)
        
        if len(high_nfe) > 0:
            with st.expander("⚠️ Brands with High Carbohydrate Content"):
                high_carb_brands = df_nfe[df_nfe['nfe_pct'] >= 35][['brand_name', 'nfe_pct', 'rating']]
                for _, row in high_carb_brands.iterrows():
                    st.write(f"- **{row['brand_name']}**: {row['nfe_pct']:.1f}% carbs (Grade: {row['rating']})")
    
    # ==========================================
    # TAB 4: DATA EXPORT
    # ==========================================
    
    with tab4:
        st.markdown('<p class="chart-title">📋 Export Data</p>', unsafe_allow_html=True)
        
        # Rename columns to be user-friendly (NO EMOJIS)
        df_display = df.copy()

        # Clean professional column names
        column_names = {
            'id': 'ID',
            'brand_name': 'Brand Name',
            'product_line': 'Product Line',
            'protein_pct': 'Protein (%)',
            'fat_pct': 'Fat (%)',
            'fiber_pct': 'Fiber (%)',
            'moisture_pct': 'Moisture (%)',
            'ash_pct': 'Ash (%)',
            'nfe_pct': 'Carbs (%)',
            'protein_dmb': 'Protein (Dry Matter)',
            'price_per_kg': 'Price per KG (RM)',
            'rating': 'Grade',
            'created_at': 'Date Added',
            'protein_value_ratio': 'Value Score',
            'total_feedings': 'Times Fed',
            'cats_fed': 'Cats Fed'
        }

        # Rename columns
        df_display = df_display.rename(columns=column_names)

        # Select and reorder important columns for display
        display_cols = [
            'Brand Name',
            'Grade',
            'Protein (%)',
            'Fat (%)',
            'Carbs (%)',
            'Price per KG (RM)',
            
        ]

        # Filter columns that exist
        display_cols = [col for col in display_cols if col in df_display.columns]

        # Show clean professional table
        st.dataframe(
            df_display[display_cols],
            use_container_width=True,
            hide_index=True,
            column_config={
                'Protein (%)': st.column_config.NumberColumn(
                    'Protein (%)',
                    help="Protein content percentage",
                    format="%.1f%%"
                ),
                'Fat (%)': st.column_config.NumberColumn(
                    'Fat (%)',
                    help="Fat content percentage",
                    format="%.1f%%"
                ),
                'Carbs (%)': st.column_config.NumberColumn(
                    'Carbs (%)',
                    help="Carbohydrate content (NFE)",
                    format="%.1f%%"
                ),
                'Price per KG (RM)': st.column_config.NumberColumn(
                    'Price per KG (RM)',
                    help="Price per kilogram in Ringgit Malaysia",
                    format="RM %.2f"
                ),
                'Value Score': st.column_config.NumberColumn(
                    'Value Score',
                    help="Protein % ÷ Price (higher is better)",
                    format="%.2f"
                ),
                'Times Fed': st.column_config.NumberColumn(
                    'Times Fed',
                    help="Number of times this food was fed"
                ),
                'Cats Fed': st.column_config.NumberColumn(
                    'Cats Fed',
                    help="Number of different cats fed this food"
                )
            }
        )
        
        col1, col2 = st.columns(2)
        
        # Option 1: Excel (Most Useful!)
        with col1:
            # Convert to Excel
            from io import BytesIO
            buffer = BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Nutrition Data', index=False)
            
            st.download_button(
                label="📥 Download Excel",
                data=buffer.getvalue(),
                file_name=f"pawlytics_nutrition_{pd.Timestamp.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
                type="primary"
            )
        
        # Option 2: PDF Report (Professional!)
        with col2:         
            if st.button("Generate PDF Report", use_container_width=True):
                # For now, show message
                # Later: Add actual PDF generation
                st.info("🚧 PDF generation coming soon! For now, use Excel or screenshot.")
        
        with st.expander("📈 Summary Statistics"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**🥩 Protein Analysis:**")
                st.write(f"Min: {df['protein_pct'].min():.1f}%")
                st.write(f"Max: {df['protein_pct'].max():.1f}%")
                st.write(f"Mean: {df['protein_pct'].mean():.1f}%")
                st.write(f"Median: {df['protein_pct'].median():.1f}%")
                
                st.markdown("**🧈 Fat Analysis:**")
                st.write(f"Min: {df['fat_pct'].min():.1f}%")
                st.write(f"Max: {df['fat_pct'].max():.1f}%")
                st.write(f"Mean: {df['fat_pct'].mean():.1f}%")
            
            with col2:
                st.markdown("**💰 Price Analysis:**")
                st.write(f"Min: RM {df['price_per_kg'].min():.2f}")
                st.write(f"Max: RM {df['price_per_kg'].max():.2f}")
                st.write(f"Mean: RM {df['price_per_kg'].mean():.2f}")
                st.write(f"Median: RM {df['price_per_kg'].median():.2f}")
                
                st.markdown("**🏆 Grade Distribution:**")
                grade_counts = df['rating'].value_counts().sort_index()
                for grade, count in grade_counts.items():
                    emoji = get_grade_emoji(grade)
                    st.write(f"{emoji} Grade {grade}: {count} brands")

except Exception as e:
    st.error(f"⚠️ Error loading analytics: {e}")

# ==========================================
# FOOTER
# ==========================================

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
st.markdown('<div style="text-align: center; color: #64748b;">🐾 Pawlytics - Data-Driven Cat Nutrition Insights</div>', unsafe_allow_html=True)


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