from flask import Flask
from flask import render_template, request, jsonify, send_file
import io
from gan import RetinaGenerator

from PIL import Image
import numpy as np

app = Flask(__name__)
generator = RetinaGenerator()

@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html', error=False)

@app.route('/loadmodel', methods=['POST'])
def loadmodel():
    try:
        generator.load_model()
        return jsonify({'successs': 'Model loaded'})
    except:
        return jsonify({'error': 'Something went wrong'})

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    result = generator.generate(file)
    img = Image.fromarray(result.astype('uint8'))
    file_obj = io.BytesIO()
    img.save(file_obj, 'PNG')
    file_obj.seek(0)
    return send_file(
        file_obj,
        mimetype='image/png'
    )

if __name__ == '__main__':
    app.run(debug=True, port=5001)
