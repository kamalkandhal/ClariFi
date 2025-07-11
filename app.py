import os
import gc
import traceback
from flask import Flask, render_template, request, url_for
from werkzeug.utils import secure_filename
from enhance import enhance_audio

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"  # Force CPU usage

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'static/uploads'
ENHANCED_FOLDER = 'static/enhanced'
ALLOWED_EXTENSIONS = {'wav'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ENHANCED_FOLDER'] = ENHANCED_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(ENHANCED_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health')
def health():
    return "OK", 200

@app.route('/enhance', methods=['POST'])
def enhance():
    try:
        if 'audiofile' not in request.files:
            return "❌ No file uploaded", 400

        file = request.files['audiofile']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            output_path = os.path.join(app.config['ENHANCED_FOLDER'], f'enhanced_{filename}')

            # # Optional: Reject large files (limit to ~15 seconds)
            # file.seek(0, os.SEEK_END)
            # if file.tell() > 500000:  # ~500KB = ~15s mono @ 16kHz
            #     return "❌ File too large. Limit to 15 seconds.", 400
            # file.seek(0)

            file.save(input_path)

            # Enhance
            enhance_audio(input_path, output_path)

            gc.collect()  # Clean memory

            return render_template('result.html',
                original_file=url_for('static', filename=f'uploads/{filename}'),
                enhanced_file=url_for('static', filename=f'enhanced/enhanced_{filename}')
            )

        return "❌ Invalid file type", 400

    except Exception as e:
        traceback.print_exc()
        return f"⚠️ Enhancement failed: {str(e)}", 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
