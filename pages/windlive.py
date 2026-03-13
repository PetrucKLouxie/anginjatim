import streamlit as st
import pandas as pd
from streamlit_echarts import st_echarts, JsCode
from streamlit_autorefresh import st_autorefresh
import os

st.set_page_config(page_title="Live Wind Monitor", layout="wide")

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


# =========================
# PATH
# =========================

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CSV_FILE = os.path.join(BASE_DIR, "wind_history.csv")

# Auto refresh 10 menit
st_autorefresh(interval=600000, key="windlive")

# =========================
# CSS
# =========================

st.markdown("""
<style>
.stApp{
background: linear-gradient(135deg,#0f0c29,#302b63,#24243e);
color:white;
}

.glass-card{
background:rgba(255,255,255,0.05);
border-radius:16px;
padding:20px;
border:1px solid rgba(255,255,255,0.1);
}

h1{
background:linear-gradient(135deg,#00d2ff,#3a7bd5);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
}
</style>
""", unsafe_allow_html=True)

# =========================
# NAVIGATION
# =========================

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

# =========================
# LOAD DATA
# =========================

@st.cache_data(ttl=600)
def load_data():

    if not os.path.exists(CSV_FILE):
        return pd.DataFrame()

    df = pd.read_csv(CSV_FILE)

    df["time"] = pd.to_datetime(df["time"], errors="coerce")
    df["speed_kt"] = pd.to_numeric(df["speed_kt"], errors="coerce")
    df["deg"] = pd.to_numeric(df["deg"], errors="coerce")

    df = df.dropna(subset=["city","speed_kt","deg"])

    return df

df = load_data()

if df.empty:
    st.warning("⚠ Tidak ada data angin tersedia")
    st.stop()

# Ambil data terakhir tiap stasiun
df = df.sort_values("time").groupby("city", as_index=False).last()

# =========================
# WIND COMPASS FUNCTION
# =========================

def wind_compass(speed, deg, size=200):

    if speed < 5:
        color = "#00d2ff"
        status = "Calm"
    elif speed < 10:
        color = "#00ff88"
        status = "Light"
    elif speed < 20:
        color = "#ffaa00"
        status = "Moderate"
    else:
        color = "#ff5555"
        status = "Strong"

    direction_formatter = JsCode("""
    function (value) {
        const dir = {
            0:"N",45:"NE",90:"E",135:"SE",
            180:"S",225:"SW",270:"W",315:"NW"
        };
        return dir[Math.round(value/45)*45 % 360] || "";
    }
    """)

    option = {
        "series":[
            {
                "type":"gauge",
                "startAngle":90,
                "endAngle":-270,
                "min":0,
                "max":359.9,

                "splitNumber":8,

                "axisLine":{
                    "lineStyle":{
                        "width":6,
                        "color":[
                            [0.25,"#00d2ff"],
                            [0.5,"#00ff88"],
                            [0.75,"#ffaa00"],
                            [1,"#ff5555"]
                        ]
                    }
                },

                "axisLabel":{
                    "distance":15,
                    "fontSize":12,
                    "color":"white",
                    "formatter":direction_formatter
                },

                "pointer":{
                    "length":"75%",
                    "width":6,
                    "itemStyle":{
                        "color":color
                    }
                },

                "anchor":{
                    "show":True,
                    "size":16,
                    "itemStyle":{
                        "color":color
                    }
                },

                "detail":{
                    "formatter":f"{speed:.1f} kt",
                    "fontSize":16,
                    "offsetCenter":[0,"60%"],
                    "color":"white"
                },

                "data":[{"value":float(deg)}]
            }
        ]
    }

    st_echarts(option, height=f"{size}px")

# =========================
# TITLE
# =========================

st.markdown("""
<h1>🧭 Live Wind Monitoring</h1>
<p>Real-time wind compass untuk setiap stasiun Jawa Timur</p>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR
# =========================

with st.sidebar:

    st.header("Wind Monitor")

    st.write("🧭 Compass menunjukkan arah angin")
    st.write("💨 Kecepatan dalam knot")
    st.write("⏱ Auto refresh 10 menit")

    if st.button("Refresh"):
        st.rerun()

# =========================
# SELECTED CITY
# =========================

if "selected_city" not in st.session_state:
    st.session_state.selected_city = df.iloc[0]["city"]

selected = df[df["city"] == st.session_state.selected_city].iloc[0]

# =========================
# BIG COMPASS
# =========================

c1,c2,c3 = st.columns([1,2,1])

with c2:

    if selected["speed_kt"] > 20:
        st.warning("⚠ Strong wind detected")

    wind_compass(selected["speed_kt"], selected["deg"], size=380)

# =========================
# GRID STATIONS
# =========================

st.markdown("### 🌐 Pilih Stasiun Lain")

grid_df = df[df["city"] != st.session_state.selected_city]

cities = grid_df.to_dict("records")

for i in range(0,len(cities),6):

    row_items = cities[i:i+6]
    cols = st.columns(len(row_items))

    for j,row in enumerate(row_items):

        with cols[j]:

            if st.button(row["city"], key=f"btn_{row['city']}", use_container_width=True):

                st.session_state.selected_city = row["city"]
                st.rerun()

            wind_compass(row["speed_kt"], row["deg"], size=180)

# =========================
# FOOTER
# =========================

st.markdown("---")

st.markdown("""
<center>
Wind Live Jawa Timur • OpenWeather API
</center>
""", unsafe_allow_html=True)
