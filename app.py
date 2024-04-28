from flask import Flask, request, jsonify, render_template
import whisper
import os
import torch

app = Flask(__name__)

# Check if GPU is available
def get_model():
    if torch.cuda.is_available():
        print("Using GPU")
        return whisper.load_model("base", device="cuda")
    else:
        print("Using CPU")
        return whisper.load_model("small.en", device="cpu")

model = get_model()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    audio_file = request.files['audio']
    audio_path = "./temp.wav"
    audio_file.save(audio_path)
    
    result = model.transcribe(audio_path)
    os.remove(audio_path)  # Clean up the temporary file
    return jsonify({"text": result['text']})

if __name__ == '__main__':
    app.run(debug=True)
