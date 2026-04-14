# Stock Price Prediction System - CNN-LSTM & LSTM Integration

## 📋 Overview

Sistem prediksi harga saham yang mengintegrasikan model **CNN-LSTM (Hybrid)** dan **LSTM standalone** ke dalam aplikasi web interaktif.

### ✨ Fitur Utama

- ✅ Dua model prediksi: CNN+LSTM dan LSTM pure
- ✅ Prediksi untuk 6 saham transportasi: BIRD.JK, BPTR.JK, GIAA.JK, LRNA.JK, PURA.JK, TAXI.JK
- ✅ Dashboard interaktif dengan visualisasi
- ✅ API backend untuk prediksi real-time
- ✅ Metrik evaluasi model (RMSE, R², MAPE, MSE)

---

## 📁 Struktur File

```
├── app.py                          # Flask backend server
├── stockprice deploy.html          # Frontend HTML
├── requirements.txt                # Python dependencies
├── DATASETFIX.xlsx                # Historical stock data
│
├── models/
│   ├── cnn_lstm/
│   │   ├── BIRD.JK_cnn_lstm.keras
│   │   ├── BPTR.JK_cnn_lstm.keras
│   │   └── ... (6 models total)
│   │
│   └── lstm/
│       ├── BIRD.JK_lstm.keras
│       ├── BPTR.JK_lstm.keras
│       └── ... (6 models total)
│
└── data/
    ├── scalers.pkl               # MinMaxScaler objects (opsional)
    └── scaled_data.pkl           # Normalized data (opsional)
```

---

## 🚀 Setup & Installation

### 1️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 2️⃣ Pastikan Model Sudah Disimpan

Jalankan notebook `HYBRID_CNN_LSTM.ipynb` hingga cell terakhir untuk:

- ✅ Melatih model CNN+LSTM untuk semua ticker
- ✅ Melatih model LSTM untuk semua ticker
- ✅ Menyimpan model ke folder `models/cnn_lstm/` dan `models/lstm/`

Struktur file model yang disimpan:

```
models/
├── cnn_lstm/
│   ├── BIRD.JK_cnn_lstm.keras      ← Model file
│   ├── BPTR.JK_cnn_lstm.keras
│   └── ... (6 tickers)
└── lstm/
    ├── BIRD.JK_lstm.keras          ← Model file
    ├── BPTR.JK_lstm.keras
    └── ... (6 tickers)
```

### 3️⃣ Jalankan Server Flask

```bash
python app.py
```

**Output yang diharapkan:**

```
============================================================
🚀 Stock Price Prediction System - Flask Server
============================================================
📁 Base Directory: c:\Users\ASUS\Downloads\umn2\New folder
📁 Models Directory: c:\Users\ASUS\Downloads\umn2\New folder\models
📦 Available Tickers: BIRD.JK, BPTR.JK, GIAA.JK, LRNA.JK, PURA.JK, TAXI.JK
============================================================
🌐 Starting server on http://localhost:5000
============================================================
```

### 4️⃣ Buka Browser

Akses aplikasi di:

```
http://localhost:5000
```

---

## 📖 Cara Menggunakan

### 1. Pilih Parameter

- **Stock Code**: Pilih salah satu dari 6 saham transportasi
- **Model Type**: Pilih antara CNN-LSTM (Hybrid) atau LSTM (Pure)
- **Data Period**: Periode data historis (3-36 bulan)
- **Activation**: Fungsi aktivasi (Auto/Linear/ReLU/Sigmoid/Tanh)
- **Optimizer**: Optimizer (Auto/Adam/Nadam/Adamax/Adagrad)
- **Prediction Days**: Jumlah hari untuk diprediksi (1/5/10/30)

### 2. Klik "Run Prediction"

Sistem akan:

1. Load model yang dipilih
2. Mengambil data historis
3. Melakukan prediksi untuk hari-hari ke depan
4. Menampilkan hasil dengan visualisasi

### 3. Interpretasi Hasil

**Prediction Summary** menampilkan:

- Current Price: Harga terakhir yang diketahui
- Final Prediction: Prediksi harga di hari terakhir
- Prediction Range: Min-Max harga prediksi
- Volatility: Tingkat volatilitas saham

**Model Evaluation** menampilkan:

