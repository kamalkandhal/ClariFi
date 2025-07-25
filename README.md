# ClariFi   
A real-time speech enhancement system powered by deep learning to denoise audio signals and improve speech intelligibility in noisy environments.

## Overview  
ClariFi leverages a Deep Neural Network (DNN) to perform speech enhancement using time-frequency masking. The model is trained on noisy-clean speech pairs to learn optimal spectral masks that filter out background noise while preserving vocal clarity.

## Features  
- Real-time audio denoising via a Flask web interface  
- Trained with log-magnitude STFT features  
- Evaluation using perceptual metrics like PESQ and STOI  
- Achieves significant improvement in speech clarity (PESQ ↑ 1.5+, STOI ↑ 0.3)  
- Designed to be lightweight and fast enough for practical deployment  

## Tech Stack  
- Python, Flask  
- TensorFlow / Keras  
- Librosa, NumPy, SciPy  
- HTML/CSS (for basic UI)  
- Deployment: Railway  

##  Project Structure  
<img width="547" height="352" alt="image" src="https://github.com/user-attachments/assets/1c41e25f-bff6-4459-ac2c-798e06e2c2f1" />


## Learnings  
- Designed and trained a DNN for regression-based speech mask prediction  
- Hands-on experience with perceptual evaluation metrics (PESQ, STOI)  
- Built a complete ML pipeline from data preprocessing to deployment

