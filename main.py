import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
import warnings

warnings.filterwarnings('ignore')

st.set_page_config(page_title="AADES | Analytics Platform", layout="wide", page_icon="⚡")

# Custom CSS for glowing effects and modern typography
st.markdown("""
<style>
    .reportview-container {
        margin-top: -2em;
    }
    #MainMenu {visibility: hidden;}
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    h1 {
        text-align: center;
        background: -webkit-linear-gradient(45deg, #00F0FF, #0055FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5em;
    }
    .st-emotion-cache-16idsys p {
        font-size: 1.1rem;
    }
</style>
""", unsafe_allow_html=True)

# -----------------
# Sidebar Content
# -----------------
with st.sidebar:
    st.markdown("## ⚡ **AADES**")
    st.markdown("Adaptive Data Analysis & Evaluation System")
    st.markdown("---")
    
    st.markdown("### 📁 Data Source")
    uploaded_file = st.file_uploader("Upload dataset", type=['csv', 'xlsx', 'xls', 'json'])
    
    st.markdown("---")
    st.markdown("### 💡 About")
    st.info("Upload your dataset to generate automated statistics, detect correlations, cluster patterns, and run predictive ML models instantly.")
    st.markdown("Designed for robust, scalable data evaluation.")

# -----------------
# Main Content
# -----------------
st.title("AADES Analytics Dashboard")

if uploaded_file is None:
    st.markdown("<h4 style='text-align: center; color: #888;'>Please upload a dataset from the sidebar to begin.</h4>", unsafe_allow_html=True)
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
except Exception as e:
    st.error(f"Error loading file: {e}")
    st.stop()

# Organize with Tabs
tab_overview, tab_analysis, tab_ml = st.tabs(["📊 Data Overview", "📈 Advanced Analysis", "🤖 ML & Prediction"])

with tab_overview:
    st.markdown("### Dataset Summary")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Total Rows", value=f"{df.shape[0]:,}")
    with col2:
        st.metric(label="Total Features", value=df.shape[1])
    with col3:
        st.metric(label="Missing Values", value=f"{df.isnull().sum().sum():,}")
        
    st.markdown("---")
    st.markdown("### Data Preview")
    st.dataframe(df.head(15), use_container_width=True)
    
    st.markdown("### Data Types & Missing Information")
    info_df = pd.DataFrame({
        'Data Type': df.dtypes.astype(str),
        'Missing Values': df.isnull().sum(),
        'Missing %': (df.isnull().sum() / len(df) * 100).round(2)
    })
    st.dataframe(info_df, use_container_width=True)

with tab_analysis:
    st.markdown("### Descriptive & Correlation Analysis")
    
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
            fig_dist.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_dist, use_container_width=True)
            
        with col_corr:
            st.markdown("#### Correlation Heatmap")
            corr = numeric_df.corr()
            fig_corr = px.imshow(corr, text_auto=".2f", aspect="auto", color_continuous_scale="Blues", title="Feature Correlations")
            fig_corr.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_corr, use_container_width=True)

with tab_ml:
    st.markdown("### Machine Learning Capabilities")
    
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
                
                scaler = StandardScaler()
                scaled_data = scaler.fit_transform(numeric_df)
                kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init='auto').fit(scaled_data)
                
                clustered_df = numeric_df.copy()
                clustered_df['Cluster'] = [f"Cluster {i+1}" for i in kmeans.labels_]
                
                st.success(f"Successfully clustered data into {num_clusters} patterns.")
                
                c1, c2 = st.columns(2)
                with c1:
                    cluster_counts = clustered_df['Cluster'].value_counts().reset_index()
                    cluster_counts.columns = ['Cluster', 'Count']
                    fig_pie = px.pie(cluster_counts, names='Cluster', values='Count', hole=0.4, 
                                     color_discrete_sequence=px.colors.sequential.Teal, title="Cluster Distribution")
                    fig_pie.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
                    st.plotly_chart(fig_pie, use_container_width=True)
                
                with c2:
                    if len(numeric_df.columns) >= 2:
                        # Plot first two features as scatter
                        x_feat = numeric_df.columns[0]
                        y_feat = numeric_df.columns[1]
                        fig_scatter = px.scatter(clustered_df, x=x_feat, y=y_feat, color="Cluster", 
                                                 title=f"{x_feat} vs {y_feat} (Clustered)",
                                                 color_discrete_sequence=px.colors.qualitative.Set3)
                        fig_scatter.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
                        st.plotly_chart(fig_scatter, use_container_width=True)
                        
        elif ml_task == "Predictive Modeling (Linear Regression)":
            st.markdown("#### Linear Regression")
            if len(numeric_df) < 5 or numeric_df.shape[1] < 2:
                st.warning("Need multiple numeric columns and sufficient rows.")
            else:
                target_col = st.selectbox("Select Target Variable to Predict", options=numeric_df.columns, index=len(numeric_df.columns)-1)
                feature_cols = [c for c in numeric_df.columns if c != target_col]
                
                X = numeric_df[feature_cols].values
                y = numeric_df[target_col].values
                
                model = LinearRegression().fit(X, y)
                score = model.score(X, y)
                
                st.success(f"Model trained! R² Score: **{score:.2f}**")
                
                preds = model.predict(X)
                
                compare_df = pd.DataFrame({
                    "Actual": y[:50],
                    "Predicted": preds[:50]
                })
                
                fig_line = go.Figure()
                fig_line.add_trace(go.Scatter(y=compare_df['Actual'], mode='lines', name='Actual', line=dict(color='#0055FF')))
                fig_line.add_trace(go.Scatter(y=compare_df['Predicted'], mode='lines', name='Predicted', line=dict(color='#00F0FF', dash='dash')))
                fig_line.update_layout(title="Actual vs Predicted (First 50 Samples)", 
                                       plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                       xaxis_title="Sample Index", yaxis_title="Value")
                st.plotly_chart(fig_line, use_container_width=True)