- **R² Score**: Seberapa baik model (0-100%)
- **RMSE**: Root Mean Squared Error
- **MAPE**: Mean Absolute Percentage Error
- **MSE**: Mean Squared Error

---

## 🔧 API Endpoints

### POST `/api/predict`

Melakukan prediksi harga

**Request:**

```json
{
  "ticker": "BIRD.JK",
  "model_type": "cnn_lstm",
  "prediction_days": 5
}
```

**Response:**

```json
{
    "ticker": "BIRD.JK",
    "model_type": "cnn_lstm",
    "status": "success",
    "historical": {
        "dates": ["2025-03-01", ...],
        "prices": [10000, ...],
        "ma7": [...],
        "ma30": [...]
    },
    "predictions": {
        "dates": ["2025-03-25", ...],
        "prices": [10500, ...]
    },
    "statistics": {...},
    "metrics": {
        "rmse": 0.045,
        "r2": 0.92,
        "mape": 3.5,
        "mse": 0.002
    }
}
```

### GET `/api/models`

Cek model mana yang tersedia

#### GET `/api/historical/<ticker>`

Ambil data historis untuk ticker tertentu

---

## ⚠️ Troubleshooting

### ❌ Error: "Model not found"

- **Solusi**: Pastikan model sudah disimpan dengan menjalankan cell terakhir di notebook
- Cek folder `models/cnn_lstm/` dan `models/lstm/` sudah ada

### ❌ Error: "Connection refused"

- **Solusi**: Pastikan Flask server sudah berjalan dengan perintah `python app.py`
- Check port 5000 tidak terpakai oleh aplikasi lain

### ❌ Error: "No data for ticker"

- **Solusi**: Pastikan file `DATASETFIX.xlsx` ada di folder yang sama dengan `app.py`

### ❌ Prediksi tidak akurat

- **Solusi**:
  - Gunakan model dengan activation & optimizer "Auto (Best)"
  - Cek model sudah selesai training (epoch=50)
  - Gunakan data period lebih lama (24-36 bulan)

---

## 📊 Model Architecture

### CNN-LSTM (Hybrid)

```
Conv1D(64 filters, kernel_size=3)
    ↓
LSTM(50 units)
    ↓
Dense(1)  ← Output
```

### LSTM (Standalone)

```
LSTM(50 units)
    ↓
Dense(1)  ← Output
```

---

## 📈 Performance Metrics Explanation

- **R² Score**:
  - 0.9-1.0: Excellent ✅
  - 0.8-0.9: Good ✅
  - 0.7-0.8: Fair ⚠️
  - <0.7: Poor ❌

- **RMSE**: Semakin kecil semakin baik (ideal < 0.05)

- **MAPE**: Mean Absolute Percentage Error
  - <5%: Excellent ✅
  - 5-10%: Good ✅
  - > 10%: Fair ⚠️

---

## 🛠️ Development

### Frontend (HTML/JavaScript)

- Framework: Vanilla JavaScript
- Plotting: Plotly.js
- Styling: Custom CSS

### Backend (Python/Flask)

- Framework: Flask + Flask-CORS
- ML: TensorFlow/Keras
- Data: Pandas + Scikit-learn

---

## 📝 Notes

1. **Real-time Prediction**: Sistem menggunakan model yang sudah pre-trained dari notebook
2. **Window Size**: Fixed 60 hari untuk sequence input
3. **Normalization**: MinMaxScaler untuk normalize data
4. **Multi-step Forecast**: Prediksi 1-30 hari ke depan secara iteratif

---

## 📄 License

Educational & Research Purposes Only

---

## 👨‍💻 Support

Jika ada pertanyaan atau issue, lakukan:

1. Check troubleshooting section
2. Cek console browser (F12 → Console)
3. Cek Flask server log

---

**Version**: 1.0.0  
**Last Updated**: March 26, 2026  
**Status**: ✅ Operational

---

## Streamlit Deployment (Recommended)

This repo now includes `streamlit_app.py` for Streamlit Cloud or local Streamlit runs.

### Run Locally

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

### Deploy on Streamlit Cloud

1. Push this project to a public GitHub repo.
2. In Streamlit Cloud, create a new app and select:
   - Main file: `streamlit_app.py`
3. Ensure `requirements.txt` and `runtime.txt` are present in the repo.

Notes:
- `runtime.txt` pins Python to 3.10 for TensorFlow compatibility.
- If models are missing, the app will display a mock prediction message.
