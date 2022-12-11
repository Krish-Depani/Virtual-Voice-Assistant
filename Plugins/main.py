import json
import os
import logging
import pyttsx3
logging.disable(logging.WARNING)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from keras_preprocessing.sequence import pad_sequences
import numpy as np
from keras.models import load_model
from pickle import load
import speech_recognition as sr
import re
from threading import Thread
import sys
sys.path.insert(0, "C:\\Users\\Hp\\PycharmProjects\\Virtual_Voice_Assistant")
from image_generation import generate_image
from gmail import send_email
from API_functionalities import *
from system_operations import *
from browsing_functionalities import *

recognizer = sr.Recognizer()

engine = pyttsx3.init()
engine.setProperty('rate', 185)

sys_ops = SystemTasks()
tab_ops = TabOpt()
win_ops = WindowOpt()

with open("..\\Data\\intents.json") as file:
    data = json.load(file)

# load trained model
model = load_model('..\\Data\\chat_model')

# load tokenizer object
with open('..\\Data\\tokenizer.pickle', 'rb') as handle:
    tokenizer = load(handle)

# load label encoder object
with open('..\\Data\\label_encoder.pickle', 'rb') as enc:
    lbl_encoder = load(enc)

def speak(text):
    print(text)
    try:
        engine.say(text)
        engine.runAndWait()
    except KeyboardInterrupt or RuntimeError:
        return

def chat(text):
    # parameters
    max_len = 20
    while True:
        result = model.predict(pad_sequences(tokenizer.texts_to_sequences([text]),
                                                                          truncating='post', maxlen=max_len), verbose=False)
        intent = lbl_encoder.inverse_transform([np.argmax(result)])[0]
        return intent

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
        intent = chat(query)
        done = False
        if "google" and "search" in query or "google" and "how to" in query or "google" in query:
            googleSearch(query)
            return
        elif "youtube" and "search" in query or "play" in query or "how to" and "youtube" in query:
            youtube(query)
            return
        if intent == "joke":
            joke = get_joke()
            speak(joke)
            done = True
        elif intent == "news":
            news = get_news()
            speak(news)
            done = True
        elif intent == "ip":
            ip = get_ip()
            speak(ip)
            done = True
        elif intent == "movies":
            speak("Some of the latest popular movies are as follows :")
            get_popular_movies()
            done = True
        elif intent == "tv_series":
            speak("Some of the latest popular tv series are as follows :")
            get_popular_tvseries()
            done = True
        elif intent == "weather":
            city = re.search(r"(in|of|for) ([a-zA-Z]*)", query)
            if city:
                city = city[2]
                weather = get_weather(city)
                speak(weather)
            else:
                weather = get_weather()
                speak(weather)
            done = True
        elif intent == "internet_speedtest":
            speak("Getting your internet speed, this may take some time")
            speed = get_speedtest()
            speak(speed)
            done = True
        elif intent == "system_stats":
            stats = system_stats()
            speak(stats)
            done = True
        elif intent == "image_generation":
            speak("what kind of image you want to generate?")
            text = record()
            speak("Generating image please wait..")
            generate_image(text)
            done = True
        elif intent == "system_info":
            info = systemInfo()
            speak(info)
            done = True
        elif intent == "email":
            speak("Type the receiver id : ")
            receiver_id = input()
            speak("Tell the subject of email")
            subject = record()
            speak("tell the body of email")
            body = record()
            success = send_email(receiver_id, subject, body)
            if success == "SENT":
                speak('Email sent successfully')
            else:
                speak("Error occurred while sending email")
            done = True
        elif intent == "select_text":
            sys_ops.select()
            done = True
        elif intent == "copy_text":
            sys_ops.copy()
            done = True
        elif intent == "paste_text":
            sys_ops.paste()
            done = True
        elif intent == "delete_text":
            sys_ops.delete()
            done = True
        elif intent == "new_file":
            sys_ops.new_file()
            done = True
        elif intent == "switch_tab":
            tab_ops.switchTab()
            done = True
        elif intent == "close_tab":
            tab_ops.closeTab()
            done = True
        elif intent == "new_tab":
            tab_ops.newTab()
            done = True
        elif intent == "close_window":
            win_ops.closeWindow()
            done = True
        elif intent == "switch_window":
            win_ops.switchWindow()
            done = True
        elif intent == "minimize_window":
            win_ops.minimizeWindow()
            done = True
        elif intent == "maximize_window":
            win_ops.maximizeWindow()
            done = True
        elif intent == "screenshot":
            win_ops.Screen_Shot()
            done = True
        elif intent == "stopwatch":
            pass
        elif intent == "wikipedia":
            description = tell_me_about(query)
            speak(description)
            done = True
        elif intent == "math":
            answer = get_general_response(query)
            speak(answer)
            done = True
        elif intent == "open_website":
            open_specified_website(query)
            done = True
        elif intent == "open_app":
            open_app(query)
            done = True
        elif intent == "note":
            speak("what would you like to take down?")
            note = record()
            take_note(note)
        elif intent == "exit":
            exit(0)
        if not done:
            answer = get_general_response(query, intent)
            if answer:
                speak(answer)
            else:
                speak("Sorry, not able to answer your query")
        return


if __name__ == "__main__":
    try:
        Thread(target=listen_audio()).start()
    except:
        pass

'''
if __name__ == "__main__":
    try:
        listen_audio()
    except KeyboardInterrupt or RuntimeError:
        pass
'''
