# 🚀 Quick Start Guide

## ⏰ 5 Menit untuk Mulai

### Step 1: Jalankan Notebook untuk Training & Saving Model ⏳ (10-15 menit)

1. Buka file `HYBRID_CNN_LSTM.ipynb` di Jupyter atau VS Code
2. Jalankan semua cell dari atas hingga bawah:
   - Cell dengan title "Data Understanding" hingga "Compare CNN+LSTM vs LSTM Performance"
   - Notebook akan:
     - ✅ Load data dari `DATASETFIX.xlsx`
     - ✅ Membersihkan dan normalize data
     - ✅ Membuat sequences
     - ✅ Train CNN+LSTM model untuk 6 ticker
     - ✅ Train LSTM standalone untuk 6 ticker
     - ✅ **Menyimpan model ke folder `models/`**
     - ✅ Membandingkan performa kedua model

3. Tunggu hingga selesai (bar loading akan menunjukkan progress)

**Output yang diharapkan:**

```
===================================================
All models saved successfully!
===================================================
✓ CNN+LSTM Model saved: models/cnn_lstm/BIRD.JK_cnn_lstm.keras
✓ LSTM Model saved: models/lstm/BIRD.JK_lstm.keras
... (6 ticker total)
```

### Step 2: Install Dependencies 📦 (2-3 menit)

Buka terminal/command prompt di folder project dan jalankan:

```bash
pip install -r requirements.txt
```

Tunggu hingga semua package selesai diinstall.

### Step 3: Jalankan Flask Server 🚀 (1 detik)

#### Opsi A: Dengan Script (Recommended)

Double-click file: **`run_server.bat`**

#### Opsi B: Manual

Buka terminal dan ketik:

```bash
python app.py
```

**Jika berhasil, akan terlihat:**

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

### Step 4: Buka Browser & Gunakan Aplikasi 💻

1. Buka browser favorit (Chrome, Firefox, Edge, Safari)
2. Ketik di address bar:

   ```
   http://localhost:5000
   ```

3. Dashboard akan terbuka dengan form input

### Step 5: Lakukan Prediksi 🎯

Pilih parameter:

- **Stock Code**: BIRD.JK, BPTR.JK, GIAA.JK, LRNA.JK, PURA.JK, atau TAXI.JK
- **Model Type**: CNN-LSTM atau LSTM
- **Prediction Days**: 1, 5, 10, atau 30 hari

Klik **"Run Prediction"** dan tunggu hasil!

---

## 📊 Interpretasi Hasil

### Prediction Summary

| Metrik               | Arti                                          |
| -------------------- | --------------------------------------------- |
| **Current Price**    | Harga saham terakhir yang diketahui           |
| **Final Prediction** | Prediksi harga di hari terakhir               |
| **Change**           | Selisih harga dari sekarang ke prediksi       |
| **Volatility**       | Tingkat perubahan harga (High = Berfluktuasi) |

### Model Evaluation

| Metrik       | Baik Jika | Penjelasan                                    |
| ------------ | --------- | --------------------------------------------- |
| **R² Score** | > 0.85    | Seberapa akurat model memprediksi (0-100%)    |
| **RMSE**     | < 0.05    | Error rata-rata (semakin kecil semakin baik)  |
| **MAPE**     | < 5%      | Persentase error (semakin kecil semakin baik) |
| **MSE**      | Low       | Mean Squared Error                            |

### Chart Explanation

- **Blue Line (Actual Price)**: Harga historis yang sebenarnya
- **Green Dotted (MA 7)**: Moving Average 7 hari
- **Orange Dotted (MA 30)**: Moving Average 30 hari
- **Red Dashed (Prediction)**: Prediksi harga ke depan

---

## ✅ Checklist Verifikasi

Pastikan setup Anda lengkap:

- [ ] Python 3.8+ terinstall
- [ ] File `DATASETFIX.xlsx` ada di folder project
- [ ] Folder `models/cnn_lstm/` berisi 6 file `.keras`
- [ ] Folder `models/lstm/` berisi 6 file `.keras`
- [ ] File `requirements.txt` ada
- [ ] Semua package di-install: `pip install -r requirements.txt`
- [ ] Flask server berjalan tanpa error
- [ ] Browser dapat akses `http://localhost:5000`

---

## 🐛 Common Issues & Solutions

### ❌ "ModuleNotFoundError: No module named 'flask'"

**Solusi:**

```bash
pip install -r requirements.txt
```

### ❌ "ConnectionError: Cannot connect to http://localhost:5000"

**Solusi:**

- Pastikan Flask server sudah berjalan
- Check firewall tidak blocking port 5000
- Cek port 5000 dapat diakses: `netstat -an | findstr 5000`

### ❌ "Model not found" di browser

**Solusi:**

- Pastikan notebook sudah dijalankan sampai habis
- Cek folder `models/cnn_lstm/` dan `models/lstm/` ada file `.keras`
- Jalankan ulang cell terakhir di notebook untuk save model

### ❌ "FileNotFoundError: DATASETFIX.xlsx"

**Solusi:**

- Pastikan file `DATASETFIX.xlsx` ada di folder yang sama dengan `app.py`

### ❌ Server crash setelah Run Prediction

**Solusi:**

- Cek TensorFlow terinstall: `pip install tensorflow`
- Restart server dengan ctrl+C lalu jalankan lagi

---

## 📈 Tips Penggunaan

### Untuk Prediksi Akurat:

1. Pilih **CNN-LSTM** (lebih akurat dari LSTM saja)
2. Gunakan **Activation: Auto** dan **Optimizer: Auto**
3. Pilih **Data Period: 24-36 bulan** (data lebih banyak = akurat)
4. Lakukan prediksi untuk **5-10 hari** (lebih pendek = lebih akurat)

### Untuk Eksplorasi:

1. Coba semua 6 saham untuk bandingkan
2. Bandingkan CNN-LSTM vs LSTM dengan parameter sama
3. Lihat perbedaan volatilitas antar saham

### Untuk Research:

1. Simpan screenshot hasil untuk dokumentasi
2. Export data dari tabel untuk analisis lebih lanjut
3. Monitor accuracy metrics (R², MAPE) antar dataset

---

## 🎓 Memahami Model

### CNN-LSTM (Hybrid)

```
Conv1D Layer (Feature Extraction)
        ↓
LSTM Layer (Sequence Learning)
        ↓
Dense Layer (Prediction)
```

**Kelebihan**: Menangkap pola lokal + urutan waktu  
**Cocok untuk**: Data dengan pola kompleks

### LSTM Standalone

```
LSTM Layer (Sequence Learning)
        ↓
Dense Layer (Prediction)
```

**Kelebihan**: Lebih sederhana, training lebih cepat  
**Cocok untuk**: Data dengan pola sederhana

---

## 📞 Perlu Bantuan?

1. **Cek log terminal**: Error message biasanya informatif
2. **Baca README.md**: Dokumentasi lengkap
3. **Check browser console**: F12 → Console untuk JS error

---

## ✨ Selesai!

Selamat! Anda sudah berhasil mengintegrasikan model CNN-LSTM & LSTM!

**Fitur yang sudah siap:**

- ✅ Prediksi real-time dengan 2 model
- ✅ Dashboard interaktif
- ✅ Visualisasi price chart
- ✅ Evaluation metrics
- ✅ API backend

**Selanjutnya:**

- Eksperimen dengan berbagai parameter
- Monitor accuracy untuk setiap ticker
- Mengembangkan strategi trading berdasarkan prediksi

---

**Happy Predicting! 🎯📈**
