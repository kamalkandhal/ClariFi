import numpy as np
import scipy.signal
import librosa
# from pypesq import pesq
import soundfile as sf
from pesq import pesq


# Constants
SR = 16000               # Sampling Rate
N_FFT = 512              # FFT window size
HOP_LENGTH = 128         # Hop length
WINDOW_TYPE = 'hann'     # STFT window type

def stft(y):
    """
    Compute the Short-Time Fourier Transform (STFT) of an audio signal.

    Args:
        y (np.ndarray): Time-domain audio signal.

    Returns:
        np.ndarray: STFT complex matrix.
    """
    return librosa.stft(y, n_fft=N_FFT, hop_length=HOP_LENGTH, window=WINDOW_TYPE)

def istft(mag, phase):
    """
    Perform inverse STFT using magnitude and phase to reconstruct time-domain signal.

    Args:
        mag (np.ndarray): Magnitude spectrogram.
        phase (np.ndarray): Phase spectrogram.

    Returns:
        np.ndarray: Time-domain reconstructed signal.
    """
    stft_matrix = mag * np.exp(1j * phase)
    return librosa.istft(stft_matrix, hop_length=HOP_LENGTH, window=WINDOW_TYPE)

def apply_istft(mag, phase):
    """
    Wrapper for inverse STFT, used to reconstruct audio from predicted magnitudes and original phase.

    Args:
        mag (np.ndarray): Predicted magnitude spectrogram.
        phase (np.ndarray): Original phase spectrogram.

    Returns:
        np.ndarray: Reconstructed audio waveform.
    """
    return istft(mag, phase)

def butter_lowpass_filter(data, cutoff=8000, fs=SR, order=6):
    """
    Apply a low-pass Butterworth filter to remove high-frequency noise.

    Args:
        data (np.ndarray): Input audio signal.
        cutoff (float): Cutoff frequency (Hz).
        fs (int): Sampling rate (Hz).
        order (int): Filter order.

    Returns:
        np.ndarray: Filtered audio signal.
    """
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq

    # Validate cutoff frequency
    if not 0 < normal_cutoff < 1:
        print("⚠️ Skipping lowpass filter: invalid cutoff frequency.")
        return data

    b, a = scipy.signal.butter(order, normal_cutoff, btype='low', analog=False)
    return scipy.signal.filtfilt(b, a, data)

def calculate_pesq(ref_file, deg_file, sr=SR):
    """
    Calculate PESQ score between a reference and degraded audio file.

    Args:
        ref_file (str): Path to the reference (clean) audio file.
        deg_file (str): Path to the degraded (enhanced) audio file.
        sr (int): Sampling rate for PESQ.

    Returns:
        float: PESQ score.
    """
    ref, sr_ref = sf.read(ref_file)
    deg, sr_deg = sf.read(deg_file)

    if sr_ref != sr or sr_deg != sr:
        raise ValueError(f"Sample rates do not match expected {sr} Hz.")

    min_len = min(len(ref), len(deg))
    ref = ref[:min_len]
    deg = deg[:min_len]

    return pesq(sr, ref, deg, 'wb')  # 'wb' = wideband PESQ
