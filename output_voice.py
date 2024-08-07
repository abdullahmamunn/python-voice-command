import speech_recognition as sr
from gtts import gTTS
import pygame
import os

def recognize_speech_from_mic():
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening...")
        audio_text = recognizer.listen(source)
        print("Recognizing...")
        
        try:
            text = recognizer.recognize_google(audio_text)
            print("You said: {}".format(text))
            return text
        except sr.UnknownValueError:
            print("Sorry, I did not get that")
            return None
        except sr.RequestError:
            print("Sorry, my speech service is down")
            return None

def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    filename = "output.mp3"
    tts.save(filename)
    
    # Initialize pygame mixer
    pygame.mixer.init()
    # Load and play the audio file
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    
    # Wait for the audio to finish playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    os.remove(filename)

if __name__ == "__main__":
    text = recognize_speech_from_mic()
    if text:
        print(f"Recognized Text: {text}")
        text_to_speech(text)
    else:
        print("Failed to recognize speech.")
