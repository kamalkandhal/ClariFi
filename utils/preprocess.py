import librosa
import numpy as np
from utils.audio_utils import WINDOW_TYPE, HOP_LENGTH, SR

def extract_features(filepath):
    y, sr = librosa.load(filepath, sr=SR)

    # Pad if audio is too short
    if len(y) < 512:
        y = np.pad(y, (0, 512 - len(y)))

    stft = librosa.stft(y, n_fft=512, hop_length=HOP_LENGTH, window=WINDOW_TYPE)
    magnitude = np.abs(stft)
    db_mag = librosa.amplitude_to_db(magnitude)
    db_mag = db_mag.T  # time-major

    return db_mag, y, stft
