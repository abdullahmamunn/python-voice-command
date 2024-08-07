import speech_recognition as sr
from gtts import gTTS
import pygame
import io
import time

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
    with io.BytesIO() as audio_file:
        tts.write_to_fp(audio_file)
        audio_file.seek(0)
        pygame.mixer.init()
        pygame.mixer.music.load(audio_file, 'mp3')
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.quit()

if __name__ == "__main__":
    try:
        while True:
            text = recognize_speech_from_mic()
            if text:
                print(f"Recognized Text: {text}")
                text_to_speech(text)
            else:
                print("Failed to recognize speech.")
            # Small delay to avoid rapid iterations
            time.sleep(1)
    except KeyboardInterrupt:
        print("Program terminated by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        pygame.quit()
