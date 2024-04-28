# LetsChat

# Overview

This Speech Recognition application allows users to record audio through their web browser and send it to a Flask server for transcription. The application provides visual feedback during the recording and processing phases to enhance user interaction.

# Features

Audio recording via the browser.
Visual feedback during recording and processing.
Server-side audio processing for transcription.

# Setup Instructions

## 1. Fork and Clone the Repository

First, fork the repository to your GitHub account by clicking on the "Fork" button at the top right of this page. Then, clone the forked repository to your local machine:

```shell
git clone https://github.com/fwromano/letsChat.git
cd letsChat
```

## 2. Create a Virtual Environment

Set up a Python virtual environment to manage dependencies:

```shell
python3 -m venv ~/.venvs/speechenv
source ~/.venvs/speechenv/bin/activate
```

## 3. Install Dependencies

Install the required Python packages specified in requirements.txt:

```shell
pip install -r requirements.txt
```

## 4. Run the Flask Application

Start the Flask server to host the application:

```shell
python app.py
```

Open http://localhost:5000/ in your web browser to access the Speech Recognition application.

# Usage

- Start Recording: Click the "Start Listening" button to begin recording your speech through the microphone.
- Stop Recording: Click the "Stop Listening" button once you finish speaking. The audio will be sent to the server for processing.
- View Transcription: Wait for the transcription to appear on the webpage. During this time, the "Processing..." indicator will be visible.

# Additional Information

- Ensure your microphone settings are configured to allow web access.
- The application's transcription accuracy and performance depend on the backend setup for processing the audio data. Adjustments may be necessary based on the specific speech-to-text technology or API used.
