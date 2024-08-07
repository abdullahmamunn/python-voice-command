import speech_recognition as sr
import openai

# Set your OpenAI API key
openai.api_key = 'YOUR_OPENAI_API_KEY'

def get_openai_response(prompt):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # Choose the model you want to use
            prompt=prompt,
            max_tokens=150  # Adjust as needed
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return None

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
            response_text = get_openai_response(text)
            return response_text
        except sr.UnknownValueError:
            print("Sorry, I did not get that")
            return None
        except sr.RequestError:
            print("Sorry, my speech service is down")
            return None
