import speech_recognition as sr
from threading import Thread

recognizer = sr.Recognizer()
#recognizer.dynamic_energy_threshold = False
#recognizer.energy_threshold = 4000

def record():
    with sr.Microphone() as mic:
        recognizer.adjust_for_ambient_noise(mic)
        recognizer.dynamic_energy_threshold = True
        print("Listening...")
        audio = recognizer.listen(mic)
        try:
            text = recognizer.recognize_google(audio, language='us-in').lower()
        except:
            return None
    return text

def listen_audio():
    try:
        while True:
            response = record()
            if response is None:
                continue
            else:
                print(response)
    except KeyboardInterrupt:
        return

try:
    Thread(target=listen_audio()).start()
except:
    pass
