import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model

print("Loading MoodGuard model...")

model = load_model("moodguard_model.h5", compile=False)
print("Model loaded!")

# ── 7 emotions with colors and emojis ─────────────────────────────────────────
EMOTIONS = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

COLORS = {
    'Angry':    (0,   0,   255),
    'Disgust':  (0,   128, 0  ),
    'Fear':     (128, 0,   128),
    'Happy':    (0,   255, 0  ),
    'Sad':      (255, 0,   0  ),
    'Surprise': (0,   165, 255),
    'Neutral':  (200, 200, 200)
}

EMOJIS = {
    'Angry':    '😠',
    'Disgust':  '🤢',
    'Fear':     '😨',
    'Happy':    '😊',
    'Sad':      '😢',
    'Surprise': '😲',
    'Neutral':  '😐'
}

# ── Stress emotions ────────────────────────────────────────────────────────────
STRESS_EMOTIONS = ['Angry', 'Fear', 'Disgust', 'Sad']

# ── Load face detector ─────────────────────────────────────────────────────────
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

def predict_emotion(face_img):
    gray    = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, (48, 48))
    norm    = resized / 255.0
    inp     = norm.reshape(1, 48, 48, 1)
    preds   = model.predict(inp, verbose=0)[0]
    idx     = np.argmax(preds)
    return EMOTIONS[idx], float(preds[idx]) * 100, preds

def calculate_stress(preds):
    stress_indices = [EMOTIONS.index(e) for e in STRESS_EMOTIONS]
    stress = sum(preds[i] for i in stress_indices) * 100
    return min(round(stress, 1), 100)

def draw_emotion_bar(frame, preds, x, y):
    bar_w = 120
    for i, (emotion, prob) in enumerate(zip(EMOTIONS, preds)):
        bar_h   = int(prob * 60)
        color   = COLORS[emotion]
        bar_x   = x + i * 18
        bar_y_b = y
        cv2.rectangle(frame,
                      (bar_x, bar_y_b - bar_h),
                      (bar_x + 14, bar_y_b),
                      color, -1)
        cv2.rectangle(frame,
                      (bar_x, bar_y_b - 60),
                      (bar_x + 14, bar_y_b),
                      (50,50,50), 1)

# ── Session tracking ───────────────────────────────────────────────────────────
emotion_history = []
frame_count     = 0

cap = cv2.VideoCapture(0)
print("MoodGuard running! Press Q to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame      = cv2.flip(frame, 1)
    h, w       = frame.shape[:2]
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_count += 1

    # ── Detect faces ──────────────────────────────────────────────────────────
    faces = face_cascade.detectMultiScale(
        gray_frame, scaleFactor=1.1,
        minNeighbors=5, minSize=(48, 48)
    )

    dominant_emotion = "Neutral"
    stress_score     = 0

    for (fx, fy, fw, fh) in faces:
        face_img = frame[fy:fy+fh, fx:fx+fw]
        emotion, confidence, preds = predict_emotion(face_img)
        stress_score = calculate_stress(preds)
        dominant_emotion = emotion
        emotion_history.append(emotion)

        color = COLORS[emotion]

        # Face rectangle
        cv2.rectangle(frame, (fx, fy), (fx+fw, fy+fh), color, 2)

        # Emotion label box
        label   = f"{emotion} {confidence:.0f}%"
        (lw,lh),_ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
        cv2.rectangle(frame,
                      (fx, fy - lh - 12),
                      (fx + lw + 8, fy),
                      color, -1)
        cv2.putText(frame, label,
                    (fx + 4, fy - 6),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                    (255,255,255), 2)

        # Emotion bars
        if fy + fh + 80 < h:
            draw_emotion_bar(frame, preds, fx, fy + fh + 70)

    # ── Top HUD ───────────────────────────────────────────────────────────────
    cv2.rectangle(frame, (0,0), (w, 55), (10,15,25), -1)
    cv2.rectangle(frame, (0,0), (w, 55), (30,45,70), 1)

    # Project name
    cv2.putText(frame, "MoodGuard",
                (12, 32),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                (45,212,191), 2)

    # Current emotion
    cv2.putText(frame, f"Emotion: {dominant_emotion}",
                (160, 32),
                cv2.FONT_HERSHEY_SIMPLEX, 0.65,
                COLORS.get(dominant_emotion,(200,200,200)), 2)

    # Stress score with color
    stress_color = (0,255,0) if stress_score < 30 else \
                   (0,165,255) if stress_score < 60 else \
                   (0,0,255)
    cv2.putText(frame, f"Stress: {stress_score:.0f}%",
                (w - 180, 32),
                cv2.FONT_HERSHEY_SIMPLEX, 0.65,
                stress_color, 2)

    # ── Bottom stats ──────────────────────────────────────────────────────────
    cv2.rectangle(frame, (0, h-45), (w, h), (10,15,25), -1)

    if len(faces) == 0:
        cv2.putText(frame, "No face detected — move closer",
                    (12, h-15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (100,100,100), 1)
    else:
        # Mood summary from history
        if len(emotion_history) > 10:
            recent   = emotion_history[-30:]
            most_common = max(set(recent), key=recent.count)
            pct      = recent.count(most_common) / len(recent) * 100
            cv2.putText(frame,
                        f"Dominant mood: {most_common} ({pct:.0f}%)",
                        (12, h-15),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (180,180,180), 1)

        cv2.putText(frame, f"Frames: {frame_count}",
                    (w-130, h-15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45,
                    (80,80,80), 1)

    cv2.imshow("MoodGuard — AI Emotion Detector", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# ── Session summary ───────────────────────────────────────────────────────────
if emotion_history:
    print("\n" + "="*45)
    print("SESSION SUMMARY")
    print("="*45)
    total = len(emotion_history)
    print(f"Total detections: {total}")
    print()
    for e in EMOTIONS:
        count = emotion_history.count(e)
        pct   = count / total * 100
        bar   = "█" * int(pct / 5)
        print(f"{e:10} {bar:20} {pct:5.1f}%")
    print()
    dominant = max(set(emotion_history), key=emotion_history.count)
    print(f"Your dominant mood: {dominant} {EMOJIS[dominant]}")
    stress_count = sum(emotion_history.count(e) for e in STRESS_EMOTIONS)
    overall_stress = stress_count / total * 100
    print(f"Overall stress level: {overall_stress:.1f}%")
    if overall_stress > 50:
        print("💡 Tip: You seemed stressed. Try deep breathing.")
    elif overall_stress > 30:
        print("💡 Tip: Moderate stress detected. Take a short break.")
    else:
        print("✅ Great session! You stayed mostly calm.")
    print("="*45)