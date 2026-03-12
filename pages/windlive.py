import streamlit as st
import pandas as pd
from streamlit_echarts import st_echarts, JsCode
from streamlit_autorefresh import st_autorefresh
import os
import pandas as pd
import time

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CSV_FILE = os.path.join(BASE_DIR, "wind_history.csv")

df = pd.read_csv(CSV_FILE)
st_autorefresh(interval=600000, key="windlive")

st.set_page_config(page_title="Live Wind Monitor", layout="wide")

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
    text-shadow: 0 0 30px rgba(0,210,255,0.3);
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

/* ===== WIND COMPASS ===== */
.wind-compass {
    text-align: center;
    padding: 20px;
}

/* ===== CITY BUTTON ===== */
div.stButton > button.city-btn {
    background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
    border: 1px solid rgba(255,255,255,0.1);
    backdrop-filter: blur(10px);
    color: white;
    padding: 15px 20px;
    border-radius: 12px;
}

div.stButton > button.city-btn:hover {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border: 1px solid rgba(255,255,255,0.2);
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

/* ===== EXPANDER ===== */
streamlit-expander {
    background: rgba(255,255,255,0.05) !important;
    border-radius: 12px !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
}

</style>
""", unsafe_allow_html=True)

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
# LOAD DATA
# =============================

with st.spinner('📊 Loading wind data...'):
    df = pd.read_csv(CSV_FILE)

df["time"] = pd.to_datetime(df["time"], errors="coerce")
df["speed_kt"] = pd.to_numeric(df["speed_kt"], errors="coerce")
df["deg"] = pd.to_numeric(df["deg"], errors="coerce")

df = df.dropna(subset=["city","speed_kt","deg"])

df = df.sort_values("time").groupby("city").tail(1)

# =========================
# COMPASS FUNCTION
# =========================

def wind_compass(speed, deg, size=200, city_name=""):
    
    # Determine color based on speed
    if speed < 3:
        color = "#00d2ff"  # Blue - light
        status = "Light"
    elif speed < 7:
        color = "#00ff88"  # Cyan - moderate
        status = "Moderate"
    elif speed < 12:
        color = "#ffaa00"  # Yellow - strong
        status = "Strong"
    else:
        color = "#ff5555"  # Red - very strong
        status = "Very Strong"

    direction_formatter = JsCode("""
    function (value) {
        const dir = {
            0:"N",
            45:"NE",
            90:"E",
            135:"SE",
            180:"S",
            225:"SW",
            270:"W",
            315:"NW"
        };
        return dir[Math.round(value/45)*45] || "";
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
                        "color": [
                            [0.125, "#00d2ff"],
                            [0.25, "#00ff88"],
                            [0.375, "#ffaa00"],
                            [0.5, "#ff5555"],
                            [0.625, "#00d2ff"],
                            [0.75, "#00ff88"],
                            [0.875, "#ffaa00"],
                            [1, "#ff5555"]
                        ]
                    }
                },

                "axisLabel":{
                    "distance":15,
                    "fontSize":12,
                    "color": "#ffffff",
                    "formatter":direction_formatter
                },

                "axisTick":{
                    "show":True,
                    "length": 8,
                    "lineStyle": {
                        "color": "#ffffff",
                        "width": 1
                    }
                },

                "splitLine":{
                    "length":12,
                    "lineStyle":{
                        "color":"#ffffff",
                        "width": 2
                    }
                },

                "pointer":{
                    "length":"75%",
                    "width":6,
                    "itemStyle": {
                        "color": """ + f'"{color}"' + """
                    }
                },

                "anchor": {
                    "show": True,
                    "showAbove": True,
                    "size": 20,
                    "itemStyle": {
                        "borderWidth": 4,
                        "color": """ + f'"{color}"' + """
                    }
                },

                "detail":{
                    "formatter":f""" + f'"{speed:.1f} kt\\n{status}"' + """,
                    "fontSize":18,
                    "offsetCenter":[0,"60%"],
                    "color": "#ffffff"
                },

                "data":[{"value":float(deg)}],
                "title": {
                    "show": True,
                    "offsetCenter": [0, "100%"],
                    "color": "#ffffff",
                    "fontSize": 14
                }
            }
        ]
    }

    st_echarts(option, height=f"{size}px")

