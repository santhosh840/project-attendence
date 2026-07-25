# AgriAI: AI-Based Personal Agriculture Officer

> **24/7 Multilingual Smart Farming Assistant Using Computer Vision, Deep Learning, Generative AI, Voice AI, GPS, and Recommendation Systems.**

---

## 🌟 Overview

**AgriAI** acts as a 24/7 virtual agricultural extension officer for farmers. It integrates Computer Vision, Deep Learning, Generative AI, Multilingual Voice AI (Kannada, Telugu, Hindi, English), GPS Geolocation Dealer Search, Live Fertilizer Market Pricing, Government Subsidy Calculations, Daily Farm Logbook, and Agricultural Expert Consultation into one intelligent platform.

---

## 📂 Project Directory Structure

```
c:/Users/ADMIN/Documents/project attendence/
├── app.py                      # Flask REST API Server & Route Controllers
├── models.py                   # SQLAlchemy Database Models (Farmer, Farm, Diagnosis, Dealers, Experts, Logbook)
├── ai_engine.py                # Computer Vision Classifier, Multi-Stage AI Validator, Crop Variety & Calendar Engine
├── agri_ai.db                  # SQLite Master Database
├── launch_agri_ai.bat          # 24/7 Auto-Restart Server Launcher Script
├── launch_agri_ai_silent.vbs   # Silent Background Launcher (No command window pop-up)
├── create_desktop_shortcut.py  # Python script to generate Desktop Shortcut icon
├── requirements.txt            # Python Dependencies List
│
├── templates/
│   └── index.html              # Main Single Page Web App (Light Mode Glassmorphic Dashboard)
│
└── static/
    ├── css/
    │   └── styles.css          # Modern Light Mode Agricultural CSS Design System
    ├── js/
    │   └── app.js              # Client Application Engine (Speech STT/TTS, Leaflet Maps, Date Pickers, Crop Roadmap)
    └── uploads/                # User Plant Image Upload Directory
```

---

## 🚀 24/7 Desktop App & Standalone Launch Instructions

### 1. Launching from Desktop Shortcut Icon (Recommended)
Double-click the **"AgriAI Agriculture Officer"** icon located on your Windows Desktop (`C:\Users\ADMIN\Desktop`).
- It silently starts the AgriAI server in the background.
- It automatically opens `http://127.0.0.1:5000` in your default web browser.
- It runs **24/7** independently even when Antigravity or command line sessions are closed!

### 2. Manual Terminal Launch
To run manually from command prompt:
```cmd
cd "c:\Users\ADMIN\Documents\project attendence"
launch_agri_ai.bat
```

---

## 📡 REST API Reference

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/` | `GET` | Renders Light Mode Web Application Dashboard |
| `/api/auth/otp/send` | `POST` | Generates & sends simulated 6-digit SMS OTP |
| `/api/auth/otp/verify` | `POST` | Verifies OTP and logs in / registers farmer account |
| `/api/auth/profile` | `GET / POST` | Retrieves & updates farmer profile details (Name, Phone, Location) |
| `/api/crop-guide/<crop_name>` | `GET` | Returns calendar-mapped day-by-day lifecycle roadmap based on variety and sowing date |
| `/api/dashboard/date-guidance` | `GET` | Returns daily tasks, fertigation, and water metrics for selected calendar date |
| `/api/diagnose` | `POST` | Multi-stage AI plant image upload & computer vision disease classification |
| `/api/dealers` | `GET` | Acquires GPS coordinates and returns nearby authorized fertilizer dealers sorted by distance (km) |
| `/api/experts` | `GET` | Returns nearby agricultural extension officers and KVK scientists with appointment booking |
| `/api/fertilizers` | `GET` | Returns fertilizer catalog with live market prices & government DBT subsidy savings |
| `/api/logbook` | `GET / POST` | Retrieves & logs daily farm activities, expenses, and harvests |
| `/api/chat` | `POST` | Generative AI Agriculture Officer ("Krishi Mitra") chatbot |

---

## 📱 Supported Languages (Voice AI)
- **English (en)**
- **Kannada (kn - ಕನ್ನಡ)**
- **Telugu (te - తెలుగు)**
- **Hindi (hi - हिंदी)**

---

## 🔧 Technical Stack
- **Backend Framework**: Python Flask, SQLAlchemy, SQLite
- **AI & Computer Vision**: PyTorch/TensorFlow deep learning simulator, OpenCV visual metrics, Multi-Stage Ensemble Validator
- **Geospatial & GPS**: Leaflet.js, OpenStreetMap, Browser HTML5 Geolocation API, Haversine Distance Engine
- **Voice AI Engine**: Web Speech API (SpeechRecognition & SpeechSynthesis)
- **UI Design System**: Vanilla JavaScript ES6+, HTML5, Custom CSS3 Light Mode Glassmorphic Design System
