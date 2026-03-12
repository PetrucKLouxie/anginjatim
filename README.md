# 🌬️ Wind Monitoring Jawa Timur

Aplikasi monitoring kecepatan dan arah angin real-time untuk wilayah Jawa Timur, Indonesia. Dibangun dengan Streamlit dan menggunakan data dari OpenWeather API.

![Wind Monitoring](https://img.shields.io/badge/Wind-Monitoring-brightgreen)
![Streamlit](https://img.shields.io/badge/Streamlit-2.0+-red)
![Python](https://img.shields.io/badge/Python-3.8+-blue)

## 📋 Fitur

### 🌪️ Live Map (Halaman Utama)
- Peta interaktif dengan PyDeck showing lokasi stasiun
- Vektor angin animasi yang menunjukkan arah dan kecepatan
- Marker untuk setiap stasiun pengukuran
- Update data otomatis setiap 60 detik

### 📈 History
- Data historis kecepatan angin
- Visualisasi waktu nyata dengan line chart
- Wind rose chart untuk distribusi arah angin
- Analisis histogram kecepatan angin
- Filter berdasarkan kota dan rentang waktu

### 🧭 Wind Live
- Compass gauge real-time untuk setiap stasiun
- Visualisasi arah angin dengan indikator
- Tampilan grid untuk membandingkan semua stasiun

## 🗺️ Lokasi Stasiun

| No | Stasiun | Latitude | Longitude |
|----|---------|----------|-----------|
| 1 | Juanda | -7.3724 | 112.7818 |
| 2 | Perak | -7.2236 | 112.7241 |
| 3 | Bawean | -5.8505 | 112.6574 |
| 4 | Kalianget | -7.0408 | 113.9159 |
| 5 | Banyuwangi | -8.2148 | 114.3554 |
| 6 | KarangPloso | -7.9006 | 112.5978 |
| 7 | Tretes | -7.7045 | 112.6357 |
| 8 | KarangKates | -8.1522 | 112.4508 |
| 9 | Sawahan | -7.7344 | 111.7669 |
| 10 | Tuban | -6.8221 | 111.9919 |
| 11 | Pacitan | -8.1945 | 111.1770 |
| 12 | Dhoho | -7.7549 | 111.9471 |

## 🚀 Cara Menjalankan

### Prerequisites
- Python 3.8 atau lebih tinggi
- OpenWeather API Key

### Installation

1. Clone repository:
```bash
git clone https://github.com/PetrucKLouxie/anginjatim.git
cd anginjatim
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Setup environment variables:
Buat file `.env` dengan konten:
```
OPENWEATHER_API=your_api_key_here
GITHUB_TOKEN=your_github_token (optional, untuk recording data)
GITHUB_REPO=your_repo (optional)
```

4. Run aplikasi:
```bash
streamlit run app.py
```

5. Buka browser di `http://localhost:8501`

## 📁 Struktur Project

```
anginjatim/
├── app.py                 # Halaman utama - Live Map
├── stations.py           # Data lokasi stasiun
├── wind_history.csv      # Data historis angin
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables
├── README.md             # Dokumentasi
└── pages/
    ├── history.py        # Halaman history (lama)
    ├── history_new.py    # Halaman history (baru)
    └── windlive.py       # Halaman Wind Live
```

## 🎨 Teknologi

- **Framework**: Streamlit
- **Visualisasi**: Plotly, PyDeck, ECharts
- **Data**: OpenWeather API
- **Styling**: Custom CSS dengan Glassmorphism

## 📊 Tampilan

Aplikasi ini menggunakan desain modern dengan:
- Glassmorphism effect
- Animasi transisi halus
- Gradient colors
- Dark theme
- Responsive layout

## 🤝 Kontribusi

Silakan buat pull request untuk improvement!

## 📝 Lisensi

MIT License

---

Dibuat dengan ❤️ untuk Jawa Timur