# =========================
# TITLE
# =========================

st.markdown("""
<div class="fade-in">
    <h1 style="font-size: 2.5rem; margin-bottom: 0.5rem;">🧭 Live Wind Monitoring</h1>
    <p style="color: rgba(255,255,255,0.6); font-size: 1rem;">
        Real-time wind compass untuk setiap stasiun di Jawa Timur
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =========================
# SIDEBAR INFO
# =========================

with st.sidebar:

    st.markdown("""
    <div style="text-align:center; padding: 20px 0;">
        <img src="https://cdn-icons-png.flaticon.com/512/1779/1779940.png" width="70" 
             style="border-radius: 50%; padding: 10px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
        <h2 style="margin: 15px 0 5px 0; font-size: 1.3rem;">Wind Monitor</h2>
        <p style="color: rgba(255,255,255,0.5); font-size: 0.9rem;">Live Compass Panel</p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("### ℹ️ Info")
    st.write("🧭 Compass menunjukkan arah angin")
    st.write("💨 Kecepatan dalam knot")
    st.write("⏱️ Auto-refresh: 10 menit")

    if st.button("🔄 Refresh", use_container_width=True):
        st.rerun()

# =========================
# SELECTED CITY
# =========================

if "selected_city" not in st.session_state:
    st.session_state.selected_city = df.iloc[0]["city"]

selected = df[df["city"] == st.session_state.selected_city].iloc[0]

# =========================
# BIG COMPASS CENTER
# =========================

st.markdown('<div class="fade-in">', unsafe_allow_html=True)

c1,c2,c3 = st.columns([1,2,1])

with c2:
    st.markdown("""
    <div class="glass-card" style="text-align: center; padding: 30px;">
        <h2 style="margin: 0 0 20px 0; color: #00d2ff;">📍 {}</h2>
    </div>
    """.format(selected['city']), unsafe_allow_html=True)
    wind_compass(selected["speed_kt"], selected["deg"], size=380, city_name=selected['city'])

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =========================
# GRID (6 PER BARIS)
# =========================

st.markdown("""
<div class="glass-card fade-in" style="padding: 20px;">
    <h3 style="margin: 0 0 15px 0;">🌐 Pilih Stasiun Lain</h3>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

grid_df = df[df["city"] != st.session_state.selected_city]

cities = grid_df.to_dict("records")

for i in range(0, len(cities), 6):

    row_items = cities[i:i+6]
    n = len(row_items)

    left_space = (6 - n) // 2
    right_space = 6 - n - left_space

    cols = st.columns(left_space + n + right_space)

    for j, row in enumerate(row_items):
        
        with cols[left_space + j]:
            # Create a card for each city
            st.markdown(f"""
            <div class="glass-card hover-lift" style="padding: 15px; text-align: center;">
                <h4 style="margin: 0 0 10px 0; color: #00d2ff;">{row['city']}</h4>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(row["city"], use_container_width=True, key=f"btn_{row['city']}"):
                st.session_state.selected_city = row["city"]
                st.rerun()

            wind_compass(row["speed_kt"], row["deg"], size=180, city_name=row['city'])

st.markdown("<br>", unsafe_allow_html=True)

# =============================
# FOOTER
# =============================

st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px; color: rgba(255,255,255,0.4);">
    <p style="margin: 0;">🧭 Wind Live Jawa Timur | Powered by OpenWeather API</p>
    <p style="margin: 5px 0 0 0; font-size: 0.8rem;">Auto-refresh every 10 minutes</p>
</div>
""", unsafe_allow_html=True)

