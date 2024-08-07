import speech_recognition as sr

def recognize_speech_from_mic():
    # Initialize recognizer class (for recognizing the speech)
    recognizer = sr.Recognizer()
    
    # Reading Microphone as source
    # Listening the speech and store in audio_text variable
    with sr.Microphone() as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening...")
        audio_text = recognizer.listen(source)
        print("Recognizing...")
        
        try:
            # Recognize speech using Google Web Speech API
            text = recognizer.recognize_google(audio_text)
            print("You said: {}".format(text))
            return text
        except sr.UnknownValueError:
            print("Sorry, I did not get that")
            return None
        except sr.RequestError:
            print("Sorry, my speech service is down")
            return None

if __name__ == "__main__":
    text = recognize_speech_from_mic()
    if text:
        print(f"Recognized Text: {text}")
    else:
        print("Failed to recognize speech.")
