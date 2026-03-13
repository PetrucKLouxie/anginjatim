import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
import numpy as np
from streamlit_autorefresh import st_autorefresh

st.set_page_config(layout="wide", page_title="Wind History - Jawa Timur")

# =============================
# CUSTOM CSS - MODERN GLASSMORPHISM
# =============================

st.markdown("""
<!-- Animate.css -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css">

<style>

/* ===== GLOBAL STYLES ===== */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

* {
    font-family: 'Poppins', sans-serif !important;
}

/* sembunyikan menu pages default */
[data-testid="stSidebarNav"] {
display:none;
}

/* ===== MAIN BACKGROUND ===== */
.stApp{
background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
color: white;
min-height: 100vh;
}

/* ===== SIDEBAR ===== */
[data-testid="stSidebar"]{
background: linear-gradient(180deg, rgba(15,12,41,0.95) 0%, rgba(48,43,99,0.95) 100%);
border-right: 1px solid rgba(255,255,255,0.08);
}

/* ===== BUTTONS ===== */
div.stButton > button {
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
color: white;
border-radius: 12px;
padding: 10px 20px;
font-weight: 600;
border: none;
transition: all 0.3s ease;
box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

div.stButton > button:hover {
transform: translateY(-2px);
box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
}

/* ===== METRIC CARDS - GLASSMORPHISM ===== */
[data-testid="stMetric"] {
background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
padding: 20px;
border-radius: 16px;
border: 1px solid rgba(255,255,255,0.1);
backdrop-filter: blur(10px);
box-shadow: 0 8px 32px rgba(0,0,0,0.3);
transition: all 0.3s ease;
}

[data-testid="stMetric"]:hover {
transform: translateY(-5px);
box-shadow: 0 12px 40px rgba(0,0,0,0.4);
}

/* ===== CUSTOM CARDS ===== */
.glass-card {
    background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.1);
    backdrop-filter: blur(10px);
    padding: 20px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    transition: all 0.3s ease;
}

.glass-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 40px rgba(0,0,0,0.4);
    border: 1px solid rgba(255,255,255,0.2);
}

/* ===== TITLE STYLING ===== */
h1 {
    background: linear-gradient(135deg, #00d2ff 0%, #3a7bd5 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: 700;
}

/* ===== ANIMATIONS ===== */
.fade-in {
    animation: fadeIn 0.5s ease-in;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.slide-in {
    animation: slideIn 0.5s ease-out;
}

@keyframes slideIn {
    from { opacity: 0; transform: translateX(-50px); }
    to { opacity: 1; transform: translateX(0); }
}

/* ===== HOVER EFFECTS ===== */
.hover-lift {
    transition: all 0.3s ease;
}

.hover-lift:hover {
    transform: translateY(-10px);
    box-shadow: 0 20px 40px rgba(0,0,0,0.4);
}

/* ===== INPUT STYLING ===== */
div[data-testid="stSelectbox"] > div,
div[data-testid="stDateInput"] > div {
    background: rgba(255,255,255,0.05) !important;
    border-radius: 10px !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
}

/* ===== SLIDER STYLING ===== */
div[data-testid="stSlider"] {
    background: rgba(255,255,255,0.05);
    border-radius: 10px;
    padding: 10px;
}

/* ===== DATAFRAME ===== */
[data-testid="stDataFrame"]{
background:rgba(255,255,255,0.02);
border-radius:10px;
}

/* ===== EXPANDER ===== */
streamlit-expander {
    background: rgba(255,255,255,0.05) !important;
    border-radius: 12px !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
}

/* ===== CUSTOM SCROLLBAR ===== */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: rgba(255,255,255,0.05);
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 4px;
}

/* ===== PLOTLY CHARTS ===== */
.js-plotly-plot .plotly .main-svg {
    background: transparent !important;
}

/* ===== WARNING & INFO BOXES ===== */
div[data-testid="stWarning"],
div[data-testid="stInfo"] {
    background: rgba(255,255,255,0.05);
    border-radius: 10px;
    border-left: 4px solid #00d2ff;
}

</style>
""", unsafe_allow_html=True)

# Auto refresh
st_autorefresh(interval=60000, key="history_refresh")

# =============================
# NAVIGATION
# =============================

nav1, nav2, nav3, nav4 = st.columns([4,1,1,1])

with nav2:
    if st.button("🌪 Live Map", use_container_width=True):
        st.switch_page("app.py")

with nav3:
    st.write("")  # placeholder

with nav4:
    if st.button("🧭 Wind Live", use_container_width=True):
        st.switch_page("pages/windlive.py")
# =============================
# TITLE
# =============================

st.markdown("""
<div class="fade-in">
    <h1 style="font-size: 2.5rem; margin-bottom: 0.5rem;">📈 Wind History</h1>
    <p style="color: rgba(255,255,255,0.6); font-size: 1rem;">
        Analisis data angin historis Jawa Timur
    </p>
</div>
""", unsafe_allow_html=True)

# =============================
# SIDEBAR
# =============================

