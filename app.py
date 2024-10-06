from flask import Flask, render_template, request, send_file, session
import secrets
from PIL import Image
from util import img2textmusic
import os

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Generate a secure secret key


def generate_random_audio_path():
    random_filename = secrets.token_urlsafe(16) + '.wav'  # Adjust the length as needed
    return os.path.join('./wavs', random_filename)


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

    audio_path = generate_random_audio_path()
    text = img2textmusic(img, audio_file_path=audio_path)

    # Store the audio_path in the session
    session['audio_path'] = audio_path

    return render_template('result.html', output_text=text)


@app.route('/audio')
def serve_audio():
    audio_path = session.get('audio_path')
    if audio_path and os.path.exists(audio_path):
        return send_file(audio_path, mimetype="audio/wav")
    else:
        return "Audio file not found", 404


if __name__ == '__main__':
    app.run(debug=True)
