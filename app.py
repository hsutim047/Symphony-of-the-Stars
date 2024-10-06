from flask import Flask, render_template, request
from PIL import Image

from util import img2textmusic

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    # Get the uploaded image file
    file = request.files['image']

    # Process the image (e.g., resize, convert to grayscale)
    img = Image.open(file)
    img = img.resize((256, 256))  # Adjust the size as needed

    text, img, music = img2textmusic(img)

    # Generate output text and image data

    return render_template('result.html', output_text=text, audio_data=music)

