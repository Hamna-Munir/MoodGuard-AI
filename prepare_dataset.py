import pandas as pd
import numpy as np
import cv2
import os

print("Converting FER2013 CSV to image folders...")

# ── Load CSV ───────────────────────────────────────────────────────────────────
df = pd.read_csv("fer2013/fer2013/fer2013.csv")
print(f"Total rows: {len(df)}")

# ── Emotion labels ─────────────────────────────────────────────────────────────
EMOTIONS = {
    0: 'angry',
    1: 'disgust',
    2: 'fear',
    3: 'happy',
    4: 'sad',
    5: 'surprise',
    6: 'neutral'
}

# ── Create folders ─────────────────────────────────────────────────────────────
for split in ['train', 'test']:
    for emotion in EMOTIONS.values():
        os.makedirs(f"dataset/{split}/{emotion}", exist_ok=True)

print("Folders created!")

# ── Convert each row to image ──────────────────────────────────────────────────
train_count = 0
test_count  = 0

for idx, row in df.iterrows():
    emotion_label = EMOTIONS[row['emotion']]
    pixels        = np.array(row['pixels'].split(), dtype=np.uint8)
    image         = pixels.reshape(48, 48)

    # Usage column tells us train or test
    usage = row['Usage']
    if usage == 'Training':
        split = 'train'
        train_count += 1
    else:
        split = 'test'
        test_count += 1

    path = f"dataset/{split}/{emotion_label}/{idx}.jpg"
    cv2.imwrite(path, image)

    if idx % 1000 == 0:
        print(f"Processed {idx} images...")

print(f"\nDone!")
print(f"Training images : {train_count}")
print(f"Testing images  : {test_count}")
print(f"Total           : {train_count + test_count}")
print(f"\nDataset ready at: dataset/train/ and dataset/test/")