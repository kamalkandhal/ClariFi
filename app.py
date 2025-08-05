from flask import Flask, render_template, request, send_file, url_for
import os
from werkzeug.utils import secure_filename
from enhance import enhance_audio  # ✅ Correct file used

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

# ✅ Uses 'audio_file' and sends correct variable names
@app.route('/upload', methods=['POST'])
def upload():
    if 'audio_file' not in request.files:
        return 'No file part'

    file = request.files['audio_file']
    if file.filename == '':
        return 'No selected file'

    filename = secure_filename(file.filename)
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    output_filename = f"enhanced_{filename}"
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)

    file.save(input_path)

    # Call enhance_audio from enhance.py
    enhance_audio(input_path, output_path)

    return render_template(
        'result.html',
        original_file='/' + input_path,
        enhanced_file='/' + output_path
    )

# ✅ /enhance now behaves like /upload (renders result.html instead of forcing download)
@app.route('/enhance', methods=['GET', 'POST'])
def enhance_endpoint():
    if request.method == 'GET':
        return "Enhance endpoint is live. Use POST with a file."

    if 'audio_file' not in request.files:
        return 'No file part', 400

    file = request.files['audio_file']
    if file.filename == '':
        return 'No selected file', 400

    filename = secure_filename(file.filename)
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    output_filename = f"enhanced_{filename}"
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)

    file.save(input_path)
    enhance_audio(input_path, output_path)

    # ✅ Render the comparison page like /upload
    return render_template(
        'result.html',
        original_file='/' + input_path,
        enhanced_file='/' + output_path
    )

@app.route('/download/<path:filename>')
def download_file(filename):
    return send_file(filename, as_attachment=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
