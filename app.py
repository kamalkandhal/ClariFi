from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
from enhance import enhance_audio

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
ENHANCED_FOLDER = "static/enhanced"
ALLOWED_EXTENSIONS = {'wav'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(ENHANCED_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Handle no file selected
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            original_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(original_path)

            # Enhance and get PESQ score
            enhanced_path, pesq_score = enhance_audio(original_path)

            if enhanced_path:
                return render_template(
                    'result.html',
                    original_file=original_path,
                    enhanced_file=enhanced_path,
                    pesq_score=pesq_score
                )
            else:
                return "Enhancement failed", 500

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
