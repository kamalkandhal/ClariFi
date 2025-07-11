import numpy as np  
import scipy.signal  
import librosa  

SR = 16000               # Sampling rate  
N_FFT = 512              # FFT window size  
HOP_LENGTH = 128         # Hop length  
WINDOW_TYPE = 'hann'     # Window function  

def stft(y):  
    return librosa.stft(y, n_fft=N_FFT, hop_length=HOP_LENGTH, window=WINDOW_TYPE)  

def istft(mag, phase):  
    stft_matrix = mag * np.exp(1j * phase)  
    return librosa.istft(stft_matrix, hop_length=HOP_LENGTH, window=WINDOW_TYPE)  

def apply_istft(mag, phase):  
    """Apply inverse STFT to reconstruct time-domain signal from magnitude and phase."""  
    return istft(mag, phase)  

def butter_lowpass_filter(data, cutoff=8000, fs=SR, order=6):  
    nyq = 0.5 * fs  
    normal_cutoff = cutoff / nyq  
    
       # Ensure cutoff is valid
    if not 0 < normal_cutoff < 1:
        print("⚠️ Skipping lowpass filter: invalid cutoff frequency.")
        return data
    
    b, a = scipy.signal.butter(order, normal_cutoff, btype='low', analog=False)  
    y = scipy.signal.filtfilt(b, a, data)  
    return y  
