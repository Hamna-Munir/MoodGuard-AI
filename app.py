import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
import tensorflow as tf
import base64
import io
from datetime import datetime

app   = Flask(__name__)
model = tf.keras.models.load_model("moodguard_model.h5", compile=False)

EMOTIONS = ['Angry','Disgust','Fear','Happy','Sad','Surprise','Neutral']
STRESS_EMOTIONS   = ['Angry','Fear','Disgust','Sad']
POSITIVE_EMOTIONS = ['Happy','Surprise']

EMOTION_COLORS = {
    'Angry':   '#E040A0','Disgust':'#00CC44','Fear':'#8B5CF6',
    'Happy':   '#7B3FF2','Sad':    '#06B6D4','Surprise':'#F59E0B',
    'Neutral': '#9B7EC8'
}
EMOTION_EMOJIS = {
    'Angry':'😠','Disgust':'🤢','Fear':'😨',
    'Happy':'😊','Sad':'😢','Surprise':'😲','Neutral':'😐'
}
MENTAL_HEALTH_TIPS = {
    'Angry':   ["Take 10 deep breaths — inhale 4 sec, exhale 6 sec",
                "Step away from the screen for 5 minutes",
                "Drink a glass of cold water slowly"],
    'Fear':    ["Ground yourself: name 5 things you can see",
                "You are safe. Focus on your breathing.",
                "Try the 4-7-8 breathing technique"],
    'Disgust': ["Take a short walk outside",
                "Listen to your favorite calming music",
                "Shift focus to something you enjoy"],
    'Sad':     ["It is okay to feel sad. Be kind to yourself.",
                "Reach out to someone you trust",
                "Write 3 things you are grateful for today"],
    'Happy':   ["Great energy! This is a perfect time to focus on your goals.",
                "Channel this positivity into your work and creative tasks!",
                "Share your good mood with someone around you today."],
    'Surprise':["Take a moment to process what surprised you",
                "Breathe steadily and re-center yourself",
                "Curiosity is great — explore what caught your attention"],
    'Neutral': ["Steady state — great focus conditions",
                "Perfect time to tackle difficult tasks",
                "Stay hydrated and maintain good posture"]
}

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

session_history = []

def predict_emotion(face_img):
    gray    = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, (48, 48))
    norm    = resized.astype('float32') / 255.0
    inp     = norm.reshape(1, 48, 48, 1)
    preds   = model.predict(inp, verbose=0)[0]
    idx     = np.argmax(preds)
    return EMOTIONS[idx], float(preds[idx]) * 100, preds

def img_to_base64(img_bgr):
    _, buf = cv2.imencode('.jpg', img_bgr)
    return base64.b64encode(buf).decode('utf-8')

def get_wellness(history):
    if not history:
        return 50
    pos = sum(1 for h in history if h['emotion'] in POSITIVE_EMOTIONS)
    neg = sum(1 for h in history if h['emotion'] in STRESS_EMOTIONS)
    return max(0, min(100, round(((pos - neg*0.5) / len(history) * 100) + 50, 1)))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    file      = request.files['photo']
    np_img    = np.frombuffer(file.read(), np.uint8)
    img_bgr   = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    gray  = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=5, minSize=(48,48))

    if len(faces) == 0:
        return jsonify({'error': 'No face detected'})

    fx, fy, fw, fh = faces[0]
    face           = img_bgr[fy:fy+fh, fx:fx+fw]
    emotion, conf, preds = predict_emotion(face)

    result = img_bgr.copy()
    cv2.rectangle(result, (fx,fy), (fx+fw,fy+fh), (123,63,242), 2)
    lbl = f"{emotion} {conf:.0f}%"
    cv2.rectangle(result, (fx, fy-30), (fx+len(lbl)*11, fy), (123,63,242), -1)
    cv2.putText(result, lbl, (fx+4, fy-8),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)

    entry = {
        'time':    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'emotion': emotion,
        'conf':    round(conf, 1),
        'color':   EMOTION_COLORS.get(emotion,'#7B3FF2'),
        'emoji':   EMOTION_EMOJIS.get(emotion,'😐')
    }
    session_history.append(entry)

    wellness = get_wellness(session_history)
    stress   = round(sum(1 for h in session_history
                         if h['emotion'] in STRESS_EMOTIONS)
                     / len(session_history) * 100, 1)
    positive = round(sum(1 for h in session_history
                         if h['emotion'] in POSITIVE_EMOTIONS)
                     / len(session_history) * 100, 1)
    dominant = max(set(h['emotion'] for h in session_history),
                   key=lambda e: sum(1 for h in session_history
                                     if h['emotion'] == e))

    return jsonify({
        'emotion':      emotion,
        'conf':         round(conf, 1),
        'color':        EMOTION_COLORS.get(emotion, '#7B3FF2'),
        'emoji':        EMOTION_EMOJIS.get(emotion, '😐'),
        'tips':         MENTAL_HEALTH_TIPS.get(emotion, []),
        'probs':        {e: round(float(p)*100, 1)
                         for e, p in zip(EMOTIONS, preds)},
        'colors':       EMOTION_COLORS,
        'result_img':   img_to_base64(result),
        'wellness':     wellness,
        'stress':       stress,
        'positive':     positive,
        'dominant':     dominant,
        'dominant_emoji': EMOTION_EMOJIS.get(dominant, '😐'),
        'dominant_color': EMOTION_COLORS.get(dominant, '#7B3FF2'),
    })

@app.route('/history')
def get_history():
    return jsonify(session_history)

@app.route('/clear_history', methods=['POST'])
def clear_history():
    session_history.clear()
    return jsonify({'ok': True})

if __name__ == '__main__':
    app.run(debug=True, port=5000)