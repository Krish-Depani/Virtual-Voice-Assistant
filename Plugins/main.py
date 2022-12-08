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
from threading import Thread
from Plugins import API_functionalities, speak

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

def main(query):
    intent_response = chat(query)
    intent = intent_response['intent']
    response = intent_response['response']
    if intent == "joke":
        API_functionalities.get_joke()
    elif intent == "news":
        API_functionalities.get_news()
    elif intent == "ip":
        API_functionalities.get_ip()
            #speak.speak(ip)


if __name__ == "__main__":
    try:
        Thread(target=listen_audio()).start()
    except:
        pass
'''
try:
    listen_audio()
except KeyboardInterrupt or RuntimeError:
    pass
    '''