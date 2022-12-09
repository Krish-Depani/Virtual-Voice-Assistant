import json
import os
import logging
logging.disable(logging.WARNING)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from keras_preprocessing.sequence import pad_sequences
import numpy as np
from keras.models import load_model
from pickle import load
import speech_recognition as sr
import re
from threading import Thread
from speak import speak
from API_functionalities import *
from system_operations import *
from browsing_functionalities import *

recognizer = sr.Recognizer()

with open("../Data/intents.json") as file:
    data = json.load(file)

# load trained model
model = load_model('..\\Data\\chat_model')

# load tokenizer object
with open('..\\Data\\tokenizer.pickle', 'rb') as handle:
    tokenizer = load(handle)

# load label encoder object
with open('..\\Data\\label_encoder.pickle', 'rb') as enc:
    lbl_encoder = load(enc)

def chat(text):
    # parameters
    max_len = 20
    intents = {"intent": "", "response": ""}
    while True:
        result = model.predict(pad_sequences(tokenizer.texts_to_sequences([text]),
                                                                          truncating='post', maxlen=max_len), verbose=False)
        tag = lbl_encoder.inverse_transform([np.argmax(result)])[0]

        for i in data['intents']:
            if i['tag'] == tag:
                intents["intent"] = tag
                intents["response"] = np.random.choice(i['responses'])
                return intents

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
                main(response)
    except KeyboardInterrupt:
        return

'''
def main(response):
    while True:
        ip = input("Enter input : ")
        print(chat(ip))

main("abc")
'''

def main(query):
    intent_response = chat(query)
    intent = intent_response['intent']
    response = intent_response['response']
    if intent == "joke":
        speak(response)
        get_joke()
    elif intent == "news":
        speak(response)
        get_news()
    elif intent == "ip":
        speak(response)
        get_ip()
    elif intent == "movies":
        speak(response)
        get_popular_movies()
    elif intent == "tv_series":
        speak(response)
        get_popular_tvseries()
    elif intent == "weather":
        speak(response)
        city = re.search(r"(in|of|for) ([a-zA-Z]*)", query)
        if city:
            city = city[2]
            get_weather(city)
        else:
            get_weather()
    elif intent == "internet_speedtest":
        speak(response)
        get_speedtest()
    elif intent == "system_stats":
        speak(response)
        system_stats()
    elif intent == "image_generation":
        pass
    elif intent == "system_info":
        pass
    elif intent == "email":
        pass
    elif intent == "select_text":
        pass
    elif intent == "copy_text":
        pass
    elif intent == "paste_text":
        pass
    elif intent == "delete_text":
        pass
    elif intent == "new_file":
        pass
    elif intent == "switch_tab":
        pass
    elif intent == "close_tab":
        pass
    elif intent == "new_tab":
        pass
    elif intent == "close_window":
        pass
    elif intent == "switch_window":
        pass
    elif intent == "minimize_window":
        pass
    elif intent == "maximize_window":
        pass
    elif intent == "screenshot":
        pass
    elif intent == "stopwatch":
        pass
    elif intent == "wikipedia":
        pass
    elif intent == "math":
        pass
    elif intent == "open_website":
        pass
    elif intent == "open_app":
        pass


'''
if __name__ == "__main__":
    try:
        Thread(target=listen_audio()).start()
    except:
        pass
'''
'''
try:
    listen_audio()
except KeyboardInterrupt or RuntimeError:
    pass
    '''