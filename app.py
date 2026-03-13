import streamlit as st
import requests
import pandas as pd
import pydeck as pdk
import plotly.express as px
import plotly.graph_objects as go
import os
import math
import numpy as np
import base64
import time 
import random

from dotenv import load_dotenv
from stations import stations
from streamlit_autorefresh import st_autorefresh
from datetime import datetime

# =============================
# CONFIG
# =============================

st.set_page_config(
    layout="wide", 
    page_title="Wind Monitoring Jawa Timur",
    page_icon="🌪️",
    initial_sidebar_state="expanded"
)

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
backdrop-filter: blur(10px);
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
background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
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
border: 1px solid rgba(255,255,255,0.2);
}

/* ===== TITLE STYLING ===== */
h1 {
    background: linear-gradient(135deg, #00d2ff 0%, #3a7bd5 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: 700;
    text-shadow: 0 0 30px rgba(0,210,255,0.3);
}

/* ===== DIVIDER ===== */
hr, [data-testid="stDivider"] {
border-color: rgba(255,255,255,0.1);
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

/* ===== ANIMATED BACKGROUND PARTICLES ===== */
.particles {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: -1;
    overflow: hidden;
}

.particle {
    position: absolute;
    width: 4px;
    height: 4px;
    background: rgba(255,255,255,0.3);
    border-radius: 50%;
    animation: float 15s infinite;
}

@keyframes float {
    0%, 100% {
        transform: translateY(0) translateX(0);
        opacity: 0;
    }
    10% {
        opacity: 1;
    }
    90% {
        opacity: 1;
    }
    100% {
        transform: translateY(-100vh) translateX(100px);
        opacity: 0;
    }
}

/* ===== RADIO BUTTON ===== */
div[data-testid="stRadio"] > div {
    background: rgba(255,255,255,0.05);
    border-radius: 12px;
    padding: 5px;
}

div[data-testid="stRadio"] > div > label {
    background: transparent;
    border-radius: 8px;
    padding: 8px 16px;
    transition: all 0.3s ease;
}

div[data-testid="stRadio"] > div > label:has(input:checked) {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* ===== PLOTLY CHARTS ===== */
.js-plotly-plot .plotly .main-svg {
    background: transparent !important;
}

/* ===== SIDEBAR TITLE ===== */
[data-testid="stSidebarNav"]::before{
content:"🌪 WIND CONTROL";
font-size:20px;
font-weight:700;
margin-left:15px;
margin-bottom:15px;
display:block;
background: linear-gradient(135deg, #00d2ff 0%, #3a7bd5 100%);
-webkit-background-clip: text;
-webkit-text-fill-color: transparent;
}

/* ===== TOGGLE STYLING ===== */
div[data-testid="stToggle"] > label {
    background: rgba(255,255,255,0.05);
    border-radius: 8px;
    padding: 8px 12px;
}

/* ===== EXPANDER ===== */
streamlit-expander {
    background: rgba(255,255,255,0.05) !important;
    border-radius: 12px !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
}

/* ===== LOADING ANIMATION ===== */
.loading-pulse {
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0% { opacity: 1; }
    50% { opacity: 0.5; }
    100% { opacity: 1; }
}

/* ===== FADE IN ANIMATION ===== */
.fade-in {
    animation: fadeIn 0.5s ease-in;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

/* ===== SLIDE IN ANIMATION ===== */
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

/* ===== STATION MARKER ===== */
.station-marker {
    display: flex;
    align-items: center;
    padding: 10px;
    margin: 5px 0;
    background: rgba(255,255,255,0.05);
    border-radius: 10px;
    transition: all 0.3s ease;
}

.station-marker:hover {
    background: rgba(255,255,255,0.1);
    transform: translateX(5px);
}

.station-marker .pulse {
    width: 10px;
    height: 10px;
    background: #00ff88;
    border-radius: 50%;
    margin-right: 10px;
    animation: pulse-dot 2s infinite;
}

@keyframes pulse-dot {
    0% { box-shadow: 0 0 0 0 rgba(0,255,136, 0.7); }
    70% { box-shadow: 0 0 0 10px rgba(0,255,136, 0); }
    100% { box-shadow: 0 0 0 0 rgba(0,255,136, 0); }
}

/* ===== WIND INDICATOR ===== */
.wind-direction {
    display: inline-block;
    animation: wind-blow 2s ease-in-out infinite;
}

@keyframes wind-blow {
    0%, 100% { transform: rotate(0deg); }
    25% { transform: rotate(15deg); }
    75% { transform: rotate(-15deg); }
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

/* ===== CHART CONTAINER ===== */
.chart-container {
    background: rgba(255,255,255,0.03);
    border-radius: 16px;
    padding: 20px;
    border: 1px solid rgba(255,255,255,0.08);
    margin: 10px 0;
}

</style>

<!-- Animated Background Script -->
<script>
function createParticles() {
    const container = document.createElement('div');
    container.className = 'particles';
    
    for(let i = 0; i < 50; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.left = Math.random() * 100 + '%';
        particle.style.top = Math.random() * 100 + '%';
        particle.style.animationDelay = Math.random() * 15 + 's';
        particle.style.animationDuration = (10 + Math.random() * 10) + 's';
        
        const size = Math.random() * 4 + 2;
        particle.style.width = size + 'px';
        particle.style.height = size + 'px';
        
        container.appendChild(particle);
    }
    
    document.body.appendChild(container);
}

if(document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', createParticles);
} else {
    createParticles();
}
</script>
""", unsafe_allow_html=True)

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API")

# Auto refresh
st_autorefresh(interval=60000, key="refresh")

# =============================
# NAVIGATION
# =============================

nav1, nav2, nav3, nav4 = st.columns([4,1,1,1])

with nav2:
    if st.button("🌪 Live Map", use_container_width=True):
        st.switch_page("app.py")



with nav3:
    if st.button("📈 History", use_container_width=True):
        st.switch_page("pages/history_new.py")

with nav4:

    if st.button("🧭 Wind Live", use_container_width=True):
        st.switch_page("pages/windlive.py")

# =============================
# TITLE
# =============================

st.markdown("""
<div class="fade-in">
    <h1 style="font-size: 2.5rem; margin-bottom: 0.5rem;">🌬️ Wind Monitoring Jawa Timur</h1>
    <p style="color: rgba(255,255,255,0.6); font-size: 1rem; margin-top: 0;">
        🔄 Data sumber: OpenWeather API • Auto-refresh every 60s
    </p>
</div>
""", unsafe_allow_html=True)

# =============================
# SIDEBAR
# =============================

with st.sidebar:

    st.markdown("""
    <div style="text-align:center; padding: 20px 0;">
        <div style="position: relative; display: inline-block;">
            <img src="https://cdn-icons-png.flaticon.com/512/1779/1779940.png" width="80" 
                 style="border-radius: 50%; padding: 10px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
            <div style="position: absolute; bottom: 10px; right: 10px; width: 15px; height: 15px; 
                        background: #00ff88; border-radius: 50%; border: 3px solid #0f0c29;"></div>
        </div>
        <h2 style="margin: 15px 0 5px 0; font-size: 1.5rem;">Wind Monitor</h2>
        <p style="color: rgba(255,255,255,0.5); font-size: 0.9rem;">Jawa Timur, Indonesia</p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("### 🗺 Layer Map")

    show_vector = st.toggle("Wind Vector", True)
    show_station = st.toggle("Station Marker", True)

    st.divider()

    st.markdown("### 📡 Lokasi Stations")

    for s in stations:
        st.markdown(f"""
        <div class="station-marker">
            <div class="pulse"></div>
            <span>{s['name']}</span>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Theme selector
    st.markdown("### 🎨 Theme")
    theme = st.radio(
        "Pilih Tampilan",
        ["Dark", "Road", "Light"],
        horizontal=True
    )

# =============================
# FUNCTION GET WEATHER
# =============================

@st.cache_data(ttl=60)
def get_weather(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    r = requests.get(url, timeout=10)
    data = r.json()

    wind = data.get("wind", {})
    speed = wind.get("speed", 0)
    deg = wind.get("deg", 0)

    return speed, deg
    except:
        return 0, 0

# =============================
# RECORD TO GITHUB
# =============================

def record_to_github(df):
    token = st.secrets["GITHUB_TOKEN"]
    repo = st.secrets["GITHUB_REPO"]
    path = "wind_history.csv"
    url = f"https://api.github.com/repos/{repo}/contents/{path}"
    headers = {"Authorization": f"token {token}"}
    r = requests.get(url, headers=headers)
    data = r.json()
    content = base64.b64decode(data["content"]).decode()
    lines = content.split("\n")
    now = datetime.utcnow()
    rounded = now.replace(minute=(now.minute // 10) * 10, second=0, microsecond=0)
    if len(lines) > 1:
        last_time = lines[-1].split(",")[0]
    else:
        last_time = None
    if str(rounded) in last_time:
        return
    new_rows = ""
    for _, row in df.iterrows():
        new_rows += f"\n{rounded},{row['city']},{row['speed_kt']},{row['deg']}"
    content += new_rows
    encoded = base64.b64encode(content.encode()).decode()
    requests.put(url, headers=headers, json={"message": "update wind history", "content": encoded, "sha": data["sha"]})

# =============================
# COLLECT DATA
# =============================

data_list=[]
for s in stations:
    speed,deg=get_weather(s["lat"],s["lon"])
    data_list.append({
        "city":s["name"],
        "lat":s["lat"],
        "lon":s["lon"],
        "speed":speed,
        "deg":deg
    })

df=pd.DataFrame(data_list)
df["speed_kt"]=(df["speed"]*1.94384).round(1)

# Record to github (commented out for demo)
# record_to_github(df)

# =============================
# METRIC PANEL - MODERN CARDS
# =============================

st.markdown('<div class="fade-in">', unsafe_allow_html=True)

col1,col2,col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="glass-card hover-lift" style="text-align: center; padding: 25px;">
        <p style="color: rgba(255,255,255,0.6); font-size: 0.9rem; margin: 0;">📡 Total Stations</p>
        <h2 style="font-size: 2.5rem; margin: 10px 0; background: linear-gradient(135deg, #00d2ff 0%, #3a7bd5 100%); 
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{}</h2>
    </div>
    """.format(len(df)), unsafe_allow_html=True)

with col2:
    max_speed = df.speed_kt.max()
    max_city = df.loc[df.speed_kt.idxmax(), 'city']
    st.markdown("""
    <div class="glass-card hover-lift" style="text-align: center; padding: 25px;">
        <p style="color: rgba(255,255,255,0.6); font-size: 0.9rem; margin: 0;">💨 Max Wind</p>
        <h2 style="font-size: 2.5rem; margin: 10px 0; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{:.1f} kt</h2>
        <p style="color: rgba(255,255,255,0.5); font-size: 0.8rem; margin: 0;">📍 {}</p>
    </div>
    """.format(max_speed, max_city), unsafe_allow_html=True)

with col3:
    avg_speed = df.speed_kt.mean()
    st.markdown("""
    <div class="glass-card hover-lift" style="text-align: center; padding: 25px;">
        <p style="color: rgba(255,255,255,0.6); font-size: 0.9rem; margin: 0;">🌊 Average Wind</p>
        <h2 style="font-size: 2.5rem; margin: 10px 0; background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{:.1f} kt</h2>
    </div>
    """.format(avg_speed), unsafe_allow_html=True)

with col4:
    # Get wind direction most common
    most_common_deg = df['deg'].mean()
    direction_labels = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    direction_idx = int((most_common_deg + 22.5) // 45) % 8
    direction = direction_labels[direction_idx]
    st.markdown("""
    <div class="glass-card hover-lift" style="text-align: center; padding: 25px;">
        <p style="color: rgba(255,255,255,0.6); font-size: 0.9rem; margin: 0;">🧭 Avg Direction</p>
        <h2 style="font-size: 2.5rem; margin: 10px 0; background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); 
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{}</h2>
    </div>
    """.format(direction), unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =============================
# THEME SETTINGS
# =============================

if theme == "Dark":
    map_style = "dark"
    plotly_template = "plotly_dark"
elif theme == "Light":
    map_style = "light"
    plotly_template = "plotly_white"
else:
    map_style = "road"
    plotly_template = "plotly_dark"

# =============================
# DATA PREPARATION FOR MAP
# =============================

df_station = pd.DataFrame(stations)
df_wind = pd.DataFrame(data_list)

df = df_station.merge(df_wind, left_on="name", right_on="city", how="left")

df["speed_kt"] = (df["speed"] * 1.94384).round(1)

df = df.rename(columns={
    "lat_x":"lat",
    "lon_x":"lon"
})
# Animated wind vectors
t = time.time()
scale = 0.08

df["lat2"] = df["lat"] + np.cos(np.radians(df["deg"])) * scale
df["lon2"] = df["lon"] + np.sin(np.radians(df["deg"])) * scale

# Add some animation
df["lat2"] += np.sin(t) * 0.015
df["lon2"] += np.cos(t) * 0.015

# Wind color function
def wind_color(speed):
    if speed < 3:
        return [0,150,255]  # Blue - light
    elif speed < 7:
        return [0,255,180]  # Cyan - moderate
    elif speed < 12:
        return [255,200,0]  # Yellow - strong
    else:
        return [255,80,80]  # Red - very strong

df["color"]=df["speed_kt"].apply(wind_color)

# =============================
# MAP WITH IMPROVED STYLING
# =============================

st.markdown("""
<div class="glass-card fade-in" style="padding: 0; overflow: hidden;">
    <div style="padding: 15px 20px; border-bottom: 1px solid rgba(255,255,255,0.1);">
        <h3 style="margin: 0;">🗺️ Interactive Wind Map</h3>
    </div>
""", unsafe_allow_html=True)

# Arrow layer with better styling
arrow_layer = pdk.Layer(
    "LineLayer",
    df,
    get_source_position='[lon,lat]',
    get_target_position='[lon2,lat2]',
    get_width=6,
    get_color=[255,140,0],
    pickable=True,
    opacity=0.8
)

# Point layer with glowing effect
point_layer = pdk.Layer(
    "ScatterplotLayer",
    df,
    get_position='[lon,lat]',
    get_radius=5000,
    get_fill_color=[255,80,80],
    pickable=True,
    opacity=0.9
)

# Layers list
layers = []
if show_vector:
    layers.append(arrow_layer)
if show_station:
    layers.append(point_layer)

# View state
view = pdk.ViewState(
    latitude=-7.8,
    longitude=112.5,
    zoom=7,
    pitch=0,
    bearing=0
)

# Tooltip with better styling
tooltip = {
"html":"""
<div style="background: rgba(15,12,41,0.95); padding: 15px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.2);">
    <b style="font-size: 1.1rem; color: #00d2ff;">{city}</b><br>
    <hr style="border-color: rgba(255,255,255,0.1); margin: 8px 0;">
    <span style="color: #00ff88;">🌬 Wind Speed:</span> <b>{speed_kt} kt</b><br>
    <span style="color: #ffaa00;">🧭 Direction:</span> <b>{deg}°</b>
</div>
""",
"style": {
    "backgroundColor": "transparent",
    "color": "white"
}
}

deck = pdk.Deck(
    layers=layers,
    initial_view_state=view,
    tooltip=tooltip,
    map_style=map_style,
    height=500
)

# Auto refresh for wind animation
st_autorefresh(interval=10000)

st.pydeck_chart(deck)

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =============================
# CHARTS SECTION
# =============================

col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.markdown("""
    <div class="glass-card fade-in" style="padding: 20px;">
        <h3 style="margin: 0 0 15px 0;">📊 Wind Speed Distribution</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Wind speed bar chart with gradient colors
    fig = px.bar(
        df.sort_values("speed_kt", ascending=True),
        x="speed_kt",
        y="city",
        orientation='h',
        title="Wind Speed by Station (kt)",
        template=plotly_template,
        color="speed_kt",
        color_continuous_scale=["#00d2ff", "#4facfe", "#f093fb", "#f5576c"]
    )
    
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis_title="Wind Speed (kt)",
        yaxis_title="",
        font=dict(family="Poppins"),
        height=400
    )
    
    fig.update_traces(
        marker=dict(line=dict(color="rgba(255,255,255,0.1)", width=1))
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col_chart2:
    st.markdown("""
    <div class="glass-card fade-in" style="padding: 20px;">
        <h3 style="margin: 0 0 15px 0;">🧭 Wind Direction (Wind Rose)</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Wind direction categorization
    df["direction"] = pd.cut(
        df["deg"],
        bins=[0,45,90,135,180,225,270,315,360],
        labels=["N","NE","E","SE","S","SW","W","NW"]
    )
    
    # Polar/Wind Rose chart
    rose_data = df.groupby("direction").size().reset_index(name="count")

    rose = px.bar_polar(
        rose_data,
        r="count",
        theta="direction",
        title="Wind Rose - Direction Frequency",
        template=plotly_template,
        color="count",
        color_continuous_scale="Turbo"
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
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Poppins"),
        height=400
    )
    
    st.plotly_chart(rose, use_container_width=True)

# =============================
# REAL-TIME WIND INDICATORS
# =============================

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<div class="glass-card fade-in" style="padding: 20px;">
    <h3 style="margin: 0 0 15px 0;">💨 Real-Time Wind Indicators</h3>
</div>
""", unsafe_allow_html=True)

# Create animated wind indicators for each station
cols = st.columns(len(df))

for i, row in df.iterrows():
    direction_labels = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    direction_idx = int((row['deg'] + 22.5) // 45) % 8
    direction = direction_labels[direction_idx]
    
    # Determine color based on speed
    if row['speed_kt'] < 3:
        color = "#00d2ff"
        status = "Light"
    elif row['speed_kt'] < 7:
        color = "#00ff88"
        status = "Moderate"
    elif row['speed_kt'] < 12:
        color = "#ffaa00"
        status = "Strong"
    else:
        color = "#ff5555"
        status = "Very Strong"
    
    with cols[i]:
        st.markdown(f"""
        <div class="glass-card hover-lift" style="padding: 15px; text-align: center;">
            <p style="margin: 0; color: rgba(255,255,255,0.6); font-size: 0.85rem;">{row['city']}</p>
            <div style="font-size: 2rem; margin: 10px 0;">
                <span class="wind-direction" style="color: {color};">{direction}</span>
            </div>
            <p style="margin: 0; font-size: 1.3rem; font-weight: 600; color: {color};">{row['speed_kt']:.1f} kt</p>
            <p style="margin: 5px 0 0 0; font-size: 0.75rem; color: rgba(255,255,255,0.5);">{status}</p>
            <p style="margin: 0; font-size: 0.75rem; color: rgba(255,255,255,0.4);">{row['deg']}°</p>
        </div>
        """, unsafe_allow_html=True)

# =============================
# DATA TABLE
# =============================

st.markdown("<br>", unsafe_allow_html=True)

with st.expander("📋 View Detailed Data", expanded=False):
    st.markdown("""
    <div class="glass-card" style="padding: 0; overflow: hidden;">
    """, unsafe_allow_html=True)
    
    # Format dataframe for display
    display_df = df[['city', 'lat', 'lon', 'speed_kt', 'deg', 'direction']].copy()
    display_df.columns = ['City', 'Latitude', 'Longitude', 'Speed (kt)', 'Direction (°)', 'Direction']
    display_df = display_df.sort_values('Speed (kt)', ascending=False)
    
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )
    
    # Download button
    csv = display_df.to_csv(index=False)
    st.download_button(
        "⬇ Download CSV",
        csv,
        "wind_data_jawa_timur.csv",
        "text/csv"
    )
    
    st.markdown("</div>", unsafe_allow_html=True)

# =============================
# FOOTER
# =============================

st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px; color: rgba(255,255,255,0.4);">
    <p style="margin: 0;">🌪️ Wind Monitoring Jawa Timur | Powered by OpenWeather API</p>
    <p style="margin: 5px 0 0 0; font-size: 0.8rem;">Auto-refresh every 60 seconds</p>
</div>
""", unsafe_allow_html=True)

