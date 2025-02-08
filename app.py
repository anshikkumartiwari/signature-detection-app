from flask import Flask, request, render_template, send_file, jsonify
import os
from signDetect import detectandMark

# Ensure directories exist
if not os.path.exists('uploads'):
    os.makedirs('uploads')
if not os.path.exists('processed'):
    os.makedirs('processed')

app = Flask(__name__)

processing_info = ""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['image']
        if file:
            input_path = os.path.join('uploads', file.filename)
            output_path = os.path.join('processed', f"processed_{file.filename}")
            file.save(input_path)
            detectandMark(input_path, output_path)
            return render_template('index.html', processed_image=f"processed_{file.filename}")
    return render_template('index.html', processed_image=None)

@app.route('/processed/<filename>')
def processed_image(filename):
    return send_file(os.path.join('processed', filename))

@app.route('/process', methods=['POST'])
def process_image():
    global processing_info
    try:
        file = request.files['image']
        if file:
            input_path = os.path.join('uploads', file.filename)
            output_path = os.path.join('processed', f"processed_{file.filename}")
            file.save(input_path)
            processing_info = detectandMark(input_path, output_path)
            return send_file(output_path)
        return "No file uploaded", 400
    except Exception as e:
        app.logger.error(f"Error processing image: {e}")
        return "Internal Server Error", 500

@app.route('/process_info')
def process_info():
    global processing_info
    return processing_info

if __name__ == '__main__':
    app.run(debug=True)