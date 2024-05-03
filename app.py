from flask import Flask, request, jsonify, render_template, send_file
import whisper
import os
import torch
from groq_agent import Agent
import subprocess

app = Flask(__name__)
agent = Agent()

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

@app.route('/agentResponse', methods=['POST'])
def handle_transcription():
    try:
        transcription = request.json.get('transcription')
        # Get response from LLM (Agent)
        agentResponse = agent.respond_to_text(transcription)
        
        return jsonify({"agentResponse": agentResponse})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/speak', methods=['POST'])
def speak():
    try:
        text = request.json.get('text')
        voice = request.json.get('voice', 'ap')  # default voice is 'ap'
        output_path = "output.wav"
        
        # Run Mimic 3 to generate speech from text
        command = ["mimic3", "-t", text, "-voice", voice, "-o", output_path]
        result = subprocess.run(command, capture_output=True, text=True)
        
        if result.returncode != 0:
            raise Exception("Mimic 3 TTS failed:", result.stderr)
        
        return send_file(output_path, mimetype="audio/wav")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)