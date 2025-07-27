
# 💬 Muro AI - Chatbot dengan FastAPI + React + Ollama

Muro AI adalah chatbot modern yang dibangun menggunakan **React.js** untuk frontend, **FastAPI** untuk backend, dan **Ollama** sebagai LLM engine. Proyek ini dirancang agar mudah dijalankan secara lokal untuk praktikum di Laboratorium Robotika,Universitas Gundarma.

---

## 📦 Fitur

- ✅ UI responsif dan modern dengan React
- ✅ Interaksi real-time dengan indikator pengetikan
- ✅ Integrasi dengan Ollama secara lokal
- ✅ Dukungan CORS antara frontend dan backend

---

## 🧠 Arsitektur

Frontend (React) --> FastAPI (Backend) --> Ollama (LLM Engine)

---

## 🚀 Cara Menjalankan

### 1. Clone Repositori
```bash
git clone https://github.com/noperi11/Muro.ai.git
cd Muro.ai
````

### 2. Jalankan Backend (FastAPI)

Pastikan Anda sudah menginstal Python 3.9+ dan `pip`.

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

> 📍 Pastikan Ollama sudah aktif dan model `deepseek-coder-v2:16b` telah di-pull:

```bash
ollama run deepseek-coder-v2:16b
```

### 3. Jalankan Frontend (React)

Buka terminal lain:

```bash
cd frontend
npm install
npm start
```

React akan berjalan di `http://localhost:3000`

---

## ⚙️ Konfigurasi Penting

* **Backend Endpoint:** `http://localhost:8000/chat`
* **Frontend Config:** Sudah menggunakan endpoint lokal di React
* **CORS:** Diaktifkan hanya untuk `http://localhost:3000`

---

## 🧠 Tentang Model

Proyek ini menggunakan model `deepseek-coder-v2:16b` dari [Ollama](https://ollama.com/), yang dapat berjalan secara lokal tanpa koneksi internet.

---

## 🤝 Kontribusi

Pull request dan ide baru sangat diterima! Silakan buka issue jika ada bug atau request fitur.

---
