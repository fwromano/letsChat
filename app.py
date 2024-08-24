from flask import Flask, request, jsonify, render_template, send_file
import whisper
import os
import torch
from local_agent import Agent as LocalAgent
from groq_agent import Agent as GroqAgent
from openai_agent import Agent as OpenAIAgent
import subprocess
import tempfile

#set up
# Agents
# default is local agent on ollama
# options are Local, groq, claude, and openai
preferred_agent = "openai"
match preferred_agent:
    case "local":
        Agent = LocalAgent
    case "groq":
        Agent = GroqAgent
    case "openai":
        Agent = OpenAIAgent
    # case "anthropic":     todo
    #     Agent = OpenAIAgent
    case _:
        Agent = LocalAgent
    
# Voice 
# options are: mimic, macbook, open ai, and eleven labs?
preffered_voice = "macbook"
match preffered_voice:
    # case "mimic":
    #     voice = "mimic"
    case "macbook":
        voice = "macbook"
    # case "openai":
    #     voice = "openai"
    # case "eleven":
    #     voice = "eleven"
    case _:
        voice = "macbook"


    

app = Flask(__name__)
agent = Agent()

# Check if GPU is available and load appropriate model
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
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400
    
    audio_file = request.files['audio']
    if audio_file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    audio_path = os.path.join(app.config['UPLOAD_FOLDER'], "temp.wav")
    audio_file.save(audio_path)
    
    try:
        result = model.transcribe(audio_path)
        os.remove(audio_path)  # Clean up the temporary file
        return jsonify({"text": result['text']})
    except Exception as e:
        os.remove(audio_path)  # Ensure cleanup even if transcription fails
        return jsonify({"error": str(e)}), 500

@app.route('/agentResponse', methods=['POST'])
def handle_transcription():
    transcription = request.json.get('transcription')
    if not transcription:
        return jsonify({"error": "No transcription provided"}), 400
    
    try:
        agent_response = agent.respond_to_text(transcription)
        print(agent_response)
        return jsonify({"agentResponse": agent_response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/speak', methods=['POST'])
def speak():
    text = request.json.get('text')
    if not text:
        return jsonify({"error": "No text provided"}), 400

    # default native mac voice
    temp_path= None
    try:
        # Create a temporary file to store the audio
        with tempfile.NamedTemporaryFile(suffix='.aiff', delete=False) as temp_file:
            temp_path = temp_file.name

        # Use the 'say' command to generate speech
        command = ["say", "-o", temp_path, text]
        subprocess.run(command, check=True, capture_output=True, text=True)

        # Send the generated audio file
        return send_file(temp_path, mimetype="audio/aiff")

    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Text-to-speech failed: {e.stderr}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        # Clean up the temporary file
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)

if __name__ == '__main__':
    app.config['UPLOAD_FOLDER'] = 'uploads'
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)