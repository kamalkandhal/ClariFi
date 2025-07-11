import numpy as np
from pesq import pesq
from pystoi import stoi
from scipy.signal import lfilter

from utils.audio_utils import SR

def segmental_snr(clean, enhanced, frame_len=256, eps=1e-8):
    clean = np.array(clean)
    enhanced = np.array(enhanced)
    num_frames = int(len(clean) / frame_len)
    segsnr = []

    for i in range(num_frames):
        start = i * frame_len
        end = start + frame_len
        c = clean[start:end]
        e = enhanced[start:end]
        noise = c - e
        if np.sum(c ** 2) < eps:
            continue
        segsnr.append(10 * np.log10(np.sum(c ** 2) / (np.sum(noise ** 2) + eps)))

    return np.mean(segsnr) if segsnr else 0.0

def compute_pesq(clean, enhanced):
    return pesq(SR, clean, enhanced, 'wb')

def compute_stoi(clean, enhanced):
    return stoi(clean, enhanced, SR, extended=False)
