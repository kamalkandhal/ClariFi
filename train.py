import os
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint
from utils.preprocess import extract_features

# Config
CLEAN_DIR = "dataset/clean"
NOISY_DIR = "dataset/noisy"
MODEL_PATH = "models/frame_model.keras"
NORM_PATH = "models/norm.pkl"
os.makedirs("models", exist_ok=True)

print("🔁 Collecting feature data...")
X = []
y = []

for fname in os.listdir(NOISY_DIR):
    if fname.endswith(".wav"):
        noisy_path = os.path.join(NOISY_DIR, fname)
        clean_path = os.path.join(CLEAN_DIR, fname)

        noisy_feats, _, _ = extract_features(noisy_path)
        clean_feats, _, _ = extract_features(clean_path)

        if noisy_feats.shape == clean_feats.shape:
            X.append(noisy_feats)
            y.append(clean_feats)

X = np.vstack(X)
y = np.vstack(y)
print(f"✅ Loaded {X.shape[0]} training frames")

# Normalization
mean = np.mean(X, axis=0)
std = np.std(X, axis=0) + 1e-10
X_norm = (X - mean) / std
y_norm = (y - mean) / std

# Save mean and std for inference
with open(NORM_PATH, 'wb') as f:
    pickle.dump({'mean': mean, 'std': std}, f)
print("✅ Saved normalization stats")

# Split
X_train, X_val, y_train, y_val = train_test_split(X_norm, y_norm, test_size=0.1, random_state=42)

# Model
model = Sequential([
    Dense(256, activation='relu', input_shape=(X.shape[1],)),
    Dropout(0.3),
    Dense(128, activation='relu'),
    Dropout(0.3),
    Dense(X.shape[1])
])
model.compile(optimizer=Adam(1e-3), loss='mse')

# Training
checkpoint = ModelCheckpoint(MODEL_PATH, save_best_only=True, monitor='val_loss', mode='min')
print("🚀 Training model...")
history = model.fit(
    X_train, y_train,
    validation_data=(X_val, y_val),
    batch_size=128,
    epochs=30,
    callbacks=[checkpoint]
)
print("✅ Training complete. Model saved at:", MODEL_PATH)
