import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 185)

def speak(text):
    print(text)
    try:
        engine.say(text)
        engine.runAndWait()
    except KeyboardInterrupt:
        return
