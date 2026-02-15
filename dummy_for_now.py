import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import math

# Page Configuration
st.set_page_config(
    page_title="Pallet-X BI Command Center",
    page_icon="🚛",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Ultra-Modern "Glow" BI Styling
st.markdown("""
    <style>
    /* Gradient Background for App */
    .stApp {
        background: radial-gradient(circle at top right, #1a1f35, #0b0e14);
        color: #e2e8f0;
    }
    
    /* Neon Glow Metric Cards */
    [data-testid="stMetric"] {
        background: rgba(22, 27, 34, 0.7);
        border: 1px solid rgba(88, 166, 255, 0.3);
        padding: 20px !important;
        border-radius: 15px;
        box-shadow: 0 0 15px rgba(88, 166, 255, 0.1);
        transition: all 0.3s ease;
    }
    
    [data-testid="stMetric"]:hover {
        border: 1px solid #58a6ff;
        box-shadow: 0 0 20px rgba(88, 166, 255, 0.2);
    }
    
    [data-testid="stMetricValue"] {
        font-size: 2.8rem !important;
        font-weight: 800 !important;
        background: linear-gradient(45deg, #00f2ff, #7000ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #0d1117;
        border-right: 2px solid #30363d;
    }
    
    .stSelectbox label, .stNumberInput label {
        font-size: 0.9rem !important;
        font-weight: 700 !important;
        color: #00f2ff !important;
        letter-spacing: 0.05rem;
    }
    
    /* Chart Container Styling */
    .chart-container {
        background: rgba(13, 17, 23, 0.6);
        padding: 25px;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    
    /* Critical Alert Styling */
    .critical-lane {
        color: #ff3e3e;
        font-weight: bold;
        background: rgba(255, 62, 62, 0.1);
        padding: 4px 8px;
        border-radius: 4px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: SLICERS & PLANNING ENGINE ---
st.sidebar.markdown("<h1 style='color:#00f2ff; font-size:1.8rem; margin-bottom:0;'>LANE ENGINE</h1>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='color:#8b949e; font-size:0.8rem;'>Route & Load Configuration</p>", unsafe_allow_html=True)

with st.sidebar.expander("🌍 ACTIVE LANE SLICER", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        origin_country = st.selectbox("Origin Country", ["Germany (DE)", "Poland (PL)", "France (FR)"])
        dest_country = st.selectbox("Dest. Country", ["Netherlands (NL)", "UK (GB)", "Spain (ES)"])
    with col2:
        origin_hub = st.selectbox("Origin Hub", ["Munich Hub", "Berlin DC", "Hamburg Port"])
        dest_hub = st.selectbox("Dest. Hub", ["Rotterdam", "London DC", "Madrid South"])

st.sidebar.markdown("---")
st.sidebar.markdown("<h2 style='color:#7000ff; font-size:1.4rem;'>📦 UNIT PARAMETERS</h2>", unsafe_allow_html=True)

total_weight = st.sidebar.number_input("Total Weight (KG)", value=12000, step=500, key="total_weight_input")
boxes_per_pallet = st.sidebar.number_input("Boxes / Pallet", value=48, key="boxes_input")
weight_per_box = st.sidebar.number_input("Weight / Box (KG)", value=15.0, key="weight_box_input")
pallet_cap = st.sidebar.selectbox("Equipment Type", options=[1200, 1500, 500], format_func=lambda x: f"Standard ({x}kg)" if x==1200 else f"Heavy ({x}kg)" if x==1500 else f"Small ({x}kg)")

# --- CALCULATION LOGIC ---
required_pallets = math.ceil(max(total_weight / pallet_cap, (total_weight / weight_per_box) / boxes_per_pallet))
utilization = (max(total_weight / pallet_cap, (total_weight / weight_per_box) / boxes_per_pallet) / required_pallets * 100) if required_pallets > 0 else 0

st.sidebar.markdown("---")
st.sidebar.markdown("### Planning Result")
st.sidebar.success(f"**Required Pallets: {required_pallets}**")

# --- MAIN DASHBOARD ---
st.markdown("<h1 style='color:white; margin-bottom:0; font-weight:900;'>🚀 PALLET-X COMMAND</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#00f2ff; font-size:1.1rem; letter-spacing:0.2rem;'>LANE ANALYTICS & GLOBAL LOGISTICS</p>", unsafe_allow_html=True)

# KPI Metrics Row
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Current Gross (T)", f"{total_weight/1000:.1f}T", delta="+2.4% Week")
kpi2.metric("Planned Pallets", f"{required_pallets}", delta="New Load")
kpi3.metric("Lane Utilization", f"{utilization:.1f}%", delta="Optimization Hub")
kpi4.metric("Annual Flow", "42.8k Units", delta="Strong Trend")

st.markdown("<br>", unsafe_allow_html=True)

# Main Row: Map and Critical Lanes
col_map, col_critical = st.columns([2, 1])

with col_map:
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    st.subheader("🌐 Global Route Intelligence")
    
    # Glow Map Data
    map_data = pd.DataFrame({
        'city': ['Munich', 'Warsaw', 'Lyon', 'Rotterdam', 'London', 'Madrid'],
        'lat': [48.13, 52.22, 45.76, 51.92, 51.50, 40.41],
        'lon': [11.58, 21.01, 4.83, 4.47, -0.12, -3.70],
        'volume': [500, 300, 200, 700, 600, 400],
        'status': ['Active', 'Active', 'Active', 'Critical', 'Critical', 'Active']
    })
    
    fig_map = px.scatter_geo(map_data, lat='lat', lon='lon', color='status', size='volume',
                             hover_name='city', projection="natural earth",
                             color_discrete_map={'Active': '#00f2ff', 'Critical': '#ff3e3e'})
    
    fig_map.update_geos(showcountries=True, countrycolor="#30363d", bgcolor="#0b0e14", 
                        showland=True, landcolor="#161b22", showocean=True, oceancolor="#0b0e14")
    
    fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, paper_bgcolor="rgba(0,0,0,0)",
                          legend=dict(orientation="h", yanchor="bottom", y=0.02, xanchor="right", x=0.98))
    st.plotly_chart(fig_map, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_critical:
    st.markdown("<div class='chart-container' style='height:100%;'>", unsafe_allow_html=True)
    st.subheader("⚠️ Critical Lanes")
    
    critical_lanes = pd.DataFrame({
        "Lane": ["DE → NL", "PL → UK", "FR → ES"],
        "Risk": ["Congestion", "Backlog", "Weight Limit"],
        "Pallets/Wk": [240, 185, 95]
    })
    
    for _, row in critical_lanes.iterrows():
        st.markdown(f"""
        <div style='margin-bottom:15px; border-left:4px solid #ff3e3e; padding-left:10px;'>
            <div style='color:#ff3e3e; font-size:0.9rem; font-weight:bold;'>{row['Lane']}</div>
            <div style='color:#8b949e; font-size:0.8rem;'>{row['Risk']} | <b>{row['Pallets/Wk']} units/wk</b></div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Detailed Lane Frequency Analytics
st.subheader("📊 Lane Throughput Analytics (Pallets & Weight)")
tab1, tab2, tab3 = st.tabs(["📅 Weekly View", "📅 Monthly View", "📅 Yearly View"])

# Generate mock lane data
lanes = ["Munich → Rotterdam", "Berlin → London", "Warsaw → Amsterdam", "Paris → Madrid"]

def generate_lane_data(multiplier):
    return pd.DataFrame({
        "Lane Route": lanes,
        "Pallet Count": [120*multiplier, 85*multiplier, 150*multiplier, 45*multiplier],
        "Total Weight (T)": [144*multiplier, 102*multiplier, 180*multiplier, 54*multiplier],
        "Growth %": ["+5%", "-2%", "+12%", "+1%"]
    })

with tab1:
    st.dataframe(generate_lane_data(1), use_container_width=True)
with tab2:
    st.dataframe(generate_lane_data(4), use_container_width=True)
with tab3:
    st.dataframe(generate_lane_data(52), use_container_width=True)

# Visualizing Volume Mix
st.markdown("<br>", unsafe_allow_html=True)
col_v1, col_v2 = st.columns(2)

with col_v1:
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    st.subheader("📦 Weight Distribution by Route")
    fig_bar = px.bar(generate_lane_data(1), x="Lane Route", y="Total Weight (T)", 
                     color="Total Weight (T)", color_continuous_scale="Viridis")
    fig_bar.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font={'color': "#8b949e"})
    st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_v2:
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    st.subheader("📈 Annual Volume Trend")
    trend_data = pd.DataFrame(np.random.randint(1000, 5000, size=(12, 1)), columns=['Volume'])
    st.line_chart(trend_data, color="#7000ff")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
st.markdown("<p style='text-align: center; color: #484f58; font-size: 0.8rem; letter-spacing: 0.2rem;'>LIVE BI STREAM | PALLET-X ANALYTICS ENGINE v4.5</p>", unsafe_allow_html=True)
