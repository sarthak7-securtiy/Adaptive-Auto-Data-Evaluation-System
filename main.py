import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
import warnings
import requests
from streamlit_lottie import st_lottie

warnings.filterwarnings('ignore')

st.set_page_config(page_title="AADES | Analytics Platform", layout="wide", page_icon="✨")

# -----------------
# Ultra-Premium CSS (Vercel/SaaS Inspired)
# -----------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');

    /* Global Typography */
    html, body, [class*="st-"] {
        font-family: 'Outfit', sans-serif !important;
    }
    
    /* Pitch Black Background */
    .stApp {
        background-color: #000000;
    }

    /* Glassmorphism/Dark Cards for Metrics and Elements */
    div[data-testid="metric-container"] {
        background: #111111;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        border-color: rgba(0, 240, 255, 0.5);
        box-shadow: 0 10px 30px rgba(0, 240, 255, 0.15);
    }
    
    /* Hero Title styling */
    h1 {
        text-align: center;
        background: -webkit-linear-gradient(45deg, #00F0FF, #8A2BE2, #0055FF);
        background-size: 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: textGradient 5s ease infinite;
        margin-bottom: 0.2em;
        font-weight: 800;
        letter-spacing: -1px;
        font-size: 3.5rem !important;
    }
    @keyframes textGradient {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }
    
    .subtitle {
        text-align: center;
        color: #888888;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        font-weight: 300;
    }
    
    /* Hide default elements */
    #MainMenu {visibility: hidden;}
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    
    /* Sidebar polish */
    [data-testid="stSidebar"] {
        background: #0a0a0a;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Pill Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: #111111;
        padding: 8px;
        border-radius: 50px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        display: flex;
        justify-content: center;
    }
    .stTabs [data-baseweb="tab"] {
        height: 40px;
        background-color: transparent;
        border-radius: 50px !important;
        color: #888888;
        font-weight: 600;
        padding: 0 25px;
        transition: all 0.3s ease;
    }
    .stTabs [aria-selected="true"] {
        color: #000000 !important;
        background: linear-gradient(90deg, #00F0FF, #0055FF) !important;
        box-shadow: 0 4px 15px rgba(0, 240, 255, 0.4) !important;
    }
    .stTabs [data-baseweb="tab-highlight"] {
        display: none;
    }
    
    /* Dataframe glass look */
    [data-testid="stDataFrame"] {
        background: #111111;
        border-radius: 12px;
        padding: 10px;
        border: 1px solid rgba(255,255,255,0.05);
    }
</style>
""", unsafe_allow_html=True)

def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# -----------------
# Sidebar Content
# -----------------
with st.sidebar:
    st.markdown("## ✨ **AADES**")
    st.markdown("<span style='color:#888;'>Adaptive Data Analysis System</span>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("### 📁 Data Source")
    uploaded_file = st.file_uploader("Upload dataset", type=['csv', 'xlsx', 'xls', 'json'])
    
    st.markdown("---")
    st.markdown("### 💡 Engine Info")
    st.info("Automated descriptive stats, correlation heatmaps, and ML predictive modeling at your fingertips.")

# -----------------
# Main Content
# -----------------
st.markdown("<h1>AADES Platform</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>The Next Generation of Automated Data Evaluation</div>", unsafe_allow_html=True)

if uploaded_file is None:
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        # A sleek floating data animation
        lottie_data = load_lottieurl("https://lottie.host/79016e78-ebdb-4c8d-ae21-a1d2e1b1d1f0/qM8QoJ6t1Y.json")
        if lottie_data:
            st_lottie(lottie_data, height=300, key="data_animation")
        else:
            st.markdown("<h3 style='text-align: center; color: #555;'>Awaiting Data Source...</h3>", unsafe_allow_html=True)
            
        st.markdown("<p style='text-align: center; color: #888;'>Drop your CSV, JSON, or Excel file in the sidebar to ignite the engine.</p>", unsafe_allow_html=True)
    st.stop()

# Load Data
try:
    filename = uploaded_file.name
    if filename.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    elif filename.endswith(('.xls', '.xlsx')):
        df = pd.read_excel(uploaded_file)
    elif filename.endswith('.json'):
        df = pd.read_json(uploaded_file)
    else:
        st.error("Unsupported file format")
        st.stop()
    st.toast("Dataset successfully processed! 🚀", icon="✅")
except Exception as e:
    st.error(f"Error loading file: {e}")
    st.stop()

# Organize with Tabs
tab_overview, tab_analysis, tab_ml = st.tabs(["📊 Overview", "📈 Advanced Analysis", "🤖 ML Engine"])

# Reusable minimalist plotly layout
def apply_minimal_layout(fig):
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', 
        paper_bgcolor='rgba(0,0,0,0)',
        font_family="Outfit",
        font_color="#A0AEC0",
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', zeroline=False)
    )
    return fig

with tab_overview:
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Total Rows", value=f"{df.shape[0]:,}")
    with col2:
        st.metric(label="Total Features", value=df.shape[1])
    with col3:
        st.metric(label="Missing Values", value=f"{df.isnull().sum().sum():,}")
        
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### Data Preview")
    st.dataframe(df.head(15), use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### Data Types & Missing Information")
    info_df = pd.DataFrame({
        'Data Type': df.dtypes.astype(str),
        'Missing Values': df.isnull().sum(),
        'Missing %': (df.isnull().sum() / len(df) * 100).round(2)
    })
    st.dataframe(info_df, use_container_width=True)

with tab_analysis:
    st.markdown("<br>", unsafe_allow_html=True)
    
    numeric_df = df.select_dtypes(include=[np.number]).dropna()
    
    if numeric_df.empty:
        st.warning("No numeric features available for analysis.")
    else:
        col_desc, col_corr = st.columns([1, 1])
        
        with col_desc:
            st.markdown("#### Feature Distributions")
            feature_to_plot = st.selectbox("Select Feature to Visualize", options=numeric_df.columns)
            fig_dist = px.histogram(numeric_df, x=feature_to_plot, marginal="box", 
                                    color_discrete_sequence=['#00F0FF'], title=f"Distribution of {feature_to_plot}")
            apply_minimal_layout(fig_dist)
            st.plotly_chart(fig_dist, use_container_width=True)
            
        with col_corr:
            st.markdown("#### Correlation Heatmap")
            corr = numeric_df.corr()
            fig_corr = px.imshow(corr, text_auto=".2f", aspect="auto", color_continuous_scale="Blues", title="Feature Correlations")
            fig_corr.update_layout(
                plot_bgcolor='rgba(0,0,0,0)', 
                paper_bgcolor='rgba(0,0,0,0)',
                font_family="Outfit",
                font_color="#A0AEC0"
            )
            st.plotly_chart(fig_corr, use_container_width=True)

with tab_ml:
    st.markdown("<br>", unsafe_allow_html=True)
    
    ml_task = st.radio("Select ML Task", ["Pattern Clustering (K-Means)", "Predictive Modeling (Linear Regression)"], horizontal=True)
    
    if numeric_df.empty:
        st.warning("ML models require numeric features.")
    else:
        if ml_task == "Pattern Clustering (K-Means)":
            st.markdown("#### K-Means Clustering")
            if len(numeric_df) < 2:
                st.warning("Insufficient data.")
            else:
                num_clusters = st.slider("Select Number of Clusters", min_value=2, max_value=10, value=3)
                
                if st.button("Run Clustering Engine"):
                    with st.spinner("Processing clusters..."):
                        scaler = StandardScaler()
                        scaled_data = scaler.fit_transform(numeric_df)
                        kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init='auto').fit(scaled_data)
                        
                        clustered_df = numeric_df.copy()
                        clustered_df['Cluster'] = [f"Cluster {i+1}" for i in kmeans.labels_]
                        
                        st.toast(f"Successfully clustered data into {num_clusters} patterns.", icon="🎉")
                        st.balloons()
                    
                    c1, c2 = st.columns(2)
                    with c1:
                        cluster_counts = clustered_df['Cluster'].value_counts().reset_index()
                        cluster_counts.columns = ['Cluster', 'Count']
                        fig_pie = px.pie(cluster_counts, names='Cluster', values='Count', hole=0.5, 
                                         color_discrete_sequence=px.colors.sequential.Teal, title="Cluster Distribution")
                        fig_pie.update_layout(
                            plot_bgcolor='rgba(0,0,0,0)', 
                            paper_bgcolor='rgba(0,0,0,0)',
                            font_family="Outfit",
                            font_color="#A0AEC0"
                        )
                        st.plotly_chart(fig_pie, use_container_width=True)
                    
                    with c2:
                        if len(numeric_df.columns) >= 2:
                            x_feat = numeric_df.columns[0]
                            y_feat = numeric_df.columns[1]
                            fig_scatter = px.scatter(clustered_df, x=x_feat, y=y_feat, color="Cluster", 
                                                     title=f"{x_feat} vs {y_feat} (Clustered)",
                                                     color_discrete_sequence=px.colors.qualitative.Set3)
                            apply_minimal_layout(fig_scatter)
                            st.plotly_chart(fig_scatter, use_container_width=True)
                        
        elif ml_task == "Predictive Modeling (Linear Regression)":
            st.markdown("#### Linear Regression")
            if len(numeric_df) < 5 or numeric_df.shape[1] < 2:
                st.warning("Need multiple numeric columns and sufficient rows.")
            else:
                target_col = st.selectbox("Select Target Variable to Predict", options=numeric_df.columns, index=len(numeric_df.columns)-1)
                feature_cols = [c for c in numeric_df.columns if c != target_col]
                
                if st.button("Train Predictive Model"):
                    with st.spinner("Training model..."):
                        X = numeric_df[feature_cols].values
                        y = numeric_df[target_col].values
                        
                        model = LinearRegression().fit(X, y)
                        score = model.score(X, y)
                        
                        st.toast(f"Model trained! R² Score: {score:.2f}", icon="🤖")
                    
                    st.success(f"Model trained! R² Score: **{score:.2f}**")
                    
                    preds = model.predict(X)
                    
                    compare_df = pd.DataFrame({
                        "Actual": y[:50],
                        "Predicted": preds[:50]
                    })
                    
                    fig_line = go.Figure()
                    fig_line.add_trace(go.Scatter(y=compare_df['Actual'], mode='lines', name='Actual', line=dict(color='#8A2BE2', width=3)))
                    fig_line.add_trace(go.Scatter(y=compare_df['Predicted'], mode='lines', name='Predicted', line=dict(color='#00F0FF', dash='dash', width=3)))
                    fig_line.update_layout(title="Actual vs Predicted (First 50 Samples)", 
                                           xaxis_title="Sample Index", yaxis_title="Value")
                    apply_minimal_layout(fig_line)
                    st.plotly_chart(fig_line, use_container_width=True)