with st.sidebar:

    st.markdown("""
    <div style="text-align:center; padding: 20px 0;">
        <img src="https://cdn-icons-png.flaticon.com/512/1779/1779940.png" width="70" 
             style="border-radius: 50%; padding: 10px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
        <h2 style="margin: 15px 0 5px 0; font-size: 1.3rem;">Wind Monitor</h2>
        <p style="color: rgba(255,255,255,0.5); font-size: 0.9rem;">History Panel</p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("### 🎛️ Filter Options")

    # City filter
    city_filter = st.selectbox(
        "Pilih Kota",
        ["Semua Kota"] + sorted([
            "Juanda", "Perak", "Bawean", "Kalianget", "Banyuwangi",
            "KarangPloso", "Tretes", "KarangKates", "Sawahan", 
            "Tuban", "Pacitan", "Dhoho"
        ])
    )

    st.divider()

    st.markdown("### ℹ️ Info")
    st.write("📈 Data update setiap 10 menit")
    st.write("⏱️ Auto-refresh every 60s")

    if st.button("🔄 Refresh Data", use_container_width=True):
        st.rerun()

# =============================
# LOAD DATA
# =============================

with st.spinner('📊 Loading data...'):
    url = "https://raw.githubusercontent.com/PetrucKLouxie/anginjatim/main/wind_history.csv?t=" + str(time.time())
    try:
        df = pd.read_csv(url)
    except:
        st.error("❌ Gagal mengambil data dari GitHub")
        st.stop()

@st.cache_data(ttl=60)
def load_data():
    url = "https://raw.githubusercontent.com/PetrucKLouxie/anginjatim/main/wind_history.csv?t=" + str(time.time())
    df = pd.read_csv(url)
    df["time"] = pd.to_datetime(df["time"])
    return df

df = load_data()
# =============================
# FILTER
# =============================

data = df.copy()

if city_filter != "Semua Kota":
    data = data[data["city"] == city_filter]

# =============================
# STATISTICS
# =============================

if data.empty:
    st.warning("⚠️ Tidak ada data untuk filter ini")
    st.stop()

st.markdown('<div class="fade-in">', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="glass-card hover-lift" style="text-align: center; padding: 20px;">
        <p style="color: rgba(255,255,255,0.6); font-size: 0.85rem; margin: 0;">💨 Max Wind</p>
        <h2 style="font-size: 2rem; margin: 10px 0; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{:.1f} kt</h2>
    </div>
    """.format(data['speed_kt'].max()), unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="glass-card hover-lift" style="text-align: center; padding: 20px;">
        <p style="color: rgba(255,255,255,0.6); font-size: 0.85rem; margin: 0;">🌊 Avg Wind</p>
        <h2 style="font-size: 2rem; margin: 10px 0; background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{:.1f} kt</h2>
    </div>
    """.format(data['speed_kt'].mean()), unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="glass-card hover-lift" style="text-align: center; padding: 20px;">
        <p style="color: rgba(255,255,255,0.6); font-size: 0.85rem; margin: 0;">📊 Records</p>
        <h2 style="font-size: 2rem; margin: 10px 0; background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); 
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{}</h2>
    </div>
    """.format(len(data)), unsafe_allow_html=True)

