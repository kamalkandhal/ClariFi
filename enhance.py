import os
import librosa
import numpy as np
import soundfile as sf
import pickle

from tensorflow.keras.models import load_model
from utils.preprocess import extract_features
from utils.audio_utils import apply_istft, butter_lowpass_filter, HOP_LENGTH, SR

MODEL_PATH = "models/frame_model.keras"
NORM_PATH = "models/norm.pkl"

# ✅ Load model and normalization once
print("🔁 Loading model and normalization data...")
model = load_model(MODEL_PATH, compile=False)
with open(NORM_PATH, 'rb') as f:
    norm_data = pickle.load(f)
mean = norm_data['mean']
std = norm_data['std']

def enhance_audio(noisy_file, output_path="static/enhanced/enhanced.wav"):
    # Extract features
    noisy_feats, y_noisy, stft_noisy = extract_features(noisy_file)

    # Normalize
    norm_noisy = (noisy_feats - mean) / std

    # Predict
    enhanced_frames = model.predict(norm_noisy)
    enhanced_frames = (enhanced_frames * std) + mean
    mag = librosa.db_to_amplitude(enhanced_frames.T)

    # Reconstruct audio
    phase = np.angle(stft_noisy[:, :mag.shape[1]])
    enhanced_audio = apply_istft(mag, phase)
    enhanced_audio = butter_lowpass_filter(enhanced_audio)

    # Save
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    sf.write(output_path, enhanced_audio, SR)
    print(f"✅ Enhanced audio saved at: {output_path}")

    return None  # lite version skips metrics/spectrogram
