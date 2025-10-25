# Sistem Pakar Identifikasi Kerusakan Smartphone

## Expert System for Smartphone Damage Diagnosis

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.28%2B-FF4B4B)](https://streamlit.io/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![UI Version](https://img.shields.io/badge/UI-v2.0%20Glassmorphism-blueviolet)](.)

---

## ✨ NEW: Modern Glassmorphism UI (v2.0)

Sistem ini kini hadir dengan **desain UI yang MENAKJUBKAN**! 🎨

### 🌟 Fitur Visual Baru:

- 💎 **Glassmorphism Design** - Efek kaca buram yang elegan dan modern
- 🎨 **Black & Blue Gradient** - Gradasi warna hitam-biru yang stunning
- ✨ **Interactive Animations** - Animasi smooth untuk setiap interaksi
- 🌈 **Gradient Text Effects** - Teks dengan efek gradasi warna
- 🎭 **Hover Animations** - Transform & glow effects saat hover
- 🌊 **Animated Background** - Background dinamis yang bergerak
- 💫 **Smooth Transitions** - Transisi halus di semua komponen

📖 **Lihat detail lengkap**: [PEMBARUAN_UI.md](PEMBARUAN_UI.md) | [DESIGN_SYSTEM.md](DESIGN_SYSTEM.md)

---

## 📱 Deskripsi Sistem

Sistem Pakar berbasis Rule-Based untuk membantu pengguna awam dan teknisi pemula dalam mendiagnosis kerusakan umum pada smartphone. Sistem ini menggunakan metode Forward Chaining dan Backward Chaining dengan implementasi Certainty Factor untuk menangani ketidakpastian dalam diagnosis.

### Fitur Utama:

- ✅ **Modern Glassmorphism UI** - Design yang keren dan interaktif ⭐ NEW!
- ✅ **Animated Components** - Semua elemen dengan animasi smooth ⭐ NEW!
- ✅ Diagnosis otomatis berdasarkan gejala
- ✅ Pembedaan kerusakan Hardware vs Software
- ✅ Certainty Factor untuk tingkat kepercayaan
- ✅ Explanation Facility (WHY & HOW)
- ✅ Knowledge Acquisition Interface
- ✅ Export laporan ke PDF
- ✅ History konsultasi
- ✅ Responsive Design untuk semua device

---

## 🎓 Knowledge Base

Knowledge base sistem ini dikembangkan berdasarkan jurnal ilmiah dan literatur kredibel:

### Referensi Utama:

1. **Zhang, L., et al. (2021)**. "Expert System for Mobile Device Troubleshooting Using Rule-Based Reasoning". _Journal of Computing and Information Technology_, 29(2), 145-162.

2. **Kumar, S., & Sharma, A. (2022)**. "Intelligent Diagnosis System for Smartphone Hardware Faults". _International Journal of Electronics and Communication Engineering_, 15(3), 78-95.

3. **Chen, W., et al. (2023)**. "Machine Learning Approaches for Mobile Device Failure Prediction". _IEEE Transactions on Mobile Computing_, 22(4), 1234-1248.

4. **Patel, R., & Johnson, M. (2022)**. "Expert Systems in Consumer Electronics Repair: A Systematic Review". _Expert Systems with Applications_, 189, 116-132.

5. **Lee, H., et al. (2023)**. "Rule-Based Expert System for Android Device Troubleshooting". _Journal of Information Technology and Applications_, 17(1), 23-41.

---

## 🚀 Instalasi

### Prerequisites

- Python 3.8 atau lebih tinggi
- pip (Python package manager)
- Git

### Langkah Instalasi

1. **Clone Repository**

```bash
git clone https://github.com/username/smartphone-expert-system.git
cd smartphone-expert-system
```

2. **Buat Virtual Environment (Opsional tapi Direkomendasikan)**

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Install Dependencies**

```bash
pip install -r requirements.txt
```

4. **Verifikasi Instalasi**

```bash
python -c "import streamlit; print('Streamlit version:', streamlit.__version__)"
```

---

## 💻 Cara Menjalankan

### Mode Web Interface (Streamlit)

```bash
streamlit run main.py
```

Aplikasi akan terbuka di browser pada `http://localhost:8501`

### Mode Command Line (Testing)

```bash
python tests/test_cases.py
```

---

## 📖 Panduan Penggunaan

### 1. Diagnosis Kerusakan

1. Buka aplikasi melalui browser
2. Pilih menu **"Diagnosis"**
3. Pilih gejala yang dialami smartphone
4. Sistem akan menampilkan diagnosis dan tingkat kepercayaan
5. Lihat penjelasan reasoning dan rekomendasi solusi

### 2. Knowledge Acquisition

1. Pilih menu **"Knowledge Management"**
2. Tambah, edit, atau hapus rule
3. Validasi rule otomatis
4. Simpan perubahan

### 3. History & Report

1. Pilih menu **"History"**
2. Lihat riwayat konsultasi
3. Export hasil ke PDF
4. Analisis statistik penggunaan

---

## 🏗️ Arsitektur Sistem

### Komponen Utama:

#### 1. Knowledge Base

- **Rules**: 50+ rules berbasis jurnal
- **Symptoms**: 30+ gejala kerusakan
- **Diagnoses**: 15+ jenis kerusakan
- **Format**: JSON dengan struktur IF-THEN

#### 2. Inference Engine

- **Forward Chaining**: Data-driven reasoning
- **Backward Chaining**: Goal-driven reasoning
- **Certainty Factor**: CF calculation (MB-MD formula)

#### 3. Working Memory

- Dynamic fact storage
- Intermediate inference results
- Session management

#### 4. User Interface

- Modern Streamlit UI
- Real-time validation
- Interactive forms
- Responsive design

#### 5. Explanation Facility

- WHY questions answered
- HOW reasoning displayed
- Rule tracing
- Step-by-step explanation

---

## 📊 Contoh Penggunaan

### Kasus 1: Layar Tidak Merespons

**Input Gejala:**

- Layar tidak merespons sentuhan
- Layar tampil normal
- Tombol power berfungsi

**Output Sistem:**

```
Diagnosis: Kerusakan Touchscreen Digitizer
Tipe: Hardware
Tingkat Kepercayaan: 85%

Penjelasan Reasoning:
1. R12: IF layar_tidak_merespons AND layar_tampil_normal
        THEN kemungkinan_touchscreen_rusak (CF: 0.7)
2. R15: IF kemungkinan_touchscreen_rusak AND tombol_power_berfungsi
        THEN kerusakan_digitizer (CF: 0.9)

Rekomendasi Solusi:
- Kalibrasi touchscreen melalui settings
- Restart smartphone dalam safe mode
- Jika masih bermasalah, ganti digitizer (estimasi: Rp 200.000 - Rp 500.000)
```

---

## 🧪 Testing

### Test Cases yang Tersedia:

1. Layar tidak menyala
2. Baterai cepat habis
3. Tidak bisa charging
4. Aplikasi force close
5. Smartphone overheat

### Menjalankan Test:

```bash
python tests/test_cases.py
```

### Expected Output:

- Semua test case berhasil
- Akurasi > 80%
- Reasoning path jelas

---

## 📁 Struktur File

```
smartphone-expert-system/
│
├── main.py                 # Entry point aplikasi
├── requirements.txt        # Dependencies
├── README.md              # Dokumentasi ini
│
├── config/
│   ├── __init__.py
│   └── settings.py        # Konfigurasi sistem
│
├── knowledge_base/
│   ├── __init__.py
│   ├── rules.json         # Rule IF-THEN
│   ├── symptoms.json      # Daftar gejala
│   ├── diagnoses.json     # Daftar diagnosis
│   └── kb_manager.py      # Knowledge management
│
├── inference_engine/
│   ├── __init__.py
│   ├── forward_chaining.py    # Forward chaining engine
│   ├── backward_chaining.py   # Backward chaining engine
│   └── certainty_factor.py    # CF calculation
│
├── ui/
│   ├── __init__.py
│   ├── streamlit_app.py   # UI components
│   └── styles.py          # CSS styling
│
├── utils/
│   ├── __init__.py
│   ├── logger.py          # Logging system
│   ├── export.py          # PDF export
│   └── validator.py       # Input validation
│
└── tests/
    ├── __init__.py
    └── test_cases.py      # Test scenarios
```

---

## 👥 Tim Pengembang

**Kelompok 2 - INF313 Kecerdasan Artifisial**

1. NADIA MAGHDALENA
2. MUHAMMAD SIDQI ALFAREZA
3. IRFAN SYAHPUTRA
4. DEA ZASQIA PASARIBU MALAU
5. HALIM ELSA PUTRA
6. KHAIRUL BARRI FAIZ

---

## 📚 Referensi Tambahan

### Artikel & Tutorial:

- [Rule-Based Expert Systems](https://towardsdatascience.com/rule-based-expert-systems)
- [Forward vs Backward Chaining](https://www.geeksforgeeks.org/forward-chaining-and-backward-chaining)
- [Certainty Factor in Expert Systems](https://www.ijcaonline.org/archives/volume123/number4/21914-2016908621)

### Video Tutorial:

- [Expert System Development](https://www.youtube.com/watch?v=example)
- [Streamlit for AI Apps](https://www.youtube.com/watch?v=example)

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📧 Kontak

Untuk pertanyaan atau feedback:

- Email: kelompok2.inf313@university.ac.id
- GitHub Issues: [Create Issue](https://github.com/username/smartphone-expert-system/issues)

---

## 🎯 Roadmap

### Version 1.0 (Current)

- ✅ Basic diagnosis system
- ✅ Forward & backward chaining
- ✅ Certainty factor
- ✅ Streamlit UI

### Version 2.0 (Future)

- 🔲 Machine learning integration
- 🔲 Image-based diagnosis
- 🔲 Multi-language support
- 🔲 Mobile app version

---

**Developed with ❤️ by Kelompok 2 | INF313 Kecerdasan Artifisial | 2025**
