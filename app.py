from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
from model import load_model, enhance_speech
from audio_utils import preprocess_audio, save_audio, calculate_pesq

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ENHANCED_FOLDER'] = 'static/enhanced'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['ENHANCED_FOLDER'], exist_ok=True)

model = load_model()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/enhance', methods=['POST'])
def enhance():
    if 'audio_file' not in request.files:
        return render_template('index.html', error="❌ No file uploaded")

    file = request.files['audio_file']
    if file.filename == '':
        return render_template('index.html', error="❌ No file selected")

    filename = secure_filename(file.filename)
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(input_path)

    # Preprocess the input
    noisy_audio, sr = preprocess_audio(input_path)

    # Enhance the speech using the model
    enhanced_audio = enhance_speech(model, noisy_audio)

    # Save enhanced audio
    enhanced_filename = f"enhanced_{filename}"
    enhanced_path = os.path.join(app.config['ENHANCED_FOLDER'], enhanced_filename)
    save_audio(enhanced_path, enhanced_audio, sr)

    # Calculate PESQ
    try:
        pesq_score = calculate_pesq(input_path, enhanced_path, sr)
    except Exception as e:
        pesq_score = None
        print("PESQ calculation failed:", e)

    return render_template(
        'result.html',
        original_file='/' + input_path,
        enhanced_file='/' + enhanced_path,
        pesq_score=pesq_score
    )

if __name__ == '__main__':
    app.run(debug=True)