with col4:
    # Time range
    if not data.empty:
        time_range = f"{data['time'].min().strftime('%d/%m')} - {data['time'].max().strftime('%d/%m')}"
    else:
        time_range = "-"
    
    st.markdown("""
    <div class="glass-card hover-lift" style="text-align: center; padding: 20px;">
        <p style="color: rgba(255,255,255,0.6); font-size: 0.85rem; margin: 0;">📅 Time Range</p>
        <h2 style="font-size: 1.2rem; margin: 10px 0; color: #00d2ff;">{}</h2>
    </div>
    """.format(time_range), unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =============================
# TIME SLIDER
# =============================

times = data["time"].drop_duplicates().sort_values().tolist()

if len(times) > 1:
    selected_time = st.select_slider(
        "Pilih waktu",
        options=times,
        value=times[-1],
        key="time_slider",
        format_func=lambda x: x.strftime("%Y-%m-%d %H:%M")
    )
else:
    selected_time = times[0]
    

snapshot = data.loc[data["time"].eq(selected_time)]

# =============================
# SNAPSHOT DATA
# =============================

st.markdown("""
<div class="glass-card fade-in" style="padding: 20px;">
    <h3 style="margin: 0 0 15px 0;">📍 Snapshot - Wind Condition</h3>
""", unsafe_allow_html=True)

# Format for display
snapshot_display = snapshot[['city', 'speed_kt', 'deg']].copy()
snapshot_display.columns = ['Kota', 'Kecepatan (kt)', 'Arah (°)']
snapshot_display = snapshot_display.sort_values('Kecepatan (kt)', ascending=False)

st.dataframe(
    snapshot_display,
    use_container_width=True,
    hide_index=True
)

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =============================
# CHARTS
# =============================

col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.markdown("""
    <div class="glass-card fade-in" style="padding: 20px;">
        <h3 style="margin: 0 0 15px 0;">📈 Wind Speed Over Time</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Line chart
    fig = px.line(
        data,
        x="time",
        y="speed_kt",
        color=None if city_filter != "Semua Kota" else "city",
        markers=True,
        template="plotly_dark"
    )
    
    fig.update_layout(
        xaxis_title="Time",
        yaxis_title="Wind Speed (kt)",
        hovermode="x unified",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Poppins"),
        height=400
    )
    
    fig.update_traces(
        line=dict(width=3),
        marker=dict(size=8)
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col_chart2:
    st.markdown("""
    <div class="glass-card fade-in" style="padding: 20px;">
        <h3 style="margin: 0 0 15px 0;">🧭 Wind Direction Distribution</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Direction categorization
    data["direction"] = pd.cut(
        data["deg"] % 360,
        bins=[0,45,90,135,180,225,270,315,360],
        labels=["N","NE","E","SE","S","SW","W","NW"],
        include_lowest=True
    )
    
    # Speed class
    data["speed_class"] = pd.cut(
        data["speed_kt"],
        bins=[0,5,10,15,20,999],
        labels=["0-5","5-10","10-15","15-20",">20"]
    )
    
    # Frequency
    rose_data = (
        data
        .groupby(["direction","speed_class"])
        .size()
        .reset_index(name="count")
    )
    
    total = rose_data["count"].sum()
    rose_data["frequency"] = rose_data["count"] / total * 100
    
    # Wind Rose Plot
    rose = px.bar_polar(
        rose_data,
        r="frequency",
        theta="direction",
        color="speed_class",
        template="plotly_dark",
        color_discrete_sequence=px.colors.sequential.Turbo
    )
    
    rose.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(
                showticklabels=True,
                gridcolor="rgba(255,255,255,0.1)"
            ),
            angularaxis=dict(
                gridcolor="rgba(255,255,255,0.1)"
            )
        ),
        legend_title="Wind Speed (kt)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Poppins"),
        height=400
    )
    
    st.plotly_chart(rose, use_container_width=True)

# =============================
# ADDITIONAL ANALYSIS
# =============================

st.markdown("<br>", unsafe_allow_html=True)

col_analysis1, col_analysis2 = st.columns(2)

with col_analysis1:
    st.markdown("""
    <div class="glass-card fade-in" style="padding: 20px;">
        <h3 style="margin: 0 0 15px 0;">📊 Speed Distribution</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Histogram
    fig_hist = px.histogram(
        data,
        x="speed_kt",
        nbins=20,
        title="Wind Speed Distribution",
        template="plotly_dark",
        color_discrete_sequence=["#00d2ff"]
    )
    
    fig_hist.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis_title="Wind Speed (kt)",
        yaxis_title="Frequency",
        font=dict(family="Poppins"),
        height=350
    )
    
    st.plotly_chart(fig_hist, use_container_width=True)

with col_analysis2:
    st.markdown("""
    <div class="glass-card fade-in" style="padding: 20px;">
        <h3 style="margin: 0 0 15px 0;">🏆 Top Windy Stations</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Top stations by average wind
    top_stations = data.groupby("city")["speed_kt"].mean().sort_values(ascending=False).head(10)
    
    fig_top = px.bar(
        top_stations,
        x="speed_kt",
        y=top_stations.index,
        orientation='h',
        title="Average Wind Speed by Station",
        template="plotly_dark",
        color="speed_kt",
        color_continuous_scale=["#00d2ff", "#f093fb", "#f5576c"]
    )
    
    fig_top.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis_title="Average Wind Speed (kt)",
        yaxis_title="",
        font=dict(family="Poppins"),
        height=350
    )
    
    st.plotly_chart(fig_top, use_container_width=True)

# =============================
# DATA TABLE & DOWNLOAD
# =============================

st.markdown("<br>", unsafe_allow_html=True)

with st.expander("📋 Tampilkan Data Record", expanded=False):
    
    download_df = data.sort_values("time", ascending=False)
    
    st.markdown("""
    <div class="glass-card" style="padding: 0; overflow: hidden;">
    """, unsafe_allow_html=True)
    
    st.dataframe(
        download_df,
        use_container_width=True,
        height=400
    )
    
    col_dl1, col_dl2 = st.columns([1, 4])
    
    with col_dl1:
        st.download_button(
            "⬇ Download CSV",
            download_df.to_csv(index=False),
            "wind_history.csv",
            "text/csv",
            use_container_width=True
        )
    
    st.markdown("</div>", unsafe_allow_html=True)

# =============================
# FOOTER
# =============================

st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px; color: rgba(255,255,255,0.4);">
    <p style="margin: 0;">📈 Wind History Jawa Timur | Powered by OpenWeather API</p>
    <p style="margin: 5px 0 0 0; font-size: 0.8rem;">Auto-refresh every 60 seconds</p>
</div>
""", unsafe_allow_html=True)

