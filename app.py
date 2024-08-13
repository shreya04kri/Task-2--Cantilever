import os
import cv2
import pytesseract
from flask import Flask, request, render_template, redirect, url_for, flash
from PIL import Image
import pyperclip

# Configure the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Adjust this path if needed

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.secret_key = 'supersecretkey'  # Required for flash messages

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def preprocess_image(image_path, brightness=1.0, contrast=1.0, threshold=127):
    # Load the image using OpenCV
    image = cv2.imread(image_path)
    
    if image is None:
        raise ValueError(f"Failed to load image at {image_path}")

    # Adjust brightness and contrast
    adjusted_image = cv2.convertScaleAbs(image, alpha=contrast, beta=int(100 * (brightness - 1)))

    # Convert the image to grayscale
    gray_image = cv2.cvtColor(adjusted_image, cv2.COLOR_BGR2GRAY)

    # Apply thresholding
    _, processed_image = cv2.threshold(gray_image, threshold, 255, cv2.THRESH_BINARY)

    return processed_image

def extract_text_from_image(image_path, brightness, contrast, threshold):
    processed_image = preprocess_image(image_path, brightness, contrast, threshold)
    pil_image = Image.fromarray(processed_image)
    custom_config = '--psm 6 --oem 1 -l eng'
    text = pytesseract.image_to_string(pil_image, config=custom_config)
    return text

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        brightness = float(request.form.get('brightness', 1.0))
        contrast = float(request.form.get('contrast', 1.0))
        threshold = int(request.form.get('threshold', 127))

        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

            try:
                extracted_text = extract_text_from_image(file_path, brightness, contrast, threshold)
                return render_template('result.html', text=extracted_text, filename=file.filename)
            except ValueError as e:
                flash(str(e))
                return redirect(request.url)

    return render_template('upload.html')

@app.route('/copy', methods=['POST'])
def copy_text():
    text = request.form.get('text')
    pyperclip.copy(text)
    return 'Text copied to clipboard!'

if __name__ == '__main__':
    app.run(debug=True)
