import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import tensorflow as tf
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

print("TensorFlow version:", tf.__version__)
print("Starting MoodGuard training on Python 3.10...")

TRAIN_DIR = "dataset/train"
TEST_DIR  = "dataset/test"
IMG_SIZE  = 48
BATCH     = 64
EPOCHS    = 50

EMOTIONS = ['angry','disgust','fear','happy','sad','surprise','neutral']

train_gen = tf.keras.preprocessing.image.ImageDataGenerator(
    rescale=1./255,
    rotation_range=10,
    horizontal_flip=True,
    zoom_range=0.1,
    width_shift_range=0.1,
    height_shift_range=0.1
)
test_gen = tf.keras.preprocessing.image.ImageDataGenerator(
    rescale=1./255
)

train_data = train_gen.flow_from_directory(
    TRAIN_DIR,
    target_size=(IMG_SIZE, IMG_SIZE),
    color_mode='grayscale',
    batch_size=BATCH,
    class_mode='categorical',
    shuffle=True
)
test_data = test_gen.flow_from_directory(
    TEST_DIR,
    target_size=(IMG_SIZE, IMG_SIZE),
    color_mode='grayscale',
    batch_size=BATCH,
    class_mode='categorical',
    shuffle=False
)

print(f"Training samples : {train_data.samples}")
print(f"Testing samples  : {test_data.samples}")

model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(32,(3,3),activation='relu',
                           padding='same',
                           input_shape=(IMG_SIZE,IMG_SIZE,1)),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.Conv2D(32,(3,3),activation='relu',padding='same'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Dropout(0.25),

    tf.keras.layers.Conv2D(64,(3,3),activation='relu',padding='same'),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.Conv2D(64,(3,3),activation='relu',padding='same'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Dropout(0.25),

    tf.keras.layers.Conv2D(128,(3,3),activation='relu',padding='same'),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.Conv2D(128,(3,3),activation='relu',padding='same'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Dropout(0.25),

    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(256,activation='relu'),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(128,activation='relu'),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(7,activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

model.summary()

checkpoint = tf.keras.callbacks.ModelCheckpoint(
    'moodguard_model.h5',
    monitor='val_accuracy',
    save_best_only=True,
    verbose=1
)
early_stop = tf.keras.callbacks.EarlyStopping(
    monitor='val_accuracy',
    patience=10,
    restore_best_weights=True,
    verbose=1
)

print("\nTraining started — takes 20-40 minutes...")
print("Go make tea and come back!\n")

history = model.fit(
    train_data,
    epochs=EPOCHS,
    validation_data=test_data,
    callbacks=[checkpoint, early_stop]
)

final_acc = max(history.history['val_accuracy'])
print(f"\n{'='*40}")
print(f"Training complete!")
print(f"Best accuracy: {final_acc*100:.1f}%")
print(f"Model saved: moodguard_model.h5")
print(f"{'='*40}")

fig, (ax1,ax2) = plt.subplots(1,2,figsize=(12,4))
ax1.plot(history.history['accuracy'],    label='Train',color='#2DD4BF')
ax1.plot(history.history['val_accuracy'],label='Test', color='#F87171')
ax1.set_title('Accuracy'); ax1.legend()
ax2.plot(history.history['loss'],        label='Train',color='#2DD4BF')
ax2.plot(history.history['val_loss'],    label='Test', color='#F87171')
ax2.set_title('Loss'); ax2.legend()
plt.tight_layout()
plt.savefig('training_results.png',dpi=150)
print("Chart saved!")