import os
import json
import pyaudio
import vosk
from transformers import pipeline
from gtts import gTTS

# Initialize Vosk for Speech Recognition
vosk_model_path = "models/vosk-model-small-en-us-0.15"
if not os.path.exists(vosk_model_path):
    print(f"Please download the Vosk model and place it in {vosk_model_path}")
    exit(1)

model = vosk.Model(vosk_model_path)
recognizer = vosk.KaldiRecognizer(model, 16000)

# Initialize GPT-2 for NLP (Text Generation)
generator = pipeline('text-generation', model='gpt2')

def listen():
    # Start recording audio
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=4096)
    stream.start_stream()

    print("Listening...")

    while True:
        data = stream.read(4096)
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            text = json.loads(result).get('text', '')
            if text:
                print(f"You said: {text}")
                return text

def generate_response(prompt):
    response = generator(prompt, max_length=50, num_return_sequences=1)
    return response[0]['generated_text']

def speak(text):
    tts = gTTS(text=text, lang='en')
    tts.save("output.mp3")
    os.system("start output.mp3")  # This works on Windows. Use "afplay output.mp3" on Mac or "mpg321 output.mp3" on Linux.

def main():
    print("Voice Assistant is ready...")

    while True:
        user_input = listen()
        if user_input:
            response = generate_response(user_input)
            print(f"Assistant: {response}")
            speak(response)

if __name__ == "__main__":
    main()
