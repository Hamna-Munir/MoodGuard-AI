# 🧠 MoodGuard · AI Mental Health Monitor

> **Real-time emotion detection powered by deep learning and computer vision — analyze facial expressions through photos or live webcam using AI.**

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.x-000000?style=flat-square&logo=flask&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.10-FF6F00?style=flat-square&logo=tensorflow&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-5C3EE8?style=flat-square&logo=opencv&logoColor=white)
![Keras](https://img.shields.io/badge/Keras-DeepLearning-D00000?style=flat-square&logo=keras&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## 📌 Overview

**MoodGuard** is an AI-powered emotion recognition and mental health monitoring web application that uses **Convolutional Neural Networks (CNN)** and **computer vision** to detect facial emotions in real time.

The system can analyze **uploaded images**, **captured photos**, and **live webcam feeds** to predict emotional states such as happiness, sadness, anger, fear, surprise, disgust, and neutrality.

It is designed with a **privacy-first local AI approach**, meaning no facial data is sent to any external server.

| Metric | Value |
|---|---|
| 🎯 Model Accuracy | **66.6%** |
| 🖼️ Training Images | **35,000+** |
| 😄 Emotion Classes | **7** |
| 🧠 Model Type | **CNN** |
| 📦 Dataset | **FER2013** |
| 🔒 Privacy | **100% Local Processing** |

---

## ✨ Features

### 📸 Photo Analysis
Upload facial images and instantly detect emotional state with AI-powered prediction.

### 🎥 Live Webcam Detection
Real-time emotion detection through webcam feed.

### 📊 Emotion Prediction Dashboard
Clean and interactive dashboard UI built with HTML, CSS, and JavaScript.

### 🕒 Detection History
Can track and display previous analysis sessions.

### 🔒 Privacy First
All processing happens locally. No cloud upload. No external APIs.

### ⚡ Fast AI Inference
TensorFlow model loaded directly in Flask for fast prediction.

### 🧠 Deep Learning Model
CNN trained on FER2013 facial expression dataset.

---

## 🛠️ Technology Stack

| Technology | Role |
|---|---|
| 🐍 Python 3.10 | Core language |
| 🌐 Flask | Backend web framework |
| 🤖 TensorFlow / Keras | CNN model loading & prediction |
| 📷 OpenCV | Face detection & image preprocessing |
| 🔢 NumPy | Numerical computation |
| 🖼️ Pillow | Image handling |
| 🎨 HTML / CSS / JS | Frontend dashboard |
| 📦 H5Py | Loading `.h5` trained model |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Webcam (for video detection)
- `moodguard_model.h5`

---

## Installation

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/MoodGuard.git
cd MoodGuard
```

### 2. Create Virtual Environment
```bash
python -m venv venv
```

### Windows
```bash
venv\Scripts\activate
```

### Mac/Linux
```bash
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Add Model File
Place:

```bash
moodguard_model.h5
```

inside project root directory.

---

## ▶ Run Project

```bash
python app.py
```

Open browser:

```bash
http://127.0.0.1:5000
```

---

## 📦 Requirements

```txt
Flask==3.0.3
tensorflow==2.10.0
opencv-python==4.10.0.84
numpy==1.23.5
Pillow==10.4.0
h5py==3.11.0
gunicorn==22.0.0
```

Install:
```bash
pip install -r requirements.txt
```

---

## 🔬 Detection Pipeline

```text
Input Image / Webcam
        │
        ▼
┌────────────────────────┐
│ 1. Image Capture       │
│ Photo Upload / Webcam  │
└────────────┬───────────┘
             │
             ▼
┌────────────────────────┐
│ 2. Face Detection      │
│ OpenCV Haar Cascade    │
└────────────┬───────────┘
             │
             ▼
┌────────────────────────┐
│ 3. Preprocessing       │
│ Resize + Normalize     │
└────────────┬───────────┘
             │
             ▼
┌────────────────────────┐
│ 4. CNN Prediction      │
│ TensorFlow / Keras     │
└────────────┬───────────┘
             │
             ▼
┌────────────────────────┐
│ 5. Emotion Output      │
│ UI + Prediction Result │
└────────────────────────┘
```

---

## 😄 Supported Emotions

MoodGuard detects 7 emotions:

- Happy 😊
- Sad 😢
- Angry 😠
- Fear 😨
- Surprise 😲
- Neutral 😐
- Disgust 😖

---

## 🧠 Model Details

| Property | Value |
|---|---|
| Model | CNN |
| Framework | TensorFlow / Keras |
| Dataset | FER2013 |
| Classes | 7 Emotions |
| Training Images | 35K+ |
| Format | `.h5` |
| Input | Facial Expressions |

---

## 📁 Project Structure

```bash
MoodGuard/
│
├── app.py
├── detect_emotion.py
├── prepare_dataset.py
├── train_model.py
├── moodguard_model.h5
├── requirements.txt
├── README.md
├── .gitignore
│
├── templates/
│   └── index.html
│
└── static/
    ├── style.css
    └── script.js
```

---

## 🖥️ App Sections

| Section | Description |
|---|---|
| 📸 Photo Analysis | Upload image → detect emotion |
| 🎥 Video Detection | Real-time webcam prediction |
| 📜 History | Previous detections |
| ℹ️ About | System overview |

---

## ⚠️ Troubleshooting

### Model file not found
Place `moodguard_model.h5` in root directory.

### Camera not opening
Check OS/browser camera permissions.

### No face detected
Use a clear front-facing image.

### Slow prediction
Close other heavy applications.

### TensorFlow install issue
Use Python 3.10 (recommended).

---

## 🗺️ Roadmap

- [ ] Mood trend analysis
- [ ] PDF reports
- [ ] Session analytics
- [ ] Database support
- [ ] Dark mode
- [ ] Login system
- [ ] Voice emotion detection
- [ ] AI chatbot integration
- [ ] Docker deployment

---

## 👩‍💻 About Creator

**Hamna Munir**  
AI/ML Engineer • Software Engineering Student

Built MoodGuard as an end-to-end AI project combining:

- Deep Learning
- CNN Architecture
- Computer Vision
- Flask Deployment
- Frontend + Backend Integration
- Real-time AI Prediction

This project demonstrates a complete machine learning workflow from preprocessing → model training → deployment.

---

## 📄 License

Licensed under **MIT License**.

---

## 🙏 Acknowledgements

- FER2013 Dataset
- TensorFlow
- OpenCV
- Flask
- Keras
- Open-source AI/ML community

---

<div align="center">
  <strong>MoodGuard · v1.0</strong><br/>
  Built with ❤️ by <strong>Hamna Munir</strong> · Python · Flask · OpenCV · TensorFlow · CNN
</div>
