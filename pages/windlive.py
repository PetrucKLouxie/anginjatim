import streamlit as st
import pandas as pd
from streamlit_echarts import st_echarts, JsCode
from streamlit_autorefresh import st_autorefresh
import os

st.set_page_config(page_title="Live Wind Monitor", layout="wide")

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
                    "formatter":f"{speed:.1f} kt\\n{status}",
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

            st.markdown(f"""
            <div class="glass-card">
            <h4 style="text-align:center">{row['city']}</h4>
            </div>
            """, unsafe_allow_html=True)

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
